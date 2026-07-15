---
name: attention-budget-screen
description: Run a bounded source workflow that screens content for low-information or mass-production risk (Slop) and then decides how much attention the source deserves. Use for articles, PDFs, reports, books, posts, transcripts, or AI-assisted content when the user asks whether it is worth reading, whether it is suspiciously slop, or both. Supports full_workflow, content_quality_only, and attention_only modes. Do not use as an AI detector, fact checker, author-intent judge, or automatic content filter.
---

# Attention Budget Screen

Use one workflow to handle two related risks in an information-flood environment:

```text
Slop / 内容污染风险筛查
          ↓
原始注意力预算决策
          ↓
跳过、延后、参考、快读、深读或先核验
```

The first stage asks whether the content shows low-information or mass-production risk. The second asks whether this source deserves the user's attention now. Keep the stages distinct: high Slop risk is evidence, not an automatic skip decision.

## Select the mode

Use `full_workflow` by default when the user gives a source and asks whether it is worth reading, or asks both content quality and reading priority.

Use `content_quality_only` when the user asks whether a post, article, script, or batch is suspiciously Slop, content-farm-like, or ready to share/publish.

Use `attention_only` when the user asks only whether a source deserves attention now, has a concrete project decision, or provides too little content for a meaningful Slop screen. Preserve the original Source Triage behavior.

Do not use this Skill for fact verification, medical/legal/academic certification, author motivation, automatic deletion, publishing, uploading, or memory writeback.

## Full workflow

1. Identify the source, user goal, attention constraint, and available content coverage.
2. Select the mode. Do not silently turn an explicit quality-only or attention-only request into the other stage.
3. In `full_workflow` or `content_quality_only`, run the content screen when正文或可代表性样本 is available:
   - `concrete_takeaway`: can the reader state a concrete concept, fact, case, data point, method, or testable claim?
   - `source_specificity`: are people, studies, data, dates, links, cases, or other locatable sources present when appropriate?
   - `author_footprint`: does the content contain concrete experience, responsibility, process detail, or judgment that cannot be swapped to any account unchanged?
   - `cognitive_progress`: does it reduce uncertainty or add a usable angle rather than only stimulate emotion?
4. If only title, thumbnail, account name, or AI disclosure is available, set the content stage to `indeterminate`; do not infer content quality.
5. In `full_workflow` or `attention_only`, run the attention gate using the smallest reliable input and the user's actual target:
   - `quick_read_now`
   - `read_deep_now`
   - `project_relevant_but_not_now`
   - `reference_only`
   - `defer_or_monitor`
   - `do_not_invest_further_now`
   - `pending_context`
6. Combine the stages into one `workflow_decision`. In `full_workflow`, this is the attention decision. In `content_quality_only`, it is `quality_screen_only`.
7. State what was inspected, uncertainty, and what was deliberately not inferred.
8. Recommend the next gate and stop. Do not automatically execute it.

## Decision rules

- `high` Slop risk does not automatically mean `do_not_invest_further_now`; user goal, decision impact, source cost, and evidence still govern attention.
- A high-value source can contain low-quality excerpts, and a low-risk source can still be irrelevant to the user's current decision.
- If content coverage is insufficient, use `indeterminate` for the content stage and continue the attention stage only when its input is sufficient.
- If attention context is insufficient, use `pending_context`; do not invent project fit.
- Use ordinal attention estimates only. Do not claim exact minutes saved or causal user outcomes.
- Do not use numeric Slop scores in v0.1; the four signals are an explainable heuristic, not a calibrated classifier.

## Hard boundaries

- AI participation does not equal Slop.
- Suspicious Slop risk does not equal falsehood, malicious intent, or zero reading value.
- Missing sources are evidence limits, not proof of low quality; personal experience and creative work do not need academic citations for every claim.
- Emotional, literary, satirical, advertising, and entertainment content needs type-aware caution.
- `indeterminate` is a valid result, not a failure.
- Do not expose private source text in public artifacts, examples, or telemetry.
- Do not route projects, install other Skills, write memory, or take external action automatically.

## Output

### 默认用户展示层

除非用户明确要求 JSON、结构化记录、评测结果或调试信息，否则必须先用中文给出可直接阅读的结论，不要把机器字段直接展示给用户，也不要以 `workflow_decision`、`mode`、`content_quality`、`attention_gate` 或 `writeback_status` 开头。

默认按以下顺序输出：

```text
先说结论：
阅读建议：现在快速筛读 / 现在值得深读 / 稍后再看 / 只作参考 / 现在不投入 / 信息不足
内容风险：低 / 中等 / 较高 / 暂无法判断

你现在怎么做：
用一句话说明下一步动作和范围。

为什么：
用一句话说明内容信号与注意力决策的关系。

四个内容信号：
- 具体收获：较强 / 一般 / 较弱 / 暂无法判断 —— 中文证据
- 来源具体性：较强 / 一般 / 较弱 / 暂无法判断 —— 中文证据
- 作者痕迹：较强 / 一般 / 较弱 / 暂无法判断 —— 中文证据
- 认知推进：较强 / 一般 / 较弱 / 暂无法判断 —— 中文证据

注意力判断：
说明实际查看范围、当前目标、主要不确定性和下一道关口。

边界：
不把内容风险当成 AI 检测、事实核验或作者动机结论。
```

字段翻译规则：

- `quick_read_now` 写成“现在快速筛读”；
- `read_deep_now` 写成“现在值得深读”；
- `project_relevant_but_not_now` 写成“与项目相关，但先放到后面”；
- `reference_only` 写成“只作参考”；
- `defer_or_monitor` 写成“稍后再看”；
- `do_not_invest_further_now` 写成“现在不投入”；
- `pending_context` 写成“信息不足，先补充目标”；
- `quality_screen_only` 写成“只完成内容风险筛查”；
- `low`、`medium`、`high`、`indeterminate` 分别写成“低”“中等”“较高”“暂无法判断”；
- `strong`、`mixed`、`weak`、`unknown` 分别写成“较强”“一般”“较弱”“暂无法判断”。

技术名称可以保留英文原名，例如 HMS、LongMemEval、LoCoMo、GitHub 和 URL；字段名、决策标签、风险等级和解释必须优先使用中文。

默认不要展示完整 inspected sections 数组、confidence 字段或 `writeback_status`。将它们转换成“已查看范围”“判断把握”“未写入任何系统”等自然语言。用户明确要求机器记录时，再在中文结论之后展示结构化字段。

### 机器记录层

需要生成或验证结构化记录时，使用 `references/output-templates.md` 中的统一 v0.1 结构：

```text
workflow_decision:
mode:
content_quality:
attention_gate:
uncertainty:
not_inferred:
recommended_next_gate:
writeback_status: none
```

The content stage must contain the four signals when evaluated. The attention stage must contain the bounded attention decision when evaluated. A `not_run` stage must be explicit.

## Resources

- Read `references/workflow-rules.md` for stage boundaries, content-type exceptions, and aggregation rules.
- Read `references/output-templates.md` when producing or validating JSON artifacts.
- Run `scripts/validate_attention_budget_screen.py` for mechanical validation.

No network, telemetry, automatic upload, automatic writeback, or installation step is required by this Skill.
