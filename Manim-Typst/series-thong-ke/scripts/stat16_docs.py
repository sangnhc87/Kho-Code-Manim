"""Generate a full teacher script, instructional storyboard and metadata manifest."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat16.lesson import (BEATS,CHAPTERS,MAIN,CHALLENGE,aggregate,rate,
    pooled_easy_weight,mix,validate)
from scripts.build_stat16_typst import FORMULAS
validate()
lecture=['# STAT16 – NGHỊCH LÝ SIMPSON TRONG THỐNG KÊ','',
 '**Đối tượng:** Học sinh lớp 10–12, mở rộng tư duy phân tích số liệu.',
 '**Dữ liệu:** hoàn toàn giả lập, không đại diện cho phương pháp ôn tập thực tế.',
 '**Giọng đọc:** nam tiếng Việt `vi-VN-NamMinhNeural` khi bật TTS.',
 '**Footer trên video:** Thầy Nguyễn Văn Sang.','']
board=['# STAT16 – STORYBOARD 8 CHƯƠNG, 32 PHÂN CẢNH','',
 '**Bố cục 2 cột:** phía trái là dữ liệu, tỉ lệ, thanh cơ cấu; phía phải là câu hỏi, suy luận và công thức.',
 '**Quy tắc sư phạm:** dữ liệu giả lập, không kết luận nhân quả, không nhãn điều phối trong video.',
 '**Thứ tự tiết lộ đáp án:** chỉ hiện tỉ lệ gộp sau khi cộng số đạt và số lượt; bài cuối không lộ đáp án ở cảnh đầu.',
 '**Lưu ý:** storyboard được thiết kế bằng Pillow, không phải MP4 hoặc ảnh Manim.','']
brief=(
 'Câu hỏi lựa chọn A/B; tỉ lệ đạt trong bài dễ và bài khó.',
 'Bảng 2 × 2 và phân biệt điểm phần trăm.',
 'Cộng tử số và mẫu số; hiện đảo chiều 46% so với 75%.',
 'Thanh cơ cấu 20/80 và 90/10; trung bình có trọng số.',
 'Chuẩn hóa về cơ cấu 50/50 và cơ cấu chung 55/45.',
 'Diễn giải phạm vi quan sát; tránh suy luận nhân quả.',
 'Nhận diện lỗi trung bình giản đơn, thiếu mẫu số và suy diễn.',
 'Bài tập A: 9/10, 8/40; B: 24/30, 1/10; tự giải rồi hiện lời giải.',
)
for chapter,title in enumerate(CHAPTERS,1):
    lecture.extend([f'## Chương {chapter:02d}. {title}',''])
    board.extend([f'## Chương {chapter:02d}. {title}',f'**Mô hình:** {brief[chapter-1]}',''])
    for b in BEATS[(chapter-1)*4:chapter*4]:
        lecture.extend([f'### {b.title}',b.voice,''])
        board.extend([f'### {b.title}',f'**Luận điểm:** {b.thesis}',
                      f'**Đồ họa:** {brief[chapter-1]}',
                      '**Tiến trình:** dữ kiện → dự đoán → kiểm chứng → kết luận.','**Lời giảng:** '+b.voice,''])
(ROOT/'LOI_GIANG_STAT16.md').write_text('\n'.join(lecture)+'\n',encoding='utf8')
(ROOT/'STORYBOARD_STAT16.md').write_text('\n'.join(board)+'\n',encoding='utf8')
manifest={
 'episode':'STAT16', 'title':'Nghịch lý Simpson trong thống kê',
 'chapters':8,'scenes':32,'seconds_base':sum(x.duration for x in BEATS),
 'narration_words':sum(len(b.voice.split()) for b in BEATS),
 'footer':'Thầy Nguyễn Văn Sang','male_voice':'vi-VN-NamMinhNeural',
 'formula_count':len(FORMULAS),'visible_internal_counters':False,
 'data_main':MAIN,'data_practice':CHALLENGE,
 'overall':{m:rate(aggregate(MAIN,m)) for m in ('A','B')},
 'standardized_equal':{m:mix(MAIN,m,.5) for m in ('A','B')},
 'pooled_easy_weight':pooled_easy_weight(MAIN),
 'render_status':'PENDING real Manim/Typst render on GitHub Actions'
}
(ROOT/'STAT16_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('STAT16_DOCS_OK',manifest['scenes'],manifest['seconds_base'],manifest['narration_words'])
