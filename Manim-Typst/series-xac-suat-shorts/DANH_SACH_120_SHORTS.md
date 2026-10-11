# DANH SÁCH 120 SHORTS · XÁC SUẤT 3 PHÚT

> Sinh tự động từ `shorts_plan.py` (`python shorts_plan.py`). Mọi đáp án đã được máy tính lại bằng liệt kê vét cạn, phân số chính xác hoặc mô phỏng có seed. Đừng sửa tay file này.

## L1 · Mở đầu (XSS001 – XSS015) · 30 – 60 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS001** | Ngẫu nhiên là gì? | Tung một đồng xu cân đối. Xác suất ra mặt ngửa? | 1/2 | coin | XS01 |
| **XSS002** | Mặt chẵn | Gieo một xúc xắc. Xác suất ra mặt chẵn? | 1/2 | die | XS04 |
| **XSS003** | Lớn hơn 4 | Gieo một xúc xắc. Xác suất số chấm lớn hơn 4? | 1/3 | die | XS04 |
| **XSS004** | Không gian mẫu | Tung hai đồng xu. Có bao nhiêu kết quả có thể? | 4 | tree | XS01 |
| **XSS005** | Bẫy của d'Alembert | Tung hai đồng xu. Xác suất được một sấp một ngửa? | 1/2 (không phải 1/3) | tree | XS04 |
| **XSS006** | Rút được át | Rút một lá từ bộ bài 52 lá. Xác suất được át? | 1/13 | cards | XS04 |
| **XSS007** | Rút được cơ | Rút một lá từ bộ bài 52 lá. Xác suất được lá cơ? | 1/4 | cards | XS04 |
| **XSS008** | Chắc chắn và không thể | Gieo một xúc xắc. P(số chấm ≤ 6) và P(số chấm = 7)? | 1 và 0 | die | XS02 |
| **XSS009** | Lấy một viên bi | Hộp có 3 bi đỏ, 2 bi xanh. Lấy 1 bi, xác suất được bi đỏ? | 3/5 | urn | XS04 |
| **XSS010** | Biến cố đối | Gieo một xúc xắc. Xác suất KHÔNG ra mặt 6? | 5/6 | die | XS06 |
| **XSS011** | 36 kết quả | Gieo hai xúc xắc. Không gian mẫu có bao nhiêu phần tử? | 36 | grid | XS01 |
| **XSS012** | Hai mặt giống nhau | Gieo hai xúc xắc. Xác suất hai mặt giống nhau? | 1/6 | grid | XS09 |
| **XSS013** | Tần suất khác xác suất | Tung đồng xu 100 lần được 47 lần ngửa. Tần suất ngửa? | 0,47 (xác suất vẫn là 0,5) | sim | XS05 |
| **XSS014** | Chia hết cho 3 | Chọn ngẫu nhiên một số từ 1 đến 20. Xác suất số đó chia hết cho 3? | 3/10 | grid | XS04 |
| **XSS015** | Sinh nhật cuối tuần | Sinh nhật năm nay của bạn rơi vào thứ Bảy hoặc Chủ nhật với xác suất bao nhiêu? | 2/7 | grid | XS04 |

