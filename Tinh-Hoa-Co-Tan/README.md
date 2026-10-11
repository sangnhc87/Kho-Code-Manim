# TINH HOA CỜ TÀN — Shorts sát cục & thực chiến danh thủ

**Hướng hiện tại (từ 11/10/2026): chỉ đăng YouTube Shorts**, nội dung ưu tiên:

1. **Sát cục** (`curriculum/mates/*.json`): đòn thí quân, chiếu liên hoàn từ các bộ sưu tập kinh điển
   (弃车绝杀 bỏ Xe tuyệt sát, 连将带杀 liên tướng đới sát, 妙局杀法, 68 sát pháp, 杀局宝典).
   Mỗi lời giải được **tự chứng minh** bằng tìm kiếm vét cạn (`xq/mate.py`): bên tấn công chiếu liên tục,
   xét **mọi** cách chống đỡ; trước khi dựng tập còn chứng minh lại lần nữa.
2. **"Vì sao xin thua?"**: thế cuối của ván đấu thật (kỳ phổ đại sư), chứng minh bên thắng có sát cục bắt buộc
   (`scripts/import_game_mates.py`).
3. **Thực chiến danh thủ**: tàn cuộc ván thật được bảng tra chessdb chấm từng nước (sai lầm, nước duy nhất).

Dựng: `python scripts/build_episodes.py --count 4` (giáo trình đặt nguồn trong `curriculum/topics.json`:
`mates`, `games`, `game_every`). Nhập nguồn mới:

```bash
python scripts/import_mates.py end-games/弃车绝杀
python scripts/import_games.py selected-games/Dai-Su-Ky-Lo-Lu-Kham
python scripts/import_game_mates.py Dai-Su-Ky-Lo-Lu-Kham
```

Nguồn kỳ phổ: kho cộng đồng [vietcotuong.com](https://github.com/chasoft/community-xiangqi-games-database)
(chỉ lấy dữ kiện nước đi; không sao chép lời bình). Lịch tự động: 2 lượt/ngày, mỗi lượt 2 Shorts
(biến repo `COTAN_DAILY=true`).

---

## Phần nền: tàn cục với bảng tra chessdb.cn

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

Hai dạng tập:
- **Thế thắng** (`result` mặc định `W`): Đỏ đi trước, tìm đường thắng nhanh nhất.
- **Thủ hòa** (`"result": "D"` trong chủ đề): Đen đi trước, chỉ 1–2 nước giữ hòa, mọi nước khác thua.

Mỗi tập kèm một **YouTube Short** câu đố khung dọc (dưới 60 giây): đề bài, đếm ngược, đáp án,
kết luận bảng tra (`scripts/make_short.py`, `src/short_scene.py`).

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
| `targets` | `both` (video + Short), `video`, `short` |
| `voice` | `edge` (vi-VN-NamMinhNeural) hoặc `zalo` (cần secret `ZALO_API_KEY`) |

Chạy tự động mỗi ngày (2 tập mới, 1080p, đăng YouTube): đặt biến repo
**Settings → Secrets and variables → Actions → Variables → `COTAN_DAILY` = `true`**.
Hạn mức YouTube API mặc định cho phép khoảng 6 lượt tải lên/ngày (mỗi tập = 2 lượt: video + Short).
Tập đăng lỗi (ví dụ hết hạn mức) có thể đăng bù bằng `episodes=unpublished`.

Quy tắc vận hành: các lượt render có thể chạy song song, nhưng **không chạy hai lượt có
`build_count > 0` cùng lúc** (sẽ trùng số tập). Lịch sử đăng ghi theo khoá `cotan3_ep-XXXX`
và `cotan3_short_ep-XXXX` trong `youtube_uploaded_history.json`.

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
