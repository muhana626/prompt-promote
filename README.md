# 🧠 prompt-promote

**Messy in, faithful out.** An Agent skill that normalizes messy user prompts into structured standard prompts *internally* — then executes them faithfully. Single pass, near-zero overhead.

**[English](README.md) | [简体中文](README.zh-CN.md)** · v0.1.1 · [MIT](LICENSE)

---

## The problem

Real prompts are messy. They arrive as half-sentences, walls of noise, three tasks packed into one line, missing context — with constraints implied but never stated.

The cost isn't style. It's **intent**:

- *"帮我优化简历"* → the model invents a project you never did
- *"写封请假邮件"* → the model borrows your chat history as an excuse you never gave
- *"13 人排班，别背靠背休息"* → the model misses the Sunday→Monday boundary

One wrong assumption can ruin a resume, an email, a schedule. prompt-promote exists to keep that from happening.

## What it does

When the agent receives a prompt, prompt-promote silently:

1. **Parses** intent, constraints, fact anchors, dependencies
2. **Classifies** the task (writing / coding / analysis / translation / other)
3. **Normalizes** it into an 8-field structured prompt (role / task / context / input / constraints / output format / example / criteria)
4. **Self-checks** four questions — intent covered? scope respected? constraints kept? facts not fabricated?
5. **Executes** — the normalized prompt never appears in the reply

**You see the result, not the machinery.** One pass, no extra API round-trip (~+10–50 tokens, +0.1–0.5 s).

## Why it's worth installing

- **🎯 Faithful intent** — *"a cola"* stays *a cola*, never becomes *"a beverage"*. Everything you asked for, nothing you didn't.
- **🚫 Fabrication guard** — chat history is not fact. Rewrites never add facts beyond the source. Missing data becomes a placeholder (`XX`) or a question — never a made-up number.
- **✅ Constraint self-check** — implicit constraints are made explicit and verified: word order, tone, format, even week-boundary rest days in a work schedule.
- **⚡ Near-zero cost** — single pass; the self-check lives inside the same inference step.
- **🌐 Bilingual, user-language content** — field labels in zh/en; content always follows the user's language.
- **🔧 Debug mode** — set the environment variable to inspect the internal normalized prompt:
  - PowerShell: `$env:PROMPT_PROMOTE_DEBUG=1`
  - CMD: `set PROMPT_PROMOTE_DEBUG=1`
  - bash: `export PROMPT_PROMOTE_DEBUG=1`

## Measured, not claimed

40 external cases (IFEval / FollowBench / WildBench / TruthfulQA), independent subagent outputs, programmatic scoring:

| Scenario | Baseline | With skill |
|---|---|---|
| Clean session (13 seed cases) | 4.85 | — |
| Contaminated session (13 seed cases) | 4.65 | **4.92** |
| Real messy prompts · WildBench (16) | 4.78 | **4.94** |
| Overall external (40) | 4.86 | **4.96** |

**0 regressions** across 40 cases. The two real-world failures that started this project — an invented resume project, a fabricated sick-leave excuse — are fixed and regression-tested. Case B9 (13-person weekly schedule) passes programmatic verification *including* the week-boundary check the baseline missed.

Methodology note: the numbers above use independent outputs + machine/checklist scoring. The early self-scored pilot (+1.11) was inflated — see `tests/overall-report.md` for the honest picture.

## Quick start

```bash
# copy the skill into your agent's skills directory
cp -r prompt-promote <agent>/skills/prompt-promote
```

That's it — no triggers, no wrappers. The agent applies it to every task prompt automatically.

## Docs

- [`examples/`](examples/README.md) — install guide + 3 end-to-end demos (fabrication guard ×2, constraint self-check ×1)
- [`tests/`](tests/README.md) — full evaluation suite: cases, raw outputs, scoring scripts, reports
- [`templates/`](templates/README.md) — the 8-field skeletons for each task type

## License

[MIT](LICENSE)