## L2 · Cơ bản (XSS016 – XSS035) · 45 – 75 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS016** | Tổng bằng 7 | Gieo hai xúc xắc. Xác suất tổng bằng 7? | 1/6 | grid | XS09 |
| **XSS017** | Tổng bằng 8 | Gieo hai xúc xắc. Xác suất tổng bằng 8? | 5/36 | grid | XS09 |
| **XSS018** | Tổng nào hay gặp nhất? | Gieo hai xúc xắc. Tổng nào có xác suất lớn nhất? | 7 | grid | XS09 |
| **XSS019** | Đúng 2 mặt ngửa | Tung ba đồng xu. Xác suất có đúng 2 mặt ngửa? | 3/8 | tree | XS03 |
| **XSS020** | Ít nhất một ngửa | Tung ba đồng xu. Xác suất có ít nhất một mặt ngửa? | 7/8 | tree | XS06 |
| **XSS021** | Hai con đều trai | Gia đình có 2 con. Xác suất cả hai là con trai? | 1/4 | tree | XS03 |
| **XSS022** | Số chẵn từ 1 đến 5 | Lập số có 2 chữ số khác nhau từ 1, 2, 3, 4, 5. Xác suất số đó chẵn? | 2/5 | cards | XS08 |
| **XSS023** | Hai bi đỏ | Hộp 4 bi đỏ, 3 bi xanh. Lấy 2 bi. Xác suất cả hai đỏ? | 2/7 | urn | XS07 |
| **XSS024** | Hai bi khác màu | Hộp 4 bi đỏ, 3 bi xanh. Lấy 2 bi. Xác suất hai bi khác màu? | 4/7 | urn | XS07 |
| **XSS025** | Chọn hai bạn nữ | Lớp 30 bạn, 12 nữ. Chọn ngẫu nhiên 2 bạn. Xác suất cả hai là nữ? | 22/145 | urn | XS07 |
| **XSS026** | Hai lá át | Rút 2 lá từ bộ bài 52 lá. Xác suất được 2 lá át? | 1/221 | cards | XS07 |
| **XSS027** | Đứng đầu hàng | Xếp ngẫu nhiên A, B, C thành hàng. Xác suất A đứng đầu? | 1/3 | cards | XS08 |
| **XSS028** | Đứng cạnh nhau | Xếp ngẫu nhiên 4 bạn thành hàng. Xác suất A và B đứng cạnh nhau? | 1/2 | cards | XS08 |
| **XSS029** | Tích là số chẵn | Gieo hai xúc xắc. Xác suất tích hai số chấm là số chẵn? | 3/4 | grid | XS09 |
| **XSS030** | Ít nhất một con 6 | Gieo hai xúc xắc. Xác suất có ít nhất một mặt 6? | 11/36 | grid | XS06 |
| **XSS031** | Số chính phương | Chọn ngẫu nhiên một số từ 1 đến 100. Xác suất đó là số chính phương? | 1/10 | grid | XS04 |
| **XSS032** | Lần sau lớn hơn | Gieo xúc xắc hai lần. Xác suất lần hai lớn hơn lần một? | 5/12 | grid | XS09 |
| **XSS033** | Đoán mật khẩu | Mật khẩu 3 chữ số (000 – 999). Đoán một lần, xác suất đúng? | 1/1000 | cards | XS04 |
| **XSS034** | Tổng hai thẻ chẵn | Rút 2 thẻ từ 5 thẻ số 1 đến 5. Xác suất tổng chẵn? | 2/5 | cards | XS07 |
| **XSS035** | 2 sấp 2 ngửa | Tung bốn đồng xu. Xác suất được 2 sấp 2 ngửa? | 3/8 | tree | XS03 |

