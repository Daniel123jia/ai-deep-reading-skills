---
name: paperscope-ai-deep-reading
version: 1.4.0
description: Evidence-grounded academic paper deep reading with claim-level traceability, experiment-evidence chains, assumption stress tests, and guided return-to-source reading.
---

# PaperScope AI Deep Reading v1.4

Use this skill when the user asks to deeply read, understand, audit, critique, or methodically inspect one academic paper (or a small set of closely related papers, max 5).

The goal is **not to summarize a paper so the user no longer needs the paper**. The goal is to help the user answer:

1. What does this paper actually claim?
2. What evidence supports each important claim?
3. What assumptions and boundaries does the argument depend on?
4. What remains uncertain, fragile, or unverified?
5. Where should the user return to the original paper, and why?

The canonical output is structured JSON conforming to `schemas/deep-reading-result.schema.json` v1.4. A renderer may convert it to Web, DOCX, Markdown, or PDF.

This skill is not a PDF parser, retriever, citation graph builder, venue recommender, or document formatting engine. Prefer structured source material from an upstream parser/retriever.

---

## Core principles

### 1. Evidence before interpretation
Build the source boundary and evidence inventory before drafting analysis. Do not draft a confident conclusion first and search for evidence afterward.

### 2. Paper-internal support is separate from external verification
A result can be strongly supported by the paper's own directly inspected experiments even if the result has not been independently reproduced. Track external verification separately.

### 3. `reported`, `inferred`, and `unknown` are semantic states
- `reported`: explicitly stated in inspected source material; must have evidence.
- `inferred`: PaperScope analysis grounded in inspected source material.
- `unknown`: the inspected materials genuinely do not establish the point.

Do **not** write a detailed substantive proposition and label it `unknown`.

### 4. No fake source text
`snippet` contains only short verbatim text from inspected material. Never generate, clean up, or reconstruct a plausible source quote.

### 5. No fake precision
Do not output arbitrary 0–100 scores, A+/B rankings, acceptance probabilities, or evidence percentages. Use calibrated qualitative judgments with reasons.

### 6. Guide the reader back to the paper
The final report must identify the most important sections, tables, figures, equations, and discussion passages to revisit. The report should function as a map into the original paper.

---

## Reading mode routing

Resolve `input.reading_goal` before analysis.

| Mode | Typical request | Focus |
|---|---|---|
| `standard` | 精读 / deep read / 全面分析 | Full workflow |
| `quick_summary` | 快速判断 / TL;DR | Judgment card + research question, but grounding core still runs |
| `reviewer_mode` | 审稿 / 找问题 | Claims, evidence, limitations, assumptions, reviewer questions |
| `followup_mode` | 下一步 / 研究方向 | Open questions, fragile assumptions, validation paths |
| `method_only` | 方法 / 算法 / 技术细节 | Method Diff, modules, equations, assumptions, ablations |

Default: `standard`.

Even in `quick_summary`, always run: identity → source boundary → evidence inventory → final QA.

---

## Source boundary

Separate four concepts:

- **Evidence grade**: what type of material was inspected (`E0`–`E3`).
- **Evidence coverage**: whether the inspected material is sufficient for the current reading task.
- **Locator mode**: how precisely a source can be located.
- **Context mode**: whether the analysis is paper-only or externally checked.

### Evidence grade

- `E0_TITLE_METADATA`
- `E1_ABSTRACT`
- `E2_BODY_TEXT`
- `E3_BODY_PLUS_ARTIFACTS`

`deep_reading` normally requires E2 or E3. E0/E1 produce `limited_reading`.

### Locator mode

- `page_grounded`: reliable PDF page indices exist.
- `structure_grounded`: reliable sections/figures/tables/equations exist, but page numbers are not reliable.
- `source_limited`: only metadata, abstract, or partial source snippets are reliable.

If `structure_grounded`, do not emit PDF page numbers.

### Coverage matrix

Populate source coverage for metadata, abstract, body text, sections, tables, figures, equations, appendix, supplement, code, and external literature. This is the human-meaningful explanation behind “材料覆盖：充分/部分/有限”.

---

## Paper-type lenses

Classify one primary type: `method`, `empirical`, `theory`, `review`, or `general`.

Read `references/paper-type-lenses.md` and apply the corresponding lens. Do not force a method-paper template onto empirical or theoretical work.

---

# Workflow

## Step 0 — Resolve mode and identity
Record the exact paper/version being analyzed. Distinguish the analyzed file/version from publication metadata when known.

## Step 1 — Establish source boundary
Set evidence grade, evidence coverage, locator mode, context mode, coverage matrix, and a short boundary note.

## Step 2 — Build the evidence inventory
Before drafting interpretation, enumerate the evidence-bearing source objects actually inspected:

- key problem-framing passages;
- method definitions;
- main figures/tables/equations;
- main result tables;
- ablations;
- robustness/sensitivity studies;
- datasets / samples / metrics / baselines;
- author interpretations;
- author-stated limitations / constraints;
- external context when explicitly retrieved.

Assign stable `ev-###` IDs. Each evidence ref includes an evidence role and a source locator.

For evidence that later supports claims, maintain `supported_claim_ids` backlinks.

## Step 3 — Build the paper map
Map section outline, inspected figures/tables/equations, datasets, metrics, baselines, ablations, and main references.

Mark visual/math artifacts `inspected: true` only if they were actually inspected, not merely mentioned in extracted prose.

## Step 4 — Analyze the research problem and Gap
Produce both `research_question` and `research_gap`.

Separate:

1. **Author problem framing** — what problem the paper says it addresses.
2. **Author claimed gap** — why prior approaches are said to be insufficient.
3. **PaperScope bottleneck** — the actual technical/theoretical bottleneck inferred from the paper.
4. **Gap assessment** — `established`, `partially_established`, `narrative_overreach`, or `unclear`, with evidence-backed rationale.

