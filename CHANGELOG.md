# Changelog

## 1.6.0

### Researcher reading model
- Introduced `Triage → Reconstruct → Verify → Critique → Transfer` as the internal reading workflow.
- Clarified that Deep Reading is a research decision/navigation layer, not a paper-replacement summary.

### Grounding
- Added required `evidence_inventory` before interpretation.
- Added required `paper_lens` with one primary and optional secondary lens.
- Expanded paper lenses to method, empirical, theory, review, resource, discovery, clinical, materials, and general.

### Research judgment
- Added `why_read` and `next_research_direction` to the judgment card.
- Kept reading priority as a decision aid rather than a paper-quality score.

### Guided reading
- Added minute budgets to the 20-minute reading path.
- Added validation that the path totals roughly 15–25 minutes.

### Knowledge transfer
- Added optional `knowledge_takeaways` sidecar for future knowledge-base workflows without creating a seventh visible report section.

### QA
- Validator now checks paper-lens coherence, evidence-inventory references, judgment-card actionability, thin inventories, and reading-route time budgets.
