# SANG MATH · COMB20 V2 · CÁC TỔNG HỆ SỐ NHỊ THỨC

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=off
Tổng thời lượng dự kiến: 1253.2 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01 · TỔNG HỆ SỐ: THAY GIÁ TRỊ

### Nhịp 01 · 00:00 · Hệ số nằm ở đâu?

Hãy quan sát khai triển của một cộng x mũ năm. Mỗi đơn thức có hệ số là một số trong hàng thứ năm của tam giác Pascal. Nếu đề chỉ yêu cầu tổng tất cả hệ số, ta có thể cộng sáu con số trên màn hình. Nhưng cách ấy rất dài khi số mũ là một trăm. Ta cần tìm một thao tác đại số thay thế cho việc cộng từng số.

**Trên màn hình:** Khai triển (1+x)^5. | Mỗi ô ứng với một số tổ hợp. | Đừng tính từng ô khi chưa cần.
**Ghi nhớ:** Đừng tính từng ô khi chưa cần.

### Nhịp 02 · 00:26 · Đặt x bằng một

Khi thay x bằng một, mọi số hạng x mũ k đều bằng một. Nhờ đó giá trị đa thức đúng bằng tổng các hệ số. Vế trái một cộng một mũ năm cho ba mươi hai, và ta không phải khai triển. Hình động sẽ làm các lũy thừa cùng co về một, còn hệ số giữ nguyên. Đây là phép thế cơ bản đầu tiên.

**Trên màn hình:** Mọi lũy thừa x trở thành 1. | Vế trái: 2^5. | Vế phải: tổng các hệ số.
**Ghi nhớ:** Vế phải: tổng các hệ số.

### Nhịp 03 · 00:52 · Tổng tổng quát

Với n bất kỳ không âm, ta viết một cộng x tất cả mũ n và dùng công thức Newton. Sau đó đặt x bằng một, nhận được tổng các hệ số tổ hợp từ k bằng không đến n bằng hai mũ n. Phải đọc đúng ký hiệu: số n nằm ở trên chữ C, còn k nằm ở dưới. Công thức này cũng chính là kết quả đếm tập con ở Video mười chín.

**Trên màn hình:** Viết khai triển Newton. | Thay x=1 vào hai vế. | Áp dụng với mọi n không âm.
**Ghi nhớ:** Áp dụng với mọi n không âm.

### Nhịp 04 · 01:18 · Xét hiệu xen dấu

Nếu thay x bằng âm một, các số hạng bậc chẵn giữ dấu dương, bậc lẻ mang dấu âm. Do một trừ một bằng không, với n nguyên dương thì tổng xen dấu bằng không. Sơ đồ hai nhóm hệ số trên hình sẽ cân bằng nhau. Cần nói rõ điều kiện n lớn hơn không, bởi khi n bằng không, tổng chỉ có một số hạng bằng một.

**Trên màn hình:** Thay x bằng -1. | Các số hạng đổi dấu luân phiên. | Hai nhóm bằng nhau nếu n>0.
**Ghi nhớ:** Hai nhóm bằng nhau nếu n>0.

### Nhịp 05 · 01:44 · Thử với n=4

Ta kiểm tra bằng ví dụ bậc bốn. Hàng tương ứng của Pascal là một, bốn, sáu, bốn, một. Các vị trí chẵn cộng lại được tám, các vị trí lẻ cũng là tám. Vì vậy tổng xen dấu bằng không. Đây là kiểm tra nhỏ nhưng giúp học sinh nhìn thấy công thức hoạt động. Khi số mũ lớn, quy luật vẫn đúng nhờ phép thế âm một.

**Trên màn hình:** Hàng Pascal 1,4,6,4,1. | Nhóm chẵn: 1+6+1=8. | Nhóm lẻ: 4+4=8.
**Ghi nhớ:** Nhóm lẻ: 4+4=8.

### Nhịp 06 · 02:10 · Quy tắc nhận diện

Chốt chương đầu, khi gặp tổng các hệ số của một đa thức, hãy nghĩ ngay đến việc thay x bằng một. Nếu các hệ số xen dấu, thường thay x bằng âm một. Nhưng nếu số hạng bị nhân thêm k, k bình phương hoặc mẫu k cộng một, phép thế đơn thuần chưa đủ. Những chương tiếp theo sẽ đưa vào đạo hàm, rồi cả tích phân để xử lý những trọng số ấy.