Do not confuse an experimental question with the underlying research Gap.

## Step 5 — Analyze the method or argument
For method papers, structure the core change as:

`Previous → Problem → Proposed → Mechanism → Expected Effect`

Then decompose major modules into:

- purpose;
- input;
- operation;
- output;
- why needed;
- measured effect, if actually tested;
- evidence refs.

For key equations/theorems that are reliably available, explain:

- what the equation is for;
- essential symbols;
- intuition;
- source verification status.

Do not invent formulas from prose.

## Step 6 — Identify assumptions
For each meaningful assumption, assign:

- `assumption_id`;
- provenance: `explicit` / `inferred`;
- risk: `low` / `medium` / `high`;
- why the method needs it;
- failure mode;
- stress test;
- evidence refs.

A hypothesis the paper is trying to prove is not automatically an assumption. Avoid circular “assumptions” such as “the proposed method is better”.

## Step 7 — Analyze contribution and novelty
Separate:

- **paper-relative delta**: what changed relative to the prior work discussed by this paper;
- **field novelty**: only populate after external literature verification.

If `context_mode = paper_only`, field novelty must remain unverified/null.

Do not treat an experiment table or benchmark coverage as a method innovation merely because it appears in the contribution list.

## Step 8 — Build experiment-evidence chains
For every experiment that materially affects the paper's conclusions, record:

`Purpose → Design → Comparison/Conditions → Result → Supported Conclusion → Unsupported Stronger Conclusion → Protocol Risks`

Read `references/experiment-evidence-rules.md`.

This step is where experiment protocol fairness, backbone comparability, metrics, sample splits, training budgets, confidence intervals, and significance evidence are assessed.

## Step 9 — Build Claim–Evidence map
For each important claim:

- stable `claim_id`;
- importance: core / secondary / context;
- plain-language claim and semantic status;
- one or more evidence links with relation (`direct`, `indirect`, `context`, `contradictory`);
- paper-internal support strength;
- why the evidence supports it;
- scope boundary;
- unsupported stronger claim;
- a **specific** action that would strengthen or stress-test it;
- external verification status.

`what_would_strengthen_it` must never be a placeholder such as “当前材料未说明”. It is an analysis output.

## Step 10 — Critical analysis
Separate:

### Author-acknowledged limitations / constraints
Only explicit author statements, with evidence.

### PaperScope analysis-derived limitations
Specific, falsifiable limitations or alternative explanations grounded in inspected material.

### Fragile assumptions
Reference assumptions by `assumption_id` and explain failure modes.

### Reviewer questions
Prefer the top 3 high-value questions rather than a long generic list.

### Applicability boundary
State where the method/argument is supported and where generalization remains untested.

## Step 11 — Open questions
Standard deep reading must produce grounded open questions when the paper supplies enough material.

Each question includes:

- origin (`author_stated` or `analysis_derived`);
- why it matters;
- a bounded validation/investigation plan;
- evidence refs.

Stop at validation. Do not automatically invent a named new network or full research proposal; that belongs to a separate innovation-generation workflow.

## Step 12 — Guided return-to-source reading
Read `references/guided-reading-rules.md`.

Produce:

- must-read locations;
- recommended locations;
- skimmable locations;
- a structured ~20-minute reading path.

Every recommended location must answer **why the reader should look there** and what they should expect to learn.

Use only locators that exist in inspected materials. If the exact table/equation number is unavailable, recommend the relevant section generically rather than inventing a locator.

## Step 13 — Contradiction check
If prose, tables, figures, supplements, or versions disagree:

- preserve both observations;
- attach both evidence refs;
- mark the affected conclusion uncertain;
- state what would resolve the discrepancy.

Never silently choose one value.

## Step 14 — Final evidence audit and QA
Before final output:

- every `reported` statement has real evidence;
- every evidence ID resolves;
- every claim-linked evidence backlink is consistent;
- structure-grounded evidence contains no PDF page numbers;
- numeric claims are supported by linked evidence containing the relevant numbers or clearly marked as indirect;
- paper-only analysis makes no field-level novelty claim;
- high-risk assumptions have failure mode + stress test;
- standard mode contains open questions and a reading guide;
- no `what_would_strengthen_it` field is a placeholder;
- author limitations and analysis limitations are not mixed;
- experiment conclusions do not exceed tested conditions.

Run `scripts/validate_result.py` after generation whenever the environment permits.

---

## Output contract

Return JSON conforming to `schemas/deep-reading-result.schema.json` v1.4.

The renderer should expose a simple six-stage user report:

1. 论文速览
2. 研究问题与 Gap
3. 核心方法与真实创新
4. 实验与证据
5. 批判性评价
6. 开放问题与精读建议

The backend schema may be richer than the visible UI.

Read `references/rendering-guidance.md` for user-facing labels. Raw enums such as `reported`, `E2_BODY_TEXT`, `paper_only`, or `null` should normally not appear in a formal report.

---

## Hard boundaries

- Do not fabricate source excerpts, locations, numbers, datasets, formulas, tables, figures, baselines, limitations, or citations.
- Do not infer page numbers under `structure_grounded`.
- Do not label a substantive, evidence-backed method statement `unknown`.
- Do not downgrade strong paper-internal evidence solely because independent replication was not checked.
- Do not claim universal superiority from a narrow benchmark.
- Do not claim field novelty from the paper's own novelty language alone.
- Do not duplicate author statements as PaperScope analysis without distinguishing provenance.
- Do not allow a claim's numerical details to be “supported” by unrelated evidence.
- Do not turn the report into a generic reviewer report unless `reviewer_mode` is requested.
- Do not generate a new manuscript or innovation proposal unless separately requested.
