# PaperScope / Scholar AI Deep Reading Skill v1.6

This skill turns one academic paper into an evidence-grounded research judgment rather than a longer summary.

## What changed in v1.6

The internal reading model is now:

`Triage → Reconstruct → Verify → Critique → Transfer`

Key upgrades:

- explicit pre-analysis Evidence Inventory;
- primary + optional secondary paper lens;
- expanded lenses for method, empirical, theory, review, resource, discovery, clinical, materials, and general papers;
- stronger 3-minute research judgment card;
- clearer Research Question vs Gap vs actual bottleneck;
- assumption chain: Why Needed → Failure Mode → Stress Test;
- experiment evidence chains instead of result-only summaries;
- claim-level strengthening plans are mandatory analysis outputs;
- 2–4 high-value core weaknesses instead of generic criticism;
- Open Question → Why it matters → Suggested validation;
- bounded research directions without auto-inventing named architectures;
- source-grounded ~20-minute return-to-paper path with per-step time budgets;
- optional transferable-knowledge sidecar for future knowledge-base workflows;
- stricter semantic validator for evidence inventory, judgment quality, and reading-guide timing.

## Stable user-facing report

The visible report remains six stages:

1. 论文速览
2. 研究问题与 Gap
3. 核心方法与真实创新
4. 实验与证据
5. 批判性评价
6. 开放问题与精读建议

The backend is deliberately richer than the visible report.

## Validate a result

```bash
python scripts/validate_result.py examples/minimal-v1.6.json --strict-warnings
```

## Output contract

Canonical schema:

`schemas/deep-reading-result.schema.json`

Default rendering target:

- 3-minute judgment layer;
- concise 4–6 page main report for a typical methods paper;
- evidence appendix for detailed traceability.

Formatting is delegated to Scholar-Format-Engine.
