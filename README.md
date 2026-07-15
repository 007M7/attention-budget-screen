# Attention Budget Screen

> Slop 洪水里，先识别信息污染，再决定把注意力花在哪里。

Attention Budget Screen 是一个把“Slop 内容风险筛查”和“原始注意力预算决策”合并到一起的开源工作流 Skill。

它解决的不是“怎样让 AI 帮我读更多”，而是更早的一步：

```text
这段内容有没有值得处理的信息？
        ↓
它现在值得占用我的时间和认知资源吗？
        ↓
我应该跳过、延后、参考、快读、深读，还是先核验？
```

## 为什么需要它

AI 降低了内容生产成本，也让低投入、低信息量、批量生产的内容更容易淹没信息流。

这类内容不一定全部由 AI 生成，也不一定全部没有价值。真正需要的不是一个“AI 检测器”，而是一套能把内容风险和注意力决策分开的前置工作流。

Attention Budget Screen 因此把两个问题放进同一个工具流：

1. **内容质量风险**：它是否存在疑似 Slop 信号？
2. **注意力预算决策**：它现在是否值得占用你的时间？

## 四个 Slop 信号

1. **具体收获**：能否复述出具体概念、事实、数据、案例、方法或可检验观点？
2. **来源具体性**：是否有可定位的人、研究、数据、日期、链接或案例？
3. **作者痕迹**：换一个账号后，内容是否仍然可以原样发布？
4. **认知推进**：内容是否减少不确定性、提供新角度，而不只是刺激情绪？

输出：

- `low`：目前看不到明显的低信息量风险；
- `medium`：信号混合，存在部分风险；
- `high`：多个信号偏弱，疑似内容污染风险较高；
- `indeterminate`：正文不足、类型特殊或证据冲突，不能负责地判断。

## 原始注意力预算决策

注意力阶段输出一个有边界的下一步：

- `quick_read_now`：现在花 5-15 分钟有限筛读；
- `read_deep_now`：当前决策足以支持 30-60 分钟以上深读；
- `project_relevant_but_not_now`：与项目相关，但当前时机不对；
- `reference_only`：保留为参考索引；
- `defer_or_monitor`：未来可能有用，等触发条件；
- `do_not_invest_further_now`：可逆地决定现在不继续投入；
- `pending_context`：上下文不足，暂不能负责地判断。

重要边界：`slop_risk=high` 不会自动变成“跳过”。用户目标、决策影响、阅读成本和来源覆盖仍然决定注意力结论。

## 三种工作模式

### 默认：完整工作流

```text
请使用 $attention-budget-screen 判断这篇文章是否值得我现在读，也检查它是否存在疑似 Slop 风险。
```

执行：内容质量筛查 → 注意力预算决策。

### 只做内容质量筛查

```text
请使用 $attention-budget-screen，只检查这批内容是否存在疑似 Slop 风险，不要判断我是否应该阅读。
```

### 只做注意力决策

```text
请使用 $attention-budget-screen，只判断这份 PDF 是否值得我现在读。
```

这会保留原 Source Triage 的注意力决策行为。

## Codex 接入

Windows PowerShell：

```powershell
git clone https://github.com/007M7/attention-budget-screen.git "$HOME\.codex\skills\attention-budget-screen"
```

macOS / Linux：

```bash
git clone https://github.com/007M7/attention-budget-screen.git ~/.codex/skills/attention-budget-screen
```

重启 Codex 或新建任务后，使用：

```text
请使用 $attention-budget-screen 先检查这篇文章的内容风险，再判断它是否值得我现在读。
```

## Claude Code 接入

个人级安装：

```bash
git clone https://github.com/007M7/attention-budget-screen.git ~/.claude/skills/attention-budget-screen
```

项目级安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/007M7/attention-budget-screen.git .claude/skills/attention-budget-screen
```

启动 Claude Code 后，可以直接调用：

```text
/attention-budget-screen
```

## 它不是什么

- 不是 AI 文本检测器；
- 不是事实核验器；
- 不是作者动机判断器；
- 不是医学、法律或学术认证器；
- 不是内容审查器；
- 不会自动删除、屏蔽、发布、上传或写入记忆。

AI 参与生产不等于 Slop。个人经历没有学术引用，也不等于低质量。文学、讽刺、广告和娱乐内容需要结合类型谨慎判断。

## 本地验证

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_attention_budget_screen.py examples/full-workflow.source-attention-screen.json
python scripts/validate_attention_budget_screen.py examples/content-quality-only.source-attention-screen.json
python scripts/validate_attention_budget_screen.py examples/attention-only.source-attention-screen.json
```

`evals/attention-budget-screen-evals.json` 包含 24 条合并工作流评测。它用于检查边界和解释质量，不是准确率、节省时间或长期行为改变的证明。

## 与旧 Skill 的关系

旧的独立 Skill 仍然可以使用：

- [source-triage](https://github.com/007M7/source-triage)：原始注意力决策的旧载体；
- [content-signal-screen](https://github.com/007M7/content-signal-screen)：Slop 四信号筛查的旧载体。

新项目 `attention-budget-screen` 是推荐的统一工作流入口。旧项目会保留兼容性和历史实现，不自动改变其原有契约。

## 隐私与开源许可

默认本地处理，没有遥测、没有自动上传来源、没有自动保存用户内容，也不会自动写入任何项目或长期记忆。

本项目使用 MIT License，详见 `LICENSE` 和 `LICENSE-STATUS.md`。