## L3 · Thông hiểu (XSS036 – XSS060) · 60 – 90 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS036** | Cược của de Méré (1) | Gieo xúc xắc 4 lần. Xác suất có ít nhất một mặt 6? | 671/1296 ≈ 0,518 | sim | XS06 |
| **XSS037** | Cược của de Méré (2) | Gieo hai xúc xắc 24 lần. Xác suất có ít nhất một lần đôi 6? | ≈ 0,491 (thua!) | sim | XS06 |
| **XSS038** | Thích Toán hoặc Anh | Lớp 40 bạn: 25 thích Toán, 20 thích Anh, 10 thích cả hai. Chọn 1 bạn: P(thích ít nhất một môn)? | 7/8 | venn | XS15 |
| **XSS039** | Át hoặc cơ | Rút một lá. Xác suất được át hoặc lá cơ? | 4/13 | cards | XS15 |
| **XSS040** | Chẵn hoặc lớn hơn 3 | Gieo một xúc xắc. Xác suất ra số chẵn hoặc lớn hơn 3? | 2/3 | venn | XS15 |
| **XSS041** | Hai xạ thủ cùng trúng | Hai xạ thủ bắn độc lập, trúng với xác suất 0,8 và 0,7. P(cả hai trúng)? | 0,56 | square | XS16 |
| **XSS042** | Ít nhất một viên trúng | Như trên: xác suất có ít nhất một viên trúng? | 0,94 | square | XS17 |
| **XSS043** | Đúng một viên trúng | Như trên: xác suất có đúng một viên trúng? | 0,38 | tree | XS17 |
| **XSS044** | Mạch nối tiếp | 3 linh kiện nối tiếp, mỗi cái hoạt động với xác suất 0,9 (độc lập). P(mạch chạy)? | 0,729 | circuit | XS17 |
| **XSS045** | Mạch song song | 2 linh kiện song song, mỗi cái 0,9. P(mạch chạy)? | 0,99 | circuit | XS17 |
| **XSS046** | Đoán mò cả 4 câu | Đoán mò 4 câu trắc nghiệm (4 phương án). P(đúng cả 4)? | 1/256 | tree | XS17 |
| **XSS047** | Đoán mò trúng ít nhất 1 | Đoán mò 4 câu. P(đúng ít nhất 1 câu)? | 175/256 | tree | XS17 |
| **XSS048** | Tung đến khi ngửa | Tung đồng xu đến khi ra ngửa. P(cần đúng 3 lần tung)? | 1/8 | tree | XS17 |
| **XSS049** | Đủ ba màu | Hộp 5 đỏ, 4 xanh, 3 vàng. Lấy 3 bi. P(đủ ba màu)? | 3/11 | urn | XS07 |
| **XSS050** | Có ít nhất một nữ | Chọn 3 người từ 6 nam, 4 nữ. P(có ít nhất 1 nữ)? | 5/6 | urn | XS11 |
| **XSS051** | Không ngồi cạnh nhau | Xếp 5 bạn vào hàng ghế. P(A và B không ngồi cạnh nhau)? | 3/5 | cards | XS08 |
| **XSS052** | Số chia hết cho 5 | Chọn ngẫu nhiên số có 3 chữ số khác nhau. P(chia hết cho 5)? | 17/81 | cards | XS08 |
| **XSS053** | Cùng nhóm | Chia 6 bạn thành 2 nhóm 3 người. P(A và B cùng nhóm)? | 2/5 | urn | XS10 |
| **XSS054** | Ba xúc xắc tổng 10 | Gieo ba xúc xắc. P(tổng bằng 10)? | 1/8 | grid | XS09 |
| **XSS055** | Ba mặt khác nhau | Gieo ba xúc xắc. P(ba mặt đôi một khác nhau)? | 5/9 | grid | XS09 |
| **XSS056** | Hoàn lại hay không? | Hộp 3 đỏ 2 xanh, rút 2 bi. P(2 đỏ) khi có hoàn lại và khi không hoàn lại? | 9/25 và 3/10 | urn | XS12 |
| **XSS057** | Hợp của hai độc lập | A, B độc lập, P(A) = 0,4; P(B) = 0,5. Tính P(A ∪ B). | 0,7 | venn | XS16 |
| **XSS058** | Xung khắc có độc lập? | A, B xung khắc và đều có xác suất dương. Chúng có độc lập không? | Không | venn | XS23 |
| **XSS059** | Tích chia hết cho 3 | Chọn 2 số khác nhau từ 1 đến 10. P(tích chia hết cho 3)? | 8/15 | grid | XS11 |
| **XSS060** | Hai mặt sát nhau | Gieo hai xúc xắc. P(hai số chấm hơn kém nhau không quá 1)? | 4/9 | grid | XS09 |