**Trên màn hình:** Không thấy k đứng trước hệ số? | Ưu tiên thế x=1 hay x=-1. | Nếu có trọng số k, cần kỹ thuật khác.
**Ghi nhớ:** Nếu có trọng số k, cần kỹ thuật khác.


## 02 · TỔNG HỆ SỐ CHẴN VÀ LẺ

### Nhịp 07 · 02:36 · Chia hai nhóm

Bây giờ ta cần tách tổng chẵn và tổng lẻ, chứ không chỉ tính tổng chung. Đặt E bằng tổng các hệ số có chỉ số k chẵn, và O bằng tổng chỉ số k lẻ. Hai nhóm không chồng nhau và chứa toàn bộ hệ số Newton. Do đó E cộng O bằng hai mũ n. Trên hình, các cột ở vị trí chẵn và lẻ sẽ được tô hai màu.

**Trên màn hình:** E là tổng chỉ số chẵn. | O là tổng chỉ số lẻ. | E+O=2^n.
**Ghi nhớ:** E+O=2^n.

### Nhịp 08 · 03:02 · Lấy hiệu hai nhóm

Thay x bằng âm một, ta thu được E trừ O bằng không với mọi n lớn hơn không. Kết hợp với E cộng O bằng hai mũ n, chúng ta có một hệ hai phương trình đơn giản. Đây là chiến thuật rất mạnh: muốn tách hai nhóm, hãy tính tổng và hiệu. Ta không cần cộng thủ công từng hàng Pascal.

**Trên màn hình:** Thay x=-1 vào Newton. | Nhóm chẵn mang dấu cộng. | Nhóm lẻ mang dấu trừ.
**Ghi nhớ:** Nhóm lẻ mang dấu trừ.

### Nhịp 09 · 03:28 · Kết luận cân bằng

Từ hai phương trình, cộng rồi chia đôi ta có cả E và O đều bằng hai mũ n trừ một. Vì thế tổng hệ số chẵn bằng tổng hệ số lẻ cho mọi n nguyên dương. Nếu n bằng không thì chỉ có hệ số C của không chọn không, nên E bằng một và O bằng không. Điều kiện biên này phải được ghi rõ trong bài giảng.

**Trên màn hình:** Giải hệ E+O và E−O. | Hai tổng bằng nhau. | Cẩn thận trường hợp n=0.
**Ghi nhớ:** Cẩn thận trường hợp n=0.

### Nhịp 10 · 03:54 · Chứng minh bằng ghép đôi

Ngoài phép thế, có một lời giải tổ hợp rất đẹp. Chọn cố định một phần tử A trong tập gồm n phần tử. Với mỗi tập con, hãy bật hoặc tắt trạng thái của A, giữ nguyên các phần tử khác. Số phần tử được chọn tăng hoặc giảm đúng một, vì vậy tính chẵn lẻ đảo lại. Phép đổi này tự nghịch đảo và ghép từng tập chẵn với đúng một tập lẻ.

**Trên màn hình:** Mỗi tập con có một trạng thái A. | Đổi trạng thái A làm đổi chẵn/lẻ. | Tạo song ánh giữa hai nhóm.
**Ghi nhớ:** Tạo song ánh giữa hai nhóm.

### Nhịp 11 · 04:20 · Bài vận dụng n=8

Xét n bằng tám. Tổng tất cả hệ số là hai mũ tám, tức hai trăm năm mươi sáu. Bởi n dương nên mỗi nhóm chẵn lẻ chiếm đúng một nửa, tức một trăm hai mươi tám. Manim sẽ tô lần lượt những cột ở vị trí không, hai, bốn, sáu và tám. Học sinh có thể kiểm tra bằng Pascal trước khi chốt kết quả.

**Trên màn hình:** Tổng hệ số 256. | Tổng chẵn và lẻ bằng nhau. | Mỗi nhóm có 128.
**Ghi nhớ:** Mỗi nhóm có 128.

### Nhịp 12 · 04:46 · Khi điều kiện khó hơn

Ta vừa dùng hai giá trị đặc biệt là một và âm một để lọc các lớp chẵn lẻ. Nếu đề yêu cầu chỉ số chia ba dư một, ý tưởng tương tự còn hoạt động nhưng cần căn bậc ba của đơn vị. Đó là bộ lọc căn đơn vị trong tổ hợp nâng cao. Ở video này ta chỉ hé mở ý tưởng, còn chứng minh và ứng dụng đầy đủ sẽ nằm trong phần cao siêu cuối Series.

**Trên màn hình:** Chẵn/lẻ kiểm bằng x=-1. | Chia lớp dư modulo m: cần bộ lọc khác. | Đây là cầu nối sang tập 25.
**Ghi nhớ:** Đây là cầu nối sang tập 25.


