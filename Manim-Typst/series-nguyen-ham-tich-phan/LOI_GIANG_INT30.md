# INT30 – Tích phân trong thiết kế: Cổng parabol, logo, mảnh vườn và chi phí

> Sinh tự động từ `int30/lesson.py` – sửa lời giảng ở đó rồi chạy lại `python scripts/build_docs.py --ep int30`.

**Số nhịp:** 24 · **Số công thức Typst:** 33 · **Từ:** 1181

## Mở đầu

### ⏱ Mở đầu: sơn một cổng parabol

**`h1`** — Một cổng chào có dạng parabol, chân cổng rộng tám mét, đỉnh cao sáu mét. Người ta sơn toàn bộ mặt cổng với giá một trăm năm mươi nghìn đồng một mét vuông. Chi phí là bao nhiêu? Đáp số: bốn triệu tám trăm nghìn đồng, và chỉ cần một tích phân.

**`h2`** — Đây là tập ba mươi của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân trong thiết kế.

**`h3`** — Sau video này, em sẽ nắm được ba điều. Một, cách đặt hệ trục lên một vật thật để có hàm số đơn giản. Hai, công thức nhanh hai phần ba cho diện tích parabol. Ba, quy trình mô hình hóa trọn vẹn: từ hình vẽ đến chi phí.

## Bản chất

### ⏱ Đặt hệ trục lên vật thật

**`c1`** — Bước quan trọng nhất là đặt hệ trục. Với cổng parabol, hãy đặt gốc tọa độ ở chính giữa chân cổng, trục tung đi qua đỉnh. Khi đó parabol đối xứng qua trục tung và có dạng y bằng h trừ a x bình phương.

**`c2`** — Tìm hệ số a từ dữ kiện: chân cổng tại x bằng cộng trừ một nửa chiều rộng, ở đó y bằng không. Với cổng rộng tám, cao sáu: sáu trừ mười sáu a bằng không, nên a bằng ba phần tám. Phương trình là y bằng sáu trừ ba phần tám x bình phương.

### ⏱ Công thức hai phần ba

**`c3`** — Diện tích bằng tích phân từ trừ bốn đến bốn của sáu trừ ba phần tám x bình phương, bằng ba mươi hai. Để ý: ba mươi hai bằng hai phần ba nhân tám nhân sáu. Đây là kết quả của Archimedes: miền parabol bằng hai phần ba hình chữ nhật bao quanh nó.

**`c3b`** — Chứng minh tổng quát: cổng rộng w, cao h có phương trình y bằng h trừ bốn h chia w bình phương nhân x bình phương. Lấy tích phân từ trừ w phần hai đến w phần hai, ta được đúng hai phần ba w h. Vì vậy quy tắc hai phần ba đúng với mọi cổng parabol, không chỉ cho số liệu cụ thể.

### ⏱ Quy trình năm bước

**`c4`** — Quy trình mô hình hóa năm bước. Một, đặt hệ trục. Hai, viết phương trình các đường biên. Ba, tìm cận. Bốn, tính tích phân để có diện tích. Năm, nhân với đơn giá và đổi đơn vị theo yêu cầu.

**`c5`** — Ba lỗi thường gặp khi làm bài thiết kế. Một, quên rằng chiều rộng là cả hai phía, cận là trừ bốn đến bốn chứ không phải không đến tám khi gốc ở giữa. Hai, nhầm đơn vị đề xi mét và mét. Ba, làm tròn quá sớm làm sai đáp số cuối.

## Ví dụ

### ⏱ Ví dụ 1: chi phí sơn cổng

**`e1`** — Ví dụ một, hoàn thành bài mở đầu. Diện tích mặt cổng ba mươi hai mét vuông, nhân với một trăm năm mươi nghìn đồng, được bốn triệu tám trăm nghìn đồng.

### ⏱ Ví dụ 2: trừ phần cửa

**`e2`** — Ví dụ hai: cổng có một cửa hình chữ nhật rộng bốn mét, cao bốn mét ở giữa, phần cửa không sơn. Diện tích cần sơn là ba mươi hai trừ mười sáu, bằng mười sáu mét vuông. Phải kiểm tra cửa nằm gọn trong cổng: tại x bằng hai, cổng cao bốn phẩy năm, lớn hơn bốn.

### ⏱ Ví dụ 3: vườn hình elip

**`e3`** — Ví dụ ba, mảnh vườn hình elip với trục lớn tám mét, trục nhỏ sáu mét. Phương trình x bình phương chia mười sáu cộng y bình phương chia chín bằng một. Diện tích bằng bốn lần tích phân của nửa trên trong góc phần tư thứ nhất, bằng pi nhân bốn nhân ba, bằng mười hai pi, khoảng ba mươi bảy phẩy bảy mét vuông.

