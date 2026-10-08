# COMB19 V2 – STORYBOARD 48 NHỊP / 8 CHƯƠNG

**Tập con và công thức 2^n – từ lựa chọn nhị phân đến hệ thức Fibonacci**

- Bố cục cố định: mô hình động bên trái, đề bài/lập luận/công thức bên phải.
- Ký hiệu đúng yêu cầu: `C^(n)_(k)` với n ở trên, k ở dưới.
- Mỗi nhịp mở bằng hình động, tiếp theo mới cho lập luận, công thức và kết luận xuất hiện.
- Trước bài toán cuối phải nhắc rõ tám vị trí xếp **trên một hàng**, không phải vòng tròn.

## 01 · TẬP CON LÀ GÌ?

**Mốc dự kiến:** 00:00 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 01 – Ba thẻ A, B, C
**Hình:** Tập ban đầu có ba phần tử.; Mỗi phần tử có thể được chọn hoặc bỏ.; Đừng quên tập rỗng.
**Công thức Typst:** `explore_0`
**Chốt:** Bắt đầu bằng liệt kê chính xác.

Hãy quan sát ba thẻ A, B, C ở bên trái. Một tập con được tạo bằng cách quyết định đối với từng thẻ: giữ lại hay không giữ. Không hề có yêu cầu phải lấy ít nhất một thẻ. Vì vậy, tập rỗng cũng là một tập con. Ta sẽ liệt kê các khả năng một cách có hệ thống, thay vì đoán số lượng từ một công thức chưa được giải thích.

### Nhịp 02 – Tập rỗng vẫn là tập con
**Hình:** Không chọn A, B hay C.; Có đúng một lựa chọn như vậy.; Tập rỗng không phải là “không có kết quả”.
**Công thức Typst:** `explore_1`
**Chốt:** Tập rỗng là một lựa chọn hợp lệ.

Nếu cả ba công tắc đều ở trạng thái không chọn, chúng ta nhận được tập rỗng. Đó chính là một tập con hợp lệ của S. Học sinh thường bỏ sót trường hợp này và kết quả sẽ thiếu một. Ta cần phân biệt khái niệm tập con với tập con khác rỗng. Bây giờ hãy bật một công tắc và xem một phần tử được đưa vào tập con như thế nào.

### Nhịp 03 – Chọn đúng một phần tử
**Hình:** Ba kết quả: {A}, {B}, {C}.; Không phân biệt thứ tự ghi các phần tử.; Mỗi tập con chỉ đếm một lần.
**Công thức Typst:** `explore_2`
**Chốt:** Có ba tập con một phần tử.

Khi chỉ chọn một thẻ, ta có ba tập con: chỉ A, chỉ B hoặc chỉ C. Chẳng hạn viết A trước hay sau một dấu ngoặc không làm thay đổi bản chất của tập hợp. Với hai phần tử, thứ tự A rồi B và B rồi A cũng không tạo ra hai tập con khác nhau. Quy ước ấy rất quan trọng để về sau không đếm trùng.

### Nhịp 04 – Chọn đúng hai phần tử
**Hình:** Ba nhóm: {A,B}, {A,C}, {B,C}.; AB và BA là một tập con.; Mỗi nhóm mang đúng hai thẻ.
**Công thức Typst:** `explore_3`
**Chốt:** Có ba tập con hai phần tử.

Ta tiếp tục chọn đúng hai trong ba thẻ. Ba kết quả là A với B, A với C và B với C. Những trường hợp đảo thứ tự không được tính thêm. Đây chính là đối tượng mà công thức tổ hợp đếm: chọn một nhóm có số phần tử xác định, không xét thứ tự. Từ ví dụ nhỏ, ta đã tạo được liên hệ trực tiếp với kiến thức ở Video 07.

### Nhịp 05 – Chọn cả ba
**Hình:** Chỉ có tập {A,B,C}.; Tập ban đầu là tập con của chính nó.; Không được bỏ qua nhóm đầy đủ.
**Công thức Typst:** `explore_4`
**Chốt:** Tập đầy đủ là tập con hợp lệ.

Còn một trường hợp: cả A, B và C đều được chọn. Khi đó tập con trùng với tập ban đầu S, và hoàn toàn hợp lệ. Đến đây ta có một tập rỗng, ba tập con một phần tử, ba tập con hai phần tử và một tập con ba phần tử. Hãy dừng hình để học sinh tự cộng lại trước khi số tám xuất hiện ở phía phải.

### Nhịp 06 – Tổng cộng tám tập con
**Hình:** Tập con được chia theo kích thước.; Các nhóm kích thước khác nhau không giao nhau.; Tổng: 1+3+3+1=8.
**Công thức Typst:** `explore_5`
**Chốt:** Mọi tập con đều nằm trong đúng một nhóm.

