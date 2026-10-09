# TINH HOA CỜ TÀN — TUYỂN TẬP 1.000 THẾ CỜ TÀN KINH ĐIỂN

**Bản 2.0: Hệ thống sản xuất tự động.** Manim + Typst + Edge/Zalo TTS + GitHub Actions, series có thể thêm vô hạn tập bằng file JSON.

### Bản sửa 0001 ngày 09/10/2026

- Hiển thị đủ cột `a..i` và hàng `0..9`: `a0` ở góc trên trái, phía Đen. Các nhãn nằm ngoài lưới, quân ở mép không che nhãn.
- Lời mở đầu giải thích tọa độ, mục tiêu **ép bắt Sĩ**, cách đếm lượt và giới hạn luật lặp nước.
- Pikafish bản nguồn tag `Pikafish-2026-09-06`, commit `4c17cee11f888ae1d48a9494f2e2239f019f0a1f`, đã xác nhận **63/63 nước hợp lệ**. Engine chọn `d7f8` UCI, tương ứng `d2f1` trên màn hình, ở độ sâu 22.
- `verification/tap-0001-pikafish.json` lưu FEN từng nước, nước hợp lệ engine trả về, log UCI và SHA-256 của tập, engine, NNUE. Test chặn báo cáo lỗi thời nếu JSON tập bị sửa.
- Test Manim đi qua mọi biến, bắt quân, đặt lại thế: kiểm tra quân không thừa/thiếu, đúng tọa độ và bàn cờ luôn còn trong scene. File `output/tap-0001/timeline.json` ghi mốc thời gian để đối chiếu video render.

Pikafish là **engine**, không phải kho tablebase cờ tàn chính xác. Kết quả 13/21 trong tập vẫn đến từ solver giải ngược mục tiêu bắt Sĩ; báo cáo Pikafish không biến các số này thành số lượt chiếu bí.

```bash
python scripts/check_pikafish.py --episode tap-0001 \
  --engine /path/to/pikafish --eval-file /path/to/matching/pikafish.nnue \
  --depth 22 --report verification/tap-0001-pikafish.json
```