## 03 · TRỌNG SỐ k NHÂN HỆ SỐ TỔ HỢP

### Nhịp 13 · 05:12 · Xuất hiện hệ số k

Hãy nhìn một tổng mới: mỗi hệ số tổ hợp C có n ở trên k ở dưới lại được nhân với k. Nếu cộng riêng từng số hạng, ta sẽ rất mất công. Điểm đáng chú ý là k chính là số mũ của x trong khai triển Newton. Khi đạo hàm x mũ k, hệ số k xuất hiện tự nhiên. Điều đó gợi ý một phép biến đổi hệ thống.

**Trên màn hình:** Tổng thường không còn đủ. | Hệ số C(n,k) bị nhân với k. | Đạo hàm sẽ kéo k xuống.
**Ghi nhớ:** Đạo hàm sẽ kéo k xuống.

### Nhịp 14 · 05:38 · Đạo hàm một lần

Ta đạo hàm hai vế khai triển một cộng x mũ n. Bên trái theo quy tắc hàm hợp nhận n nhân một cộng x mũ n trừ một. Bên phải, mỗi x mũ k trở thành k nhân x mũ k trừ một. Đây là bước quan trọng nhất: trọng số k không xuất hiện ngẫu nhiên, mà là kết quả trực tiếp của phép đạo hàm.

**Trên màn hình:** Bắt đầu từ (1+x)^n. | Lấy đạo hàm hai vế. | Hệ số k xuất hiện trước x^(k−1).
**Ghi nhớ:** Hệ số k xuất hiện trước x^(k−1).

### Nhịp 15 · 06:04 · Thay x bằng một

Sau khi lấy đạo hàm, thay x bằng một. Các lũy thừa x đều trở thành một nên vế phải chính là tổng có trọng số k. Vế trái cho n nhân hai mũ n trừ một. Vậy ta có công thức cực kỳ hữu dụng mà không cần khai triển. Lưu ý số hạng k bằng không tự biến mất, nên viết tổng từ không hay một đều được.

**Trên màn hình:** Sau đạo hàm mới thế x=1. | Vế phải trở thành tổng cần tính. | Vế trái thu gọn tức thì.
**Ghi nhớ:** Vế trái thu gọn tức thì.

### Nhịp 16 · 06:30 · Chứng minh bằng đếm đôi

Chúng ta có thể chứng minh công thức ấy mà không dùng đạo hàm. Hãy đếm các cặp gồm một tập con S và một phần tử được đánh dấu nằm trong S. Nếu S có k phần tử, có k cách chọn dấu nên vế trái xuất hiện. Mặt khác, chọn phần tử được đánh dấu trong n cách, các phần tử còn lại tùy chọn hai trạng thái, cho n nhân hai mũ n trừ một.

**Trên màn hình:** Chọn tập con S. | Đánh dấu một phần tử thuộc S. | Đếm theo phần tử được đánh dấu.
**Ghi nhớ:** Đếm theo phần tử được đánh dấu.

### Nhịp 17 · 06:56 · Ví dụ n=5

Xét n bằng năm. Công thức cho năm nhân hai mũ bốn bằng tám mươi. Để nhìn thấy ý nghĩa, hãy chọn một thẻ đánh dấu trong năm thẻ trước, rồi bật hoặc tắt bốn thẻ còn lại. Có năm cách chọn vị trí đánh dấu, mỗi cách sinh mười sáu tập con. Hình động minh họa chính xác mối liên hệ giữa đại số và tổ hợp.

**Trên màn hình:** Tổng 5·C(5,5)+... | Làm nổi bật số vị trí được đánh dấu. | Kết quả 5×16=80.
**Ghi nhớ:** Kết quả 5×16=80.

### Nhịp 18 · 07:22 · Mở rộng có a,b

Với những tổng có thêm a mũ n trừ k và b mũ k, ta sử dụng đa thức a cộng b nhân x tất cả mũ n. Sau một lần đạo hàm, bên trái xuất hiện hệ số n nhân b; bên phải có k nhân từng hệ số tổ hợp. Thay x bằng một sẽ thu đúng tổng có trọng số. Đây là sự chuẩn bị cần thiết cho bài toán rất khó ở cuối video.

**Trên màn hình:** Đạo hàm (a+bx)^n. | Một lần đạo hàm sinh hệ số b. | Thế x=1 sau khi đạo hàm.
**Ghi nhớ:** Thế x=1 sau khi đạo hàm.


