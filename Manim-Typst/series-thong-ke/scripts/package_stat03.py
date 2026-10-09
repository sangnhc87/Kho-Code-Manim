from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT.parent
SKIP_PARTS={'__pycache__','.pytest_cache','.git','media','artifacts','voice'}
IGNORE_SUFFIX={'.pyc','.mp4','.mp3'}
BASE_ZIP=TARGET/'SangMath_ThongKe_STAT01_STAT02_GitHubReady.zip'
FULL_ZIP=TARGET/'SangMath_ThongKe_STAT01_STAT02_STAT03_GitHubReady.zip'
PATCH_ZIP=TARGET/'SangMath_ThongKe_STAT03_Patch_GitHubReady.zip'

new_items=[]
for f in ROOT.rglob('*'):
    if not f.is_file():continue
    rel=f.relative_to(ROOT)
    if any(seg in SKIP_PARTS for seg in rel.parts):continue
    if f.suffix in IGNORE_SUFFIX:continue
    # avoid runtime-created SVG (not in this environment)
    new_items.append((rel.as_posix(),f))
new_items.sort()
required=['.github/workflows/render-stat03.yml','stat03/lesson.py',
          'stat03/scene.py','scripts/prepare_stat03.py','scripts/qa_stat03.py',
          'scripts/build_stat03_typst.py','tests/test_stat03.py',
          'LOI_GIANG_STAT03.md','STORYBOARD_STAT03.md',
          'preview/stat03/STAT03_storyboard_8_chapters.png']
byname={name:path for name,path in new_items}
assert all(r in byname for r in required)
old_content={}
with zipfile.ZipFile(BASE_ZIP) as z:
    for name in z.namelist():old_content[name]=z.read(name)
changed={name for name,f in new_items if name in old_content and f.read_bytes()!=old_content[name]}
assert changed=={'README.md','README_THONG_KE_SERIES.md'},changed
assert all(name in byname for name in old_content)
new_count=sum(name not in old_content for name,f in new_items)
metadata={
    'title':'SangMath STAT03 - Mean Median Mode',
    'new_episode':'STAT03',
    'baseline_zip':BASE_ZIP.name,
    'base_entries':len(old_content),
    'new_entries':new_count,
    'baseline_changed':sorted(changed),
    'duration_silent_seconds':800,
    'python_unittests_passed':125,
    'manim_render_verified':False,
    'typst_compilation_verified':False,
    'readme':'Code ready for GitHub Actions preview; real render still needs pedagogical QA.'
}
meta_file=ROOT/'STAT03_MANIFEST.json';meta_file.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
new_items.append((meta_file.name,meta_file))

def pack(out,selected):
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for name,f in selected:z.write(f,arcname=name)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        names=set(z.namelist())
        assert set(required).issubset(names)
        if out==FULL_ZIP:
            assert set(old_content).issubset(names)
            for key,content in old_content.items():
                if key not in changed:assert z.read(key)==content,key
        print(out.name,len(names),'files',round(out.stat().st_size/1024/1024,2),'MiB','ZIP_OK')
pack(FULL_ZIP,new_items)
patch=[(name,f) for name,f in new_items if name not in old_content or name in changed]
pack(PATCH_ZIP,patch)
print('Preserved baseline files unchanged:',len(old_content)-len(changed),'of',len(old_content))
print('New source files:',new_count)
