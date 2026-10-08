# COMB25 V2 · STORYBOARD CHI TIẾT 48 NHỊP

Thời lượng nền: 24:53.

## CHƯƠNG 01. 01 · VÒNG HẠT VÀ BỔ ĐỀ BURNSIDE

### Nhịp 01 – Tại sao 64 chưa phải đáp án?
**Cột trái:** mô hình trực quan `burnside` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Sáu hạt, mỗi hạt hai màu; Có 2⁶ = 64 dãy có đánh vị trí; Đổi vị trí bắt đầu có thể trùng.
**Công thức Typst:** `2^6=64`.
**Kết luận:** Ta phải đếm các quỹ đạo, không đếm nhãn.

**Lời giảng:** Nếu tô sáu vị trí trên vòng tròn bằng hai màu, bảng nhị phân chứa sáu mươi tư dãy. Nhưng một vòng hạt không có vị trí bắt đầu cố định. Xoay vòng đi một hạt có thể tạo cùng hình thật. Vì thế sáu mươi tư mới là số dãy có nhãn, không phải số mẫu vòng phân biệt. Chúng ta cần một quy tắc đếm các lớp tương đương.

### Nhịp 02 – Một quỹ đạo là gì?
**Cột trái:** mô hình trực quan `burnside` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Xoay 0,1,...,5 bước; Mỗi phép quay tác động lên cách tô; Các ảnh của cùng mẫu thuộc một lớp.
**Công thức Typst:** `G=C_6`.
**Kết luận:** Không phải quỹ đạo nào cũng có sáu phần tử.

**Lời giảng:** Hãy lấy một mẫu gồm ba hạt tối và ba hạt sáng, rồi quay lần lượt một đến năm nấc. Tất cả hình trùng nhau dưới phép quay được gom vào một quỹ đạo. Với mẫu bất đối xứng, quỹ đạo có sáu phần tử; nhưng mẫu lặp đều có thể có ít hơn. Vì kích thước các quỹ đạo khác nhau, phép chia đơn giản sáu mươi tư cho sáu là sai.

### Nhịp 03 – Đếm bằng số cấu hình bất biến
**Cột trái:** mô hình trực quan `burnside` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** Phép quay g giữ nguyên một số cách tô; Kí hiệu Fix(g) là tập được giữ nguyên; Lấy trung bình theo sáu phép quay.
**Công thức Typst:** `N=frac(1,6)sum_(g in G)|Fix(g)|`.
**Kết luận:** Bổ đề Burnside đếm số lớp quỹ đạo.

**Lời giảng:** Burnside đưa ra một đổi góc nhìn bất ngờ. Thay vì cố dựng từng quỹ đạo, ta lấy tất cả phép quay, hỏi mỗi phép quay giữ nguyên bao nhiêu cách tô rồi lấy trung bình. Dấu Fix nghĩa là cấu hình bất biến: thực hiện phép quay mà tất cả màu tại các vị trí vẫn khớp như ban đầu. Đây chính là công cụ nền tảng để xử lý đối xứng.

### Nhịp 04 – Số chu trình quyết định số cách
**Cột trái:** mô hình trực quan `burnside` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** Phép quay tách sáu vị trí thành chu trình; Mỗi chu trình phải đồng màu; Nếu có c chu trình: 2ᶜ cách.
**Công thức Typst:** `|Fix(g)|=2^(c(g))`.
**Kết luận:** Hình đối xứng được mã hóa bằng chu trình.

**Lời giảng:** Khi một phép quay chuyển vị trí thứ nhất sang thứ tư, màu ở hai vị trí ấy phải bằng nhau để hình không đổi. Điều kiện lan truyền khắp từng chu trình. Mỗi chu trình được chọn một trong hai màu một cách độc lập, nên số cách tô bất biến bằng hai lũy thừa số chu trình. Manim sẽ tô sáng từng chu trình để chứng minh điều này bằng mắt.

### Nhịp 05 – Phân loại sáu phép quay
**Cột trái:** mô hình trực quan `burnside` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** Quay 0: 2⁶ = 64; Quay 1,5: mỗi phép 2 cách; Quay 2,4: 4 cách; quay 3: 8.
**Công thức Typst:** `64+2+4+8+4+2=84`.
**Kết luận:** Phải tính từng phép, không chỉ mỗi góc khác nhau.

**Lời giảng:** Phép đồng nhất có sáu chu trình một phần tử nên giữ toàn bộ sáu mươi tư cách tô. Quay một hoặc năm bước nối tất cả vị trí thành một chu trình nên chỉ còn hai cách. Quay hai hoặc bốn bước cho hai chu trình, còn quay ba bước cho ba chu trình. Cộng lần lượt ta nhận tám mươi tư, là tổng số cấu hình bất biến của sáu phép quay.

### Nhịp 06 – Kết luận và tự kiểm chứng
**Cột trái:** mô hình trực quan `burnside` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Tổng bất biến = 84; Chia 6 phép quay được 14; Liệt kê đại diện cũng được 14.
**Công thức Typst:** `N=frac(84,6)=14`.
**Kết luận:** Burnside chính xác, kể cả quỹ đạo ngắn.

**Lời giảng:** Kết quả có mười bốn mẫu vòng hạt hai màu nếu hai mẫu chỉ khác phép quay được coi như nhau. Để kiểm tra, ta có thể sinh sáu mươi tư dãy, chuẩn hóa mỗi dãy thành đại diện nhỏ nhất trong sáu phép quay rồi đếm các đại diện khác nhau. Cách liệt kê độc lập cũng cho mười bốn. Đây là một phép thử mạnh cho công thức vừa chứng minh.

