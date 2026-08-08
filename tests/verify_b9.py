# -*- coding: utf-8 -*-
"""B9 排班表程序化校验：宽松解析（忽略列头/汇总列，只取 W/X 单元格）。
检查：13 行、每人恰好 4 工 3 休、周五/六/日至少一天休、每天>=7 人工作、无背靠背休息（含周日->周一环回）。
"""
import json, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FILES = {
    'baseline': 'fixtures/outputs/baseline_BC.jsonl',
    'skill':    'fixtures/outputs/skill_BC.jsonl',
}

def get_b9(path):
    for line in open(path, encoding='utf-8'):
        d = json.loads(line)
        if d.get('id') == 'B9':
            return d.get('output', '')
    return ''

def parse_table(text):
    """提取 markdown 表格所有数据行，每行返回 [cell...]（strip 后）。"""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            # 跳过表头行：包含星期名或 Name
            joined = ' '.join(cells)
            if re.search(r'(?i)monday|tuesday|wednesday|thursday|friday|saturday|sunday|name', joined):
                continue
            if all(re.fullmatch(r'-+', c) for c in cells if c):
                continue
            rows.append(cells)
    return rows

def verify(rows):
    """返回 (ok, details)。"""
    details = []
    # 每行取前 7 个 W/X 单元格（忽略 'Days worked' 数值列）
    sched = []
    for r in rows:
        wx = [c for c in r if c in ('W', 'X')]
        if len(wx) < 7:
            details.append(f'行 {r} 的 W/X 单元格不足 7 个: {wx}')
            continue
        sched.append(wx[:7])

    checks = {}
    checks['13 行'] = len(sched) == 13
    if not checks['13 行']:
        details.append(f'解析到 {len(sched)} 行（期望 13）')
        for r in rows:
            details.append('  ROW: ' + repr(r))

    ok = True
    if checks['13 行']:
        # 1. 每人恰好 4 工 3 休
        counts = [row.count('W') for row in sched]
        checks['每人 4 工 3 休'] = all(c == 4 and row.count('X') == 3 for row, c in zip(sched, counts))
        if not checks['每人 4 工 3 休']:
            ok = False
            details.append('  工休计数: ' + str(counts))
        # 2. 周五/六/日至少一天休（列 4/5/6）
        fri_sat_sun = [any(row[i] == 'X' for i in (4, 5, 6)) for row in sched]
        checks['周五/六/日至少一休'] = all(fri_sat_sun)
        if not checks['周五/六/日至少一休']:
            ok = False
            details.append('  缺周末休的人: ' + str([i+1 for i, v in enumerate(fri_sat_sun) if not v]))
        # 3. 每天 >= 7 人工作（即每天 X 数 <= 6，13 人）
        daily_work = [13 - sum(row[i] == 'X' for row in sched) for i in range(7)]
        checks['每天>=7人工作'] = all(n >= 7 for n in daily_work)
        if not checks['每天>=7人工作']:
            ok = False
            details.append('  每日工作人数: ' + str(daily_work))
        # 4. 无背靠背休息（含周日->周一环回）
        b2b = []
        for idx, row in enumerate(sched, 1):
            days = [i for i, v in enumerate(row) if v == 'X']
            for a, b in zip(days, days[1:]):
                if b - a == 1:
                    b2b.append((idx, a, b))
            if 0 in days and 6 in days:
                b2b.append((idx, 6, 0))
        checks['无背靠背休息'] = len(b2b) == 0
        if b2b:
            ok = False
            details.append('  背靠背休息: ' + str(b2b))
    else:
        ok = False

    return ok, checks, details

for name, path in FILES.items():
    text = get_b9(path)
    print('=' * 30, name.upper())
    if not text:
        print('!! 未找到 B9 输出')
        continue
    rows = parse_table(text)
    print(f'解析出 {len(rows)} 行数据')
    ok, checks, details = verify(rows)
    for k, v in checks.items():
        print(f'  [{("PASS" if v else "FAIL")}] {k}')
    for dline in details:
        print('  DETAIL: ' + dline)
    print(f'  ==> 总体: {"全部通过" if ok else "存在问题"}')
    print()