Chúng ta cộng một, ba, ba và một, nhận được tám tập con. Cách chia theo số phần tử bảo đảm không bỏ sót: mỗi tập con có một kích thước xác định từ không đến ba. Đồng thời, không thể thuộc hai nhóm kích thước khác nhau, nên không đếm trùng. Ở phần tiếp theo, ta sẽ tìm một cách khác giải thích số tám mà không cần viết ra từng tập con.

## 02 · HAI QUYẾT ĐỊNH CHO MỖI PHẦN TỬ

**Mốc dự kiến:** 02:24 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 07 – Mỗi thẻ có hai trạng thái
**Hình:** Có thể chọn hoặc không chọn.; Hai trạng thái là khác nhau.; Quyết định không ảnh hưởng thẻ khác.
**Công thức Typst:** `switches_0`
**Chốt:** Mỗi phần tử đóng góp hệ số 2.

Thay vì liệt kê tập con, ta gắn cho mỗi thẻ một công tắc. Chọn được ký hiệu bằng một, không chọn bằng không. Cả ba công tắc có thể bật tắt độc lập. Mỗi công tắc có hai trạng thái nên theo quy tắc nhân, có hai nhân hai nhân hai cách thiết lập. Điều cần lưu ý là mỗi thiết lập tương ứng đúng một tập con, và ngược lại.

### Nhịp 08 – Mã nhị phân 000
**Hình:** 000 nghĩa là không chọn thẻ nào.; Tương ứng với tập rỗng.; Không nhầm mã với số tự nhiên.
**Công thức Typst:** `switches_1`
**Chốt:** Một mã nhị phân ứng với một tập con.

Một dãy gồm ba chữ số không và một chỉ là mã để ghi trạng thái chọn. Chẳng hạn mã không, không, không tương ứng tập rỗng. Ta không đang đếm các số có ba chữ số, vì chữ số đầu bằng không vẫn được phép. Đây là dãy trạng thái của ba phần tử, và ba vị trí có vai trò riêng. Sự phân biệt nhỏ này tránh một lỗi đếm thường gặp.

### Nhịp 09 – Mã 101 và tập {A,C}
**Hình:** Vị trí 1 tương ứng A.; Vị trí 2 tương ứng B.; Vị trí 3 tương ứng C.
**Công thức Typst:** `switches_2`
**Chốt:** 101 nghĩa là chọn A và C.

Hãy nhìn mã một, không, một. Trạng thái thứ nhất bật nên A được chọn; trạng thái thứ hai tắt nên B bị bỏ; trạng thái thứ ba bật nên C được chọn. Do đó mã tương ứng tập A và C. Nếu ta bắt đầu từ một tập con bất kỳ, ta cũng xác định ngược lại được chính xác một mã. Đây là một song ánh, tức quan hệ một đối một giữa hai bộ đối tượng.

### Nhịp 10 – Bốn phần tử và mười sáu mã
**Hình:** Thêm D vào dãy lựa chọn.; Mỗi tập con cũ sinh hai tập con mới.; Số lượng tăng gấp đôi.
**Công thức Typst:** `switches_3`
**Chốt:** Mỗi phần tử thêm vào nhân đôi số tập con.

Bây giờ thêm thẻ D. Với mỗi tập con đã có từ ba thẻ đầu tiên, ta được đúng hai tập con mới: không có D hoặc có D. Do đó tám tập con cũ tạo thành mười sáu tập con. Hình động sẽ cho thấy các thẻ bên trái được nhân đôi thành hai tầng. Ta không cần liệt kê mười sáu bộ bằng tay để biết kết quả.

### Nhịp 11 – Quy nạp theo số phần tử
**Hình:** Tập không phần tử: một tập con.; Thêm mỗi phần tử mới: nhân hai.; Lặp lại n lần.
**Công thức Typst:** `switches_4`
**Chốt:** Số tập con của n phần tử bằng 2^n.

Ta có thể chứng minh tổng quát bằng quy nạp. Tập có không phần tử có đúng một tập con, là tập rỗng. Giả sử một tập có n trừ một phần tử có một số cách chọn đã biết. Khi thêm phần tử mới, mỗi tập con cũ sinh hai tập con, vì phần tử này hoặc được chọn hoặc không. Như vậy số tập con tăng gấp đôi ở mỗi bước.

### Nhịp 12 – Công thức tổng quát
**Hình:** n phần tử phân biệt.; Mỗi phần tử: hai lựa chọn độc lập.; Kết quả: 2 mũ n.
**Công thức Typst:** `switches_5`
**Chốt:** Áp dụng cho mọi n nguyên không âm.