## CHƯƠNG 02. 02 · THÊM ĐỐI XỨNG GƯƠNG: NHÓM DIHEDRAL

### Nhịp 07 – Lật gương có được xem là trùng?
**Cột trái:** mô hình trực quan `bracelet` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Vòng cổ xoay được; Vòng tay có thể lật mặt theo mô hình; Phải đọc đúng quy ước đề bài.
**Công thức Typst:** `D_6={r^j,s r^j}`.
**Kết luận:** Nhóm đối xứng phụ thuộc phép được cho phép.

**Lời giảng:** Đây là điểm mấu chốt của nhiều bài toán vòng tròn. Nếu một mặt sản phẩm được đánh dấu và không được lật, ta chỉ xét phép quay. Nhưng nếu lật hình mà mẫu vẫn coi là một, ta phải thêm các phép phản chiếu. Khi ấy nhóm đối xứng gồm sáu phép quay và sáu phép phản chiếu, thường ký hiệu là nhóm dihedral D sáu.

### Nhịp 08 – Sáu phép phản chiếu
**Cột trái:** mô hình trực quan `bracelet` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Ba trục đi qua cặp đỉnh đối diện; Ba trục đi qua cặp cạnh đối diện; Hai kiểu có số chu trình khác nhau.
**Công thức Typst:** `|D_6|=12`.
**Kết luận:** Không được cộng tất cả ảnh gương như nhau.

**Lời giảng:** Với lục giác đều, ta có ba trục đối xứng đi qua hai đỉnh đối diện và ba trục đi qua trung điểm hai cạnh đối diện. Các vị trí được cố định trên trục làm thay đổi số chu trình của phép phản chiếu. Vì vậy hai loại trục có số cách tô bất biến khác nhau. Video sẽ xoay đường gương qua từng loại để học sinh thấy chỗ nào đứng yên và chỗ nào đổi chỗ.

### Nhịp 09 – Trục qua hai đỉnh
**Cột trái:** mô hình trực quan `bracelet` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** Có hai vị trí đứng yên; Bốn vị trí ghép thành hai cặp; Tổng cộng bốn chu trình: 2⁴.
**Công thức Typst:** `2^4=16`.
**Kết luận:** Mỗi trục loại này giữ 16 cách tô.

**Lời giảng:** Một đường gương đi qua hai đỉnh đối diện giữ nguyên đúng hai vị trí nằm trên trục. Bốn vị trí còn lại đổi chỗ thành hai cặp, tức chúng phải cùng màu theo từng cặp. Vậy phép phản chiếu có tổng cộng bốn chu trình và giữ nguyên mười sáu cách tô. Có ba trục loại này, nên đóng góp tất cả bốn mươi tám.

### Nhịp 10 – Trục qua hai cạnh
**Cột trái:** mô hình trực quan `bracelet` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** Không có đỉnh nào đứng yên; Sáu vị trí ghép thành ba cặp; Ba chu trình: 2³ = 8.
**Công thức Typst:** `2^3=8`.
**Kết luận:** Mỗi trục loại này giữ tám cách tô.

**Lời giảng:** Nếu trục gương đi qua trung điểm hai cạnh đối diện, không có hạt nào nằm chính trên trục. Cả sáu hạt ghép thành ba cặp đối xứng, nên ta được ba chu trình. Khi màu ở từng cặp phải giống nhau, sẽ có hai mũ ba bằng tám cấu hình bất biến. Có ba trục như vậy, tổng đóng góp là hai mươi bốn.

### Nhịp 11 – Trung bình trên mười hai phép
**Cột trái:** mô hình trực quan `bracelet` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** Nhóm quay đóng góp 84; Sáu phản chiếu đóng góp 48 + 24; Tổng 156, chia 12 phép đối xứng.
**Công thức Typst:** `N=frac(84+48+24,12)=13`.
**Kết luận:** Số vòng tay hai màu là 13.

**Lời giảng:** Bây giờ ta áp dụng chính bổ đề Burnside nhưng với nhóm gồm mười hai phép biến đổi. Các phép quay đã có tổng số cố định bằng tám mươi tư; hai họ phản chiếu lần lượt thêm bốn mươi tám và hai mươi bốn. Lấy tổng chia mười hai, ta được mười ba mẫu. Có đúng một cặp mẫu vòng cổ bị gộp thêm khi cho phép lật gương.

### Nhịp 12 – Đặt hai đáp số cạnh nhau
**Cột trái:** mô hình trực quan `bracelet` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Chỉ quay: 14 mẫu; Quay và phản chiếu: 13 mẫu; Sự khác nhau đến từ nhóm tác động.
**Công thức Typst:** `N_(quay)=14,quad N_(guong)=13`.
**Kết luận:** Cùng vật liệu, khác quy ước, khác kết quả.

**Lời giảng:** Qua hai chương đầu, ta rút ra một nguyên tắc phương pháp luận: trước khi dùng Burnside, nhất thiết xác định nhóm phép biến đổi hợp lệ. Không thể lấy công thức vòng cổ cho vòng tay hoặc ngược lại mà không đọc kỹ yêu cầu. Trong các bài Olympic, việc nhận ra nhóm đối xứng thường khó và quan trọng hơn phép tính cuối cùng.

## CHƯƠNG 03. 03 · CỐ ĐỊNH SỐ HẠT MỖI MÀU

