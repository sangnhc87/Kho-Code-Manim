"""Build exact scene timetable, optional Vietnamese TTS and synchronized SRT.
If voice is requested but TTS fails, the workflow MUST fail rather than
misleading the teacher with a silent MP4.
"""
from __future__ import annotations
import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat02.lesson import BEATS,N,validate


def duration(path):
    data=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration',
              '-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True)
    return float(data.strip())

async def voice_generate(path,text,voice,rate='+0%'):
    import edge_tts
    for attempt in range(3):
        try:
            await edge_tts.Communicate(text,voice=voice,rate=rate).save(str(path))
            return
        except Exception as e:
            if attempt == 2:
                raise
            await asyncio.sleep(2 * (attempt + 1))


def stamp(seconds):
    ms=round(seconds*1000)
    h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def chunks(text,target=64):
    words=text.split();blocks=[];carry=[]
    for word in words:
        carry.append(word)
        if len(' '.join(carry))>=target:
            blocks.append(' '.join(carry));carry=[]
    if carry:blocks.append(' '.join(carry))
    return blocks

async def run():
    ap=argparse.ArgumentParser()
    ap.add_argument('--voice',choices=['on','off'],default='on')
    ap.add_argument('--voice-id',default='vi-VN-NamMinhNeural')
    ap.add_argument('--rate',default='+0%')
    a=ap.parse_args()
    validate()
    (ROOT/'stat02'/'voice').mkdir(parents=True,exist_ok=True)
    plan=[];subtitles=[];cursor=0.;num=0
    for i,b in enumerate(BEATS):
        speech=0.;rel=''
        if a.voice=='on':
            p=ROOT/'stat02'/'voice'/f'beat_{i+1:02d}.mp3'
            if not p.exists() or p.stat().st_size < 1000:
                await voice_generate(p,b.voice,a.voice_id,a.rate)
            speech=duration(p)
            rel=p.relative_to(ROOT).as_posix()
            if speech<=1:raise RuntimeError('TTS returned blank/invalid audio')
        slot=max(b.duration,speech+1.6)
        plan.append({'chapter':b.chapter,'step':b.step,'duration':slot,'voice':rel,
                     'audio_seconds':speech,'title':b.title})
        parts=chunks(b.voice)
        usable=min(slot-.5,speech if rel else slot-1.0)
        for j,part in enumerate(parts):
            start=cursor+(j/len(parts))*usable
            finish=cursor+((j+1)/len(parts))*usable
            num+=1
            subtitles.append(f'{num}\n{stamp(start)} --> {stamp(finish)}\n{part}\n')
        cursor+=slot
    plan_doc={'scene':'STAT02','voice':a.voice,'data_count':N,'duration_expected':cursor,
              'chapters':8,'beats':plan}
    (ROOT/'stat02'/'runtime_plan.json').write_text(
        json.dumps(plan_doc,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'STAT02_vi.srt').write_text('\n'.join(subtitles)+'\n',encoding='utf-8')
    print('STAT02 runtime ready; duration',round(cursor,2),'seconds;',
          len(BEATS),'beats;',num,'subtitle entries; voice',a.voice)

if __name__=='__main__': asyncio.run(run())
