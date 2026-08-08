# 网上提示词测试集调研（候选评估基准）

> 调研日期：2026-08-08
> 调研目的：为 prompt-promote 找到可用于评测的外部提示词测试集/基准，重点匹配三条核心能力线：
> **约束遵循**（意图/约束字段、自检四问）、**真实脏提示词处理**（单程加工管线）、**事实边界**（改写不添加来源外信息、不编造）。
> 结论先行：**没有现成基准直接对应"脏提示词 → 标准提示词"这条管线**；现有基准分别覆盖其子能力，需组合使用 + 保留自建用例（C01–C13）。

---

## 一、候选测试集评估表

| # | 名称 | 链接 | 内容/规模 | 与 prompt-promote 的相关性 | 建议用途 |
|---|------|------|-----------|---------------------------|---------|
| 1 | **IFEval**（Google, 2023） | 论文 arXiv:2311.07911 ✅可达；数据 HF google/IFEval ❌被墙 → 镜像 ModelScope `google/IFEval` ✅可达 | 25 类"可验证指令"（字数、关键词次数、JSON 格式等），约 500 条提示词，每条含 1+ 条可验证指令 | **高**：直接测"显式约束遵循"，对应 SKILL 的约束字段与自检"约束是否守住" | 加工后跑一遍，对比基线（干净 vs 注入 SKILL 后）的指令遵循率 |
| 2 | **IFBench**（Ai2, NeurIPS 2025） | GitHub allenai/IFBench ❌；博客 allenai.org/blog/ifbench-artificial-analysis | 58 个新的、多样的、更难的可验证指令任务，泛化 IFEval | **高**：约束遵循的"更高难度"版本 | IFEval 达标后的进阶测试 |
| 3 | **FollowBench**（2023/ACL 2024） | 论文 arXiv:2310.20410 ✅可达；数据 HF YuxinJiang/FollowBench ❌ | 5 类细粒度约束（内容/情境/风格/格式/示例），多级机制逐级叠加约束 | **高**：多约束组合正是"意图覆盖 + 约束"的极端场景 | 测加工后模型在叠加约束下不丢项 |
| 4 | **ComplexConstraints**（2025） | surgehq.ai/blog/complexconstraints-a-benchmark-for-entangled-instruction-following | 75 条专家手写提示词，1,559 条评估规则，约束互相纠缠 | 中高：约束纠缠 = 真实用户"一条提示里塞多个要求" | 抽样 10–20 条做压力测试 |
| 5 | **Inverse IFEval**（字节 Seed, 2024） | BAAI 报道 hub.baai.ac.cn/view/41354 ✅可达 | 1,012 条**中英双语**问题，覆盖 23 个领域，8 类"反直觉指令" | **高**：中文 + 反直觉指令（用户说 A 但期望模型识别反直觉意图） | 中文侧约束/意图测试首选 |
| 6 | **Multi-IF**（Meta, 2025） | 论文/报道（hub.baai.ac.cn 同文提及） | 8 种语言，4,501 条三轮对话 | 中：多轮多语言指令遵循 | 多轮场景可选 |
| 7 | **WildBench**（Ai2, 2024） | 报告 allenai.github.io/WildBench/WildBench_paper.pdf ✅可达 | 挑战性真实用户查询 + 自动评估框架 | **高**：真实用户"脏/模糊/长"查询 | 端到端"脏提示词 → 理想结果"的现成样本 |
| 8 | **WildChat**（AllenAI, 2024） | 论文 arXiv:2405.01470 ✅可达；数据 HF allenai/WildChat-1M ❌ | 100 万条真实用户-ChatGPT 对话（>250 万轮） | **高**：**脏提示词原料库**——可抽样子集作输入 | 抽样 20–50 条真实用户提示词，扩展 C01–C13 |
| 9 | **LMSYS-Chat-1M**（2023） | 论文 arXiv:2309.11998；数据 HF lmsys/lmsys-chat-1m ❌ | 100 万条真实多模型对话，21 万用户 | 中高：同 WildChat，可交叉抽样 | 交叉验证真实提示词分布 |
| 10 | **HaluEval**（人大, 2023） | GitHub RUCAIBox/HaluEval ❌ | 5,000 条通用用户查询 + 30,000 条任务样例（含幻觉标注） | **高**：直接对应"事实边界"——模型是否编造来源外内容 | 测加工后模型不编造；对照 C09/C11 污染基线 |
| 11 | **TruthfulQA**（2022） | arXiv:2109.07958 | 817 条问题，测事实性与误导 | 中高：事实性，偏知识问答，与"来源外信息"不完全同构 | 辅助参考 |
| 12 | **FActScore / LongFact**（2023） | 论文 arXiv:2305.14251 | 长文本生成逐句归因打分 | 中：细粒度归因，与"改写不添加来源外信息"直接相关 | 长文改写场景的边界检查 |
| 13 | **MT-Bench**（LMSYS, 2023） | 数据 HF lmsys/mt_bench_human_judgments ❌；question.jsonl 在 GitHub lm-sys/FastChat ❌ | 80 条多轮问题 + 3.3K 人类偏好标注 | 中：整体对话质量，非约束专测 | 一般质量参考 |
| 14 | **Natural Instructions / SUPER-NATURALINSTRUCTIONS**（2022） | GitHub allenai/natural-instructions ❌；HF Muennighoff/natural-instructions ❌ | 1,616 个 NLP 任务的自然语言指令 | 中：任务指令多样性 | 通用任务理解参考 |
| 15 | **PromptBench**（Microsoft, 2023） | GitHub microsoftarchive/promptbench（搜索结果可达，代码在 GitHub ❌） | 统一评测库 + 7 类对抗提示攻击（TextBugger/TextFooler/BertAttack/DeepWordBug/Checklist/StressTest/semantics） | 中：对抗扰动 ≈ "噪声输入"，但非用户型脏话 | 噪声鲁棒性参考 |
| 16 | **PINT**（Lakera, 2024） | GitHub lakeraai/pint-benchmark ❌ | 3,007 条英文 prompt injection 输入 | 低-中：安全注入，非本 skill 核心，但可测"意图边界"被攻击时是否坚守 | 安全边界可选测试 |
| 17 | **SuperCLUE 指令遵循（SC-On）** | superclueai.com ✅ | 中文通用大模型测评中的"精确指令遵循"维度 | 中高：中文指令遵循专测；但公开数据有限 | 中文榜单参考 |