Kết luận: với n phần tử phân biệt, số tập con là hai mũ n, kể cả tập rỗng và toàn bộ tập ban đầu. Khi n bằng không, hai mũ không bằng một, phù hợp trường hợp tập rỗng. Công thức chỉ phụ thuộc số phần tử chứ không phụ thuộc tên gọi hay cách sắp thứ tự của chúng. Tiếp theo, ta sẽ nối kết quả này với số tổ hợp C có n ở trên, k ở dưới.

## 03 · PHÂN TẦNG THEO KÍCH THƯỚC

**Mốc dự kiến:** 04:24 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 13 – Chia theo số phần tử
**Hình:** Tập con cỡ 0, 1, ... , n.; Mỗi tập con có kích thước duy nhất.; Các lớp không giao nhau.
**Công thức Typst:** `sizes_0`
**Chốt:** Đếm tất cả bằng cách cộng các lớp.

Có một cách đếm thứ hai: phân loại tập con theo số lượng phần tử được chọn. Nhóm đầu tiên có không phần tử, nhóm kế tiếp có một phần tử, cứ như vậy đến nhóm có đủ n phần tử. Mỗi tập con xuất hiện trong đúng một nhóm theo kích thước, nên ta có thể cộng số tập con trong các nhóm. Nhìn ở góc độ này, bài toán tạo cầu nối trực tiếp đến hệ số nhị thức Newton.

### Nhịp 14 – Lớp không phần tử
**Hình:** Chỉ có tập rỗng.; Số cách chọn không phần tử từ n là 1.; Điều này đúng với mọi n.
**Công thức Typst:** `sizes_1`
**Chốt:** Lớp đầu tiên luôn có một tập con.

Bất kể tập ban đầu chứa bao nhiêu phần tử, luôn có đúng một cách chọn không phần tử: không chọn gì cả. Ta ghi số cách bằng C có n ở trên, không ở dưới, và giá trị bằng một. Đây không phải một công thức phải học thuộc máy móc; nó chính là cách diễn đạt của tập rỗng trong phép đếm tổ hợp.

### Nhịp 15 – Chọn k trong n
**Hình:** Mỗi tập con k phần tử là một nhóm k phần tử.; Thứ tự không quan trọng.; Có C_k^n tập con như vậy.
**Công thức Typst:** `sizes_2`
**Chốt:** Lớp kích thước k có C_k^n phần tử.

Muốn tạo một tập con đúng k phần tử, ta chọn k phần tử trong n phần tử phân biệt. Đó chính là bài toán tổ hợp đã học: thứ tự không tạo ra kết quả mới. Vì vậy lớp kích thước k có C có n ở trên, k ở dưới phần tử. Trực quan, các thẻ cùng số lượng được xếp trên một hàng để học sinh thấy rõ cách phân tầng.

### Nhịp 16 – Ví dụ n=5
**Hình:** Sáu lớp có kích thước 0 đến 5.; Số lượng: 1, 5, 10, 10, 5, 1.; Tổng cộng 32.
**Công thức Typst:** `sizes_3`
**Chốt:** Các hệ số hàng thứ năm của Pascal.

Với năm phần tử, các số lượng theo kích thước lần lượt là một, năm, mười, mười, năm, một. Ta nhận đúng hàng thứ năm của tam giác Pascal, rồi cộng được ba mươi hai. Cảnh này sẽ giữ nguyên các lớp trong lúc tô sáng tổng hàng để nối trực tiếp với Video 18. Học sinh không phải ghi nhớ một đẳng thức mới tách rời kiến thức cũ.

### Nhịp 17 – Đẳng thức quan trọng
**Hình:** Đếm các tập con theo hai cách.; Cách 1: mỗi phần tử chọn hoặc không.; Cách 2: phân theo kích thước.
**Công thức Typst:** `sizes_4`
**Chốt:** Hai phép đếm cùng một tập hợp.

Đếm theo công tắc cho hai mũ n. Đếm theo từng lớp kích thước cho tổng các hệ số tổ hợp từ k bằng không tới n. Cả hai đều đếm đúng toàn bộ tập con của cùng một tập n phần tử. Do vậy hai biểu thức phải bằng nhau. Đây là chứng minh tổ hợp: chứng minh một đẳng thức bằng hai cách đếm, không cần khai triển đại số.

### Nhịp 18 – Khi nào nên phân lớp?
**Hình:** Có yêu cầu đúng k phần tử.; Có điều kiện chẵn lẻ của kích thước.; Có giới hạn số phần tử chọn.
**Công thức Typst:** `sizes_5`
**Chốt:** Chia lớp giúp kiểm soát điều kiện.

