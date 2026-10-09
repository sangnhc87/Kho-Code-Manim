from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat01.lesson import BEATS,CHAPTERS,SCORES,FREQUENCY
lines=['# THONG-KE-01: Storyboard chi tiết và lời giảng','',
       '**Chủ đề:** Dữ liệu biết nói – từ 40 điểm đến bức tranh của lớp.','',
       '**Dữ liệu:** 40 điểm giả lập, không phải kết quả học sinh thật.','',
       '**Bố cục:** hình động bên trái, thông tin suy luận bên phải; 16:9.','',
       '**Thời lượng hình nền:** 32 × 22 = 704 giây (11 phút 44 giây).', '',
       '## Dữ liệu gốc', '',
       '`'+', '.join(map(str,SCORES))+'`','',
       '## Nhịp giảng theo chương','']
for i,b in enumerate(BEATS):
    if b.step==1:lines+=['',f'### Chương {b.chapter:02d} – {CHAPTERS[b.chapter-1]}','']
    lines+=[f'**Nhịp {i+1:02d} ({b.duration:g} giây) – {b.title}.**',
            '',f'- Ý chính hiển thị: {b.thought}',
            '- Hình động: '+('thẻ số → sắp xếp và chọn nhóm' if b.chapter<=2 else
                              'bảng tần số và tổng tích lũy' if b.chapter==3 else
                              'cột và chấm được vẽ từ bảng tần số' if b.chapter in (4,6) else
                              'biểu đồ phân bổ tỉ lệ chính xác' if b.chapter==5 else
                              'kiểm tra trục, nhập trùng, chọn mẫu' if b.chapter==7 else
                              'nhấn sáng bài tập và đáp án'),
            '',f'- Lời giảng: {b.narration}','']
(ROOT/'STORYBOARD_STAT01.md').write_text('\n'.join(lines),encoding='utf8')
(ROOT/'LOI_GIANG_STAT01.md').write_text('\n'.join(
    ['# Lời thuyết minh THONG-KE-01',
     '**32 nhịp, mỗi nhịp đọc riêng, không cắt lời.**',''] +
    [f'## {i+1:02d}. {b.title}\n\n{b.narration}\n' for i,b in enumerate(BEATS)]),encoding='utf8')
print('Storyboard markdown and narration generated.')