### Nhịp 13 – Một ràng buộc mới
**Cột trái:** mô hình trực quan `fixedweight` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Sáu hạt có đúng ba hạt đen; Chỉ có C₃⁶ = 20 dãy có nhãn; Mẫu vòng chỉ xét tương đương theo quay.
**Công thức Typst:** `C_3^6=20`.
**Kết luận:** Không thể dùng nguyên 2ᶜ nữa.

**Lời giảng:** Nếu đề yêu cầu đúng ba hạt đen và ba hạt trắng, ta không còn được tùy ý chọn màu cho từng chu trình. Điều kiện tổng số hạt đen làm các chu trình phụ thuộc nhau. Trước khi xét đối xứng, số dãy tuyến tính có nhãn là tổ hợp chập ba của sáu, bằng hai mươi. Hãy xem Burnside có thể xử lý ràng buộc này như thế nào.

### Nhịp 14 – Phép quay 0
**Cột trái:** mô hình trực quan `fixedweight` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Mọi cách tô đủ 3 đen đều bất biến; Có 20 cấu hình; Đồng nhất không áp thêm điều kiện.
**Công thức Typst:** `|Fix(e)|=20`.
**Kết luận:** Đóng góp của đồng nhất là 20.

**Lời giảng:** Phép đồng nhất không làm thay đổi bất cứ vị trí nào nên tất cả hai mươi cách tô có đúng ba hạt đen đều được giữ nguyên. Đây là hạng tử lớn nhất trong tổng Burnside. Cần ghi nhớ rằng ta đang đếm số cách tô thỏa cả điều kiện số lượng màu lẫn điều kiện bất biến theo phép quay đang xét, chứ không phải chỉ điều kiện đối xứng.

### Nhịp 15 – Quay hai và bốn bước
**Cột trái:** mô hình trực quan `fixedweight` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** Hai chu trình, mỗi chu trình dài 3; Chọn một chu trình làm đen; Mỗi phép quay có 2 cấu hình cố định.
**Công thức Typst:** `|Fix(r^2)|=|Fix(r^4)|=2`.
**Kết luận:** Độ dài chu trình phải cộng thành 3.

**Lời giảng:** Khi quay hai bước, sáu hạt phân thành hai chu trình, mỗi chu trình chứa ba hạt. Muốn có đúng ba hạt đen, ta chọn đúng một trong hai chu trình tô đen, chu trình còn lại tô trắng. Có hai cách. Quay bốn bước cho cùng cấu trúc chu trình, cũng có hai cách. Đây là minh họa vì sao số cách tô cố định cần xét đa thức trọng số theo độ dài chu trình.

### Nhịp 16 – Những phép quay còn lại
**Cột trái:** mô hình trực quan `fixedweight` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** Quay 1 hoặc 5: một chu trình dài 6; Quay 3: ba chu trình dài 2; Không tạo được tổng trọng số đen bằng 3.
**Công thức Typst:** `|Fix(r)|=|Fix(r^3)|=|Fix(r^5)|=0`.
**Kết luận:** Các phép này góp 0.

**Lời giảng:** Quay một hay năm bước nối toàn bộ sáu vị trí, buộc tất cả hạt cùng màu; điều kiện đúng ba đen bị phá. Quay ba bước ghép hạt thành ba cặp, nên số hạt đen luôn là số chẵn, không thể bằng ba. Vì vậy ba phép quay ấy không giữ cấu hình hợp lệ nào. Số không ở đây là một hệ quả của cấu trúc chu trình, không phải do xóa tùy tiện trường hợp.

### Nhịp 17 – Burnside có trọng số
**Cột trái:** mô hình trực quan `fixedweight` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** Tổng cố định là 20 + 2 + 2; Chia cho 6 phép quay; Có 4 mẫu vòng với đúng 3 hạt đen.
**Công thức Typst:** `N=frac(20+2+2,6)=4`.
**Kết luận:** Chọn hệ số là phép lọc số lượng màu.

**Lời giảng:** Cộng số cấu hình cố định của sáu phép quay rồi chia cho sáu ta thu được bốn mẫu vòng hạt chứa đúng ba hạt đen. So với mười bốn mẫu khi không ràng buộc màu, kết quả nhỏ hơn là hợp lý. Bằng phép sinh tất cả hai mươi dãy chứa ba số một và gom theo phép quay, ta cũng thu được bốn quỹ đạo.

### Nhịp 18 – Chốt kỹ thuật hệ số
**Cột trái:** mô hình trực quan `fixedweight` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Chu trình độ dài d sinh 1 + zᵈ; Nhân các nhân tử theo chu trình; Hệ số z³ đếm đúng 3 hạt đen.
**Công thức Typst:** `[z^3]prod_(j)(1+z^(d_j))`.
**Kết luận:** Đây là cầu nối trực tiếp đến Pólya.

**Lời giảng:** Thay vì tự liệt kê từng điều kiện, ta gán cho một chu trình dài d hai lựa chọn: sơn trắng đóng góp một, sơn đen đóng góp z mũ d. Nhân trên các chu trình rồi lấy hệ số của z mũ ba sẽ cho đúng số cấu hình có ba hạt đen. Kỹ thuật lấy hệ số này nối kiến thức hàm sinh ở tập hai mươi mốt với định lý Pólya ở chương tới.

## CHƯƠNG 04. 04 · ĐỊNH LÝ PÓLYA VÀ ĐA THỨC CHU TRÌNH

### Nhịp 19 – Đếm mẫu tô hình vuông
**Cột trái:** mô hình trực quan `polya` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Bốn đỉnh, mỗi đỉnh ba màu; Có 3⁴ = 81 cách tô có nhãn; Các phép quay có thể cho cùng mẫu.
**Công thức Typst:** `3^4=81`.
**Kết luận:** Pólya tổ chức Burnside bằng chu trình.

