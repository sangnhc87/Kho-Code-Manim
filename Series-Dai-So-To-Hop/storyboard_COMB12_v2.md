# SANG MATH · COMB12 V2 · PHƯƠNG PHÁP GỘP KHỐI

Video độc lập số 12 của Series Đại số tổ hợp: **Các phần tử bắt buộc đứng cạnh nhau**.

**Chuẩn hình ảnh:** Manim Community + Typst, nền tối 16:9, minh họa bên trái và đề bài / lập luận / công thức bên phải. Các cảnh phải giải thích tính đúng đắn của phép đếm, không kéo dài bằng hiệu ứng trang trí.

**Kế hoạch:** 48 nhịp; 8 chương; thời lượng tối thiểu khoảng 18 phút 12 giây chưa tính lời đọc; bật TTS thì thời gian mỗi nhịp tự điều chỉnh theo âm thanh thật.

## Mục tiêu học tập

- Giải thích được tại sao việc gộp một nhóm phần tử liên tiếp tạo ra một đối tượng mới và vì sao phải nhân với số thứ tự bên trong khối.
- Không áp dụng gộp khối độc lập khi các nhóm có chung phần tử; xét đúng thứ tự nội bộ và điều kiện bất khả thi.
- Dùng quy tắc cộng, phần bù, nguyên lý bao hàm – loại trừ cho điều kiện **ít nhất một**, **đúng một**, **không có**.
- Chuyển mô hình từ xếp thành hàng sang xếp vòng tròn, luôn nói rõ quy ước quay/lật/ghế đánh số.

## Bảng kịch bản 8 chương


### Chương 01 — 01 · TỪ HAI NGƯỜI ĐẾN MỘT KHỐI (bắt đầu khoảng 00:00)

- **Nhịp 1:** BÀI TOÁN MỞ ĐẦU. Minh họa: Năm học sinh A, B, C, D, E.; Xếp thành một hàng.; A và B bắt buộc đứng liền nhau.. **Thông điệp:** HÃY BẮT ĐẦU TỪ ĐIỀU KIỆN, CHƯA VIẾT CÔNG THỨC.

- **Nhịp 2:** THỬ ĐẶT HAI BẠN CẠNH NHAU. Minh họa: Xếp mẫu A – B – C – D – E.; Đổi A, B thành B – A.; Cả hai đều thỏa điều kiện.. **Thông điệp:** ĐỨNG CẠNH KHÔNG CÓ NGHĨA LÀ CỐ ĐỊNH THỨ TỰ.

- **Nhịp 3:** GỘP A VÀ B THÀNH MỘT KHỐI. Minh họa: Đặt [AB] cạnh C, D, E.; Từ 5 người thành 4 đối tượng.; Bốn đối tượng có 4! thứ tự.. **Thông điệp:** KHỐI [AB] KHÔNG THỂ BỊ TÁCH RA KHI XẾP.

- **Nhịp 4:** NHÂN SỐ CÁCH TRONG KHỐI. Minh họa: Thứ tự bốn đối tượng: 4!.; Trong khối có AB hoặc BA: 2!.; Tổng 2! × 4! = 48.. **Thông điệp:** NHÂN HOÁN VỊ CÁC KHỐI VỚI HOÁN VỊ BÊN TRONG.

- **Nhịp 5:** CHỨNG MINH LẠI BẰNG VỊ TRÍ. Minh họa: Cặp AB có thể bắt đầu ở vị trí 1–4.; Mỗi vị trí có 2 thứ tự AB, BA.; Ba người còn lại có 3! cách.. **Thông điệp:** HAI CÁCH ĐẾM CÙNG CHO RA 48.

- **Nhịp 6:** KHÁI QUÁT HAI NGƯỜI TRONG n NGƯỜI. Minh họa: Tất cả n người phân biệt, n ≥ 2.; Gộp hai người thành một khối.; Có 2 × (n − 1)! cách.. **Thông điệp:** CHỈ ÁP DỤNG KHI ĐÚNG HAI NGƯỜI PHẢI ĐỨNG LIỀN.



### Chương 02 — 02 · BA NGƯỜI ĐỨNG LIỀN NHAU (bắt đầu khoảng 02:15)

- **Nhịp 1:** NẾU BA NGƯỜI PHẢI LIỀN NHAU?. Minh họa: Sáu học sinh A, B, C, D, E, F.; A, B, C đứng thành một đoạn liên tiếp.; Bên trong chưa quy định thứ tự.. **Thông điệp:** THAY BA NGƯỜI BẰNG MỘT KHỐI.

