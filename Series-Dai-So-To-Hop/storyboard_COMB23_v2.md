# STORYBOARD COMB23 V2 – 48 NHỊP / 8 CHƯƠNG

Chuẩn cố định 16:9 Full HD: cột trái mô hình trực quan, cột phải đề bài → suy luận → công thức Typst. Ký hiệu C_k^n (n trên, k dưới).

Thời lượng nền: 22:29; 3.992 từ thuyết minh. Storyboard là tài liệu dựng cảnh, chưa phải video đã render.

## 01 · BA TẬP HỢP VÀ BAO HÀM–LOẠI TRỪ

### Nhịp 01 — Vì sao cộng rồi trừ?
- Hình động: mô hình `three_sets` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: 30 số nguyên từ 1 đến 30; Chia hết cho 2, 3 hoặc 5; Cùng một số có thể thỏa nhiều điều kiện
- Kết luận: Các nhóm có giao nhau không thể cộng thẳng.
- Công thức Typst: `15+10+6`

Hãy xét ba mươi số tự nhiên đầu tiên. Ta cần đếm những số chia hết cho hai hoặc ba hoặc năm. Nếu cộng số bội của hai, số bội của ba và số bội của năm, các số như sáu hay mười đã xuất hiện nhiều lần. Mô hình ba vùng trên màn hình cho thấy ngay vì sao phép cộng ban đầu không thể là đáp án cuối cùng.

### Nhịp 02 — Giao của hai tập
- Hình động: mô hình `three_sets` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: A: 15 số chia hết cho 2; B: 10 số chia hết cho 3; Giao A∩B gồm 5 bội của 6
- Kết luận: Giao phải được trừ để tránh đếm hai lần.
- Công thức Typst: `15+10-5=20`

Đầu tiên chỉ xét hai điều kiện. Trong ba mươi số, có mười lăm bội của hai và mười bội của ba. Năm bội của sáu thuộc đồng thời cả hai nhóm. Khi cộng, mỗi bội của sáu đã bị đếm hai lần; trừ đi một lần thì mỗi số hợp lệ được giữ đúng một lần. Đây là mẫu hình cơ bản của nguyên lý bao hàm và loại trừ.

### Nhịp 03 — Thêm tập thứ ba
- Hình động: mô hình `three_sets` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Bội của 5 có 6 số; Trừ giao 2–5: 3 số; Trừ giao 3–5: 2 số
- Kết luận: Thêm một điều kiện tạo những giao mới.
- Công thức Typst: `15+10+6-5-3-2`

Bây giờ thêm sáu bội của năm. Các số vừa chia hết cho hai vừa chia hết cho năm phải bị trừ, cũng như các số cùng chia hết cho ba và năm. Tuy vậy, một số chia hết cho cả hai, ba và năm đang bị cộng ba lần rồi trừ ba lần, nghĩa là biến mất. Ta cần một bước sửa cuối cùng để đưa số ấy trở lại.

### Nhịp 04 — Giao của cả ba
- Hình động: mô hình `three_sets` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Bội chung 2, 3, 5 là 30; Có đúng một số trong giao ba; Cộng lại đúng một lần
- Kết luận: Dấu của giao ba tập là dấu cộng.
- Công thức Typst: `15+10+6-5-3-2+1=22`

Số ba mươi nằm trong giao cả ba tập. Khi cộng ba số lượng ban đầu, ta đã tính nó ba lần; trừ ba giao đôi làm số lần còn không. Vì nó thực sự thỏa yêu cầu, phải cộng lại một lần. Sau khi sửa, số kết quả là hai mươi hai. Đây là lý do dấu của các giao luân phiên cộng, trừ rồi cộng, chứ không phải một mẹo để ghi nhớ.

### Nhịp 05 — Nguyên lý tổng quát
- Hình động: mô hình `three_sets` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn một số điều kiện phải đồng thời đúng; Mỗi giao được cộng hoặc trừ; Dấu phụ thuộc số điều kiện trong giao
- Kết luận: Mỗi kết quả hợp lệ cuối cùng được tính một lần.
- Công thức Typst: `N=sum_(j=1)^m (-1)^(j+1) S_j`

Với nhiều điều kiện, ta xét các giao của một điều kiện, rồi hai điều kiện, ba điều kiện, và tiếp tục. Tổng giao một điều kiện mang dấu cộng; tổng giao hai điều kiện mang dấu trừ; giao ba điều kiện lại mang dấu cộng. Với từng đối tượng thỏa đúng r điều kiện, tổng các hệ số luôn là một, còn đối tượng không thỏa điều kiện nào đóng góp bằng không. Nhờ đó nguyên lý đúng cho bất kỳ số điều kiện hữu hạn.

### Nhịp 06 — Cầu nối sang hoán vị
- Hình động: mô hình `three_sets` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Mỗi sự kiện cấm là một điều kiện; Giao nhiều điều kiện sẽ dễ đếm hơn; Ta sẽ dùng điều này để đếm hoán vị
- Kết luận: Đôi khi điều bị cấm dễ đếm hơn điều được phép.
- Công thức Typst: `N_("hợp lệ")=N_("tất cả")-N_("bị loại")`

