# COMB05 V2 — Hướng dẫn render video Hoán vị (Manim–Typst)

## Mục tiêu sản xuất

- Mã scene: `episodes/comb05_permutations.py`, tên Scene: `COMB05`.
- 8 chương × 6 nhịp = 48 nhịp; nội dung giảng: `comb05_beats.json`.
- Bài giảng có lời: 2.803 từ tiếng Việt; sinh một clip TTS riêng cho mỗi nhịp.
- Thời lượng nền khi chưa dùng TTS: 893,3 giây + 5,2 giây kết = **898,5 giây (14 phút 58,5 giây)**. Có TTS, thời lượng sẽ tính theo thời gian thật của clip để không cắt lời.
- Mẫu màu sắc và bố cục thống nhất với COMB01–COMB04 V2.

## Làm ngay trên GitHub (không cần Codespaces, không cần Codex Cloud)

1. Giải nén toàn bộ ZIP vào thư mục repository đang dùng, để `.github/workflows/` nằm ngay tại gốc repository (cẩn thận thư mục ẩn `.github`). Giữ các tập trước; chúng đều nằm trong ZIP.
2. `git add . && git commit -m "Add COMB05 V2 full lecture" && git push` (hoặc dùng GitHub Desktop).
3. Truy cập **Actions → Render COMB05 V2 - Bai giang day du Manim Typst → Run workflow**.
4. Lần đầu chọn `quality=preview`. Nếu TTS có kết nối mạng, chọn `voice=on`; nếu chỉ kiểm tra hình và công thức, chọn `voice=off`.
5. Tải Artifact `COMB05-V2-preview-voice-...`. Trong đó có `COMB05.mp4`, phụ đề `.srt`, bảng kiểm tra 8 chương và JSON báo cáo. Nếu chất lượng đạt, chạy lại `quality=fullhd`.

### Nếu render thất bại

- Lỗi Typst: gửi log của bước **Compile Typst**; không bỏ qua vì công thức đang do Typst biên dịch.
- Lỗi TTS (mạng tới dịch vụ giọng đọc): dùng `voice=off` để kiểm tra hình, không tự ý gọi đây là bài giảng có thuyết minh.
- Lỗi Manim: gửi các dòng lỗi từ bước **Render Manim preview**.
- Lỗi QA: gửi báo cáo và video. QA sẽ kiểm tra thời lượng, độ phân giải và có luồng âm thanh khi bật voice. Chỉ vượt qua QA không đồng nghĩa bố cục và chất lượng sư phạm đã được duyệt bằng mắt.
- GitHub Actions tạo MP4 trong Artifacts, không tự xuất bản lên YouTube.

## Chạy thủ công (Linux có Manim, Typst, ffmpeg)

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/prepare_comb05_v2.py --voice off
manim -ql -r 854,480 --fps 24 episodes/comb05_permutations.py COMB05
# Lựa chọn có lời thuyết minh (cần mạng):
python scripts/prepare_comb05_v2.py --voice on
manim -qh -r 1920,1080 --fps 30 episodes/comb05_permutations.py COMB05
```

## Chú ý toán học

- Hoán vị `P_n=n!` chỉ dùng khi `n` phần tử **phân biệt**, tất cả được xếp, thứ tự có ý nghĩa.
- Năm học sinh A, B đứng cạnh: `2 × 4! = 48` (phải nhân 2 vì AB và BA khác nhau).
- Năm học sinh A, B không đứng cạnh: `5! - 2×4! = 72`.
- Kiểm tra độc lập bằng khoảng trống: `3! × C^(4)_(2) × 2! = 72` theo quy ước chỉ số thầy yêu cầu (4 viết trên, 2 viết dưới).
- Trong năm người, A đứng trước B: `5!/2 = 60` (không bắt buộc sát nhau).
- Sáu người, A và B hai đầu: `2! × 4! = 48`.
- Sáu người, A và B không kề: `6! - 2 × 5! = 480`.
