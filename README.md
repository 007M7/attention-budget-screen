# Attention Budget Screen

> 在 Slop 信息洪水里，先判断内容值不值得处理，再决定注意力应该花在哪里。

Attention Budget Screen 是一个开源工作流 Skill，合并了两项能力：

1. 筛查内容是否存在低信息量、低投入和批量生产风险；
2. 决定一份来源现在应该跳过、延后、参考、快速筛读还是深读。

它不是帮你读更多，而是帮你少读无效内容，把有限的时间和认知资源留给真正值得处理的来源。

## 它解决什么问题

现在打开一篇文章、一个 PDF 或一份报告之前，通常有两个问题：

```text
这段内容有没有值得处理的信息？
它现在值得占用我的注意力吗？
```

很多内容并非完全错误，但可能充满套话、情绪刺激、宏大愿景和批量化表达。它们会先消耗注意力，再让你决定要不要继续。

Attention Budget Screen 把这两个判断放进一个工作流：

```text
来源 / 文章 / PDF / 报告
          ↓
内容质量风险筛查：是否疑似 Slop
          ↓
原始注意力预算决策：现在投入多少注意力
          ↓
下一步：跳过、延后、参考、快读、深读或先核验
```

## 它具体会做什么

### 1. 筛查四个内容信号

- **具体收获**：能否复述出具体概念、事实、数据、案例或方法？
- **来源具体性**：是否有可定位的人、研究、数据、日期、链接或案例？
- **作者痕迹**：换一个账号后，内容是否仍然可以原样发布？
- **认知推进**：是否减少不确定性、提供新角度，而不只是刺激情绪？

内容风险会被表达为：低、中等、较高或暂无法判断。

### 2. 做原始注意力预算决策

注意力决策包括：

- 现在快速筛读；
- 现在值得深读；
- 与项目相关，但先放到后面；
- 只作参考；
- 稍后再看；
- 现在不投入；
- 信息不足，先补充目标。

最重要的规则是：**内容风险较高，不会自动等于跳过。**

一篇内容可能质量一般，但仍然是研究信息生态的样本；一篇内容质量不错，也可能和你当前目标无关。

## 适合什么场景

### 阅读文章前

```text
这篇公众号文章值得我现在读吗？同时帮我看看它是不是主要靠宣传叙事和情绪刺激。
```

### 面对长 PDF 或书籍

```text
这份 200 页报告我只有 15 分钟，请先判断内容风险，再告诉我应该看哪些部分。
```

### 做项目或技术研究

```text
这篇 AI Agent 基础设施文章和我的项目有关吗？哪些内容值得深读，哪些只是市场宣传？
```

### 转发或发布内容前

```text
请检查这批 AI 辅助文案是否存在低信息量和批量生产风险，不要自动发布。
```

### 个人阅读队列整理

```text
我收藏了十篇文章，请帮我区分现在快读、稍后再看、只作参考和暂时跳过。
```

## 三种使用方式

### 默认：完整工作流

```text
请使用 $attention-budget-screen，先检查这篇文章的内容风险，再判断它是否值得我现在读。
```

执行顺序：内容质量筛查 → 注意力预算决策。

### 只检查内容风险

```text
请使用 $attention-budget-screen，只检查这批内容是否存在疑似 Slop 风险，不要判断我是否应该阅读。
```

### 只做注意力决策

```text
请使用 $attention-budget-screen，只判断这份 PDF 是否值得我现在读。
```

这会保留原 Source Triage 的注意力决策能力。

## 它不是什么

- 不是 AI 文本检测器；
- 不是事实核验器；
- 不是作者动机判断器；
- 不是医学、法律或学术认证器；
- 不是内容审查器；
- 不会自动删除、屏蔽、发布、上传或写入记忆。

AI 参与生产不等于 Slop。个人经历没有学术引用，也不等于低质量。文学、讽刺、广告和娱乐内容需要结合内容类型谨慎判断。

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
请使用 $attention-budget-screen 先检查内容风险，再判断这篇来源是否值得我现在读。
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

## 与旧 Skill 的关系

新项目 `attention-budget-screen` 是推荐的统一工作流入口。

旧项目仍然保留：

- [source-triage](https://github.com/007M7/source-triage)：只做注意力预算决策的旧入口；
- [content-signal-screen](https://github.com/007M7/content-signal-screen)：只做 Slop 四信号筛查的旧入口。

旧项目不会自动改变原有契约；新用户直接安装本项目即可。

## 隐私、验证与开源许可

默认本地处理，没有遥测、没有自动上传来源、没有自动保存用户内容，也不会自动写入任何项目或长期记忆。

本地验证：

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_attention_budget_screen.py examples/full-workflow.source-attention-screen.json
```

项目包含 24 条边界评测，用于检查工作流行为和解释质量，不是准确率、节省时间或长期行为改变的证明。

本项目使用 MIT License，详见 `LICENSE` 和 `LICENSE-STATUS.md`。