Ý tưởng quan trọng nhất không phải chỉ là trừ các phần giao. Điều sâu sắc hơn là chuyển cách nhìn: thay vì hỏi những kết quả nào thỏa tất cả yêu cầu, hãy liệt kê những điều kiện có thể làm kết quả bị loại. Nếu mỗi giao của vài điều kiện cấm lại có cấu trúc đơn giản, nguyên lý bao hàm và loại trừ sẽ giải được những bài tưởng như không thể đếm trực tiếp. Bây giờ ta thử với các lá thư.

## 02 · HOÁN VỊ KHÔNG ĐIỂM CỐ ĐỊNH

### Nhịp 07 — Thư và phong bì
- Hình động: mô hình `derange` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: 4 lá thư mang tên A, B, C, D; 4 phong bì mang tên tương ứng; Không lá thư nào về đúng phong bì
- Kết luận: Đây là hoán vị không điểm cố định.
- Công thức Typst: `D_4=9`

Có bốn lá thư và bốn phong bì. Ta đặt ngẫu nhiên mỗi lá thư vào đúng một phong bì nhưng không lá nào được về phong bì mang tên nó. Nếu không có điều kiện, có bốn giai thừa bằng hai mươi bốn cách xếp. Mỗi ô chéo đỏ trên sơ đồ biểu diễn một việc cấm: người thứ i nhận đúng vị trí của mình. Ta sẽ loại đồng thời cả bốn điều kiện này.

### Nhịp 08 — Một vị trí bị cố định
- Hình động: mô hình `derange` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: E_i: thư i về đúng chỗ i; Có (n−1)! hoán vị thuộc E_i; Có n lựa chọn vị trí cố định
- Kết luận: Một điều kiện cố định đơn lẻ rất dễ đếm.
- Công thức Typst: `N(E_i)=(n-1)!`

Gọi E i là biến cố lá thư thứ i vào đúng phong bì thứ i. Nếu điều đó đã xảy ra, ta chỉ cần hoán vị n trừ một lá thư còn lại. Vì vậy mỗi biến cố cấm chứa đúng giai thừa n trừ một kết quả. Có n biến cố kiểu này. Nhưng khi cộng tất cả biến cố, những hoán vị có hai vị trí đúng sẽ bị tính hai lần, nên ta chưa thể chỉ lấy n giai thừa rồi trừ ngay.

### Nhịp 09 — Hai hoặc nhiều vị trí cố định
- Hình động: mô hình `derange` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn k vị trí bắt buộc đúng; Các vị trí khác tùy ý hoán vị; Số phần giao là (n−k)!
- Kết luận: Giao của k điều kiện có cấu trúc giai thừa.
- Công thức Typst: `N(E_(i_1) cap dots cap E_(i_k))=(n-k)!`

Nếu đã chọn k lá thư buộc phải về đúng địa chỉ, chúng chiếm k phong bì phân biệt. Còn n trừ k lá thư chưa bị ràng buộc trong phép đếm phần giao, nên có đúng giai thừa n trừ k cách sắp xếp. Với mỗi k, có tổ hợp chập k của n cách chọn những vị trí bị cố định. Điều này làm tất cả số hạng của nguyên lý bao hàm và loại trừ trở nên tính được.

### Nhịp 10 — Công thức hoán vị không cố định
- Hình động: mô hình `derange` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Tổng số hoán vị là n!; Trừ giao lẻ, cộng giao chẵn; Số cách không ai đúng vị trí
- Kết luận: D_n là số hoán vị không điểm cố định.
- Công thức Typst: `D_n=sum_(k=0)^n (-1)^k C_k^n (n-k)!`

Ghép các kết quả vừa tìm được, số hoán vị không có vị trí đúng bằng tổng các số hạng có dấu luân phiên. Với k bằng không, ta có tất cả n giai thừa hoán vị. Với k bằng một, ta trừ các hoán vị cố định một vị trí. Với k bằng hai, cộng lại các giao đôi, và tiếp tục đến k bằng n. Công thức này chính là một ứng dụng tiêu biểu của bao hàm và loại trừ.

### Nhịp 11 — Tính D4 và D5
- Hình động: mô hình `derange` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: D4 = 9 và D5 = 44; D6 = 265; Liệt kê trực tiếp chỉ để kiểm chứng
- Kết luận: Công thức mở rộng được cho n lớn.
- Công thức Typst: `D_4=9,quad D_5=44,quad D_6=265`

Với bốn lá thư ta thu được chín hoán vị hợp lệ. Khi tăng lên năm lá thư có bốn mươi bốn cách, còn sáu lá thư có hai trăm sáu mươi lăm cách. Máy có thể kiểm tra những số nhỏ bằng liệt kê, nhưng lời giải toán học không cần sinh ra tất cả hoán vị. Một khi đã có công thức, số điều kiện càng nhiều thì việc nhóm các giao theo kích thước càng quan trọng.

### Nhịp 12 — Hai cách viết và xấp xỉ
- Hình động: mô hình `derange` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Rút gọn C_k^n(n−k)! = n!/k!; D_n/n! tiến gần 1/e; Xác suất xấp xỉ 36,8 phần trăm
- Kết luận: Công thức hữu hạn dẫn tới hằng số e.
- Công thức Typst: `D_n=n! sum_(k=0)^n (-1)^k / k!`

Thay tổ hợp chập k của n bằng n giai thừa chia k giai thừa nhân n trừ k giai thừa, số hạng rút gọn thành n giai thừa chia k giai thừa. Vì thế xác suất một hoán vị ngẫu nhiên không có điểm cố định là một tổng xen dấu của các nghịch đảo giai thừa. Khi n tăng, tổng ấy tiến về một chia e, xấp xỉ ba mươi sáu phẩy tám phần trăm. Đây là một liên hệ đẹp giữa tổ hợp hữu hạn và giải tích.

