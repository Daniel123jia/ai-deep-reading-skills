---
name: paperscope-ai-deep-reading
description: Use when the user asks for AI paper deep reading, paper understanding, method analysis, claim-evidence review, assumption audit, research follow-up, or evidence-grounded paper interpretation in PaperScope / Scholar AI.
---

# PaperScope AI Deep Reading

Use this skill to deep-read one academic paper or a small set of closely related papers (up to 5) and return an evidence-grounded structured report.

The skill is responsible for reading logic, evidence discipline, critical analysis, and structured output. It is not a PDF parser, retriever, citation-graph builder, venue recommender, ranking system, document formatter, or UI contract.

Version `1.3` focuses on **consistency and report completeness**. It strengthens status assignment, source-boundary consistency, author-vs-analysis limitation separation, claim-level external-verification tracking, open-question generation, reading guidance, contradiction handling, and semantic validation.

The frontend may still render the familiar six-stage report:

1. 论文速览
2. 研究问题与 Gap
3. 核心方法与真实创新
4. 实验与证据
5. 批判性评价
6. 开放问题与精读建议

The structured JSON must remain richer than the visible UI so important judgments can be traced to evidence without exposing backend implementation details.

---

## Reading Mode Routing

Resolve `input.reading_goal` before analysis. If unspecified, use `standard`.

| Mode | Typical triggers | Main emphasis |
|---|---|---|
| `quick_summary` | 一句话总结, 摘要, quick take, tldr | judgment card + research question |
| `standard` | 精读, deep read, 全面分析 | full report |
| `reviewer_mode` | 审稿, peer review, 找问题 | critical review + claim-evidence + audit |
| `followup_mode` | 下一步, research direction, open questions | open questions + assumptions + follow-up validation |
| `method_only` | 方法, 算法, how it works | method + assumptions + claim-evidence |

Always run the grounding core even in `quick_summary`:

`identity → source boundary → evidence inventory → status assignment → final audit`.

Do not skip grounding merely because the requested output is short.

---

## Inputs

Accept:

- Parsed Paper JSON.
- Extracted paper text with metadata and structural boundaries.
- A title, DOI, arXiv id, URL, or uploaded PDF when a retriever/parser exists upstream.

If only title/metadata/abstract is available, produce a visibly limited reading rather than inventing unseen content.

### Evidence grade

- `E0_TITLE_METADATA`: title and metadata only.
- `E1_ABSTRACT`: metadata + abstract.
- `E2_BODY_TEXT`: readable body text.
- `E3_BODY_PLUS_ARTIFACTS`: body text + inspected figures/tables/equations/appendix/supplement.

`deep_reading` requires E2 or E3. E0/E1 must use `limited_reading`.

Evidence grade is not the same as coverage, locator precision, or external verification.

### Source boundary

Every paper must establish:

- `evidence_grade`: what material was actually inspected.
- `evidence_coverage`: whether those materials sufficiently cover this reading task.
- `locator_mode`: how precisely evidence can be located.
- `context_mode`: paper-only vs external checking.
- `boundary_note`: concise statement of what can and cannot be claimed.

Locator modes:

- `page_grounded`: reliable PDF page indices are available.
- `structure_grounded`: section/figure/table/equation structure is reliable, but PDF page indices are not.
- `source_limited`: only metadata, abstract, or partial excerpts are reliable.

Hard consistency rule:

- If `locator_mode = structure_grounded`, all evidence `location.page` values must be `null`.
- If `locator_mode = source_limited`, page/figure/table/equation locators must be `null` unless the inspected limited source itself explicitly supplies that locator.
- Do not advertise a weaker locator mode while emitting stronger locators.

### Evidence snippets

`snippet` is reserved for short verbatim text copied from inspected source material.

- Never synthesize, rewrite, translate, or repair a `snippet`.
- Put model interpretation in `paraphrase`.
- If no source excerpt is available, use `snippet: null`.

---

## Status Semantics

Use statement status carefully:

### `reported`
The inspected paper explicitly states the point. Attach one or more real evidence refs.

### `inferred`
The point is PaperScope/agent analysis grounded in inspected material, but the authors do not state it directly.

### `unknown`
The inspected material genuinely does not establish the point.

Critical rule:

> Do not write a detailed positive proposition and label it `unknown`.