Nếu đề bài hỏi đúng k phần tử thì ta chỉ lấy một lớp. Nếu hỏi nhiều nhất r phần tử thì lấy tổng các lớp từ không đến r. Nếu hỏi số phần tử chẵn, ta cộng riêng các lớp chẵn. Phân tầng không phải thao tác trang trí: nó chính là chiến lược toán học để đưa điều kiện phức tạp vào bài toán một cách chính xác.

## 04 · CHỨA HAY KHÔNG CHỨA A

**Mốc dự kiến:** 06:24 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 19 – Cố định một phần tử A
**Hình:** A được chọn hoặc không.; Hai lớp không giao nhau.; Hai lớp phủ hết các tập con.
**Công thức Typst:** `special_0`
**Chốt:** Chia theo sự xuất hiện của A.

Giả sử tập có năm phần tử và ta quan tâm riêng đến A. Mỗi tập con hoặc chứa A, hoặc không chứa A, không có trường hợp thứ ba. Hai lớp này không giao nhau và hợp của chúng là toàn bộ tập con. Sơ đồ phía trái sẽ tách thành hai nhóm lớn để học sinh nhìn thấy phép phân hoạch trước khi tính số lượng.

### Nhịp 20 – Bắt buộc chứa A
**Hình:** Giữ A cố định trong tập con.; Bốn phần tử còn lại tự do.; Có 16 tập con.
**Công thức Typst:** `special_1`
**Chốt:** Cố định A làm giảm một bậc tự do.

Nếu đề yêu cầu tập con phải chứa A, ta không còn phải lựa chọn A nữa: A chắc chắn xuất hiện. Bốn phần tử còn lại độc lập chọn hoặc không chọn, nên có hai mũ bốn bằng mười sáu cách. Phải chú ý rằng đây là mọi kích thước, từ một phần tử A đến cả năm phần tử; nếu đề yêu cầu đúng một kích thước, phương pháp sẽ khác.

### Nhịp 21 – Bắt buộc không chứa A
**Hình:** Loại A khỏi tập được chọn.; Bốn phần tử còn lại tự do.; Cũng có 16 tập con.
**Công thức Typst:** `special_2`
**Chốt:** Không chứa A cũng cho 2^(n-1).

Nếu cấm A xuất hiện, ta cố định công tắc A ở trạng thái tắt. Bốn công tắc khác vẫn độc lập, cho mười sáu trường hợp. Như vậy hai nhóm có A và không A bằng nhau về số lượng. Chúng ta còn có thể ghép từng tập không chứa A với tập được tạo bằng cách thêm A, tạo nên một song ánh rất trực quan.

### Nhịp 22 – Có A nhưng không có B
**Hình:** A luôn chọn, B luôn bỏ.; Ba phần tử còn lại được chọn tự do.; Có 8 cách.
**Công thức Typst:** `special_3`
**Chốt:** Mỗi điều kiện cố định giảm một công tắc.

Bây giờ đặt đồng thời hai điều kiện: A phải thuộc tập con, còn B không được thuộc. Hai công tắc tương ứng đã bị cố định. Với năm phần tử ban đầu, chỉ còn ba công tắc tự do. Do đó có tám tập con phù hợp. Điều quan trọng là không lấy mười sáu nhân mười sáu: các lựa chọn không diễn ra thành hai bước độc lập như vậy.

### Nhịp 23 – Chính xác một trong A,B
**Hình:** Hoặc có A không B, hoặc B không A.; Hai trường hợp tách biệt.; Mỗi trường hợp có 8 tập con.
**Công thức Typst:** `special_4`
**Chốt:** Chính xác một: 8+8=16.

Cụm từ chính xác một trong A và B nghĩa là ta chọn một trong hai, nhưng không chọn cả hai và cũng không bỏ cả hai. Có hai trường hợp rời nhau: A xuất hiện và B không, hoặc B xuất hiện và A không. Mỗi trường hợp có tám lựa chọn cho ba phần tử khác. Cộng lại được mười sáu, không phải hai mươi bốn.

### Nhịp 24 – Ít nhất một trong A,B
**Hình:** Lấy tất cả 32 tập con.; Loại 8 tập không có cả A lẫn B.; Còn 24 tập con.
**Công thức Typst:** `special_5`
**Chốt:** Ít nhất một cho phép chọn cả hai.

Cụm từ ít nhất một cho phép chọn A, chọn B, hoặc chọn cả hai. Cách nhanh nhất là đếm phần bù: có ba mươi hai tập con tất cả, nhưng tám tập không chứa cả A lẫn B. Lấy hiệu được hai mươi bốn. Trên hình, vùng có cả A và B sẽ vẫn được giữ lại, nhắc học sinh không nhầm ít nhất một với đúng một.

## 05 · TẬP CON CHẴN VÀ LẺ