## 03 · CHỈ CẤM CỐ ĐỊNH MỘT VÀI VỊ TRÍ

### Nhịp 13 — Không cấm tất cả các vị trí
- Hình động: mô hình `fixed_ban` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: 6 người nhận 6 phần việc; Chỉ A, B, C không được tự nhận việc; D, E, F có thể nhận đúng
- Kết luận: Phân biệt 3 điều kiện cấm với 6 điều kiện.
- Công thức Typst: `N=426`

Có sáu người và sáu công việc, mỗi người nhận đúng một việc. Chỉ ba người đầu tiên là A, B và C bị cấm nhận công việc trùng tên; ba người còn lại hoàn toàn không có điều kiện này. Vì vậy chúng ta có ba biến cố cấm, chứ không phải sáu. Nếu lấy ngay số hoán vị không điểm cố định của sáu phần tử, ta đã vô tình thêm ba điều kiện mà đề bài không yêu cầu.

### Nhịp 14 — Tổng ban đầu
- Hình động: mô hình `fixed_ban` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: 6! = 720 phép phân công; Một người tự nhận: 5! cách; Có 3 người cần xét cấm
- Kết luận: Luôn xác định đúng tập biến cố cấm.
- Công thức Typst: `6!-3 cdot 5!`

Ta bắt đầu từ bảy trăm hai mươi cách phân công không điều kiện. Nếu người A nhận đúng việc A, năm người khác có năm giai thừa cách. Tương tự với B và C. Vậy tổng ba biến cố đơn là ba nhân năm giai thừa. Tuy nhiên, trong tổng này có những phép phân công đồng thời để A và B nhận đúng, nên phần giao tiếp tục xuất hiện và cần được khôi phục.

### Nhịp 15 — Cộng lại các giao đôi
- Hình động: mô hình `fixed_ban` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Có C_2^3 = 3 cặp; Mỗi cặp cố định cho 4! cách; Cộng lại 3 · 4!
- Kết luận: Mỗi giao đôi có cùng số cách.
- Công thức Typst: `6!-3 cdot 5!+3 cdot 4!`

Chọn hai trong ba người A, B, C để bắt buộc nhận đúng việc tương ứng. Có ba lựa chọn như vậy. Sau khi cố định hai công việc, còn bốn người có thể sắp vào bốn nhiệm vụ còn lại với bốn giai thừa cách. Các phép phân công bị trừ hai lần ở bước trước cần được cộng trở lại một lần. Trên bảng, những ô giao được đổi từ màu đỏ sang màu tím khi dấu phép đếm thay đổi.

### Nhịp 16 — Trừ giao cả ba
- Hình động: mô hình `fixed_ban` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: A, B và C đều nhận đúng việc; Còn 3! cách cho D, E, F; Giao ba mang dấu trừ
- Kết luận: Trừ lần cuối để mỗi kết quả được tính đúng.
- Công thức Typst: `720-360+72-6=426`

Cuối cùng, nếu cả A, B, C đều nhận đúng việc, chỉ còn ba người D, E, F hoán vị các việc còn lại, có sáu cách. Những kết quả này đã cộng trừ thừa một lần và phải trừ tiếp. Vậy số phép phân công hợp lệ bằng bảy trăm hai mươi trừ ba trăm sáu mươi, cộng bảy mươi hai rồi trừ sáu, bằng bốn trăm hai mươi sáu.

### Nhịp 17 — Viết công thức với m vị trí cấm
- Hình động: mô hình `fixed_ban` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Có n phần tử, m vị trí tự cố định bị cấm; Chọn k trong m điều kiện để giao; Mỗi giao có (n−k)! cách
- Kết luận: Số biến cố cấm m có thể nhỏ hơn n.
- Công thức Typst: `N=sum_(k=0)^m (-1)^k C_k^m (n-k)!`

Với n phần tử nhưng chỉ m vị trí tự cố định bị cấm, ta không cần tạo một công thức hoàn toàn mới. Chỉ việc thay n ở số cách chọn điều kiện bằng m, nhưng giai thừa của những vị trí còn lại vẫn là n trừ k. Sự phân biệt hai tham số m và n rất quan trọng: m đếm số điều kiện cấm, còn n là tổng số đối tượng được phân công.

### Nhịp 18 — Tại sao không dùng (n−m)!D_m?
- Hình động: mô hình `fixed_ban` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Người không bị cấm vẫn có thể chiếm việc của A; Những vị trí giữa hai nhóm tương tác; Không tách thành hai phép đếm độc lập
- Kết luận: Không nhân số cách nếu các lựa chọn phụ thuộc.
- Công thức Typst: `N_(6,3)=426`

Một sai lầm phổ biến là cho rằng ba người bị cấm tự nhận việc tạo thành một bài toán hoán vị không điểm cố định trên ba người, rồi nhân với ba giai thừa của những người còn lại. Nhưng mỗi người có thể nhận việc thuộc nhóm kia. Hai nhóm không độc lập và cách nhân đó loại sai những phép phân công hợp lệ. Phép đếm bằng các biến cố cấm đã bao quát đúng mọi khả năng, kể cả các trường hợp trao đổi qua lại giữa hai nhóm.

