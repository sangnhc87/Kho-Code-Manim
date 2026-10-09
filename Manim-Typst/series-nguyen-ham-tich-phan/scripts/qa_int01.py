"""Video QA: verifies real encoded tracks, durations and chapter snapshots."""
from __future__ import annotations
import sys,json,subprocess,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def probe(video):
    result=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)],
                        capture_output=True,text=True,check=True)
    return json.loads(result.stdout)
def qa(video,quality,voice):
    if not video.is_file() or video.stat().st_size<6000:raise RuntimeError('Missing/empty MP4')
    info=probe(video);streams=info['streams']
    streams_video=[s for s in streams if s['codec_type']=='video']
    streams_audio=[s for s in streams if s['codec_type']=='audio']
    if len(streams_video)!=1:raise RuntimeError('Expected one video stream')
    expected={'preview':(854,480),'fullhd':(1920,1080)}[quality]
    stream=streams_video[0]
    if (stream['width'],stream['height'])!=expected:raise RuntimeError('Wrong dimensions')
    if voice=='on' and not streams_audio:raise RuntimeError('Narration requested but MP4 has no audio stream')
    planned=json.loads((ROOT/'int01/runtime_plan.json').read_text(encoding='utf8'))
    if planned['voice']!=voice:raise RuntimeError('Runtime audio mode mismatch')
    length=float(info['format']['duration']);target=float(planned['total_duration'])
    if abs(length-(target+.6))>max(6,target*.015):raise RuntimeError(f'Timeline mismatch {length:.1f} vs {target:.1f}')
    out=ROOT/'artifacts/int01_qa';out.mkdir(parents=True,exist_ok=True)
    cursor=0.;images=[]
    for i in range(8):
        chapter=planned['segments'][i*4:i*4+4]
        midpoint=cursor+sum(b['duration'] for b in chapter[:2])
        target_png=out/f'chapter_{i+1:02d}.png'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(midpoint),'-i',str(video),
                        '-frames:v','1',str(target_png)],check=True)
        if not target_png.is_file() or target_png.stat().st_size<1000:
            raise RuntimeError('Empty chapter snapshot '+str(i+1))
        images.append(str(target_png.relative_to(ROOT)))
        cursor+=sum(s['duration'] for s in chapter)
    report=dict(result='AUTOMATED_TECHNICAL_QA_PASS__VISUAL_REVIEW_REQUIRED',
                episode='INT01',voice=voice,expected_resolution=expected,duration=length,
                audio_tracks=len(streams_audio),snapshots=images,
                note='Automated probe does not establish mathematical or visual quality. Watch video and listen to voice.')
    (out/'qa_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('INT01_QA_OK',quality,voice,'duration',round(length,2),'audio',len(streams_audio),'images',len(images))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--video',type=Path,required=True)
    p.add_argument('--quality',choices=['preview','fullhd'],default='preview')
    p.add_argument('--voice',choices=['on','off'],default='off');args=p.parse_args()
    qa(args.video,args.quality,args.voice)
