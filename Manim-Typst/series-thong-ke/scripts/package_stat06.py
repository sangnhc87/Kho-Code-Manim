"""Create cumulative and additive STAT06 GitHub zips, verify integrity and old files."""
from __future__ import annotations
from pathlib import Path
import hashlib,zipfile,json
ROOT=Path(__file__).resolve().parents[1]
OLD=Path('/mnt/data/work_STAT05')
BASE=Path('/mnt/data')
CUM=BASE/'SangMath_ThongKe_STAT01_STAT06_GitHubReady.zip'
PATCH=BASE/'SangMath_ThongKe_STAT06_Patch_GitHubReady.zip'

def source_files():
    return [p for p in ROOT.rglob('*') if p.is_file() and not any(q in p.parts for q in (
        '__pycache__','voice','media','.git','artifacts')) and p.suffix not in ('.pyc',)]

files=source_files()
old=[p for p in OLD.rglob('*') if p.is_file() and not any(q in p.parts for q in (
   '__pycache__','media','.git','artifacts','voice')) and p.suffix!='.pyc']
exceptions={'README.md','README_THONG_KE_SERIES.md'}
for f in old:
    rel=f.relative_to(OLD)
    target=ROOT/rel
    if not target.is_file():raise RuntimeError(f'Deleted legacy file: {rel}')
    if rel.as_posix() not in exceptions:
        if hashlib.sha256(f.read_bytes()).digest()!=hashlib.sha256(target.read_bytes()).digest():
            raise RuntimeError(f'Old source changed: {rel}')

new_paths={p.relative_to(ROOT).as_posix() for p in files}-{p.relative_to(OLD).as_posix() for p in old}
patch_paths=new_paths|exceptions

def write_zip(target,relpaths):
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as archive:
        for rel in sorted(relpaths):archive.write(ROOT/rel,arcname=rel)
    with zipfile.ZipFile(target) as archive:
        bad=archive.testzip()
        if bad:raise RuntimeError(f'Corrupt ZIP member: {bad}')
        found=set(archive.namelist())
        if found!=set(relpaths):raise RuntimeError('ZIP manifest mismatch')
        for need in ('.github/workflows/render-stat06.yml','stat06/scene.py',
                     'stat06/lesson.py','tests/test_stat06.py','STAT06_vi.srt'):
            if need not in found:raise RuntimeError(f'Missing required file: {need}')
    return len(relpaths),target.stat().st_size
full=write_zip(CUM,{p.relative_to(ROOT).as_posix() for p in files})
patch=write_zip(PATCH,patch_paths)
print('OLD_SOURCE_FILES_PRESERVED',len(old)-len(exceptions))
print('ZIP_FULL',CUM,'files',full[0],'bytes',full[1])
print('ZIP_PATCH',PATCH,'files',patch[0],'bytes',patch[1])
