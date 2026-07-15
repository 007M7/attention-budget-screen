# Attention Budget Screen 工作流规则

## 1. 模式选择

### `full_workflow`

默认模式。用户提供来源并询问“值不值得读”“是否存在信息污染”或同时提出两个问题时使用。

流程：内容质量筛查 → 注意力预算决策。

### `content_quality_only`

用户只问内容是否疑似 Slop、是否像内容农场、是否适合转发或发布前检查时使用。

注意力阶段明确标记为 `not_run`，不得擅自决定用户是否阅读。

### `attention_only`

用户只问来源是否值得读，或来源内容不足但有明确注意力目标时使用。

内容阶段明确标记为 `not_run` 或 `indeterminate`，保留 Source Triage 的注意力决策边界。

## 2. 内容质量阶段

每个信号必须有 rating、evidence 和 confidence：

- `concrete_takeaway`：能否复述具体概念、事实、数据、案例、方法或可检验观点。
- `source_specificity`：是否有可定位的人、研究、数据、日期、链接或案例。
- `author_footprint`：是否存在具体经历、过程细节、责任承诺或不可替代判断。
- `cognitive_progress`：是否减少不确定性、提供新角度或可执行理解，而不是只刺激情绪。

信号等级：`strong`、`mixed`、`weak`、`unknown`。

### 内容阶段风险聚合

- `low`：具体内容、来源、作者痕迹或认知推进总体充分。
- `medium`：信号混合，存在部分低信息量风险。
- `high`：输入足够、至少三个信号为 `weak`、无明显类型例外、每个弱信号都有证据。
- `indeterminate`：正文不足、类型特殊或信号冲突，不能负责地判断。
- 不输出百分比、评分或“确定是 AI 生成”。

## 3. 注意力阶段

注意力阶段使用以下决策：

- `quick_read_now`：现在进行 5-15 分钟有限筛读。
- `read_deep_now`：当前决策足以支持 30-60 分钟以上深读或研究。
- `project_relevant_but_not_now`：与明确项目相关，但当前时机不对。
- `reference_only`：保留为参考索引，现在不深读。
- `defer_or_monitor`：未来可能有用，等明确触发条件。
- `do_not_invest_further_now`：可逆地决定现在不继续投入。
- `pending_context`：来源或注意力目标不足以负责地判断。

注意力阶段必须记录实际检查的 sections，并区分来源相关性、事实可信度和项目适配度。

## 4. 两阶段合并规则

- 高 Slop 风险只能进入注意力阶段的 `basis`，不能单独决定跳过。
- 低 Slop 风险也不能证明来源值得深读；深读需要用户目标和决策影响。
- 内容 `indeterminate` 时，如果标题/目录/摘要足以做注意力筛查，仍可运行注意力阶段。
- 注意力 `pending_context` 时，不能用内容风险代替用户目标。
- `full_workflow` 的 `workflow_decision` 必须等于注意力阶段的 `triage_decision`。
- `content_quality_only` 的 `workflow_decision` 必须为 `quality_screen_only`。
- `attention_only` 的 `workflow_decision` 必须等于注意力阶段的 `triage_decision`。

## 5. 内容类型例外

- 诗歌、小说、讽刺、艺术表达：来源和作者痕迹可能不是主要质量标准。
- 个人经历：外部来源少不必然低质。
- 广告与营销：情绪诉求可能是任务本身，但仍可检查具体承诺、限制和证据。
- 新闻、医学、法律、学术内容：本 Skill 不做事实或专业认证，应推荐来源核验和专家审查。
- 只有标题、封面、账号名或短摘录：内容阶段优先 `indeterminate`。

## 6. 固定否定边界

每次输出都要明确：

- 不推断 AI 作者身份；
- 不推断作者动机；
- 不把疑似 Slop 当成事实错误；
- 不把风险当成阅读价值的最终结论；
- 不自动删除、屏蔽、发布、上传或写入记忆。
