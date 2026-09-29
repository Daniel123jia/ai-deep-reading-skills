# Rendering Guidance — v1.5

The backend schema is technical; the user-facing report should be readable and research-oriented.

## Stable six-stage report
1. 论文速览
2. 研究问题与 Gap
3. 核心方法与真实创新
4. 实验与证据
5. 批判性评价
6. 开放问题与精读建议

## Do not expose raw enums by default
Translate:
- `reported` → 作者明确说明
- `inferred` → 基于论文分析
- `unknown` → 当前材料无法确认
- `strong` → 支持充分
- `moderate` → 有一定支持
- `weak` → 支持较弱
- `paper_only` → 仅基于本文
- `structure_grounded` → 可定位至章节/图表

Do not show `null` in a formal report. Render the meaning, e.g. “领域首创性：未进行系统外部文献核验，暂不判断。”

## Material coverage
Prefer a component view over a vague single word:
- 正文：已获取
- 章节结构：已解析
- 表格：部分解析
- 图：未视觉核验
- 公式：部分解析
- Supplement：未获取
- Code：未核验
- 外部文献：未核验

## Signature research judgment card
Show concise items:
- 核心问题
- 核心方法
- 相对本文 prior work 的真正变化
- 最强证据
- 最大风险
- 关键假设
- 最重要开放问题
- 阅读优先级 + 理由

Do not score these numerically.

## Evidence presentation
Web:
`AI judgment → 查看依据 → source / snippet / why relevant / support / boundary`

Word/Markdown:
- show a short evidence locator next to important claims;
- avoid repeating the same long source snippet multiple times;
- place full evidence excerpts in an Evidence Index/Appendix;
- support cross-links when the document format allows it.

## Claim cards
User-facing claim names should be meaningful, e.g.:
- Claim 1｜核心方法变化
- Claim 2｜主实验性能主张
- Claim 3｜消融结论

Backend ids (`cl-001`) may remain hidden.

## Experiments
Prefer:
`实验目的 → 比较条件 → 结果 → 真正支持什么 → 不能证明什么 → 协议风险`

## Assumptions
Prefer:
`假设 → 为什么需要 → 风险 → Failure Mode → 如何压力测试`

## Guided reading
The final section must tell the reader where to return to the paper and why. A 20-minute reading path should be ordered and actionable.


## v1.5 user-facing additions

- Render `claim_title` rather than exposing raw IDs such as `cl-001` as the primary heading. The internal ID may remain hidden or secondary.
- In section 05, distinguish three layers: author-acknowledged limitations, PaperScope analysis-derived limitations, and the 2–4 **core weaknesses**. Core weaknesses should be visually prominent and include why it matters, potential impact, and how to validate.
- In section 06, render Open Questions first, then **bounded research directions**, then the guided reading path. Label research directions as PaperScope-derived unless author-stated.
- Never render placeholder text such as “当前材料未说明” for `what_would_strengthen_it`, weakness validation, open-question rationale, or suggested validation.