**Mốc dự kiến:** 08:24 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 25 – Phân theo chẵn lẻ
**Hình:** Kích thước tập con là số nguyên.; Một tập con hoặc chẵn, hoặc lẻ.; Hai nhóm tách biệt.
**Công thức Typst:** `parity_0`
**Chốt:** Tổng hai nhóm bằng 2^n.

Đối với mỗi tập con, ta có thể xem số phần tử của nó là chẵn hay lẻ. Tập rỗng có không phần tử, nên thuộc nhóm chẵn. Hai nhóm chẵn và lẻ không giao nhau, đồng thời bao phủ toàn bộ tập con. Vì vậy tổng số tập con chẵn và lẻ luôn bằng hai mũ n. Câu hỏi thú vị là chúng có số lượng bằng nhau hay không.

### Nhịp 26 – Ghép đôi bằng một phần tử A
**Hình:** Chọn A làm phần tử cố định.; Thêm hoặc bỏ A làm đổi tính chẵn lẻ.; Các tập con được ghép thành cặp.
**Công thức Typst:** `parity_1`
**Chốt:** Ghép đôi một–một, không dư.

Giữ một phần tử A làm dấu mốc. Với mỗi tập con, ta đổi trạng thái chọn của A: nếu đang có A thì bỏ đi; nếu chưa có A thì thêm vào. Số phần tử vì vậy đổi từ chẵn thành lẻ hoặc ngược lại. Thao tác làm lần hai đưa ta trở lại tập con cũ, nên các tập con được ghép thành từng cặp một chẵn, một lẻ, không thừa, không thiếu.

### Nhịp 27 – Kết quả cho n phần tử
**Hình:** n phải lớn hơn hoặc bằng 1.; Số tập con chẵn bằng số tập con lẻ.; Mỗi nhóm chiếm đúng một nửa.
**Công thức Typst:** `parity_2`
**Chốt:** Cả hai nhóm có 2^(n−1).

Vì tổng có hai mũ n tập con và hai nhóm có số lượng bằng nhau, mỗi nhóm có hai mũ n trừ một tập con. Kết quả này đúng khi tập ban đầu có ít nhất một phần tử, bởi ta cần một phần tử để thực hiện thao tác đổi trạng thái. Đừng vội áp dụng cho n bằng không: đó là ngoại lệ cần giải thích riêng.

### Nhịp 28 – Ví dụ năm phần tử
**Hình:** Tất cả có 32 tập con.; Số tập con chẵn = 16.; Số tập con lẻ = 16.
**Công thức Typst:** `parity_3`
**Chốt:** Một minh chứng cho các hàng Pascal xen kẽ.

Với năm phần tử, có ba mươi hai tập con. Các lớp kích thước chẵn là không, hai và bốn, cộng được một cộng mười cộng năm bằng mười sáu. Các lớp kích thước lẻ là một, ba và năm, cộng được năm cộng mười cộng một, cũng bằng mười sáu. Hai phép đếm kiểm chứng cùng kết quả, và nối với tổng hệ số tổ hợp theo chỉ số chẵn, lẻ.

### Nhịp 29 – Đẳng thức tổng xen dấu
**Hình:** Trừ số lớp lẻ khỏi số lớp chẵn.; Hai nhóm bằng nhau khi n >= 1.; Tổng xen dấu bằng không.
**Công thức Typst:** `parity_4`
**Chốt:** Chứng minh trực quan cho (1−1)^n.

Từ phép ghép đôi, số tập con chẵn trừ số tập con lẻ bằng không. Khi thay số lượng mỗi lớp bằng hệ số tổ hợp, ta thu được tổng xen dấu của các hệ số C có n ở trên. Đây cũng là kết quả thay x bằng âm một trong khai triển nhị thức Newton, nhưng cách ghép đôi giúp giải thích vì sao các phần dương và âm triệt tiêu nhau.

### Nhịp 30 – Ngoại lệ khi n bằng không
**Hình:** Chỉ có tập rỗng.; Một tập con chẵn, không có tập con lẻ.; Không thể chọn A để ghép đôi.
**Công thức Typst:** `parity_5`
**Chốt:** Điều kiện n ≥ 1 không được bỏ qua.

Cuối chương, ta xét tập rỗng làm tập ban đầu. Tập này có đúng một tập con là chính nó, với kích thước bằng không nên thuộc loại chẵn. Không tồn tại tập con lẻ. Bởi vậy công thức mỗi loại bằng hai mũ n trừ một không thể dùng ở n bằng không. Đây là ví dụ đẹp cho việc kiểm tra điều kiện trước khi áp dụng một định lý.

## 06 · TẬP CON VÀ PHÉP LẤY PHẦN BÙ

**Mốc dự kiến:** 10:24 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 31 – Sơ đồ các tập con
**Hình:** Mỗi nút là một tập con.; Các tầng ghi kích thước của nút.; Một cạnh thêm đúng một phần tử.
**Công thức Typst:** `lattice_0`
**Chốt:** Tập con tạo thành một mạng phân tầng.

