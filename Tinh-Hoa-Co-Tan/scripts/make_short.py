"""Generate high-retention 9:16 vertical YouTube Shorts (1080x1920)
from standard 16:9 Manim video, with top headline banner and bottom VietQR banner.
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_short_banners(ep_data, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    title = ep_data.get('title', 'TINH HOA CỜ TÀN')
    category = ep_data.get('category', 'CỜ TÀN').upper()
    subtitle = ep_data.get('subtitle', 'Tuyệt kỹ cờ tàn thực chiến')
    
    title_literal = json.dumps(title, ensure_ascii=False)
    sub_literal = json.dumps(subtitle, ensure_ascii=False)
    
    # 1. Top Banner (1080x480 px ≈ 166mm x 74mm at 165 PPI)
    top_typ = f'''#set page(width: 166mm, height: 74mm, margin: (x: 8mm, top: 5mm, bottom: 4mm), fill: none)
#set text(fill: rgb("#f9eee0"), font: ("Liberation Sans", "Arial", "Roboto", "Segoe UI"))
#align(center)[
  #rect(width: 45mm, height: 1.5mm, fill: rgb("#E9B66E"))
  #v(2mm)
  #text(size: 13pt, fill: rgb("#E9B66E"), weight: "bold")[TINH HOA CỜ TÀN  •  {category}]
  #v(2.5mm)
  #text(size: 22pt, weight: "bold", fill: rgb("#FFFFFF"), {title_literal})
  #v(2.5mm)
  #text(size: 11.5pt, fill: rgb("#64D2FF"), weight: "medium", {sub_literal})
  #v(2mm)
  #text(size: 11pt, fill: rgb("#FF3B30"), weight: "bold")[\\#Shorts]
]
'''
    top_src = out_dir / 'short_top.typ'
    top_png = out_dir / 'short_top.png'
    top_src.write_text(top_typ, encoding='utf-8')
    subprocess.run(['typst', 'compile', '--pages', '1', '--format', 'png', '--ppi', '165', str(top_src), str(top_png)], check=True)

    # 2. Bottom Banner with VietQR (1080x480 px)
    qr_asset = ROOT / 'assets' / 'qr_coffee.jpg'
    has_qr = qr_asset.exists()
    if has_qr:
        import shutil
        shutil.copyfile(qr_asset, out_dir / 'qr_coffee.jpg')

    bot_typ = f'''#set page(width: 166mm, height: 74mm, margin: (x: 8mm, top: 5mm, bottom: 5mm), fill: none)
#set text(fill: rgb("#f9eee0"), font: ("Liberation Sans", "Arial", "Roboto", "Segoe UI"))
#grid(
  columns: (1fr, 34mm),
  gutter: 4mm,
  align: (left + horizon, center + horizon),
  [
    #rect(width: 25mm, height: 1.2mm, fill: rgb("#E9B66E"))
    #v(2mm)
    #text(size: 12.5pt, weight: "bold", fill: rgb("#E9B66E"))[☕ MỜI KÊNH LY CÀ PHÊ]
    #v(1.5mm)
    #text(size: 9.5pt, fill: rgb("#B8C9DA"))[Nếu thấy thế cờ hay, hãy tiếp thêm động lực cho kênh nhé!]
    #v(2.5mm)
    #rect(
      width: 100%,
      fill: rgb("#16253b"),
      stroke: 0.5pt + rgb("#35465d"),
      radius: 3pt,
      inset: (x: 3mm, y: 2mm)
    )[
      #grid(
        columns: (auto, 1fr),
        gutter: 2mm,
        [#text(size: 9pt, fill: rgb("#E9B66E"), weight: "bold")[VPBank:]],
        [#text(size: 11pt, weight: "bold", fill: rgb("#64D2FF"))[10389821115]],
        [#text(size: 9pt, fill: rgb("#E9B66E"), weight: "bold")[Nội dung:]],
        [#text(size: 9pt, fill: rgb("#B8C9DA"))[Ủng hộ cà phê]]
      )
    ]
  ],
  [
    #block(
      fill: rgb("#ffffff"),
      inset: 1mm,
      radius: 4pt,
      stroke: 1pt + rgb("#E9B66E"),
      clip: true
    )[
      #image("qr_coffee.jpg", height: 48mm, fit: "contain")
    ]
    #v(1mm)
    #text(size: 8pt, fill: rgb("#E9B66E"), weight: "bold")[Quét VietQR]
  ]
)
'''
    bot_src = out_dir / 'short_bot.typ'
    bot_png = out_dir / 'short_bot.png'
    bot_src.write_text(bot_typ, encoding='utf-8')
    subprocess.run(['typst', 'compile', '--pages', '1', '--format', 'png', '--ppi', '165', str(bot_src), str(bot_png)], check=True)

    return top_png, bot_png

    return top_png, bot_png


def create_short_video(input_mp4, ep_data, output_short_mp4):
    input_mp4 = Path(input_mp4)
    output_short_mp4 = Path(output_short_mp4)
    temp_dir = output_short_mp4.parent / 'short_assets'
    
    top_png, bot_png = build_short_banners(ep_data, temp_dir)
    
    # FFmpeg 9:16 vertical composition:
    # 1. Downscale background to 108:192, blur & darken, then upscale to 1080x1920 (super fast).
    # 2. Scale clean input to 1080:608 and place in the center (y=656).
    # 3. Overlay top banner at y=80.
    # 4. Overlay bottom banner at y=1360.
    cmd = [
        'ffmpeg', '-y',
        '-i', str(input_mp4),
        '-i', str(top_png),
        '-i', str(bot_png),
        '-filter_complex',
        '[0:v]scale=108:192:force_original_aspect_ratio=increase,crop=108:192,boxblur=4:2,colorchannelmixer=aa=1:rr=0.4:gg=0.4:bb=0.4,scale=1080:1920:flags=bilinear[bg]; '
        '[0:v]scale=1080:608[fg]; '
        '[bg][fg]overlay=0:656[base]; '
        '[base][1:v]overlay=0:80[with_top]; '
        '[with_top][2:v]overlay=0:1360[outv]',
        '-map', '[outv]',
        '-map', '0:a?',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '22',
        '-c:a', 'aac',
        '-shortest',
        str(output_short_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f'✅ Successfully created YouTube Short: {output_short_mp4}')


def main():
    parser = argparse.ArgumentParser(description="Generate 9:16 YouTube Shorts")
    parser.add_argument('--episode', required=True, help="Episode ID, e.g. tap-0001")
    args = parser.parse_args()
    
    ep_file = ROOT / 'episodes' / f'{args.episode}.json'
    if not ep_file.exists():
        raise SystemExit(f'Episode file {ep_file} not found!')
    
    ep_data = json.loads(ep_file.read_text(encoding='utf-8'))
    in_video = ROOT / 'output' / args.episode / f'{args.episode}.mp4'
    out_video = ROOT / 'output' / args.episode / f'{args.episode}_short.mp4'
    
    if not in_video.exists():
        raise SystemExit(f'Source video {in_video} not found!')
        
    create_short_video(in_video, ep_data, out_video)


if __name__ == '__main__':
    main()