Nguồn engine: [Pikafish release](https://github.com/official-pikafish/Pikafish/releases/tag/Pikafish-2026-09-06). Dùng NNUE đi cùng release, tránh tải `master-net` mới rồi ghép với engine cũ.

## Sửa đúng lỗi bàn cờ bị mất

- **Bàn cờ tiêu chuẩn 9 cột × 10 hàng, hiển thị trọn vẹn**, không phóng lớn và không bị cắt ở phần trên.
- `src/layout.py` khóa tọa độ bàn cờ, ranh giới tiêu đề, footer, panel bên phải. Test sẽ báo lỗi nếu phần trên/dưới hoặc cạnh phải bị tràn.
- Các biến cờ có FEN bắt đầu riêng; khi chuyển biến, **bàn cờ không biến mất**, chỉ thay quân cờ, không nhảy nối biến khác.
- Panel chỉ ghi nước đang phân tích và kết quả, không trình chiếu đoạn văn dài.
- Footer trong suốt series: `☕ Ủng hộ kênh ly cà phê — VPBank: 10389821115 (Quét VietQR cuối video)`.

## Tập 001 — Mã đấu đơn Sĩ

FEN: `3k1a3/9/3N5/9/9/9/9/4K4/9/9 w`. Đỏ đi trước.

Nội dung cờ cụ thể theo phương pháp giải ngược trạng thái bốn quân:

| Phương án | Kết quả mô hình | Diễn giải |
|---|---|---|
| Mã d2–f1 hoặc d2–c4 | 13 **lượt đi của cả hai bên** tối đa | Giữ thế cưỡng bức bắt Sĩ nhanh nhất |
| Sau Mã d2–f1, Đen Sĩ e1–f0 | Tổng cộng 7 lượt | Sĩ lui sai: mất nhanh |
| Sau Mã d2–f1, Đen Sĩ e1–d2 | Tổng cộng 9 lượt | Sĩ rẽ sai: mất nhanh |
| Đen d0–d1 sau khi Đỏ d2–f1 | Tổng cộng 9 lượt | Tướng đi kém, mất Sĩ sớm |
| Mã d2–e0 | 21 lượt | Vẫn ép bắt Sĩ nhưng chậm hơn |
| Tướng e7–d7 | Không còn ép được bắt Sĩ | Đỏ bỏ lỡ cơ hội thắng trong mô hình |

**Giới hạn kiểm chứng cần hiểu rõ:** Đây là phép giải WDL/độ dài cho cấu hình **hai Tướng + một Mã Đỏ + một Sĩ Đen**, mục tiêu *bắt được Sĩ*, với luật nước đi, chiếu và bí/hết nước thông thường. Chưa mã hóa đủ quy định xử lý **trường chiếu, trường tróc, cấm lặp nước** của các luật thi đấu cờ tướng. Vì vậy **13/21 không phải số nước chiếu bí hoặc bằng chứng kết thúc ván cờ theo mọi bộ luật giải đấu**. Trước khi quảng bá là “thế tất thắng” theo luật giải đấu, nên kiểm chứng tiếp bằng Pikafish và tài liệu cờ tàn. Không được thay số liệu mô hình bằng số liệu “mate in N” giả định.

Công cụ tính lại biến: `PYTHONPATH=. python scripts/build_episode_001.py` (tự tính retrograde rồi ghi `episodes/tap-0001.json`). Tập có **18 phân đoạn**, âm thanh theo từng đoạn, 63 lượt di chuyển trên màn hình cộng các ảnh cờ tĩnh.

## Cập nhật repository GitHub

1. Commit/push mã nguồn trong `Tinh-Hoa-Co-Tan` vào repository này.
2. Vào **Actions → Tinh Hoa Co Tan - Manim Typst → Run workflow**.
3. Chọn `episodes=tap-0001`, `quality=preview`, `voice=edge`.
4. Tải MP4 ở **Artifacts**; nhìn cả quân Đen ở hàng trên và quân Đỏ ở hàng dưới, rồi mới chạy `quality=full`.
5. Chạy thủ công `quality=full` sẽ **tự đăng công khai** bằng YouTube Secrets đã cấu hình. Mỗi lần chạy full thành công tạo một video mới; video cũ không tự đổi hoặc bị xóa. Tránh bấm full nhiều lần cho cùng bản sửa.

Giọng `edge`: nam tiếng Việt `vi-VN-NamMinhNeural`, **không cam kết đúng giọng miền Nam**. Giọng `zalo`: speaker 3 (nam miền Nam); phải đặt `ZALO_API_KEY` trong **Settings → Secrets and variables → Actions**. Dịch vụ Zalo có thể có phí/hạn mức riêng.

## Kiểm tra trước khi dựng

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
PYTHONPATH=. python scripts/produce.py --episode tap-0001 --skip-render
```

GitHub Actions tự thực hiện kiểm tra hợp lệ rồi mới render. Giới hạn workflow là 128 tập/lần chạy, tối đa 4 runner song song (có thể điều chỉnh theo quyền runner); toàn bộ catalog không giới hạn số tập.

## Cấu trúc chính

```text
../.github/workflows/render-xiangqi.yml # GitHub Actions
src/core.py                          # FEN, luật di chuyển cơ bản, branch validation
src/layout.py                        # tọa độ và kiểm tra vùng an toàn 16:9
src/scene.py                         # Manim: bàn cờ, 4 quân, hiệu ứng, chuyển biến
src/voice.py                         # Giọng Nam tiếng Việt / nam miền Nam, đồng bộ audio
src/typst_cards.py                   # Title/outro bằng Typst
episodes/tap-0001.json               # 18 phân đoạn tập 001
scripts/solve_masi.py                # Giải ngược các trạng thái 4 quân
scripts/build_episode_001.py         # Tính biến và tạo data 001
scripts/check_pikafish.py            # Kiểm tra engine độc lập (tùy chọn)
scripts/produce.py                   # Xuất MP4
scripts/plan.py                      # Chọn lô tập để dựng
tests/test_core.py                   # logic, luật, bố cục, độ mới của bằng chứng engine
tests/test_display.py                # tọa độ engine, quân hiển thị sau mọi biến
```

## Render và lưu ý

- `preview` = 854×480, 15 fps; `full` = 1920×1080, 30 fps.
- Dùng `voice=edge` để test không cần Zalo API key; giọng miền Nam thực sự là `voice=zalo`.
- Không lưu API key trong repository hoặc JSON.
- Cần xem MP4 preview thật trên GitHub trước khi chạy full để công bố.
- GitHub Actions, Zalo AI và lưu trữ artifact đều chịu hạn mức/quy định của dịch vụ tương ứng.