## 04 · TRỌNG SỐ k(k−1) VÀ k BÌNH PHƯƠNG

### Nhịp 19 · 07:48 · Đánh dấu hai phần tử

Bây giờ hãy đánh dấu hai phần tử khác nhau trong cùng một tập con, có phân biệt dấu thứ nhất và dấu thứ hai. Với một tập có k phần tử, dấu đầu có k cách, dấu sau còn k trừ một cách. Vì thế số cách là k nhân k trừ một. Phép đếm sẽ tạo ra tổng trọng số mới, và hai lần đạo hàm chính là công cụ tương ứng.

**Trên màn hình:** Một tập có k phần tử. | Chọn cặp dấu có thứ tự. | Có k(k−1) cách.
**Ghi nhớ:** Có k(k−1) cách.

### Nhịp 20 · 08:14 · Đạo hàm hai lần

Từ khai triển Newton, ta đạo hàm hai lần. Bên trái xuất hiện tích n nhân n trừ một, cùng lũy thừa một cộng x mũ n trừ hai. Bên phải, hệ số k nhân k trừ một xuất hiện trước x mũ k trừ hai. Đây là một công thức cần điều kiện n ít nhất bằng hai trong dạng viết trực tiếp; các trường hợp biên phải xét riêng nếu cần.

**Trên màn hình:** Đạo hàm Newton lần thứ nhất. | Lấy đạo hàm tiếp một lần. | Thu k(k−1) trước x^(k−2).
**Ghi nhớ:** Thu k(k−1) trước x^(k−2).

### Nhịp 21 · 08:40 · Tổng trọng số rơi

Thay x bằng một vào đẳng thức đạo hàm hai lần. Tổng có k nhân k trừ một sẽ bằng n nhân n trừ một nhân hai mũ n trừ hai. Có một cách hiểu tổ hợp: chọn hai phần tử đánh dấu theo thứ tự rồi chọn tùy ý trong n trừ hai phần tử còn lại. Công thức không phải mẹo; nó phản ánh một phép đếm hoàn toàn xác định.

**Trên màn hình:** Thế x=1 sau hai đạo hàm. | Vế phải thành tổng k(k−1)C. | Vế trái cho n(n−1)2^(n−2).
**Ghi nhớ:** Vế trái cho n(n−1)2^(n−2).

### Nhịp 22 · 09:06 · Tách k bình phương

Khi gặp k bình phương, đừng cố đạo hàm một cách thiếu kiểm soát. Ta tách k bình phương thành k nhân k trừ một cộng k. Cả hai loại trọng số này đã được tính ở những nhịp trước. Hình động sẽ tách mỗi cột k bình phương thành hai phần có màu khác nhau, tượng trưng cho hai tổng mà ta có thể xử lý độc lập.

**Trên màn hình:** Viết k²=k(k−1)+k. | Hai tổng đều đã biết. | Cộng hai kết quả.
**Ghi nhớ:** Cộng hai kết quả.

### Nhịp 23 · 09:32 · Công thức tổng k²

Gộp hai kết quả thu được n nhân n trừ một nhân hai mũ n trừ hai, cộng n nhân hai mũ n trừ một. Rút nhân tử chung, ta được n nhân n cộng một nhân hai mũ n trừ hai. Công thức có giá trị với n ít nhất bằng một; n bằng không cho tổng bằng không và nên được ghi riêng thay vì xử lý lũy thừa âm máy móc.

**Trên màn hình:** Cộng tổng bậc hai rơi. | Cộng tổng bậc nhất. | Thu n(n+1)2^(n−2).
**Ghi nhớ:** Thu n(n+1)2^(n−2).

### Nhịp 24 · 09:58 · Thử với n=4

Ta kiểm chứng với n bằng bốn. Vế phải là bốn nhân năm nhân bốn, được tám mươi. Vế trái có các hạng không, bốn, hai mươi bốn, ba mươi sáu và mười sáu, cũng cho tám mươi. Manim sẽ dùng một biểu đồ cột biểu diễn từng đóng góp. Học sinh nhìn thấy các trọng số lớn làm thay đổi độ cao so với hàng Pascal ban đầu.

**Trên màn hình:** Vế phải: 4×5×4=80. | Vế trái dùng hàng 1,4,6,4,1. | Hai kết quả bằng nhau.
**Ghi nhớ:** Hai kết quả bằng nhau.


## 05 · TRỌNG SỐ BẬC CAO VÀ ĐẠO HÀM LẶP

### Nhịp 25 · 10:24 · Ba dấu có thứ tự

