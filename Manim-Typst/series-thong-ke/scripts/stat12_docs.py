"""Generate narration text, storyboard and an episode manifest from the actual lesson."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from stat12.lesson import BEATS,CHAPTERS,MAIN,OTHER,RAW,PRACTICE,validate
validate()
lines=['# STAT12 – PHƯƠNG SAI VÀ ĐỘ LỆCH CHUẨN CỦA MẪU SỐ LIỆU GHÉP NHÓM',
       '', 'Bài giảng Thống kê lớp 12. Lời đọc: nam giới tiếng Việt. Bản dữ liệu 40 điểm được mô phỏng để minh họa.',
       'Số liệu ghép nhóm được tính từ trung điểm lớp nên phải nêu rõ tính chất ước lượng.','']
frames=['# STORYBOARD STAT12 – 32 phân cảnh trong 8 chương','',
        'Footer xuất hiện trên video: **Thầy Nguyễn Văn Sang**. Không hiển thị bộ đếm, mã nội bộ hay tên công nghệ.','',
        'Hình được chia hai cột: mô hình bên trái, lập luận và công thức bên phải. Công thức chỉ xuất hiện ở phần cuối mỗi chương.','']
for i,title in enumerate(CHAPTERS,1):
    lines.extend([f'## Chương {i:02d}. {title}',''])
    frames.extend([f'## Chương {i:02d}. {title}',''])
    for beat in BEATS[(i-1)*4:i*4]:
        lines.extend([f'### {beat.title}',beat.voice,''])
        frames.extend([f'**{beat.step}. {beat.title}**',f'- Nhận xét chính: {beat.thesis}',
         '- Hình: biểu đồ/cột/trục số thay đổi theo dữ liệu; kết luận chỉ hiện khi đã giải thích.',''])
(ROOT/'LOI_GIANG_STAT12.md').write_text('\n'.join(lines),encoding='utf-8')
(ROOT/'STORYBOARD_STAT12.md').write_text('\n'.join(frames),encoding='utf-8')
manifest={
 'episode':'STAT12', 'name':'Phương sai và độ lệch chuẩn mẫu số liệu ghép nhóm',
 'chapters':8,'lesson_states':32,'designed_duration_seconds':sum(b.duration for b in BEATS),
 'formula_svgs':8,'narration_voice_default':'vi-VN-NamMinhNeural',
 'footer':'Thầy Nguyễn Văn Sang','screen_internal_counters':False,
 'measurements':{'grouped_mean':MAIN.mean,'grouped_variance':MAIN.variance,'grouped_sd':MAIN.sd,
 'raw_mean':RAW.mean,'raw_variance':RAW.variance,'comparison_variance':OTHER.variance,
 'practice_variance':PRACTICE.variance},
 'status':'code_prepared_not_yet_real_manim_rendered'}
(ROOT/'STAT12_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('STAT12_DOCS_PASS',len(BEATS),'states; narration words',sum(len(b.voice.split()) for b in BEATS))
