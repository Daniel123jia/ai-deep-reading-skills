# Evidence Rules

Use these rules whenever the deep reading report makes a factual statement, an inference, or a criticism about a paper.

## Input Evidence Grades

Record the evidence grade separately for each paper. It describes material actually inspected, not material that may exist elsewhere.

`E0_TITLE_METADATA`: Title and metadata only. You may describe topic clues, but cannot assert method details, experiments, results, limitations, or contributions.

`E1_ABSTRACT`: Title, metadata, and abstract. You may restate author-claimed problem, method overview, and abstract-level findings, marked as reported claims.

`E2_BODY_TEXT`: Readable body text. You may analyze problem definition, method details, experiment setup, and text-reported conclusions with section or page locations when available.

`E3_BODY_PLUS_ARTIFACTS`: Body text plus figures, tables, appendix, or supplementary material. You may report precise table/figure conclusions and ablation details when evidence references locate them.

`deep_reading` requires `E2_BODY_TEXT` or `E3_BODY_PLUS_ARTIFACTS`. Use `limited_reading` for `E0_TITLE_METADATA` or `E1_ABSTRACT`.

## Statement Status

Each conclusion-like field must use one status:

`reported`: The paper explicitly reports this point in inspected material.

`inferred`: The point is a reasonable inference from inspected material, but the authors did not directly state it.

`unknown`: The inspected material does not establish the point.

Never use the paper's overall evidence grade as a replacement for statement-level evidence references.

## Wording Rules

- For `reported`, use wording such as "The paper states", "The authors report", or "Table/Figure X shows" only when a real evidence reference is available.
- For `inferred`, use wording such as "This suggests", "A reasonable inference is", or "Based on the inspected material".
- For `unknown`, use wording such as "The inspected material does not specify" or "Current materials do not establish".
- Never write "the authors believe/argue/show" for inferred or unknown statements.
- If a page, section, table, or figure location is unavailable, set the unavailable location fields to `null` and explain the limitation in the evidence note.
- "Not mentioned" does not mean "not present"; write "current materials do not specify."

## Claim-Evidence Checks

For each important claim:

- Identify the claim text in plain language.
- Assign one statement status.
- Attach one or more evidence references when available.
- Judge support strength as `strong`, `moderate`, `weak`, `missing`, or `overclaimed`.
- Explain what would strengthen the claim, such as missing baseline, ablation, statistical test, dataset diversity, or qualitative evidence.

## Downgrade Rules

Downgrade a claim when:

- The result is only shown on one dataset but generalized broadly.
- The paper claims robustness without stress tests, domain shift, or ablation evidence.
- The claimed novelty is not compared with the closest prior work.
- The method improvement is reported without enough baseline detail.
- The conclusion depends on an assumption not tested by the paper.

Unsupported claims should appear in `evidence_audit.unsupported_or_overclaimed`, not as confirmed findings.

Code, dataset availability, and reproduction runs do not upgrade paper evidence grade. Track them as separate verification status when the caller provides that information.