Với tập bốn phần tử, chúng ta có thể đặt mười sáu tập con thành những tầng theo kích thước. Tầng dưới cùng là tập rỗng, trên cùng là toàn bộ tập ban đầu. Hai nút ở hai tầng liên tiếp nối với nhau khi nút lớn được tạo bằng cách thêm đúng một phần tử. Hình này cho học sinh thấy quan hệ bao hàm, chứ không chỉ số lượng đơn thuần.

### Nhịp 32 – Phép lấy phần bù
**Hình:** Mỗi tập con T có một phần bù S\T.; Hai phần hợp thành S.; Lấy phần bù hai lần trở về T.
**Công thức Typst:** `lattice_1`
**Chốt:** Mỗi tập con được ghép với một tập bù.

Khi đã chọn một tập con T của S, ta cũng xác định duy nhất tập bù gồm những phần tử không được chọn. Nếu lấy phần bù lần nữa, ta trở lại T. Vì vậy phép lấy phần bù tạo thành sự ghép đôi một đối một giữa các tập con. Đặc biệt, tập con có k phần tử ghép với tập có n trừ k phần tử, là lời giải thích trực quan cho tính đối xứng của hệ số tổ hợp.

### Nhịp 33 – Tập con khác rỗng
**Hình:** Loại đúng một tập rỗng.; Các tập con còn lại đều có ít nhất một phần tử.; Không loại tập S nếu đề không yêu cầu.
**Công thức Typst:** `lattice_2`
**Chốt:** Số tập con khác rỗng là 2^n−1.

Nếu đề yêu cầu tập con khác rỗng, ta đếm toàn bộ hai mũ n rồi loại đúng một tập rỗng. Với n bằng năm, từ ba mươi hai còn ba mươi mốt. Chú ý tập ban đầu S vẫn được tính, vì nó khác rỗng. Tên gọi tập con khác rỗng không đồng nghĩa với tập con thực sự; học sinh phải đọc kỹ điều kiện của đề.

### Nhịp 34 – Tập con thực sự khác rỗng
**Hình:** Loại tập rỗng và tập toàn bộ.; Hai tập này phân biệt nếu n>0.; Còn 2^n−2 cách.
**Công thức Typst:** `lattice_3`
**Chốt:** Điều kiện n≥1 để loại hai tập khác nhau.

Một tập con thực sự là tập con không bằng S. Nếu đồng thời yêu cầu khác rỗng, ta phải loại cả tập rỗng và tập S. Với n lớn hơn không, đó là hai tập khác nhau, nên còn hai mũ n trừ hai. Trong ví dụ năm phần tử, số tập thỏa mãn là ba mươi. Khi tập ban đầu rỗng, hai trường hợp bị loại lại trùng nhau, vì vậy cần xét điều kiện riêng.

### Nhịp 35 – Chọn đúng hai trong ba phần tử đặc biệt
**Hình:** Ba phần tử A, B, C là đặc biệt.; Chọn đúng hai trong ba phần tử này.; Hai phần tử D, E chọn tùy ý.
**Công thức Typst:** `lattice_4`
**Chốt:** Có 3×4=12 tập con.

Xét tập năm phần tử A, B, C, D, E. Đề yêu cầu tập con phải chứa đúng hai phần tử trong nhóm đặc biệt A, B, C. Ta chọn hai trong ba phần tử ấy bằng số tổ hợp có giá trị ba. Còn D và E hoàn toàn tự do, mỗi phần tử có hai lựa chọn, tạo bốn cách. Kết quả là ba nhân bốn bằng mười hai.

### Nhịp 36 – Tổng quát điều kiện hai nhóm
**Hình:** Có r phần tử đặc biệt trong m phần tử.; Chọn đúng k phần tử đặc biệt.; n−m phần tử còn lại tự do.
**Công thức Typst:** `lattice_5`
**Chốt:** Công thức phối hợp tổ hợp và lũy thừa hai.

Ta tổng quát bài toán. Trong n phần tử phân biệt có m phần tử đặc biệt. Muốn chọn một tập con chứa đúng k phần tử đặc biệt, ta có C k của m cách chọn nhóm đặc biệt. Những n trừ m phần tử thông thường được chọn tùy ý, tạo hai mũ n trừ m cách. Nhân hai kết quả được công thức tổng quát, với điều kiện k nằm giữa không và m.

## 07 · KHÔNG CHỌN HAI PHẦN TỬ KỀ NHAU

