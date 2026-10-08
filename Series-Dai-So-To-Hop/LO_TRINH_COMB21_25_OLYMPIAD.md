# SANG MATH · ĐẠI SỐ TỔ HỢP · 5 TẬP CHUYÊN SÂU CUỐI (COMB21–25)

**Định hướng:** Vận dụng cao → HSG chuyên → Olympic. Kế thừa cả 20 video đầu, không lặp lại các chứng minh cơ bản. Mỗi tập hướng tới 18–25 phút (thực tế tùy lời đọc), có ít nhất một bài toán giải bằng hai cách độc lập và kiểm thử các trường hợp nhỏ bằng Python.

**Quy ước ký hiệu toàn Series:** `C^(n)_(k)` và `A^(n)_(k)` trong Typst; n ở trên, k ở dưới theo đúng yêu cầu của người dùng. Toàn bộ khung hình 1920×1080; hình trái, đề bài và chứng minh phải; không đè chữ lên hình.

## COMB21 · HÀM SINH (GENERATING FUNCTIONS) — từ hệ số đến công thức đóng

**Nhiệm vụ sư phạm:** hiểu công cụ biến một dãy số thành hàm số; đếm bằng lấy hệ số thay vì đếm trực tiếp.

1. Hàm sinh thường OGF: `A(x)=Σ a_n x^n`, đọc hệ số như một bài toán đếm.
2. Các hàm sinh chuẩn: `1/(1-x)`, `1/(1-x)^m`, `1/(1-x-x²)`; chứng minh trên một miền hội tụ phù hợp hoặc bằng chuỗi hình thức.
3. Phép cộng, tích và phép chập: giải thích nhân hàm sinh bằng chọn tổng chỉ số.
4. Đếm số nghiệm nguyên không âm, biến thể sao–vạch và giới hạn trên từng biến.
5. Biến đổi dịch chỉ số, đạo hàm, tích phân trên hàm sinh.
6. Phân tích phân thức thành phần đơn giản, khai triển và tìm công thức đóng của một dãy truy hồi.
7. Hàm sinh mũ EGF cho cấu trúc có nhãn; vì sao xuất hiện hệ số `1/n!`.
8. Capstone HSG: hai lời giải cho bài đếm dãy bước 1 hoặc 2, trong đó có điều kiện chính xác số bước 2; so sánh OGF và đếm trực tiếp.

**Animation:** “băng chuyền hệ số”, hai dãy số chập thành một, các đồng xu tạo thành mũi tên đến hệ số cần tìm.

## COMB22 · QUY HOẠCH ĐỘNG TỔ HỢP (DP) VÀ MA TRẬN CHUYỂN

1. Ý tưởng trạng thái: `dp[i][state]` phải xác định được đối tượng đang đếm.
2. Truy hồi Fibonacci từ lát gạch 1×n; hai cách đếm.
3. Đếm xâu nhị phân không có hai số 1 kề nhau, trạng thái kết thúc 0/1.
4. Xâu tránh mẫu `101`: tự động trạng thái biểu diễn tiền tố khớp dài nhất.
5. Bài toán bước đi trên lưới, vật cản và các điều kiện đường đi.
6. DP theo tổng hoặc theo số phần tử đã chọn; đối chiếu hàm sinh.
7. Ma trận chuyển, luỹ thừa ma trận, tính số cách với n rất lớn.
8. Capstone Olympic: đếm xâu dài n tránh đồng thời nhiều mẫu cho trước bằng automaton và ma trận; xác minh `n≤12` bằng liệt kê brute force.

**Animation:** bảng trạng thái phát sáng, mũi tên chuyển, các đường đi bị cấm xóa dần; ma trận được nhân với vector trạng thái từng bước.

## COMB23 · BAO HÀM–LOẠI TRỪ CỰC TRỊ, DERANGEMENTS, ROOK POLYNOMIALS

1. Vì sao đếm phần bù có nhiều điều kiện giao nhau không thể trừ máy móc.
2. Công thức bao hàm–loại trừ tổng quát cho n biến cố, chứng minh bằng hệ số xuất hiện của một đối tượng.
3. Hoán vị không điểm cố định: `D_n=n! Σ_{k=0}^n (-1)^k/k!`.
4. Số điểm cố định đúng r: công thức rencontres với `C^(n)_(r)D_{n-r}`.
5. Bàn cờ cấm: dấu chấm cấm trên ma trận phân công người–việc.
6. Đa thức xe R(x): số cách đặt k xe trên các ô cấm, không cùng hàng hoặc cột.
7. Đếm các hoán vị tránh ô cấm bằng `Σ(-1)^k r_k(n-k)!`.
8. Capstone: bài phân công có các dải cấm và cấm trùng lặp, kiểm chứng bằng Python duyệt tất cả hoán vị khi n nhỏ.