If you can specifically describe the method, contribution, result, limitation, or mechanism from inspected material, it is normally `reported` or `inferred`. `unknown` should usually describe non-establishment, for example: “Current materials do not establish whether the gain persists under domain shift.”

Do not use `unknown` as a safe default.

---

## Workflow

Run the steps in order.

### Step 0 — Resolve reading mode

Set `input.reading_mode`.

### Step 1 — Coarse scan and source boundary

Record identity, abstract, section list, tentative paper type, source boundary, and available materials.

Do not infer publication status from an arXiv source alone. Preserve the analyzed version separately through `identity.version_note` when known.

### Step 2 — Classify paper type

Choose `method`, `empirical`, `theory`, `review`, `general`, or `unknown` based on argument/evidence structure.

Paper type changes emphasis but does not change evidence rules.

### Step 3 — Build evidence inventory and paper map

Enumerate before drafting conclusions:

- metadata and source version;
- section outline;
- inspected figures/tables/equations;
- datasets/populations;
- metrics/outcomes;
- baselines/comparators;
- ablations/stress tests;
- author-stated limitations/constraints;
- important experimental results;
- main references discussed by the paper.

Mark inspected artifacts explicitly. Do not treat artifact names mentioned in prose as visually inspected artifacts unless actually inspected.

### Step 4 — Identify research problem and gap

State the research question and the paper-claimed gap.

Distinguish:

- author framing (`reported`);
- PaperScope assessment of the actual bottleneck (`inferred`).

Do not convert the paper’s rhetoric into independently verified field history.

### Step 5 — Extract assumptions

Each assumption needs:

- stable `assumption_id`;
- `provenance`: `explicit` or `inferred`;
- `risk_level`: `low`, `medium`, or `high`;
- evidence refs;
- failure mode when meaningful;
- a concrete stress-test idea when meaningful.

High-risk assumptions must also appear in `critical_review.fragile_assumptions` by `assumption_id`.

### Step 6 — Analyze method and mechanism

Structure the method as:

`previous_approach → proposed_change → mechanism → expected_benefit`.

For major modules capture:

- module name;
- purpose;
- input;
- operation;
- output;
- why needed;
- measured effect if directly tested;
- evidence refs.

If module purpose or effect is inferred rather than stated, label the relevant statement accordingly.

### Step 7 — Assess contribution and novelty carefully

Separate:

- `paper_relative_delta`: what changes relative to the prior work the paper itself discusses;
- `field_novelty`: only after targeted external prior-art checking.

If `context_mode = paper_only`, `field_novelty` must be `null`.

Do not call something first, unprecedented, field-novel, or broad SOTA merely because the authors do.

### Step 8 — Build Claim–Evidence map

Create stable claim ids and include only meaningful claims.

For each claim record:

- `claim_id`;
- importance: `core`, `secondary`, or `context`;
- claim text + `reported`/`inferred` status;
- evidence refs;
- `paper_internal_support`;
- why the evidence supports the claim;
- scope boundary;
- a stronger conclusion the evidence does not justify, if any;
- a concrete action that would strengthen or broaden the claim;
- external verification status.

`paper_internal_support` measures support inside the inspected paper only.

> Absence of external replication must not automatically lower paper-internal support.

Track external verification separately.

`what_would_strengthen_it` is an analysis field. Do not answer “current materials do not specify.” Propose a concrete baseline, ablation, statistical test, domain test, replication, robustness check, or other bounded validation when useful.

### Step 9 — Evidence support audit

Apply downgrade and protect rules from `references/evidence-rules.md`.

Important:

- a directly reported comparison can strongly support a bounded paper-internal claim without third-party replication;
- broad generalization still requires broader evidence;
- claim scope and evidence scope must match.

### Step 10 — Separate limitations correctly

Create two distinct layers:

#### Author-acknowledged limitations

Only include limitations, constraints, caveats, or unresolved issues explicitly acknowledged in inspected paper text. These must be `reported` and evidence-grounded.

Do not place agent-generated criticism here.

#### Analysis limitations

Place PaperScope/agent-derived limitations, alternative explanations, missing controls, generalization risks, reproducibility concerns, and evaluation risks in `critical_review.analysis_limitations` and related fields. These are analysis, not author statements.

### Step 11 — Generate open questions and reading guide

