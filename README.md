# prompt-promote

> 将用户非标准格式的提示词在内部加工为结构化标准提示词并直接执行，忠实覆盖用户意图，单程、低开销的 PenguinHarness skill。

**状态**：v0.1.1（评测完成，可安装试用）。完整评测证据见 `tests/`，总体结论见 `tests/overall-report.md`。

## 这是什么

用户发来的提示词常常是脏的——口语化、夹带噪声、多任务混装、省略上下文、隐含约束。prompt-promote 在**模型内部**把它加工成 8 字段结构化标准提示词：

```
【角色】ROLE  【任务】TASK  【上下文】CONTEXT  【输入】INPUT
【约束】CONSTRAINTS  【输出格式】OUTPUT FORMAT  【示例】EXAMPLE  【评判标准】CRITERIA
```

随后做自检四问（意图覆盖 / 范围不超 / 约束不丢 / 事实不虚构），再**直接执行**——加工过程不展示给用户，单程、无额外 API 往返。

### 设计要点

- 形态：skill（`SKILL.md`），装到 agent 上内联使用，优化后的提示词不展示给用户
- 单程加工：一次加工 → 执行；自检嵌入同一次推理的思考阶段
- 标记级双语：结构字段中英双写，内容语言跟随用户
- 轻量任务分类：writing / coding / analysis / translation / other
- 事实边界规则：历史闲聊非事实依据；改写材料不添加来源外信息；"合理推断"同样属于添加
- debug 模式（默认关）：开启时打印内部加工结果

## 评测结果（诚实口径）

| 场景 | 用例数 | 基线 | 加工后 | Δ |
|---|---|---|---|---|
| 种子·干净会话 | 13 | 4.85 | — | — |
| 种子·脏会话污染 | 13 | 4.65 | 4.92 | **+0.27** |
| 外部·真实脏提示词（WildBench） | 16 | 4.78 | 4.94 | **+0.16** |
| 外部·总体（IFEval/FollowBench/WildBench/TruthfulQA） | 40 | 4.86 | 4.96 | **+0.10** |

- **0 回退**（40 条外部用例：6 条改善、34 条持平、0 条回退）
- 提升集中在三类机制：**事实边界纪律**（C09 简历不编造、C11 请假不虚构理由——忠实类失败修复）、**隐式/交互约束自检**（A9 词序、B9 排班表跨周边界连休，程序可验证）、**多子任务完整性**（B3/B4/B7/B8）
- 对显式格式遵循（IFEval）与模型知识类任务（TruthfulQA）几乎无增益——那是模型能力问题，不是提示词加工问题
- 方法学说明：早期自评 pilot 的 +1.11 高估；上表为独立 subagent 生成输出 + 机器/checklist 打分口径（详见 `tests/overall-report.md`）

## 安装与使用

见 [examples/README.md](examples/README.md)：安装到 agent 的 skills 目录、debug 模式、以及三个端到端演示（事实边界 ×2、约束自检 ×1）。

## 目录结构

```
prompt-promote/
├── SKILL.md                  # skill 本体（核心交付物）
├── LICENSE                   # MIT
├── README.md
├── PLAN.md                   # 设计决策 + 路线图
├── CHANGELOG.md              # 版本记录
├── docs/
│   └── test-sets-survey.md   # 外部测试集调研（17 个候选基准评估）
├── templates/                # 8 字段骨架详解 + 参考模板
├── examples/                 # 安装说明 + 端到端演示
└── tests/                    # 评测集（用例 + 输出 + 评分脚本 + 报告）
    ├── seed-cases.md         # 13 条种子用例
    ├── baseline.md           # 干净基线（4.85）
    ├── baseline-contaminated.md  # 污染基线（4.65，触发 C09/C11 忠实类失败）
    ├── ab-test.md            # A/B 测试（加工后 4.92，失败被修复）+ v0.1.1 回归
    ├── external-eval.md      # 外部评测 pilot（14 条，自评口径）
    ├── external-eval-expanded.md  # 外部评测扩展（40 条，机器口径）
    ├── overall-report.md     # 总体评测报告
    ├── verify_b9.py          # B9 排班表程序化校验脚本
    └── fixtures/             # 外部用例、输出、种子用例附件
```

## 路线图

1. ✅ 收集种子用例（13 条）
2. ✅ 测基线（干净 4.85 / 污染 4.65）
3. ✅ 起草模板 v0.1 + SKILL.md
4. ✅ 测加工后效果（污染 4.65 → 4.92）
5. ✅ 按失败案例迭代（v0.1.1：协议泄漏 + 事实边界收紧，回归通过）
6. ✅ 开源发布

## License

[MIT](LICENSE)
