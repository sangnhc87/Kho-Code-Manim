"""Verify rendered MP4 duration, audio stream, and export eight chapter screenshots."""
import argparse, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb01_lesson_data import BEATS


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--video',required=True)
    ap.add_argument('--voice',choices=['on','off'],default='off')
    args=ap.parse_args()
    video=Path(args.video)
    if not video.exists():raise FileNotFoundError(video)
    info=probe(video)
    dur=float(info['format']['duration'])
    streams=info.get('streams',[])
    width=next((s['width'] for s in streams if s['codec_type']=='video'),None)
    if dur<660: raise AssertionError(f'Video too short: {dur:.1f}s; expected >=660s')
    if width is None: raise AssertionError('No video stream')
    if args.voice=='on' and not any(s['codec_type']=='audio' for s in streams):
        raise AssertionError('Voice enabled but MP4 contains no audio stream')
    manifest=json.loads((ROOT/'voice'/'comb01_voice_manifest.json').read_text(encoding='utf-8'))
    current=0.; chapters=[]
    for i,beat in enumerate(BEATS):
        if i==0 or BEATS[i-1].section!=beat.section:
            chapters.append((beat.section,current))
        a=manifest['clips'].get(f'{i:03}',{})
        current+=max(beat.min_seconds,float(a.get('duration',0))+.9)
    shot_dir=ROOT/'qa_comb01_v2'; shot_dir.mkdir(exist_ok=True)
    thumbnails=[]
    for chapter,sec in chapters:
        fname=shot_dir/f'{chapter}.jpg'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(min(sec+6,dur-3)),
                '-i',str(video),'-frames:v','1','-q:v','3',str(fname)],check=True)
        im=Image.open(fname).convert('RGB')
        thumb=ImageOps.contain(im,(640,360))
        cv=Image.new('RGB',(660,396),'#101827')
        cv.paste(thumb,((660-thumb.width)//2,8))
        ImageDraw.Draw(cv).text((14,370),chapter.upper(),fill='white')
        thumbnails.append(cv)
    board=Image.new('RGB',(1320,1584),'#0b1120')
    for k,im in enumerate(thumbnails):board.paste(im,((k%2)*660,(k//2)*396))
    board.save(shot_dir/'contact_sheet.jpg',quality=92)
    report={'video':str(video),'duration_seconds':round(dur,2),'resolution_width':width,
            'audio_present':any(s['codec_type']=='audio' for s in streams),'screenshots':len(chapters),
            'math_beats':len(BEATS),'result':'PASS'}
    (shot_dir/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
