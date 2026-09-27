# Changelog

## 1.3.0 — 2026-09-27

Consistency and report-completeness release.

### Added

- stable `assumption_id`;
- source-boundary `boundary_note`;
- claim-level `external_verification_status`;
- `author_acknowledged_limitations`;
- `unresolved_unknowns`;
- `critical_review.analysis_limitations`;
- `critical_review.applicability_boundary`;
- open-question `origin` and bounded `suggested_validation`;
- `reading_guide` with a 20-minute path;
- contradiction tracking;
- research-value rationale;
- reading-priority reason;
- semantic validator;
- rendering guidance;
- schema invariant documentation.

### Changed

- strict status semantics: `unknown` is true non-establishment only;
- claim support renamed to `paper_internal_support`;
- evidence audit overall support renamed to `paper_internal_support`;
- judgment card uses `paper_internal_evidence_strength`;
- external replication no longer automatically downgrades internal evidence;
- claim evidence refs are stored once at claim-item level;
- high-risk fragile assumptions reference the source assumption by id;
- `what_would_strengthen_it` must be concrete analysis, not a source-placeholder;
- source locator precision must match the declared locator mode.

### Removed / replaced

- `paper_report.evidence_grade` duplicate (use `source_boundary.evidence_grade`);
- `limitations_or_unknowns`;
- `critical_review.main_limitations`;
- open-question statement `status`;
- unexplained scalar research-value labels;
- unexplained scalar reading priority.

## 1.2.0

Claim-level evidence-grounding release: source boundary, evidence coverage, locator modes, real snippets vs paraphrases, two-axis assumptions, structured modules, claim boundaries, novelty verification, and core-claim weighted evidence audit.

## 1.1.0

Added reading modes, assumptions, fragile assumptions, equations, multi-dimensional research value, and protect rules.
