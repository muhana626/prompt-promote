# prompt-promote

> A PenguinHarness skill that normalizes messy user prompts into structured standard prompts **internally** and executes them faithfully — single-pass, low overhead.

**[English](README.md) | [简体中文](README.zh-CN.md)**

**Status**: v0.1.1 (evaluated; ready to install). Evaluation evidence lives in `tests/`, overall conclusion in `tests/overall-report.md`.

## What it is

User prompts are often messy — colloquial, noisy, multi-task, missing context, carrying implicit constraints. prompt-promote normalizes them into an 8-field structured standard prompt **inside the model**:

```
【角色】ROLE  【任务】TASK  【上下文】CONTEXT  【输入】INPUT
【约束】CONSTRAINTS  【输出格式】OUTPUT FORMAT  【示例】EXAMPLE  【评判标准】CRITERIA
```

Then runs a four-question self-check (intent coverage / scope / constraints / fact boundary) and **executes directly** — the normalized prompt is never shown to the user. One pass, no extra API round-trips.

### Design highlights

- Form: a skill (`SKILL.md`) installed on an agent; the optimized prompt is not shown to the user
- Single-pass: normalize → self-check → execute; self-check lives in the same inference step (no extra model call)
- Bilingual field labels (zh/en); content language follows the user
- Lightweight task classification: writing / coding / analysis / translation / other
- Fact-boundary rules: chat history is not a fact source; never add information beyond the source material; "reasonable inference" counts as adding
- Debug mode (off by default): prints the internal normalized prompt for development

## Evaluation (honest numbers)

| Scenario | Cases | Baseline | With skill | Δ |
|---|---|---|---|---|
| Seed · clean session | 13 | 4.85 | — | — |
| Seed · contaminated session | 13 | 4.65 | 4.92 | **+0.27** |
| External · real messy prompts (WildBench) | 16 | 4.78 | 4.94 | **+0.16** |
| External · overall (IFEval/FollowBench/WildBench/TruthfulQA) | 40 | 4.86 | 4.96 | **+0.10** |

- **Zero regressions** (40 external cases: 6 improved, 34 unchanged, 0 worse)
- Gains concentrate in three mechanisms: **fact-boundary discipline** (C09 resume, C11 leave email — faithfulness failures fixed), **implicit/interactive constraint self-check** (A9 word order, B9 weekly-schedule week-boundary rest, programmatically verified), **multi-subtask completeness** (B3/B4/B7/B8)
- Almost no gain on explicit format compliance (IFEval) or knowledge tasks (TruthfulQA) — those are model-capability issues, not prompt-normalization issues
- Methodology note: the early self-scored pilot (+1.11) was inflated; the table above uses independent subagent outputs with programmatic/checklist scoring (see `tests/overall-report.md`)

## Install & usage

See [examples/README.md](examples/README.md): install into an agent's skills directory, debug mode, and three end-to-end demos (fact boundary ×2, constraint self-check ×1).

## Layout

```
prompt-promote/
├── SKILL.md                  # the skill itself (core deliverable)
├── LICENSE                   # MIT
├── README.md                 # this file (en)
├── README.zh-CN.md           # 中文 README
├── PLAN.md                   # design decisions + roadmap
├── CHANGELOG.md              # version history
├── docs/
│   └── test-sets-survey.md   # external benchmark survey (17 candidates)
├── templates/                # 8-field skeleton details + reference template
├── examples/                 # install guide + end-to-end demos
└── tests/                    # evaluation suite (cases + outputs + scripts + reports)
    ├── seed-cases.md         # 13 seed cases
    ├── baseline.md           # clean baseline (4.85)
    ├── baseline-contaminated.md  # contaminated baseline (4.65; triggers C09/C11 failures)
    ├── ab-test.md            # A/B test (4.92 after skill) + v0.1.1 regression
    ├── external-eval.md      # external pilot (14 cases, self-scored)
    ├── external-eval-expanded.md  # external expansion (40 cases, machine-scored)
    ├── overall-report.md     # overall evaluation report
    ├── verify_b9.py          # programmatic verifier for case B9
    └── fixtures/             # external cases, outputs, seed-case attachments
```

## Roadmap

1. ✅ Seed cases (13)
2. ✅ Baselines (clean 4.85 / contaminated 4.65)
3. ✅ Template v0.1 + SKILL.md
4. ✅ Post-skill effect (contaminated 4.65 → 4.92)
5. ✅ Iterate on failures (v0.1.1: protocol leakage + stricter fact boundary; regression passed)
6. ✅ Published to GitHub (Gitee pending)

## License

[MIT](LICENSE)
