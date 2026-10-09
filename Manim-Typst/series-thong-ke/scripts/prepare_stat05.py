"""Prepare per-beat durations, exact Vietnamese narration audio, and subtitles.
Voice-on must fail when TTS is missing (never ship an accidentally silent video).
"""
from __future__ import annotations
import argparse,asyncio,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat05.lesson import BEATS,validate

def duration(path):
    result=subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True)
    return float(result.strip())

def stamp(seconds):
    milliseconds=round(seconds*1000)
    hour,milliseconds=divmod(milliseconds,3600000)
    minute,milliseconds=divmod(milliseconds,60000)
    second,milliseconds=divmod(milliseconds,1000)
    return f'{hour:02d}:{minute:02d}:{second:02d},{milliseconds:03d}'

def split_text(text,target=65):
    result=[];current=[]
    for word in text.split():
        current.append(word)
        if len(' '.join(current))>=target:
            result.append(' '.join(current));current=[]
    if current:result.append(' '.join(current))
    return result

async def synthesize(text,path,voice,rate='+0%'):
    import edge_tts
    for attempt in range(3):
        try:
            await edge_tts.Communicate(text,voice=voice,rate=rate).save(str(path))
            return
        except Exception as e:
            if attempt == 2:
                raise
            await asyncio.sleep(2 * (attempt + 1))

async def main():
    arg=argparse.ArgumentParser()
    arg.add_argument('--voice',choices=['on','off'],default='on')
    arg.add_argument('--voice-id',default='vi-VN-NamMinhNeural')
    arg.add_argument('--rate',default='+0%')
    a=arg.parse_args()
    validate()
    out=ROOT/'stat05'/'voice';out.mkdir(parents=True,exist_ok=True)
    beats=[];subtitles=[];time=0.0;number=0
    for i,b in enumerate(BEATS):
        speech=0.0;voice_path=''
        if a.voice=='on':
            path=out/f'beat_{i+1:02d}.mp3'
            if not path.exists() or path.stat().st_size < 1000:
                await synthesize(b.voice,path,a.voice_id,a.rate)
            speech=duration(path)
            if speech<=1:raise RuntimeError(f'Invalid/empty TTS for beat {i+1}')
            voice_path=path.relative_to(ROOT).as_posix()
        seconds=max(b.duration,speech+1.8)
        beats.append(dict(chapter=b.chapter,step=b.step,duration=seconds,voice=voice_path,
                          audio_seconds=speech,title=b.title))
        chunks=split_text(b.voice)
        usable=min(seconds-1.0,speech if voice_path else seconds-1.5)
        for j,chunk in enumerate(chunks):
            beginning=time+j*usable/len(chunks)
            ending=time+(j+1)*usable/len(chunks)
            number+=1
            subtitles.append(f'{number}\n{stamp(beginning)} --> {stamp(ending)}\n{chunk}\n')
        time+=seconds
    plan=dict(scene='STAT05',voice=a.voice,beats=beats,chapters=8,duration_expected=time)
    (ROOT/'stat05'/'runtime_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'STAT05_vi.srt').write_text('\n'.join(subtitles)+'\n',encoding='utf-8')
    print('STAT05_PREPARE_OK',len(beats),'beats;',number,'subtitles;',round(time,2),'seconds; voice:',a.voice)
if __name__=='__main__':asyncio.run(main())
