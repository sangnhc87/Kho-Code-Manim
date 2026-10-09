"""Generate classroom-ready spoken script and 32-scene storyboard."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat15.lesson import BEATS,CHAPTERS,BAR_VALUES,YEARS,YEAR_VALUES,CLASSES,TREND_VALUES,validate
from scripts.build_stat15_typst import FORMULAS
validate()
lecture=['# STAT15 – NHỮNG BIỂU ĐỒ THỐNG KÊ GÂY HIỂU NHẦM','','**Đối tượng:** Toán 10–12.','**Dữ liệu:** các ví dụ giả lập; không cáo buộc bất kỳ tổ chức hoặc người vẽ biểu đồ nào.',
 '**Thuyết minh:** giọng nam tiếng Việt `vi-VN-NamMinhNeural` khi bật giọng đọc.','']
board=['# STORYBOARD STAT15 – TÁM CHƯƠNG, BA MƯƠI HAI PHÂN CẢNH','',
 '**Bố cục:** hai cột cố định; hình và trục bên trái; câu hỏi, lập luận và công thức bên phải.',
 '**Footer video:** Thầy Nguyễn Văn Sang.',
 '**Quy tắc hình:** không hiện bộ đếm trạng thái, lệnh dựng hay tên công nghệ; không tiết lộ đáp án trước phần phân tích.',
 '**Tính chính xác:** mọi chiều cao, diện tích, thời gian và cỡ mẫu lấy từ `stat15/lesson.py`.',
 '**Lưu ý:** hình storyboard chỉ là bản thiết kế, chưa phải ảnh xuất từ Manim.','']
visuals=[
 'Số liệu 80–100 → hai cột gốc 75 → hai cột gốc 0 → tiêu chí kiểm tra.',
 'Bốn giá trị 40–44–52–56 → trục tung hẹp 38–58 → trục rộng 0–100.',
 'Bốn năm 2020, 2021, 2024, 2025 → khoảng đều sai → khoảng thời gian thật.',
 'Hai hình tròn giá trị 20–40 → bán kính nhân hai sai → bán kính nhân căn hai đúng.',
 'Hai lớp 18/30 và 24/80 → cột số lượng → cột tỉ lệ 60% và 30%.',
 'Đoạn 2022–2023 → mở toàn bộ 2020–2025 → so ngắn hạn và toàn kỳ.',
 'Bốn lớp độ rộng 2–4–1–3 → tần số → mật độ 4–3–6–3.',
 'Thử thách 62% và 68% với gốc 60 → sửa trục gốc 0 → bốn bước tự kiểm.',
]
for ch,chapter in enumerate(CHAPTERS,1):
    lecture+= [f'## Chương {ch:02d}. {chapter}','']
    board+= [f'## Chương {ch:02d}. {chapter}',f'**Hình trực quan:** {visuals[ch-1]}','']
    for b in BEATS[(ch-1)*4:ch*4]:
        lecture.extend([f'### {b.title}',b.voice,''])
        board.extend([f'### {b.title}',f'**Thông điệp:** {b.thesis}',
            '**Trình tự:** học sinh quan sát dữ kiện → dự đoán → kiểm chứng → kết luận.','**Lời giảng:** '+b.voice,''])
(ROOT/'LOI_GIANG_STAT15.md').write_text('\n'.join(lecture)+'\n',encoding='utf8')
(ROOT/'STORYBOARD_STAT15.md').write_text('\n'.join(board)+'\n',encoding='utf8')
manifest={
 'episode':'STAT15','topic':'Những biểu đồ thống kê gây hiểu nhầm',
 'chapters':8,'scenes':32,'base_seconds':sum(b.duration for b in BEATS),
 'narration_words':sum(len(b.voice.split()) for b in BEATS),
 'formula_svg_count':len(FORMULAS),'footer':'Thầy Nguyễn Văn Sang',
 'voice':'vi-VN-NamMinhNeural','visible_internal_counters':False,
 'data':{'bar_values':BAR_VALUES,'times':YEARS,'observations':YEAR_VALUES,
  'histogram_classes':CLASSES,'trend':TREND_VALUES},
 'status':'python_mock_tested_real_manim_typst_render_pending'}
(ROOT/'STAT15_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print('STAT15_DOCS_OK',manifest['scenes'],manifest['narration_words'],manifest['base_seconds'])