## 04 · BÀN CỜ CẤM VÀ ĐA THỨC XE

### Nhịp 19 — Bàn cờ 4×4
- Hình động: mô hình `diagonal` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Hàng là học sinh, cột là nhiệm vụ; Mỗi hoán vị đặt 4 quân xe; Các ô đường chéo bị cấm
- Kết luận: Một phép phân công chính là một cách đặt xe.
- Công thức Typst: `R(x)=1+4x+6x^2+4x^3+x^4`

Ta đổi cách nhìn: bốn người là bốn hàng và bốn nhiệm vụ là bốn cột trên bàn cờ. Một phép phân công đặt đúng một quân xe ở mỗi hàng và mỗi cột, các quân không ăn nhau. Những ô cấm nằm trên đường chéo chính. Khi một hoán vị đi vào ô cấm, ta coi đó là một điều kiện sai. Mô hình bàn cờ sẽ dẫn đến công cụ mang tên đa thức xe.

### Nhịp 20 — Chọn một ô cấm
- Hình động: mô hình `diagonal` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Một quân xe có 4 vị trí cấm; Hệ số r1 = 4; r0 = 1 là chọn rỗng
- Kết luận: Hệ số r_k đếm k xe trên các ô cấm.
- Công thức Typst: `r_0=1,quad r_1=4`

Để xây đa thức xe, không đặt ngay đủ bốn quân. Ta đếm các cách đặt k quân chỉ vào những ô màu đỏ, vẫn yêu cầu không chung hàng và không chung cột. Khi k bằng không có đúng một cách chọn rỗng, nên hệ số đầu là một. Với k bằng một có bốn ô đỏ. Tính chất không ăn nhau chính là điều kiện bảo đảm các vị trí cấm có thể cùng xảy ra trong một hoán vị.

### Nhịp 21 — Hai và ba quân xe
- Hình động: mô hình `diagonal` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn 2 trong 4 ô chéo: 6 cách; Chọn 3 trong 4 ô chéo: 4 cách; 4 quân có 1 cách đặt
- Kết luận: Đa thức xe gom các giao theo số ô cấm.
- Công thức Typst: `r_2=6,quad r_3=4,quad r_4=1`

Bốn ô cấm đều nằm ở hàng và cột khác nhau. Vì thế chọn hai ô bất kỳ tạo một cách đặt hai xe không ăn nhau; có sáu cách. Chọn ba ô được bốn cách, và chọn đủ bốn ô được một cách. Các hệ số một, bốn, sáu, bốn, một giống một hàng của tam giác Pascal. Điều đó không phải ngẫu nhiên: ở bàn chéo, mọi tập hợp các điều kiện cấm đều tương thích.

### Nhịp 22 — Lập đa thức R(x)
- Hình động: mô hình `diagonal` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: R(x) = Σ r_k x^k; Hệ số chứa thông tin mọi giao cấm; Đa thức không phải số hoán vị hợp lệ
- Kết luận: Chưa được đọc số cách hợp lệ từ R(1).
- Công thức Typst: `R(x)=(1+x)^4`

Đưa các hệ số vừa đếm vào đa thức xe. Số mũ k ghi rằng chúng ta đã cố định k ô cấm đồng thời, còn hệ số r k là số cách chọn những ô ấy mà không xung đột nhau. Đa thức này chỉ tóm tắt cấu trúc của những điều kiện bị cấm. Nó chưa phải hàm sinh của các hoán vị hợp lệ, và giá trị tại một không cho ta trực tiếp số phép phân công cần tìm.

### Nhịp 23 — Phép khử từ đa thức xe
- Hình động: mô hình `diagonal` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn k ô cấm tương thích; Còn (n−k)! cách xếp phần còn lại; Cộng trừ theo k để loại điều kiện cấm
- Kết luận: r_k thay thế việc liệt kê từng giao.
- Công thức Typst: `N=sum_(k=0)^n (-1)^k r_k (n-k)!`

Với một cách đặt k xe không ăn nhau trên các ô cấm, ta đã ấn định k người vào k nhiệm vụ bị cấm. Còn n trừ k hàng và cột chưa được dùng nên có n trừ k giai thừa cách hoàn tất. Nguyên lý bao hàm và loại trừ cho thấy cứ k điều kiện cấm đồng thời thì lấy hệ số dấu âm một mũ k. Vì vậy r k nhân với giai thừa n trừ k là đúng số hạng cần cộng hoặc trừ.

### Nhịp 24 — Thu lại kết quả chín cách
- Hình động: mô hình `diagonal` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: 24 − 4·6 + 6·2 − 4·1 + 1; Số cách là 9; Đối chiếu trực tiếp D4
- Kết luận: Đa thức xe mở rộng bài toán derangement.
- Công thức Typst: `24-24+12-4+1=9`

Trên bàn chéo bốn nhân bốn, ta thay lần lượt r không đến r bốn vào công thức. Kết quả là hai mươi bốn trừ hai mươi bốn, cộng mười hai, trừ bốn, cộng một: còn chín cách. Đây chính là số hoán vị không điểm cố định đã tìm trước đó. Điểm quan trọng là công cụ mới không chỉ giải được đường chéo: nó vẫn hoạt động khi các ô cấm tạo thành một hình bất kỳ trên bàn cờ.

## 05 · BẢNG CẤM KHÔNG ĐỐI XỨNG