**Lời giảng:** Xét bốn đỉnh của một hình vuông, mỗi đỉnh có thể chọn một trong ba màu. Nếu đánh số bốn đỉnh, có tám mươi mốt cách tô. Nhưng khi phép quay hình vuông được xem là giữ nguyên mẫu, nhiều dãy màu phải gộp lại. Burnside vẫn sử dụng được, song ta muốn một ký pháp ngắn gọn hơn để ghi nhớ số chu trình của mỗi loại phép quay.

### Nhịp 20 – Bốn phép quay của hình vuông
**Cột trái:** mô hình trực quan `polya` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Quay 0: bốn chu trình; Quay 180°: hai chu trình; Quay 90° và 270°: một chu trình.
**Công thức Typst:** `3^4+3^2+2 cdot 3=96`.
**Kết luận:** Mỗi số chu trình c đóng góp 3ᶜ.

**Lời giảng:** Phép không quay để lại bốn đỉnh độc lập, có ba mũ bốn cách tô bất biến. Quay nửa vòng ghép chúng thành hai cặp nên có ba bình phương cách. Quay một phần tư hoặc ba phần tư vòng buộc cả bốn đỉnh cùng màu, mỗi phép chỉ giữ ba cấu hình. Tổng số cấu hình bất biến theo bốn phép quay là chín mươi sáu.

### Nhịp 21 – Hai mươi bốn mẫu quay
**Cột trái:** mô hình trực quan `polya` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** Tổng số bất biến = 96; Chia cho bốn phần tử của nhóm C₄; Còn đúng 24 mẫu.
**Công thức Typst:** `frac(3^4+3^2+2 cdot 3,4)=24`.
**Kết luận:** Đối chiếu bằng liệt kê 81 cách tô.

**Lời giảng:** Sau khi lấy trung bình, chín mươi sáu chia bốn cho hai mươi bốn mẫu tô ba màu trên bốn đỉnh hình vuông, khi chỉ đồng nhất các phép quay. Để kiểm tra, ta liệt kê toàn bộ tám mươi mốt cách tô có nhãn, tìm đại diện chuẩn dưới bốn phép quay và đếm số đại diện phân biệt. Kết quả vẫn là hai mươi bốn.

### Nhịp 22 – Đa thức chu trình
**Cột trái:** mô hình trực quan `polya` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** Mỗi chu trình độ dài j gán aⱼ; Lấy trung bình các tích chu trình; Nhận đa thức chỉ số chu trình Z(G).
**Công thức Typst:** `Z(C_4)=frac(a_1^4+a_2^2+2a_4,4)`.
**Kết luận:** Thay aⱼ = q cho q màu độc lập.

**Lời giảng:** Bây giờ ta đặt biến a chỉ số một cho chu trình dài một, a chỉ số hai cho chu trình dài hai, và tương tự. Mỗi phép quay đóng góp tích những biến tương ứng với cấu trúc chu trình của nó. Trung bình các tích ấy tạo đa thức chỉ số chu trình. Khi thay mọi a chỉ số j bởi cùng số màu q, đa thức cho số quỹ đạo tô màu. Đó là dạng cơ bản của định lý Pólya.

### Nhịp 23 – Nếu tính cả phản chiếu
**Cột trái:** mô hình trực quan `polya` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** Nhóm D₄ có tám phép; Các kiểu chu trình bổ sung từ trục gương; Đa thức mới cho 21 mẫu.
**Công thức Typst:** `Z(D_4)=frac(a_1^4+2a_1^2a_2+3a_2^2+2a_4,8)`.
**Kết luận:** Không chỉ thay mẫu số; phải thêm biến đổi.

**Lời giảng:** Nếu cho phép lật gương hình vuông, nhóm tăng từ bốn lên tám phép. Bốn phép phản chiếu gồm hai loại: qua đỉnh và qua cạnh; các chu trình mới phải được cộng đầy đủ vào đa thức. Thay số màu bằng ba sẽ cho kết quả hai mươi mốt mẫu, khác với hai mươi bốn khi chỉ xoay. Một lần nữa nhóm tác động phải được xác định trước phép tính.

### Nhịp 24 – So sánh và nối tiếp
**Cột trái:** mô hình trực quan `polya` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Ba màu, quay: 24 mẫu; Ba màu, cả gương: 21 mẫu; Một công thức xử lý rất nhiều màu.
**Công thức Typst:** `Z(C_4)(3)=24,quad Z(D_4)(3)=21`.
**Kết luận:** Pólya = Burnside được đóng gói bằng chu trình.

**Lời giảng:** Giá trị lớn nhất của Pólya không phải ở việc giải một ví dụ hình vuông. Một khi biết chỉ số chu trình của nhóm, ta có thể thay hai, ba hay mười màu vào cùng biểu thức, hoặc thay những hàm sinh màu có trọng số để áp thêm điều kiện. Từ một bài đếm hình học, ta tạo thành công cụ đại số có thể tái sử dụng.

## CHƯƠNG 05. 05 · BỘ LỌC CĂN ĐƠN VỊ

### Nhịp 25 – Một tổng tổ hợp kỳ lạ
**Cột trái:** mô hình trực quan `roots` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Xét C₀⁹ + C₃⁹ + C₆⁹ + C₉⁹; Ta chỉ lấy các chỉ số chia hết cho ba; Đếm trực tiếp được 170.
**Công thức Typst:** `S=sum_(k equiv 0 mod 3) C_k^9`.
**Kết luận:** Cần lọc chỉ số theo phần dư, không theo vị trí.

