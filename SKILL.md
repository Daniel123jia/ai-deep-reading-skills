---
name: paperscope-ai-deep-reading
description: Deep-read academic papers for PaperScope by turning parsed paper content into evidence-grounded structured analysis. Use when the user asks for AI paper deep reading, paper understanding, method analysis, claim-evidence review, or research follow-up questions.
---

# PaperScope AI Deep Reading

Use this skill to analyze one academic paper or a small set of closely related papers with a PaperScope-style deep reading report.

This skill defines the reading workflow and output contract. It is not a PDF parser, paper retriever, venue recommender, ranking system, citation graph builder, or UI layout contract. Prefer receiving structured paper content: metadata, abstract, sections, paragraphs, figure/table captions, equations when available, references, and source locations such as page or section labels.

## Inputs

Accept any of these inputs:

- Parsed Paper JSON from PaperScope or another parser.
- Extracted paper text with metadata and section boundaries.
- A paper title, DOI, arXiv id, URL, or uploaded PDF when a parser/retriever is available.

If only a raw PDF or title is available, first use the available retrieval/parsing path to get structured content. If full text cannot be obtained, state the limitation and produce only a partial report from the available title, metadata, or abstract. Do not invent missing sections, experiments, figures, numbers, formulas, datasets, limitations, or claims.

Evidence grade represents material actually inspected, not material that may exist:

- `E0`: title and metadata only.
- `E1`: title, metadata, and abstract.
- `E2`: readable body text.
- `E3`: body text plus figures, tables, appendix, or supplementary material.

`deep_reading` requires at least `E2`. If the available evidence is only `E0` or `E1`, output `limited_reading` and make the limitation explicit in `global_limitations`.

## Workflow

1. Build a paper map: title, venue/year, authors if available, identifiers, evidence grade, abstract, section outline, figures/tables actually inspected, method modules, datasets, metrics, and main references.
2. Classify the paper type: `method`, `empirical`, `theory`, `review`, or `general`.
3. Identify the actual research problem and the gap the paper claims to address.
4. Extract assumptions. Separate explicit assumptions from inferred assumptions and high-risk assumptions.
5. Analyze the core idea as `previous approach -> proposed change -> mechanism -> expected benefit`.
6. Compare the method or argument against the closest prior work mentioned in the paper.
7. Build a Claim-Evidence map. Each important claim must point to evidence records when available; do not use the paper-level evidence grade as a substitute for field-level evidence.
8. Judge whether the evidence supports the paper's claims. Distinguish strong evidence, weak evidence, missing evidence, and over-claiming.
9. Produce a reviewer-style critical reading: limitations, fragile assumptions, missing baselines, statistical or evaluation risks, reproducibility concerns, and likely reviewer questions.
10. Extract follow-up research opportunities and open questions grounded in the paper.
11. Run an evidence audit before final output. Downgrade unsupported statements and label model-side analysis clearly.

For evidence labels and wording rules, read [references/evidence-rules.md](references/evidence-rules.md) when producing claims, inferences, or criticism.

## Output Contract

Return structured JSON first, conforming to [schemas/deep-reading-result.schema.json](schemas/deep-reading-result.schema.json). After the JSON, optionally provide a short human-readable summary if the user asked for conversational output.

The JSON should support frontend rendering, so keep fields concise and structured. Avoid long Markdown blobs inside fields unless a field explicitly expects prose.

## Required Report Sections

The result must include:

- `schema_version`
- `analysis_type`
- `input`
- `papers`
- `global_limitations`

Each paper in `papers` must include identity, inspected evidence, research question, method summary, contributions, evaluation or findings, limitations or unknowns, uncertainties, claim-evidence mapping, evidence audit, critical review, open questions, and a judgment card.

## Boundaries

- Do not present inferred or model-side analysis as the authors' explicit claim.
- Do not fabricate missing experiments, baselines, datasets, numbers, page locations, figure/table ids, formulas, code behavior, limitations, or citations.
- Do not turn a paper into a generic summary. Focus on problem, mechanism, evidence, limitations, and research value.
- Do not create many sub-skills or agents for a single paper by default. A single model pass sequence is enough unless the caller explicitly asks for parallel verification.
- Do not rewrite the paper or generate a new manuscript unless the user separately asks for writing help.
- Do not output quality scores, novelty scores, SOTA judgments, or rankings unless the caller provides explicit scoring rules and evidence.
- Do not mix preprint, accepted, and published versions unless the input clearly maps which evidence came from which version.
- If evidence is weak or unavailable, say so directly in the structured result.