- **Nhịp 2:** ĐẾM SỐ ĐỐI TƯỢNG SAU GỘP. Minh họa: Khối [ABC], D, E, F.; Chỉ còn 4 đối tượng.; Sắp xếp ngoài khối: 4! cách.. **Thông điệp:** BA NGƯỜI CHIẾM MỘT ĐOẠN KHÔNG BỊ CHIA CẮT.

- **Nhịp 3:** HOÁN VỊ BÊN TRONG KHỐI. Minh họa: ABC, ACB, BAC, BCA, CAB, CBA.; Có 3! = 6 thứ tự nội bộ.; Tất cả vẫn là ba người liền nhau.. **Thông điệp:** KHÔNG ĐƯỢC QUÊN 3! THỨ TỰ TRONG KHỐI.

- **Nhịp 4:** SÁU NGƯỜI, BA NGƯỜI ĐI LIỀN. Minh họa: Ngoài khối có 4! cách.; Bên trong khối có 3! cách.; Tổng cộng 3! × 4! = 144.. **Thông điệp:** BA NGƯỜI TÙY Ý: ĐẾM ĐỦ SÁU THỨ TỰ.

- **Nhịp 5:** NẾU BẮT BUỘC ĐÚNG ABC. Minh họa: A phải trước B, B phải trước C.; Chỉ còn một thứ tự trong khối.; Có đúng 4! = 24 hàng.. **Thông điệp:** ĐIỀU KIỆN THỨ TỰ THAY ĐỔI ĐÁP SỐ.

- **Nhịp 6:** CÔNG THỨC MỘT KHỐI k NGƯỜI. Minh họa: n người phân biệt; k người tạo một khối.; Bên ngoài: (n − k + 1)! cách.; Bên trong: k! cách.. **Thông điệp:** k! × (n − k + 1)! NẾU KHÔNG RÀNG BUỘC THỨ TỰ.



### Chương 03 — 03 · HAI KHỐI RỜI NHAU (bắt đầu khoảng 04:31)

- **Nhịp 1:** HAI CẶP KHÁC NHAU. Minh họa: A, B phải đứng cạnh nhau.; C, D cũng phải đứng cạnh nhau.; Có sáu học sinh phân biệt.. **Thông điệp:** GỘP THÀNH HAI KHỐI KHÔNG GIAO NHAU.

- **Nhịp 2:** VẼ HAI KHỐI ĐỘC LẬP. Minh họa: [AB], [CD], E, F.; Có bốn đối tượng phân biệt.; Sắp xếp ngoài khối: 4! cách.. **Thông điệp:** HAI KHỐI LÀ HAI ĐỐI TƯỢNG RIÊNG.

- **Nhịp 3:** HAI HOÁN VỊ BÊN TRONG. Minh họa: Khối AB có 2 thứ tự.; Khối CD cũng có 2 thứ tự.; Tổng 2 × 2 × 4! = 96.. **Thông điệp:** CÁC KHỐI RỜI NHAU THÌ NHÂN ĐƯỢC CÁC SỐ CÁCH.

- **Nhịp 4:** NẾU HAI KHỐI ĐÃ CỐ ĐỊNH THỨ TỰ. Minh họa: Phải là AB, không được BA.; Phải là CD, không được DC.; Chỉ còn 4! = 24 cách.. **Thông điệp:** KHÔNG NHÂN HOÁN VỊ NỘI BỘ KHI THỨ TỰ ĐÃ CỐ ĐỊNH.

- **Nhịp 5:** BA CẶP TRONG SÁU NGƯỜI. Minh họa: [AB], [CD], [EF].; Ba khối phân biệt xếp 3! cách.; Mỗi khối có 2 thứ tự.. **Thông điệp:** 3! × 2³ = 48 CÁCH.

- **Nhịp 6:** MỞ RỘNG n NGƯỜI, r KHỐI RỜI. Minh họa: Các khối có kích thước k₁, ..., kᵣ.; Số đối tượng còn n − ∑(kᵢ − 1).; Nhân với ∏kᵢ! nếu được đổi nội bộ.. **Thông điệp:** ĐẢM BẢO CÁC KHỐI KHÔNG CÓ PHẦN TỬ CHUNG.



### Chương 04 — 04 · HAI ĐIỀU KIỆN CÓ CHUNG PHẦN TỬ (bắt đầu khoảng 06:47)

- **Nhịp 1:** HAI CẶP CÓ CHUNG B. Minh họa: A cạnh B và B cạnh C.; B tham gia cả hai điều kiện.; Không thể tạo hai khối độc lập [AB], [BC].. **Thông điệp:** KHỐI GIAO NHAU CẦN XÉT CẤU TRÚC LIÊN TIẾP.

