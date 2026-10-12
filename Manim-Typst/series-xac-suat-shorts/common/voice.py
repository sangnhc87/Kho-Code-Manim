"""Narration for the Shorts (copied from the INT series, faster pace): Edge TTS (or VieNeu on CI) per beat, exact durations, sentence timings, SRT.

voice=on  → every beat must get a real MP3 (retries, then hard failure; never
            publish a silent video pretending to be narrated).
voice=off → durations are estimated from the text so layout can be reviewed.
"""
from __future__ import annotations

import asyncio
import os
import hashlib
import json
import re
import subprocess
from pathlib import Path

VOICE_ID = 'vi-VN-NamMinhNeural'
RATE = '+6%'           # Shorts: brisk but still clear
PAD = 0.45         # silence after each beat's narration (seconds)
LEAD = 0.15        # narration starts slightly after the beat's visual cue
WORDS_PER_SEC = 3.45  # vi-VN-NamMinhNeural at +6% (estimate)
ATTEMPTS = int(os.environ.get('XSS_TTS_ATTEMPTS', 6))  # pack_voice.sh raises it: Edge often drops runs of requests
# Edge refuses datacenter IPs (GitHub runners, 2026-10). XSS_TTS_ENGINE=vieneu clones NamMinh offline on the runner
# with VieNeu-TTS from assets_voice/namminh_ref.wav; VieNeu talks faster, so every clip is stretched (atempo) to
# NamMinh's own pace, measured on 733 Edge clips of this series: median 3.28 words per second.
ENGINE = os.environ.get('XSS_TTS_ENGINE', 'edge')
NAMMINH_WPS = float(os.environ.get('XSS_NAMMINH_WPS', '3.28'))
VIENEU_REF = Path(__file__).resolve().parents[1] / 'assets_voice' / 'namminh_ref.wav'
_VIENEU = None


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                   '-of', 'default=noprint_wrappers=1:nokey=1', str(path)], text=True)
    return float(out.strip())


def split_sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p for p in parts if p]


def estimate(text: str) -> tuple[float, list[dict]]:
    """Offline estimate (voice=off): proportional to word count."""
    t = 0.0
    sentences = []
    for s in split_sentences(text):
        d = len(s.split()) / WORDS_PER_SEC + 0.35
        sentences.append({'start': round(t, 3), 'end': round(t + d - 0.3, 3), 'text': s})
        t += d
    return t, sentences


def _azure_once(text: str, path: Path, voice: str) -> list[dict]:
    """Official Azure Speech REST (same neural voices as Edge, allowed from cloud IPs); used when AZURE_SPEECH_KEY is set."""
    import urllib.request
    from xml.sax.saxutils import escape
    region = os.environ.get('AZURE_SPEECH_REGION') or 'southeastasia'
    ssml = (f"<speak version='1.0' xml:lang='vi-VN'><voice name='{voice}'>"
            f"<prosody rate='{RATE}'>{escape(text)}</prosody></voice></speak>")
    req = urllib.request.Request(f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1', data=ssml.encode('utf-8'),
                                 headers={'Ocp-Apim-Subscription-Key': os.environ['AZURE_SPEECH_KEY'],
                                          'Content-Type': 'application/ssml+xml',
                                          'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
                                          'User-Agent': 'xss-shorts'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        path.write_bytes(resp.read())
    return []  # no boundaries from REST: synthesize() scales the estimated sentence timings to the audio length


def _vieneu_once(text: str, path: Path) -> list[dict]:
    global _VIENEU
    if _VIENEU is None:
        from vieneu import Vieneu
        _VIENEU = Vieneu()
    raw = path.with_suffix('.raw.wav')
    _VIENEU.save(_VIENEU.infer(text, ref_audio=str(VIENEU_REF)), str(raw))
    target = len(text.split()) / NAMMINH_WPS
    tempo = min(1.05, max(.6, ffprobe_duration(raw) / target))  # < 1 slows the clip down to NamMinh's pace
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-filter:a', f'atempo={tempo:.3f}',
                    '-ac', '1', '-ar', '24000', '-b:a', '64k', str(path)], check=True)
    raw.unlink(missing_ok=True)
    return []  # no boundaries: synthesize() scales the estimated sentence timings to the audio length


async def _synth_once(text: str, path: Path, voice: str) -> list[dict]:
    if ENGINE == 'vieneu':
        return _vieneu_once(text, path)
    if os.environ.get('AZURE_SPEECH_KEY'):
        return _azure_once(text, path, voice)
    import edge_tts
    comm = edge_tts.Communicate(text, voice=voice, rate=RATE, boundary='SentenceBoundary')
    sentences = []
    with path.open('wb') as fh:
        async for chunk in comm.stream():
            if chunk['type'] == 'audio':
                fh.write(chunk['data'])
            elif chunk['type'] == 'SentenceBoundary':
                start = chunk['offset'] / 1e7
                sentences.append({'start': round(start, 3),
                                  'end': round(start + chunk['duration'] / 1e7, 3),
                                  'text': chunk['text']})
    return sentences


