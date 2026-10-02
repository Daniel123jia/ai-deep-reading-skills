---
name: paperscope-ai-deep-reading
version: 1.6.0
description: Evidence-grounded academic deep reading that helps users triage, reconstruct, verify, critique, and transfer one paper, with claim-level traceability and a guided return-to-source reading path.
---

# PaperScope / Scholar AI Deep Reading v1.6

Use this skill to deeply read one academic paper and produce a structured, evidence-grounded research judgment. The goal is **not** to replace the paper with a longer summary. The goal is to help a researcher decide:

1. Is this paper worth more attention?
2. What problem and gap does it actually address?
3. What did the paper truly change relative to its own prior-work framing?
4. What evidence supports each important claim, and where do the conclusions stop?
5. Which assumptions, weaknesses, failure modes, and missing controls matter most?
6. What should the reader return to in the original paper, and what follow-up questions are worth testing?

The canonical output is JSON conforming to `schemas/deep-reading-result.schema.json` v1.6. Rendering is delegated to Scholar-Format-Engine.

This skill is not a PDF parser, bibliography manager, novelty-search engine, reviewer-decision engine, or document formatter. Prefer reliable source material from an upstream parser/retriever.

---

## Product philosophy: five research-reading tasks

Every standard run should internally follow this sequence:

`Triage → Reconstruct → Verify → Critique → Transfer`

### Triage
Decide why the paper may be worth the reader's time. Identify the core problem, real method delta, strongest evidence, biggest risk, and recommended reading priority.

### Reconstruct
Rebuild the research logic:

`Problem → Prior limitation → Gap/Bottleneck → Core idea → Method/Argument → Expected effect`

### Verify
Map major claims to the experiments, tables, figures, equations, proofs, or source passages that support them. Separate paper-internal support from external replication.

### Critique
Identify the 2–4 most consequential weaknesses, fragile assumptions, missing controls, alternative explanations, and failure modes. Critique must be specific and falsifiable.

### Transfer
Extract bounded open questions, follow-up research directions, and a source-grounded 20-minute reading route. Do not invent a named architecture or full research proposal unless a separate innovation-generation task is requested.

Read `references/researcher-reading-framework.md` for the full internal model.

---

## Core principles

### 1. Evidence before interpretation
Build the source boundary and evidence inventory before writing analytical conclusions.

### 2. Evidence inventory must be explicit
Before analysis, identify where the paper's central evidence actually lives: problem framing, method definition, main results, ablations/sensitivity tests, limitations, and critical artifacts.

### 3. Paper-internal support ≠ external verification
A paper can internally support a claim strongly even when no third-party replication has been checked. Track these separately.

### 4. Provenance is semantic
- `reported`: explicitly stated in inspected paper material; requires evidence.
- `inferred`: Scholar AI/PaperScope analysis grounded in inspected material.
- `unknown`: the inspected material genuinely does not establish the point.

Never write a substantive proposition and label it `unknown` merely because the paper did not phrase the analysis exactly that way.

### 5. No fake source text or locators
`snippet` is verbatim source text only. Do not reconstruct quotations. Do not invent page, figure, table, equation, or section numbers.

### 6. No fake precision or pseudo-ranking
Do not output arbitrary 0–100 scores, A+/B grades, or acceptance probabilities. Use qualitative judgments with reasons.

### 7. Critical + creative reading
Do not only ask “what is wrong?”. Also identify what idea is worth preserving, what mechanism is transferable, and which unresolved question could support a useful follow-up study.

### 8. Main report should guide the reader back to the paper
The deep-reading result must include a reading guide. The report is a navigation layer over the paper, not a substitute for the paper.

---

## Reading modes

Resolve `input.reading_mode` first.

| Mode | Purpose | Default emphasis |
|---|---|---|
| `standard` | normal deep reading | full five-task workflow |
| `quick_summary` | fast triage | judgment card + problem/gap + grounding core |
| `reviewer_mode` | critique | claims, evidence, weaknesses, reviewer questions |
| `followup_mode` | research continuation | fragile assumptions, open questions, validation paths |
| `method_only` | technical mechanism | Method Diff, modules, equations, assumptions, ablations |

