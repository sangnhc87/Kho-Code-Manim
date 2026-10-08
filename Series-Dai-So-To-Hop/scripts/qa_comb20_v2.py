#!/usr/bin/env python3
"""Strict post-render QC: minimum duration, voice stream, sections, screenshots."""
import argparse, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb20_lesson_data import BEATS, CHAPTER_LABELS


def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))


def check_video(path,voice):
    info=probe(path)
    seconds=float(info['format']['duration'])
    streams=info.get('streams',[])
    vids=[x for x in streams if x['codec_type']=='video']
    auds=[x for x in streams if x['codec_type']=='audio']
    if not vids:raise AssertionError('Video stream not found')
    if seconds<1100:raise AssertionError(f'Export too short: {seconds:.2f}s (expected >=1100s)')
    if voice=='on' and not auds:raise AssertionError('Narration requested but MP4 has no audio stream')
    manifest=ROOT/'voice'/'comb20_voice_manifest.json'
    if not manifest.exists():raise AssertionError('Missing COMB20 narration manifest')
    data=json.loads(manifest.read_text(encoding='utf-8'))
    if data['mode']!=voice:raise AssertionError(f'Voice mismatch: expected {voice}; prepared {data["mode"]}')
    expectation=float(data['target_seconds'])
    if abs(expectation-seconds)>12:
        raise AssertionError(f'Time mismatch: expected {expectation:.1f}s, got {seconds:.1f}s')
    width=vids[0]['width'];height=vids[0]['height']
    if (width,height) not in ((854,480),(1920,1080)):
        raise AssertionError(f'Unexpected resolution {width}x{height}')
    return data,seconds,width,height,bool(auds)


def frames(video,meta,seconds):
    out=ROOT/'qa_comb20_v2';out.mkdir(exist_ok=True)
    sec=0;last=None;chapters=[]
    for i,b in enumerate(BEATS):
        if b.section!=last:
            chapters.append((b.section,sec))
            last=b.section
        dur=float(meta['clips'].get(f'{i:03}',{}).get('duration',0))
        sec+=max(b.min_seconds,dur+.85)
    previews=[]
    for ch,start in chapters:
        fname=out/f'{ch}.jpg'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(min(seconds-4,start+7)),
                        '-i',str(video),'-frames:v','1','-q:v','3',str(fname)],check=True)
        pic=Image.open(fname).convert('RGB')
        thumb=ImageOps.contain(pic,(640,360))
        tile=Image.new('RGB',(660,400),'#101827')
        tile.paste(thumb,((660-thumb.width)//2,9))
        ImageDraw.Draw(tile).text((18,374),CHAPTER_LABELS[ch],fill='white',font=ImageFont.truetype('DejaVuSans.ttf',16))
        previews.append(tile)
    contact=Image.new('RGB',(1320,1600),'#0b1120')
    for i,tile in enumerate(previews):contact.paste(tile,((i%2)*660,(i//2)*400))
    contact.save(out/'contact_sheet.jpg',quality=90)
    return out,len(previews)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--video',required=True)
    ap.add_argument('--voice',choices=['on','off'],required=True)
    args=ap.parse_args()
    movie=Path(args.video)
    if not movie.exists():raise FileNotFoundError(movie)
    meta,seconds,width,height,audio=check_video(movie,args.voice)
    destination,nframes=frames(movie,meta,seconds)
    report={'status':'PASS','video':str(movie),'seconds':round(seconds,2),
            'resolution':f'{width}x{height}','audio_stream':audio,'voice':args.voice,
            'frames':nframes,'lesson_beats':len(BEATS),'chapters':list(CHAPTER_LABELS)}
    (destination/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
