# Schema Invariants — v1.5

These rules define semantic correctness beyond JSON Schema validation.

## Evidence inventory and backlinks
1. Every `ev-*` id exists exactly once.
2. Every referenced evidence id resolves.
3. Every non-null `snippet` is verbatim inspected source text.
4. Every `reported` statement has at least one real evidence ref.
5. `supported_claim_ids` on evidence refs must point to existing claims.
6. Claim evidence links and evidence backlinks should agree for direct/indirect support.

## Locator consistency
7. `structure_grounded` forbids PDF page locators.
8. `source_limited` forbids page/figure/table/equation locators unless explicitly present in the limited inspected source.
9. The report cannot emit a locator stronger than its source boundary.

## Statement semantics
10. `reported` = paper-explicit.
11. `inferred` = PaperScope analysis grounded in inspected material.
12. `unknown` = genuine non-establishment, not a safety placeholder.
13. A detailed positive method/result proposition should not be `unknown` when inspected evidence establishes it.

## Claims
14. Claim ids are unique.
15. Each important claim has at least one evidence link.
16. `paper_internal_support` is determined from paper-internal evidence, not external replication status.
17. External replication absence alone cannot force paper-internal support to `weak`.
18. `what_would_strengthen_it` must be a concrete analysis-derived test/check.
19. Quantitative claim details should be traceable to linked evidence containing the relevant numeric result or a verified table/figure source.
20. A claim with only context evidence cannot be graded as strongly directly supported.

## Evidence backlinks
21. Evidence used by a claim should list that claim in `supported_claim_ids` unless the relation is `context` or `contradictory`.
22. An evidence backlink must not point to a nonexistent claim.

## Research Gap
23. Research question and research Gap are not the same object.
24. `paperscope_bottleneck` is normally `inferred`, unless the paper explicitly states the same bottleneck.
25. Gap assessment must include evidence-backed rationale.

## Assumptions
26. Assumption ids are unique.
27. Risk and provenance are independent dimensions.
28. High-risk assumptions require `why_needed`, `failure_mode`, and `stress_test`.
29. High-risk assumptions appear in `critical_review.fragile_assumptions` by id.
30. A target claim such as “the proposed method is better” should not be recycled as an assumption.

## Experiments
31. Experiment ids are unique.
32. Every experiment has evidence refs.
33. Experiment conclusions are bounded by the tested protocol.
34. When comparison conditions differ materially, protocol risks must say so.

## Novelty
35. `paper_relative_delta` may be assessed from the paper.
36. `field_novelty` requires external literature verification.
37. If `context_mode = paper_only`, `field_novelty` must be null/unverified.

## Limitations
38. Author-acknowledged limitations are `reported` and evidence-backed.
39. PaperScope limitations belong in `critical_review.analysis_limitations` and are normally `inferred`.
40. Do not duplicate the same point across author limitations and analysis limitations without explaining the provenance difference.

## Open questions and guided reading
41. Standard E2/E3 deep reading should normally produce at least one grounded open question.
42. Every open question contains a bounded validation plan.
43. Standard E2/E3 deep reading should provide reading-guide items and a structured 20-minute path.
44. Reading-guide locators must come from inspected material.
45. Every reading-guide item explains why the reader should look there.

## Material coverage
46. Coverage matrix and evidence grade must not contradict each other.
47. “Partial” coverage should explain what is present and what is missing rather than functioning as a vague label.

## Contradictions
48. Source conflicts are preserved, not silently reconciled.
49. A contradiction references at least two evidence refs.
50. The affected conclusion is marked uncertain or bounded accordingly.


## v1.5 invariants

1. Every claim has a non-empty, descriptive `claim_title`; renderers should prefer it to raw claim IDs.
2. In standard/reviewer/followup modes, if the source boundary is at least E2 and critique is possible, `critical_review.core_weaknesses` should contain the highest-value weaknesses rather than a generic list of missing checks.
3. Every core weakness must resolve all evidence refs and related claim/assumption IDs.
4. `why_it_matters`, `potential_impact`, and `suggested_validation` for core weaknesses may not use placeholders such as “当前材料未说明”.
5. Every open question must contain substantive `why_it_matters` and `suggested_validation`.
6. Research directions must be analysis-bounded and may not silently become named architecture proposals.