### Nhịp 25 — Bảng cấm không đối xứng
- Hình động: mô hình `board` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: 4 người nhận 4 việc; A bị cấm việc 1 và 2; B cấm 2; C cấm 3; D cấm 4
- Kết luận: Không còn tính chất mọi ô đỏ khác hàng.
- Công thức Typst: `N=6`

Ta xét một danh sách phân công khó hơn: người A bị cấm hai công việc đầu, B bị cấm công việc thứ hai, C bị cấm thứ ba và D bị cấm thứ tư. Bàn cờ có năm ô cấm, nhưng hai ô nằm cùng hàng A. Chúng không thể cùng xuất hiện trong một hoán vị vì mỗi người chỉ nhận một nhiệm vụ. Do đó hệ số của đa thức xe không còn là tổ hợp chập k của năm một cách máy móc.

### Nhịp 26 — Một quân: r1 = 5
- Hình động: mô hình `board` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Đếm trực tiếp 5 ô đỏ; Chỉ đặt 1 xe nên không xung đột; Không cần xét hàng cột khác nhau
- Kết luận: r1 bằng số ô cấm.
- Công thức Typst: `r_1=5`

Khi chỉ đặt một quân xe, mọi ô cấm đều là một vị trí hợp lệ để đặt quân, vì chưa có quân nào khác gây xung đột. Ta đếm được năm ô màu đỏ và nhận r một bằng năm. Nhưng từ bước hai xe, hình dạng bàn cờ bắt đầu ảnh hưởng: hai ô cùng hàng A không thể được chọn đồng thời. Các trường hợp không tương thích phải bị loại ngay trong lúc tính hệ số.

### Nhịp 27 — Hai quân: r2 = 8
- Hình động: mô hình `board` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Có C_2^5 = 10 cặp ô; Trừ cặp trùng hàng A; Trừ cặp trùng cột 2
- Kết luận: Phải kiểm tra cả hàng và cột.
- Công thức Typst: `r_2=10-1-1=8`

Nếu chỉ chọn hai trong năm ô đỏ sẽ có mười cặp. Có một cặp nằm cùng hàng A: ô A một và A hai. Có thêm một cặp cùng cột hai: ô A hai và B hai. Hai cặp ấy không thể chứa đồng thời hai quân xe không ăn nhau. Các cặp còn lại đều hợp lệ, vì thế r hai bằng tám. Đây là bước học sinh dễ quên khi áp dụng đa thức xe.

### Nhịp 28 — Ba, bốn quân: 5 và 1
- Hình động: mô hình `board` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Liệt kê các bộ ba không xung đột; Có 5 cách đặt ba xe; Có 1 cách đặt đủ bốn xe
- Kết luận: Hệ số cao phụ thuộc hình dạng bảng cấm.
- Công thức Typst: `R(x)=1+5x+8x^2+5x^3+x^4`

Với ba quân, ta chỉ giữ những lựa chọn ba ô cấm nằm ở ba hàng và ba cột khác nhau. Có đúng năm cách. Khi đặt bốn quân vào bốn ô cấm không ăn nhau, chỉ còn một cách. Vì thế đa thức xe của bảng bất đối xứng này là một cộng năm x, cộng tám x bình phương, cộng năm x lập phương và x mũ bốn. Các hệ số không còn là hệ số nhị thức đơn giản như ở bàn đường chéo.

### Nhịp 29 — Tính số phép phân công
- Hình động: mô hình `board` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: N = 4! − 5·3! + 8·2!; Tiếp tục −5·1! +1·0!; Được 6 cách
- Kết luận: Thay hệ số xe vào đúng giai thừa còn lại.
- Công thức Typst: `24-30+16-5+1=6`

Sau khi có đa thức xe, phần tính toán tuân theo cùng một nguyên tắc. Bắt đầu bằng bốn giai thừa, trừ năm nhân ba giai thừa, cộng tám nhân hai giai thừa, trừ năm nhân một giai thừa và cộng một nhân không giai thừa. Kết quả bằng sáu cách phân công hợp lệ. Chương trình có thể duyệt cả hai mươi bốn hoán vị để xác nhận con số sáu, nhưng lời giải không cần kiểm tra từng phép phân công riêng lẻ.

### Nhịp 30 — Chọn mô hình đúng với đề
- Hình động: mô hình `board` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Mỗi hàng đúng một người; Mỗi cột đúng một nhiệm vụ; Ô đỏ thể hiện một cặp bị cấm
- Kết luận: Vẽ sai bàn cờ tức là giải sai đề.
- Công thức Typst: `N=6`

Trước khi dùng một công thức khó, hãy kiểm tra mô hình. Một người là một hàng, một nhiệm vụ là một cột; một ô đỏ là đúng một cặp người và nhiệm vụ bị cấm. Hai ô đỏ cùng hàng hay cùng cột có thể tạo xung đột trong cách đặt xe, nên không phải cứ có m ô cấm là hệ số r k sẽ bằng tổ hợp chập k của m. Toán học chính xác bắt đầu từ việc phiên dịch đúng điều kiện.

## 06 · ĐÚNG k ĐIỂM CỐ ĐỊNH

### Nhịp 31 — Không phải ai cũng sai vị trí
- Hình động: mô hình `rencontres` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Xếp 5 vật vào 5 vị trí; Yêu cầu đúng chính xác 2 vị trí; Ba vật còn lại phải đều sai
- Kết luận: Đúng k vị trí cố định khác ít nhất k vị trí.
- Công thức Typst: `R_(5,2)=20`