Nếu đánh dấu ba phần tử khác nhau của một tập con và phân biệt thứ tự ba dấu, số cách là k nhân k trừ một nhân k trừ hai. Đây là giai thừa rơi bậc ba. Trực quan, ba màu lần lượt đặt lên ba thẻ phân biệt. Cách đếm này sẽ tương ứng với lần đạo hàm thứ ba, và về sau tổng quát tới bất kỳ bậc r.

**Trên màn hình:** Lấy ba phần tử khác nhau. | Thứ tự ba dấu quan trọng. | Trọng số k(k−1)(k−2).
**Ghi nhớ:** Trọng số k(k−1)(k−2).

### Nhịp 26 · 10:50 · Đạo hàm bậc r

Đối với đạo hàm bậc r, mỗi lần đạo hàm một đơn thức lại kéo xuống một thừa số. Kết quả là tích k, k trừ một, đến k trừ r cộng một. Ở vế trái cũng xuất hiện tích tương tự bắt đầu từ n. Thay x bằng một cho công thức tổng quát về giai thừa rơi. Điều kiện tự nhiên là r nằm giữa không và n.

**Trên màn hình:** Mỗi lần kéo một thừa số xuống. | Thu trọng số (k)_r. | Vế trái có (n)_r.
**Ghi nhớ:** Vế trái có (n)_r.

### Nhịp 27 · 11:16 · Viết k³ theo giai thừa rơi

Để xử lý trọng số k lập phương, ta không cần lập một phép tính hoàn toàn mới. Có một đẳng thức đẹp: k lập phương bằng tích k nhân k trừ một nhân k trừ hai, cộng ba lần k nhân k trừ một, cộng k. Mỗi thành phần là giai thừa rơi, nên công thức tổng đã có sẵn. Đây là bước đầu nhận diện cấu trúc của số Stirling loại hai.

**Trên màn hình:** Tách thành (k)_3. | Cộng 3(k)_2. | Cuối cùng cộng k.
**Ghi nhớ:** Cuối cùng cộng k.

### Nhịp 28 · 11:42 · Tổng k³C

Áp dụng lần lượt các công thức của giai thừa rơi bậc ba, bậc hai và bậc nhất. Sau khi rút gọn, tổng k lập phương nhân hệ số tổ hợp bằng n bình phương nhân n cộng ba nhân hai mũ n trừ ba. Với các giá trị n nhỏ, nên hiểu qua đẳng thức đa thức rồi kiểm tra trực tiếp, vì cách viết chứa lũy thừa hai với số mũ âm.

**Trên màn hình:** Áp dụng tổng r=3. | Thêm ba lần tổng r=2. | Cộng tổng r=1.
**Ghi nhớ:** Cộng tổng r=1.

### Nhịp 29 · 12:08 · Số Stirling xuất hiện

Nhìn tổng quát, mọi lũy thừa k mũ r đều có thể viết thành tổng các giai thừa rơi, với hệ số là các số Stirling loại hai. Đó là một trong những công thức đẹp và ít gặp của tổ hợp. Hôm nay học sinh chỉ cần nắm tư duy phân rã trọng số; phần triển khai bảng Stirling và hàm sinh sẽ xuất hiện ở các tập cao cấp sau.

**Trên màn hình:** k^r là tổ hợp các giai thừa rơi. | Hệ số là Stirling loại hai. | Cầu nối sang hàm sinh và DP.
**Ghi nhớ:** Cầu nối sang hàm sinh và DP.

### Nhịp 30 · 12:34 · Tư duy chọn công cụ

Đến đây ta có một quy tắc lựa chọn công cụ. Thấy trọng số k thì đạo hàm một lần; thấy k nhân k trừ một thì đạo hàm hai lần; thấy lũy thừa k cao hơn thì đổi cơ sở sang giai thừa rơi. Ngoài ra, toán tử x nhân đạo hàm cũng thường xuất hiện trong lời giải ngắn. Cách nhìn này sẽ giúp xử lý các tổng trông rất lạ mà vẫn có phương pháp.

**Trên màn hình:** k, k², k³: dùng đạo hàm. | Phân rã sang giai thừa rơi. | Không mở rộng n số hạng bằng tay.
**Ghi nhớ:** Không mở rộng n số hạng bằng tay.


## 06 · MẪU SỐ k+1 VÀ TÍCH PHÂN

### Nhịp 31 · 13:00 · Tổng có mẫu