## L4 · Vận dụng (XSS061 – XSS085) · 75 – 120 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS061** | Biết tổng bằng 8 | Gieo hai xúc xắc, biết tổng bằng 8. P(có một mặt 3)? | 2/5 | grid | XS20 |
| **XSS062** | Biết có ít nhất một trai | Gia đình 2 con, biết có ít nhất một con trai. P(cả hai là trai)? | 1/3 | tree | XS20 |
| **XSS063** | Biết con cả là trai | Gia đình 2 con, biết con cả là trai. P(cả hai là trai)? | 1/2 | tree | XS20 |
| **XSS064** | P(A|B) khác P(B|A) | 60 nam (24 đeo kính), 40 nữ (16 đeo kính). P(kính \| nam) và P(nam \| kính)? | 0,4 và 0,6 | table | XS21 |
| **XSS065** | Rút liên tiếp 2 đỏ | Hộp 5 đỏ, 3 xanh, rút lần lượt 2 bi không hoàn lại. P(cả hai đỏ)? | 5/14 | tree | XS22 |
| **XSS066** | Lần hai cũng như lần một | Như trên: xác suất bi thứ hai là đỏ? | 5/8 | tree | XS22 |
| **XSS067** | Nhìn ngược thời gian | Như trên: biết bi thứ hai đỏ, P(bi thứ nhất đỏ)? | 4/7 | tree | XS25 |
| **XSS068** | Phế phẩm từ đâu ra? | Xưởng I làm 60 % sản phẩm (2 % lỗi), xưởng II 40 % (5 % lỗi). P(một sản phẩm bị lỗi)? | 0,032 | tree | XS24 |
| **XSS069** | Truy nguồn phế phẩm | Như trên: biết sản phẩm bị lỗi, P(nó từ xưởng II)? | 0,625 | square | XS25 |
| **XSS070** | Dương tính có chắc bệnh? | Bệnh 1 %, xét nghiệm nhạy 99 %, dương tính giả 5 %. Dương tính thì P(bệnh)? | 1/6 ≈ 0,17 | square | XS25 |
| **XSS071** | Xét nghiệm lần hai | Như trên, xét nghiệm lần hai (độc lập) cũng dương tính. P(bệnh)? | ≈ 0,80 | square | XS27 |
| **XSS072** | Chọn hộp rồi rút bi | Hộp I: 3 đỏ 2 xanh; hộp II: 1 đỏ 4 xanh. Chọn ngẫu nhiên một hộp rồi rút 1 bi. P(đỏ)? | 2/5 | tree | XS24 |
| **XSS073** | Bi đỏ từ hộp nào? | Như trên: biết rút được bi đỏ, P(bi từ hộp I)? | 3/4 | tree | XS25 |
| **XSS074** | Chuyển một bi | Hộp I: 3 đỏ 2 xanh; hộp II: 2 đỏ 2 xanh. Chuyển 1 bi từ I sang II rồi rút 1 bi từ II. P(đỏ)? | 13/25 | tree | XS26 |
| **XSS075** | Qua hai vòng thi | Qua vòng 1 với xác suất 0,8; đã qua vòng 1 thì qua vòng 2 với xác suất 0,6. P(qua cả hai)? | 0,48 | tree | XS22 |
| **XSS076** | Mưa và tắc đường | P(mưa) = 0,3; tắc đường khi mưa 0,6, khi không mưa 0,2. P(tắc đường)? | 0,32 | tree | XS24 |
| **XSS077** | Tắc đường vì mưa? | Như trên: biết hôm nay tắc đường, P(trời mưa)? | 9/16 | square | XS25 |
| **XSS078** | Lọc thư rác | 40 % thư là rác; chữ "khuyến mãi" có trong 30 % thư rác và 3 % thư thường. Thấy chữ đó: P(rác)? | 20/23 ≈ 0,87 | square | XS27 |
| **XSS079** | Độc lập bất ngờ | Gieo hai xúc xắc. A = "lần 1 chẵn", B = "tổng chẵn". A và B có độc lập? | Có | grid | XS23 |
| **XSS080** | Rút thăm trước hay sau? | 3 người lần lượt rút 3 lá thăm, chỉ 1 lá trúng. P(người thứ ba trúng)? | 1/3 | tree | XS22 |
| **XSS081** | Lần thứ 3 mới gặp lỗi | 10 sản phẩm có 3 lỗi, kiểm tra lần lượt. P(lần thứ 3 mới gặp sản phẩm lỗi đầu tiên)? | 7/40 | tree | XS22 |
| **XSS082** | Ba viên đạn | Mỗi viên trúng đích với xác suất 0,6; bắn đến khi trúng, tối đa 3 viên. P(trúng đích)? | 0,936 | tree | XS17 |
| **XSS083** | Từ P(A|B) ra P(A ∪ B) | P(A) = 0,5; P(B) = 0,4; P(A\|B) = 0,3. Tính P(A ∪ B). | 0,78 | venn | XS22 |
| **XSS084** | Ai bắn trúng? | Hai xạ thủ 0,8 và 0,7; biết có đúng một viên trúng. P(người thứ nhất trúng)? | 12/19 | tree | XS25 |
| **XSS085** | Đồng xu hai mặt ngửa | 2 đồng xu thường, 1 đồng hai mặt ngửa. Chọn 1 đồng, tung được ngửa. P(đó là đồng hai mặt ngửa)? | 1/2 | tree | XS25 |

