#!/usr/bin/env python3
"""One GitHub runner creates one episode. Run PYTHONPATH=. python scripts/produce.py --episode tap-0001."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.core import read_episode
from src.typst_cards import make_cards
from src.voice import generate_voice


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--episode',required=True)
    p.add_argument('--quality',choices=['preview','full'],default='preview')
    p.add_argument('--voice',choices=['edge','zalo','mock'],default='edge')
    p.add_argument('--skip-render',action='store_true')
    args=p.parse_args()
    path=ROOT/'episodes'/f'{args.episode}.json'
    if not path.is_file(): raise SystemExit(f'Episode not found: {path}')
    data=read_episode(path)
    out=ROOT/'output'/args.episode
    out.mkdir(parents=True,exist_ok=True)
    (out/'episode.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    if args.skip_render:
        print(f'Validated {args.episode} - {len(data["beats"])} segments')
        return
    timing=generate_voice(data,out/'voice',args.voice)
    make_cards(data,out/'cards')
    env=os.environ.copy();env['XIANGQI_EPISODE']=str(path);env['XIANGQI_OUTPUT']=str(out)
    quality=['-r','1920,1080','--fps','30'] if args.quality=='full' else ['-r','854,480','--fps','15']
    cmd=[sys.executable,'-m','manim',*quality,'--disable_caching',str(ROOT/'src'/'scene.py'),'XiangqiLesson','--media_dir',str(out/'media'),'-o',args.episode]
    subprocess.run(cmd,env=env,check=True,cwd=ROOT)
    matching=list((out/'media').rglob(args.episode+'.mp4'))
    if not matching: raise RuntimeError('Manim did not produce final video')
    video=matching[0]
    final=out/f'{args.episode}.mp4'
    import shutil
    shutil.copy2(video,final)
    total=sum(x['seconds'] for x in timing)
    print(f'OUTPUT {final} | narration ~{total/60:.1f} minutes')

if __name__=='__main__': main()
