#!/usr/bin/env python3
"""Validate PaperScope AI Deep Reading v1.3 results.

Performs JSON Schema validation plus semantic invariant checks that are difficult to
express in JSON Schema alone. Exits 0 on success, 1 on errors. Warnings do not fail.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator
except Exception:  # pragma: no cover
    Draft202012Validator = None

NUM_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:%|s|ms)?")
PLACEHOLDER_PATTERNS = (
    "当前材料未说明",
    "当前材料无法说明",
    "current materials do not specify",
    "not specified",
    "unknown",
)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def walk_evidence_statements(obj: Any, path: str = "$") -> Iterable[tuple[str, dict[str, Any]]]:
    if isinstance(obj, dict):
        if {"text", "status", "evidence_refs", "support_strength"}.issubset(obj.keys()):
            yield path, obj
        for k, v in obj.items():
            yield from walk_evidence_statements(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_evidence_statements(v, f"{path}[{i}]")


def numeric_tokens(text: str) -> set[str]:
    return {m.group(0).lower() for m in NUM_RE.finditer(text or "")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("result", type=Path, help="deep-reading-result.json")
    ap.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "schemas" / "deep-reading-result.schema.json",
    )
    ap.add_argument("--strict-warnings", action="store_true", help="Treat warnings as errors")
    args = ap.parse_args()

    data = load_json(args.result)
    schema = load_json(args.schema)

    errors: list[str] = []
    warnings: list[str] = []

    if Draft202012Validator is None:
        warnings.append("jsonschema is unavailable; JSON Schema validation was skipped")
    else:
        validator = Draft202012Validator(schema)
        for e in sorted(validator.iter_errors(data), key=lambda x: list(x.absolute_path)):
            loc = "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in e.absolute_path)
            errors.append(f"schema {loc}: {e.message}")

    if data.get("schema_version") != "1.3":
        errors.append("schema_version must be 1.3")

    reading_mode = ((data.get("input") or {}).get("reading_mode"))

    for pi, paper in enumerate(data.get("papers") or []):
        base = f"$.papers[{pi}]"
        boundary = paper.get("source_boundary") or {}
        locator_mode = boundary.get("locator_mode")
        grade = boundary.get("evidence_grade")
        coverage = ((boundary.get("evidence_coverage") or {}).get("level"))
        context_mode = boundary.get("context_mode")

        evs = paper.get("evidence_refs") or []
        ev_map: dict[str, dict[str, Any]] = {}
        for i, ev in enumerate(evs):
            eid = ev.get("id")
            if eid in ev_map:
                errors.append(f"{base}.evidence_refs[{i}]: duplicate evidence id {eid}")
            if eid:
                ev_map[eid] = ev

            loc = ev.get("location") or {}
            if locator_mode == "structure_grounded" and loc.get("page") is not None:
                errors.append(f"{base}: structure_grounded forbids page locator on {eid}")
            if locator_mode == "source_limited":
                for k in ("page", "figure", "table", "equation"):
                    if loc.get(k) is not None:
                        errors.append(f"{base}: source_limited forbids {k} locator on {eid}")
            if ev.get("snippet") is not None and ev.get("verification_status") == "unavailable":
                warnings.append(f"{base}: {eid} has snippet but verification_status=unavailable")

        def require_refs(refs: Iterable[str], where: str) -> None:
            for ref in refs or []:
                if ref not in ev_map:
                    errors.append(f"{where}: unresolved evidence ref {ref}")

        # Evidence statements: status semantics and ref resolution
        for spath, st in walk_evidence_statements(paper, base):
            refs = st.get("evidence_refs") or []
            require_refs(refs, spath)
            status = st.get("status")
            strength = st.get("support_strength")
            text = (st.get("text") or "").strip()
            if status == "reported" and not refs:
                errors.append(f"{spath}: reported statement requires evidence_refs")
            if status == "unknown" and strength not in ("missing", "not_applicable"):
                warnings.append(f"{spath}: unknown statement should normally use missing/not_applicable support")
            if status == "unknown" and refs:
                warnings.append(f"{spath}: unknown statement has evidence refs; verify it is true non-establishment, not a misclassified supported statement")
            if status == "unknown" and len(text) > 160:
                warnings.append(f"{spath}: long detailed statement labeled unknown; likely status misuse")

        # Assumptions
        assumptions = ((paper.get("method_summary") or {}).get("assumptions") or [])
        assumption_map: dict[str, dict[str, Any]] = {}
        for i, a in enumerate(assumptions):
            aid = a.get("assumption_id")
            if aid in assumption_map:
                errors.append(f"{base}.method_summary.assumptions[{i}]: duplicate assumption id {aid}")
            if aid:
                assumption_map[aid] = a
            require_refs(a.get("evidence_refs") or [], f"{base}.method_summary.assumptions[{i}]")
            if a.get("risk_level") == "high":
                if not (a.get("failure_mode") or "").strip():
                    errors.append(f"{base}: high-risk assumption {aid} requires failure_mode")
                if not (a.get("testability") or "").strip():
                    warnings.append(f"{base}: high-risk assumption {aid} should include testability")

        fragile = ((paper.get("critical_review") or {}).get("fragile_assumptions") or [])
        fragile_ids = set()
        for i, fa in enumerate(fragile):
            aid = fa.get("assumption_id")
            fragile_ids.add(aid)
            if aid not in assumption_map:
                errors.append(f"{base}.critical_review.fragile_assumptions[{i}]: unknown assumption id {aid}")
            require_refs(fa.get("evidence_refs") or [], f"{base}.critical_review.fragile_assumptions[{i}]")
        for aid, a in assumption_map.items():
            if a.get("risk_level") == "high" and aid not in fragile_ids:
                errors.append(f"{base}: high-risk assumption {aid} missing from fragile_assumptions")

        # Author limitations must be reported
        for i, lim in enumerate(paper.get("author_acknowledged_limitations") or []):
            if lim.get("status") != "reported":
                errors.append(f"{base}.author_acknowledged_limitations[{i}]: must be status=reported")
            require_refs(lim.get("evidence_refs") or [], f"{base}.author_acknowledged_limitations[{i}]")

        # Claims
        claim_ids = set()
        core_strengths = []
        for i, c in enumerate(paper.get("claim_evidence") or []):
            cpath = f"{base}.claim_evidence[{i}]"
            cid = c.get("claim_id")
            if cid in claim_ids:
                errors.append(f"{cpath}: duplicate claim id {cid}")
            claim_ids.add(cid)
            refs = c.get("evidence_refs") or []
            require_refs(refs, cpath)
            claim = c.get("claim") or {}
            if claim.get("status") == "reported" and not refs:
                errors.append(f"{cpath}: reported claim requires evidence refs")
            strengthen = (c.get("what_would_strengthen_it") or "").strip().lower()
            if any(pat in strengthen for pat in PLACEHOLDER_PATTERNS):
                warnings.append(f"{cpath}: what_would_strengthen_it looks like a placeholder")
            if c.get("importance") == "core":
                core_strengths.append(c.get("paper_internal_support"))

            # Heuristic numeric grounding check
            claim_nums = numeric_tokens(claim.get("text") or "")
            if claim_nums and refs:
                source_text = " ".join(
                    ((ev_map.get(r) or {}).get("snippet") or "") + " " + ((ev_map.get(r) or {}).get("paraphrase") or "")
                    for r in refs
                )
                source_nums = numeric_tokens(source_text)
                missing_nums = claim_nums - source_nums
                # ignore common structural integers (shot/way/k values may be paraphrased elsewhere)
                if len(missing_nums) >= 2:
                    warnings.append(f"{cpath}: quantitative tokens not found in cited evidence: {sorted(missing_nums)}")

        audit = paper.get("evidence_audit") or {}
        overall = audit.get("paper_internal_support")
        if any(s in ("missing", "overclaimed") for s in core_strengths) and overall == "strong":
            errors.append(f"{base}: overall paper_internal_support cannot be strong with missing/overclaimed core claim")
        if any(s == "weak" for s in core_strengths) and overall == "strong":
            errors.append(f"{base}: overall paper_internal_support cannot be strong with weak core claim")

        judgment = paper.get("judgment_card") or {}
        jstrength = judgment.get("paper_internal_evidence_strength")
        if overall and jstrength and overall != jstrength:
            warnings.append(f"{base}: judgment strength ({jstrength}) differs from audit support ({overall})")

        rp = (judgment.get("reading_priority") or {}).get("level")
        if rp == "insufficient_evidence" and grade in ("E2_BODY_TEXT", "E3_BODY_PLUS_ARTIFACTS") and coverage == "sufficient" and overall in ("strong", "moderate"):
            warnings.append(f"{base}: insufficient_evidence reading priority conflicts with sufficient E2/E3 material and {overall} internal support")

        # Novelty
        novelty = paper.get("novelty_verification") or {}
        if context_mode == "paper_only" and novelty.get("field_novelty") is not None:
            errors.append(f"{base}: field_novelty must be null when context_mode=paper_only")

        # Open questions / reading guide completeness
        open_questions = paper.get("open_questions") or []
        if reading_mode in ("standard", "followup_mode") and grade in ("E2_BODY_TEXT", "E3_BODY_PLUS_ARTIFACTS") and not open_questions:
            warnings.append(f"{base}: standard/followup E2/E3 reading has no open questions")
        for i, q in enumerate(open_questions):
            require_refs(q.get("evidence_refs") or [], f"{base}.open_questions[{i}]")

        guide = paper.get("reading_guide") or {}
        if reading_mode == "standard" and grade in ("E2_BODY_TEXT", "E3_BODY_PLUS_ARTIFACTS") and not (guide.get("items") or []):
            warnings.append(f"{base}: standard E2/E3 reading has empty reading guide")
        for i, item in enumerate(guide.get("items") or []):
            require_refs(item.get("evidence_refs") or [], f"{base}.reading_guide.items[{i}]")

        # Contradictions
        cx_ids = set()
        for i, cx in enumerate(paper.get("contradictions") or []):
            cpath = f"{base}.contradictions[{i}]"
            cid = cx.get("contradiction_id")
            if cid in cx_ids:
                errors.append(f"{cpath}: duplicate contradiction id {cid}")
            cx_ids.add(cid)
            refs = cx.get("evidence_refs") or []
            require_refs(refs, cpath)
            if len(refs) < 2:
                errors.append(f"{cpath}: contradiction needs at least two evidence refs")

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors or (args.strict_warnings and warnings):
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