**`e3b`** — Tiếp ví dụ ba: mảnh đất hình chữ nhật tám nhân sáu mét bao quanh vườn elip, phần còn lại trồng cỏ. Diện tích trồng cỏ bằng bốn mươi tám trừ mười hai pi, khoảng mười phẩy ba mét vuông. Đây là kiểu câu hỏi hình ghép rất hay gặp trong đề.

### ⏱ Ví dụ 4: logo hai parabol

**`e4`** — Ví dụ bốn, logo: miền giữa hai parabol y bằng x bình phương và y bằng hai trừ x bình phương, đơn vị đề xi mét. Hai đường cắt nhau tại trừ một và một. Diện tích bằng tích phân của hai trừ hai x bình phương, bằng tám phần ba đề xi mét vuông, tức là tám phần ba nhân một phần trăm mét vuông.

**`e5`** — Mẹo kiểm tra nhanh mọi bài cổng parabol: diện tích bằng hai phần ba nhân rộng nhân cao. Với elip, diện tích là pi a b. Biết hai công thức này, em có thể kiểm tra đáp án trắc nghiệm trong vài giây.

### ⏱ Đặt hệ trục khác

**`e6`** — Nếu đặt gốc tọa độ ở chân trái của cổng thì sao? Khi đó parabol có dạng y bằng ba phần tám nhân x nhân tám trừ x, và cận từ không đến tám. Tích phân vẫn ra ba mươi hai. Kết quả không phụ thuộc cách đặt hệ trục, nhưng đặt gốc ở giữa thì phương trình gọn và tính nhanh hơn.

## Đề thi mới

### ⏱ Câu hỏi Đúng/Sai

**`x1`** — Câu hỏi dạng đúng sai. Một cổng parabol rộng sáu mét, cao bốn phẩy năm mét. Đặt gốc tọa độ ở giữa chân cổng. Sơn mặt cổng với giá hai trăm nghìn đồng một mét vuông. Em hãy tạm dừng video và đánh giá bốn mệnh đề.

**`x2`** — Ý a đúng: bốn phẩy năm trừ a nhân chín bằng không cho a bằng một phần hai. Ý b đúng: diện tích bằng hai phần ba nhân sáu nhân bốn phẩy năm, bằng mười tám mét vuông.

**`x3`** — Ý c sai: hai mươi bảy là diện tích cả hình chữ nhật bao quanh, không phải của cổng. Ý d sai: chi phí bằng mười tám nhân hai trăm nghìn, bằng ba triệu sáu trăm nghìn đồng.

### ⏱ Câu trả lời ngắn

**`x4`** — Câu trả lời ngắn: một vườn hoa hình elip có trục lớn mười mét, trục nhỏ sáu mét. Chi phí trồng hoa là năm mươi nghìn đồng một mét vuông. Tính tổng chi phí theo đơn vị triệu đồng, làm tròn đến hàng phần trăm.

**`x5`** — Bán trục a bằng năm, b bằng ba. Diện tích bằng pi nhân năm nhân ba, bằng mười lăm pi, khoảng bốn mươi bảy phẩy mười hai mét vuông. Chi phí bằng mười lăm pi nhân không phẩy không năm triệu, khoảng hai phẩy ba sáu triệu đồng. Ghi vào phiếu: hai, phẩy, ba, sáu.

## Tổng kết

### ⏱ Tổng kết và bài tập tự luyện

**`o1`** — Tóm tắt ba ý. Một, đặt hệ trục khéo léo: gốc ở giữa, trục tung đi qua đỉnh. Hai, cổng parabol có diện tích hai phần ba rộng nhân cao, elip có diện tích pi a b. Ba, mô hình hóa năm bước, nhân đơn giá ở cuối và cẩn thận với đơn vị.

**`o2`** — Bài tập tự luyện. Một, diện tích cổng parabol rộng bốn mét, cao ba mét. Hai, logo giữa y bằng x bình phương và y bằng tám trừ x bình phương. Ba, diện tích elip có a bằng bốn, b bằng hai. Đáp số hiện ở cuối màn hình.

**`o3`** — Ở tập ba mươi mốt, ta chuyển sang bồn chứa và bể nước: lưu lượng thay đổi theo thời gian, và tích phân cho biết lượng nước đã chảy vào. Cảm ơn các em đã theo dõi. Hẹn gặp lại!

## Bài tập tự luyện

1. Cổng parabol rộng 4 m, cao 3 m: diện tích → **8 m²**
2. Logo giữa y = x² và y = 8 − x² → **64/3**
3. Elip a = 4, b = 2: diện tích → **8π**
