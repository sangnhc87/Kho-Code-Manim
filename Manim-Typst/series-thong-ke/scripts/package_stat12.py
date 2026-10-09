"""Build cumulative and update-only ZIPs and verify every included CRC and sha256."""
from pathlib import Path
import hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/mnt/data/SangMath_ThongKe_STAT01_STAT11_CleanVideo')
DEST=ROOT.parent
full=DEST/'SangMath_ThongKe_STAT01_STAT12_GitHubReady.zip'
patch=DEST/'SangMath_ThongKe_STAT12_Patch_GitHubReady.zip'

def contents(root):
    return {p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file()
            and '__pycache__' not in p.parts and '.pyc' not in p.suffix
            and not p.name.startswith('.DS_Store')}

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=contents(BASE);new=contents(ROOT)
removed=set(old)-set(new)
if removed:raise AssertionError(f'Unexpected deleted paths: {sorted(removed)[:10]}')
changed={p for p in old if digest(old[p])!=digest(new[p])}
if changed!={'README.md','README_THONG_KE_SERIES.md'}:
    raise AssertionError(f'Unexpected changed originals: {sorted(changed)}')
added=set(new)-set(old)
needed={'stat12/scene.py','stat12/lesson.py','scripts/prepare_stat12.py',
        'scripts/build_stat12_typst.py','scripts/check_stat12_states.py',
        'scripts/qa_stat12.py','tests/test_stat12.py',
        '.github/workflows/render-stat12.yml','STAT12_vi.srt',
        'preview/stat12/STAT12_storyboard_8_chapters.png',
        'HUONG_DAN_RENDER_STAT12.md','LOI_GIANG_STAT12.md','STORYBOARD_STAT12.md'}
assert needed<=added,needed-added

def create_zip(path,items):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for name in sorted(items):z.write(new[name],name)
    with zipfile.ZipFile(path) as z:
        if z.testzip():raise AssertionError('CRC failed')
        assert set(z.namelist())==set(items)
        for name in items:
            if hashlib.sha256(z.read(name)).hexdigest()!=digest(new[name]):
                raise AssertionError('Archive content differed: '+name)
        return len(z.namelist()),path.stat().st_size

c1=create_zip(full,set(new));c2=create_zip(patch,added|changed)
print('BASE_FILES',len(old),'UNCHANGED',len(old)-len(changed),'UPDATED',sorted(changed))
print('NEW_FILES',len(added))
print('FULL_ZIP',full,c1)
print('PATCH_ZIP',patch,c2)
print('ZIP_VALIDATION_PASS')