**Mốc dự kiến:** 12:24 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 37 – Các vị trí xếp trên hàng
**Hình:** Năm thẻ mang số từ 1 đến 5.; Không chọn đồng thời hai số liền nhau.; Các tập con được biểu diễn bằng ô sáng.
**Công thức Typst:** `separated_0`
**Chốt:** Điều kiện phụ thuộc quan hệ kề nhau.

Ta thay tên chữ cái bằng năm vị trí một đến năm trên một hàng ngang. Điều kiện mới là không có hai vị trí được chọn nào kề nhau. Hai phần tử không còn tự do lựa chọn độc lập như trước, vì chọn một vị trí sẽ ngăn chọn vị trí sát bên. Do vậy không thể dùng trực tiếp công thức hai mũ năm; phải tìm một cách đếm tôn trọng ràng buộc.

### Nhịp 38 – Ví dụ những tập con hợp lệ
**Hình:** Tập rỗng hợp lệ.; Các tập đơn đều hợp lệ.; Các cặp như {1,3}, {2,5} hợp lệ.
**Công thức Typst:** `separated_1`
**Chốt:** Tập có hai số liên tiếp bị loại.

Khi chỉ chọn một vị trí thì chắc chắn hợp lệ. Một số cặp như một và ba, hai và năm không đứng kề nhau nên hợp lệ; trái lại, một và hai hoặc ba và bốn phải bị loại. Tập một, ba, năm cũng hợp lệ vì giữa các vị trí được chọn luôn có ít nhất một ô trống. Hình động tô đỏ ngay khi hai ô cạnh nhau cùng sáng.

### Nhịp 39 – Đếm theo số vị trí chọn
**Hình:** Chọn 0 vị trí: 1 cách.; Chọn 1: 5 cách; chọn 2: 6 cách.; Chọn 3: 1 cách.
**Công thức Typst:** `separated_2`
**Chốt:** Tổng 1+5+6+1=13.

Phân chia các tập con hợp lệ theo số vị trí đã chọn. Không chọn gì có một cách; chọn một có năm cách. Chọn hai vị trí không kề nhau có sáu cách. Chọn ba vị trí chỉ có bộ một, ba, năm. Không thể chọn bốn vị trí trong năm ô mà vẫn để chúng cách nhau. Cộng lại được mười ba tập con hợp lệ.

### Nhịp 40 – Công thức chọn k vị trí
**Hình:** Các vị trí tăng dần i_1<...<i_k.; Bỏ đi k−1 khoảng cách bắt buộc.; Bài toán trở thành chọn k trong n−k+1.
**Công thức Typst:** `separated_3`
**Chốt:** Công thức áp dụng cho dãy thẳng.

Giả sử ta chọn k vị trí tăng dần i một, i hai cho tới i k. Để không kề nhau, vị trí sau phải cách vị trí trước ít nhất hai đơn vị. Ta chuyển sang các chỉ số mới bằng cách trừ lần lượt không, một, hai cho tới k trừ một. Chúng trở thành k số phân biệt bất kỳ trong một đến n trừ k cộng một. Do đó số cách là tổ hợp k của n trừ k cộng một.

### Nhịp 41 – Đếm tổng bằng truy hồi
**Hình:** Nếu bỏ ô cuối: bài toán n−1 ô.; Nếu chọn ô cuối: phải bỏ ô trước.; Còn bài toán n−2 ô.
**Công thức Typst:** `separated_4`
**Chốt:** f(n)=f(n−1)+f(n−2).

Một cách khác là phân biệt vị trí cuối cùng. Nếu không chọn ô thứ n, ta chọn một tập con hợp lệ của n trừ một ô đầu. Nếu chọn ô cuối, ô ngay trước bắt buộc bị bỏ, và ta tùy ý chọn từ n trừ hai ô đầu còn lại. Hai trường hợp không giao nhau và bao phủ hết các khả năng. Vì vậy ta nhận được hệ thức truy hồi kiểu Fibonacci.

### Nhịp 42 – Sáu vị trí và Fibonacci
**Hình:** f(0)=1, f(1)=2.; f(2)=3, f(3)=5, f(4)=8.; f(5)=13, f(6)=21.
**Công thức Typst:** `separated_5`
**Chốt:** Liên hệ Fibonacci xuất hiện từ phép chia trường hợp.

Ta bắt đầu từ tập không có ô nào: có một cách không chọn. Với một ô có hai cách. Hệ thức truy hồi lần lượt cho ba, năm, tám, mười ba và hai mươi mốt cách. Vì thế sáu ô có hai mươi mốt tập con không chứa hai vị trí kề nhau. Cần chú ý đây là dãy Fibonacci bị dịch chỉ số, không phải tự động lấy số Fibonacci thứ n theo mọi quy ước.

## 08 · BÀI TOÁN TỔNG HỢP TÁM VỊ TRÍ

