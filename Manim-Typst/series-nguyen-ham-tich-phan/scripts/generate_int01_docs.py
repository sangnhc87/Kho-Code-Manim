from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from int01.lesson import SEGMENTS,CHAPTERS,FORMULAS

def generate():
    sb=['# INT01 – STORYBOARD 8 CHƯƠNG, 32 PHÂN CẢNH',
        '', '**Bài:** Đi ngược đạo hàm – Bản chất của nguyên hàm.',
        '', '**Tổng thời lượng nền:** 864 giây = 14 phút 24 giây (khi bật TTS có thể tăng).',
        '', '**Khung:** 16:9, 2 cột cố định, đồ thị trái / giảng giải và Typst phải.',
        '', '**Lưu ý:** Các số phân cảnh trong tài liệu chỉ để sản xuất, tuyệt đối không hiển thị trong video.',
        '']
    speech=['# INT01 – KỊCH BẢN LỜI GIẢNG GIỌNG NAM',
        '', 'Giọng mặc định `vi-VN-NamMinhNeural`; giọng đọc cần được nghe và rà soát trước khi phát hành.',
        '', 'Không đọc tên kỹ thuật của cảnh, số phân đoạn, tên công cụ hoặc tên phần mềm.', '']
    for i,chapter in enumerate(CHAPTERS,1):
        sb.extend([f'## Chương {i:02d} – {chapter}', ''])
        speech.extend([f'## Chương {i:02d} – {chapter}',''])
        for item in SEGMENTS[(i-1)*4:i*4]:
            sb.extend([f'### Phân cảnh {i:02d}.{item.step:02d} – {item.title}',
                       f'- **Thông điệp:** {item.takeaway}',
                       f'- **Mô hình động:** `{item.visual}`.',
                       f'- **Công thức Typst:** `{item.formula}` → `$'+FORMULAS[item.formula]+'$`.',
                       f'- **Thời lượng nền:** {item.duration:.0f} giây.',
                       f'- **Thuyết minh:** {item.voice}',''])
            speech.extend([f'### {item.title}',item.voice,''])
    (ROOT/'STORYBOARD_INT01.md').write_text('\n'.join(sb)+'\n',encoding='utf8')
    (ROOT/'LOI_GIANG_INT01.md').write_text('\n'.join(speech)+'\n',encoding='utf8')
    print('INT01_DOCS_OK',len(SEGMENTS),'segments')
if __name__=='__main__':generate()
