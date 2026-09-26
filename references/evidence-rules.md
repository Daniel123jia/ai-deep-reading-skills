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

## Source Boundary, Coverage, and Locator Mode

Evidence grade, evidence coverage, locator mode, and context mode are separate concepts:

- Evidence grade: what kind of material was inspected.
- Evidence coverage: whether the inspected material sufficiently covers the claims being evaluated.
- Locator mode: how precisely evidence can be located.
- Context mode: whether the analysis is paper-only or externally checked.

Use locator modes as follows:

`page_grounded`: page numbers are reliable. Page + section + figure/table/equation may be used when present.

`structure_grounded`: readable sections, figures, tables, or equations are available, but page numbers are absent or unreliable. Do not invent page numbers.

`source_limited`: only metadata, abstract, or partial snippets are available. Do not cite pages, figures, tables, or equations unless they are truly present in inspected material.

If `context_mode` is `paper_only`, do not claim field-level novelty, first-in-field status, or broad SOTA status. Limit novelty language to paper-relative delta.

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

## Evidence Reference Rules

Each evidence ref must distinguish source text from interpretation:

- `snippet`: short verbatim text from parsed source material only. If unavailable, set it to `null`.
- `paraphrase`: concise model summary of the source. It must not be displayed as original source text.
- `verification_status`: `verified`, `needs_verification`, or `unavailable`.

Never generate plausible-looking source text to fill `snippet`. If a claim can only be guided to a likely section, create a source-limited evidence ref with `snippet: null` and mark it as a verification suggestion.

Every evidence ref cited by a claim, assumption, contribution, method module, or open question must exist in `evidence_refs`.

---

## Assumption Classification Rules

When extracting assumptions in step 5 of the workflow, classify each as:

`provenance = explicit`: The paper directly states this as an assumption, precondition, or scope limitation. Attach an evidence ref with the location.

`provenance = inferred`: The assumption is implied by the method design or experimental setup but not stated. Explain the reasoning.

`risk_level = high`: The assumption, if violated, would invalidate the core claim or main result. Flag these prominently in both `method_summary.assumptions` and `critical_review.fragile_assumptions`. A high-risk assumption may be explicit or inferred.

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
4. Assign a stable `claim_id` and importance: `core`, `secondary`, or `context`.
5. Judge support strength as `strong`, `moderate`, `weak`, `missing`, or `overclaimed`.
6. Explain the support relation in `support_reason`.
7. State the scope boundary: what conditions, datasets, methods, or materials the evidence actually covers.
8. State any unsupported stronger claim that the evidence does not justify.
9. State what would strengthen the claim: a missing baseline, ablation, statistical test, dataset diversity, qualitative evidence, or external replication.

---

## Downgrade Rules

Downgrade a claim's support strength when any of the following apply:

- The result is shown on only one dataset but the conclusion is stated generally.
- Robustness is claimed without stress tests, domain shift experiments, or ablation evidence.
- Claimed novelty is not compared with the closest prior work mentioned in the paper.
- Field-level novelty is asserted while `context_mode` is `paper_only`.
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
- Any non-null `snippet` must be copied from inspected source material. Model paraphrases belong in `paraphrase`, not `snippet`.
- Evidence refs with `locator_mode = source_limited` must not include invented page, figure, table, or equation locators.
- Claims with field-level novelty language require `context_mode` of `targeted_external_check` or `externally_verified`.
- Overclaimed items found during the audit move to `evidence_audit.unsupported_or_overclaimed`.
- Items that cannot be established from inspected material move to `evidence_audit.missing_evidence` as strings describing what is missing.
- After the audit, `evidence_audit.overall_support` is determined primarily by core claims, then secondary claims. A paper cannot receive `strong` overall support if any indispensable core claim is `missing` or `overclaimed`; if a core claim is `weak`, overall support is at most `moderate`.
