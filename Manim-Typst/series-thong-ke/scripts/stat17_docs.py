"""Generate narration, detailed storyboard and release manifest from one source of truth."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat17.lesson import (BEATS,CHAPTERS,X,Y,PRACTICE_X,PRACTICE_Y,statistics,
                           OUTLIER_Y,CURVED_Y,validate)
from scripts.build_stat17_typst import FORMULAS
validate()
lecture=['# STAT17 – TƯƠNG QUAN VÀ HỒI QUY TUYẾN TÍNH','',
    '**Đối tượng:** Học sinh THPT, phần tương quan và hồi quy là mở rộng ứng dụng thống kê.',
    '**Số liệu:** giả lập, không suy luận nhân quả từ mô tả mẫu.',
    '**Giọng nam:** `vi-VN-NamMinhNeural` khi bật TTS.',
    '**Footer trong video:** Thầy Nguyễn Văn Sang.','']
board=['# STAT17 – STORYBOARD 8 CHƯƠNG, 32 PHÂN CẢNH','',
    '**Bố cục video:** cột trái là đám mây điểm và hình động; cột phải là dữ kiện, lập luận và công thức.',
    '**Chuẩn hình:** không nhãn điều phối, không chú thích kỹ thuật, footer chỉ ghi Thầy Nguyễn Văn Sang.',
    '**Nguyên tắc:** không dùng r hay R² để suy luận nhân quả. Phân biệt dự báo, nội suy và ngoại suy.',
    '**Chú ý:** bản storyboard là minh họa thiết kế, không phải bản render Manim.','']
brief=(
 'Tám điểm bật lần lượt theo cặp quan sát, x giờ ôn – y điểm kiểm tra.',
 'Ba dạng đám mây: dương, âm, đường cong hình U có r bằng 0.',
 'Trung bình và tâm đám mây; Sxx, Syy, Sxy; tính hệ số Pearson.',
 'Dựng đường ŷ = 8/7 + (6/7)x lên cùng tám điểm.',
 'Phần dư thẳng đứng và ý nghĩa bình phương tối thiểu.',
 'Điểm dự đoán x=5; ngoại suy x>8; r bình phương.',
 'Điểm ngoại lệ x=8, y:9→18, đường cong hình U và cảnh báo nhân quả.',
 'Năm điểm mới; lời giải có trì hoãn tới phân cảnh ba.',
)
for chapter,title in enumerate(CHAPTERS,1):
    lecture.extend([f'## Chương {chapter:02d}. {title}',''])
    board.extend([f'## Chương {chapter:02d}. {title}',f'**Mô hình:** {brief[chapter-1]}',''])
    for b in BEATS[(chapter-1)*4:chapter*4]:
        lecture.extend([f'### {b.title}',b.voice,''])
        board.extend([f'### {b.title}',f'**Luận điểm:** {b.thesis}',
            f'**Hình minh họa:** {brief[chapter-1]}',
            '**Hiệu ứng:** đưa dữ liệu lên trước, hiển thị suy luận sau, cuối cùng chứng minh bằng công thức.',
            '**Lời thuyết minh:** '+b.voice,''])
(ROOT/'LOI_GIANG_STAT17.md').write_text('\n'.join(lecture)+'\n',encoding='utf8')
(ROOT/'STORYBOARD_STAT17.md').write_text('\n'.join(board)+'\n',encoding='utf8')
s=statistics()
manifest={
    'episode':'STAT17','title':'Tương quan và hồi quy tuyến tính',
    'chapters':8,'scenes':32,'seconds_base':sum(b.duration for b in BEATS),
    'narration_words':sum(len(b.voice.split()) for b in BEATS),
    'footer':'Thầy Nguyễn Văn Sang','male_voice':'vi-VN-NamMinhNeural',
    'visible_internal_counters':False,'formula_count':len(FORMULAS),
    'main_x':X,'main_y':Y,'sxx':s['sxx'],'sxy':s['sxy'],'syy':s['syy'],
    'slope':s['slope'],'intercept':s['intercept'],'pearson_r':s['r'],'r_squared':s['r2'],
    'practice_x':PRACTICE_X,'practice_y':PRACTICE_Y,
    'outlier_y':OUTLIER_Y,'curved_y':CURVED_Y,
    'render_status':'PENDING: real Manim/Typst smoke render on GitHub Actions',
}
(ROOT/'STAT17_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('STAT17_DOCS_OK',len(BEATS),manifest['narration_words'])
