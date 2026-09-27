# Evidence Rules

These rules govern factual statements, analytical inferences, criticism, novelty judgments, and follow-up questions in all reading modes.

## 1. Evidence grade

`E0_TITLE_METADATA` — metadata only.

`E1_ABSTRACT` — metadata + abstract.

`E2_BODY_TEXT` — readable body text.

`E3_BODY_PLUS_ARTIFACTS` — body text + inspected figures/tables/equations/appendix/supplement.

`deep_reading` requires E2 or E3. E0/E1 use `limited_reading`.

Evidence grade describes what was inspected. It does not indicate external replication or how completely the current reading task is covered.

## 2. Source boundary

Track separately:

- evidence grade;
- evidence coverage;
- locator mode;
- context mode;
- boundary note.

### Locator rules

`page_grounded` — reliable PDF page indices are available.

`structure_grounded` — section/figure/table/equation structure is reliable, but PDF page indices are not.

`source_limited` — metadata, abstract, or partial excerpts only.

Hard rules:

- `structure_grounded` => no non-null page locators anywhere in evidence refs.
- `source_limited` => no invented page/figure/table/equation locators.
- Do not emit a locator stronger than the established source boundary.

## 3. Statement status

### `reported`
The inspected source explicitly states the point.

Requirements:

- at least one real evidence ref;
- wording does not exceed source scope.

### `inferred`
PaperScope/agent analysis grounded in inspected material.

Use for:

- actual bottleneck assessment;
- method interpretation not explicitly stated;
- alternative explanation;
- critical limitation;
- inferred assumption;
- general lesson.

### `unknown`
The material genuinely does not establish the point.

Do not use `unknown` as a safety default.

A detailed positive proposition such as “the module uses k-NN cosine matching” cannot be both specific and `unknown` if the inspected paper supports it.

For genuine unknowns, write the non-establishment itself, e.g.:

> Current materials do not establish whether the gain persists under domain shift.

## 4. Evidence refs

Each evidence ref separates source from interpretation.

- `snippet`: short verbatim source excerpt only.
- `paraphrase`: model summary/interpretation.
- `verification_status`: verification of source excerpt/locator, not external scientific replication.

Never synthesize a plausible source quote.

If a source location is known but no excerpt was retained:

- `snippet = null`;
- keep an accurate paraphrase;
- mark source verification appropriately.

## 5. Paper-internal support vs external verification

These are independent.

`paper_internal_support` asks:

> Does the inspected paper itself provide evidence for this bounded claim?

`external_verification_status` asks:

> Has the claim been checked outside this paper or reproduced independently?

Lack of external replication must not automatically reduce paper-internal support.

Example:

- a direct ablation table can strongly support a bounded within-paper comparison;
- external verification may still be `not_checked`.

Do not repeatedly weaken a claim merely because code was not rerun.

## 6. Support scale

`strong` — direct, well-matched evidence supports the bounded claim.

`moderate` — useful direct or converging evidence exists, with meaningful limitations.

`weak` — evidence is indirect, narrow, incomplete, or confounded.

`missing` — the paper/material does not provide evidence for the claim.

`overclaimed` — the claim materially exceeds available evidence.

`not_applicable` — support grading does not apply.

## 7. Downgrade rules

Downgrade when:

- a narrow experiment is generalized broadly;
- robustness is claimed without stress tests;
- a causal claim lacks causal design;
- novelty is claimed without relevant comparison;
- a key assumption is untested and decisive;
- baseline details prevent fair comparison;
- evaluation covers only a narrow population/domain while conclusion is general;
- a quantitative claim is not supported by the cited evidence.

## 8. Protect rules

Do not over-downgrade.

A bounded claim may be `strong` or `moderate` when:

- direct comparison/ablation exists;
- standard metrics are used;
- setup is sufficiently described;
- no identified flaw invalidates the comparison.

External replication is valuable, but its absence alone is not a reason to reduce a well-supported paper-internal claim.

An `inferred` statement may also receive `moderate` support when the inference follows directly from clearly inspected evidence.

## 9. Assumptions

Assumption provenance and risk are independent.

`provenance`:

- `explicit` — author-stated assumption/precondition;
- `inferred` — implied by design or evaluation.

`risk_level`:

- `low`;
- `medium`;
- `high`.

High-risk assumptions require:

- a stable `assumption_id`;
- failure mode;
- stress-test idea;
- mirrored reference in `critical_review.fragile_assumptions`.

## 10. Claim–Evidence checks

Each important claim must include:

1. stable claim id;
2. importance;
3. claim text and provenance status;
4. evidence refs;
5. paper-internal support;
6. support reason;
7. scope boundary;
8. unsupported stronger claim when useful;
9. concrete strengthening action;
10. external verification status.

### Strengthening action

`what_would_strengthen_it` is PaperScope analysis.

Do not answer:

- “current materials do not specify”;
- “unknown”;
- “not mentioned”.

Instead propose a bounded check, such as:

- matched-backbone baseline;
- missing ablation;
- statistical test;
- additional dataset/population;
- cross-domain test;
- sensitivity analysis;
- code reproduction;
- independent replication.

## 11. Author limitations vs analysis limitations

### Author-acknowledged limitations

Only include points explicitly acknowledged by authors.

Requirements:

- status `reported`;
- evidence refs required.

If authors describe a constraint without calling it a “limitation”, it may still be included when clearly framed as a constraint/caveat; do not misrepresent it as a formal limitation if the distinction matters.

### Analysis limitations

Agent/PaperScope criticism belongs in `critical_review.analysis_limitations` and is normally `inferred`.

Never mix the two categories.

## 12. Novelty

`paper_relative_delta` is what changes relative to prior work discussed by the paper.

`field_novelty` requires targeted external verification.

If `context_mode = paper_only`:

- `field_novelty = null`;
- do not claim first/unprecedented/field-novel/broad-SOTA status.

## 13. Open questions

Open questions do not require an explicit Future Work section.

They may be derived from:

- assumptions;
- failure modes;
- parameter sensitivity;
- anomalous results;
- narrow evaluation;
- unresolved comparisons;
- missing robustness tests;
- author caveats.

Each question includes:

- origin: `author_stated` or `analysis_derived`;
- why it matters;
- bounded suggested validation;
- evidence refs.

Do not automatically design a new named architecture or module.

## 14. Reading guide

A standard deep reading should identify high-value original locations to inspect.

Prioritize:

- method-defining section/equation;
- key comparison table;
- key ablation/sensitivity table;
- discussion/limitations;
- any figure essential to mechanism.

Only recommend locators actually present in inspected material.

## 15. Contradictions and mismatches

When source materials disagree:

1. retain both values/statements;
2. attach both evidence refs;
3. describe impact;
4. state what would resolve the discrepancy.

Do not silently reconcile.

For quantitative claim–evidence mismatches:

- split the claim;
- correct the evidence mapping;
- or downgrade support.

## 16. Final evidence audit

Before output check:

- every `reported` statement resolves to evidence;
- every evidence id exists;
- `unknown` is genuine non-establishment;
- snippets are source-derived;
- source-boundary and locator precision are consistent;
- field novelty is externally grounded;
- high-risk assumptions are linked correctly;
- author limitations and analysis limitations are separated;
- quantitative claims match cited evidence;
- `what_would_strengthen_it` is concrete;
- external verification did not improperly lower paper-internal support;
- open questions are populated when defensible;
- reading guide is populated for standard deep readings;
- contradictions are surfaced.