## L5 · Khó (XSS086 – XSS105) · 90 – 150 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS086** | Monty Hall | 3 cửa, 1 xe. Bạn chọn cửa 1, người dẫn mở một cửa có dê. Đổi cửa thì P(thắng)? | 2/3 | sim | XS27 |
| **XSS087** | Nghịch lý ngày sinh | Lớp 23 người. P(có hai người trùng ngày sinh)? | ≈ 0,507 | curve | XS13 |
| **XSS088** | Cần bao nhiêu người? | Cần ít nhất bao nhiêu người để P(trùng ngày sinh) > 99 %? | 57 | curve | XS13 |
| **XSS089** | Bốn cặp vợ chồng | 4 cặp vợ chồng xếp hàng ngang ngẫu nhiên. P(mọi cặp đều ngồi cạnh nhau)? | 1/105 | cards | XS12 |
| **XSS090** | Thư bỏ nhầm phong bì | 4 lá thư bỏ ngẫu nhiên vào 4 phong bì. P(không lá nào đúng địa chỉ)? | 3/8 | cards | XS13 |
| **XSS091** | Con số 1/e | n lá thư, n phong bì, n rất lớn. P(không lá nào đúng) tiến về đâu? | 1/e ≈ 0,368 | curve | XS13 |
| **XSS092** | Chia tiền cược | Ai thắng trước 3 ván được thưởng; A thắng 2, B thắng 1 thì dừng. Chia thưởng theo P(A thắng)? | 3/4 | tree | XS22 |
| **XSS093** | Đi ngẫu nhiên | Mỗi bước tiến hoặc lùi 1 với xác suất 1/2. P(sau 4 bước về đúng chỗ cũ)? | 3/8 | tree | XS18 |
| **XSS094** | Hộp của Bertrand | 3 hộp: 2 vàng, 2 bạc, 1 vàng 1 bạc. Chọn hộp, rút được đồng vàng. P(đồng còn lại cũng vàng)? | 2/3 | tree | XS25 |
| **XSS095** | Con trai sinh thứ Ba | Gia đình 2 con, biết có một con trai sinh vào thứ Ba. P(cả hai là trai)? | 13/27 | grid | XS20 |
| **XSS096** | Gieo đến khi ra 6 | Gieo xúc xắc đến khi ra 6. P(số lần gieo là số chẵn)? | 5/11 | tree | XS18 |
| **XSS097** | Ai ngửa trước thắng | A và B lần lượt tung đồng xu, A tung trước, ai ra ngửa trước thắng. P(A thắng)? | 2/3 | tree | XS18 |
| **XSS098** | Tổng 7 hay tổng 8 trước? | Gieo liên tục hai xúc xắc. P(tổng 7 xuất hiện trước tổng 8)? | 6/11 | grid | XS20 |
| **XSS099** | Tam giác đều trong lục giác | Chọn ngẫu nhiên 3 đỉnh của lục giác đều. P(được tam giác đều)? | 1/10 | geo | XS07 |
| **XSS100** | Tam giác vuông trong bát giác | Chọn 3 đỉnh của bát giác đều. P(được tam giác vuông)? | 3/7 | geo | XS07 |
| **XSS101** | Bàn tròn 6 người | 6 người ngồi ngẫu nhiên quanh bàn tròn. P(A và B ngồi cạnh nhau)? | 2/5 | geo | XS12 |
| **XSS102** | Thùng 5 lá | Rút 5 lá từ bộ bài 52 lá. P(5 lá cùng chất)? | 33/16660 ≈ 0,002 | cards | XS07 |
| **XSS103** | Ba máy sản xuất | Máy I, II, III làm 50 %, 30 %, 20 % sản phẩm, lỗi 1 %, 2 %, 3 %. Sản phẩm lỗi: P(từ máy III)? | 6/17 | square | XS26 |
| **XSS104** | Chuyển hai bi | Hộp I: 4 đỏ 2 xanh; hộp II: 3 đỏ 3 xanh. Chuyển 2 bi từ I sang II rồi rút 1 bi từ II. P(đỏ)? | 13/24 | tree | XS26 |
| **XSS105** | Bayes sau khi chuyển bi | Như trên: biết bi rút ra là đỏ, P(hai bi đã chuyển đều đỏ)? | 6/13 | tree | XS26 |

