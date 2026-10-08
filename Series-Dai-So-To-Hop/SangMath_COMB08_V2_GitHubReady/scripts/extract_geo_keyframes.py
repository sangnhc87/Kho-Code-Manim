"""Sample frames of a rendered Manim video to verify visual layout."""
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--video',required=True)
    p.add_argument('--out',required=True)
    args=p.parse_args()
    target=Path(args.out)
    target.mkdir(parents=True,exist_ok=True)
    result=subprocess.check_output(['ffprobe','-v','quiet','-show_format','-of','json',args.video])
    duration=float(json.loads(result)['format']['duration'])
    shots=[]
    for n,fraction in enumerate((.03,.16,.29,.41,.54,.66,.79,.93),1):
        path=target/f'frame_{n:02}.png'
        seconds=duration*fraction
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                        '-ss',str(seconds),'-i',args.video,'-frames:v','1',str(path)],check=True)
        shots.append((seconds,path))
    board=Image.new('RGB',(1280,4*204+40),(13,20,34))
    draw=ImageDraw.Draw(board)
    for i,(seconds,path) in enumerate(shots):
        im=Image.open(path).convert('RGB')
        im=ImageOps.contain(im,(612,172))
        col,row=i%2,i//2
        left,top=col*640+14,row*204+10
        board.paste(im,(left,top))
        draw.text((left,top+174),f'{seconds:.1f}s',fill=(230,234,240))
    board.save(target/'contact_sheet.png')
    print(f'Video duration: {duration:.1f}s, extracted 8 images')

if __name__=='__main__':
    main()