> ❌ = 当前网络环境（中国大陆）直连不可达，需镜像/代理；✅ = 已实测可达。

---

## 二、按 prompt-promote 能力线分类

| 能力线 | 对应基准 | 说明 |
|--------|---------|------|
| 约束遵循 | IFEval、IFBench、FollowBench、ComplexConstraints、Inverse IFEval | 可验证/可叠加/纠缠/反直觉的指令 |
| 真实脏提示词 | WildBench、WildChat、LMSYS-Chat-1M | 真实用户原始输入，作为端到端输入样本 |
| 事实边界 | HaluEval、TruthfulQA、FActScore/LongFact | 不编造、不添加来源外信息 |
| 对抗/安全 | PromptBench、PINT | 噪声与注入鲁棒性（参考） |
| 中文 | Inverse IFEval（中英双语）、SuperCLUE SC-On、IFEval 中文版（EvalScope/ModelScope） | 中文指令遵循 |

---

## 三、推荐评测方案（供下一轮迭代）

1. **A 组·约束遵循**：IFEval（经 ModelScope 镜像取中文版/原版）+ FollowBench 子集。量化"注入 SKILL.md 后显式约束遵循率"的提升。
2. **B 组·真实脏提示词**：从 WildChat / LMSYS-Chat-1M 抽样 20–50 条真实用户首轮提示词（中文优先），按现有端到端流程（脏提示词 → 理想结果）打分，与 C01–C13 同量表。
3. **C 组·事实边界**：HaluEval 通用查询子集（10–20 条）+ FActScore 式逐句检查，复刻 C09/C11 污染基线的"编造/挪作理由"场景。
4. **保留并扩展自建用例**：C01–C13 是 prompt-promote 独有的测试点（"内容信任"型污染、单程加工、协议不泄漏），外部基准无法替代，建议与 A/B/C 组并行维护。

---

## 四、调研过程备注

- 工具：Firecrawl keyless 免费层（`npx -y firecrawl-cli@latest search`）+ 必应（cn.bing.com）；未消耗 API key。
- 网络实测：arXiv、ModelScope、BAAI hub、superclueai.com、allenai.github.io 可达；HuggingFace、GitHub 直连失败（000）——取数需走 ModelScope 镜像或 ghproxy 等代理。
- 局限：keyless 层有限流，未逐一抓取全部数据集卡片做深度核验；表格中规模数字来自论文摘要/搜索摘要，使用前应以数据集卡片为准。
