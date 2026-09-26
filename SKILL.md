---
name: paperscope-ai-deep-reading
description: Use when the user asks for AI paper deep reading, paper understanding, method analysis, claim-evidence review, assumption audit, or research follow-up questions in PaperScope.
---

# PaperScope AI Deep Reading

Use this skill to analyze one academic paper or a small set of closely related papers (up to 5) with a PaperScope-style deep reading report.

This skill defines the reading workflow, output contract, and reading mode routing. It is not a PDF parser, paper retriever, venue recommender, ranking system, citation graph builder, or UI layout contract. Prefer receiving structured paper content: metadata, abstract, sections, paragraphs, figure/table captions, equations when available, references, and source locations such as page or section labels.

Version `1.2` is an evidence-grounding upgrade. The frontend may still render the familiar six-stage report, but the structured output must support claim-level evidence panels: source, source excerpt, paraphrase, support relation, support strength, scope boundary, and unsupported stronger conclusions.

---

## Reading Mode Routing

Before starting analysis, resolve the `input.reading_goal` field to one of the following modes. If the user does not specify, default to `standard`.

| Mode | Trigger phrases | Primary output focus |
|---|---|---|
| `quick_summary` | "一句话总结", "摘要", "quick take", "tldr" | Emphasize `judgment_card` + `research_question`; keep the full JSON shell |
| `standard` | default, "精读", "deep read", "全面分析" | Full report, all sections |
| `reviewer_mode` | "审稿", "peer review", "找问题", "挑毛病" | `critical_review` + `claim_evidence` + `evidence_audit` emphasized |
| `followup_mode` | "研究方向", "follow-up", "下一步", "open questions" | `open_questions` + `method_summary` + `contributions` emphasized |
| `method_only` | "方法", "算法", "how it works", "技术细节" | `method_summary` + `assumptions` + `claim_evidence` emphasized |

In `quick_summary` mode, keep only `judgment_card` and `research_question` substantive. Always run the grounding core first: paper identity, source boundary, evidence coverage, locator mode, evidence inventory, and final evidence audit. Other required fields may be empty arrays or valid placeholder objects. In all other modes, run the full workflow and adjust emphasis in the human-readable summary.

---

## Inputs

Accept any of these inputs:

- Parsed Paper JSON from PaperScope or another parser.
- Extracted paper text with metadata and section boundaries.
- A paper title, DOI, arXiv id, URL, or uploaded PDF when a parser/retriever is available.

If only a raw PDF or title is available, first use the available retrieval/parsing path to get structured content. If full text cannot be obtained, state the limitation and produce only a partial report from the available title, metadata, or abstract. Do not invent missing sections, experiments, figures, numbers, formulas, datasets, limitations, or claims.

Evidence grade represents material actually inspected, not material that may exist:

- `E0_TITLE_METADATA`: title and metadata only.
- `E1_ABSTRACT`: title, metadata, and abstract.
- `E2_BODY_TEXT`: readable body text.
- `E3_BODY_PLUS_ARTIFACTS`: body text plus figures, tables, equations, appendix, or supplementary material.

`deep_reading` requires at least `E2_BODY_TEXT`. If the available evidence is only `E0_TITLE_METADATA` or `E1_ABSTRACT`, output `limited_reading` and make the limitation explicit in `global_limitations`.

Record evidence grade separately from:

- `evidence_coverage`: whether the available material sufficiently covers the claims this reading task needs to evaluate.
- `locator_mode`: whether evidence can be grounded by page, by structure only, or only by source-limited hints.
- `context_mode`: whether the analysis is paper-only, targeted external check, or externally verified.

Use locator modes as follows:

- `page_grounded`: reliable PDF page locations are available.
- `structure_grounded`: readable source structure is available, but page numbers are unreliable or absent.
- `source_limited`: only metadata, abstract, or partial snippets are available.

Evidence references must separate real source text from model paraphrase. `snippet` is reserved for short verbatim text from parsed source material. If no real source text is available, set `snippet: null` and provide a `paraphrase` or verification suggestion instead. Do not write model-generated prose into `snippet`.

---

## Workflow

Run steps in order. Steps 1–2 are a coarse pass; step 3 onward uses the paper type to guide depth.

**Step 0 — Resolve reading mode.**
Check `input.reading_goal` and set the active mode per the routing table above.

**Step 1 — Coarse paper scan.**
Record: title, venue/year, authors if available, identifiers, evidence grade, abstract, rough section list, and a preliminary paper type guess. Also establish `source_boundary`: evidence grade, evidence coverage, locator mode, and context mode. This is a fast pass; details are filled in later steps.

**Step 2 — Classify paper type.**
Based on the coarse scan, classify as `method`, `empirical`, `theory`, `review`, or `general`. This classification governs how deeply to analyze each section. For example, a `theory` paper warrants deeper attention to equations and proofs; an `empirical` paper warrants deeper attention to datasets, metrics, and baselines.

**Step 3 — Build full paper map.**
Using the paper type from step 2, complete the paper map and evidence inventory: section outline with summaries and locations, figures/tables/equations actually inspected, datasets, metrics, baselines, ablations, author-stated limitations, and main references. Mark each figure, table, and equation as `inspected: true` or `inspected: false`.

