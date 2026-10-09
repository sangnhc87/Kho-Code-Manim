"""Generate release docs from the teaching script (single source of truth)."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from stat18.lesson import (BEATS,CHAPTERS,TRUE_P,N,VOLUNTARY_YES,
                           PRACTICE_YES,PRACTICE_N,PRACTICE_CONVENIENCE_YES,
                           sample,trials,sd_sample_proportion,approx_interval,validate)
from scripts.build_stat18_typst import FORMULAS
validate()
intro=[
    '**Khán giả:** Học sinh THPT (mở rộng tư duy lấy mẫu và suy luận thống kê).',
    '**Quần thể:** 1.000 học sinh giả lập, đúng 400 chọn A (40%).',
    '**Quy trình lấy mẫu:** ngẫu nhiên đơn không hoàn lại trong từng lần rút; các lần mô phỏng độc lập.',
    '**Không được suy rộng:** mọi số liệu ở đây hoàn toàn giả lập.',
    '**Giọng nam:** `vi-VN-NamMinhNeural`; **footer:** Thầy Nguyễn Văn Sang.',
]
lecture=['# STAT18 – LẤY MẪU, THIÊN LỆCH VÀ MÔ PHỎNG','']+intro+['']
board=['# STAT18 – STORYBOARD 8 CHƯƠNG / 32 PHÂN CẢNH','',
  '**Bố cục:** 16:9, hai cột cố định, mô hình và biểu đồ bên trái, lý giải–công thức bên phải.',
  '**Nguyên tắc:** nêu vấn đề trước, giải thích, sau đó mới hiện đáp án. Không nhãn kỹ thuật trên video.',
  '**QA:** đây là thiết kế, không phải hình dựng Manim; phải duyệt MP4 trước khi dạy.','']
visuals=(
 'Lưới 100 chấm đại diện đúng tỉ lệ 400/1000; chú thích 1 chấm ứng với 10 học sinh.',
 'Rút chính xác từ quần thể: 7/20, 37/80; so sánh với chọn thuận tiện.',
 'Biểu đồ 40% so với 70%; minh họa tự nguyện, không phản hồi và nhầm lẫn cơ bản.',
 'Histogram 300 tỉ lệ mẫu n=20 và n=80, vạch chuẩn 40%, có hạt giống cố định.',
 'Độ lệch chuẩn tỉ lệ mẫu; dùng hiệu chỉnh quần thể hữu hạn khi rút không hoàn lại.',
 'Khoảng trên trục tỉ lệ, đánh dấu 44%, hai đầu xấp xỉ 37,1% và 50,9%.',
 'Biểu đồ thiên lệch, con trỏ thật di chuyển minh họa 70% về mốc 40%; checklist.',
 'Đề bài 88/200 và 150/200; trì hoãn đáp án 44%/75% tới phân cảnh thứ ba; tổng kết.',
)
for c,title in enumerate(CHAPTERS,1):
    lecture += [f'## Chương {c:02d}. {title}','']
    board += [f'## Chương {c:02d}. {title}',f'**Thiết kế hình:** {visuals[c-1]}','']
    for b in BEATS[(c-1)*4:c*4]:
        lecture += [f'### {b.title}',b.voice,'']
        board += [f'### {b.title}',f'**Thông điệp:** {b.thesis}',
                  f'**Hình:** {visuals[c-1]}',
                  '**Dựng:** giới thiệu dữ liệu và hình trước, sau đó mới có kết quả suy luận phù hợp.',
                  f'**Lời thuyết minh:** {b.voice}','']
(ROOT/'LOI_GIANG_STAT18.md').write_text('\n'.join(lecture)+'\n',encoding='utf8')
(ROOT/'STORYBOARD_STAT18.md').write_text('\n'.join(board)+'\n',encoding='utf8')
p,lo,hi=approx_interval(PRACTICE_YES,PRACTICE_N)
manifest={
 'episode':'STAT18','title':'Lấy mẫu, thiên lệch và mô phỏng',
 'series_complete':True,'chapters':8,'scenes':len(BEATS),
 'seconds_base':sum(b.duration for b in BEATS),
 'narration_words':sum(len(b.voice.split()) for b in BEATS),
 'footer':'Thầy Nguyễn Văn Sang','male_voice':'vi-VN-NamMinhNeural',
 'visible_internal_counters':False,'formula_count':len(FORMULAS),
 'population_size':N,'population_yes':int(TRUE_P*N), 'true_p':TRUE_P,
 'random_20_yes':sum(sample(20)),'random_80_yes':sum(sample(80)),
 'simulation_repeats_each':len(trials(20)),
 'se_20':sd_sample_proportion(20),'se_80':sd_sample_proportion(80),
 'voluntary_yes':VOLUNTARY_YES,'practice_random_yes':PRACTICE_YES,
 'practice_random_n':PRACTICE_N,
 'practice_convenience_yes':PRACTICE_CONVENIENCE_YES,
 'practice_wald_interval_uncorrected':{'estimate':p,'lower':lo,'upper':hi},
 'render_status':'PENDING: Manim and Typst rendering and human visual/audio review in GitHub Actions',
}
(ROOT/'STAT18_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('STAT18_DOCS_OK',len(BEATS),manifest['narration_words'])
