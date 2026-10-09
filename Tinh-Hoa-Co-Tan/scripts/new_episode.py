import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--title',required=True);p.add_argument('--fen',required=True);p.add_argument('--number',type=int,required=True)
a=p.parse_args();out=Path('episodes')/f'tap-{a.number:04d}.json'
if out.exists(): raise SystemExit(f'Already exists: {out}')
obj={'id':out.stem,'title':a.title,'subtitle':'BÀI TẬP CỜ TÀN','fen':a.fen,
     'analysis_status':'draft_not_engine_verified',
     'beats':[{'label':'MỞ ĐẦU','headline':'Thử thách', 'narration':'Viết lời bình đầy đủ tại đây.', 'insight':'Ý chính của cảnh này.', 'moves':[]},
              {'label':'GIẢI THÍCH','headline':'Giải cờ', 'narration':'Giải thích mục đích mỗi nước đi.', 'insight':'Ghi nhớ điểm quan trọng.', 'moves':[]}]}
out.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
