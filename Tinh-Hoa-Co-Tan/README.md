# TINH HOA CỜ TÀN — Nguyễn Văn Sang

**Series video cờ tướng không giới hạn tập**: Manim Community + Typst + giọng đọc tiếng Việt + GitHub Actions. Bộ dựng có bàn cờ 9×10, luật FEN/nước đi, chân Mã, hiệu ứng di chuyển, title card, footer MoMo, và mỗi tập có âm thanh độc lập.

**Footer mặc định mọi tập**: `Nguyễn Văn Sang · Mời tôi ly cà phê — MoMo: 0389.821.115`.

## Bắt đầu trên GitHub (không phải chạy trên Mac)

1. Tạo một GitHub repository. Giải nén ZIP, **chép cả thư mục `.github`** vào thư mục gốc repository, sau đó commit/push.
2. Vào **Actions** → chọn `Tinh Hoa Co Tan - Manim Typst` → **Run workflow**.
3. Chọn `episodes=latest`, `quality=preview`, `voice=edge` để kiểm tra render 480p.
4. Nếu ổn, chọn `quality=full` để xuất 1920×1080/30 fps.
5. Tải MP4 trong **Actions → lần chạy → Artifacts → cotan-tap-0001**.

**Để nghe đúng giọng nam miền Nam**, lấy API key từ Zalo AI TTS và lưu vào GitHub: **Settings → Secrets and variables → Actions → New repository secret**; Name `ZALO_API_KEY`; Value = key thật. Sau đó chạy workflow với `voice=zalo` (speaker `3`: nam miền Nam). Giọng mặc định `edge` dùng `vi-VN-NamMinhNeural` để thử miễn phí, nhưng **không được đảm bảo là giọng Nam**. API Zalo AI có thể có hạn mức hoặc phí riêng; kiểm tra tài khoản Zalo AI.

## Thêm tập mới mà không sửa code Manim

Tạo `episodes/tap-0002.json` bằng lệnh mẫu (có thể chạy trên Codespaces/cloud):

```bash
python scripts/new_episode.py --number 2 --title 'Mã vây Tướng' --fen '4k4/3a5/9/9/6N2/9/9/9/9/3K5 w'
```

Sau đó sửa các `beats` trong JSON: `label`, `headline`, `narration`, `insight`, `moves` (ví dụ `g4e3`), `spotlight` (ví dụ `d1`), `horse_leg` (ví dụ `["g4","e3"]`), `pause` (giây). Những nước đi được kiểm tra tính hợp lệ trước khi dựng. Định dạng tọa độ: **a0 là góc trên bên Đen, i9 là góc dưới bên Đỏ**. Chữ quân: **K Tướng, A Sĩ, B/E Tượng, N/H Mã, R Xe, C Pháo, P Binh**; chữ hoa là Đỏ, chữ thường là Đen. FEN hướng chuẩn từ phía Đen trên cùng.

Một tập 5–10 phút cần khoảng 800–1.400 từ lời bình tiếng Việt (tùy tốc độ TTS). Âm thanh được đo thời lượng và video tự giữ cảnh cho đến khi lời bình kết thúc. Các tập mới không có giới hạn số lượng: `tap-0001.json`, `tap-0002.json` ...

### Chạy nhiều runner song song

Trong `Run workflow` → `episodes` có thể nhập:

- `latest` (tập có số lớn nhất)
- `tap-0001,tap-0002` (các tập cụ thể)
- `range:0001-0016` (một lô 16 tập)
- `all` (tất cả nếu không quá 128 tập trong *một lần chạy*)

`max-parallel: 4` cho tối đa 4 job mỗi job một video; thay thành `8` nếu gói/quyền runner của repo phù hợp. Catalog series không bị giới hạn bởi con số này, nhưng **matrix một lần chạy phải phân lô**. Khi push code workflow tự xuất `latest` ở chế độ preview để tránh bất ngờ tốn nhiều máy.

## RẤT QUAN TRỌNG: đúng luật ≠ giải cờ tối ưu

Tập `tap-0001` là **video nhập môn minh họa cơ chế Mã đấu Sĩ**, không có biến thắng cưỡng bức đã được xác minh. Các nước Mã/Sĩ được **kiểm tra hợp lệ bằng bộ luật nội bộ**. Không nên gọi các nước này là "lời giải bắt buộc".

Trước khi phát hành video chiến thuật hoặc khẳng định "Đỏ thắng cưỡng bức", cần đối chiếu với sách cờ tàn và dùng **Pikafish** kiểm tra nhiều nhánh. Script tùy chọn:

```bash
python scripts/check_pikafish.py --episode tap-0001 --engine /duong-dan/pikafish --depth 24
```

Tạo `output/tap-0001/engine_report.json` chứa nước engine đề nghị cho **thế ban đầu**, **không phải chứng minh toàn bộ thế thắng**. Không tự đổi `analysis_status` sang `engine_verified` trừ khi đã đối chiếu tất cả nhánh cần thiết. Ngoài chuyện từng nước hợp lệ, những quy tắc cờ tàn như lặp nước và hòa phải được kiểm tra bằng công cụ mạnh và người biên tập. `src/core.py` chỉ là **bộ kiểm tra cơ bản**; không phải trọng tài đầy đủ cho mọi tình huống cờ tướng tranh chấp/luật giải đấu.

## Cấu trúc

```text
.github/workflows/render-series.yml  # GitHub Actions matrix
src/core.py                         # FEN, bàn cờ và nước đi
src/scene.py                        # thư viện Manim dùng mọi tập
src/voice.py                        # Zalo miền Nam / Edge / mock
src/typst_cards.py                  # Typst -> PNG tiêu đề + outro
scripts/plan.py                     # chọn tập/lô
scripts/produce.py                  # kiểm tra -> giọng -> Typst -> MP4
scripts/new_episode.py              # tạo tập mới
scripts/check_pikafish.py           # phân tích engine tùy chọn
scripts/make_demo.py                # sinh storyboard tập 01
episodes/tap-0001.json              # pilot 10 phân cảnh, ~1134 từ
```

## Kiểm tra không cần Manim

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
python scripts/produce.py --episode tap-0001 --skip-render
python scripts/plan.py latest
```

## Chạy thử có âm thanh giả / tại máy riêng (tùy chọn)

Trên hệ thống có `ffmpeg`, `typst`, Python 3.11, thư viện Linux Cairo/Pango và phông Noto:

```bash
pip install -r requirements.txt
python scripts/produce.py --episode tap-0001 --quality preview --voice mock
```

`voice=mock` là track im lặng chỉ dùng smoke test, **không phải bản xuất bản**. MP4 xuất trong `output/tap-0001/`.

## Chi phí và xuất bản

Runner chuẩn GitHub có thể miễn phí theo điều kiện của repo public; repo private tính vào quota phút sử dụng và mức giá của gói. TTS Zalo và API bên thứ ba có điều khoản riêng. Giới hạn thời gian mỗi job và dung lượng artifact vẫn áp dụng; "không giới hạn tập" nghĩa là mã nguồn có thể thêm tập tiếp, không có nghĩa miễn phí vô hạn.

Không đưa API key vào JSON hoặc code; chỉ dùng `ZALO_API_KEY` trong GitHub Secrets. Kiểm tra quyền sử dụng giọng đọc và âm thanh trước khi đăng YouTube. Footer có thông tin MoMo công khai theo yêu cầu của chủ series.
