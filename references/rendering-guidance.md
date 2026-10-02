# Rendering guidance for Deep Reading v1.6

The structured JSON can be detailed; the default user-facing report should not expose all detail at once.

## Three reading layers

### Layer 1 — 3-minute judgment
Show one-sentence takeaway, research judgment card, reading priority, compact material coverage, strongest evidence, biggest weakness, and next bounded research direction.

### Layer 2 — deep reading
Show the six stable stages with concise Gap, Method Diff, experiments, claims, core weaknesses, open questions, and reading route.

### Layer 3 — evidence appendix
Show source snippets, detailed evidence metadata, material boundary, and full traceability only when the user wants to verify.

## Human-facing labels
Do not expose raw enums such as `reported`, `E2_BODY_TEXT`, `paper_only`, `null`, `cl-001`, or `ev-003` as primary visible text.

Prefer:
- reported → 作者明确说明
- inferred → 基于论文分析
- strong → 支持充分
- moderate → 有一定支持
- paper_only → 仅基于本文
- E2_BODY_TEXT → 已获取正文

## Default report size
For a typical 8–15 page methods paper, aim for a **4–6 page main report** plus an evidence appendix. Page count is a presentation target, not a scientific truncation rule.