**Lời giảng:** Tưởng tượng ta muốn cộng các hệ số tổ hợp chập không, ba, sáu và chín của chín. Cách liệt kê cho một cộng tám mươi tư cộng tám mươi tư cộng một bằng một trăm bảy mươi. Với n lớn hơn rất nhiều, tính từng số hạng trở nên bất tiện. Bộ lọc căn đơn vị giúp chọn đúng những bậc đồng dư mong muốn từ một nhị thức trong một lần thao tác.

### Nhịp 26 – Ba căn bậc ba của 1
**Cột trái:** mô hình trực quan `roots` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Lấy ω³ = 1 và ω khác 1; Ta có 1 + ω + ω² = 0; Mọi số mũ có phần dư 0,1,2.
**Công thức Typst:** `1+omega+omega^2=0`.
**Kết luận:** Tính trực giao làm biến mất bậc sai.

**Lời giảng:** Hãy lấy một căn bậc ba nguyên thủy của một trên đường tròn đơn vị, gọi là ô mê ga. Ba điểm một, ô mê ga và ô mê ga bình phương cách đều nhau. Tổng ba véc tơ bằng không. Khi nâng lũy thừa, số mũ chỉ quan trọng qua phần dư modulo ba. Hình học trên đường tròn phức trở thành công cụ lọc các hạng tử đại số.

### Nhịp 27 – Cơ chế lọc hệ số
**Cột trái:** mô hình trực quan `roots` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** Nếu 3 chia hết k: tổng ba lũy thừa là 3; Nếu không: tổng bằng 0; Chia ba để được hàm chỉ thị.
**Công thức Typst:** `frac(1+omega^k+omega^(2k),3)=[3 mid k]`.
**Kết luận:** Các hệ số sai phần dư bị khử chính xác.

**Lời giảng:** Ta xét biểu thức một cộng ô mê ga mũ k cộng ô mê ga mũ hai k, rồi chia ba. Nếu k là bội của ba, cả ba số hạng bằng một và giá trị nhận được bằng một. Nếu k không là bội của ba, ba căn đơn vị khác nhau xuất hiện và tổng bằng không. Đây là một hàm chỉ thị tuyệt đối chính xác chứ không phải một phép gần đúng số học.

### Nhịp 28 – Áp dụng vào Nhị thức Newton
**Cột trái:** mô hình trực quan `roots` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** (1+x)⁹ chứa mọi hệ số Cₖ⁹; Thay x lần lượt bằng 1,ω,ω²; Lấy trung bình ba khai triển.
**Công thức Typst:** `S=frac(2^9+(1+omega)^9+(1+omega^2)^9,3)`.
**Kết luận:** Chỉ còn các k là bội của ba.

**Lời giảng:** Trong khai triển một cộng x tất cả mũ chín, hệ số của x mũ k là tổ hợp chập k của chín. Để giữ lại những k chia hết cho ba, ta cộng ba giá trị của đa thức tại một, ô mê ga và ô mê ga bình phương, rồi chia ba. Tính trực giao của các căn đơn vị bảo đảm mọi hạng tử bậc sai bị triệt tiêu.

### Nhịp 29 – Tính tổng được 170
**Cột trái:** mô hình trực quan `roots` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** 1+ω = −ω² nên (1+ω)⁹ = −1; Tương tự (1+ω²)⁹ = −1; S = (512 − 1 − 1)/3.
**Công thức Typst:** `S=frac(512-1-1,3)=170`.
**Kết luận:** Nhìn số phức, thu kết quả nguyên rất đẹp.

**Lời giảng:** Vì một cộng ô mê ga bằng âm ô mê ga bình phương, nâng lũy thừa chín cho âm một. Biểu thức liên hợp của nó cũng cho âm một. Do đó tổng cần tìm bằng năm trăm mười hai trừ hai, chia ba, được một trăm bảy mươi. Kết quả khớp với phép cộng trực tiếp bốn hệ số. Cái hay nằm ở chỗ tổng nhiều hạng tử được nén thành ba giá trị đại số.

### Nhịp 30 – Tổng quát bộ lọc modulo m
**Cột trái:** mô hình trực quan `roots` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Chọn ζ là căn bậc m nguyên thủy; Lấy trung bình m giá trị F(ζʲ); Có thể lọc mọi lớp dư r.
**Công thức Typst:** `sum_(k equiv r mod m)a_k=frac(1,m)sum_(j=0)^(m-1)zeta^(-jr)F(zeta^j)`.
**Kết luận:** Một công cụ mạnh cho đề Olympic về chia hết.

**Lời giảng:** Khi thay ba bằng một số nguyên dương m, nguyên lý vẫn giữ nguyên. Ta lấy căn bậc m nguyên thủy và trung bình các giá trị hàm sinh tại các căn đơn vị, thêm trọng số để chọn phần dư r. Công thức này xuất hiện trong bài toán dãy số, tổng nhị thức và những điều kiện chia hết khó. Nó chính là biến đổi Fourier rời rạc ở dạng sơ cấp nhất.

## CHƯƠNG 06. 06 · PÓLYA CÓ RÀNG BUỘC MÀU

### Nhịp 31 – Tám hạt, đúng bốn đen
**Cột trái:** mô hình trực quan `weighted` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Có C₄⁸ = 70 dãy mang nhãn; Ta chỉ xét tương đương theo quay; Không thể thay q=2 máy móc.
**Công thức Typst:** `C_4^8=70`.
**Kết luận:** Cần dùng đa thức trọng số theo chu trình.

