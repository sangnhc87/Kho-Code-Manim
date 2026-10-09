"""Create full and incremental GitHub bundles, validate entries against STAT09 base."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/mnt/data/work_STAT09')
FULL=Path('/mnt/data/SangMath_ThongKe_STAT01_STAT10_GitHubReady.zip')
PATCH=Path('/mnt/data/SangMath_ThongKe_STAT10_Patch_GitHubReady.zip')
EXCLUDE={'__pycache__','.pytest_cache','.DS_Store'}

def valid(p):
    return all(z not in EXCLUDE for z in p.parts) and p.suffix not in ('.pyc',) and 'voice' not in p.parts

def files(root):
    return {p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and valid(p.relative_to(root))}
current=files(ROOT);previous=files(BASE)
missing=set(previous)-set(current)
if missing:raise RuntimeError(f'Existing old files missing: {sorted(missing)}')
changed=[]
for key,prev in previous.items():
    if sha256(prev.read_bytes()).digest()!=sha256(current[key].read_bytes()).digest():changed.append(key)
expected_changed={'README.md','README_THONG_KE_SERIES.md'}
if set(changed)!=expected_changed:raise RuntimeError(f'Unexpected changes in existing episodes: {changed}')
new=sorted(set(current)-set(previous))
assert any(s.startswith('stat10/') for s in new)
assert any(s.startswith('scripts/build_stat10') for s in new)
assert '.github/workflows/render-stat10.yml' in new
for zipfile,names in ((FULL,sorted(current)),(PATCH,sorted(set(new)|set(changed)))):
    with ZipFile(zipfile,'w',compression=ZIP_DEFLATED,compresslevel=8) as z:
        for name in names:z.write(current[name],arcname=name)
    with ZipFile(zipfile) as z:
        assert z.testzip() is None
        members=set(z.namelist())
        required={'stat10/scene.py','stat10/lesson.py','.github/workflows/render-stat10.yml',
                  'scripts/build_stat10_typst.py','scripts/check_stat10_states.py',
                  'scripts/prepare_stat10.py','scripts/qa_stat10.py',
                  'LOI_GIANG_STAT10.md','STORYBOARD_STAT10.md',
                  'preview/stat10/STAT10_storyboard_8_chapters.png',
                  'HUONG_DAN_RENDER_STAT10.md', 'STAT10_vi.srt'}
        assert required.issubset(members),sorted(required-members)
    print(zipfile.name,'entries',len(names),'size_MB',round(zipfile.stat().st_size/1e6,2))
print('STAT01-STAT09_UNCHANGED',len(previous)-len(changed),'old files; README updates',len(changed))
print('STAT10_NEW_FILES',len(new))
