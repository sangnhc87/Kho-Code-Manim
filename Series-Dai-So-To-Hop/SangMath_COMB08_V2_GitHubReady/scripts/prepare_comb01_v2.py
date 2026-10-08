#!/usr/bin/env python3
"""Prepare COMB01 v2: compile Typst formulas and produce synchronized Vietnamese TTS.

Examples:
  python scripts/prepare_comb01_v2.py --voice off
  python scripts/prepare_comb01_v2.py --voice on --voice-name vi-VN-NamMinhNeural

GitHub Actions has network access; offline systems can build silent pedagogical
video of the same length with --voice off.
"""
import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from comb01_lesson_data import BEATS, FORMULAS, CHAPTER_LABELS, spoken_text

FORMULA_COLORS = {'overlap8':'#FBBF24','quiz7overlap':'#FBBF24', 'set_union':'#22D3EE'}


def formula_sources():
    target = ROOT/'assets'/'comb01v2'
    target.mkdir(parents=True, exist_ok=True)
    for name, expr in FORMULAS.items():
        fg = FORMULA_COLORS.get(name, '#22D3EE')
        path=target/f'{name}.typ'
        path.write_text(
            '#set page(width: 13cm, height: 2.8cm, margin: 0pt, fill: none)\n'
            '#set text(font: "Noto Serif", size: 27pt, fill: rgb("'+fg+'"))\n'
            '#align(center + horizon)[$ '+expr+' $]\n',encoding='utf-8')
    return target


def compile_typst():
    target=formula_sources()
    from PIL import Image
    for name in FORMULAS:
        source=target/f'{name}.typ'
        out=target/f'{name}.png'
        subprocess.run(['typst','compile','--format','png','--ppi','250',str(source),str(out)],check=True)
        im=Image.open(out).convert('RGBA')
        bbox=im.getchannel('A').getbbox()
        if not bbox:
            raise RuntimeError(f'Empty formula image: {name}')
        pad=14
        box=(max(0,bbox[0]-pad),max(0,bbox[1]-pad),min(im.width,bbox[2]+pad),min(im.height,bbox[3]+pad))
        im.crop(box).save(out)
    print(f'Typst: compiled {len(FORMULAS)} transparent mathematical formula images.')


async def voice(voice_mode, voice_name, rate):
    voice_dir=ROOT/'voice'; voice_dir.mkdir(parents=True,exist_ok=True)
    try:
        from mutagen.mp3 import MP3
    except ImportError as e:
        raise RuntimeError('Please install mutagen, listed in requirements.txt') from e
    clips={}
    if voice_mode=='on':
        try:
            import edge_tts
        except ImportError as e:
            raise RuntimeError('Please install edge-tts, listed in requirements.txt') from e

    for i,beat in enumerate(BEATS):
        clip_key=f'{i:03}'
        filename=f'comb01_{i:03}.mp3'
        target=voice_dir/filename
        if voice_mode=='on':
            if not target.exists() or target.stat().st_size<1000:
                for attempt in range(3):
                    try:
                        communicate=edge_tts.Communicate(spoken_text(beat),voice_name,rate=rate)
                        await communicate.save(str(target))
                        break
                    except Exception as e:
                        if attempt==2:
                            raise RuntimeError(f'TTS failed at beat {i}; rerun with --voice off to debug silently') from e
                        await asyncio.sleep(2*(attempt+1))
            duration=float(MP3(str(target)).info.length)
            clips[clip_key]={'file': filename,'duration':round(duration,3),'section':beat.section}
        else:
            clips[clip_key]={'duration':0.0,'section':beat.section}
    meta={
        'version':'COMB01-v2.0', 'mode':voice_mode, 'voice':voice_name if voice_mode=='on' else None,
        'clips':clips,
        'target_seconds':round(sum(max(b.min_seconds,clips[f'{i:03}']['duration']+.9) for i,b in enumerate(BEATS))+5,2),
        'tts_words':sum(len(spoken_text(b).split()) for b in BEATS),
        'beats':len(BEATS),
    }
    (voice_dir/'comb01_voice_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    transcript=ROOT/'narration_COMB01_v2.md'
    lines=['# COMB01 · QUY TẮC CỘNG · BẢN THUYẾT MINH ĐỒNG BỘ', '',
           'Giọng mặc định: vi-VN-NamMinhNeural. Lời đọc được chia theo 42 nhịp.',
           'Mỗi nhịp bắt đầu đồng thời với hoạt hình; thời gian dựa trên clip MP3 thật.', '',
           f'**Thời gian video dự kiến:** {meta["target_seconds"]/60:.1f} phút; đọc {meta["tts_words"]} từ tiếng Việt.', '']
    current=None
    elapsed=0
    for i,b in enumerate(BEATS):
        if b.section!=current:
            current=b.section
            lines.extend(['',f'## {CHAPTER_LABELS[current]}',''])
        d=max(b.min_seconds,clips[f'{i:03}']['duration']+.9)
        m,s=divmod(int(elapsed),60)
        lines.extend([f'### Nhịp {i+1:02d} · {m:02d}:{s:02d} · {b.heading}', '',spoken_text(b),'',f'*Dòng chữ chính: {b.takeaway}*',''])
        elapsed+=d
    transcript.write_text('\n'.join(lines),encoding='utf-8')
    print(f"Prepared {len(BEATS)} beats, {meta['tts_words']} spoken words, estimated {meta['target_seconds']:.1f}s, audio={voice_mode}.")
    return meta


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--voice',choices=['off','on'],default='off')
    p.add_argument('--voice-name',default='vi-VN-NamMinhNeural')
    p.add_argument('--rate',default='+0%')
    p.add_argument('--skip-typst',action='store_true')
    a=p.parse_args()
    if not a.skip_typst:
        compile_typst()
    else:
        formula_sources()
    asyncio.run(voice(a.voice,a.voice_name,a.rate))


if __name__=='__main__':main()