**Animation:** ma trận bảng cấm, các quân xe được đặt từng bước; phép bao hàm–loại trừ thay đổi dấu và xoá phần giao.

## COMB24 · CATALAN, ĐƯỜNG ĐI DYCK, NGUYÊN LÝ PHẢN XẠ VÀ SONG ÁNH

1. Đếm các dãy dấu ngoặc đúng, phân biệt dãy hợp lệ và sai tại tiền tố đầu tiên.
2. Lưới đường đi không vượt đường chéo; nguyên lý phản xạ biến đường sai thành đường đặc biệt.
3. Tìm Catalan `Cat_n = C^(2n)_(n) - C^(2n)_(n+1) = C^(2n)_(n)/(n+1)`.
4. Hệ thức truy hồi Catalan bằng lần ghép cặp dấu ngoặc đầu tiên.
5. Các tam giác hoá đa giác lồi; song ánh với ngoặc đúng.
6. Cây nhị phân phẳng và cách mã hoá đường Dyck.
7. Bài toán lá phiếu Bertrand (Ballot Problem), điều kiện nghiêm ngặt và không nghiêm ngặt.
8. Capstone HSG: đồng nhất thức Catalan bằng hai song ánh khác nhau, kiểm tra số trường hợp nhỏ.

**Animation:** đường đi bị phản xạ qua đường chéo, dấu ngoặc chuyển thành cây, đa giác hiện các đường chéo không cắt nhau.

## COMB25 · BURNSIDE – PÓLYA – CĂN ĐƠN VỊ: BỘ CÔNG CỤ OLYMPIC

1. Khi nào hai cách tô màu chỉ khác phép quay là cùng một cấu hình.
2. Đếm số cấu hình bất biến dưới một phép quay.
3. Bổ đề Burnside: trung bình số cấu hình cố định bởi mỗi đối xứng.
4. Dây chuyền hạt, phép quay và lật, phân biệt nhóm cyclic/dihedral.
5. Chu trình của hoán vị và đa thức chỉ số chu trình (cycle index).
6. Định lý Pólya để đếm các cấu hình tô màu không phân biệt đối xứng.
7. Bộ lọc căn bậc m của đơn vị: chỉ lấy hệ số có bậc đồng dư một số dư cố định modulo m.
8. Capstone Olympic: đối chiếu Burnside/Pólya với liệt kê quỹ đạo độc lập; thêm ràng buộc số hạt mỗi màu hoặc tổng trọng số modulo m.

**Animation:** nhóm tác động trực tiếp lên vòng hạt, đỉnh và cạnh hình vuông; cấu hình cố định được giữ sáng, các bản quay tương đương chập thành một quỹ đạo.

## Checklist kỹ thuật cho 21–25

- Các chứng minh cần phân biệt kỹ song ánh, đếm đôi, phân hoạch và bao hàm–loại trừ; công thức phải ghi đúng điều kiện áp dụng.
- Mỗi công thức trọng tâm có kiểm thử brute force tối thiểu ở miền n nhỏ hoặc một kiểm chứng số học độc lập.
- Quy hoạch động phải giải thích *trạng thái đủ thông tin* và vì sao không đếm trùng.
- Hàm sinh phải phân biệt chuỗi hình thức với phân tích hội tụ nếu trình bày giải tích.
- Nhóm đối xứng phải nêu rõ được phép quay, lật hay ghế/vị trí đã có nhãn.
- Cảnh 3D nếu có chỉ dùng khi mô hình cần phép đối xứng không gian; giữ camera ổn định và không hy sinh tính chính xác.
- Sau mỗi video: kiểm thử Python → biên dịch Typst → render preview → QA ảnh/timing/audio → Full HD.

**Tình trạng:** đây là *đề cương để sản xuất COMB21–COMB25*, chưa phải mã nguồn hay MP4 của năm video ấy. Bộ code sẽ được thực hiện theo thứ tự sau khi nghiệm thu COMB20.