**Lời giảng:** Ta quay trở lại vòng hạt nhưng nâng độ khó. Có tám vị trí, đúng bốn hạt đen và bốn hạt trắng, các cách chỉ khác phép quay được xem là như nhau. Trước khi đồng nhất theo đối xứng, tổ hợp chập bốn của tám bằng bảy mươi. Đây là bài toán màu có số lượng cố định, nên thay mỗi biến chu trình bằng hai sẽ đếm cả các mẫu có sai số hạt đen.

### Nhịp 32 – Chu trình cho hàm sinh
**Cột trái:** mô hình trực quan `weighted` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Chu trình độ dài d: 1 + zᵈ; Tích trên các chu trình của phép quay; Lấy hệ số z⁴.
**Công thức Typst:** `[z^4]prod_(j)(1+z^(d_j))`.
**Kết luận:** Hệ số theo số hạt đen rồi mới trung bình.

**Lời giảng:** Đối với một chu trình dài d, mọi vị trí phải cùng màu để mẫu bất biến. Nếu chọn trắng, trọng số là một; nếu chọn đen, trọng số là z mũ d. Ta nhân các lựa chọn của từng chu trình rồi lấy hệ số z mũ bốn. Hệ số chính là số cấu hình bất biến của phép quay đang xét đồng thời có đúng bốn hạt đen.

### Nhịp 33 – Phép quay đồng nhất
**Cột trái:** mô hình trực quan `weighted` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** Tám chu trình dài một; Hàm sinh (1+z)⁸; Hệ số z⁴ bằng 70.
**Công thức Typst:** `[z^4](1+z)^8=70`.
**Kết luận:** Hạng tử thứ nhất luôn dễ nhất.

**Lời giảng:** Phép không quay giữ cả tám vị trí độc lập, mỗi vị trí tạo nhân tử một cộng z. Tích cho một cộng z mũ tám. Hệ số z mũ bốn là bảy mươi, đúng bằng số chọn bốn vị trí đen. Đây là bước kiểm chứng tự nhiên giữa ngôn ngữ hàm sinh và công thức tổ hợp thông thường.

### Nhịp 34 – Quay bốn vị trí
**Cột trái:** mô hình trực quan `weighted` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** Có bốn chu trình dài hai; Chọn hai trong bốn chu trình đen; Đóng góp C₂⁴ = 6.
**Công thức Typst:** `[z^4](1+z^2)^4=C_2^4=6`.
**Kết luận:** Sáu cấu hình cố định cho phép quay nửa vòng.

**Lời giảng:** Quay nửa vòng chia tám vị trí thành bốn cặp đối diện. Muốn có bốn hạt đen, ta chọn đúng hai trong bốn cặp cùng đen. Do đó có tổ hợp chập hai của bốn bằng sáu cấu hình bất biến. Học sinh có thể quan sát hai cặp hạt sáng và hai cặp hạt tối được tô nổi bật trong hoạt hình.

### Nhịp 35 – Quay hai hoặc sáu
**Cột trái:** mô hình trực quan `weighted` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** Mỗi phép có hai chu trình dài bốn; Chọn một chu trình đen; Mỗi phép đóng góp 2.
**Công thức Typst:** `[z^4](1+z^4)^2=2`.
**Kết luận:** Các phép quay khác không cho đủ bốn đen.

**Lời giảng:** Nếu quay hai hoặc sáu vị trí, vòng chia thành hai chu trình, mỗi chu trình dài bốn. Để chọn đủ bốn hạt đen, ta tô đen một chu trình và để chu trình còn lại trắng, có hai cách cho mỗi phép quay. Những phép quay một, ba, năm hoặc bảy vị trí nối thành một chu trình dài tám nên không thể có đúng bốn hạt đen. Vì thế chúng đóng góp bằng không.

### Nhịp 36 – Kết quả 10 mẫu
**Cột trái:** mô hình trực quan `weighted` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Tổng cố định 70 + 6 + 2 + 2; Trung bình trên tám phép quay; Có đúng 10 vòng phân biệt.
**Công thức Typst:** `N=frac(70+6+2+2,8)=10`.
**Kết luận:** Kết hợp Burnside với hàm sinh có trọng số.

**Lời giảng:** Tổng đóng góp của tám phép quay là tám mươi, chia tám ta được mười mẫu vòng hạt với đúng bốn hạt đen. Nếu cho phép lật gương, đáp số đổi thành tám, nhưng ở bài này chúng ta chỉ đồng nhất phép quay. Đây là bước kiểm tra quan trọng về quy ước đối xứng, và cũng là ví dụ trọn vẹn về việc áp dụng Pólya cùng hàm sinh.

## CHƯƠNG 07. 07 · NHẬN DIỆN CÔNG CỤ CHO BÀI CỰC KHÓ

### Nhịp 37 – Nhìn câu hỏi trước công thức
**Cột trái:** mô hình trực quan `synthesis` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Thứ tự quan trọng hay không?; Nhóm đối xứng có những phép nào?; Có số lượng màu cố định không?.
**Công thức Typst:** `N_(orbits)=frac(1,|G|)sum_(g in G)|Fix(g)|`.
**Kết luận:** Sơ đồ quyết định quan trọng hơn học thuộc.

**Lời giảng:** Một bài tổ hợp khó thường không nói trước phải dùng công thức nào. Ta cần phân loại đối tượng: đó là dãy được đánh số, vòng không đánh số, hay hình có thể lật? Tiếp đó phải nhận diện nhóm phép biến đổi thực sự và ràng buộc về số lượng màu. Chỉ khi ba câu hỏi ấy rõ ràng, công thức Burnside hay Pólya mới có thể áp dụng đúng.