- **Nhịp 2:** AI PHẢI Ở GIỮA?. Minh họa: B phải đứng cạnh cả A và C.; Trong hàng, B có tối đa hai hàng xóm.; Chỉ có A – B – C hoặc C – B – A.. **Thông điệp:** PHẢI CHUNG MỘT KHỐI BA NGƯỜI.

- **Nhịp 3:** ĐẾM HÀNG CÓ SÁU NGƯỜI. Minh họa: [ABC] có đúng 2 dạng được phép.; Ngoài khối là D, E, F: 4 đối tượng.; Số cách 2 × 4! = 48.. **Thông điệp:** KHÔNG PHẢI 2² × 4! VÌ HAI CẶP KHÔNG ĐỘC LẬP.

- **Nhịp 4:** NẾU A CẠNH C VÀ A CẠNH B. Minh họa: A phải là người ở giữa.; Khối có B – A – C hoặc C – A – B.; Cũng có 2 × 4! = 48.. **Thông điệp:** ĐỌC ĐÚNG ĐỈNH CHUNG CỦA HAI ĐIỀU KIỆN.

- **Nhịp 5:** CẢ BA CẶP ĐỀU CẠNH NHAU?. Minh họa: A cạnh B, B cạnh C, A cạnh C.; Trong một hàng ba người chỉ có hai cặp kề.; Không có cách nào thỏa mãn.. **Thông điệp:** KHÔNG PHẢI HỆ ĐIỀU KIỆN NÀO CŨNG CÓ NGHIỆM.

- **Nhịp 6:** NHẬN DIỆN KHỐI CHỒNG LẤN. Minh họa: Vẽ đồ thị điều kiện kề.; Các cạnh AB và BC nối thành đường A–B–C.; Dựa vào cấu trúc để đếm thứ tự hợp lệ.. **Thông điệp:** VẼ ĐIỀU KIỆN TRƯỚC, RỒI MỚI GỘP.



### Chương 05 — 05 · ÍT NHẤT MỘT CẶP ĐỨNG CẠNH (bắt đầu khoảng 09:03)

- **Nhịp 1:** Ít NHẤT MỘT CẶP PHẢI KỀ. Minh họa: Sáu người A, B, C, D, E, F.; A đứng cạnh B hoặc C đứng cạnh D.; Có thể cả hai cặp cùng đứng cạnh.. **Thông điệp:** CHỮ HOẶC CẦN KIỂM TRA PHẦN GIAO.

- **Nhịp 2:** ĐẶT HAI BIẾN CỐ. Minh họa: E₁: A cạnh B.; E₂: C cạnh D.; Mỗi biến cố có 2 × 5! = 240.. **Thông điệp:** HAI SỐ 240 CHƯA PHẢI ĐÁP SỐ CẦN TÌM.

- **Nhịp 3:** TÍNH PHẦN GIAO. Minh họa: E₁ ∩ E₂: cả hai cặp đều kề.; Gộp [AB], [CD], E, F.; Phần giao có 2² × 4! = 96.. **Thông điệp:** PHẦN GIAO ĐÃ BỊ ĐẾM HAI LẦN.

- **Nhịp 4:** ÁP DỤNG BAO HÀM–LOẠI TRỪ. Minh họa: |E₁ ∪ E₂| = |E₁| + |E₂| − |E₁ ∩ E₂|.; Thay số: 240 + 240 − 96.; Kết quả 384 cách.. **Thông điệp:** TRỪ MỘT LẦN PHẦN GIAO ĐỂ HẾT ĐẾM TRÙNG.

- **Nhịp 5:** KHÔNG CẶP NÀO ĐƯỢC KỀ. Minh họa: Tất cả sáu người: 6! = 720.; Có ít nhất một cặp kề: 384.; Không cặp nào kề: 720 − 384 = 336.. **Thông điệp:** PHẦN BÙ LÀ CÁCH ĐẾM MẠNH KHI CÓ CHỮ KHÔNG.

- **Nhịp 6:** KIỂM CHỨNG BẰNG LIỆT KÊ. Minh họa: Duyệt tất cả 720 hoán vị.; Đếm riêng hai biến cố và phần giao.; 384 + 336 = 720.. **Thông điệp:** HAI NHÓM KẾT QUẢ PHÂN HOẠCH TOÀN BỘ CÁC HÀNG.



### Chương 06 — 06 · ĐÚNG MỘT CẶP ĐỨNG CẠNH (bắt đầu khoảng 11:19)

