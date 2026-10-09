"""Generate full spoken script, 32-shot storyboard and trustworthy lesson manifest."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat14.lesson import (QUEUE_A,QUEUE_B,QUEUE_OUTLIER,PA,PB,PO,
    EA,EB,EXERCISE_A,EXERCISE_B,RAW,GROUPED,COHORTS,BEATS,CHAPTERS,validate)
validate()
header='# STAT14 – BÀI TOÁN THỐNG KÊ TỔNG HỢP VÀ VẬN DỤNG THỰC TẾ'
lecture=[header,'','**Khối lớp:** 10–12, bài tổng hợp và vận dụng.','**Dữ liệu:** hoàn toàn giả lập, không suy diễn kết quả ra toàn bộ cộng đồng.',
 '**Giọng đọc:** nam Việt (NamMinhNeural) khi bật tính năng giọng đọc.','']
board=[header,'',
 '**Khung hình:** trái là dữ liệu, biểu đồ chính xác; phải là đề bài, luận điểm và công thức xuất hiện theo tiến trình.',
 '**Footer trong video:** Thầy Nguyễn Văn Sang.',
 '**Nội bộ:** mỗi chương bốn trạng thái; không xuất số trạng thái hoặc thông tin điều phối trên video.',
 '**Công thức:** phương sai chia n; tứ phân vị tính theo trung vị của nửa dưới và nửa trên dữ liệu.',
 '**Quy trình:** mở đề → quan sát → lập luận → kết luận, không bật đáp án trước.', '']
shots=(
  'Hai dãy chấm thời gian chờ A/B trên chung trục; thêm đường trung bình 8 phút.',
  'Hai biểu đồ hộp đồng tỉ lệ; hiện các mốc Q1 Q3, sau đó sd A/B.',
  'Hai hàng 10 ô đổi màu theo tiêu chí chờ tối đa 10 hoặc 5 phút.',
  'Một chấm 10 phút dịch đến 30 phút; đối chiếu trung bình, trung vị và phương sai.',
  'Các điểm gốc → histogram ghép nhóm, phân biệt trung bình 7,1 với 7,6.',
  'Hai nhóm lần lượt 10 và 30 học sinh: số ô đúng với quy mô.',
  'Bốn nguyên tắc báo cáo, hiện dần từng ô.',
  'Hai dãy thời gian C/D (8 giá trị): tự tính rồi mới xuất lời giải.',
)
for ch,chapter in enumerate(CHAPTERS,1):
    lecture.extend([f'## Chương {ch:02d}. {chapter}',''])
    board.extend([f'## Chương {ch:02d}. {chapter}','',f'**Mô hình động:** {shots[ch-1]}',''])
    for b in BEATS[(ch-1)*4:ch*4]:
        lecture.extend([f'### {b.title}', b.voice,''])
        board.extend([f'### {b.title}',f'**Kiến thức:** {b.thesis}',
         '**Diễn tiến:** dữ kiện xuất hiện trước, bước giải sau; không hiển thị số thứ tự kỹ thuật.',
         '**Đọc:** '+b.voice,''])
(ROOT/'LOI_GIANG_STAT14.md').write_text('\n'.join(lecture)+'\n',encoding='utf-8')
(ROOT/'STORYBOARD_STAT14.md').write_text('\n'.join(board)+'\n',encoding='utf-8')
manifest=dict(episode='STAT14', title='Bài toán thống kê tổng hợp và vận dụng thực tế',
       chapters=8,scenes=32,base_seconds=sum(b.duration for b in BEATS),
       narration_words=sum(len(b.voice.split()) for b in BEATS),
       formula_svgs=8,footer='Thầy Nguyễn Văn Sang',voice='vi-VN-NamMinhNeural',
       internal_counters_visible=False,
       observed_wait_times=dict(A=list(QUEUE_A),B=list(QUEUE_B),with_outlier=list(QUEUE_OUTLIER)),
       sample_profiles=dict(A=PA.__dict__,B=PB.__dict__,outlier=PO.__dict__),
       raw_stats=dict(mean=RAW.mean,variance=RAW.variance),
       grouped_approximations=dict(mean=GROUPED.mean,variance=GROUPED.variance),
       class_groups=list(COHORTS),practice=dict(C=EA.__dict__,D=EB.__dict__),
       stage='source_verified_real_manim_typst_render_not_yet_run')
(ROOT/'STAT14_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('STAT14_DOCS_OK',len(BEATS),manifest['narration_words'],manifest['base_seconds'])