Sau những bài cấm tất cả hoặc chỉ một số vị trí, ta xét yêu cầu tinh tế hơn: một hoán vị của năm phần tử có chính xác hai vị trí cố định. Chữ chính xác rất quan trọng. Nếu chọn hai vị trí đúng mà không buộc ba vị trí còn lại sai, ta sẽ đếm cả những hoán vị có ba hoặc bốn điểm cố định. Chúng ta cần kết hợp một phép chọn với bài toán hoán vị không điểm cố định.

### Nhịp 32 — Chọn các điểm đúng
- Hình động: mô hình `rencontres` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn 2 trong 5 vị trí: C_2^5; Các vị trí ấy giữ nguyên; Phần còn lại gồm 3 vị trí
- Kết luận: Bước đầu chọn tập vị trí đúng, không sắp lại.
- Công thức Typst: `C_2^5=10`

Trước hết quyết định hai vị trí nào được giữ nguyên. Vì không quan tâm thứ tự chọn hai vị trí đúng, ta dùng tổ hợp chập hai của năm, được mười lựa chọn. Một khi đã chọn, hai phần tử ở những vị trí ấy được cố định. Ba phần tử còn lại bắt buộc phải hoán vị giữa ba chỗ của chúng theo cách không phần tử nào đứng đúng, nếu không sẽ xuất hiện thêm điểm cố định thứ ba.

### Nhịp 33 — Hoán vị phần còn lại
- Hình động: mô hình `rencontres` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Ba phần tử còn lại đều phải sai; D3 = 2 cách; Nhân với 10 lựa chọn phần đúng
- Kết luận: Hai bước độc lập sau khi đã cố định tập đúng.
- Công thức Typst: `C_2^5 D_3=10 cdot 2=20`

Với ba phần tử, có đúng hai hoán vị không điểm cố định: hai chu trình ba phần tử theo hai chiều. Vì mỗi lựa chọn tập hai vị trí đúng đều cho đúng hai cách sắp phần còn lại, số hoán vị có chính xác hai điểm cố định là mười nhân hai, bằng hai mươi. Hình động sẽ giữ hai thẻ màu xanh ở đúng vị trí, rồi cho ba thẻ màu tím xoay vòng để học sinh nhìn thấy cả hai cách.

### Nhịp 34 — Công thức rencontres
- Hình động: mô hình `rencontres` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn k điểm cố định trong n; Hoán vị n−k điểm còn lại không cố định; Nhân số cách hai công đoạn
- Kết luận: Công thức chính xác k điểm cố định.
- Công thức Typst: `R_(n,k)=C_k^n D_(n-k)`

Tổng quát, số hoán vị n phần tử có chính xác k điểm cố định bằng số cách chọn tập k điểm đúng nhân số hoán vị không điểm cố định của n trừ k phần tử còn lại. Công thức này thường được gọi là số rencontres. Nó giúp giải rất nhanh những câu hỏi kiểu có đúng k học sinh nhận đúng đồ của mình hoặc đúng k người được phân công việc trùng số thứ tự. Điều kiện chính xác phải được giữ ở cả hai bước.

### Nhịp 35 — Đếm các trường hợp 0,1,2,3,4,5
- Hình động: mô hình `rencontres` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: D5=44 không ai đúng; Đúng 1 điểm: 45; đúng 2: 20; Các trường hợp khác hoàn tất 120
- Kết luận: Phân bố số điểm đúng phải cộng thành 5!.
- Công thức Typst: `44+45+20+10+0+1=120`

Với năm phần tử, số hoán vị có không, một, hai, ba, bốn và năm điểm cố định lần lượt là bốn mươi bốn, bốn mươi lăm, hai mươi, mười, không và một. Cộng tất cả bằng một trăm hai mươi, đúng bằng năm giai thừa. Vì không thể có đúng bốn điểm cố định mà điểm thứ năm lại sai, ô tương ứng phải bằng không. Phân bố này là một kiểm tra rất tốt cho cả công thức và lời giải.

### Nhịp 36 — Kỳ vọng một điểm đúng
- Hình động: mô hình `rencontres` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Gọi Xi = 1 nếu vị trí i đúng; Xác suất Xi bằng 1/n; Tổng kỳ vọng bằng 1
- Kết luận: Kỳ vọng số điểm cố định luôn bằng 1.
- Công thức Typst: `E(X)=sum_(i=1)^n 1/n=1`

Một kết quả thú vị là trong hoán vị ngẫu nhiên của n phần tử, số điểm cố định trung bình luôn bằng một, bất kể n lớn đến đâu. Đặt biến chỉ báo X i bằng một nếu phần tử i đứng đúng chỗ và bằng không nếu không. Xác suất của mỗi sự kiện đúng chỗ là một chia n. Nhờ tính tuyến tính của kỳ vọng, tổng kỳ vọng bằng n nhân một chia n, tức bằng một. Đây là một công thức vừa lạ vừa đẹp, không đòi hỏi tính toàn bộ phân bố.

## 07 · TRUY HỒI ĐA THỨC XE

### Nhịp 37 — Đếm xe bằng truy hồi
- Hình động: mô hình `rook_recurrence` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Một bàn cờ cấm B bất kỳ; Chọn một ô đỏ p; Chia: đặt xe ở p hoặc không
- Kết luận: Chia hai trường hợp rời nhau ngay ở một ô.
- Công thức Typst: `R_B(x)=R_(B-p)(x)+xR_(B-r-c)(x)`