### Nhịp 38 – Những lỗi dễ mắc
**Cột trái:** mô hình trực quan `synthesis` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Không được chia tổng cấu hình cho |G|; Không được gộp gương nếu đề cấm; Không được bỏ qua chu trình dài.
**Công thức Typst:** `|Orb(x)|=frac(|G|,|Stab(x)|)`.
**Kết luận:** Đếm số cố định đúng từng phép biến đổi.

**Lời giảng:** Sai lầm nổi bật là lấy tổng số cách tô rồi chia ngay cho số đối xứng. Công thức này chỉ đúng nếu mọi cấu hình có quỹ đạo cùng kích thước, điều hiếm gặp khi có hình đối xứng. Burnside xử lý chính xác bằng số phần tử bất biến. Một lỗi khác là tự thêm phép phản chiếu dù đề chỉ cho phép quay. Cuối cùng, đối với điều kiện số lượng màu, mọi chu trình phải giữ nguyên đồng màu.

### Nhịp 39 – Bài vòng cổ và vòng tay
**Cột trái:** mô hình trực quan `synthesis` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** 6 hạt hai màu: 14 hoặc 13; 8 hạt có 4 đen: 10 hoặc 8; Sự khác biệt đều do nhóm tác động.
**Công thức Typst:** `(14,13),quad(10,8)`.
**Kết luận:** Cùng dữ kiện màu chưa đủ để xác định đáp số.

**Lời giảng:** Hãy đối chiếu bốn kết quả từ các chương trước. Vòng sáu hạt hai màu cho mười bốn mẫu nếu chỉ quay và mười ba nếu cho cả lật. Với tám hạt có bốn màu đen, hai quy ước lần lượt cho mười và tám mẫu. Đó là một lời nhắc rất thực tế: số mẫu không chỉ phụ thuộc số hạt hay số màu, mà còn phụ thuộc điều kiện coi những hình nào là giống nhau.

### Nhịp 40 – Tổng hệ số từ căn đơn vị
**Cột trái:** mô hình trực quan `synthesis` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** Cần lọc số k theo modulo m?; Đặt đa thức F(x) chứa hệ số cần đếm; Áp bộ lọc căn đơn vị.
**Công thức Typst:** `S_r=frac(1,m)sum_(j=0)^(m-1)zeta^(-jr)F(zeta^j)`.
**Kết luận:** Đổi từ tổng tổ hợp sang giá trị hàm.

**Lời giảng:** Nếu bài cho một tổng hệ số nhị thức chỉ chạy qua các chỉ số cùng phần dư modulo một số nguyên, trực tiếp cộng từng hạng tử có thể rất dài. Hãy viết đa thức hay hàm sinh tạo ra những hệ số ấy, rồi dùng bộ lọc căn đơn vị để chọn phần dư. Phương pháp này không cần mô hình hình học đối xứng nhưng có cùng tư tưởng trung bình những tác động để giữ lại phần bất biến.

### Nhịp 41 – Từ đường tròn đến lập phương
**Cột trái:** mô hình trực quan `synthesis` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** Vòng hạt có nhóm quay Cₙ; Lập phương có 24 phép quay không gian; Phân loại theo chu trình trên sáu mặt.
**Công thức Typst:** `|G_(cube)|=24`.
**Kết luận:** Burnside mở rộng sang hình ba chiều.

**Lời giảng:** Ở vòng tròn ta đếm biến đổi của các vị trí xung quanh tâm. Với một khối lập phương, các phép quay trong không gian có thể hoán vị sáu mặt. Nhóm quay của khối có hai mươi bốn phần tử, lớn hơn rất nhiều so với bài vòng hạt. Nhưng tư tưởng không thay đổi: phân nhóm các phép quay theo cấu trúc chu trình, tính số cách tô bất biến và lấy trung bình.

### Nhịp 42 – Chuẩn bị bài kết thúc
**Cột trái:** mô hình trực quan `synthesis` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Sáu mặt, mỗi mặt ba màu; Chỉ cho phép quay, không phản chiếu; Hỏi có bao nhiêu mẫu tô khác nhau?.
**Công thức Typst:** `3^6=729`.
**Kết luận:** Bài Olympic cuối cùng của toàn Series.

**Lời giảng:** Bài cuối của hai mươi lăm tập sẽ kết hợp trực giác hình học, nhóm phép quay và công thức đếm cố định. Có sáu mặt lập phương, mỗi mặt chọn một trong ba màu; ba màu được xem là phân biệt. Chúng ta coi hai mẫu tương đương nếu phép quay cứng của khối đưa mẫu này đến mẫu kia, không tính đối xứng gương. Trước khi xét phép quay, số mẫu có nhãn là ba mũ sáu bằng bảy trăm hai mươi chín.

## CHƯƠNG 08. 08 · OLYMPIC: TÔ MÀU SÁU MẶT LẬP PHƯƠNG

### Nhịp 43 – Phân nhóm 24 phép quay
**Cột trái:** mô hình trực quan `cube` ở trạng thái 0, tô sáng yếu tố then chốt.
**Cột phải:** Một phép đồng nhất; Sáu quay 90°, ba quay 180° qua mặt; Tám quay 120° qua đỉnh, sáu quay 180° qua cạnh.
**Công thức Typst:** `1+6+3+8+6=24`.
**Kết luận:** Phải đủ 1 + 6 + 3 + 8 + 6 = 24.

