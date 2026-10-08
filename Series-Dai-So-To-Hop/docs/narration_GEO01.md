# GEO01 — Điều kiện để điểm nằm trong miền trong tam giác

**Dự án:** SANG MATH · Video độc lập trước COMB03  
**Thể loại:** Hình học tọa độ Oxy, đại số hóa điều kiện hình học  
**Thời lượng lời giảng đề xuất:** khoảng 7–9 phút (cần đồng bộ thêm với bản render)  
**Ký hiệu:** dấu `<` / `>` là miền trong; `≤` / `≥` là miền đóng, kể cả cạnh.

## Phân đoạn 1 — Nêu đề và câu hỏi dẫn nhập

Cho tam giác A B C với A có tọa độ không, ba; B âm một, hai; C hai, một. Điểm M có hoành độ m, tung độ bằng hai m trừ một, chia hai. Hãy tìm điều kiện để M nằm **bên trong** tam giác A B C. Nếu điều kiện viết được dưới dạng a nhỏ hơn m nhỏ hơn b, hãy tính tám a cộng bốn b.

Trước hết, chúng ta không vội thay tọa độ vào ba đường thẳng. Hãy quan sát tam giác: với mỗi m, điểm M đi theo một quỹ tích, và chỉ những vị trí ở trong vùng tam giác mới thỏa mãn yêu cầu.

## Phân đoạn 2 — Quỹ tích của M

Từ hoành độ x bằng m, tung độ y bằng m trừ một phần hai, ta suy ra y bằng x trừ một phần hai. Đây là một đường thẳng có hệ số góc một. Khi m tăng, M di chuyển từ dưới bên trái lên trên bên phải.

Một điểm M ở trong tam giác khi nó nằm đồng thời về phía trong của cả ba đường thẳng chứa các cạnh. Ở bài này, quỹ tích chỉ cắt một phần rất nhỏ gần đỉnh C. Vì vậy, chúng ta sẽ **phóng đại đều** vùng gần C để nhìn rõ hai điểm giao, không làm biến dạng hình.

## Phân đoạn 3 — Phóng đại vùng giao

Đường tím là quỹ tích M. Hai đường cyan là những phần của cạnh A C và B C. Khoảng xanh lá nằm giữa hai giao điểm. Trong khoảng đó, M nằm trong tam giác. Tại hai đầu đoạn, M nằm **trên cạnh**, không còn nằm trong miền trong.

Chúng ta cần tìm hai giá trị m ở biên. Giá trị nhỏ ứng với giao điểm của quỹ tích với cạnh B C. Giá trị lớn ứng với cạnh A C.

## Phân đoạn 4 — Tìm chính xác hai đầu đoạn

Đường thẳng B C có phương trình x cộng ba y bằng năm. Thay y bằng x trừ một phần hai vào, ta được x cộng ba nhân x trừ một phần hai bằng năm. Suy ra bốn x bằng mười ba phần hai, nên x bằng mười ba phần tám.

Đường thẳng A C có phương trình x cộng y bằng ba. Thay y bằng x trừ một phần hai, ta được hai x trừ một phần hai bằng ba. Vậy hai x bằng bảy phần hai, nên x bằng bảy phần bốn.

Đây mới là hai giá trị tại biên. Ta còn phải kiểm tra đoạn giữa thực sự ở trong tam giác. Một cách đảm bảo chặt chẽ hơn là dùng hệ bất phương trình của ba nửa mặt phẳng.

## Phân đoạn 5 — Ba nửa mặt phẳng

Ta viết các điều kiện của một điểm N có tọa độ x, y nằm bên trong tam giác này.

Cạnh A B có phương trình y bằng x cộng ba. Đỉnh C nằm dưới đường này, vậy điều kiện là x trừ y cộng ba lớn hơn không.

Cạnh B C có phương trình x cộng ba y bằng năm. Đỉnh A nằm phía có x cộng ba y lớn hơn năm. Vì vậy điều kiện thứ hai là x cộng ba y trừ năm lớn hơn không.

Cạnh C A có phương trình x cộng y bằng ba. Đỉnh B nằm phía có x cộng y nhỏ hơn ba. Điều kiện thứ ba là ba trừ x trừ y lớn hơn không.

Phải lấy **giao** cả ba điều kiện, chứ không phải chỉ chọn một trong ba.

## Phân đoạn 6 — Thay M vào các điều kiện

