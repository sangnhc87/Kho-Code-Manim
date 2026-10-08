#!/usr/bin/env python3
"""Compile Typst, synthesize synchronized Vietnamese speech and export script/SRT.

Audio output uses one *complete* narrated paragraph per lesson beat. The
Manim Scene reads actual MP3 durations so captions, visuals and voice align.
"""
from __future__ import annotations
import argparse
import asyncio
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb14_lesson_data import BEATS, FORMULAS, CHAPTER_LABELS, validate


def formula_sources():
    target=ROOT/'assets'/'comb14v2'
    target.mkdir(parents=True,exist_ok=True)
    for name,expr in FORMULAS.items():
        fg='#FBBF24' if name in ('capstone_4','capstone_5','binary_4','fixed_3','pin_3','groups_2') else '#22D3EE'
        content=(
            '#set page(width: 17cm, height: 2.4cm, margin: 0pt, fill: none)\n'
            f'#set text(font: "Noto Serif", size: 28pt, fill: rgb("{fg}"))\n'
            f'#align(center + horizon)[$ {expr} $]\n'
        )
        (target/f'{name}.typ').write_text(content,encoding='utf-8')
    return target


def compile_formulas():
    folder=formula_sources()
    for name in FORMULAS:
        src=folder/f'{name}.typ'; dst=folder/f'{name}.png'
        subprocess.run(['typst','compile','--format','png','--ppi','255',str(src),str(dst)],check=True)
        with Image.open(dst) as raw:
            img=raw.convert('RGBA')
        bbox=img.getchannel('A').getbbox()
        if not bbox: raise RuntimeError(f'Typst formula has no visible pixels: {src}')
        pad=16
        left,top,right,bottom=bbox
        img.crop((max(0,left-pad),max(0,top-pad),min(img.width,right+pad),min(img.height,bottom+pad))).save(dst)
    print(f'TYPST_OK formulas={len(FORMULAS)}')


def ts(v):
    hours,rest=divmod(int(round(v*1000)),3600000)
    minutes,rest=divmod(rest,60000)
    seconds,ms=divmod(rest,1000)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}'


def chunks(text):
    # Split subtitle text by sentences, preserving complete Vietnamese words.
    sentences=re.split(r'(?<=[.!?])\s+',text.strip())
    chunks=[];buffer=[];count=0
    for item in sentences:
        size=len(item.split())
        if count+size>22 and buffer:
            chunks.append(' '.join(buffer));buffer=[];count=0
        buffer.append(item);count+=size
    if buffer:chunks.append(' '.join(buffer))
    return chunks


def export_script(manifest):
    lines=['# SANG MATH · COMB14 V2 · PHƯƠNG PHÁP GỘP KHỐI','','## Bản thuyết minh đồng bộ',
           '',f'Số nhịp: {len(BEATS)} · 8 chương · TTS={manifest["mode"]}',
           f'Tổng thời lượng dự kiến: {manifest["target_seconds"]:.1f} giây.',
           'Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.','']
    captions=[];time=0.;current=None;section_times={}
    for i,beat in enumerate(BEATS):
        if beat.section!=current:
            current=beat.section
            section_times[current]=round(time,2)
            lines.extend(['',f'## {CHAPTER_LABELS[current]}',''])
        dur=max(beat.min_seconds,manifest['clips'][f'{i:03}']['duration']+.85)
        lines.extend([f'### Nhịp {i+1:02d} · {int(time//60):02d}:{int(time%60):02d} · {beat.heading}',
                      '',beat.narration,'',f'**Trên màn hình:** {" | ".join(beat.lines)}',
                      f'**Ghi nhớ:** {beat.takeaway}',''])
        snippets=chunks(beat.narration)
        word_counts=[len(x.split()) for x in snippets]
        total_words=sum(word_counts)
        pos=time
        for k,seg in enumerate(snippets):
            segment_duration=(dur*word_counts[k]/total_words) if k!=len(snippets)-1 else time+dur-pos
            captions.append((pos,pos+segment_duration,seg))
            pos+=segment_duration
        time+=dur
    (ROOT/'narration_COMB14_v2.md').write_text('\n'.join(lines),encoding='utf-8')
    srt=[]
    for i,(start,end,string) in enumerate(captions,1):
        srt.extend([str(i),f'{ts(start)} --> {ts(end)}',string,''])
    (ROOT/'subtitles_COMB14_v2.srt').write_text('\n'.join(srt),encoding='utf-8')
    manifest['chapter_seconds']=section_times
    (ROOT/'voice'/'comb14_voice_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'SCRIPT_OK beats={len(BEATS)} words={manifest["tts_words"]} expected_duration={manifest["target_seconds"]:.1f}s srt_cues={len(captions)}')


async def prepare_voice(mode,name,rate):
    output=ROOT/'voice';output.mkdir(parents=True,exist_ok=True)
    old={}
    old_path=output/'comb14_clip_fingerprints.json'
    if old_path.exists():old=json.loads(old_path.read_text(encoding='utf-8'))
    new={};clips={}
    if mode=='on':
        import edge_tts
        from mutagen.mp3 import MP3
    for i,b in enumerate(BEATS):
        key=f'{i:03}'
        info={'duration':0.0,'section':b.section}
        if mode=='on':
            filename=f'comb14_{key}.mp3'
            path=output/filename
            fingerprint=hashlib.sha256((b.narration+'\n'+name+'\n'+rate).encode()).hexdigest()
            if old.get(key)!=fingerprint or not path.exists() or path.stat().st_size<1000:
                for attempt in range(4):
                    try:
                        await edge_tts.Communicate(b.narration,voice=name,rate=rate).save(str(path))
                        break
                    except Exception as exc:
                        if attempt==3:raise RuntimeError(f'TTS failed on beat {i+1}; choose voice=off for a silent technical preview') from exc
                        await asyncio.sleep(2+3*attempt)
            duration=float(MP3(str(path)).info.length)
            if duration<=0:raise ValueError(f'Voice clip unexpectedly empty: {path}')
            info.update({'file':filename,'duration':round(duration,3)})
            new[key]=fingerprint
        clips[key]=info
    if mode=='on':old_path.write_text(json.dumps(new,indent=2),encoding='utf-8')
    duration=sum(max(x.min_seconds,clips[f'{i:03}']['duration']+.85) for i,x in enumerate(BEATS))+5.2
    result={
        'version':'COMB14-v2.0','mode':mode,'voice_name':name if mode=='on' else None,
        'rate':rate if mode=='on' else None,'beats':len(BEATS),
        'clips':clips,'target_seconds':round(duration,2),
        'tts_words':sum(len(x.narration.split()) for x in BEATS)
    }
    export_script(result)
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--voice',choices=['on','off'],default='off')
    p.add_argument('--voice-name',default='vi-VN-NamMinhNeural')
    p.add_argument('--rate',default='+0%')
    p.add_argument('--skip-typst',action='store_true',help='Create .typ sources but skip PNG compile (for tests only)')
    a=p.parse_args()
    validate()
    if a.skip_typst:formula_sources()
    else:compile_formulas()
    asyncio.run(prepare_voice(a.voice,a.voice_name,a.rate))

if __name__=='__main__':main()
