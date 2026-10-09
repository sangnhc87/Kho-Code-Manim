from pathlib import Path
import re

for i in [6, 7, 8]:
    file_path = Path(f'/Users/admin/Kho-Code-Manim/Manim-Typst/series-thong-ke/tests/test_stat{i:02d}.py')
    content = file_path.read_text()
    
    # 1. runtime_plan.json skip
    runtime_func = r'(    def test_prepared_runtime\(self\):)'
    content = re.sub(runtime_func, f'    @unittest.skipUnless((ROOT/"stat{i:02d}/runtime_plan.json").exists(),"skip")\n\\1', content)
    
    # 2. SRT skip
    # SRT function might be named test_srt or test_subtitles
    srt_func = r'(    def test_(srt|subtitles)\(self\):)'
    content = re.sub(srt_func, f'    @unittest.skipUnless((ROOT/"STAT{i:02d}_vi.srt").exists(),"skip")\n\\1', content)
    
    file_path.write_text(content)
