"""Strict final video validation, sound check, and eight chapter contact frames."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--video',required=True)
    parser.add_argument('--quality',choices=['preview','fullhd'],required=True)
    parser.add_argument('--voice',choices=['on','off'],required=True)
    a=parser.parse_args()
    path=Path(a.video)
    if not path.is_file():raise FileNotFoundError(path)
    plan=json.loads((ROOT/'stat05'/'runtime_plan.json').read_text(encoding='utf-8'))
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format',
        '-show_streams','-of','json',str(path)],text=True))
    v=next((x for x in streams.get('streams',[]) if x.get('codec_type')=='video'),None)
    audio=next((x for x in streams.get('streams',[]) if x.get('codec_type')=='audio'),None)
    if not v:raise AssertionError('MP4 has no video stream')
    size=(int(v['width']),int(v['height']))
    wanted=(854,480) if a.quality=='preview' else (1920,1080)
    if size!=wanted:raise AssertionError(f'Wrong resolution: {size} vs {wanted}')
    length=float(streams['format']['duration'])
    expected=float(plan['duration_expected'])
    if expected<840:raise AssertionError(f'Lesson unexpectedly short: {expected}')
    if abs(length-expected)>3.0:raise AssertionError(f'Duration differs from plan: {length} vs {expected}')
    if plan['voice']!=a.voice:raise AssertionError('Voice setting differs from prepared plan')
    if a.voice=='on' and audio is None:raise AssertionError('Voice ON but rendered MP4 is silent')
    result=ROOT/'artifacts'/'stat05_qa';result.mkdir(parents=True,exist_ok=True)
    cursor=0.;count=0
    for i,b in enumerate(plan['beats']):
        if i%4==1:
            t=cursor+float(b['duration'])/2
            target=result/f'chapter_{i//4+1:02d}.jpg'
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(path),
                             '-frames:v','1','-q:v','3',str(target)],check=True)
            if target.stat().st_size<1000:raise RuntimeError(f'Bad thumbnail: {target}')
            count+=1
        cursor+=float(b['duration'])
    if count!=8:raise AssertionError('Expected eight review frames')
    report=dict(scene='STAT05',quality=a.quality,voice=a.voice,duration=length,
                expected=expected,resolution=list(size),audio=bool(audio),frames=count,
                status='TECHNICAL_PASS; VISUAL_PEDAGOGICAL_REVIEW_PENDING')
    (result/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('STAT05_QA_OK',json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
