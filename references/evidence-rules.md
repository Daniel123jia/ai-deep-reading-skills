# Evidence Rules

Use these rules whenever the deep reading report makes a factual statement, an inference, or a criticism about a paper. These rules apply to all reading modes. In `quick_summary` mode, apply them only to the fields that are produced.

---

## Input Evidence Grades

Record the evidence grade separately for each paper. It describes material actually inspected, not material that may exist elsewhere.

`E0_TITLE_METADATA`: Title and metadata only. You may describe topic clues from the title, but cannot assert method details, experiments, results, limitations, or contributions.

`E1_ABSTRACT`: Title, metadata, and abstract. You may restate author-claimed problem, method overview, and abstract-level findings, marked as `reported` claims. You may not fill in experiment details or numbers not in the abstract.

`E2_BODY_TEXT`: Readable body text. You may analyze problem definition, method details, experiment setup, and text-reported conclusions with section or page locations when available.

`E3_BODY_PLUS_ARTIFACTS`: Body text plus figures, tables, equations, appendix, or supplementary material. You may report precise table/figure/equation conclusions and ablation details when evidence references locate them.

`deep_reading` requires `E2_BODY_TEXT` or `E3_BODY_PLUS_ARTIFACTS`. Use `limited_reading` for `E0_TITLE_METADATA` or `E1_ABSTRACT`.

Code availability, dataset availability, and reproduction runs do not upgrade the paper evidence grade. Track them as a separate `verification_status` field when the caller provides that information.

---

## Statement Status

Each conclusion-like field must carry one status:

`reported`: The paper explicitly states this point in inspected material. A real evidence ref must be attached.

`inferred`: The point is a reasonable inference from inspected material, but the authors did not directly state it. An evidence ref should be attached if possible; if not, explain why in the note.

`unknown`: The inspected material does not establish the point. Do not attach a speculative evidence ref; explain the gap instead.

Never use the paper's overall evidence grade as a replacement for statement-level evidence references. A paper with `E3` grade can still have individual `unknown` statements if a specific sub-claim is not covered in the inspected material.

---

## Wording Rules

- For `reported`, use: "The paper states", "The authors report", "Table X shows", "Section Y describes". Only use these phrases when a real evidence ref is attached.
- For `inferred`, use: "This suggests", "A reasonable inference is", "Based on the inspected material", "The pattern in Table X implies".
- For `unknown`, use: "The inspected material does not specify", "Current materials do not establish", "This is not addressed in the inspected sections".
- Never write "the authors believe", "the authors argue", or "the authors show" for `inferred` or `unknown` statements.
- "Not mentioned" does not mean "not present in the paper"; write "current materials do not specify."
- If a page, section, table, figure, or equation location is unavailable, set the location fields to `null` and explain the limitation in the evidence note. Do not invent locations.

---

## Assumption Classification Rules

When extracting assumptions in step 5 of the workflow, classify each as:

`explicit`: The paper directly states this as an assumption, precondition, or scope limitation. Attach an evidence ref with the location.

`inferred`: The assumption is implied by the method design or experimental setup but not stated. Explain the reasoning.

`high_risk`: The assumption, if violated, would invalidate the core claim or main result. Flag these prominently in both `method_summary.assumptions` and `critical_review.fragile_assumptions`. A high-risk assumption may be explicit or inferred.

Examples of high-risk assumptions:
- i.i.d. data assumption when the paper does not test out-of-distribution.
- Linear scalability claim without multi-scale experiments.
- Claim of generality when only one domain or language is tested.

---

## Claim-Evidence Checks

For each important claim:

1. State the claim text in plain language.
2. Assign one statement status.
3. Attach one or more evidence refs when available.
4. Judge support strength as `strong`, `moderate`, `weak`, `missing`, or `overclaimed`.
5. State what would strengthen the claim: a missing baseline, ablation, statistical test, dataset diversity, qualitative evidence, or external replication.

---

## Downgrade Rules

Downgrade a claim's support strength when any of the following apply:

- The result is shown on only one dataset but the conclusion is stated generally.
- Robustness is claimed without stress tests, domain shift experiments, or ablation evidence.
- Claimed novelty is not compared with the closest prior work mentioned in the paper.
- The method improvement is reported without enough baseline detail to judge effect size.
- The conclusion depends on an assumption that the paper itself does not test.
- A single metric is used when the task has established multi-metric standards.
- Results are only on in-distribution test splits with no held-out or out-of-domain evaluation.

Unsupported or overclaimed findings belong in `evidence_audit.unsupported_or_overclaimed`, not in `contributions` or `evaluation_or_findings` as confirmed results.

---

## Protect Rules (do not over-downgrade)

Do not downgrade a claim below `moderate` when all of the following hold:

- The paper provides a direct experimental comparison (a table or figure with the proposed method and at least two prior baselines).
- The metrics used are standard and established for that task.
- The experimental setup is described in enough detail that a reader could reproduce it.
- No methodological flaw is identified that would invalidate the comparison.

In this case, downgrading to `weak` solely because external replication is absent is incorrect. Lack of external replication is a legitimate note in `evidence_audit.missing_evidence`, but it does not automatically lower a well-supported result.

Similarly, do not mark every `inferred` statement as `weak`. An inference that follows directly and unambiguously from a clearly reported result may be `moderate`.

The goal is calibrated assessment, not systematic pessimism.

---

## Evidence Audit Application

Before finalizing output, scan every field containing a factual claim:

- Statements without an attached evidence ref must be status `inferred` or `unknown`, not `reported`.
- Any statement marked `reported` must have at least one evidence ref with a real location or an explicit note explaining why the location is unavailable.
- Overclaimed items found during the audit move to `evidence_audit.unsupported_or_overclaimed`.
- Items that cannot be established from inspected material move to `evidence_audit.missing_evidence` as strings describing what is missing.
- After the audit, `evidence_audit.overall_support` is set based on the ratio of strongly to weakly supported claims: if most key claims are strong or moderate, set `moderate` or `strong`; if most are weak or missing, set `weak` or `insufficient`.
