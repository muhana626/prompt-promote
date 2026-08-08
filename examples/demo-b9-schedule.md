# 演示：约束自检 —— 13 人排班表（B9）

> 场景来源：外部评测扩展用例 B9（WildBench v2 Planning）。完整记录见 `../tests/external-eval-expanded.md`，程序化校验脚本 `../tests/verify_b9.py`。

## 用户请求（原样，脏提示词）

> using numbers as names from 1-13 create a weekly schedule for work so everyone works 4 days a week and doesnt work 3 days . Rows should be the names and collumns should be the days of the week. Everyone should get at least a day in friday,saturday or sunday. Also, everyday at least 7 people should work so the max that people can have daily is 6. based on these create a fair schedule and try not to have people have their of back to back. Moreover search for any mistakes you may have before you provide me with an answer. In the content cells there should be an W for working and an X for not working.

（口语化、语法残缺，但可解析出 5 条约束：每人 4 工 3 休 / 周末至少一休 / 每天 ≥7 人工作 / 避免背靠背休息 / 单元格用 W 和 X。）

## 对比（程序化校验结果）

`tests/verify_b9.py` 对两张表逐项检查（13 行解析 + 约束判定）：

| 检查项 | 不装 skill | 装 skill |
|---|---|---|
| 13 行（1-13 人） | ✅ | ✅ |
| 每人恰好 4 工 3 休 | ✅ | ✅ |
| 周五/六/日至少一休 | ✅ | ✅ |
| 每天 ≥7 人工作 | ✅ | ✅ |
| 无背靠背休息（**含周日→周一环回**） | ❌ **人 6 周日+周一连续休** | ✅ |

### 不装 skill（4.5/5）

排班表本身不错，但**人 6 周日休息、周一又休息**——跨周边界的连续休息。用户要求"try not to have people have their of back to back"，而且明确说"search for any mistakes you may have"，基线在自检说明里列出了人 6 的休日 "Mon/Thu/Sun" 却没发现周日→周一相邻。

### 装 skill（5.0/5）

- 约束清单把 5 条限制**逐条显式化**（含"每天最多 6 人休息"的等价推论）
- 自检说明明确检查了 "across the week boundary: nobody rests both Sunday and Monday"——**约束自检覆盖了模型默认不会检查的跨周边界**
- 输出还附了每日人数统计与总数核对（13×4=52=7+7+8+7+8+7+8）

## 机制对应

| prompt-promote 规则 | 效果 |
|---|---|
| Step 1 约束清单：附加/隐式约束单独列出 | "避免背靠背休息"被显式化为检查项 |
| Step 4 自检四问·约束：每条约束都有对应执行动作 | 跨周边界纳入"无背靠背"的检查范围 |
| Step 4 自检四问·完整性 | 输出附每日统计，可复核 |

## 可复现

```bash
cd tests
python verify_b9.py   # 输出 baseline / skill 两组校验结果
```
