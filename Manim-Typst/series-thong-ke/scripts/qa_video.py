"""After rendering: verify duration, resolution, audio mode; extract 8 QA frames."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat01.lesson import FREQUENCY,SCORES,BEATS

def ffprobe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format',
        '-show_streams','-of','json',str(path)],text=True))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--video',required=True)
    ap.add_argument('--quality',choices=['preview','fullhd'],required=True)
    ap.add_argument('--voice',choices=['on','off'],required=True)
    a=ap.parse_args()
    video=Path(a.video)
    if not video.is_file():raise FileNotFoundError(video)
    plan=json.loads((ROOT/'assets'/'runtime_plan.json').read_text(encoding='utf8'))
    probe=ffprobe(video)
    length=float(probe['format']['duration'])
    expected=float(plan['duration_expected'])
    streams=probe['streams'];v=next((s for s in streams if s['codec_type']=='video'),None)
    if not v:raise AssertionError('MP4 has no video stream')
    w,h=(v['width'],v['height'])
    desired=(854,480) if a.quality=='preview' else (1920,1080)
    assert (w,h)==desired,(w,h,desired)
    assert abs(length-expected)<3.0,(length,expected)
    assert expected>=640,'Video is too short for a full lesson'
    has_audio=any(s['codec_type']=='audio' for s in streams)
    if a.voice=='on':assert has_audio,'Voice on selected but MP4 has no audio!'
    folder=ROOT/'artifacts'/'qa';folder.mkdir(parents=True,exist_ok=True)
    cursor=0.0
    times=[]
    for i,b in enumerate(plan['beats']):
        if i%4==1:times.append((i//4+1,cursor+b['duration']*.5))
        cursor+=b['duration']
    for chapter,t in times:
        dst=folder/f'stat01_chapter_{chapter:02d}.jpg'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),
             '-i',str(video),'-frames:v','1','-q:v','3',str(dst)],check=True)
        assert dst.stat().st_size>1000
    report={'scene':'STAT01','duration_seconds':length,'expected_seconds':expected,
            'resolution':[w,h],'voice_mode':a.voice,'audio_stream_found':has_audio,
            'frames':len(times),'score_count':len(SCORES),'frequency':FREQUENCY,
            'status':'TECHNICAL_QA_PASS_VISUAL_REVIEW_REQUIRED'}
    (folder/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