## L6 · Rất khó (XSS106 – XSS120) · 120 – 180 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS106** | Bẻ que thành tam giác | Bẻ que tại 2 điểm ngẫu nhiên. P(ba đoạn tạo thành tam giác)? | 1/4 | geo | XS30 |
| **XSS107** | Cây kim của Buffon | Thả kim dài bằng khoảng cách các đường kẻ song song. P(kim cắt một đường kẻ)? | 2/π ≈ 0,637 | sim | XS30 |
| **XSS108** | Hẹn gặp trong một giờ | Hai người đến ngẫu nhiên trong 1 giờ, mỗi người chờ 15 phút. P(gặp nhau)? | 7/16 | square | XS30 |
| **XSS109** | Đo số π bằng xác suất | Chọn điểm ngẫu nhiên trong hình vuông. P(điểm nằm trong hình tròn nội tiếp)? | π/4 ≈ 0,785 | sim | XS05 |
| **XSS110** | Con bạc phá sản | Có 2 đồng, mỗi ván thắng/thua 1 đồng (1/2). Dừng khi có 5 đồng hoặc hết tiền. P(đạt 5 đồng)? | 2/5 | tree | XS30 |
| **XSS111** | Kiểm phiếu | A được 3 phiếu, B được 2 phiếu, kiểm ngẫu nhiên. P(A luôn dẫn trước suốt quá trình)? | 1/5 | tree | XS30 |
| **XSS112** | Bao lâu ra mặt 6? | Gieo xúc xắc đến khi ra 6. Trung bình cần bao nhiêu lần? | 6 | sim | XS30 |
| **XSS113** | Sưu tầm đủ 6 mặt | Gieo xúc xắc đến khi thấy đủ cả 6 mặt. Trung bình cần bao nhiêu lần? | 14,7 | sim | XS30 |
| **XSS114** | Trò chơi Penney | Tung đồng xu liên tục. P(cặp "sấp – ngửa" xuất hiện trước cặp "ngửa – ngửa")? | 3/4 | sim | XS30 |
| **XSS115** | Tam giác nhọn trên đường tròn | Chọn 3 điểm ngẫu nhiên trên đường tròn. P(tam giác nhọn)? | 1/4 | geo | XS30 |
| **XSS116** | Vị trí lá át đầu tiên | Xáo bộ bài 52 lá, lật dần. Trung bình lá át đầu tiên ở vị trí thứ mấy? | 53/5 = 10,6 | cards | XS30 |
| **XSS117** | Xét nghiệm bao nhiêu lần? | Bệnh 1 %, nhạy 99 %, dương tính giả 5 %. Cần mấy lần dương tính liên tiếp để P(bệnh) > 99 %? | 4 | square | XS27 |
| **XSS118** | Galilei và ba xúc xắc | Gieo ba xúc xắc. Tổng 9 hay tổng 10 dễ ra hơn? | Tổng 10 (27/216 so với 25/216) | grid | XS09 |
| **XSS119** | Bình của Pólya | Bình 1 đỏ 1 xanh; rút 1 bi, trả lại kèm 1 bi cùng màu; làm 10 lần. P(có đúng k bi đỏ thêm vào)? | 1/11 với mọi k | urn | XS30 |
| **XSS120** | Nguyên tố cùng nhau | Chọn hai số nguyên dương ngẫu nhiên. P(chúng nguyên tố cùng nhau)? | 6/π² ≈ 0,608 | grid | XS30 |