Ta chuyển sang dạng tổng hoàn toàn khác: mỗi hệ số tổ hợp được chia cho k cộng một. Đạo hàm làm tăng hệ số k, nên không thể trực tiếp tạo ra một mẫu số như thế. Hãy nhớ công thức nguyên hàm của x mũ k: khi tích phân từ không tới một sẽ được một chia k cộng một. Đây là dấu hiệu mạnh cho biết nên tích phân khai triển Newton.

**Trên màn hình:** Tổng C(n,k)/(k+1). | Đạo hàm không tạo mẫu này. | Tích phân x^k sẽ sinh 1/(k+1).
**Ghi nhớ:** Tích phân x^k sẽ sinh 1/(k+1).

### Nhịp 32 · 13:26 · Diện tích dưới đồ thị

Trên hình, mỗi hàm x mũ k có một miền diện tích dưới đồ thị từ không tới một. Diện tích ấy bằng một chia k cộng một, kể cả k bằng không. Khi cộng các hàm với hệ số Newton, tích phân tuyến tính cho phép cộng các diện tích có trọng số. Như vậy một bài tính tổng hệ số có mẫu được biến thành bài tính một tích phân rất quen thuộc.

**Trên màn hình:** Trên [0,1], x^k không âm. | Diện tích ứng với 1/(k+1). | Gom các diện tích bằng tính tuyến tính.
**Ghi nhớ:** Gom các diện tích bằng tính tuyến tính.

### Nhịp 33 · 13:52 · Tích phân Newton

Ta viết khai triển Newton của một cộng x mũ n rồi tích phân từng vế trên đoạn từ không đến một. Ở vế phải, mỗi đơn thức tạo ra mẫu số k cộng một, đúng tổng đang tìm. Ở vế trái, tích phân của một cộng x mũ n lại rất dễ. Điều quan trọng là phép đổi tổng và tích phân hợp lệ vì đây chỉ là một tổng hữu hạn.

**Trên màn hình:** Tích phân hai vế từ 0 đến 1. | Vế phải là I_n. | Vế trái tích phân (1+x)^n.
**Ghi nhớ:** Vế trái tích phân (1+x)^n.

### Nhịp 34 · 14:18 · Công thức bất ngờ

Tính nguyên hàm và thế hai đầu mút, ta được hai mũ n cộng một trừ một, tất cả chia cho n cộng một. Học sinh sẽ thấy một tổng gồm rất nhiều phân số bất ngờ rút lại thành một phân số đơn giản. Đây là một công thức hay và khá lạ trong phần tổ hợp, đồng thời minh họa tư duy chọn phép toán dựa theo trọng số của tổng.

**Trên màn hình:** Nguyên hàm: (1+x)^(n+1)/(n+1). | Lấy giá trị tại 1 trừ tại 0. | Nhận biểu thức đóng.
**Ghi nhớ:** Nhận biểu thức đóng.

### Nhịp 35 · 14:44 · Kiểm chứng n=3

Ta thay n bằng ba để kiểm tra. Tổng có bốn số hạng, gồm một, ba phần hai, một và một phần tư, bằng mười lăm phần tư. Công thức tổng quát cho hai mũ bốn trừ một chia bốn, cũng bằng mười lăm phần tư. Kết quả khớp nhau. Tuy nhiên chứng minh thực sự vẫn là bước tích phân, chứ không phải chỉ kiểm tra vài giá trị.

**Trên màn hình:** Tổng: 1+3/2+3/3+1/4. | Vế phải: (16−1)/4. | Kết quả 15/4.
**Ghi nhớ:** Kết quả 15/4.

### Nhịp 36 · 15:10 · Bài toán gợi mở

Muốn tạo mẫu tích của k cộng một và k cộng hai, ta có thể xét tích phân của x mũ k nhân một trừ x. Tích phân này cho đúng nghịch đảo của tích hai số liên tiếp. Như vậy phép tích phân mở ra cả một họ đồng nhất thức có mẫu. Video chuyên sâu về hàm sinh sẽ khai thác thêm những biến đổi tương tự một cách có hệ thống.

**Trên màn hình:** Nếu mẫu là (k+1)(k+2)? | Tích phân hai lần hoặc đổi cơ sở. | Chuẩn bị cho hàm Beta và hàm sinh.
**Ghi nhớ:** Chuẩn bị cho hàm Beta và hàm sinh.


## 07 · TỔNG XEN DẤU KHÔNG ĐẦY ĐỦ

### Nhịp 37 · 15:36 · Không thể dùng ngay x=-1