Khi bàn cờ có nhiều ô cấm phức tạp, việc liệt kê trực tiếp mọi cách đặt xe không ăn nhau cũng trở nên vất vả. Ta có thể sử dụng một truy hồi đơn giản bằng cách chọn một ô đỏ p bất kỳ. Mọi cách đặt xe hợp lệ rơi vào đúng một trong hai trường hợp: không đặt xe tại p, hoặc có đặt xe tại p. Đây là một lần áp dụng quy tắc cộng cho hai họ cấu hình không trùng nhau.

### Nhịp 38 — Nhánh không chọn ô p
- Hình động: mô hình `rook_recurrence` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Xóa riêng ô p khỏi tập ô đỏ; Các ô cấm khác vẫn giữ nguyên; Số quân xe không đổi
- Kết luận: Không chọn p cho đa thức R của B bỏ p.
- Công thức Typst: `R_(B-p)(x)`

Nếu một cấu hình không đặt quân tại ô p, ta chỉ cần xem p như ô không được chọn nữa. Tất cả các ô đỏ còn lại của bàn cờ vẫn sẵn có. Số quân xe trong cấu hình không thay đổi. Do đó đa thức đếm của nhánh này chính là đa thức xe của bảng B sau khi xóa riêng ô p khỏi danh sách ô được phép đặt xe, chứ không phải xóa cả hàng hay cả cột của p.

### Nhịp 39 — Nhánh có chọn ô p
- Hình động: mô hình `rook_recurrence` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Đã dùng một quân xe; Xóa cả hàng và cột chứa p; Hệ số nhân thêm x
- Kết luận: Chọn p khiến hàng và cột của nó bị khóa.
- Công thức Typst: `xR_(B-r-c)(x)`

Nếu có đặt xe ở ô p, toàn bộ hàng và cột chứa p không thể có xe nào khác. Ta xóa hàng và cột ấy khỏi bài toán còn lại, đồng thời ghi nhận đã đặt sẵn một quân xe bằng cách nhân với x. Phần còn lại chính là một bàn cờ cấm nhỏ hơn với các ô chưa bị xung đột. Ghép hai nhánh cho một công thức truy hồi tính đa thức xe rất hiệu quả.

### Nhịp 40 — Điều kiện dừng
- Hình động: mô hình `rook_recurrence` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Bàn cờ không có ô đỏ: R=1; Không đủ hàng/cột thì hệ số cao bằng 0; Có thể dùng nhớ trạng thái để tăng tốc
- Kết luận: Truy hồi dừng khi không còn ô cấm.
- Công thức Typst: `R_empty(x)=1`

Khi không còn ô đỏ, chỉ có cách đặt không quân xe, nên đa thức bằng một. Đây là điều kiện dừng cho thuật toán đệ quy. Với bàn cờ lớn, những bàn con giống nhau có thể xuất hiện ở nhiều nhánh; ta lưu kết quả để tránh tính lại. Lúc đó đa thức xe kết nối trực tiếp với quy hoạch động vừa học trong Video 22. Điểm khác là trạng thái bây giờ lưu cả một dãy hệ số, không chỉ một số cách.

### Nhịp 41 — Thử truy hồi cho bảng 4×4
- Hình động: mô hình `rook_recurrence` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn ô (A,1) trong bảng 5 ô cấm; Tách thành hai bàn con; Khôi phục hệ số 1,5,8,5,1
- Kết luận: Truy hồi và liệt kê phải cho cùng đa thức.
- Công thức Typst: `R(x)=1+5x+8x^2+5x^3+x^4`

Hãy áp dụng hai nhánh vào ô A một của bảng bốn nhân bốn đã xét. Nhánh không chọn giữ bốn ô cấm khác, còn nhánh chọn phải loại cả hàng A lẫn cột một. Khi cộng hai đa thức của hai bảng con, các hệ số lần lượt trở lại một, năm, tám, năm, một. Phương pháp đệ quy này có ưu điểm không phải vẽ mọi tổ hợp các quân xe, và rất phù hợp để máy tính kiểm chứng một lời giải tay.

### Nhịp 42 — Từ đa thức đến lời giải
- Hình động: mô hình `rook_recurrence` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Tính r0, r1, ..., rn; Chèn hệ số vào tổng xen dấu; Không quên (n−k)!
- Kết luận: Đếm xe chỉ là bước đầu của phép đếm hoán vị.
- Công thức Typst: `N=sum_(k=0)^n (-1)^k r_k (n-k)!`

Cuối cùng cần phân biệt rõ mục đích: đa thức xe giúp ta đếm các giao của điều kiện cấm, còn nguyên lý bao hàm và loại trừ mới biến chúng thành số hoán vị được phép. Nếu dừng tại đa thức, bài toán phân công vẫn chưa giải xong. Luôn nhân hệ số r k với giai thừa số hàng chưa cố định, đặt dấu xen kẽ và cộng đầy đủ các số hạng. Với công thức ấy, ta sẵn sàng xử lý thử thách cuối cùng.

## 08 · OLYMPIC: HAI VỊ TRÍ CẤM MỖI NGƯỜI

