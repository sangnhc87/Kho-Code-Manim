"""Prepare narration MP3, exact animation durations and Vietnamese SRT.
The voice=on switch must stop on any TTS/network/audio failure.
"""
from __future__ import annotations
import argparse,sys,json,asyncio,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from int01.lesson import SEGMENTS,CHAPTERS,validate

def duration(path):
    cmd=['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)]
    return float(subprocess.check_output(cmd,text=True).strip())
def timestamp(sec):
    milliseconds=round(sec*1000); hours,milliseconds=divmod(milliseconds,3600000)
    minutes,milliseconds=divmod(milliseconds,60000);secs,milliseconds=divmod(milliseconds,1000)
    return f'{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}'
def chunks(s,threshold=75):
    words=s.split(); current=[]; out=[]
    for w in words:
        current.append(w)
        if len(' '.join(current))>=threshold:
            out.append(' '.join(current));current=[]
    if current:out.append(' '.join(current))
    return out
async def synthesize(text,path,voice):
    import edge_tts
    await edge_tts.Communicate(text,voice=voice,rate='-5%').save(str(path))
async def prepare(voice,voice_id):
    validate()
    audio=ROOT/'int01/voice';audio.mkdir(parents=True,exist_ok=True)
    result=[]; lines=[];time=0.;idx=0
    for i,segment in enumerate(SEGMENTS,1):
        clip=''; length=0.
        if voice=='on':
            path=audio/f'part_{i:02d}.mp3'
            await synthesize(segment.voice,path,voice_id)
            if not path.exists() or path.stat().st_size<1000:raise RuntimeError('No audio generated for segment '+str(i))
            length=duration(path)
            if length<=1:raise RuntimeError('Audio too short for segment '+str(i))
            clip=path.relative_to(ROOT).as_posix()
        seconds=max(segment.duration,length+1.6)
        result.append(dict(chapter=segment.chapter,step=segment.step,title=segment.title,formula=segment.formula,
                           visual=segment.visual,voice_path=clip,audio_duration=length,duration=seconds))
        pieces=chunks(segment.voice)
        readable=min(seconds-1.0,length if clip else seconds-1.8)
        for j,piece in enumerate(pieces):
            idx+=1;start=time+readable*j/len(pieces);end=time+readable*(j+1)/len(pieces)
            lines.append(f'{idx}\n{timestamp(start)} --> {timestamp(end)}\n{piece}\n')
        time+=seconds
    payload={'episode':'INT01','voice':voice,'voice_id':voice_id if voice=='on' else '',
             'total_duration':time,'chapters':list(CHAPTERS),'segments':result}
    (ROOT/'int01/runtime_plan.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'INT01_vi.srt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('INT01_PREPARE_OK',len(result),'segments',round(time,2),'seconds, voice',voice)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--voice',choices=['on','off'],default='off')
    parser.add_argument('--voice-id',default='vi-VN-NamMinhNeural');a=parser.parse_args()
    asyncio.run(prepare(a.voice,a.voice_id))
