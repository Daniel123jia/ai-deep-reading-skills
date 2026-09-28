# Evidence Rules — v1.4

These rules govern factual statements, analytical inferences, criticism, novelty judgments, experiment interpretation, and guided reading.

## Evidence grade and coverage
`E0_TITLE_METADATA`: metadata only.

`E1_ABSTRACT`: metadata + abstract.

`E2_BODY_TEXT`: readable body text.

`E3_BODY_PLUS_ARTIFACTS`: body text plus inspected figures/tables/equations/appendix/supplement.

Evidence grade is not external replication status. Coverage matrix explains which material classes are actually available.

## Source boundary
Track evidence grade, task-level evidence coverage, locator mode, context mode, coverage matrix, and a human-readable boundary note.

### Locator rules
- `page_grounded`: reliable PDF pages.
- `structure_grounded`: reliable structure, unreliable/absent PDF pages.
- `source_limited`: limited sources only.

Hard rule: `structure_grounded` means page must be null.

## Statement status
### reported
Explicitly stated by the inspected paper/material. Requires evidence.

### inferred
PaperScope interpretation grounded in inspected evidence.

### unknown
The materials genuinely do not establish the point. Unknown is not a default safety label.

## Evidence refs
Every evidence ref separates source text from interpretation:
- `snippet`: short verbatim source text only;
- `paraphrase`: model summary;
- `verification_status`: whether the excerpt/locator itself is source-verified;
- `evidence_role`: why this evidence matters;
- `supported_claim_ids`: backlinks into the claim map.

Never generate plausible source text.

## Claim evidence links
Each claim links evidence with a relation:
- `direct`: directly measures/defines the claim;
- `indirect`: supports the claim through a reasonable step;
- `context`: background/context only;
- `contradictory`: conflicts with the claim or part of it.

A strong claim should normally have at least one direct evidence link.

## Paper-internal support vs external verification
These are independent.

Paper-internal support answers whether the paper itself supports the bounded claim.

External verification answers whether independent literature/reproduction has checked it.

Do not downgrade a well-supported paper-internal experiment solely because external replication is absent.

## Support scale
- `strong`: direct, well-matched evidence for a bounded claim.
- `moderate`: useful direct/converging evidence with meaningful limitations.
- `weak`: narrow, indirect, incomplete, or confounded.
- `missing`: no evidence.
- `overclaimed`: wording exceeds evidence.
- `not_applicable`: grading not applicable.

## Numeric traceability
For important numeric claims, direct linked evidence should contain the same numbers or point to an inspected table/figure containing them.

If the linked source only provides qualitative context, relation must be `indirect` or `context`, not direct numeric support.

## Experiments
Interpret experiments through:
`purpose → design → conditions → result → supported conclusion → unsupported stronger conclusion → protocol risks`.

Do not treat author interpretation as equivalent to measured evidence.

## Assumptions
Provenance (`explicit`/`inferred`) and risk (`low`/`medium`/`high`) are independent.

For high-risk assumptions include:
- why the method needs it;
- failure mode;
- stress test.

A claim being tested is not automatically an assumption.

## Author limitations vs analysis limitations
Author limitations/constraints are reported and source-grounded.
PaperScope limitations are analytical and normally inferred.
Keep them separate.

## Novelty
Paper-relative delta may be analyzed from the paper.
Field novelty requires external literature verification.

If context mode is paper-only, do not claim first/unprecedented/field-novel/SOTA-across-field status.

## Open questions
Open questions may be derived from assumptions, parameter sensitivity, anomalies, narrow evaluation, missing robustness, or author caveats.

Every open question includes why it matters and how to validate it.

Do not automatically invent a named new architecture.

## Guided reading
Recommend only source locations actually available. Each recommendation explains why it matters and what to learn there.

## Final audit
Check:
- all refs resolve;
- every reported statement is evidenced;
- no fabricated snippets;
- locator rules hold;
- numeric claims map to proper evidence;
- evidence backlinks and claim links agree;
- high-risk assumptions have failure/stress-test logic;
- experiments do not overgeneralize;
- author vs analysis limitations are separated;
- open questions and reading guide are present in standard E2/E3 reading;
- field novelty obeys external-verification boundary;
- contradictions are surfaced.
