# mm-write-novel｜小说创作 Skill

`mm-write-novel` 是一个面向 Codex 的原创小说工作流 Skill。它不以“一次生成很多字”为目标，而是把成熟作者与编辑的工作方式固化为可持续项目：从灵感、市场定位、故事圣经、人物与世界、总纲和章节卡，到正文、连续性、伏笔、双语同步和完结审计。

## 能做什么

- 创建中文短篇、中篇、长篇与百万字级连载；
- 续写、重构、修订、补线、查错和规划完结；
- 适配番茄、知乎、微信读书、掌阅、七猫及平台中立项目；
- 面向英语大众商业小说、移动付费连载、社区连载和类型长连载；
- 为西方题材并行维护完整中文审核稿与英文海外稿；
- 用外置账本管理事实、时间线、人物认知、关系、地点、资源、故事线、伏笔和读者问题；
- 自动建立项目骨架、索引正文、统计篇幅、装配最小上下文包并检查结构化错误；
- 每次启动主动提供范例、推荐默认值和下一步入口。

## 安装

将 `mm-write-novel/` 目录复制到个人 Skills 目录：

```bash
git clone https://github.com/CodeBlueFriend/mm-write-novel.git
cp -R mm-write-novel/mm-write-novel ~/.codex/skills/mm-write-novel
```

重启 Codex 或新开任务后，使用 `$mm-write-novel` 显式调用。也可把整个仓库放在任意工作目录中，要求 Codex 使用其中的 `mm-write-novel/SKILL.md`。

## 30 秒开始

直接发送任意一种请求：

```text
使用 $mm-write-novel。我只有一句灵感：一个殡仪馆化妆师发现每位死者都梦见同一扇门。请先给我三个短篇方向。
```

```text
使用 $mm-write-novel。规划一部 30 万字番茄男频连载：失去神力的河神在现代县城做水利员。先做项目启动单，不写正文。
```

```text
使用 $mm-write-novel。把这个西方题材做成中英双语移动连载，中文稿用于国内审核，英文稿面向美国读者；先帮我确定边界和故事引擎。
```

如果只说“我想写小说”，Skill 会给出可直接选择的范例，而不是要求先填一整张表。

## 创建项目目录

脚本仅使用 Python 标准库：

```bash
python3 mm-write-novel/scripts/init_project.py ./projects/my-novel \
  --title "潮汐县志" \
  --mode long \
  --language zh-CN
```

参数：

| 参数 | 可选值 | 说明 |
|---|---|---|
| `--title` | 任意文本 | 项目书名，可稍后更改 |
| `--mode` | `short` / `novella` / `long` / `serial` | 篇幅与规划粒度 |
| `--language` | `zh-CN` / `en` / `bilingual` | 单语或中英双语 |
| `--force` | 开关 | 只补齐缺失文件；不会覆盖已有文件 |

初始化后，先编辑或让 Skill 完成 `00-project-brief.md`。双语项目自动创建 `manuscript-zh/`、`manuscript-en/` 和映射账本；单语项目创建 `manuscript/`。

## 推荐工作流

1. 启动单：确定创作模式、篇幅、题材、平台、市场、语言交付和审核方式。
2. 市场定位：区分平台长期特征、当前趋势和限时活动。
3. 故事发现：锁定一句话故事、命题、故事引擎与结局承诺。
4. 故事圣经：确认人物、世界规则、秘密、伏笔方向、声纹和禁区。
5. 结构：按短篇节拍、中篇章弧、长篇分卷或连载三层规划推进。
6. 章节卡：写清 POV、进入状态、欲望、阻力、转折、退出状态和阅读动力。
7. 正文：通常每批 1—3 章；超长连载可每批 1—5 章。
8. 审核：先功能与因果，再连续性与人物，最后才是语言。
9. 锁定：通过后更新全部账本和摘要，生成下一批最小上下文包。
10. 完结：检查主线、人物弧、关系、伏笔、研究项和双语一致性。

默认“严格确认模式”会在市场方向、故事圣经、总体结构、首批章节卡与首批正文后等待确认。熟悉流程后可使用辅助确认或自动推进；任何 BLOCKER、结局改变和双语故事层分叉仍会暂停。

## 日常命令

```bash
# 检查必需文件、CSV 表头、引用章节和双语映射
python3 mm-write-novel/scripts/validate_project.py ./projects/my-novel

# 统计中英文正文的章节数、字符数和词数
python3 mm-write-novel/scripts/manuscript_stats.py ./projects/my-novel

# 建立章节索引
python3 mm-write-novel/scripts/index_manuscript.py ./projects/my-novel

# 检查时间线、人物认知和资源台账中的可检测问题
python3 mm-write-novel/scripts/continuity_checks.py ./projects/my-novel

# 检查逾期、孤儿和缺少公平性证据的伏笔
python3 mm-write-novel/scripts/foreshadowing_checks.py ./projects/my-novel

# 装配写下一批章节所需的最小上下文
python3 mm-write-novel/scripts/build_context_pack.py ./projects/my-novel --chapters CH006 CH007

# 导出隐藏控制信息与连续性更新的纯净合订稿
python3 mm-write-novel/scripts/compile_manuscript.py ./projects/my-novel
```

所有检查脚本成功返回 `0`；发现问题返回 `1`；用法或文件错误返回 `2`。脚本只做确定性的结构检查，不能替代文学判断或事实核验。

## 项目事实层

项目目录中的 `continuity/` 是正式事实源：

- `canon.yaml`：锁定人物、世界规则和核心秘密；
- `timeline.csv`：事件时间、地点、参与者与持续时间；
- `character-state.csv` / `knowledge-state.csv`：人物状态与信息边界；
- `relationship-ledger.csv`：关系、信任、债务和称呼变化；
- `props-resources.csv`：关键道具、证据、金钱、能力与所有权；
- `plot-thread-ledger.csv` / `foreshadowing-ledger.csv`：故事线与伏笔生命周期；
- `reader-question-ledger.csv`：读者正在等待的答案；
- `bilingual-sync-ledger.csv`：双语章节、场景、共享事实和差异审批。

锁定正文后必须同步更新账本。任何锁定事实变更都要先在 `change-log.md` 写影响范围，不能在聊天里悄悄改掉。

## 双语项目原则

中文稿和英文稿共享人物、事件、因果、秘密、伏笔与结局，但分别写作。中文稿应能独立送国内平台审核；英文稿应符合目标地区语言和文化默认知识，而非逐句翻译。称呼、解释密度、段落节奏等属于表达差异；年龄、人物认知、事件顺序或结局变化属于故事层分叉，必须明确批准。

## 目录

- `mm-write-novel/SKILL.md`：触发、路由、审核门和资源选择；
- `references/`：按任务加载的工作流、市场、题材和审核知识；
- `assets/`：项目启动单、故事圣经、章节矩阵、账本和审核报告模板；
- `scripts/`：零第三方依赖的项目工具；
- `tests/`：脚本回归测试。

## 设计边界

- 市场信号有时效；联网复核后才把最新榜单或政策作为当前依据。
- 只抽象参考作品的节奏、叙事距离等维度，不复制人物组合、关键设定和情节链。
- 不模仿在世作家的可识别风格；优先建立作者自己的声纹。
- 医疗、法律、历史、地域文化等高风险事实必须标记来源和核验状态。
- “无 Bug”指可结构化硬矛盾在锁定前清零，不承诺替代专业审读。

## 许可证

MIT
