# 安装与使用

## 安装

prompt-promote 是一个 agent skill（行为协议）。安装方式取决于宿主平台：

**PenguinHarness**：将本仓库的 `SKILL.md`（或整个目录）放入目标 agent 的 skills 目录：

```
<app_data_dir>/agents/<agent_id>/agent_state/skills/prompt-promote/SKILL.md
```

**其他 agent 框架**（Claude Code / Codex 等）：按平台各自的 skill/plugin 安装流程，把 `SKILL.md` 注册为 skill 即可。

## 使用

装好后**无需触发词**：agent 收到任何任务类请求，都会在内部按 SKILL.md 加工为标准提示词并执行。纯闲聊、寒暄不加工。

用户视角无感——内部加工结果不展示，回复就是最终执行结果。

## 调试

默认关闭。需要观察内部加工结果时设置环境变量：

```bash
PROMPT_PROMOTE_DEBUG=1
```

开启后执行前会输出一段"内部加工"小节（8 字段结构化提示词），仅用于开发调试。

## 验证安装是否生效

1. 跑一个带隐含约束的请求，例如："帮我写一封给老板的请假邮件，语气要既尊重又随意，大概200字"，并在会话历史里提前闲聊一句"我妈说我奶奶最近身体不太好"。
2. 若安装生效：邮件**不会**用"奶奶生病"当理由（那是历史闲聊，不是当前请求的事实锚点），理由会用占位符。
3. 对照演示：`demo-c11-leave-email.md`。

## 端到端演示

| 文件 | 演示点 | 评测证据 |
|---|---|---|
| `demo-c09-resume.md` | 事实边界·改写不添加来源外信息 | tests/baseline-contaminated.md + tests/ab-test.md |
| `demo-c11-leave-email.md` | 事实边界·历史闲聊不是事实依据 | 同上 |
| `demo-b9-schedule.md` | 约束自检·跨周边界等隐式约束 | tests/external-eval-expanded.md + tests/verify_b9.py |

完整评测集与复现方法见 `../tests/README.md`。
