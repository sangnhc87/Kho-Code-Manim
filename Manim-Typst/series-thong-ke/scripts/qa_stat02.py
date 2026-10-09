"""Probe rendered MP4 duration, resolution, sound; extract 8 review frames."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--video',required=True)
    ap.add_argument('--quality',choices=['preview','fullhd'],required=True)
    ap.add_argument('--voice',choices=['on','off'],required=True)
    a=ap.parse_args()
    path=Path(a.video)
    if not path.is_file():raise FileNotFoundError(path)
    plan=json.loads((ROOT/'stat02'/'runtime_plan.json').read_text(encoding='utf-8'))
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format',
                    '-show_streams','-of','json',str(path)],text=True))
    video=next((s for s in probe['streams'] if s['codec_type']=='video'),None)
    audio=next((s for s in probe['streams'] if s['codec_type']=='audio'),None)
    if not video:raise AssertionError('No MP4 video stream')
    width,height=video['width'],video['height']
    expected_size=(854,480) if a.quality=='preview' else (1920,1080)
    if (width,height)!=expected_size:raise AssertionError(('Wrong resolution',width,height))
    actual=float(probe['format']['duration']);expected=float(plan['duration_expected'])
    if expected<700:raise AssertionError(('Lesson too short',expected))
    if abs(actual-expected)>3:raise AssertionError(('Duration mismatch',actual,expected))
    if a.voice=='on' and not audio:raise AssertionError('TTS was enabled but video is silent')
    if a.voice!=plan['voice']:raise AssertionError('Audio plan mismatch')
    folder=ROOT/'artifacts'/'stat02_qa';folder.mkdir(parents=True,exist_ok=True)
    start=0.;times=[]
    for i,b in enumerate(plan['beats']):
        if i%4==1:times.append((i//4+1,start+b['duration']/2))
        start+=b['duration']
    for chapter,time_s in times:
        outfile=folder/f'stat02_chapter_{chapter:02d}.jpg'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(time_s),'-i',str(path),
                        '-frames:v','1','-q:v','3',str(outfile)],check=True)
        if outfile.stat().st_size<1000:raise AssertionError('Empty QA frame')
    report={'episode':'STAT02','duration':actual,'expected_duration':expected,
            'resolution':[width,height],'has_audio':bool(audio),
            'voice_mode':a.voice,'eight_frames':len(times),
            'status':'TECHNICAL_CHECKS_PASS; VISUAL_AND_PEDAGOGICAL_REVIEW_REQUIRED'}
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