Open questions may be `author_stated` or `analysis_derived`.

In `standard` and `followup_mode`, when E2/E3 material is available and the paper contains identifiable assumptions, limitations, anomalies, parameter sensitivity, missing conditions, or unresolved evidence, derive useful open questions rather than waiting for an explicit “Future Work” section.

Each open question must include:

- question;
- origin;
- why it matters;
- suggested validation;
- evidence refs.

Stop at **how to test the question**. Do not automatically invent a new named network/module/architecture. Innovation generation belongs to a separate workflow.

Also produce `reading_guide`:

- must-read sections/tables/figures/equations;
- recommended items;
- skimmable items;
- a concise ordered `twenty_minute_path`.

Use only locators available in inspected material. Never invent an equation/table/section merely to complete the guide.

### Step 12 — Detect contradictions and evidence mismatches

When prose, tables, figures, supplements, or multiple source blocks disagree:

1. record both sides;
2. do not silently choose one;
3. explain the impact;
4. state what would resolve it.

Also check that quantitative claims are actually supported by their referenced evidence. If a claim contains a number not present in the cited evidence and no other cited source establishes it, downgrade or split the claim.

### Step 13 — Final audit

Before output:

- every `reported` statement has evidence refs;
- every evidence ref resolves;
- `unknown` is not used for a detailed positive claim;
- source-boundary and locator usage are consistent;
- source snippets are genuine source text;
- author limitations and analysis limitations are separate;
- external verification did not improperly lower paper-internal support;
- paper-relative delta is separated from field novelty;
- high-risk assumptions link by `assumption_id`;
- claim quantitative details match cited evidence;
- `what_would_strengthen_it` is concrete, not a placeholder;
- standard deep readings include useful open questions when defensible;
- standard deep readings include a reading guide;
- contradictions are surfaced rather than silently reconciled.

Run `scripts/validate_result.py` when available.

---

## Output Contract

Return structured JSON first, conforming to `schemas/deep-reading-result.schema.json` v1.3.

A conversational summary may follow when requested.

Keep structured fields concise. Evidence snippets live centrally under `evidence_refs`; do not duplicate long source excerpts throughout the JSON.

---

## Human-Readable Rendering Rules

Structured enums are backend values. Formal Word/Markdown/Web reports should translate them into natural language.

Examples:

- `reported` → 作者明确说明 / 论文明确报告
- `inferred` → 基于论文分析
- `unknown` → 当前材料无法确认
- `strong` → 支持充分
- `moderate` → 有一定支持
- `weak` → 支持较弱
- `paper_only` → 仅基于本文
- `structure_grounded` → 可定位至章节/图表

Do not print raw labels such as `[unknown]`, `[reported]`, `E2_BODY_TEXT`, or `structure_grounded` repeatedly inside a polished user-facing report unless the user explicitly requests technical metadata.

Do not repeat the same evidence snippet every time an evidence id is referenced. A renderer may show the snippet once and later references as `Evidence E-003` / `查看依据`.

See `references/rendering-guidance.md`.

---

## Required Paper Report Components

Every standard paper report must include:

- identity;
- source boundary;
- evidence refs;
- paper map;
- research question;
- method summary;
- assumptions;
- contributions;
- novelty verification;
- evaluation/findings;
- author-acknowledged limitations;
- unresolved unknowns;
- claim-evidence mapping;
- evidence audit;
- critical review;
- open questions;
- reading guide;
- contradictions;
- judgment card.

`quick_summary` may leave deep-analysis arrays empty, but must still establish source boundary and grounding.

---

## Boundaries

- Do not fabricate experiments, baselines, datasets, numbers, pages, figures, tables, equations, formulas, code behavior, limitations, citations, or source snippets.
- Do not use `unknown` as a blanket safety label for content that is actually supported.
- Do not confuse lack of external replication with weak paper-internal evidence.
- Do not present author framing as externally verified history.
- Do not claim field-level novelty without external verification.
- Do not mix preprint/accepted/published versions without source mapping.
- Do not output novelty scores, acceptance predictions, or fake precision ratings.
- Do not turn open questions into automatically designed new methods unless the user separately asks for innovation generation.
- Do not create many sub-agents by default for a single paper.
- The 5-paper limit preserves reasoning quality; larger sets should be chunked by the application layer.
