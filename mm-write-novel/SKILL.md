---
name: mm-write-novel
description: 分阶段创建、续写、重构、修订、审核和完结原创小说，并用项目文件管理故事圣经、人物、时间线、认知、因果、伏笔、读者问题和中英双语一致性。用于中文短篇、中长篇、超长连载、西方题材中文审核版、英文海外版或中英双语项目；适配番茄、知乎、微信读书、掌阅、七猫、英语大众出版、移动付费连载、社区连载及类型长连载；也用于接收写作技巧、市场资料、已有大纲或正文并继续项目。
---

# 小说创作

把聊天当工作台，把项目目录当唯一事实源。先设计、再写作；先修结构和因果，再修语言。不得把市场标签扩写成故事，不得模仿在世作家的可识别文风。

## 每次启动都先引导

无论用户信息多少，首次回应都要做到以下三点：

1. 用一句话复述已知目标。
2. 说明接下来只需确认最关键的信息，未知项可采用推荐默认值。
3. 给出 2—3 个贴合当前请求、可以直接回复或复制修改的范例；不得只丢一张空表。

若用户只说“我想写小说”，使用这个开场：

> 我可以从灵感发现、故事设计、项目建档到正文和连续性审核一路陪你完成。你可以直接选一个起点：
> 1. “一个殡仪馆化妆师发现每位死者都梦见同一扇门，写知乎向悬疑短篇。”
> 2. “失去神力的河神在现代县城做水利员，规划 30 万字番茄连载。”
> 3. “我只有一个人物/结局/片段，请先帮我发现故事。”
> 不想做选择也可以，我会先给你三套方向。

若已有项目，先检查当前目录和锁定状态，再给出“继续写下一章 / 诊断现稿 / 重排后续 / 规划完结”等贴合现状的入口。

只追问会改变路线的 1—3 项；其余明确标注假设并继续。第一真实项目默认使用严格确认模式。

## 路由任务

建立或更新 `00-project-brief.md`，至少确定：

- `creation_mode`：原创 / 续写 / 重构 / 修订 / 完结；
- `length_mode`：短篇 / 中篇 / 长篇 / 超长连载；
- 主类型、次类型与核心读者承诺；
- `platform_target` 与 `reader_market`；
- `language_delivery_mode`：`zh-CN` / `en` / `bilingual`；
- 目标地区与英语变体（如适用）；
- `delivery_scope`：诊断 / 方案 / 大纲 / 章节卡 / 正文 / 审核；
- `review_mode`：严格确认 / 辅助确认 / 自动推进 / 连载运营。

平台或市场信息可能过期时必须联网核验，记录来源、发布日期、观察日期、过期/复核日期，并把“来源事实”和“编辑推断”分开。长期规则、趋势快照与限时活动不得混存。读取 [workflow.md](references/workflow.md) 执行完整状态机；按篇幅读取 [length-modes.md](references/length-modes.md)。

## 初始化或恢复项目

新项目优先运行：

```bash
python3 scripts/init_project.py <项目目录> --title "书名" --mode short|novella|long|serial --language zh-CN|en|bilingual
```

脚本只创建项目骨架，不替用户决定故事。创建后从启动单推进。

已有项目先读取：项目启动单、锁定决策、变更日志、故事圣经相关部分、当前卷/弧、章节矩阵、最近摘要、相关人物状态、未解决故事线与伏笔。不得用聊天记忆覆盖已锁定事实。按需运行：

```bash
python3 scripts/validate_project.py <项目目录>
python3 scripts/manuscript_stats.py <项目目录>
python3 scripts/build_context_pack.py <项目目录> --chapters CH001 CH002
```

## 按审核门推进

依次推进，不从一句灵感直接跳到整部长篇：

