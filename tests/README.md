# 评测集说明

本目录是 prompt-promote 的完整评测证据：用例、输出、评分脚本与报告，均可复现。

## 数据总览

| 文件 | 内容 |
|---|---|
| `seed-cases.md` | 13 条种子用例（我拟 8 + 用户真实 5），含理想结果与隐藏陷阱 |
| `baseline.md` | 种子·干净基线（平均 4.85/5） |
| `baseline-contaminated.md` | 种子·污染基线（平均 4.65/5，注入内容信任型污染，触发 C09/C11 忠实类失败） |
| `ab-test.md` | 加工后 A/B（4.65 → 4.92，失败修复）+ v0.1.1 回归验证 |
| `external-eval.md` | 外部 pilot 14 条（3.43 → 4.54，**自评口径，已由 v2 修正，仅作方向参考**） |
| `external-eval-expanded.md` | 外部扩展 40 条（4.86 → 4.96，subagent 生成 + 机器/checklist 打分，**主口径**） |
| `overall-report.md` | 总体报告（全部轮次汇总 + 方法学修正 + 对外口径建议） |
| `verify_b9.py` | B9 排班表程序化校验脚本 |

## 用例与输出

- `fixtures/external-eval-cases.jsonl` —— pilot 14 条用例（含 prompt/ideal/gold）
- `fixtures/external-eval-cases-expanded.jsonl` —— 扩展 40 条用例
- `fixtures/outputs/` —— 40 条用例的原始输出：
  - `baseline_A.jsonl` / `skill_A.jsonl` —— A 组 12 条（IFEval + FollowBench 中文）
  - `baseline_BC.jsonl` / `skill_BC.jsonl` —— B/C 组 28 条（WildBench + TruthfulQA）
- `fixtures/report.pdf` / `report.docx` / `sales-data.csv` / `make_pdf.py` —— 种子用例 C02/C05 的测试附件

## 复现方法

### B9 程序化校验（最严格）

```bash
cd tests
python verify_b9.py
# 输出：baseline 5 项检查 4 过 1 败（人 6 跨周连休）；skill 5 项全过
```

### A 组机器打分（IFEval 约束判定）

用 `fixtures/outputs/baseline_A.jsonl` / `skill_A.jsonl` 对照 `external-eval-cases-expanded.jsonl` 中的可验证条件（词数/禁词/格式/语言）逐项判定。

### B/C 组

- B 组：对照 `external-eval-cases-expanded.jsonl` 中每条 `gold.checklist`，按通过条目数/总条目数换算（通过率 ×5）
- C 组：对照 TruthfulQA 正误答案（`fixtures/outputs/*_BC.jsonl` 中 C1-C12）

### 生成新输出（可选）

用与评测相同的设置重新生成：基线 = 未装 skill 的干净会话直接回答；加工后 = 加载 `SKILL.md` 后执行。同模型、同用例、同评分口径。

## 方法与局限（务必先读）

1. **v1（pilot 自评）高估**：+1.11 来自同一 agent 模拟双条件并自评，主观偏差约 10 倍，**不可用作结论**。
2. **v2（扩展 40 条）为准**：独立 subagent 生成输出 + 机器/checklist 打分，总体 +0.10、真实脏提示词 +0.16、0 回退。
3. **种子轮可复现**：污染注入固定、失败可定位，人工对照打分（+0.27 在脏会话口径成立）。
4. **局限**：单模型（deepseek-v4-flash）；B 组 checklist 换算粗粒度；C 组（TruthfulQA）对强模型无区分度。