**Mốc dự kiến:** 14:24 (nhịp cố định 24 giây); mốc chính xác xem manifest.

### Nhịp 43 – Tám ô và điều kiện kề nhau
**Hình:** Chọn các vị trí từ 1 đến 8.; Không có hai ô được chọn kề nhau.; Phải có ít nhất một đầu mút.
**Công thức Typst:** `challenge_0`
**Chốt:** Hai đầu mút là vị trí 1 và 8.

Ta xét tám vị trí được xếp thành một hàng từ một đến tám. Chỉ được chọn các tập con không có hai vị trí liên tiếp. Đồng thời, tập được chọn phải chứa ít nhất một trong hai đầu mút, nghĩa là vị trí một hoặc vị trí tám, hoặc cả hai. Ta cần đếm chính xác theo hai phương pháp để kiểm tra đáp án.

### Nhịp 44 – Đếm phần bù
**Hình:** Tất cả tập con không kề: f(8)=55.; Loại những tập không chứa cả hai đầu.; Sáu vị trí giữa còn 21 cách.
**Công thức Typst:** `challenge_1`
**Chốt:** Kết quả: 55−21=34.

Ta bắt đầu từ năm mươi lăm tập con không chứa hai vị trí kề nhau của tám ô. Trường hợp không đạt điều kiện đầu mút là không chọn cả vị trí một và tám. Khi ấy chỉ còn sáu ô từ hai đến bảy, và điều kiện không kề nhau cho hai mươi mốt cách. Lấy hiệu năm mươi lăm trừ hai mươi mốt, được ba mươi bốn.

### Nhịp 45 – Chỉ chứa vị trí đầu
**Hình:** Bắt buộc chọn 1, không chọn 8.; Vị trí 2 bị cấm do kề 1.; Năm ô 3 đến 7 có 13 cách.
**Công thức Typst:** `challenge_2`
**Chốt:** Trường hợp chỉ có đầu trái: 13.

Để đếm trực tiếp, trước hết xét trường hợp có vị trí một nhưng không có vị trí tám. Vì một được chọn, vị trí hai bắt buộc bỏ. Phần còn lại là năm vị trí từ ba đến bảy, độc lập với hai vị trí đầu và cuối đã cố định. Có mười ba cách chọn không kề nhau trong năm ô ấy. Hãy quan sát ô thứ hai đổi sang màu đỏ ngay khi ô thứ nhất sáng.

### Nhịp 46 – Chỉ chứa vị trí cuối
**Hình:** Bắt buộc chọn 8, không chọn 1.; Vị trí 7 bị cấm do kề 8.; Năm ô 2 đến 6 có 13 cách.
**Công thức Typst:** `challenge_3`
**Chốt:** Trường hợp chỉ có đầu phải: 13.

Trường hợp chỉ có đầu phải hoàn toàn đối xứng. Ta bắt buộc chọn tám, cấm bảy và không chọn một. Năm vị trí tự do là từ hai đến sáu, và cũng cho mười ba cách. Ta không được nhân hai nếu hai nhóm có giao nhau, nhưng ở đây chúng ta đã quy định đúng một đầu được chọn, nên hai trường hợp hoàn toàn rời nhau.

### Nhịp 47 – Chọn cả hai đầu
**Hình:** Chọn 1 và 8.; Cấm 2 và 7 do kề nhau.; Bốn ô 3,4,5,6 có 8 cách.
**Công thức Typst:** `challenge_4`
**Chốt:** Trường hợp có cả hai đầu: 8.

Cuối cùng ta chọn đồng thời cả vị trí một và tám. Chúng không kề nhau vì đây là hàng thẳng, không phải vòng tròn. Hai vị trí hai và bảy bị cấm, chỉ còn bốn ô từ ba đến sáu. Có tám cách chọn trong bốn ô sao cho không có hai ô kề nhau. Phân biệt hàng thẳng và bàn tròn là điểm then chốt của trường hợp này.

### Nhịp 48 – Hai lời giải khớp nhau
**Hình:** Trực tiếp: 13+13+8=34.; Phần bù: 55−21=34.; Cả hai đều đếm đúng một tập nghiệm.
**Công thức Typst:** `challenge_5`
**Chốt:** Kết thúc: chứng minh rồi mới khẳng định.

Ba trường hợp trực tiếp là chỉ có đầu trái, chỉ có đầu phải và có cả hai đầu. Chúng rời nhau, nên cộng mười ba, mười ba và tám để được ba mươi bốn. Phép đếm phần bù ở trước cũng cho ba mươi bốn. Hai kết quả khớp nhau không thay thế được một chứng minh, nhưng sau khi đã chứng minh từng phép đếm, chúng là cách kiểm chứng đáng tin cậy. Đây là tinh thần chung của Series: hiểu trước, tính sau.
