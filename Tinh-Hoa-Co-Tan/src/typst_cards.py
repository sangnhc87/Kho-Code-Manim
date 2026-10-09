"""Render title/outro as real Typst PNG cards for the video."""
import json
import shutil
import subprocess
from pathlib import Path


def make_cards(data, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    if not shutil.which('typst'):
        raise RuntimeError('Typst CLI not installed (GitHub workflow uses typst-community/setup-typst@v5).')

    # Copy QR code asset to destination folder for local referencing in Typst
    assets_qr = Path(__file__).resolve().parents[1] / 'assets' / 'qr_coffee.jpg'
    has_qr = assets_qr.exists()
    if has_qr:
        shutil.copyfile(assets_qr, folder / 'qr_coffee.jpg')

    category = data.get('category', 'CHUYÊN ĐỀ CỜ TÀN')
    title_literal = json.dumps(data.get('title', 'TINH HOA CỜ TÀN'), ensure_ascii=False)
    subhead_literal = json.dumps(data.get('subtitle', 'Tuyển tập cờ tàn căn bản đến nâng cao'), ensure_ascii=False)
    cat_literal = json.dumps(category.upper(), ensure_ascii=False)

    intro_src = f'''#set page(width: 170mm, height: 92mm, margin: (x: 10mm, top: 8mm, bottom: 8mm), fill: rgb("#0d1829"))
#set text(fill: rgb("#f9eee0"))
#rect(width: 35mm, height: 1.2mm, fill: rgb("#E9B66E"))
#v(3mm)
#text(size: 11pt, fill: rgb("#E9B66E"), weight: "bold")[TINH HOA CỜ TÀN  •  #text(fill: rgb("#E9B66E"))[{category.upper()}]]
#v(3mm)
#text(size: 21pt, weight: "bold", fill: rgb("#FFFFFF"), {title_literal})
#v(3mm)
#text(size: 11.5pt, fill: rgb("#B8C9DA"), {subhead_literal})
#v(1fr)
#text(size: 9.5pt, fill: rgb("#E9B66E"))[Tuyệt kỹ và bí quyết cờ tàn căn bản đến nâng cao • Chúc các bạn kỳ nghệ tinh tiến!]
'''

    if has_qr:
        outro_src = '''#set page(width: 170mm, height: 92mm, margin: (x: 8mm, top: 6mm, bottom: 5mm), fill: rgb("#0d1829"))
#set text(fill: rgb("#f9eee0"))

#grid(
  columns: (1fr, 48mm),
  gutter: 6mm,
  align: (left + top, center + horizon),
  [
    #rect(width: 35mm, height: 1.2mm, fill: rgb("#E9B66E"))
    #v(2.5mm)
    #text(size: 11pt, fill: rgb("#E9B66E"), weight: "bold")[TINH HOA CỜ TÀN  •  GIAO LƯU HỌC HỎI]
    #v(2mm)
    #text(size: 18pt, weight: "bold", fill: rgb("#FFFFFF"))[BẠN ĐÃ NẮM ĐƯỢC BÍ QUYẾT?]
    #v(2mm)
    #text(size: 9.5pt, fill: rgb("#B8C9DA"))[
      Cảm ơn bạn đã theo dõi! Nếu thấy bài phân tích hữu ích, hãy ủng hộ kênh một ly cà phê để tiếp thêm năng lượng sáng tạo nhé! ☕
    ]
    #v(3mm)
    #rect(
      width: 100%,
      fill: rgb("#16253b"),
      stroke: 0.5pt + rgb("#35465d"),
      radius: 3pt,
      inset: (x: 3.5mm, y: 2.5mm)
    )[
      #grid(
        columns: (auto, 1fr),
        gutter: 2.5mm,
        [#text(size: 9pt, fill: rgb("#E9B66E"), weight: "bold")[Ngân hàng:]],
        [#text(size: 9pt, fill: rgb("#FFFFFF"))[VPBank (Việt Nam Thịnh Vượng)]],
        [#text(size: 9pt, fill: rgb("#E9B66E"), weight: "bold")[Số tài khoản:]],
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
      #image("qr_coffee.jpg", height: 68mm, fit: "contain")
    ]
    #v(1.5mm)
    #text(size: 8.5pt, fill: rgb("#E9B66E"), weight: "bold")[Quét VietQR trên App Ngân hàng]
  ]
)
'''
    else:
        outro_src = '''#set page(width: 170mm, height: 92mm, margin: (x: 10mm, top: 8mm, bottom: 8mm), fill: rgb("#0d1829"))
#set text(fill: rgb("#f9eee0"))
#rect(width: 35mm, height: 1.2mm, fill: rgb("#E9B66E"))
#v(3mm)
#text(size: 11pt, fill: rgb("#E9B66E"), weight: "bold")[TINH HOA CỜ TÀN]
#v(3mm)
#text(size: 21pt, weight: "bold", fill: rgb("#FFFFFF"))[BẠN ĐÃ NẮM ĐƯỢC BÍ QUYẾT?]
#v(3mm)
#text(size: 11.5pt, fill: rgb("#B8C9DA"))[Hãy thử giải lại thế cờ mà không nhìn đáp án để khắc sâu bài học!]
#v(1fr)
#text(size: 9.5pt, fill: rgb("#E9B66E"))[☕ Mời tôi ly cà phê — VPBank: 10389821115 (Ung ho ca phe)]
'''

    cards = [('intro', intro_src), ('outro', outro_src)]
    for kind, src_text in cards:
        src_file = folder / f'{kind}.typ'
        src_file.write_text(src_text, encoding='utf-8')
        subprocess.run(['typst', 'compile', '--format', 'png', '--ppi', '165', str(src_file), str(folder / f'{kind}.png')], check=True)
