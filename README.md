# PaperScope AI Deep Reading Skill

Codex skill for evidence-grounded academic paper deep reading in PaperScope.

## Contents

- `SKILL.md` — main workflow, reading mode routing, and boundaries.
- `references/evidence-rules.md` — evidence grading, statement status, downgrade rules, and protect rules.
- `schemas/deep-reading-result.schema.json` — structured output contract (v1.1).
- `agents/openai.yaml` — agent metadata.

## What's new in v1.1

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

v1.1 is not backwards-compatible with v1.0 outputs due to:
- `judgment_card.research_value` changed from `string` to `object`.
- `method_summary.assumptions` is a new required field.
- `critical_review.fragile_assumptions` is a new required field.
- `paper_map.equations` is a new required field.
- `input.reading_mode` is a new required field.

If you have existing v1.0 outputs, use the v1.0 schema for validation and migrate
gradually as you re-run analyses.
