# PaperScope AI Deep Reading Skill

Evidence-grounded academic paper deep reading for PaperScope / Scholar AI.

Version: **1.3.0**

## What this skill does

It turns parsed paper content into a structured deep-reading result that supports:

- research problem and gap analysis;
- method and mechanism reconstruction;
- assumption auditing;
- contribution and novelty-boundary analysis;
- claim → evidence → support → scope mapping;
- author-vs-analysis limitation separation;
- reviewer-style critical reading;
- open questions with bounded validation ideas;
- original-paper reading guidance;
- contradiction and evidence-mismatch tracking.

The skill does **not** parse PDFs, retrieve papers, format Word documents, rank papers, or predict acceptance.

## Files

- `SKILL.md` — main workflow and boundaries.
- `references/evidence-rules.md` — evidence semantics and support rules.
- `references/schema-invariants.md` — semantic invariants beyond JSON Schema.
- `references/rendering-guidance.md` — mapping from backend JSON to polished user-facing reports.
- `schemas/deep-reading-result.schema.json` — v1.3 structured output contract.
- `scripts/validate_result.py` — schema + semantic validator.
- `agents/openai.yaml` — agent metadata.
- `examples/minimal-v1.3.json` — valid compact example.
- `CHANGELOG.md` — version history.

## v1.3 highlights

v1.3 is a consistency and completeness upgrade based on real report testing.

### 1. Strict status semantics

`unknown` is no longer a safe default. Detailed supported method/result statements must be `reported` or `inferred`.

### 2. Source-boundary consistency

`structure_grounded` cannot emit PDF page numbers. Locator strength must match the declared boundary.

### 3. Internal evidence vs external verification

A claim now records:

- `paper_internal_support`;
- `external_verification_status`.

Lack of third-party replication does not automatically weaken a direct within-paper comparison.

### 4. Author limitations vs PaperScope criticism

- `author_acknowledged_limitations` = author-explicit only.
- `critical_review.analysis_limitations` = agent/PaperScope analysis.

### 5. Better Claim–Evidence records

Claim evidence is no longer duplicated inside nested evidence statements. Claims include:

- stable id;
- importance;
- evidence refs;
- internal support;
- support reason;
- scope boundary;
- unsupported stronger claim;
- concrete strengthening action;
- external verification status.

### 6. Open questions and reading guide

Standard E2/E3 deep readings should derive useful open questions when defensible and provide a must-read / recommended / skim reading guide plus a 20-minute path.

### 7. Stable assumption links

Assumptions now have `assumption_id`, allowing section 03 assumptions to link cleanly to section 05 fragile-assumption failure modes.

### 8. Contradiction tracking

Conflicting source values/statements are preserved and surfaced rather than silently reconciled.

### 9. Human-readable rendering guidance

Raw backend enums should not appear repeatedly in formal Word/Markdown reports.

### 10. Semantic validator

Run:

```bash
python scripts/validate_result.py result.json
```

It checks both JSON Schema and semantic invariants such as:

- unresolved evidence ids;
- locator-mode conflicts;
- reported statements without evidence;
- high-risk assumption links;
- novelty/context conflicts;
- empty open questions/reading guide warnings;
- suspicious quantitative claim/evidence mismatch;
- reading-priority/support inconsistency.

## Install

Copy the repository into your skill directory, for example:

```text
$CODEX_HOME/skills/paperscope-ai-deep-reading
```

## Reading modes

| Mode | Use |
|---|---|
| `quick_summary` | fast triage |
| `standard` | default full deep reading |
| `reviewer_mode` | peer-review preparation |
| `followup_mode` | open questions and research follow-up |
| `method_only` | technical method deep dive |

## Architecture

```text
Title / DOI / arXiv / PDF
        ↓
Retriever + Parser
        ↓
Structured source bundle
        ↓
PaperScope AI Deep Reading Skill
        ↓
deep-reading-result.json v1.3
        ↓
Web renderer / Scholar Format Engine
```

The deep-reading skill should not own Word typography or document export. A separate formatting/delivery layer should consume the structured result.

## Six-stage UI mapping

The backend can remain detailed while the user sees:

1. 论文速览
2. 研究问题与 Gap
3. 核心方法与真实创新
4. 实验与证据
5. 批判性评价
6. 开放问题与精读建议

See `references/rendering-guidance.md`.

## v1.2 → v1.3 migration

v1.3 is intentionally not backward compatible with v1.2.

Main changes:

- removed duplicated top-level `paper_report.evidence_grade`; use `source_boundary.evidence_grade`;
- added `source_boundary.boundary_note`;
- assumptions require `assumption_id`;
- claim nested object no longer carries its own evidence refs/support strength;
- `claim_evidence.support_strength` → `paper_internal_support`;
- claim adds `external_verification_status`;
- `evidence_audit.overall_support` → `paper_internal_support`;
- `judgment_card.evidence_strength` → `paper_internal_evidence_strength`;
- research value dimensions now include `level + rationale`;
- reading priority now includes `level + reason`;
- `limitations_or_unknowns` removed;
- added `author_acknowledged_limitations` and `unresolved_unknowns`;
- `critical_review.main_limitations` → `analysis_limitations`;
- open questions use `origin + suggested_validation` rather than statement status;
- added `reading_guide`;
- added `contradictions`.

## Design principle

The product should not merely say:

> “AI thinks this paper is good.”

It should be able to say:

> “This is the judgment, this is the source, this is why the source supports it, this is the boundary, and this is what remains unverified.”
