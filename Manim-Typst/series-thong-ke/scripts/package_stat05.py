"""Package complete and incremental STAT05 GitHub Ready distributions; verify hashes."""
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD=Path('/mnt/data/work_STAT04')
OUTPUT=Path('/mnt/data')
sys.path.insert(0,str(ROOT))
from scripts.build_stat05_typst import FORMULAS
from stat05.lesson import BASE,EXTREME,EXERCISE,BEATS,validate

validate()
for name,formula in FORMULAS.items():
    (ROOT/'typst'/'stat05'/f'{name}.typ').write_text(
        '#set page(width: auto, height: auto, margin: 5pt)\n'
        '#set text(size: 20pt, fill: rgb("#edf6ff"))\n'
        +formula+'\n',encoding='utf-8')

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def include(path):
    rel=path.relative_to(ROOT)
    return '__pycache__' not in rel.parts and path.suffix not in ('.pyc','.pyo')

old_files={p.relative_to(OLD).as_posix():p for p in OLD.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
new_files={p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file() and include(p)}
modified=[f for f,p in old_files.items() if f in new_files and digest(p)!=digest(new_files[f])]
missing=[f for f in old_files if f not in new_files]
if missing:raise AssertionError(('Old files missing',missing))
if sorted(modified)!=['README.md','README_THONG_KE_SERIES.md']:
    raise AssertionError(('Unexpected old files modified',modified))
added=sorted(set(new_files)-set(old_files))
assert 'stat05/scene.py' in added and 'stat05/lesson.py' in added
assert '.github/workflows/render-stat05.yml' in added

manifest={'episode':'STAT05','name':'Khoang bien thien, IQR va bieu do hop',
    'old_episodes':['STAT01','STAT02','STAT03','STAT04'],
    'beats':len(BEATS),'base_duration_seconds':sum(x.duration for x in BEATS),
    'figures':8,'source_data':'stat01/lesson.py (synthetic scores)',
    'quartile_convention':'stat04/lesson.py (median-of-halves)',
    'baseline_five_numbers':[BASE[x] for x in ('minimum','q1','median','q3','maximum')],
    'baseline_outliers':list(BASE['outliers']),
    'extreme_outliers':list(EXTREME['outliers']),
    'exercise_outliers':list(EXERCISE['outliers']),
    'old_files_missing':len(missing),
    'old_files_unchanged':len(old_files)-len(modified),
    'old_files_changed':modified,
    'new_files':len(added),
    'tests_status':'run unittest on runner; not an attestation of Manim render',
    'manim_rendered_here':False,'typst_compiled_here':False,
    'artifacts_expected':['STAT05.mp4','STAT05_vi.srt','eight review frames']}
manifest_path=ROOT/'STAT05_MANIFEST.json'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
new_files['STAT05_MANIFEST.json']=manifest_path

full_path=OUTPUT/'SangMath_ThongKe_STAT01_STAT05_GitHubReady.zip'
patch_path=OUTPUT/'SangMath_ThongKe_STAT05_Patch_GitHubReady.zip'
patch_keys=set(added)|set(modified)|{'STAT05_MANIFEST.json'}

def make(path,keys):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for name in sorted(keys):z.write(new_files[name],arcname=name)
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:raise AssertionError('ZIP integrity failure')
        if set(z.namelist())!=set(keys):raise AssertionError('ZIP entries mismatch')
    return (len(keys),round(path.stat().st_size/1024/1024,2))

full=make(full_path,new_files)
patch=make(patch_path,patch_keys)
print('STAT05_PACKAGED_SUCCESSFULLY')
print('STAT05_OLD_UNCHANGED',len(old_files)-len(modified),'OLD_MODIFIED',modified)
print('STAT05_FULL',full_path.name,'files',full[0],'MiB',full[1])
print('STAT05_PATCH',patch_path.name,'files',patch[0],'MiB',patch[1])
print('STAT05_ZIP_INTEGRITY PASS')