**Lời giảng:** Khối lập phương có hai mươi bốn phép quay bảo toàn hướng. Ta chia thành năm nhóm theo trục và góc quay: đồng nhất, quay một phần tư vòng qua tâm hai mặt đối diện, quay nửa vòng cùng trục mặt, quay một phần ba vòng qua hai đỉnh đối diện, và quay nửa vòng qua trung điểm hai cạnh đối diện. Số lượng lần lượt là một, sáu, ba, tám và sáu. Hãy kiểm tra tổng đúng hai mươi bốn.

### Nhịp 44 – Đồng nhất và trục mặt
**Cột trái:** mô hình trực quan `cube` ở trạng thái 1, tô sáng yếu tố then chốt.
**Cột phải:** Đồng nhất: 3⁶ = 729; Quay 90° qua mặt: 3³ = 27; Quay 180° qua mặt: 3⁴ = 81.
**Công thức Typst:** `3^6+6 cdot 3^3+3 cdot 3^4`.
**Kết luận:** Số chu trình được đọc từ chuyển động sáu mặt.

**Lời giảng:** Phép đồng nhất giữ sáu mặt riêng biệt nên có ba mũ sáu cách tô bất biến. Quay chín mươi độ quanh trục đi qua tâm hai mặt đối diện cố định hai mặt, đồng thời quay bốn mặt bên thành một chu trình: tổng ba chu trình, cho hai mươi bảy cách. Quay một trăm tám mươi độ theo trục ấy cho hai mặt đứng yên cùng hai cặp mặt bên, tổng bốn chu trình, cho tám mươi mốt cách.

### Nhịp 45 – Trục qua hai đỉnh
**Cột trái:** mô hình trực quan `cube` ở trạng thái 2, tô sáng yếu tố then chốt.
**Cột phải:** Có tám phép quay ±120°; Sáu mặt chia thành hai bộ ba; Hai chu trình: 3² = 9.
**Công thức Typst:** `8 cdot 3^2=72`.
**Kết luận:** Nhóm quay qua đỉnh đóng góp 8·9.

**Lời giảng:** Một trục nối hai đỉnh đối diện cho phép quay một trăm hai mươi hoặc hai trăm bốn mươi độ. Có bốn trục như vậy, tạo tổng tám phép quay. Dưới mỗi phép, sáu mặt được chia thành hai chu trình dài ba. Mỗi chu trình phải có một màu chung, cho ba bình phương bằng chín cách tô bất biến. Toàn nhóm đóng góp tám nhân chín bằng bảy mươi hai.

### Nhịp 46 – Trục qua hai cạnh
**Cột trái:** mô hình trực quan `cube` ở trạng thái 3, tô sáng yếu tố then chốt.
**Cột phải:** Có sáu phép quay 180°; Ba cặp mặt bị tráo với nhau; Ba chu trình: 3³ = 27.
**Công thức Typst:** `6 cdot 3^3=162`.
**Kết luận:** Nhóm qua cạnh đóng góp 6·27.

**Lời giảng:** Một phép quay nửa vòng quanh trục đi qua trung điểm hai cạnh đối diện sẽ đổi chỗ cả sáu mặt thành ba cặp. Vì có sáu trục kiểu này, ta có sáu phép quay. Mỗi phép có ba chu trình độ dài hai; các mặt trong từng cặp bắt buộc cùng màu để hình không đổi. Do đó số cách tô bất biến bằng ba mũ ba, tức hai mươi bảy, cho tổng đóng góp một trăm sáu mươi hai.

### Nhịp 47 – Tổng Burnside cho lập phương
**Cột trái:** mô hình trực quan `cube` ở trạng thái 4, tô sáng yếu tố then chốt.
**Cột phải:** 729 + 6·27 + 3·81; Thêm 8·9 + 6·27; Chia 24: kết quả 57.
**Công thức Typst:** `N=frac(729+162+243+72+162,24)=57`.
**Kết luận:** Mỗi phép quay đã được tính đúng một lần.

**Lời giảng:** Bây giờ cộng số cách tô bất biến của năm nhóm: bảy trăm hai mươi chín, một trăm sáu mươi hai, hai trăm bốn mươi ba, bảy mươi hai và một trăm sáu mươi hai. Tổng là một nghìn ba trăm sáu mươi tám. Chia cho hai mươi bốn phép quay, ta được năm mươi bảy mẫu tô khác nhau. Đây là câu trả lời hoàn chỉnh cho bài toán Olympic.

### Nhịp 48 – Chứng minh độc lập bằng máy
**Cột trái:** mô hình trực quan `cube` ở trạng thái 5, tô sáng yếu tố then chốt.
**Cột phải:** Sinh đủ 3⁶ = 729 cách tô; Sinh 24 phép quay bằng ma trận; Chuẩn hóa quỹ đạo, thu đúng 57.
**Công thức Typst:** `N_(orbit)=57`.
**Kết luận:** Hai cách đếm độc lập khớp tuyệt đối.

**Lời giảng:** Để tự kiểm tra chứ không chỉ tin công thức, ta xây dựng hai mươi bốn phép quay của khối lập phương dưới dạng các hoán vị sáu mặt. Với mỗi trong bảy trăm hai mươi chín cách tô, ta sinh tất cả ảnh dưới phép quay rồi chọn đại diện chuẩn. Số đại diện khác nhau được chương trình tính độc lập đúng bằng năm mươi bảy. Cách kiểm chứng này cũng là minh chứng rằng việc phân loại năm nhóm ở trên là đầy đủ.
