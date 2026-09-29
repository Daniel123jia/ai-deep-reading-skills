# PaperScope AI Deep Reading Skill v1.5

Evidence-grounded academic paper deep reading for PaperScope / Scholar AI.

v1.5 focuses on three goals:

- **More rigorous** — clearer source boundary, experiment protocol reasoning, assumption stress tests, and stronger status semantics.
- **More traceable** — claim→evidence links, evidence→claim backlinks, numeric grounding checks, contradiction handling.
- **More guided** — source-aware reading recommendations and a structured 20-minute return-to-paper path.

## Main files

- `SKILL.md` — workflow and hard boundaries.
- `schemas/deep-reading-result.schema.json` — v1.5 output contract.
- `references/evidence-rules.md` — evidence semantics.
- `references/paper-type-lenses.md` — method / empirical / theory / review lenses.
- `references/experiment-evidence-rules.md` — experiment interpretation protocol.
- `references/guided-reading-rules.md` — return-to-source reading guidance.
- `references/schema-invariants.md` — semantic invariants beyond JSON Schema.
- `references/rendering-guidance.md` — user-facing report guidance.
- `scripts/validate_result.py` — schema + semantic QA.
- `examples/minimal-v1.5.json` — valid reference output.

## User-facing six-stage report

1. 论文速览
2. 研究问题与 Gap
3. 核心方法与真实创新
4. 实验与证据
5. 批判性评价
6. 开放问题与精读建议

The backend is richer than these six sections so the UI can stay simple.

## What changed from v1.3

### Traceability
- Evidence refs now carry `evidence_role` and `supported_claim_ids` backlinks.
- Claims use evidence links with `direct / indirect / context / contradictory` relations.
- Validator checks missing backlinks and suspicious numeric claim/evidence mismatches.

### Rigor
- Added component-level material `coverage_matrix`.
- Added structured `research_gap` rather than treating the research question as the Gap.
- Added structured experiment-evidence chains.
- Assumptions now include `why_needed`, `failure_mode`, and `stress_test`.
- Method analysis can include verified key-equation explanations.

### Guided reading
- Reading guide now includes structured source targets and a structured ~20-minute path.
- Judgment card adds core problem, core method, paper-relative innovation, strongest evidence, biggest risk, key assumptions, and the most important open question.

## Validate an output

```bash
python scripts/validate_result.py examples/minimal-v1.5.json
```

Expected:

```text
OK: 0 errors, 0 warning(s)
```

## Integration

Recommended architecture:

```text
Title / DOI / arXiv / PDF
        ↓
Retriever + Parser
        ↓
Structured source bundle
        ↓
PaperScope AI Deep Reading v1.5
        ↓
deep-reading-result.json
        ↓
Web renderer / Scholar-Format-Engine
        ↓
Web / DOCX / Markdown / PDF
```

This skill does not format Word documents. Use Scholar-Format-Engine for final document delivery.