async def synthesize(text: str, path: Path, voice: str = VOICE_ID) -> tuple[float, list[dict]]:
    last = None
    for attempt in range(1, ATTEMPTS + 1):
        try:
            sentences = await _synth_once(text, path, voice)
            if path.stat().st_size < 1000:
                raise RuntimeError('audio too small')
            length = ffprobe_duration(path)
            if length <= 1.0:
                raise RuntimeError('audio too short')
            if not sentences:
                _, sentences = estimate(text)
                scale = length / max(sentences[-1]['end'], 0.1)
                for s in sentences:
                    s['start'] = round(s['start'] * scale, 3)
                    s['end'] = round(s['end'] * scale, 3)
            return length, sentences
        except Exception as exc:  # network / service hiccups are common
            last = exc
            path.unlink(missing_ok=True)
            wait = min(2 ** attempt, 30)
            print(f'  TTS attempt {attempt}/{ATTEMPTS} failed ({exc}); retry in {wait}s', flush=True)
            await asyncio.sleep(wait)
    raise RuntimeError(f'TTS failed after {ATTEMPTS} attempts: {last}')


def text_hash(text: str, voice: str) -> str:
    return hashlib.sha1(f'{voice}|{RATE}|{text}'.encode()).hexdigest()[:12]


async def prepare(lesson, paths: dict, mode: str, voice: str = VOICE_ID) -> dict:
    audio_dir: Path = paths['voice']
    audio_dir.mkdir(parents=True, exist_ok=True)
    old = {}
    if paths['plan'].exists():
        try:
            old = {b['id']: b for b in json.loads(paths['plan'].read_text('utf-8'))['beats']}
        except Exception:
            old = {}
    beats = []
    for i, beat in enumerate(lesson.BEATS, 1):
        h = text_hash(beat.text, voice)
        entry = {'id': beat.id, 'part': beat.part, 'chapter': beat.chapter, 'hash': h}
        if mode == 'on':
            mp3 = audio_dir / f'{i:02d}_{beat.id}.mp3'
            prev = old.get(beat.id)
            if prev and prev.get('hash') == h and prev.get('audio') and mp3.exists():
                length, sentences = prev['audio_duration'], prev['sentences']
                print(f'[{i:02d}/{len(lesson.BEATS)}] {beat.id}: cached {length:.2f}s', flush=True)
            else:
                length, sentences = await synthesize(beat.text, mp3, voice)
                print(f'[{i:02d}/{len(lesson.BEATS)}] {beat.id}: {length:.2f}s', flush=True)
            entry.update(audio=mp3.relative_to(paths['pkg'].parent).as_posix(), audio_duration=round(length, 3))
        else:
            length, sentences = estimate(beat.text)
            entry.update(audio='', audio_duration=0.0)
        entry['sentences'] = [dict(s, start=round(s['start'] + LEAD, 3), end=round(s['end'] + LEAD, 3))
                              for s in sentences]
        entry['duration'] = round(LEAD + length + PAD, 3)
        beats.append(entry)
    plan = {
        'episode': lesson.EPISODE['code'],
        'voice': mode,
        'voice_id': voice if mode == 'on' else '',
        'lead': LEAD,
        'total_duration': round(sum(b['duration'] for b in beats), 3),
        'parts': [list(p) for p in lesson.PARTS],
        'beats': beats,
    }
    paths['plan'].parent.mkdir(parents=True, exist_ok=True)
    paths['plan'].write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    return plan


# ---------------------------------------------------------------- subtitles
def _ts(sec: float) -> str:
    ms = max(0, round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def _chunks(text: str, limit: int = 84) -> list[str]:
    words, cur, out = text.split(), [], []
    for w in words:
        if cur and len(' '.join(cur + [w])) > limit:
            out.append(' '.join(cur))
            cur = []
        cur.append(w)
    if cur:
        out.append(' '.join(cur))
    return out


def build_srt(plan: dict, starts: list[float]) -> str:
    """Subtitles from sentence boundaries, shifted by each beat's real start."""
    lines, idx = [], 0
    for beat, t0 in zip(plan['beats'], starts):
        for s in beat['sentences']:
            pieces = _chunks(s['text'])
            total = sum(len(p) for p in pieces)
            a = s['start']
            span = max(s['end'] - s['start'], 0.8)
            for p in pieces:
                b = a + span * len(p) / total
                idx += 1
                lines.append(f'{idx}\n{_ts(t0 + a)} --> {_ts(t0 + b)}\n{p}\n')
                a = b
    return '\n'.join(lines) + '\n'


def chapters(plan: dict, starts: list[float]) -> list[tuple[float, str]]:
    return [(t0, b['chapter']) for b, t0 in zip(plan['beats'], starts) if b.get('chapter')]


def stamp(sec: float) -> str:
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'
