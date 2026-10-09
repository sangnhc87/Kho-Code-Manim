"""Render title/outro as real Typst PNG cards for the video."""
import json
import shutil
import subprocess
from pathlib import Path


def make_cards(data, folder):
    folder=Path(folder); folder.mkdir(parents=True, exist_ok=True)
    if not shutil.which('typst'):
        raise RuntimeError('Typst CLI not installed (GitHub workflow uses typst-community/setup-typst@v5).')
    labels=[('intro',data['title'],data.get('subtitle','Tuyển tập cờ tàn dễ hiểu')),
            ('outro','BẠN ĐÃ NHỚ BÍ QUYẾT?', 'Hãy thử giải lại thế cờ mà không nhìn đáp án!')]
    for kind,headline,subhead in labels:
        headline_literal=json.dumps(headline,ensure_ascii=False)
        subhead_literal=json.dumps(subhead,ensure_ascii=False)
        source='''#set page(width: 170mm, height: 91mm, margin: 10mm, fill: rgb("#101d2f"))
#set text(font: "Noto Sans", fill: rgb("#f9eee0"))
#rect(width: 150mm, height: 1.2mm, fill: rgb("#E9B66E"))
#v(7mm)
#text(size: 12pt, fill: rgb("#E9B66E"), weight: "bold")[TINH HOA CỜ TÀN]
#v(5mm)
#text(size: 23pt, weight: "bold", '''+headline_literal+''')
#v(6mm)
#text(size: 12pt, fill: rgb("#B8C9DA"), '''+subhead_literal+''')
#v(1fr)
#text(size: 10pt, fill: rgb("#E9B66E"))[Nguyễn Văn Sang  •  Mời tôi ly cà phê: MoMo 0389.821.115]
'''
        src=folder/f'{kind}.typ'
        src.write_text(source,encoding='utf-8')
        subprocess.run(['typst','compile','--format','png','--ppi','165',str(src),str(folder/f'{kind}.png')],check=True)
