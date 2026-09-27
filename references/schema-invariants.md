# Schema Invariants — v1.3

These invariants define semantic correctness beyond JSON Schema validation.

## Evidence references

1. Every referenced `ev-*` id must exist exactly once in `paper.evidence_refs`.
2. Every `reported` statement must reference at least one real evidence id.
3. A non-null `snippet` must be verbatim source text, not model-generated prose.
4. `snippet` and `paraphrase` must never be presented as the same provenance.

## Locator consistency

5. `source_boundary.locator_mode = structure_grounded` forbids non-null page numbers in evidence refs.
6. `source_boundary.locator_mode = source_limited` forbids page/figure/table/equation locators unless the limited inspected source explicitly contains that locator.
7. The report must not advertise a weaker locator boundary while emitting stronger locators.

## Statement status

8. `reported` means paper-explicit and evidence-grounded.
9. `inferred` means analysis grounded in inspected material.
10. `unknown` means genuine non-establishment. It must not be used as a default label for detailed method/result/contribution statements.
11. An `unknown` evidence statement should normally use `support_strength = missing` and contain no fabricated positive detail.

## Claims

12. Claim ids are unique.
13. Claim-level `paper_internal_support` is based on paper-internal evidence only.
14. External replication status must not automatically lower paper-internal support.
15. `what_would_strengthen_it` must be a concrete analysis-derived action, not a placeholder.
16. Quantitative details in a claim must be supported by at least one cited evidence source or explicitly marked as needing verification.

## Assumptions

17. Assumption ids are unique.
18. Every high-risk assumption should have a non-empty failure mode and testability note.
19. Every high-risk assumption must have a matching `critical_review.fragile_assumptions` entry by `assumption_id`.

## Limitations

20. `author_acknowledged_limitations` contains author-explicit constraints/caveats only and uses `reported` status.
21. Agent/PaperScope criticism belongs in `critical_review.analysis_limitations`, normally as `inferred`.
22. Do not duplicate the same limitation into both categories without explaining the different provenance.

## Novelty

23. When `context_mode = paper_only`, `novelty_verification.field_novelty` must be null.
24. Field-level novelty requires external evidence and a compatible novelty status.

## Open questions and reading guide

25. In `standard` or `followup_mode`, an E2/E3 paper should usually have at least one open question when assumptions, limitations, sensitivity, anomalies, narrow evaluation, or unresolved comparisons exist.
26. Open-question validation stops at how to test the question; it does not automatically invent a new named method.
27. A standard deep reading should include a non-empty reading guide when useful source locations are available.

## Overall support and reading priority

28. `judgment_card.paper_internal_evidence_strength` should align with `evidence_audit.paper_internal_support` unless an explicit reason explains the difference.
29. A core claim with `missing` or `overclaimed` support prevents an overall `strong` paper-internal support rating.
30. If a core claim is `weak`, overall support is at most `moderate`.
31. `reading_priority = insufficient_evidence` should not be used merely because external replication is absent. It is for genuinely inadequate material/evidence coverage.

## Contradictions

32. Source disagreements must be recorded rather than silently reconciled.
33. A contradiction item needs at least two evidence refs.