Ở chương hai, thay x bằng âm một cho tổng xen dấu của cả hàng Pascal bằng không. Nhưng bây giờ tổng chỉ dừng ở k bằng r, nhỏ hơn n. Ta không thể lấy đáp án bằng không, bởi những số hạng phía sau đã bị bỏ mất. Để xử lý tổng từng đoạn, ta sẽ khai thác hệ thức Pascal cho hai phần tử tổ hợp liền nhau.

**Trên màn hình:** Tổng chỉ chạy đến k=r<n. | Không phải tất cả hệ số Newton. | Cần một phép triệt tiêu khác.
**Ghi nhớ:** Cần một phép triệt tiêu khác.

### Nhịp 38 · 16:02 · Tách mỗi hệ số

Ta áp dụng hệ thức Pascal: hệ số tổ hợp có n ở trên, k ở dưới bằng tổng hai hệ số thuộc hàng n trừ một. Thay vào tổng xen dấu, ta thu hai tổng lệch chỉ số một đơn vị. Mỗi số hạng ở giữa xuất hiện một lần dương và một lần âm nên bị triệt tiêu. Hình động sẽ cho các ô triệt tiêu từng đôi, chỉ còn một ô ở mép phải.

**Trên màn hình:** Dùng C(n,k)=C(n−1,k)+C(n−1,k−1). | Thay vào tổng xen dấu. | Hai chuỗi số hạng triệt tiêu.
**Ghi nhớ:** Hai chuỗi số hạng triệt tiêu.

### Nhịp 39 · 16:28 · Công thức tổng đoạn

Khi mọi số hạng ở giữa bị triệt tiêu, chỉ còn hệ số ở hàng n trừ một, cột r, kèm dấu âm một mũ r. Đây là đồng nhất thức tổng xen dấu từng phần. Nó rất hữu ích trong bài toán tính tổng lạ, và cũng là bước đầu cho kỹ thuật telescoping, tức làm các số hạng liên tiếp khử nhau trong một tổng.

**Trên màn hình:** Các hạng giữa triệt tiêu. | Chỉ còn hạng cuối mang dấu (-1)^r. | Điều kiện 0≤r<n.
**Ghi nhớ:** Điều kiện 0≤r<n.

### Nhịp 40 · 16:54 · Thử n=6,r=3

Kiểm chứng với n bằng sáu và r bằng ba. Tổng bốn số hạng đầu là một trừ sáu cộng mười lăm trừ hai mươi, được âm mười. Công thức bên phải là âm của tổ hợp chọn ba trong năm, cũng bằng âm mười. Trên tam giác Pascal, ta sẽ tô bốn hệ số đầu của hàng thứ sáu và kéo kết quả về một hệ số ở hàng thứ năm.

**Trên màn hình:** Lấy 1−6+15−20. | Giá trị bằng −10. | Vế phải −C(5,3)=−10.
**Ghi nhớ:** Vế phải −C(5,3)=−10.

### Nhịp 41 · 17:20 · Cẩn thận các đầu mút

Hãy kiểm tra đầu mút của công thức. Nếu r bằng không, tổng có duy nhất một số hạng bằng một, và biểu thức ở hàng n trừ một cũng bằng một. Nếu r bằng n, tổng trở thành cả hàng xen dấu, bằng không với n dương. Công thức dành cho đoạn r nhỏ hơn n, vì vậy không thay r bằng n vào C có n trừ một ở trên một cách máy móc.

**Trên màn hình:** r=0: tổng bằng 1. | r=n: tổng toàn hàng bằng 0 (n>0). | Không áp dụng công thức đoạn sai miền.
**Ghi nhớ:** Không áp dụng công thức đoạn sai miền.

### Nhịp 42 · 17:46 · Mở rộng định hướng

Ta vừa gặp một đồng nhất thức khá bất ngờ: cộng những số lớn xen dấu lại chỉ còn một hệ số tổ hợp ở hàng trước. Bản chất nằm ở hệ thức Pascal và phép triệt tiêu. Điều này sẽ xuất hiện nhiều lần trong bao hàm trừ nâng cao, đặc biệt khi đếm những trường hợp bị cấm theo số điều kiện vi phạm. Đó là hướng phát triển của các tập cao cấp.

**Trên màn hình:** Có thể biến đổi tổng từng đoạn. | Đặc biệt mạnh khi hệ số xen dấu. | Nối tới bù trừ nâng cao.
**Ghi nhớ:** Nối tới bù trừ nâng cao.


## 08 · BÀI OLYMPIC: TỔNG CÓ TRỌNG SỐ VÀ HỆ SỐ MŨ

