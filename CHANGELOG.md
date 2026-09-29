# Changelog

## 1.5.0 — Traceable Critical Reading

- Added `claim_title` for human-readable Claim–Evidence reporting.
- Added `critical_review.core_weaknesses` with weakness → why it matters → impact → validation chains.
- Added bounded `research_directions` derived from evidence-backed weaknesses/open questions.
- Added semantic rules that reject placeholder text in claim strengthening, weakness validation, open-question rationale/validation, and research directions.
- Added cross-links from core weaknesses to claims and assumptions.
- Updated guided reading so it can route the reader back to the source most diagnostic for the paper's biggest risk.
- Updated example, validator, rendering guidance, schema invariants, and agent metadata for schema v1.5.


## 1.4.0 — Traceable & Guided Reading

- Added component-level source coverage matrix.
- Added evidence roles and Evidence → Claim backlinks.
- Replaced plain claim evidence refs with relation-aware evidence links.
- Added structured research-gap analysis: author problem, claimed gap, PaperScope bottleneck, gap assessment.
- Added experiment-evidence chains with protocol risks and bounded conclusions.
- Added assumption `why_needed` and `stress_test` fields.
- Added optional key-equation explanations for method/theory papers.
- Added structured 20-minute return-to-source reading path.
- Expanded research judgment card with core problem/method/innovation/evidence/risk/open-question fields.
- Added paper-type lenses and guided-reading rules.
- Strengthened semantic validator for backlinks, numeric grounding, coverage coherence, assumption stress tests, experiment evidence, and reading-guide completeness.

## 1.3.0

- Corrected `unknown` semantics.
- Separated author limitations from PaperScope analysis limitations.
- Separated paper-internal support from external verification.
- Added stable assumption IDs, open questions, reading guide, contradictions, and semantic validation.

## 1.2.0

- Added source boundary, evidence coverage, locator modes, claim-level support boundaries, structured modules, and novelty verification.