### Nhịp 43 — Năm người, hai vị trí cấm
- Hình động: mô hình `menage` ở trạng thái 1/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: 5 người A, B, C, D, E; Người i cấm ghế i và ghế kế theo; Ghế được đánh số, không đồng nhất khi quay
- Kết luận: Đếm hoán vị của 5 ghế có 10 ô cấm.
- Công thức Typst: `N=13`

Bài cuối có năm người và năm chiếc ghế được đánh số cố định từ một đến năm. Mỗi người không được ngồi ghế mang cùng số thứ tự, cũng không được ngồi ở ghế ngay sau nó khi đếm vòng từ năm trở lại một. Từng người có đúng hai ghế bị cấm. Cần nhấn mạnh đây là năm ghế có nhãn, nên quay toàn bộ người sang ghế khác tạo một kết quả mới, không chia cho số phép quay.

### Nhịp 44 — Bàn cờ mười ô đỏ
- Hình động: mô hình `menage` ở trạng thái 2/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Mỗi hàng có hai ô cấm; Tổng cộng 10 ô đỏ; Các ô đỏ tạo một chu trình trên bàn
- Kết luận: Hình dạng tập ô cấm quyết định hệ số r_k.
- Công thức Typst: `r_1=10`

Trên bảng năm nhân năm, đánh đỏ hai ô ở mỗi hàng: một ô đường chéo và một ô ngay bên phải, với hàng cuối nối về cột đầu. Có mười ô đỏ, vì vậy r một bằng mười. Nhưng các ô cấm không độc lập: nhiều cặp nằm chung hàng hoặc cột. Ta không thể coi mười ô đỏ là mười điều kiện hoàn toàn tương thích rồi lấy trực tiếp các hệ số tổ hợp của mười.

### Nhịp 45 — Đếm hai quân
- Hình động: mô hình `menage` ở trạng thái 3/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Chọn hai ô trong 10: 45 cặp; Có 5 cặp trùng hàng; Có 5 cặp trùng cột
- Kết luận: Loại cặp xe ăn nhau.
- Công thức Typst: `r_2=45-5-5=35`

Chọn hai trong mười ô đỏ sẽ có bốn mươi lăm cặp. Có năm cặp chung hàng, bởi mỗi hàng chứa đúng hai ô đỏ. Tương tự có năm cặp chung cột. Những cặp không hợp lệ ấy không bị giao nhau trong chính bài đếm cặp, vì hai ô khác nhau không thể đồng thời chung cả hàng lẫn cột. Trừ đi mười cặp xung đột, ta được ba mươi lăm cách đặt hai quân xe không ăn nhau.

### Nhịp 46 — Các hệ số cao
- Hình động: mô hình `menage` ở trạng thái 4/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: r3=50 và r4=25; r5=2 cách đặt đủ 5 xe; Có thể đếm bằng truy hồi
- Kết luận: R(x) chứa sáu hệ số cần thiết.
- Công thức Typst: `R(x)=1+10x+35x^2+50x^3+25x^4+2x^5`

Khi tăng số quân xe, các nhóm ô đỏ không xung đột được đếm bằng phép chia trường hợp hoặc truy hồi ở chương trước. Ta thu được năm mươi cách đặt ba xe, hai mươi lăm cách đặt bốn xe, và chỉ hai cách đặt đủ năm xe. Hai cách cuối tương ứng với hai tập năm ô tạo thành hai đường hoán vị cấm hoàn chỉnh. Tất cả hệ số một, mười, ba mươi lăm, năm mươi, hai mươi lăm, hai tạo nên đa thức xe đặc trưng của bài toán này.

### Nhịp 47 — Bao hàm–loại trừ cuối
- Hình động: mô hình `menage` ở trạng thái 5/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Số giai thừa còn lại theo số xe; Dấu xen kẽ + − + − + −; Kết quả 13 cách hợp lệ
- Kết luận: Số hoán vị hợp lệ bằng tổng xen dấu.
- Công thức Typst: `120-240+210-100+25-2=13`

Thay sáu hệ số vào tổng bao hàm và loại trừ: bắt đầu từ năm giai thừa bằng một trăm hai mươi, trừ mười nhân bốn giai thừa, cộng ba mươi lăm nhân ba giai thừa, trừ năm mươi nhân hai giai thừa, cộng hai mươi lăm và trừ hai. Sau các phép rút gọn, kết quả là mười ba cách phân công. Một chương trình duyệt đủ một trăm hai mươi hoán vị cũng cho đúng mười ba, nhưng chứng minh toán học nằm ở đa thức xe.

### Nhịp 48 — Thông điệp của Video 23
- Hình động: mô hình `menage` ở trạng thái 6/6, đối tượng/ô cấm được đánh dấu.
- Lập luận: Đặt đúng các biến cố cấm; Đếm giao bằng quân xe không ăn nhau; Chứng minh bằng tổng xen dấu
- Kết luận: Đa thức xe kết nối hình học bàn cờ và tổ hợp.
- Công thức Typst: `N=sum_(k=0)^n (-1)^k r_k (n-k)!`

Điểm kết thúc của video không phải chỉ là con số mười ba. Điều đáng giữ lại là một chiến lược tổng quát: mã hóa phép phân công thành bàn cờ, chuyển từng cặp bị cấm thành ô đỏ, đếm những bộ ô đỏ cùng tồn tại bằng đa thức xe, rồi dùng bao hàm và loại trừ để suy ra kết quả được phép. Chiến lược này giải được cả những bài hoán vị có bảng cấm rất phức tạp trong các kỳ thi học sinh giỏi và Olympic.