- **Nhịp 1:** ĐÚNG MỘT TRONG HAI CẶP. Minh họa: AB đứng kề hoặc CD đứng kề.; Nhưng không được đồng thời cả hai.; Đây là điều kiện hoặc loại trừ.. **Thông điệp:** KHÁC HẲN CỤM TỪ ÍT NHẤT MỘT.

- **Nhịp 2:** TRƯỜNG HỢP AB CÓ, CD KHÔNG. Minh họa: AB kề: 240 cách.; AB và CD cùng kề: 96 cách.; Còn 240 − 96 = 144 cách.. **Thông điệp:** TRỪ PHẦN GIAO NGAY TRONG NHÓM AB.

- **Nhịp 3:** TRƯỜNG HỢP CD CÓ, AB KHÔNG. Minh họa: Tương tự trường hợp trước.; Có 240 − 96 = 144 cách.; Hai trường hợp không giao nhau.. **Thông điệp:** DÙNG QUY TẮC CỘNG CHO HAI NHÓM RỜI NHAU.

- **Nhịp 4:** TỔNG HỢP KẾT QUẢ. Minh họa: Đúng một cặp kề: 144 + 144.; Kết quả 288 cách.; Có thể lấy 384 − 96 để kiểm tra.. **Thông điệp:** ĐẾM ĐÚNG MỘT = ĐẾM ÍT NHẤT MỘT − ĐẾM CẢ HAI.

- **Nhịp 5:** BÀI BIẾN THỂ: AB CÓ, CD KHÔNG. Minh họa: Không yêu cầu đổi vai trò hai cặp.; Chỉ đếm một trong hai nhóm.; Kết quả riêng là 144 cách.. **Thông điệp:** CẦN XEM ĐỀ NÓI ĐÚNG MỘT HAY ĐÚNG CẶP CHỈ ĐỊNH.

- **Nhịp 6:** NÂNG CAO: E ĐỨNG TRƯỚC F. Minh họa: AB và CD đều đứng cạnh nhau.; E phải xuất hiện trước F.; 96 : 2 = 48 cách.. **Thông điệp:** DÙNG PHÉP ĐỔI CHỖ E VÀ F ĐỂ CHIA ĐÔI.



### Chương 07 — 07 · GỘP KHỐI KHI XẾP VÒNG TRÒN (bắt đầu khoảng 13:35)

- **Nhịp 1:** KHI KHỐI ĐƯỢC XẾP QUANH BÀN. Minh họa: Sáu người ngồi bàn tròn không đánh số.; A và B bắt buộc ngồi kề.; Hai cách chỉ khác phép quay xem như một.. **Thông điệp:** KHÔNG ÁP DỤNG CÔNG THỨC HÀNG NGANG NGUYÊN XI.

- **Nhịp 2:** GỘP AB TRÊN BÀN TRÒN. Minh họa: Khối [AB], C, D, E, F.; Có 5 đối tượng trên vòng.; Chỉ xét phép quay: (5 − 1)! cách.. **Thông điệp:** CỐ ĐỊNH MỘT KHỐI LÀM MỐC.

- **Nhịp 3:** ĐẾM HAI CHIỀU TRONG KHỐI. Minh họa: AB hoặc BA vẫn khác nhau.; Nhân 2 với 4!.; Có 48 cách ngồi vòng.. **Thông điệp:** CÙNG LÀ 48 NHƯ VÍ DỤ NĂM NGƯỜI XẾP HÀNG, NHƯNG LÝ DO KHÁC.

- **Nhịp 4:** HAI KHỐI RỜI NHAU TRÊN VÒNG. Minh họa: [AB], [CD], E, F.; Bốn đối tượng vòng tròn: 3!.; Nhân 2² được 24 cách.. **Thông điệp:** CÔNG THỨC VÒNG TRÒN DÙNG (SỐ ĐỐI TƯỢNG − 1)!

- **Nhịp 5:** BA NGƯỜI LIỀN NHAU TRÊN VÒNG. Minh họa: [ABC] cùng D, E, F: 4 đối tượng.; 3! thứ tự vòng ngoài khối.; 3! thứ tự trong khối: 36 cách.. **Thông điệp:** ĐẾM VÒNG VÀ ĐẾM BÊN TRONG LÀ HAI BƯỚC.

- **Nhịp 6:** LƯU Ý NGƯỜI NÀO LÀM MỐC. Minh họa: Bàn tròn chỉ đồng nhất phép quay.; Không đồng nhất phép lật trái–phải.; Ghế đánh số thì cách đếm thay đổi.. **Thông điệp:** PHẢI NÊU RÕ QUY ƯỚC CỦA BÀI TOÁN VÒNG.



