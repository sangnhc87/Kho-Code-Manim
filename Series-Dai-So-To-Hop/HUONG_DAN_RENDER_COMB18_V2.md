# COMB18 V2 - Tam giac Pascal | Huong dan GitHub Actions

## Giai nen va cap nhat repository

1. Tai `SangMath_COMB18_V2_GitHubReady.zip`, giai nen tren may tinh.
2. Mo thu muc da giai nen, **chep tat ca noi dung** (bao gom `.github` an) vao thu muc goc repository GitHub cu.
3. Commit va push. Khong tai len file ZIP nguyen khoi.
4. Mo **Actions > Render COMB18 V2 - Tam giac Pascal - tinh chat va ung dung > Run workflow**.
5. Chon `quality=preview` va `voice=off`, sau do bam Run workflow.
6. Mo run da hoan tat > Artifacts > tai file COMB18 V2 ve, mo MP4 va 8 anh chup.
7. Chi khi da xem va duyet hinh anh: chay lai `voice=on`, kiem tra phat am tieng Viet, roi `quality=fullhd` de lay ban 1920x1080 30 fps.

## Duong dan quan trong

- Manim Scene: `episodes/comb18_pascal_triangle.py`; ten Scene: `COMB18`.
- Data 48 nhip: `comb18_beats.json`, `comb18_chapters.json`, `comb18_formulas.json`, `comb18_lesson_data.py`.
- Typst + TTS + script + subtitle: `scripts/prepare_comb18_v2.py`.
- Manim post-render QA: `scripts/qa_comb18_v2.py`.
- 8 storyboard PNG: `preview/comb18_v2/`.
- 32 phep kiem tra moi: `tests/test_comb18_pascal.py`.
- GitHub workflow: `.github/workflows/render-comb18-v2.yml`.

## Lenh de debug tren may da cai Manim/Typst

```bash
python -m unittest discover -s tests -v
python scripts/prepare_comb18_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb18_pascal_triangle.py COMB18
```

Hoac dung workflow cua GitHub de cai dat Manim, Typst, FFmpeg, font Noto va thu vien phu thuoc. Giong doc `on` can ket noi internet den dich vu TTS; neu TTS loi, kiem tra hinh bang voice=off truoc.

## Quy tac giao vien can duyet

1. Nhin duoc mui ten tu hai o cha ve mot o con, khong de chuyen dong che mat so.
2. Cau hoi xuat hien truoc ket qua; cac de bai co gioi han duoc doc du bang tieng Viet.
3. Ki hieu trong cong thuc: `C^(n)_(k)` voi n o tren va k o duoi.
4. Thoi luong thiet ke it nhat 1157 giay khong TTS; ban co TTS co the dai hon.
5. Workflow chi xac nhan video neu co MP4, dung thoi luong, dung kich thuoc va co audio khi bat voice.
6. Giai toan da duoc test tu dong, nhung chu/de an hinh, panning, nhac, chat luong thuye minh can kiem tra MP4 that.

**Tinh trang ban giao:** source Python/Typst, pytest/unittest, kịch bản, storyboard va YAML da san sang. MP4 Manim that chua render trong moi truong soan ma; **khong** khang dinh hinh anh va giong doc da nghiem thu.
