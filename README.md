# PaperScope AI Deep Reading Skill

Codex skill for evidence-grounded academic paper deep reading in PaperScope.

## Contents

- `SKILL.md` — main workflow, reading mode routing, and boundaries.
- `references/evidence-rules.md` — evidence grading, statement status, downgrade rules, and protect rules.
- `schemas/deep-reading-result.schema.json` — structured output contract (v1.2).
- `agents/openai.yaml` — agent metadata.

## What's new in v1.2

v1.2 upgrades the skill from a strong deep-reading schema to a claim-level evidence-grounding protocol. The frontend can still render a simple six-stage report, while the JSON supports evidence panels behind important judgments.

- **Source boundary** — each paper records `evidence_grade`, `evidence_coverage`, `locator_mode`, and `context_mode` separately.
- **Locator modes** — distinguish `page_grounded`, `structure_grounded`, and `source_limited` evidence.
- **Evidence refs split source from interpretation** — `snippet` is real parsed source text only; `paraphrase` is model interpretation.
- **Two-axis assumptions** — assumptions now use `provenance` (`explicit` / `inferred`) plus independent `risk_level` (`low` / `medium` / `high`).
- **Structured method modules** — modules capture purpose, input, operation, output, why needed, measured effect, and evidence refs.
- **Claim-level support boundaries** — claims now include `claim_id`, importance, `support_reason`, `scope_boundary`, and `unsupported_stronger_claim`.
- **Novelty verification split** — `paper_relative_delta` is separated from externally verified `field_novelty`.
- **Core-claim weighted audit** — overall support is driven by core claim support, not a simple ratio of strong/weak claims.

## What was added in v1.1

- **Reading mode routing** — resolve `quick_summary`, `standard`, `reviewer_mode`, `followup_mode`, or `method_only` from `input.reading_goal` before starting analysis. Each mode adjusts required output sections and emphasis.
- **Assumption fields** — `method_summary.assumptions` now captures explicit, inferred, and high-risk assumptions with a dedicated `assumption_item` type.
- **Fragile assumptions** — `critical_review.fragile_assumptions` surfaces high-risk assumptions separately from general limitations, with a required `failure_mode` explanation.
- **Equations support** — `paper_map.equations` tracks key equations and theorems as first-class inspected items alongside figures and tables.
- **Multi-dimensional judgment card** — `judgment_card.research_value` is now a breakdown object with `methodological`, `empirical`, and `application` dimensions instead of a single score.
- **Protect rules** — `references/evidence-rules.md` adds explicit protect rules to prevent over-downgrading well-supported results.
- **`reading_mode` in input** — `input.reading_mode` records the resolved mode for downstream rendering.
- **Schema `$id` fix** — changed from `paperscope.local` to a `urn:` identifier for portability.
- **5-paper limit explanation** — documented in both `SKILL.md` and `agents/openai.yaml`.

## Install

Copy this repository into:

```
$CODEX_HOME/skills/paperscope-ai-deep-reading
```

Then use it when running AI paper deep reading, paper understanding, method analysis,
claim-evidence review, assumption auditing, or research follow-up workflows.

## Reading Modes

| Mode | When to use |
|---|---|
| `quick_summary` | Fast triage — emphasizes judgment card and research question while preserving the full JSON shell |
| `standard` | Default full deep reading |
| `reviewer_mode` | Peer review prep — emphasizes critical review and evidence audit |
| `followup_mode` | Research planning — emphasizes open questions and contributions |
| `method_only` | Technical deep-dive — emphasizes method, assumptions, and claims |

## Schema Compatibility

v1.2 is not backwards-compatible with v1.1 outputs due to:
- `schema_version` changed to `1.2`.
- `paper_report.source_boundary` is required.
- `evidence_ref` replaces mixed `note` with `source_type`, `locator_mode`, `source_block_id`, `snippet`, `paraphrase`, and `verification_status`.
- `assumption_item.assumption_type` was replaced by `provenance` and `risk_level`.
- `method_summary.main_modules` now uses structured module objects, not generic evidence statements.
- `claim_evidence` items require `claim_id`, `importance`, `support_reason`, `scope_boundary`, and `unsupported_stronger_claim`.
- `novelty_verification` is required.

v1.1 was not backwards-compatible with v1.0 outputs due to:
- `judgment_card.research_value` changed from `string` to `object`.
- `method_summary.assumptions` is a new required field.
- `critical_review.fragile_assumptions` is a new required field.
- `paper_map.equations` is a new required field.
- `input.reading_mode` is a new required field.

If you have existing v1.0 or v1.1 outputs, use their original schema for validation and migrate
gradually as you re-run analyses.