**Step 4 — Identify the research problem and gap.**
State the actual research problem and the gap the paper claims to address. Distinguish what the paper says the gap is (reported) from your assessment of whether it is a real gap (inferred).

**Step 5 — Extract and classify assumptions.**
For each identifiable assumption, classify two independent dimensions:

- `provenance`: `explicit` if the paper states it directly, or `inferred` if implied by method design or experiment setup.
- `risk_level`: `low`, `medium`, or `high` depending on how severely failure would affect the core claim.

For high-risk assumptions, include a failure mode and testability note. Also surface them in `critical_review.fragile_assumptions`.

**Step 6 — Analyze core idea.**
Structure the method as `previous_approach → proposed_change → mechanism → expected_benefit`. Each component is an `evidence_statement` with a status and evidence refs. For main modules, use structured module objects: purpose, input, operation, output, why needed, measured effect, and evidence refs.

**Step 7 — Compare against prior work.**
Compare the method or argument against the closest prior work mentioned in the paper. Separate `paper_relative_delta` from `field_novelty`. Without targeted external checks, do not claim field-level novelty, first-in-field status, or universal originality. Anchor every comparison to evidence refs, not to your general knowledge of the field.

**Step 8 — Build Claim-Evidence map.**
For each important claim, assign a stable `claim_id`, importance (`core`, `secondary`, `context`), evidence refs, support strength, support reason, scope boundary, unsupported stronger claim, and what would strengthen it. Do not use the paper-level evidence grade as a substitute for statement-level evidence references.

**Step 9 — Evaluate support quality.**
Judge whether the evidence supports the paper's claims. Populate `evidence_audit` with strongly supported, weakly supported, and unsupported/overclaimed items. For the audit application of downgrade and protect rules, read `references/evidence-rules.md`.

**Step 10 — Critical review.**
Produce a reviewer-style critical reading: main limitations, fragile assumptions, missing baselines, statistical or evaluation risks, reproducibility concerns, and likely reviewer questions. Record fragile assumptions in `critical_review.fragile_assumptions`, not merged into `main_limitations`.

**Step 11 — Open questions and follow-up opportunities.**
Extract follow-up research opportunities and open questions grounded in the paper. Each item must include why it matters and a suggested next step.

**Step 12 — Evidence audit pass.**
Before producing final output, scan every field that contains a factual statement. Downgrade any statement not supported by an evidence ref. Label model-side analysis with `inferred` status. Move unsupported statements to `evidence_audit.unsupported_or_overclaimed`. Ensure every `reported` statement has a real evidence ref, every cited evidence ref exists, and no `snippet` was model-generated.

For wording rules and downgrade/protect criteria, read `references/evidence-rules.md`.

---

## Output Contract

Return structured JSON first, conforming to `schemas/deep-reading-result.schema.json` v1.2. After the JSON, optionally provide a short human-readable summary if the user asked for conversational output.

The JSON must support frontend rendering: keep fields concise and structured. Avoid long Markdown blobs inside fields unless a field explicitly expects prose.

---

## Required Report Sections

The result must always include:

- `schema_version`
- `analysis_type`
- `input` (with `reading_mode` populated)
- `papers`
- `global_limitations`

Each paper in `papers` must include identity, evidence grade, source boundary, evidence refs, paper map, research question, method summary (with assumptions and structured modules), contributions, novelty verification, evaluation or findings, limitations or unknowns, uncertainties, claim-evidence mapping, evidence audit, critical review (with fragile assumptions), open questions, and a judgment card.

In `quick_summary` mode, only `research_question` and `judgment_card` should contain substantive analysis. All other schema-required paper fields must still be present as empty arrays or valid placeholder objects, never omitted.

---

## Boundaries

- Do not present inferred or model-side analysis as the authors' explicit claim.
- Do not fabricate missing experiments, baselines, datasets, numbers, page locations, figure/table/equation ids, formulas, code behavior, limitations, or citations.
- Do not fabricate source snippets. `snippet` must come from real parsed source text; otherwise use `snippet: null`.
- Do not turn a paper into a generic summary. Focus on problem, mechanism, evidence, assumptions, limitations, and research value.
- Do not create many sub-agents for a single paper by default. A single model pass sequence is enough unless the caller explicitly requests parallel verification.
- Do not rewrite the paper or generate a new manuscript unless the user separately asks for writing help.
- Do not output novelty scores, SOTA rankings, or acceptance predictions unless the caller provides explicit scoring rules and verified evidence.
- Do not mix preprint, accepted, and published versions unless the input clearly maps which evidence came from which version.
- Do not state field-level novelty, "first", "unprecedented", or "SOTA across the field" unless `context_mode` indicates external verification and the evidence refs support the claim.
- Do not over-downgrade. If a claim has clear experimental support (e.g., a comparison table with multiple baselines and standard metrics), it may be `strong` or `moderate` even without external replication. See `references/evidence-rules.md` for protect rules.
- The 5-paper limit per call exists to preserve output quality and avoid context fragmentation. For larger sets, run multiple calls and merge results at the application layer.
- If evidence is weak or unavailable, say so directly in the structured result.
