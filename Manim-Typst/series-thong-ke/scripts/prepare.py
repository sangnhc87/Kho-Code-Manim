"""Prepare a runtime plan, optionally synthesize Vietnamese voice, and write .srt.
Voice-on mode FAILS on TTS errors instead of silently returning a muted video.
"""
import argparse
import asyncio
import json
import math
import re
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat01.lesson import BEATS,N,FREQUENCY,validate


def duration(path):
    r=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration',
                  '-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True)
    return float(r.strip())

async def generate_voice(path, text, voice):
    import edge_tts
    await edge_tts.Communicate(text, voice=voice,rate='-5%').save(str(path))


def stamp(s):
    ms=round(s*1000)
    h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'


def sentence_chunks(text, target=65):
    # A subtitle never takes over the whole frame with 40 words.
    words=text.split()
    lines=[];cur=[]
    for word in words:
        cur.append(word)
        if len(' '.join(cur))>=target:
            lines.append(' '.join(cur));cur=[]
    if cur:lines.append(' '.join(cur))
    return lines

async def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--voice',choices=['off','on'],default='off')
    ap.add_argument('--voice-id',default='vi-VN-HoaiMyNeural')
    args=ap.parse_args()
    validate()
    voices=ROOT/'assets'/'voice'
    voices.mkdir(parents=True,exist_ok=True)
    entries=[];lines=[];cursor=0.0;k=0
    for i,b in enumerate(BEATS):
        rel=''
        speech_duration=0.0
        if args.voice=='on':
            dst=voices/f'stat01_{i+1:02d}.mp3'
            await generate_voice(dst,b.narration,args.voice_id)
            speech_duration=duration(dst)
            rel=dst.relative_to(ROOT).as_posix()
        slot=max(b.duration,speech_duration+1.3)
        entries.append({'chapter':b.chapter,'beat':i+1,'duration':slot,
                        'voice':rel,'narration':b.narration,'speech_seconds':speech_duration})
        chunks=sentence_chunks(b.narration)
        usable=min(slot-.35,speech_duration if args.voice=='on' else slot-1.0)
        for j,chunk in enumerate(chunks):
            a=cursor+(j/len(chunks))*usable
            end=cursor+((j+1)/len(chunks))*usable
            k+=1
            lines.append(f'{k}\n{stamp(a)} --> {stamp(end)}\n{chunk}\n')
        cursor+=slot
    plan={'scene':'STAT01','voice':args.voice,'n':N,'frequency':FREQUENCY,
          'beats':entries,'duration_expected':cursor}
    (ROOT/'assets'/'runtime_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
    (ROOT/'STAT01_vi.srt').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print('Prepared',len(entries),'beats, seconds',round(cursor,1),'voice',args.voice,
          'subtitle lines',k)

if __name__=='__main__':asyncio.run(main())
