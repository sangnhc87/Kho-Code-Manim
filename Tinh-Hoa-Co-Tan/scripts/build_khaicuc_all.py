#!/usr/bin/env python3
"""Dựng toàn bộ tập khai cục theo thứ tự giáo trình khaicuc/meta.json -> khaicuc/episodes + khaicuc/index.json."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
meta = json.loads((ROOT / 'khaicuc' / 'meta.json').read_text(encoding='utf-8'))
number, index = 1, []
for item in meta['syllabus']:
    if item['slug'] == '@traps':
        out = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_khaicuc_traps.py'), '--group', str(item['group']),
                              '--size', '6', '--number', str(number)], capture_output=True, text=True, check=True).stdout
        m = re.search(r'ước tính (\d+) phút', out)
        index.append({'id': f'kc-{number:04d}', 'opening': f'bay-nhom-{item["group"]}', 'name': item['name'], 'part': 1, 'parts': 1,
                      'minutes': int(m.group(1)), 'reviewed': False})
        print(out.strip())
        number += 1
        continue
    part, total = 1, 1
    while part <= total:
        out = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_khaicuc_episode.py'), '--opening', item['slug'],
                              '--part', str(part), '--number', str(number)], capture_output=True, text=True, check=True).stdout
        m = re.search(r'phần (\d+)/(\d+).*ước tính (\d+) phút', out)
        total = int(m.group(2))
        index.append({'id': f'kc-{number:04d}', 'opening': item['slug'], 'name': item['name'], 'part': part, 'parts': total,
                      'minutes': int(m.group(3)), 'reviewed': item['reviewed']})
        print(out.strip())
        number += 1
        part += 1
(ROOT / 'khaicuc' / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
print(f'Tổng {len(index)} tập, khoảng {sum(i["minutes"] for i in index) / 60:.0f} giờ')