### Chương 08 — 08 · BA CẶP CẤM KỀ NHAU (bắt đầu khoảng 15:51)

- **Nhịp 1:** BÀI TỔNG HỢP BẢY NGƯỜI. Minh họa: A, B, C, D, E, F, G xếp hàng.; Không AB, không CD, không EF kề.; Tìm số cách hợp lệ.. **Thông điệp:** BA ĐIỀU KIỆN CẤM KHÔNG THỂ TRỪ ĐỘC LẬP.

- **Nhịp 2:** TỔNG VÀ MỘT BIẾN CỐ VI PHẠM. Minh họa: Tổng số hàng là 7! = 5040.; Mỗi cặp kề: 2 × 6! = 1440.; Ba cặp: trừ 3 × 1440.. **Thông điệp:** PHẢI ĐẾM ĐƯỢC CẢ TRƯỜNG HỢP GIAO NHAU.

- **Nhịp 3:** HAI CẶP CÙNG VI PHẠM. Minh họa: Chọn hai cặp trong ba: 3 cách.; Hai khối, còn 5 đối tượng.; Mỗi giao có 2² × 5! = 480.. **Thông điệp:** CỘNG LẠI VÌ VỪA BỊ TRỪ HAI LẦN.

- **Nhịp 4:** CẢ BA CẶP CÙNG VI PHẠM. Minh họa: Khối [AB], [CD], [EF], và G.; Có 4 đối tượng và 2³ dạng nội bộ.; Giao ba biến cố: 2³ × 4! = 192.. **Thông điệp:** TRỪ PHẦN GIAO BA LẦN CUỐI CÙNG.

- **Nhịp 5:** RÚT GỌN BIỂU THỨC. Minh họa: 5040 − 3×1440 + 3×480 − 192.; Tính được 1968.; Kiểm tra bằng liệt kê đủ 7! hàng.. **Thông điệp:** ĐÁP SỐ CUỐI CÙNG LÀ 1968 CÁCH.

- **Nhịp 6:** PHƯƠNG PHÁP CHO BÀI KHÓ TIẾP THEO. Minh họa: Nhận diện các nhóm bắt buộc / bị cấm.; Xét khối rời hay khối giao nhau.; Dùng phần bù và bao hàm–loại trừ khi cần.. **Thông điệp:** MỖI PHÉP NHÂN PHẢI GẮN VỚI MỘT SONG ÁNH ĐÚNG.



## Ghi chú sản xuất

1. Chương 01–04: cho người học nhìn thấy các thẻ nhập vào khối. Chuyển động hoán đổi phải thể hiện số thứ tự bên trong khối.
2. Chương 05–06: sơ đồ giao hai biến cố chỉ là biểu diễn quan hệ tập hợp, không ngụ ý diện tích các miền tỉ lệ với số cách.
3. Chương 07: phân biệt phép quay trên bàn tròn không đánh số với ghế đánh số; không tự ý đồng nhất phép phản xạ.
4. Chương 08: tại mỗi mức giao một/hai/ba biến cố có các khối phân biệt; mỗi thành phần giao được kiểm chứng bằng liệt kê toàn bộ 7! hoán vị.
5. Đề và câu hỏi phải hiện trước; công thức xuất hiện sau bước trực quan. Với ảnh preview, kiểm tra chữ không vượt khung cả hai cột.

## Kiểm tra toán học độc lập

- Năm người A, B phải đứng cạnh: \(2!\cdot 4!=48\).
- Sáu người A, B, C liên tiếp theo thứ tự tự do: \(3!\cdot 4!=144\); theo đúng thứ tự ABC: \(4!=24\).
- Hai khối [AB], [CD] trong sáu người: \(2^2\cdot4!=96\).
- A cạnh B và B cạnh C trong sáu người: \(2\cdot4!=48\).
- Ít nhất một trong AB, CD đứng cạnh: 384; không cặp nào: 336; đúng một: 288.
- Sáu người quanh bàn tròn không đánh số, AB kề: 48; AB và CD đều kề: 24.
- Bảy người, ba cặp AB, CD, EF đều không kề: \(7!-3(2\cdot6!)+3(2^2\cdot5!)-2^3\cdot4!=1968\).

**Trạng thái kiểm thử:** cần render Manim thực tế trên GitHub Actions để nghiệm thu hình ảnh và âm thanh. Kiểm thử Python không thay thế kiểm tra video.