Even `quick_summary` must run identity → source boundary → evidence inventory → QA.

---

## Source boundary

Track four independent concepts:

- **Evidence grade**: material type inspected (`E0`–`E3`).
- **Evidence coverage**: whether the material is enough for the requested reading task.
- **Locator mode**: how precisely evidence can be located.
- **Context mode**: paper-only vs external verification.

### Locator modes

- `page_grounded`: reliable PDF page indices exist.
- `structure_grounded`: reliable section/figure/table/equation/block locators exist, but page numbers are unreliable.
- `source_limited`: only metadata, abstract, or partial excerpts are reliable.

If `structure_grounded`, never emit PDF page numbers.

Populate the component-level coverage matrix for body text, sections, tables, figures, equations, appendix, supplement, code, and external literature.

---

## Paper lenses

Classify one primary lens and at most one secondary lens:

- `method`
- `empirical`
- `theory`
- `review`
- `resource`
- `discovery`
- `clinical`
- `materials`
- `general`

Choose by argument/evidence structure, not field name. A methods paper with a substantial dataset contribution may use `method + resource`.

Read `references/paper-type-lenses.md`.

---

# Workflow

## Step 0 — Identify the exact paper/version
Record the analyzed file/version separately from publication metadata. Do not silently merge arXiv, conference, and journal versions.

## Step 1 — Establish the source boundary
Set evidence grade, coverage, locator mode, context mode, coverage matrix, and boundary note.

## Step 2 — Build the evidence inventory
Before interpretation, assign stable `ev-###` IDs to inspected evidence.

At minimum, inventory:

- problem framing;
- method/argument definition;
- main results;
- central ablations or sensitivity analyses;
- experimental protocol;
- author limitations/constraints;
- essential figures/tables/equations;
- missing critical evidence.

Populate `evidence_inventory` before drafting the report.

## Step 3 — Build the paper map and paper lens
Map sections, figures, tables, equations, datasets/samples, metrics, baselines, ablations, and major references. Mark artifacts inspected only when actually inspected.

## Step 4 — Triage / research judgment
Create a concise judgment card answering:

- core problem;
- core method;
- paper-relative innovation;
- strongest evidence;
- biggest risk / weakness;
- most important assumption/open question;
- why the paper is worth reading;
- the most promising bounded next research direction;
- reading priority and reason.

This is the “3-minute decision layer”, not a full summary.

## Step 5 — Reconstruct the research problem and Gap
Separate:

1. Author problem framing.
2. Author-claimed gap.
3. Scholar AI/PaperScope analysis of the actual bottleneck.
4. Gap assessment: `established`, `partially_established`, `narrative_overreach`, or `unclear`.

Do not confuse an experimental question with the actual research Gap.

## Step 6 — Reconstruct the method/argument
For method papers, use:

`Previous → Problem → Proposed → Mechanism → Expected Effect`

Then decompose key modules into purpose, input, operation, output, why needed, measured effect (if tested), and evidence.

For essential formulas/theorems, explain purpose, symbols, intuition, and verification status. Never reconstruct missing formulas from prose.

## Step 7 — Audit assumptions
For each meaningful assumption:

`Assumption → Why Needed → Failure Mode → Stress Test`

An empirical hypothesis that the paper is trying to establish is not automatically an assumption. Avoid circular assumptions such as “the proposed method is better”.

## Step 8 — Separate paper-relative delta from field novelty
- `paper_relative_delta`: what changed relative to the prior work discussed by the paper.
- `field_novelty`: only after external literature verification.

When `context_mode = paper_only`, field novelty stays unverified/null.

## Step 9 — Build experiment-evidence chains
For every experiment that materially affects the conclusion, record:

`Purpose → Claim tested → Design/Conditions → Result → Supported conclusion → Unsupported stronger conclusion → Protocol risks`

Assess baseline fairness, backbone parity, data augmentation, sample split, budget, uncertainty, significance, oracle inputs, and generalization where relevant.

Read `references/experiment-evidence-rules.md`.

## Step 10 — Build the Claim–Evidence map
Each important claim requires:

