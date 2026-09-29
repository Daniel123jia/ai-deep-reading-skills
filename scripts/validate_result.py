#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

try:
    import jsonschema
except Exception:  # pragma: no cover
    jsonschema = None

NUM_RE = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?%?(?:±\d+(?:\.\d+)?)?")
PLACEHOLDERS = (
    "当前材料未说明",
    "current materials do not specify",
    "not mentioned",
    "unknown",
    "tbd",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def walk(obj: Any, path: str = "$"):
    yield path, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")


def walk_evidence_statements(obj: Any, path: str = "$"):
    if isinstance(obj, dict):
        if {"text", "status", "evidence_refs", "support_strength"}.issubset(obj.keys()):
            yield path, obj
        for k, v in obj.items():
            yield from walk_evidence_statements(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_evidence_statements(v, f"{path}[{i}]")


def nums(text: str) -> set[str]:
    return {m.group(0).replace(" ", "") for m in NUM_RE.finditer(text or "")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate PaperScope AI Deep Reading v1.5 output")
    ap.add_argument("result")
    ap.add_argument("--schema", default=None)
    ap.add_argument("--strict-warnings", action="store_true")
    args = ap.parse_args()

    result_path = Path(args.result)
    schema_path = Path(args.schema) if args.schema else Path(__file__).resolve().parents[1] / "schemas" / "deep-reading-result.schema.json"
    data = load_json(result_path)
    schema = load_json(schema_path)

    errors: list[str] = []
    warnings: list[str] = []

    if jsonschema is not None:
        validator_cls = getattr(jsonschema, "Draft202012Validator", jsonschema.Draft7Validator)
        resolver = jsonschema.RefResolver(
            "#",
            schema,
            store={"": schema, "#": schema, schema.get("$id", ""): schema},
        )
        validator = validator_cls(schema, resolver=resolver)
        for e in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
            loc = "$" + "".join(f"[{p}]" if isinstance(p, int) else f".{p}" for p in e.absolute_path)
            errors.append(f"schema {loc}: {e.message}")
    else:
        warnings.append("jsonschema package unavailable; schema validation skipped")

    if data.get("schema_version") != "1.5":
        errors.append("schema_version must be 1.5")

    reading_mode = ((data.get("input") or {}).get("reading_mode"))

    for pi, paper in enumerate(data.get("papers") or []):
        base = f"$.papers[{pi}]"
        boundary = paper.get("source_boundary") or {}
        locator_mode = boundary.get("locator_mode")
        grade = boundary.get("evidence_grade")
        coverage_level = ((boundary.get("evidence_coverage") or {}).get("level"))
        context_mode = boundary.get("context_mode")

        # Evidence inventory
        evs = paper.get("evidence_refs") or []
        ev_map: dict[str, dict[str, Any]] = {}
        for i, ev in enumerate(evs):
            ep = f"{base}.evidence_refs[{i}]"
            eid = ev.get("id")
            if not eid:
                continue
            if eid in ev_map:
                errors.append(f"{ep}: duplicate evidence id {eid}")
            ev_map[eid] = ev
            loc = ev.get("location") or {}
            if locator_mode == "structure_grounded" and loc.get("page") is not None:
                errors.append(f"{ep}: structure_grounded forbids page locator")
            if locator_mode == "source_limited":
                for k in ("page", "figure", "table", "equation"):
                    if loc.get(k) is not None:
                        errors.append(f"{ep}: source_limited forbids {k} locator")
            if ev.get("snippet") is not None and ev.get("verification_status") == "unavailable":
                warnings.append(f"{ep}: snippet exists while verification_status=unavailable")

        def require_refs(refs: Iterable[str], where: str):
            for ref in refs or []:
                if ref not in ev_map:
                    errors.append(f"{where}: unresolved evidence ref {ref}")

        # All evidence statements
        for spath, st in walk_evidence_statements(paper, base):
            refs = st.get("evidence_refs") or []
            require_refs(refs, spath)
            status = st.get("status")
            strength = st.get("support_strength")
            text = (st.get("text") or "").strip()
            if status == "reported" and not refs:
                errors.append(f"{spath}: reported statement requires evidence_refs")
            if status == "unknown" and strength not in ("missing", "not_applicable"):
                warnings.append(f"{spath}: unknown should normally use missing/not_applicable support")
            if status == "unknown" and len(text) > 140:
                warnings.append(f"{spath}: detailed positive proposition labeled unknown; likely status misuse")

        # Claims
        claims = paper.get("claim_evidence") or []
        claim_map: dict[str, dict[str, Any]] = {}
        core_strengths = []
        for i, c in enumerate(claims):
            cp = f"{base}.claim_evidence[{i}]"
            cid = c.get("claim_id")
            if cid in claim_map:
                errors.append(f"{cp}: duplicate claim id {cid}")
            if cid:
                claim_map[cid] = c
            title = (c.get("claim_title") or "").strip()
            if len(title) < 3:
                errors.append(f"{cp}: claim_title must be descriptive")
            links = c.get("evidence_links") or []
            if not links:
                errors.append(f"{cp}: claim requires evidence_links")
            linked_ids = []
            direct_ids = []
            for j, link in enumerate(links):
                eid = link.get("evidence_id")
                linked_ids.append(eid)
                if eid not in ev_map:
                    errors.append(f"{cp}.evidence_links[{j}]: unresolved evidence ref {eid}")
                if link.get("relation") == "direct":
                    direct_ids.append(eid)
            if c.get("claim", {}).get("status") == "reported" and not linked_ids:
                errors.append(f"{cp}: reported claim requires evidence")
            strengthen = (c.get("what_would_strengthen_it") or "").strip().lower()
            if not strengthen:
                errors.append(f"{cp}: what_would_strengthen_it is empty")
            elif any(p.lower() in strengthen for p in PLACEHOLDERS):
                warnings.append(f"{cp}: what_would_strengthen_it looks like a placeholder")
            if c.get("paper_internal_support") == "strong" and not direct_ids:
                warnings.append(f"{cp}: strong claim has no direct evidence link")
            if c.get("importance") == "core":
                core_strengths.append(c.get("paper_internal_support"))

            # Numeric grounding heuristic: for quantitative claims, prefer direct evidence containing the numbers.
            claim_nums = nums((c.get("claim") or {}).get("text") or "")
            if claim_nums and direct_ids:
                source = " ".join(
                    ((ev_map.get(eid) or {}).get("snippet") or "") + " " + ((ev_map.get(eid) or {}).get("paraphrase") or "")
                    for eid in direct_ids
                )
                missing = claim_nums - nums(source)
                # one missing structural number (e.g. 5-way) can be harmless; 2+ is suspicious
                if len(missing) >= 2:
                    warnings.append(f"{cp}: quantitative tokens not found in direct evidence: {sorted(missing)}")

        # Backlinks evidence -> claims
        for eid, ev in ev_map.items():
            for cid in ev.get("supported_claim_ids") or []:
                if cid not in claim_map:
                    errors.append(f"{base}: evidence {eid} backlinks to nonexistent claim {cid}")
            # Every non-context/non-contradictory use should usually be backlinkable
        for cid, c in claim_map.items():
            for link in c.get("evidence_links") or []:
                eid = link.get("evidence_id")
                rel = link.get("relation")
                if eid in ev_map and rel in ("direct", "indirect"):
                    if cid not in (ev_map[eid].get("supported_claim_ids") or []):
                        warnings.append(f"{base}: evidence {eid} used by {cid} but supported_claim_ids lacks backlink")

        # Source coverage coherence
        matrix = boundary.get("coverage_matrix") or {}
        if grade in ("E2_BODY_TEXT", "E3_BODY_PLUS_ARTIFACTS"):
            body_status = ((matrix.get("body_text") or {}).get("status"))
            if body_status in ("missing", "not_checked"):
                errors.append(f"{base}: {grade} conflicts with coverage_matrix.body_text={body_status}")
        if grade == "E3_BODY_PLUS_ARTIFACTS":
            artifact_statuses = [((matrix.get(k) or {}).get("status")) for k in ("tables","figures","equations","appendix","supplement")]
            if not any(x in ("available", "partial") for x in artifact_statuses):
                warnings.append(f"{base}: E3 declared but coverage matrix shows no inspected artifacts")

        # Research gap
        gap = paper.get("research_gap") or {}
        for key in ("author_problem", "author_claimed_gap", "paperscope_bottleneck"):
            st = gap.get(key) or {}
            require_refs(st.get("evidence_refs") or [], f"{base}.research_gap.{key}")
        ga = gap.get("gap_assessment") or {}
        require_refs(ga.get("evidence_refs") or [], f"{base}.research_gap.gap_assessment")

        # Assumptions and fragile assumptions
        assumptions = ((paper.get("method_summary") or {}).get("assumptions") or [])
        assumption_map: dict[str, dict[str, Any]] = {}
        for i, a in enumerate(assumptions):
            apath = f"{base}.method_summary.assumptions[{i}]"
            aid = a.get("assumption_id")
            if aid in assumption_map:
                errors.append(f"{apath}: duplicate assumption id {aid}")
            if aid:
                assumption_map[aid] = a
            require_refs(a.get("evidence_refs") or [], apath)
            if a.get("risk_level") == "high":
                for field in ("why_needed", "failure_mode", "stress_test"):
                    if not (a.get(field) or "").strip():
                        errors.append(f"{apath}: high-risk assumption requires {field}")

        fragile = ((paper.get("critical_review") or {}).get("fragile_assumptions") or [])
        fragile_ids = set()
        for i, fa in enumerate(fragile):
            fp = f"{base}.critical_review.fragile_assumptions[{i}]"
            aid = fa.get("assumption_id")
            fragile_ids.add(aid)
            if aid not in assumption_map:
                errors.append(f"{fp}: unknown assumption id {aid}")
            require_refs(fa.get("evidence_refs") or [], fp)
        for aid, a in assumption_map.items():
            if a.get("risk_level") == "high" and aid not in fragile_ids:
                errors.append(f"{base}: high-risk assumption {aid} missing from fragile_assumptions")

        # Actionability: core weaknesses, open questions, research directions
        crit = paper.get("critical_review") or {}
        weakness_ids = set()
        for i, w in enumerate(crit.get("core_weaknesses") or []):
            wp = f"{base}.critical_review.core_weaknesses[{i}]"
            wid = w.get("weakness_id")
            if wid in weakness_ids:
                errors.append(f"{wp}: duplicate weakness id {wid}")
            if wid:
                weakness_ids.add(wid)
            require_refs(w.get("evidence_refs") or [], wp)
            for fld in ("why_it_matters", "potential_impact", "suggested_validation"):
                val = (w.get(fld) or "").strip().lower()
                if not val:
                    errors.append(f"{wp}.{fld}: must be substantive")
                elif any(p.lower() in val for p in PLACEHOLDERS):
                    errors.append(f"{wp}.{fld}: placeholder is not allowed")
            for cid in w.get("related_claim_ids") or []:
                if cid not in claim_map:
                    errors.append(f"{wp}: related claim {cid} does not exist")
            for aid in w.get("related_assumption_ids") or []:
                if aid not in assumption_map:
                    errors.append(f"{wp}: related assumption {aid} does not exist")

        for i, q in enumerate(paper.get("open_questions") or []):
            qp = f"{base}.open_questions[{i}]"
            require_refs(q.get("evidence_refs") or [], qp)
            for fld in ("why_it_matters", "suggested_validation"):
                val = (q.get(fld) or "").strip().lower()
                if not val:
                    errors.append(f"{qp}.{fld}: must be substantive")
                elif any(p.lower() in val for p in PLACEHOLDERS):
                    errors.append(f"{qp}.{fld}: placeholder is not allowed")

        for i, rd in enumerate(paper.get("research_directions") or []):
            rdp = f"{base}.research_directions[{i}]"
            require_refs(rd.get("evidence_refs") or [], rdp)
            for wid in rd.get("related_weakness_ids") or []:
                if wid not in weakness_ids:
                    errors.append(f"{rdp}: related weakness {wid} does not exist")
            for fld in ("target_problem", "rationale", "validation_focus", "boundary_note"):
                val = (rd.get(fld) or "").strip().lower()
                if not val:
                    errors.append(f"{rdp}.{fld}: must be substantive")
                elif any(p.lower() in val for p in PLACEHOLDERS):
                    errors.append(f"{rdp}.{fld}: placeholder is not allowed")

        # Standard/reviewer/followup readings should be useful for critique when E2/E3 is available.
        if reading_mode in ("standard", "reviewer_mode", "followup_mode") and grade in ("E2_BODY_TEXT", "E3_BODY_PLUS_ARTIFACTS"):
            if not (crit.get("core_weaknesses") or []):
                warnings.append(f"{base}: no core_weaknesses produced despite body-text evidence")
        if reading_mode in ("standard", "followup_mode") and grade in ("E2_BODY_TEXT", "E3_BODY_PLUS_ARTIFACTS"):
            if not (paper.get("open_questions") or []):
                warnings.append(f"{base}: no open_questions produced despite body-text evidence")
            if not (paper.get("research_directions") or []):
                warnings.append(f"{base}: no bounded research_directions produced despite body-text evidence")

        # Experiments
        ex_ids = set()
        for i, ex in enumerate(paper.get("experiments") or []):
            xp = f"{base}.experiments[{i}]"
            xid = ex.get("experiment_id")
            if xid in ex_ids:
                errors.append(f"{xp}: duplicate experiment id {xid}")
            ex_ids.add(xid)
            require_refs(ex.get("evidence_refs") or [], xp)
            result_nums = nums(ex.get("result") or "")
            if result_nums:
                source = " ".join(
                    ((ev_map.get(eid) or {}).get("snippet") or "") + " " + ((ev_map.get(eid) or {}).get("paraphrase") or "")
                    for eid in ex.get("evidence_refs") or []
                )
                if len(result_nums - nums(source)) >= 2:
                    warnings.append(f"{xp}: experiment numeric result not well grounded in linked evidence")

        # Author limitations must be reported
        for i, lim in enumerate(paper.get("author_acknowledged_limitations") or []):
            lp = f"{base}.author_acknowledged_limitations[{i}]"
            if lim.get("status") != "reported":
                errors.append(f"{lp}: author limitation must be status=reported")
            require_refs(lim.get("evidence_refs") or [], lp)

        # Novelty boundary
        novelty = paper.get("novelty_verification") or {}
        if context_mode == "paper_only" and novelty.get("field_novelty") is not None:
            errors.append(f"{base}: field_novelty must be null when context_mode=paper_only")

        # Evidence audit consistency
        audit = paper.get("evidence_audit") or {}
        overall = audit.get("paper_internal_support")
        if any(s in ("missing", "overclaimed") for s in core_strengths) and overall == "strong":
            errors.append(f"{base}: overall support cannot be strong with missing/overclaimed core claim")
        if any(s == "weak" for s in core_strengths) and overall == "strong":
            errors.append(f"{base}: overall support cannot be strong with weak core claim")

        # Open questions
        oq = paper.get("open_questions") or []
        if reading_mode in ("standard", "followup_mode") and grade in ("E2_BODY_TEXT","E3_BODY_PLUS_ARTIFACTS") and not oq:
            warnings.append(f"{base}: E2/E3 standard/followup report has no open questions")
        for i, q in enumerate(oq):
            require_refs(q.get("evidence_refs") or [], f"{base}.open_questions[{i}]")
            if not (q.get("suggested_validation") or "").strip():
                errors.append(f"{base}.open_questions[{i}]: suggested_validation required")

        # Reading guide
        guide = paper.get("reading_guide") or {}
        items = guide.get("items") or []
        path = guide.get("twenty_minute_path") or []
        if reading_mode == "standard" and grade in ("E2_BODY_TEXT","E3_BODY_PLUS_ARTIFACTS"):
            if not items:
                warnings.append(f"{base}: standard E2/E3 report has empty reading guide")
            if not path:
                warnings.append(f"{base}: standard E2/E3 report has empty 20-minute path")
        for i, item in enumerate(items):
            require_refs(item.get("evidence_refs") or [], f"{base}.reading_guide.items[{i}]")
        for i, step in enumerate(path):
            require_refs(step.get("evidence_refs") or [], f"{base}.reading_guide.twenty_minute_path[{i}]")

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
                errors.append(f"{cpath}: contradiction requires at least two evidence refs")

        # Reading priority sanity
        judgment = paper.get("judgment_card") or {}
        rp = ((judgment.get("reading_priority") or {}).get("level"))
        if rp == "insufficient_evidence" and grade in ("E2_BODY_TEXT","E3_BODY_PLUS_ARTIFACTS") and coverage_level == "sufficient" and overall in ("strong","moderate"):
            warnings.append(f"{base}: insufficient_evidence reading priority conflicts with sufficient materials and {overall} support")

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