### Nhịp 43 · 18:12 · Đề bài tổng hợp

Bài toán cuối tập yêu cầu tính tổng của k bình phương nhân hệ số tổ hợp chọn k trong sáu, nhân hai mũ k và ba mũ sáu trừ k. Nhìn thoáng qua có rất nhiều nhân tử. Nhưng ta đã có đủ công cụ: hệ số của a cộng b x, đạo hàm tạo trọng số k, và hai lần đạo hàm tạo k nhân k trừ một. Ta sẽ giải bằng hai cách độc lập.

**Trên màn hình:** Cho tổng Σ k² C(6,k) 2^k 3^(6−k). | Trọng số vừa k² vừa có hai lũy thừa. | Không nên khai triển bảy hạng bằng tay.
**Ghi nhớ:** Không nên khai triển bảy hạng bằng tay.

### Nhịp 44 · 18:38 · Dựng đa thức nguồn

Đặt F của x bằng ba cộng hai x tất cả mũ sáu. Khai triển nhị thức Newton cho những số hạng có đúng hai mũ k và ba mũ sáu trừ k như trong đề. Do đó chỉ cần biến đổi F để sinh thêm trọng số k bình phương. Không có lý do gì phải khai triển bảy số hạng rất lớn; ta tìm một biểu thức đại số có cấu trúc đúng yêu cầu.

**Trên màn hình:** F(x)=(3+2x)^6. | Khai triển sinh 2^k3^(6−k). | Đánh dấu hệ số k² cần tạo.
**Ghi nhớ:** Đánh dấu hệ số k² cần tạo.

### Nhịp 45 · 19:04 · Hai đạo hàm có trọng số

Quan sát các hệ số của đa thức F. F phẩy khi thế x bằng một cho tổng nhân k, còn F phẩy hai cho tổng k nhân k trừ một. Vì k bình phương bằng tổng hai trọng số ấy, ta có S bằng F phẩy một cộng F phẩy hai, cùng tính tại x bằng một. Đó là bước phân tích mang tính quyết định, không phải chỉ thay công thức một cách ngẫu nhiên.

**Trên màn hình:** xF′ tạo k·hệ số. | x²F″ tạo k(k−1)·hệ số. | Cộng lại tạo k².
**Ghi nhớ:** Cộng lại tạo k².

### Nhịp 46 · 19:30 · Tính F′(1)

Đạo hàm lần thứ nhất của ba cộng hai x mũ sáu cho mười hai nhân ba cộng hai x mũ năm. Tại x bằng một, cơ số trở thành năm, và kết quả là mười hai nhân năm mũ năm, tức ba mươi bảy nghìn năm trăm. Hình động sẽ tô nhóm đóng góp của hạng bậc nhất trong phép phân rã k bình phương.

**Trên màn hình:** F′(x)=12(3+2x)^5. | Thay x=1 được 12·5^5. | Kết quả 37.500.
**Ghi nhớ:** Kết quả 37.500.

### Nhịp 47 · 19:56 · Tính F″(1)

Lấy đạo hàm lần thứ hai, ta được một trăm hai mươi nhân ba cộng hai x mũ bốn. Thay x bằng một, có một trăm hai mươi nhân năm mũ bốn, tức bảy mươi lăm nghìn. Đó là tổng của những thành phần k nhân k trừ một trong đề. Cộng với kết quả của một đạo hàm ta sẽ có tổng cần tìm.

**Trên màn hình:** F″(x)=120(3+2x)^4. | Thay x=1 được 120·5^4. | Kết quả 75.000.
**Ghi nhớ:** Kết quả 75.000.

### Nhịp 48 · 20:22 · Kết quả và lời giải tổ hợp

Cộng ba mươi bảy nghìn năm trăm với bảy mươi lăm nghìn, ta thu một trăm mười hai nghìn năm trăm. Có một cách hiểu tổ hợp độc lập: phân phối sáu vị trí, mỗi vị trí chọn một trong hai hoặc ba màu có trọng số, rồi đánh dấu một vị trí thuộc nhóm hai màu, hoặc một cặp vị trí có thứ tự thuộc nhóm ấy. Hai kiểu dấu tạo tương ứng k và k nhân k trừ một. Vì tổng số dấu là k bình phương, hai phép đếm khớp nhau.

**Trên màn hình:** 37.500+75.000=112.500. | Đánh dấu 1 hoặc 2 vị trí đặc biệt. | Hai cách đếm cùng kết quả.
**Ghi nhớ:** Hai cách đếm cùng kết quả.