- stable `claim_id` and short user-facing `claim_title`;
- importance: core / secondary / context;
- claim provenance;
- evidence links with relation: direct / indirect / context / contradictory;
- paper-internal support strength;
- support reason;
- scope boundary;
- unsupported stronger claim;
- a concrete strengthening/stress-test plan;
- external verification status.

`what_would_strengthen_it` is an analysis output. In standard mode, it must never be a placeholder such as “当前材料未说明”.

## Step 11 — Critical analysis
Keep three layers distinct.

### Author-acknowledged limitations / constraints
Only what the authors explicitly state, with evidence.

### Analysis-derived limitations
Specific concerns or alternative explanations inferred from inspected evidence.

### Core weaknesses
Select only the 2–4 most consequential weaknesses. Each must include:

- what the weakness is;
- why it matters;
- potential impact on claims/generalization;
- related claim/assumption IDs;
- concrete validation or stress test;
- evidence refs.

Avoid generic criticism such as “more experiments are needed” unless you specify which experiment and what it would test.

## Step 12 — Open questions and bounded research directions
Each open question must include:

- question;
- origin (`author_stated` / `analysis_derived`);
- why it matters;
- suggested validation;
- evidence basis.

Then derive a small number of research directions from the strongest weaknesses/open questions. Stop at target problem + rationale + validation focus. Do not invent a named model/network by default.

## Step 13 — Guided return-to-source reading
Produce:

- must-read locations;
- recommended locations;
- skimmable locations;
- a structured ~20-minute path.

Each path step includes an approximate minute budget, why to read it, and the expected takeaway. Use only verified locators.

Read `references/guided-reading-rules.md`.

## Step 14 — Optional transferable-knowledge sidecar
If useful, populate `knowledge_takeaways` with transferable concepts, methods, formulas, experimental designs, or evaluation practices. This is for future knowledge-base workflows and is **not** a seventh main report section by default.

## Step 15 — Contradiction check
When paper prose, tables, figures, supplements, or versions disagree, preserve both observations, attach evidence, mark the conclusion uncertain, and state what would resolve the discrepancy.

## Step 16 — Final QA
Before output, verify:

- every `reported` statement has real evidence;
- every evidence ID resolves;
- evidence backlinks to claims are coherent;
- numeric claims are grounded in the linked evidence or explicitly marked indirect;
- source-locator rules are respected;
- paper-only analysis does not claim field novelty;
- high-risk assumptions include failure mode + stress test;
- core weaknesses are specific and testable;
- standard mode contains substantive open questions and reading guidance;
- no strengthening/why-it-matters field contains placeholders;
- author limitations and analysis criticism are not mixed;
- experiment conclusions do not exceed tested conditions;
- the 20-minute path uses real locators and totals roughly 15–25 minutes.

Run `scripts/validate_result.py` whenever the environment permits.

---

## User-facing output contract

Return JSON conforming to `schemas/deep-reading-result.schema.json` v1.6.

The renderer should expose only six stable stages:

1. 论文速览
2. 研究问题与 Gap
3. 核心方法与真实创新
4. 实验与证据
5. 批判性评价
6. 开放问题与精读建议

The backend may be much richer than the visible report. Do not add a seventh main section merely because an internal object exists.

### Default presentation intent

- first layer: 3-minute research judgment;
- second layer: deep analysis;
- third layer: evidence appendix / source verification.

Read `references/rendering-guidance.md`.

---

## Hard boundaries

- Do not fabricate excerpts, locators, numbers, formulas, tables, figures, baselines, limitations, citations, or metadata.
- Do not infer page numbers under `structure_grounded`.
- Do not call paper-relative delta “field novelty” without external verification.
- Do not downgrade paper-internal evidence solely because independent replication was not checked.
- Do not force a fixed number of weaknesses or failure cases by inventing filler.
- Do not output accept/reject decisions unless the user explicitly requests reviewer-mode judgment in a separate review workflow.
- Do not turn bounded research directions into named architectures or full proposals unless the user asks for innovation generation.
- Do not generate a longer report simply because more schema fields exist; analysis depth and presentation length are separate concerns.
