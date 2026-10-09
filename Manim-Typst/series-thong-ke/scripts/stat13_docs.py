"""Regenerate spoken lecture, shot plan and per-episode metadata from source-of-truth."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat13.lesson import (A,B,PA,PB,EA,EB,BEATS,CHAPTERS,
    GROUPED_A,GROUPED_B,validate)
validate()
head='# STAT13 – SO SÁNH HAI MẪU SỐ LIỆU'
lect=[head,'',
    '**Khối lớp:** 10–12, ôn tập và vận dụng thống kê mô tả.',
    '**Đặc điểm:** bộ số liệu mô phỏng, lời đọc nam tiếng Việt. Hai mẫu 10 điểm giả lập dùng chung thang điểm.',
    '**Nguyên tắc:** mô tả trong mẫu, không suy diễn quan hệ nhân quả hay suy rộng tổng thể.',
    '']
shot=['# STORYBOARD STAT13 – SO SÁNH HAI MẪU SỐ LIỆU','',
    '**Chuẩn video:** hai cột cố định, hình học–biểu đồ bên trái, đề bài–lập luận bên phải.',
    '**Footer:** Thầy Nguyễn Văn Sang. Không dùng nhãn điều phối hay số bước nội bộ trên video.',
    '**Phân cảnh:** 8 chương, mỗi chương 4 trạng thái. Công thức SVG xuất hiện từ trạng thái thứ ba của chương.',
    '**Thống kê:** phương sai chia cho n; quy ước tứ phân vị theo trung vị của hai nửa mẫu.',
    '']
scenes=('Hai trục điểm và vạch trung bình cùng vị trí',
        'Hai dãy điểm sắp tăng dần, lần lượt hiện ba số đo trung tâm',
        'Dựng hai biểu đồ hộp trên cùng trục; nhấn mạnh độ rộng hộp',
        'Các chấm cách trung bình; nối các đoạn độ lệch và hiện phương sai',
        'Hai histogram có cùng ranh giới lớp, trung điểm và tổng tần số',
        'Hai dãy ô màu đạt chuẩn, thay ngưỡng từ sáu đến chín',
        'Bốn thẻ cảnh báo: đơn vị, ngoại lệ, tính đại diện, suy diễn',
        'Hai bài tập tám điểm; từng bước hiện trung bình, IQR, phương sai')
for i,chapter in enumerate(CHAPTERS,1):
    lect.extend([f'## Chương {i:02d}. {chapter}',''])
    shot.extend([f'## Chương {i:02d}. {chapter}','',f'**Minh họa:** {scenes[i-1]}.',''])
    for beat in BEATS[(i-1)*4:i*4]:
        lect.extend([f'### {beat.title}',beat.voice,''])
        shot.extend([f'**{beat.title}**',
            f'- Luận điểm chính: {beat.thesis}',
            '- Cảnh hiển thị đúng phần kiến thức đang giảng, không hiện kết luận quá sớm.',
            '- Chỉ thay đổi số liệu theo nguồn duy nhất trong stat13/lesson.py.',''])
(ROOT/'LOI_GIANG_STAT13.md').write_text('\n'.join(lect),encoding='utf-8')
(ROOT/'STORYBOARD_STAT13.md').write_text('\n'.join(shot),encoding='utf-8')
manifest={
    'episode':'STAT13','lesson_title':'So sánh hai mẫu số liệu',
    'chapters':8,'scenes':32,'base_seconds':sum(b.duration for b in BEATS),
    'formula_svgs':8,'voice_default':'vi-VN-NamMinhNeural',
    'footer':'Thầy Nguyễn Văn Sang','internal_counters_visible':False,
    'two_groups':{'A':list(A),'B':list(B)},
    'metrics':{'A':PA.__dict__,'B':PB.__dict__,
               'grouped_mean_A':GROUPED_A.mean,'grouped_mean_B':GROUPED_B.mean,
               'grouped_var_A':GROUPED_A.variance,'grouped_var_B':GROUPED_B.variance,
               'practice_variances':[EA.variance,EB.variance]},
    'status':'source_tested_real_manim_typst_render_pending'}
(ROOT/'STAT13_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('STAT13_DOCS_OK','chapters',len(CHAPTERS),'beats',len(BEATS),'words',sum(len(b.voice.split()) for b in BEATS))
