"""Safe zip builds; full preserves prior files and patch includes only modified/new files."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OLD=Path('/mnt/data/work_STAT06')
DEST=Path('/mnt/data')
SKIP={'__pycache__','.DS_Store','.git'}

def files(root):
    return {p.relative_to(root).as_posix():p for p in root.rglob('*')
            if p.is_file() and not any(x in SKIP for x in p.relative_to(root).parts)
            and not p.name.endswith('.pyc')}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
old=files(OLD);new=files(ROOT)
changed=[p for p in new if p not in old or sha(new[p])!=sha(old[p])]
prior_unmodified=[p for p in old if p in new and sha(old[p])==sha(new[p])]
removed=[p for p in old if p not in new]
assert not removed, f'Old source accidentally removed: {removed[:5]}'
expected_updates={'README.md','README_THONG_KE_SERIES.md'}
old_changed={p for p in changed if p in old}
assert old_changed<=expected_updates, f'Old file modified unexpectedly: {old_changed}'
need=['stat07/scene.py','stat07/lesson.py','scripts/build_stat07_typst.py',
      'scripts/prepare_stat07.py','scripts/qa_stat07.py','scripts/check_stat07_states.py',
      '.github/workflows/render-stat07.yml','tests/test_stat07.py','STAT07_vi.srt',
      'stat07/runtime_plan.json','preview/stat07/STAT07_storyboard_8_chapters.png',
      'LOI_GIANG_STAT07.md','STORYBOARD_STAT07.md','HUONG_DAN_RENDER_STAT07.md']
assert all(x in new for x in need)
manifest={
 'project':'SangMath Thong Ke / STAT07','mode':'source ready for GitHub smoke-render; MP4 not yet verified',
 'source_count':len(new),'patch_count':len(changed),'old_preserved':len(prior_unmodified),
 'old_updated':sorted(old_changed),'old_removed':removed,'new_or_changed_files':sorted(changed),
}
(ROOT/'STAT07_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
new=files(ROOT)
changed=sorted(set(changed)|{'STAT07_MANIFEST.json'})
for name,selected in [('SangMath_ThongKe_STAT01_STAT07_GitHubReady.zip',sorted(new)),
                      ('SangMath_ThongKe_STAT07_Patch_GitHubReady.zip',changed)]:
    dest=DEST/name
    with ZipFile(dest,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
        for p in selected:z.write(new[p],arcname=p)
    with ZipFile(dest) as z:
        assert z.testzip() is None
        assert all(p in z.namelist() for p in need)
    print('ZIP_OK',name,'files',len(selected),'bytes',dest.stat().st_size)
print('PREVIOUS_UNMODIFIED',len(prior_unmodified),'OLD_UPDATED',sorted(old_changed),'NO_OLD_REMOVED',not removed)
