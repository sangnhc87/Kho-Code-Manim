"""Narration backends: licensed Zalo male Southern (key), Edge generic male, or local silent tests."""
import asyncio
import json
import os
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path


def cmd(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)


def chunks(text,limit=320):
    sentences=re.split(r'(?<=[.!?;:])\s+',text.strip())
    pieces=[]; cur=''
    for sentence in sentences:
        for segment in ([sentence[i:i+limit] for i in range(0,len(sentence),limit)] if len(sentence)>limit else [sentence]):
            if cur and len(cur)+len(segment)+1>limit:
                pieces.append(cur);cur=''
            cur = (cur+' '+segment).strip()
    if cur: pieces.append(cur)
    return pieces


def zalo_request(text,out):
    key=os.getenv('ZALO_API_KEY')
    if not key: raise RuntimeError('Giọng nam miền Nam yêu cầu GitHub Secret ZALO_API_KEY.')
    payload=urllib.parse.urlencode({'input':text,'speaker_id':3,'speed':1.0}).encode()
    req=urllib.request.Request('https://api.zalo.ai/v1/tts/synthesize',data=payload,headers={'apikey':key},method='POST')
    with urllib.request.urlopen(req,timeout=40) as r:
        res=json.load(r)
    if res.get('error_code') != 0 or not res.get('data',{}).get('url'):
        raise RuntimeError('Zalo TTS error: '+str(res.get('error_message',res.get('error_code'))))
    url=res['data']['url']
    if not url.startswith('https://'): raise RuntimeError('Invalid TTS URL')
    for attempt in range(8):
        try:
            with urllib.request.urlopen(url,timeout=50) as r:
                out.write_bytes(r.read())
            if out.stat().st_size>500: return
        except Exception:
            if attempt == 7: raise
        time.sleep(3+attempt)
    raise RuntimeError('Zalo audio unavailable; check account balance/limits')


async def edge_request(text,out):
    import edge_tts
    await edge_tts.Communicate(text,voice='vi-VN-NamMinhNeural',rate='-5%').save(str(out))


def generate_voice(data, folder, provider='edge'):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    timing=[]
    for idx,beat in enumerate(data['beats']):
        parts=[]
        for j,part in enumerate(chunks(beat['narration'])):
            path=folder / f'part_{idx:03d}_{j:02d}'
            if provider=='zalo':
                raw=path.with_suffix('.raw')
                zalo_request(part,raw)
            elif provider=='edge':
                raw=path.with_suffix('.mp3')
                asyncio.run(edge_request(part,raw))
            elif provider=='mock':
                # Local smoke test only; never publish as voiceover.
                raw=path.with_suffix('.wav')
                duration=max(1.5,len(part.split())/2.4)
                cmd(['ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100', '-t',str(duration),str(raw)])
            else: raise ValueError('Voice provider must be edge, zalo or mock')
            parts.append(raw)
        # Decode each chunk to PCM first; Zalo may return WAV despite .raw extension.
        wavs=[]
        for j,part in enumerate(parts):
            wave=folder/f'decode_{idx:03d}_{j:02d}.wav'
            cmd(['ffmpeg','-y','-v','error','-i',str(part),'-ac','2','-ar','44100','-c:a','pcm_s16le',str(wave)])
            wavs.append(wave)
        concat=folder/f'concat_{idx:03d}.txt'
        concat.write_text(''.join("file '"+p.resolve().as_posix()+"'\n" for p in wavs),encoding='utf-8')
        result=folder/f'voice_{idx:03d}.wav'
        cmd(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c:a','pcm_s16le',str(result)])
        probe=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(result)],text=True)
        timing.append({'audio':str(result.resolve()),'seconds':round(float(probe.strip()),3)})
    (folder/'timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
    return timing