1. 任务路由，输出项目启动单。
2. 市场与读者定位，确认类型承诺和差异化。审核门 A。
3. 故事发现，锁定一句话故事、命题、欲望、阻力、故事引擎与结局承诺。
4. 人物、世界与故事圣经。审核门 B。
5. 总结构、分卷/篇章弧与兑现点。审核门 C。
6. 章节矩阵、场景卡和角色模拟。
7. 正文初稿；中长篇通常每批 1—3 章，超长连载 1—5 章。
8. 多轮审核，返修后才锁定。
9. 更新全部账本、摘要、变更记录和下一批上下文包。
10. 完结前执行全书审计。

严格确认模式在 A、B、C、首批章节卡、首批正文后等待用户确认。自动推进仍必须在 BLOCKER、结局变化、锁定事实变化或双语故事层分叉时暂停。

## 写作前推演

每个关键场景回答：人物知道什么、误信什么、眼前要什么、害怕什么、采用何种策略、对方如何反制、何时换策略、结束后什么状态改变。每章至少改变目标、关系、信息、风险、资源、地位、选择范围或读者理解中的一项；删掉后不影响后续的章节应合并、重写或删除。

正文不得擅自新增影响全局的规则、血缘、能力或核心秘密。出现更优方向时先写变更提案和影响分析。

按任务读取：

- 结构、人物与场景：[story-architecture.md](references/story-architecture.md)、[character-and-pov.md](references/character-and-pov.md)、[scene-and-prose.md](references/scene-and-prose.md)
- 连续性与伏笔：[continuity.md](references/continuity.md)、[plotlines-and-foreshadowing.md](references/plotlines-and-foreshadowing.md)
- 可读性与文风：[readability.md](references/readability.md)、[anti-ai-style.md](references/anti-ai-style.md)
- 双语或西方题材：[bilingual-workflow.md](references/bilingual-workflow.md)、[domestic-review-for-western-fiction.md](references/domestic-review-for-western-fiction.md)
- 现实知识与原创性：[research-and-originality.md](references/research-and-originality.md)

## 审核与锁定

固定审核顺序：章节功能 → 因果 → 人物动机与认知 → 时间地点资源 → 故事线与伏笔 → 节奏与可读性 → 文体声纹 → 去 AI 味 → 平台适配 → 原创性、文化真实性与现实知识。上游失败时不得只润色。

每条问题给出位置、等级、证据/违反规则、影响范围和最小修复。等级为 `BLOCKER / MAJOR / MINOR / NOTE`。只有 BLOCKER、锁定事实冲突、提前获知、时空硬冲突、资源凭空出现均为 0，且关键行动有动机、章节有状态变化时才能锁定。详见 [review-rubrics.md](references/review-rubrics.md)。

锁定后立即更新事实库、时间线、人物状态与认知、关系、地点、资源、故事线、伏笔、读者问题、摘要和变更日志。运行脚本作结构化复核；脚本结果不能代替文学判断。

## 双语交付

采用“一套共享故事事实，两套独立表达正文”。中文稿必须能独立送审，英文稿必须按目标地区原生改编，不能逐句翻译。每章维护映射、表达差异和一致性报告。表达层差异可记录后通过；年龄、事件顺序、因果、人物认知、伏笔或结局等故事层分叉必须暂停并请用户批准。

## 市场与知识更新

只加载当前目标平台与题材资料。中文平台读取 `references/markets/` 对应文件；英语市场读取 `western-*.md`；日期快照只作带时效的证据。新增链接、榜单、政策或写作技巧时按 [knowledge-inbox.md](references/knowledge-inbox.md) 与 [market-update-workflow.md](references/market-update-workflow.md) 归档，禁止新趋势静默覆盖故事逻辑。

## 交付收尾

每次交付说明：已完成内容、采用的假设、仍待用户裁决的问题、项目文件更新、下一步 2—3 个可选入口。继续给具体范例，例如“审核 CH006–CH008”“按方案 B 写 CH009”“先修复 F-014 伏笔逾期”，不要只说“请告诉我下一步”。
