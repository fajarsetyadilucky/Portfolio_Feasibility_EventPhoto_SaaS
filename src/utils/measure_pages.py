from pathlib import Path

content = Path('reports/Laporan_Kelayakan_Bisnis_CEO_EventPhoto_SaaS.html').read_text(encoding='utf-8')
parts = content.split('<!-- ====================')
for i, pt in enumerate(parts[1:], 1):
    print(f'Part {i} length: {len(pt)} chars')
