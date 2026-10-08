# COMB08 V2 - HUONG DAN RENDER GITHUB ACTIONS

## 1. Tinh trang ban giao

- Scene Manim: `COMB08`
- Source: `episodes/comb08_synthesis.py`
- Loi giang: `comb08_beats.json` va `narration_COMB08_v2.md`
- Cong thuc Typst: `comb08_lesson_data.py` va `assets/comb08v2/*.typ`
- Thoi luong nen (khong giong doc): 1013,2 giay = **16 phut 53 giay**.
- 48 nhip / 8 chuong / 3.522 tu thuyet minh / 203 doan phu de.
- Truoc khi dung tren lop, can kiem tra MP4 thuc te tu Github Actions, chua duoc render trong moi truong dong goi.

## 2. Cach dua len GitHub

1. Tai va giai nen `SangMath_COMB08_V2_GitHubReady.zip`.
2. **Chep toan bo noi dung ben trong thu muc** vao goc repository cu cua thầy, giu nguyen thu muc an `.github`.
3. Commit va push, khong upload nguyen tep ZIP.
4. Mo tab **Actions** va workflow **Render COMB08 V2 - Bai giang Tong hop Hoan vi Chinh hop To hop**.
5. Chon **Run workflow**, `quality = preview`, `voice = off` de xem bo cuc nhanh.
6. Tai MP4 va `qa_comb08_v2/contact_sheet.jpg` trong **Artifacts**.
7. Khi hinh tot, chay lai `voice = on` de nghe TTS tieng Viet; neu on, chon `quality = fullhd`.

## 3. Files quan trong

| File | Nhiem vu |
|---|---|
| `episodes/comb08_synthesis.py` | Manim Scene COMB08 2 cot, 48 nhip |
| `comb08_lesson_data.py` | Cong thuc, phep dem va kiem tra phep dem |
| `comb08_beats.json` | Noi dung giang tung nhip va thoi luong |
| `scripts/prepare_comb08_v2.py` | Typst, TTS, SRT, manifest |
| `scripts/qa_comb08_v2.py` | Kiem tra MP4, am thanh, 8 anh QA |
| `tests/test_comb08_v2.py` | Kiem thu toan hoc va pipeline |
| `.github/workflows/render-comb08-v2.yml` | Workflow |
| `preview/comb08_v2/storyboard_8_chapters.png` | Ban phac thao 8 chuong |

## 4. Chay thu cong tren may co Manim va Typst

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb08_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb08_synthesis.py COMB08

# Sau khi preview dat:
python scripts/prepare_comb08_v2.py --voice on
manim -qh -r 1920,1080 --fps 30 episodes/comb08_synthesis.py COMB08
```

## 5. Quy uoc ky hieu

The user's series follows `A^(n)_(k)`, `C^(n)_(k)` (n o tren, k o duoi). Cac cong thuc duoc render Typst, khong dung ky hieu nCr lam mac dinh.

## 6. Cac diem nghiem thu

1. Kiem tra scene mo dau phai hien yeu cau day du va chua lo dap an.
2. Kiem tra nhom hai nguoi AB va BA trong chuong 03 (hoan doi vai tro).
3. Chon doi 3 nguoi co 1 truong: **168** va 2 cach chung minh.
4. Khong cho A lam truong trong bai phan cong 7 hoc sinh: **180**.
5. Chon nhom 4 nam, 3 nu, it nhat 1 nu: **31**; dung 2 nam 1 nu: **18**.
6. Lap so chan 3 chu so khac nhau tu 0,1,2,3,4: **30**.
7. Bai capstone: hai cach 168-60-21 va 42+45 deu bang **87**.
8. Kiem tra am thanh TTS neu `voice=on`: may GitHub phai co Internet va dich vu Edge TTS hoat dong.
9. Kiem tra thoi luong (khong duoi 900 giay) va khung hinh 854x480/1920x1080.

**Quan trong:** Bo test Python khong thay the duyet hinh va nghe MP4 that. Neu GitHub Actions bao loi, gui log de sua dung theo ket qua chay.
