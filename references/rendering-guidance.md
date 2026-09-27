# Human-Readable Rendering Guidance

The structured JSON is a backend contract. A polished Word/Markdown/Web report should translate backend enums into natural language and avoid showing implementation noise.

## Recommended Chinese labels

| Backend value | User-facing label |
|---|---|
| `reported` | 作者明确说明 / 论文明确报告 |
| `inferred` | 基于论文分析 |
| `unknown` | 当前材料无法确认 |
| `strong` | 支持充分 |
| `moderate` | 有一定支持 |
| `weak` | 支持较弱 |
| `missing` | 缺少证据 |
| `overclaimed` | 结论超出证据范围 |
| `paper_only` | 仅基于本文 |
| `targeted_external_check` | 已做定向外部核验 |
| `externally_verified` | 已做外部核验 |
| `page_grounded` | 可定位至 PDF 页码 |
| `structure_grounded` | 可定位至章节/图表/公式 |
| `source_limited` | 材料定位有限 |

Do not repeatedly print raw values such as `[reported]`, `[unknown]`, `E2_BODY_TEXT`, `structure_grounded`, or `paper_only` in formal prose.

## Six-stage rendering map

### 01 论文速览
Use:
- identity;
- source boundary summary;
- judgment card;
- one-sentence takeaway;
- research value;
- reading priority.

### 02 研究问题与 Gap
Use:
- research question;
- relevant author framing;
- PaperScope inferred bottleneck/gap assessment when available.

### 03 核心方法与真实创新
Use:
- method summary;
- structured modules;
- assumptions;
- contributions;
- novelty verification.

### 04 实验与证据
Use:
- evaluation/findings;
- claim-evidence items;
- evidence audit;
- contradiction items relevant to results.

### 05 批判性评价
Keep separate subsections:
- 作者明确指出的局限/约束;
- PaperScope 分析出的局限;
- 脆弱假设;
- Reviewer Questions;
- 适用边界.

### 06 开放问题与精读建议
Use:
- open questions;
- suggested validation;
- must-read/recommended/skim guide;
- 20-minute reading path.

## Evidence snippet policy

Evidence snippets are centralized in `evidence_refs`.

For Word/Markdown:

- show a snippet the first time it materially helps;
- later references may show only evidence id + location;
- avoid repeating the same quote several times;
- a final Evidence Index/Appendix may collect snippets.

For Web:

- prefer `查看依据` expansion at claim level;
- show source location, snippet, paraphrase, support relationship, and scope boundary.

## External verification

Do not repeat “not externally replicated” after every experimental sentence.

Show external verification once in a suitable metadata/audit area and only repeat it when it materially affects a specific claim.

Paper-internal evidence and external replication are distinct.