Với x bằng m và y bằng m trừ một phần hai, điều kiện từ cạnh A B trở thành bảy phần hai lớn hơn không. Điều này luôn đúng.

Điều kiện từ cạnh B C trở thành bốn m trừ mười ba phần hai lớn hơn không. Suy ra m lớn hơn mười ba phần tám.

Điều kiện từ cạnh C A trở thành bảy phần hai trừ hai m lớn hơn không. Suy ra m nhỏ hơn bảy phần bốn.

Kết hợp lại, m lớn hơn mười ba phần tám và nhỏ hơn bảy phần bốn. Hai dấu đều là dấu **nghiêm ngặt** vì đề hỏi điểm nằm bên trong.

## Phân đoạn 7 — Kết quả và phép tính

So sánh với a nhỏ hơn m nhỏ hơn b, ta có a bằng mười ba phần tám, b bằng bảy phần bốn. Tám a bằng mười ba. Bốn b bằng bảy. Do đó T bằng hai mươi.

Bây giờ hãy rút ra một phương pháp có thể dùng cho **mọi tam giác**, bất kể hình quay theo hướng nào.

## Phân đoạn 8 — Tổng quát bằng tích có hướng

Cho tam giác bất kỳ A B C không thẳng hàng, và điểm N có tọa độ x, y. Ta sử dụng tích có hướng trong mặt phẳng. Với hai vectơ u và v, tích có hướng bằng hoành độ u nhân tung độ v, trừ tung độ u nhân hoành độ v.

Đặt D là tích có hướng của vectơ A B và A C. D khác không, vì tam giác không suy biến. Nếu D dương thì A, B, C được định hướng ngược chiều kim đồng hồ. Khi đó N nằm trong tam giác nếu tích có hướng của A B với A N, của B C với B N, và của C A với C N đều dương.

Nếu D âm, cả ba dấu sẽ đảo ngược. Để viết thống nhất, ta nhân các tích có hướng đó với dấu của D rồi yêu cầu cả ba tích đều lớn hơn không. Đây là phép thử đúng với **mọi tọa độ, mọi hướng** của tam giác.

## Phân đoạn 9 — Miền trong, biên và bên ngoài

Một điểm nằm trong tam giác thì thỏa đồng thời ba bất phương trình nghiêm ngặt. Một điểm trên cạnh cho ít nhất một tích bằng không và hai tích còn lại không âm. Nếu cả ba điều kiện không âm, điểm nằm trong **tam giác đóng**, bao gồm cả ba cạnh.

Lưu ý: việc một điểm thuộc đường thẳng chứa cạnh không đủ để kết luận điểm nằm trên đoạn cạnh. Nó còn phải thỏa hai điều kiện còn lại.

## Phân đoạn 10 — Tiêu chuẩn tương đương: tọa độ tỉ cự

Một cách khác dùng tọa độ tỉ cự. Ta viết N bằng alpha nhân A cộng beta nhân B cộng gamma nhân C, với alpha cộng beta cộng gamma bằng một. Khi tam giác không suy biến, bộ ba hệ số này là duy nhất.

N nằm trong miền trong khi cả alpha, beta, gamma đều lớn hơn không. Nếu các hệ số đều không âm, điểm thuộc tam giác đóng. Đây là công cụ hữu ích khi học sinh học tiếp về phương trình tham số, diện tích và các mô hình hình học phức tạp hơn.

## Phân đoạn 11 — Tổng kết

Hãy ghi nhớ ba bước: viết phương trình ba cạnh; xác định nửa mặt phẳng phía trong với mỗi cạnh, bằng cách thử đỉnh đối diện hoặc dùng tích có hướng; cuối cùng lấy giao ba bất phương trình. Nếu điểm có tham số, thay tọa độ theo tham số và giải hệ điều kiện.

Với bài toán ban đầu, đáp số là T bằng hai mươi. Quan trọng hơn, chúng ta đã có một **phương pháp tổng quát**, không cần đoán bằng hình vẽ.

---

**Ghi chú sản xuất:** Scene hiện chưa đồng bộ lời giảng hoặc TTS. Kéo dài các đoạn `wait()` và chỉnh `run_time` theo file thu âm cuối cùng; chỉ thêm âm thanh sau khi kiểm duyệt bố cục và toán học. Các ảnh `contact_sheet.png` do GitHub Actions trích tự động không thay thế cho xem toàn bộ video.
