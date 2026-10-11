"""Lời đọc tiếng Việt cho từng bước của kịch bản (Edge TTS, Zalo TTS hoặc giả lập).

Mỗi bước (step) có một file âm thanh riêng để nước đi khớp đúng câu đọc.
Kết quả: voice/timing.json = [[{'audio', 'seconds'} cho từng step] cho từng beat].
"""
import asyncio
import hashlib
import json
import os
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

EDGE_VOICE = 'vi-VN-NamMinhNeural'


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def duration(path):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                   '-of', 'default=nw=1:nk=1', str(path)], text=True)
    return float(out.strip())


def speakable(text):
    """Chuẩn hoá để giọng đọc tự nhiên: bỏ ký hiệu, đọc '–' thành ngắt nghỉ."""
    text = text.replace('–', ',').replace('—', ',').replace('…', '.').replace('★', '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


async def _edge(text, out):
    import edge_tts
    for attempt in range(6):
        try:
            await edge_tts.Communicate(text, voice=EDGE_VOICE, rate='-4%').save(str(out))
            if out.exists() and out.stat().st_size > 800:
                return
        except Exception:
            if attempt == 5:
                raise
        await asyncio.sleep(2 + 2 * attempt)
    raise RuntimeError('Edge TTS không trả âm thanh')


def _zalo(text, out):
    key = os.getenv('ZALO_API_KEY')
    if not key:
        raise RuntimeError('Giọng Zalo cần GitHub Secret ZALO_API_KEY.')
    payload = urllib.parse.urlencode({'input': text, 'speaker_id': 3, 'speed': 1.0}).encode()
    req = urllib.request.Request('https://api.zalo.ai/v1/tts/synthesize', data=payload,
                                 headers={'apikey': key}, method='POST')
    with urllib.request.urlopen(req, timeout=40) as r:
        res = json.load(r)
    url = res.get('data', {}).get('url')
    if res.get('error_code') != 0 or not url:
        raise RuntimeError('Zalo TTS lỗi: ' + str(res.get('error_message', res.get('error_code'))))
    for attempt in range(8):
        try:
            with urllib.request.urlopen(url, timeout=50) as r:
                out.write_bytes(r.read())
            if out.stat().st_size > 500:
                return
        except Exception:
            if attempt == 7:
                raise
        time.sleep(3 + attempt)


def _render_one(text, raw, provider):
    if provider == 'edge':
        asyncio.run(_edge(text, raw))
    elif provider == 'zalo':
        _zalo(text, raw)
    elif provider == 'mock':
        secs = max(1.2, len(text.split()) / 3.2)
        run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
             '-t', f'{secs:.2f}', str(raw)])
    else:
        raise ValueError('provider phải là edge, zalo hoặc mock')


def generate_voice(data, folder, provider='edge'):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    timing = []
    for b, beat in enumerate(data['beats']):
        clips = []
        for s, step in enumerate(beat['steps']):
            text = speakable(step['say'])
            digest = hashlib.sha1(f'{provider}|{EDGE_VOICE}|{text}'.encode()).hexdigest()[:12]
            wav = folder / f'v{b:02d}_{s:02d}_{digest}.wav'
            if not wav.exists():
                raw = folder / f'raw_{digest}{".wav" if provider == "mock" else ".mp3"}'
                _render_one(text, raw, provider)
                run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw), '-ac', '2', '-ar', '44100',
                     '-c:a', 'pcm_s16le', str(wav)])
                raw.unlink(missing_ok=True)
            clips.append({'audio': str(wav.resolve()), 'seconds': round(duration(wav), 3)})
        timing.append(clips)
    (folder / 'timing.json').write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding='utf-8')
    return timing
