# TINH HOA CỜ TÀN — bản 3 (dữ liệu bảng tra chessdb.cn)

Series video cờ tàn cờ tướng, Manim + Typst, dựng và đăng hoàn toàn trên GitHub Actions.
**Không chạy engine trên máy cá nhân**: mọi kết luận Thắng/Hòa, số nước đến chiếu bí,
nước duy nhất, nước sai… đều tra từ bảng tra cờ tàn (EGTB, độ đo DTM) của
[chessdb.cn](https://www.chessdb.cn/query/) qua API công khai.

## Vì sao làm lại

Bản cũ dùng solver tự viết với mục tiêu "bắt quân" và Pikafish chỉ để kiểm tra nước hợp lệ,
nên nhiều kết luận chưa chứng minh (ví dụ tập 0001 cũ nói "13 lượt bắt Sĩ"; bảng tra cho thấy
thế đó Đỏ **chiếu bí sau 12 nước**, kết thúc bằng thế Đen hết nước đi). Bản 3 thay bằng dữ liệu chân xác.

## Một tập gồm những gì

1. **Thế cờ** và **kiến thức nền** của chủ đề — số liệu trong lý thuyết lấy từ khảo sát bảng tra
   (`scripts/topic_stats.py`, ví dụ: Pháo đơn vs Tướng đơn hòa 50/50 thế, Pháo + Sĩ thắng 50/50).
2. **Thử thách**: đếm ngược để người xem tự tìm nước.
3. **Bảng tra**: so sánh các nước đầu (Thắng sau N nước / Hòa / Thua).
4. **Biến chính** tối ưu hai bên, lời bình khớp từng nước: nước duy nhất, nước chờ
   (phát hiện bằng cách lật lượt đi rồi tra lại), bị ép nước, Tướng chiếm lộ khống chế mặt Tướng…
5. **Bẫy cần tránh**: nước sai hấp dẫn nhất (chiếu, ăn quân, đẩy Binh xuống đáy…) và cách đối phương trừng phạt.
6. **Giải phẫu thế bí**: ô thoát nào bị quân nào khống chế.
7. **Tổng kết**.

## Cấu trúc

```text
xq/board.py          luật cờ đầy đủ (toạ độ chuẩn chessdb/UCI: a0 góc dưới trái, Đỏ ở dưới)
xq/notation.py       ký pháp Việt: "Mã 2 tiến 3", "Xe trước bình 4", Binh (Đỏ) / Tốt (Đen)
xq/cdb.py            client chessdb.cn + cache data/cdb/*.json (commit vào repo)
xq/analyze.py        biến chính, nước duy nhất, nước chờ, ép nước, bẫy, giải phẫu thế bí
xq/commentary.py     sinh kịch bản/lời bình tiếng Việt từ dữ kiện phân tích
xq/sample.py         sinh thế ngẫu nhiên hợp lệ theo vật chất, khoá chống trùng (đối xứng gương)
xq/validate.py       kiểm tra kịch bản trước khi render
curriculum/topics.json  giáo trình: chủ đề, lý thuyết, số tập mỗi chủ đề
catalog.json         danh mục tập đã dựng
episodes/ep-XXXX.json   kịch bản từng tập (kèm phân tích đầy đủ và metadata YouTube)
scripts/build_episodes.py  dựng tập mới (tự tìm thế có giá trị dạy học)
scripts/produce.py   giọng đọc + Typst + Manim → MP4
src/scene.py         cảnh Manim
```

## Chạy trên GitHub Actions

**Actions → Tinh Hoa Co Tan - Manim Typst → Run workflow**

| Mục | Ý nghĩa |
|---|---|
| `build_count` | Số tập mới dựng theo giáo trình (tra chessdb ngay trên runner, tự commit) |
| `episodes` | `new` (vừa dựng), `latest`, `unpublished`, `ep-0001,ep-0002`, `range:1-5` |
| `quality` | `preview` 480p chỉ để xem (artifact); `full` 1080p **và đăng YouTube công khai** |
| `voice` | `edge` (vi-VN-NamMinhNeural) hoặc `zalo` (cần secret `ZALO_API_KEY`) |

Chạy tự động mỗi ngày (2 tập mới, 1080p, đăng YouTube): đặt biến repo
**Settings → Secrets and variables → Actions → Variables → `COTAN_DAILY` = `true`**.
Hạn mức YouTube API mặc định cho phép khoảng 6 lượt tải lên/ngày.

## Mở rộng tới 1000 tập

Thêm chủ đề vào `curriculum/topics.json` (vật chất, ràng buộc ô đặt quân, khoảng DTM, số tập,
lý thuyết). Trước khi viết lý thuyết, khảo sát số liệu:

```bash
python scripts/topic_stats.py RP:RA R:NA --n 60
```

Chỉ viết những nhận định mà bảng tra xác nhận. Bảng tra chessdb bao phủ phần lớn thế tàn tới
khoảng 10 quân (ví dụ Xe Mã vs Xe Sĩ Tượng); thế ngoài bảng tra bị từ chối.

## Kiểm tra local (không cần mạng)

```bash
CDB_OFFLINE=1 python -m unittest discover -s tests -v
```

Test đối chiếu bộ sinh nước với **mọi thế đã lưu trong cache chessdb**, kiểm tra ký pháp,
và kiểm tra từng kịch bản khớp bảng tra.
