# DANH SÁCH 440 SHORTS · XÁC SUẤT 3 PHÚT

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
| **XSS083** | Từ điều kiện tới phép hợp | P(A) = 0,5; P(B) = 0,4; P(A\|B) = 0,3. Tính P(A ∪ B). | 0,78 | venn | XS22 |
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
| **XSS091** | Hằng số e xuất hiện | n lá thư, n phong bì, n rất lớn. P(không lá nào đúng) tiến về đâu? | 1/e ≈ 0,368 | curve | XS13 |
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

## L7 · Sơ đồ cây (XSS121 – XSS140) · 60 – 120 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS121** | Ba phát, trúng đúng hai | Xạ thủ bắn 3 phát, mỗi phát trúng 0,6, độc lập. P(trúng đúng 2 phát)? | 0,432 | tree | XS18 |
| **XSS122** | Trung bình rút mấy lần? | Hộp 2 đỏ 3 xanh, rút lần lượt không hoàn lại đến khi được bi đỏ. Trung bình rút mấy lần? | 2 | tree | XS22 |
| **XSS123** | Ném rổ tối đa ba lần | Ném rổ đến khi vào, tối đa 3 lần, mỗi lần vào 0,7. P(ném vào)? | 0,973 | tree | XS06 |
| **XSS124** | Thi bằng lái ba lần | Lần 1 đậu 0,6; trượt thì lần 2 đậu 0,7; trượt nữa thì lần 3 đậu 0,8. P(đậu)? | 0,976 | tree | XS22 |
| **XSS125** | Mưa hai ngày tới | Hôm nay mưa. Mưa thì mai mưa 0,6; tạnh thì mai mưa 0,2. P(ngày kia mưa)? | 0,44 | tree | XS24 |
| **XSS126** | Thắng 2 trong 3 ván | A thắng mỗi ván 0,6. Ai thắng 2 ván trước là vô địch. P(A vô địch)? | 0,648 | tree | XS18 |
| **XSS127** | Vì sao chung kết đánh 5 ván? | A thắng mỗi ván 0,6. Ai thắng 3 ván trước là vô địch. P(A vô địch)? | ≈ 0,683 | tree | XS18 |
| **XSS128** | Không hai ngửa liền nhau | Tung đồng xu 4 lần. P(không có hai lần ngửa liên tiếp)? | 1/2 | tree | XS03 |
| **XSS129** | Rút rồi đổi màu | Hộp 2 đỏ 1 xanh. Rút 1 bi, thay bằng 1 bi màu kia, rồi rút tiếp. P(lần hai được đỏ)? | 5/9 | tree | XS24 |
| **XSS130** | Xúc xắc chọn hộp | Gieo xúc xắc: 1–2 chọn hộp A (1 đỏ 1 xanh), 3–5 hộp B (2 đỏ 1 xanh), 6 hộp C (3 đỏ). P(đỏ)? | 2/3 | tree | XS24 |
| **XSS131** | Oẳn tù tì ba người | Ba người oẳn tù tì một lượt. P(hòa: cả ba giống nhau hoặc đủ ba kiểu)? | 1/3 | tree | XS09 |
| **XSS132** | Ba người thi tung xu | A, B, C lần lượt tung đồng xu, ai ra ngửa trước thắng. P(A thắng)? | 4/7 | tree | XS18 |
| **XSS133** | Rút đến khi đủ hai đỏ | Hộp 2 đỏ 2 xanh, rút lần lượt không hoàn lại đến khi đủ 2 bi đỏ. P(dừng ở lần thứ 3)? | 1/3 | tree | XS22 |
| **XSS134** | Đồng xu quyết định | Tung xu: ngửa thì gieo 1 xúc xắc, sấp thì gieo 2 xúc xắc. P(tổng số chấm bằng 6)? | 11/72 | tree | XS24 |
| **XSS135** | Ra 6 vì tung ngửa? | Như trên, biết tổng số chấm bằng 6. P(đồng xu đã ra ngửa)? | 6/11 | tree | XS25 |
| **XSS136** | Máy dự phòng | Máy chính hỏng 0,1; khi đó máy phụ khởi động được 0,8 và chạy tốt 0,9. P(hệ thống vẫn chạy)? | 0,972 | tree | XS22 |
| **XSS137** | Phong độ ảnh hưởng | Trận 1 thắng 0,5. Thắng trận trước thì trận sau thắng 0,7, thua thì 0,4. P(thắng đúng 2/3 trận)? | 0,305 | tree | XS22 |
| **XSS138** | Con kiến trên hình lập phương | Kiến ở một đỉnh hình lập phương, mỗi bước bò sang đỉnh kề ngẫu nhiên. P(sau 3 bước ở đỉnh đối diện)? | 2/9 | tree | XS30 |
| **XSS139** | Tennis: điểm deuce | Đang deuce, A thắng mỗi điểm 0,6; ai hơn 2 điểm thắng game. P(A thắng game)? | 9/13 | tree | XS30 |
| **XSS140** | Con kiến trên tam giác | Kiến ở một đỉnh tam giác, mỗi bước sang một đỉnh khác ngẫu nhiên. P(sau 5 bước về chỗ cũ)? | 5/16 | tree | XS30 |

## L8 · Có điều kiện (XSS141 – XSS160) · 60 – 120 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS141** | Biết có mặt 6 | Gieo 2 xúc xắc, biết có ít nhất một mặt 6. P(tổng ≥ 10)? | 5/11 | grid | XS20 |
| **XSS142** | Đảo điều kiện | Gieo 2 xúc xắc, biết tổng ≥ 10. P(có ít nhất một mặt 6)? | 5/6 | grid | XS20 |
| **XSS143** | Đọc bảng hai chiều | Lớp 40 bạn: 24 nữ, 16 nam; 12 nữ và 8 nam thích Toán. Gặp bạn thích Toán: P(là nữ)? | 3/5 | table | XS21 |
| **XSS144** | Học thêm cả hai môn | 60 % học sinh học thêm Toán; trong số đó 70 % học thêm Lý. P(học thêm cả Toán và Lý)? | 0,42 | tree | XS22 |
| **XSS145** | Biết có ít nhất một ngửa | Tung đồng xu 3 lần, biết có ít nhất một lần ngửa. P(cả 3 lần ngửa)? | 1/7 | tree | XS20 |
| **XSS146** | Biết có một lá át | Rút 2 lá từ bộ 52 lá, biết có ít nhất một lá át. P(cả hai là át)? | 1/33 | cards | XS20 |
| **XSS147** | Biết có át bích | Rút 2 lá, biết trong đó có át bích. P(cả hai là át)? | 1/17 | cards | XS28 |
| **XSS148** | Hai mặt khác nhau | Gieo 2 xúc xắc, biết hai mặt khác nhau. P(tổng bằng 7)? | 1/5 | grid | XS20 |
| **XSS149** | Ba lá cơ liên tiếp | Rút lần lượt 3 lá không hoàn lại. P(cả 3 lá đều là cơ)? | 11/850 | cards | XS22 |
| **XSS150** | Biết tích chẵn | Gieo 2 xúc xắc, biết tích hai số chấm là số chẵn. P(tổng là số chẵn)? | 1/3 | grid | XS20 |
| **XSS151** | Chỉ một mũi tên trúng | A trúng 0,8, B trúng 0,6, mỗi người bắn 1 mũi. Biết bia trúng đúng 1 mũi. P(mũi đó của A)? | 8/11 | tree | XS25 |
| **XSS152** | Bia đã bị trúng | A trúng 0,8, B trúng 0,6, mỗi người bắn 1 mũi. Biết bia bị trúng. P(cả hai cùng trúng)? | 12/23 | tree | XS20 |
| **XSS153** | Người sau trúng thăm | 10 lá thăm có 3 lá trúng, rút lần lượt. Biết người thứ 2 trúng: P(người thứ 1 cũng trúng)? | 2/9 | urn | XS20 |
| **XSS154** | Biết tổng chẵn | Gieo 2 xúc xắc, biết tổng là số chẵn. P(cả hai mặt đều là 6)? | 1/18 | grid | XS20 |
| **XSS155** | Hai lần ngửa liên tiếp | Một xu chuẩn, một xu hai mặt ngửa. Chọn 1 đồng, tung 2 lần đều ngửa. P(đã chọn xu chuẩn)? | 1/5 | tree | XS25 |
| **XSS156** | Ít nhất hai con trai | Gia đình 3 con, biết có ít nhất 2 con trai. P(cả 3 đều là trai)? | 1/4 | tree | XS20 |
| **XSS157** | Đôi một độc lập | Tung 2 xu. A: xu 1 ngửa; B: xu 2 ngửa; C: hai xu giống nhau. A, B, C có độc lập (cả ba) không? | Không (chỉ đôi một độc lập) | grid | XS23 |
| **XSS158** | Biết có đúng 3 ngửa | Tung xu 5 lần, biết có đúng 3 lần ngửa. P(lần đầu ra ngửa)? | 3/5 | tree | XS20 |
| **XSS159** | Biết có bi đỏ | Hộp 3 đỏ 2 xanh, rút 2 bi, biết có ít nhất 1 bi đỏ. P(cả hai đỏ)? | 1/3 | urn | XS20 |
| **XSS160** | Hai nhân chứng | Sự kiện xảy ra với xác suất 1/2. A nói thật 3/4, B nói thật 4/5, cả hai nói "có". P(thật sự có)? | 12/13 | tree | XS27 |

## L9 · Toàn phần – Bayes (XSS161 – XSS175) · 75 – 150 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS161** | Đi học muộn | 40 % đi xe buýt; đi muộn 10 % nếu đi buýt, 5 % nếu tự đi. P(một bạn đi muộn)? | 0,07 | tree | XS24 |
| **XSS162** | Muộn vì xe buýt? | Như trên, biết bạn đó đi muộn. P(bạn đi xe buýt)? | 4/7 | tree | XS25 |
| **XSS163** | Nhân chứng taxi | 85 % taxi màu xanh lá, 15 % xanh dương; nhân chứng nhận đúng màu 80 %. Nói "xanh dương": P(đúng)? | 12/29 ≈ 0,41 | square | XS27 |
| **XSS164** | Biết hay đoán mò? | Học sinh biết đáp án 60 %, không biết thì đoán 1 trong 4. Trả lời đúng: P(thật sự biết)? | 6/7 | tree | XS25 |
| **XSS165** | Dự báo có mưa | Ngày mưa 20 %. Mưa thì đài báo mưa 90 %, tạnh vẫn báo mưa 30 %. Đài báo mưa: P(mưa)? | 3/7 | tree | XS27 |
| **XSS166** | Ba nhà cung cấp | Đèn từ 3 nơi: 45 %, 35 %, 20 %; đạt chuẩn 98 %, 96 %, 95 %. P(đèn đạt chuẩn)? | 0,967 | tree | XS26 |
| **XSS167** | Tìm ngược tỉ lệ lỗi | Máy A làm 60 % sản phẩm, lỗi 2 %; tỉ lệ lỗi chung là 3 %. Tỉ lệ lỗi của máy B? | 4,5 % | tree | XS24 |
| **XSS168** | Hai bi đỏ từ hộp nào? | Hộp I: 2 đỏ 3 xanh; hộp II: 3 đỏ 2 xanh. Chọn hộp, rút 2 bi đều đỏ. P(hộp II)? | 3/4 | tree | XS25 |
| **XSS169** | Tín hiệu bị nhiễu | Gửi bit 1 với xác suất 0,3, bit 0 với 0,7; mỗi bit bị lật 10 %. Nhận 1: P(đã gửi 1)? | 27/34 | tree | XS27 |
| **XSS170** | Gửi lặp hai lần | Như trên nhưng gửi mỗi bit 2 lần, nhận được "1 1". P(đã gửi 1)? | 243/250 = 0,972 | tree | XS27 |
| **XSS171** | Câu hỏi nhạy cảm | Tung xu: ngửa thì trả lời thật "có quay cóp không?", sấp thì nói "có". 60 % nói "có". Tỉ lệ quay cóp? | 20 % | tree | XS24 |
| **XSS172** | Súng tốt hay súng thường? | 3 súng tốt trúng 0,9; 2 súng thường trúng 0,6. Chọn 1 súng, bắn trúng. P(súng tốt)? | 9/13 | tree | XS26 |
| **XSS173** | Bắn tiếp phát hai | Như trên, dùng lại khẩu súng đó bắn phát thứ hai. P(lại trúng)? | 21/26 | tree | XS26 |
| **XSS174** | Chuyền bi qua ba hộp | Ba hộp đều 1 đỏ 1 xanh. Chuyển 1 bi từ I sang II, 1 bi từ II sang III, rồi rút từ III. P(đỏ)? | 1/2 | tree | XS26 |
| **XSS175** | Ba đồng xu bí ẩn | Xu chuẩn, xu lệch P(ngửa) = 3/4, xu hai mặt ngửa. Chọn 1 đồng, tung ra ngửa. P(lần sau cũng ngửa)? | 29/36 | tree | XS26 |

## L10 · Chặn điểm 8-9-10 (XSS176 – XSS190) · 90 – 170 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS176** | Phương trình có nghiệm | Gieo xúc xắc 2 lần được b rồi c. P(phương trình x² + bx + c = 0 có nghiệm)? | 19/36 | grid | XS29 |
| **XSS177** | Hai đội mạnh cùng bảng | 8 đội chia ngẫu nhiên thành 2 bảng 4 đội. P(hai đội mạnh nhất cùng bảng)? | 3/7 | cards | XS10 |
| **XSS178** | Nữ không đứng cạnh nhau | 5 nam, 5 nữ xếp hàng ngang. P(không có hai bạn nữ nào đứng cạnh nhau)? | 1/42 | cards | XS12 |
| **XSS179** | Bàn tròn xen kẽ | 4 nam, 4 nữ ngồi ngẫu nhiên quanh bàn tròn. P(nam nữ ngồi xen kẽ)? | 1/35 | geo | XS12 |
| **XSS180** | Chữ số tăng dần | Chọn ngẫu nhiên một số có 3 chữ số. P(các chữ số tăng dần từ trái sang phải)? | 7/75 | grid | XS08 |
| **XSS181** | Ba số lập cấp số cộng | Chọn 3 số khác nhau từ 1 đến 20. P(ba số lập thành cấp số cộng)? | 3/38 | grid | XS10 |
| **XSS182** | Ba điểm thẳng hàng | Chọn 3 trong 9 điểm của lưới 3 × 3. P(ba điểm thẳng hàng)? | 2/21 | geo | XS07 |
| **XSS183** | Ba cạnh tam giác | Gieo 3 xúc xắc. P(ba số chấm là độ dài ba cạnh của một tam giác)? | 37/72 | grid | XS09 |
| **XSS184** | An rút trước, Bình rút sau | Hộp 6 đỏ 4 xanh. An lấy 1 bi, Bình lấy tiếp 2 bi; biết 2 bi của Bình cùng màu. P(An lấy đỏ)? | 4/7 | tree | XS29 |
| **XSS185** | Gặp một bạn nam | 45 % học sinh thích bóng đá; trong đó 60 % là nam, nhóm còn lại 30 % là nam. Gặp bạn nam: P(thích bóng đá)? | 18/29 ≈ 0,62 | tree | XS29 |
| **XSS186** | Trúng đủ hai phát thì dừng | Bắn đến khi trúng 2 phát thì dừng, mỗi phát trúng 0,6. P(dừng ở phát thứ 4)? | 0,1728 | tree | XS18 |
| **XSS187** | Tam giác tù trong 12-giác | Chọn 3 đỉnh của đa giác đều 12 cạnh. P(được tam giác tù)? | 6/11 | geo | XS07 |
| **XSS188** | Hai số từ 1 đến 100 | Chọn 2 số khác nhau từ 1 đến 100. P(tích của chúng chia hết cho 3)? | 83/150 | grid | XS29 |
| **XSS189** | Ngửa nhiều hơn sấp | Tung đồng xu 10 lần. P(số lần ngửa nhiều hơn số lần sấp)? | 193/512 ≈ 0,377 | tree | XS18 |
| **XSS190** | Đoán bừa 10 câu | Đề 10 câu, mỗi câu 4 phương án, đoán bừa tất cả. P(đúng ít nhất 5 câu)? | ≈ 0,078 | curve | XS18 |

## L11 · Học sinh giỏi (XSS191 – XSS200) · 120 – 180 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS191** | Gối của Lewis Carroll | Túi có 1 bi, đỏ hoặc trắng (1/2). Bỏ thêm 1 bi đỏ, rút ra được đỏ. P(bi còn lại là đỏ)? | 2/3 | tree | XS30 |
| **XSS192** | Nghịch lý Simpson | Thuốc A khỏi 81/87 ca nhẹ, 192/263 ca nặng; B: 234/270 và 55/80. Thuốc nào khỏi chung nhiều hơn? | B (83 % so với 78 %) | table | XS28 |
| **XSS193** | Thêm một đồng xu | An tung 4 đồng xu, Bình tung 3 đồng xu. P(An được nhiều mặt ngửa hơn Bình)? | 1/2 | tree | XS30 |
| **XSS194** | Viên bi cuối cùng | Hộp 5 đỏ 3 xanh, rút lần lượt đến hết. P(viên bi cuối cùng màu xanh)? | 3/8 | urn | XS30 |
| **XSS195** | Bước lên cầu thang | Mỗi bước lên 1 hoặc 2 bậc với xác suất như nhau. P(chân chạm đúng bậc thứ 4)? | 11/16 | tree | XS30 |
| **XSS196** | Chọn người giỏi nhất | 3 ứng viên lần lượt. Bỏ qua người đầu, chọn người đầu tiên giỏi hơn mọi người trước. P(chọn được người giỏi nhất)? | 1/2 | cards | XS30 |
| **XSS197** | Chờ hai ngửa liên tiếp | Tung đồng xu đến khi có hai lần ngửa liên tiếp. Trung bình cần bao nhiêu lần? | 6 | sim | XS30 |
| **XSS198** | Loạt luân lưu | Mỗi đội sút 5 quả luân lưu, mỗi quả vào 0,75. P(hòa sau 5 lượt)? | ≈ 0,29 | sim | XS30 |
| **XSS199** | Giải độc đắc 6/45 | Chọn 6 số trong 45 số. P(trùng đủ 6 số được quay)? | 1/8 145 060 | cards | XS07 |
| **XSS200** | Monty Hall 100 cửa | 100 cửa, 1 cửa có xe. Bạn chọn 1, người dẫn mở 98 cửa có dê. Đổi cửa: P(trúng xe)? | 99/100 | cards | XS28 |

## L12 · Bốc bi đa hộp (XSS201 – XSS216) · 75 – 150 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS201** | Mỗi hộp một bi | Hộp I: 3 đỏ 2 xanh; hộp II: 2 đỏ 4 xanh. Rút mỗi hộp 1 bi. P(hai bi cùng màu)? | 7/15 | tree | XS17 |
| **XSS202** | Cùng màu thì màu gì? | Như trên, biết hai bi cùng màu. P(cả hai bi đều đỏ)? | 3/7 | tree | XS20 |
| **XSS203** | Ba hộp, đúng hai đỏ | Hộp k có k đỏ và 4 − k xanh (k = 1, 2, 3). Rút mỗi hộp 1 bi. P(đúng 2 bi đỏ)? | 13/32 | tree | XS18 |
| **XSS204** | Bi đỏ duy nhất từ đâu? | Như trên, biết rút được đúng 1 bi đỏ. P(bi đỏ đó từ hộp 3)? | 9/13 | tree | XS25 |
| **XSS205** | Tung xu chọn hộp | Hộp I: 4 đỏ 1 xanh; hộp II: 1 đỏ 4 xanh. Tung xu chọn hộp, rút 2 bi. P(1 đỏ 1 xanh)? | 2/5 | tree | XS24 |
| **XSS206** | Bi thứ hai cùng hộp | Như trên: rút 1 bi được đỏ, rút tiếp bi thứ hai cùng hộp. P(bi thứ hai cũng đỏ)? | 3/5 | tree | XS26 |
| **XSS207** | Hoàn lại vẫn phụ thuộc | Như trên nhưng rút có hoàn lại: lần 1 đỏ. P(lần 2 cũng đỏ)? | 17/25 | tree | XS23 |
| **XSS208** | Xúc xắc chọn hộp, hai bi đỏ | Gieo xúc xắc: ra 6 chọn hộp A (5 đỏ 1 xanh), khác 6 chọn hộp B (2 đỏ 4 xanh). Rút 2 bi đều đỏ. P(hộp A)? | 2/3 | tree | XS25 |
| **XSS209** | Luân phiên hai hộp | An rút ở hộp I (2 đỏ 3 xanh), Bình ở hộp II (3 đỏ 1 xanh), luân phiên, không hoàn lại; ai được đỏ trước thắng. P(An thắng)? | 19/40 | tree | XS22 |
| **XSS210** | Đến khi đủ hai màu | Hộp 3 đỏ 2 xanh, rút lần lượt đến khi có đủ hai màu. P(cần đúng 3 lần)? | 3/10 | tree | XS22 |
| **XSS211** | Hai bi xanh liền nhau | Hộp 4 đỏ 2 xanh, rút lần lượt đến hết. P(hai bi xanh được rút liền nhau)? | 1/3 | urn | XS12 |
| **XSS212** | Đỏ luôn không ít hơn | Hộp 3 đỏ 3 xanh, rút lần lượt đến hết. P(mọi lúc số đỏ đã rút ≥ số xanh)? | 1/4 | urn | XS30 |
| **XSS213** | Số lớn nhất là 7 | Rút 3 bi từ 10 bi đánh số 1 đến 10. P(số lớn nhất là 7)? | 1/8 | urn | XS07 |
| **XSS214** | Nhỏ nhất 3, lớn nhất 7 | Như trên, biết số nhỏ nhất là 3. P(số lớn nhất là 7)? | 1/7 | urn | XS20 |
| **XSS215** | Ba hộp, hai bi khác màu | Hộp I: 2 đỏ 2 xanh; II: 3 đỏ 1 xanh; III: 4 đỏ. Chọn hộp, rút 2 bi khác màu. P(hộp I)? | 4/7 | tree | XS26 |
| **XSS216** | Thêm bi cùng màu | Hộp 1 đỏ 1 xanh; rút 1 bi, trả lại kèm 1 bi cùng màu, rút lần 2 được đỏ. P(lần 1 đỏ)? | 2/3 | tree | XS25 |

## L13 · Chuyển bi (XSS217 – XSS232) · 90 – 170 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS217** | Chuyển một, rút hai | Hộp I: 3 đỏ 2 xanh; II: 2 đỏ 2 xanh. Chuyển 1 bi từ I sang II, rồi rút 2 bi từ II. P(2 đỏ)? | 11/50 | tree | XS24 |
| **XSS218** | Bi chuyển màu gì? | Như trên, biết 2 bi rút từ II đều đỏ. P(bi đã chuyển là đỏ)? | 9/11 | tree | XS25 |
| **XSS219** | Chuyển đi rồi chuyển về | Hộp I: 2 đỏ 1 xanh; II: 1 đỏ 2 xanh. Chuyển 1 bi I → II, rồi 1 bi II → I, rút từ I. P(đỏ)? | 7/12 | tree | XS24 |
| **XSS220** | Truy ngược hai lần chuyển | Như trên, biết bi rút từ I là đỏ. P(bi chuyển I → II lúc đầu là đỏ)? | 4/7 | tree | XS25 |
| **XSS221** | Chuyển hai, rút hai | Hộp I: 3 đỏ 3 xanh; II: 2 đỏ 2 xanh. Chuyển 2 bi I → II, rồi rút 2 bi từ II. P(cùng màu)? | 32/75 | tree | XS24 |
| **XSS222** | Hai bi chuyển đều đỏ? | Như trên, biết 2 bi rút từ II đều đỏ. P(2 bi đã chuyển đều đỏ)? | 3/8 | tree | XS26 |
| **XSS223** | Đổi bi giữa hai hộp | Hộp I: 3 đỏ 1 xanh; II: 1 đỏ 3 xanh. Đổi ngẫu nhiên 1 bi của I lấy 1 bi của II, rồi rút từ I. P(đỏ)? | 5/8 | tree | XS24 |
| **XSS224** | Đổi hai lần, về như cũ | Như trên, đổi bi 2 lần. P(hộp I lại có đúng 3 đỏ 1 xanh)? | 11/32 | tree | XS24 |
| **XSS225** | Đồng xu quyết định số bi | Ngửa: chuyển 1 bi, sấp: chuyển 2 bi từ hộp I (3 đỏ 1 xanh) sang II (1 đỏ 1 xanh); rút 1 bi từ II. P(đỏ)? | 29/48 | tree | XS26 |
| **XSS226** | Bi bị giấu đi | Hộp 3 đỏ 2 xanh. Lấy 1 bi cất đi không xem, rồi rút 1 bi. P(bi rút ra đỏ)? | 3/5 | tree | XS28 |
| **XSS227** | Bi giấu màu gì? | Như trên, biết bi rút ra đỏ. P(bi đã cất đi cũng đỏ)? | 1/2 | tree | XS25 |
| **XSS228** | Chuyền qua ba hộp | Hộp I: 2 đỏ; II và III: mỗi hộp 1 đỏ 1 xanh. Chuyển 1 bi I → II → III rồi rút từ III. P(đỏ)? | 5/9 | tree | XS24 |
| **XSS229** | Hai hộp đổ vào một | Lấy 1 bi từ I (2 đỏ 1 xanh) và 1 bi từ II (1 đỏ 2 xanh) bỏ vào III (1 đỏ). Rút từ III. P(đỏ)? | 2/3 | tree | XS24 |
| **XSS230** | Bi từ hộp II đỏ không? | Như trên, biết bi rút từ III là đỏ. P(bi lấy từ II là đỏ)? | 4/9 | tree | XS26 |
| **XSS231** | Chuyển hai vào hộp toàn xanh | Chuyển 2 bi từ I (4 đỏ 2 xanh) sang II (2 xanh), rút 1 bi II được đỏ. P(đúng 1 bi đỏ đã được chuyển)? | 2/5 | tree | XS26 |
| **XSS232** | Đi một vòng trở về | Hộp I: 3 đỏ 2 xanh; II: 2 đỏ 3 xanh. Chuyển 1 bi I → II rồi 1 bi II → I. P(hộp I như cũ)? | 17/30 | tree | XS24 |

## L14 · Đa điều kiện (XSS233 – XSS248) · 75 – 150 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS233** | Hai điều kiện cùng lúc | Gieo 2 xúc xắc, biết tổng chẵn và có mặt 6. P(tổng ≥ 10)? | 3/5 | grid | XS20 |
| **XSS234** | Ngửa đầu và ít nhất hai ngửa | Tung xu 3 lần, biết lần 1 ngửa và có ít nhất 2 ngửa. P(cả 3 lần ngửa)? | 1/3 | tree | XS20 |
| **XSS235** | Ai bắn trượt? | Ba xạ thủ trúng 0,5; 0,6; 0,7. Biết đúng 2 người trúng. P(người thứ nhất trượt)? | 21/44 | tree | XS25 |
| **XSS236** | Ít nhất hai người trúng | Như trên, biết có ít nhất 2 người trúng. P(cả 3 cùng trúng)? | 21/65 | tree | XS20 |
| **XSS237** | Xúc xắc rồi đồng xu | Gieo xúc xắc được k chấm rồi tung k đồng xu. P(không có mặt ngửa nào)? | 21/128 | tree | XS24 |
| **XSS238** | Không ngửa nào, xúc xắc ra mấy? | Như trên, biết không có mặt ngửa nào. P(xúc xắc ra 1 chấm)? | 32/63 | tree | XS25 |
| **XSS239** | Gieo đến khi ra 6: không nhớ | Gieo đến khi ra 6. Biết cần ít nhất 3 lần. P(cần đúng 4 lần)? | 5/36 | tree | XS20 |
| **XSS240** | Có cả trai lẫn gái | Gia đình 4 con, biết có cả trai lẫn gái. P(đúng 2 trai)? | 3/7 | tree | XS20 |
| **XSS241** | Xu bí ẩn: lần hai | Chọn ngẫu nhiên xu chuẩn hoặc xu lệch (ngửa 0,9), tung 2 lần. Lần 1 ngửa: P(lần 2 ngửa)? | 53/70 | tree | XS23 |
| **XSS242** | Xu bí ẩn: lần ba | Như trên, biết 2 lần đầu đều ngửa. P(lần 3 ngửa)? | 427/530 ≈ 0,806 | tree | XS26 |
| **XSS243** | Bị loại ở vòng nào? | Qua vòng 1: 0,8; qua 1 thì qua vòng 2: 0,6; qua 2 thì qua vòng 3: 0,5. Biết bị loại. P(loại ở vòng 2)? | 8/19 | tree | XS25 |
| **XSS244** | Ba mặt khác nhau có 6? | Gieo 3 xúc xắc, biết ba mặt khác nhau. P(có mặt 6)? | 1/2 | grid | XS20 |
| **XSS245** | Có 6 thì khác nhau? | Gieo 3 xúc xắc, biết có ít nhất một mặt 6. P(ba mặt khác nhau)? | 60/91 | grid | XS20 |
| **XSS246** | Ba phát trúng liên tiếp | Bắn 5 phát (mỗi phát trúng 0,6), biết trúng đúng 3 phát. P(3 phát trúng liên tiếp)? | 3/10 | tree | XS18 |
| **XSS247** | Chọn n rồi chọn m | Chọn ngẫu nhiên n từ 1 đến 4, rồi chọn ngẫu nhiên m từ 1 đến n. P(m = 1)? | 25/48 | tree | XS24 |
| **XSS248** | Lần ngược hai bước chọn | Như trên, biết m = 1. P(n = 1)? | 12/25 | tree | XS25 |

## L15 · Tham số xuôi – ngược (XSS249 – XSS264) · 75 – 150 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS249** | Hộp có bao nhiêu bi? | Hộp có n bi, trong đó 3 đỏ. Rút 2 bi, P(2 đỏ) = 1/5. Tìm n. | n = 6 | urn | XS07 |
| **XSS250** | Hai đáp số cho x | Hộp 5 đỏ, x xanh. Rút 2 bi, P(khác màu) = 5/9. Tìm x. | x = 4 hoặc x = 5 | urn | XS07 |
| **XSS251** | Tìm xác suất bắn trúng | Bắn 2 phát độc lập, P(trúng ít nhất 1 phát) = 0,96. Tìm xác suất trúng p mỗi phát. | p = 0,8 | tree | XS17 |
| **XSS252** | Bắn bao nhiêu phát? | Mỗi phát trúng 0,3. Bắn ít nhất bao nhiêu phát để P(trúng ít nhất 1) ≥ 0,95? | 9 | tree | XS18 |
| **XSS253** | Tỉ lệ bệnh là bao nhiêu? | Xét nghiệm nhạy 90 %, dương tính giả 10 %. P(bệnh \| dương tính) = 0,5. Tìm tỉ lệ bệnh x. | x = 0,1 | square | XS27 |
| **XSS254** | Tìm số bi đỏ hộp II | Hộp I: 2 đỏ 3 xanh; II: x đỏ 2 xanh. Chọn hộp ngẫu nhiên rồi rút 1 bi, P(đỏ) = 1/2. Tìm x. | x = 3 | tree | XS24 |
| **XSS255** | Tham số sau khi chuyển bi | Chuyển 1 bi từ I (3 đỏ 1 xanh) sang II (a đỏ 2 xanh), rút từ II: P(đỏ) = 5/8. Tìm a. | a = 3 | tree | XS24 |
| **XSS256** | Tìm tay nghề xạ thủ | Hai xạ thủ trúng p và 0,8. P(đúng 1 người trúng) = 0,38. Tìm p. | p = 0,7 | tree | XS17 |
| **XSS257** | Điều kiện là một phép hợp | A, B độc lập, P(A) = 0,5; P(B) = 0,4. Tính P(A \| A ∪ B). | 5/7 | square | XS23 |
| **XSS258** | Nhóm có bao nhiêu bạn? | n bạn xếp hàng ngang, P(Hà và Lan đứng cạnh nhau) = 1/4. Tìm n. | n = 8 | cards | XS12 |
| **XSS259** | n đỏ, n xanh | Hộp n đỏ, n xanh. Rút 2 bi, P(cùng màu) = 4/9. Tìm n. | n = 5 | urn | XS07 |
| **XSS260** | Đồng xu lệch bao nhiêu? | Xu lệch, ngửa với xác suất p > 1/2. Tung 2 lần, P(1 ngửa 1 sấp) = 0,48. Tìm p. | p = 0,6 | tree | XS18 |
| **XSS261** | p nào tốt nhất? | Xu lệch ngửa p, tung 3 lần. p bằng bao nhiêu thì P(đúng 2 ngửa) lớn nhất? | p = 2/3 | curve | XS18 |
| **XSS262** | Ít nhất bao nhiêu bi đỏ? | Hộp n đỏ, 3 xanh. Tìm n nhỏ nhất để P(rút 2 bi đều đỏ) > 1/2. | n = 8 | urn | XS07 |
| **XSS263** | Đài báo nhầm bao nhiêu? | Mưa 30 %; trời mưa thì báo mưa 90 %. P(mưa \| báo mưa) = 0,72. Tìm tỉ lệ báo mưa khi trời tạnh. | 0,15 | tree | XS27 |
| **XSS264** | Chọn hộp I với xác suất p | Hộp I: 3 đỏ 1 xanh; II: 1 đỏ 3 xanh; chọn I với xác suất p. Rút được đỏ thì P(hộp I) = 0,9. Tìm p. | p = 0,75 | tree | XS25 |

## L16 · Cây hay – lạ (XSS265 – XSS280) · 90 – 175 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS265** | Xu lệch hóa công bằng | Xu lệch ngửa 0,7. Tung từng cặp: NS thì A, SN thì B, còn lại tung lại. Trung bình mấy cặp? | 50/21 ≈ 2,38 | tree | XS30 |
| **XSS266** | Trò craps | Gieo 2 xúc xắc: 7, 11 thắng; 2, 3, 12 thua; khác thì gieo tiếp đến khi lặp lại số đó (thắng) hoặc ra 7 (thua). P(thắng)? | 244/495 ≈ 0,493 | tree | XS30 |
| **XSS267** | Con bạc có lợi thế | Có 2 đồng, mỗi ván thắng 2/3 (thêm 1 đồng) hoặc thua. Dừng khi có 4 đồng hoặc hết tiền. P(đạt 4)? | 4/5 | tree | XS30 |
| **XSS268** | Dẫn 2–0 trong loạt 7 ván | Thắng 4 ván trước là vô địch, A thắng mỗi ván 0,6 và đang dẫn 2–0. P(A vô địch)? | ≈ 0,913 | tree | XS30 |
| **XSS269** | Người dẫn không biết | Monty Hall nhưng người dẫn không biết, mở ngẫu nhiên và tình cờ ra dê. Đổi cửa: P(trúng xe)? | 1/2 | tree | XS28 |
| **XSS270** | Dòng họ tuyệt chủng | Mỗi cá thể sinh 0, 1, 2 con với xác suất 1/4, 1/4, 1/2. P(dòng họ từ một cá thể tuyệt chủng)? | 1/2 | tree | XS30 |
| **XSS271** | Bàn Galton | Bi rơi qua 4 hàng đinh, mỗi đinh lệch trái hoặc phải 1/2. P(rơi vào ô chính giữa)? | 3/8 | tree | XS18 |
| **XSS272** | Hai khâu kiểm tra | Hàng lỗi 10 %; mỗi khâu bắt lỗi 90 %, báo nhầm hàng tốt 5 %. Hàng qua cả 2 khâu: P(là hàng lỗi)? | 4/3253 ≈ 0,0012 | tree | XS27 |
| **XSS273** | Nhánh đấu loại trực tiếp | A gặp B, C gặp D, thắng vào chung kết. A thắng ai cũng 0,6; các trận khác 1/2. P(C vô địch)? | 0,22 | tree | XS22 |
| **XSS274** | Chuột trong mê cung | Chuột chọn ngẫu nhiên 1 trong 3 cửa: cửa 1 ra ngoài sau 2 phút, cửa 2, 3 quay lại sau 3 và 5 phút. Trung bình bao lâu ra? | 10 phút | tree | XS30 |
| **XSS275** | Hơn nhau hai ngửa | Tung xu đến khi số ngửa hơn số sấp 2 hoặc ngược lại. P(dừng sau đúng 4 lần)? | 1/4 | tree | XS30 |
| **XSS276** | Ba người, cùng tháng sinh | 3 người. P(có ít nhất 2 người sinh cùng tháng)? | 17/72 | tree | XS13 |
| **XSS277** | Kiến về đỉnh đối diện | Kiến đi ngẫu nhiên trên cạnh hình lập phương. Trung bình bao nhiêu bước tới đỉnh đối diện? | 10 | tree | XS30 |
| **XSS278** | Bốn bạn chuyền bóng | 4 bạn, mỗi lần chuyền bóng ngẫu nhiên cho 1 trong 3 bạn kia. P(sau 4 lần, bóng về người đầu)? | 7/27 | tree | XS30 |
| **XSS279** | Cậu bé bên cửa sổ | Gia đình 2 con; nhìn qua cửa sổ thấy ngẫu nhiên 1 đứa là trai. P(cả hai là trai)? | 1/2 | tree | XS28 |
| **XSS280** | Ba người, ba cơ hội | A, B, C lần lượt gieo xúc xắc; A thắng nếu ra 1; B nếu ra 1, 2; C nếu ra 1, 2, 3. P(A thắng)? | 3/13 | tree | XS30 |

## L17 · Ếch nhảy (XSS281 – XSS296) · 75 – 150 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS281** | Ếch nhảy 1, 2, 3 lá | Ếch ở lá 0, mỗi lần nhảy tới 1, 2 hoặc 3 lá (xác suất như nhau). P(ếch đáp đúng lá 4)? | 37/81 | tree | XS30 |
| **XSS282** | Ếch thích nhảy tới | Ếch trên trục số, mỗi bước +1 (xác suất 2/3) hoặc −1. P(sau 4 bước ở vị trí 2)? | 32/81 | tree | XS18 |
| **XSS283** | Ếch về chỗ cũ | Ếch mỗi bước nhảy trái hoặc phải 1 ô (1/2). P(sau 6 bước về đúng chỗ cũ)? | 5/16 | tree | XS18 |
| **XSS284** | Ếch trên hình vuông | Ếch ở một đỉnh hình vuông, mỗi bước sang một đỉnh kề. P(sau 4 bước ở đỉnh đối diện)? | 1/2 | tree | XS30 |
| **XSS285** | Ếch trên ngũ giác | Ếch ở một đỉnh ngũ giác, mỗi bước sang một đỉnh kề. P(sau 5 bước về chỗ cũ)? | 1/16 | tree | XS30 |
| **XSS286** | Lá sen bị hỏng | Ếch ở lá 0, mỗi lần nhảy 1 hoặc 2 lá (1/2); lá 3 hỏng, đáp vào là rơi. P(ếch đáp lá 5)? | 3/16 | tree | XS30 |
| **XSS287** | Biết ếch tới lá 4 | Ếch ở lá 0, mỗi lần nhảy 1 hoặc 2 lá (1/2). Biết ếch đáp lá 4: P(nó từng đáp lá 2)? | 9/11 | tree | XS25 |
| **XSS288** | Kiến đi qua hai điểm | Kiến từ (0; 0), mỗi bước sang phải hoặc lên (1/2). P(đi qua cả (1; 1) và (3; 3))? | 3/16 | grid | XS22 |
| **XSS289** | Ếch có gió đẩy | Ếch ở 0, mỗi bước +1 (3/4) hoặc −1 (1/4). P(chạm 2 trước khi chạm −2)? | 9/10 | tree | XS30 |
| **XSS290** | Hai ếch gặp nhau | Ếch A ở 0, ếch B ở 4; mỗi giây mỗi con nhảy ±1 (1/2), độc lập. P(gặp nhau sau đúng 2 giây)? | 1/16 | tree | XS30 |
| **XSS291** | Ếch quen hướng | Bước đầu ±1 (1/2); sau đó giữ hướng cũ với xác suất 2/3. P(sau 3 bước cách gốc 3 đơn vị)? | 4/9 | tree | XS22 |
| **XSS292** | Bao nhiêu bước qua sông? | Tung xu: ngửa nhảy 1 lá, sấp nhảy 2 lá. Trung bình cần mấy bước để tới hoặc vượt lá 4? | 23/8 | tree | XS30 |
| **XSS293** | Ếch giữa hai bờ | Lá 1, 2, 3, 4 thẳng hàng; lá 1 và 4 là bờ. Ếch ở lá 2, mỗi bước ±1 (1/2). P(lên bờ ở lá 4)? | 1/3 | tree | XS30 |
| **XSS294** | Mấy bước thì lên bờ? | Như trên: ếch ở lá 2. Trung bình mấy bước thì lên bờ? | 2 | tree | XS30 |
| **XSS295** | Ếch lười | Mỗi giây ếch nhảy trái 1/4, phải 1/4, đứng yên 1/2. P(sau 2 giây ở đúng chỗ cũ)? | 3/8 | tree | XS18 |
| **XSS296** | Chưa từng sang bờ âm | Ếch nhảy ±1 (1/2) trong 4 bước. Biết cuối cùng về gốc: P(chưa lần nào ở vị trí âm)? | 1/3 | tree | XS20 |

## L18 · Quy hoạch động (XSS297 – XSS312) · 90 – 170 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS297** | Lên 6 bậc | Chọn ngẫu nhiên một cách lên 6 bậc thang, mỗi bước 1 hoặc 2 bậc. P(dùng đúng hai bước 2 bậc)? | 6/13 | tree | XS10 |
| **XSS298** | Bước 1, 2, 3 bậc | Chọn ngẫu nhiên một cách lên 5 bậc, mỗi bước 1, 2 hoặc 3 bậc. P(không dùng bước 3 bậc)? | 8/13 | tree | XS10 |
| **XSS299** | Bước dài hay bước ngắn | Mỗi bước lên 1 bậc (1/3) hoặc 2 bậc (2/3). P(chân chạm đúng bậc 4)? | 55/81 | tree | XS30 |
| **XSS300** | Đường ngắn nhất qua (1; 1) | Chọn ngẫu nhiên một đường ngắn nhất từ (0; 0) tới (3; 3) trên lưới. P(đi qua (1; 1))? | 3/5 | grid | XS10 |
| **XSS301** | Tránh điểm (1; 1) | Như trên, biết đường đi không qua (1; 1). P(đường đi qua (2; 2))? | 1/2 | grid | XS20 |
| **XSS302** | Robot rẽ ngẫu nhiên | Robot từ (0; 0) tới (3; 3), mỗi ngã rẽ chọn phải/lên (1/2), chạm mép thì đi thẳng. P(qua góc (3; 0))? | 1/8 | grid | XS28 |
| **XSS303** | Quân vua trên bàn 3 × 3 | Quân vua ở góc bàn 3 × 3, mỗi bước sang một ô kề cạnh ngẫu nhiên. P(sau 2 bước ở ô tâm)? | 1/3 | grid | XS30 |
| **XSS304** | Quân mã trên bàn 3 × 3 | Quân mã ở góc bàn 3 × 3, mỗi bước đi một nước mã hợp lệ ngẫu nhiên. P(sau 4 bước về chỗ cũ)? | 3/8 | grid | XS30 |
| **XSS305** | Hai vũng nước | Đường ngắn nhất ngẫu nhiên từ (0; 0) tới (3; 3), tránh (1; 2) và (2; 1). P(đường đi khô ráo)? | 1/10 | grid | XS10 |
| **XSS306** | Không ba ngửa liền | Tung xu 6 lần. P(không có 3 lần ngửa liên tiếp)? | 11/16 | tree | XS18 |
| **XSS307** | Tám lần không hai ngửa | Tung xu 8 lần. P(không có 2 lần ngửa liên tiếp)? | 55/256 | tree | XS18 |
| **XSS308** | Tổng dồn chạm đúng 6 | Gieo xúc xắc nhiều lần, cộng dồn số chấm. P(tổng có lúc bằng đúng 6)? | 16807/46656 ≈ 0,36 | tree | XS30 |
| **XSS309** | Rắn và thang mini | Ô 0 → 4: ngửa tiến 1, sấp tiến 2; đáp ô 3 là bị rắn đẩy về ô 1. Trung bình mấy lượt về đích? | 6 | tree | XS30 |
| **XSS310** | Tiến, tiến hai, lùi | Mỗi lượt đi +1, +2 hoặc −1 (như nhau). P(sau 3 lượt ở đúng vị trí 3)? | 4/27 | tree | XS18 |
| **XSS311** | Chờ ba ngửa liên tiếp | Tung xu đến khi có 3 lần ngửa liên tiếp. Trung bình cần bao nhiêu lần? | 14 | sim | XS30 |
| **XSS312** | Hai robot ngược chiều | Robot A từ (0; 0) tới (2; 2), B từ (2; 2) về (0; 0), cùng tốc độ, chọn đường ngắn nhất ngẫu nhiên. P(gặp nhau)? | 1/2 | grid | XS30 |

## L19 · Hình học có điều kiện (XSS313 – XSS328) · 75 – 160 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS313** | Có cạnh lục giác thì vuông? | Chọn 3 đỉnh lục giác đều, biết tam giác có cạnh là cạnh lục giác. P(tam giác vuông)? | 2/3 | geo | XS20 |
| **XSS314** | Cân rồi có đều? | Chọn 3 đỉnh của đa giác đều 12 cạnh, biết tam giác cân. P(tam giác đều)? | 1/13 | geo | XS20 |
| **XSS315** | Điểm dưới đường chéo | Chọn x, y ngẫu nhiên trong [0; 1], biết x + y < 1. P(x < 2y)? | 2/3 | square | XS30 |
| **XSS316** | Phần trái dài hơn 0,3 | Chọn điểm x ngẫu nhiên trên đoạn [0; 1]. Biết x > 0,3: P(x > 2(1 − x))? | 10/21 | geo | XS30 |
| **XSS317** | Bẻ que có điều kiện | Bẻ que tại 2 điểm ngẫu nhiên, biết đoạn bên trái ngắn hơn nửa que. P(ba đoạn tạo tam giác)? | 1/3 | square | XS30 |
| **XSS318** | An đến sớm | Hai bạn đến ngẫu nhiên trong 1 giờ, chờ nhau 15 phút. Biết An đến trong 15 phút đầu. P(gặp nhau)? | 3/8 | square | XS30 |
| **XSS319** | Không cạnh nào là cạnh đa giác | Chọn 3 đỉnh đa giác đều 10 cạnh, biết tam giác không có cạnh nào là cạnh đa giác. P(tam giác tù)? | 1/5 | geo | XS20 |
| **XSS320** | Tam giác trên lưới 3 × 3 | Chọn 3 trong 9 điểm lưới 3 × 3, biết chúng tạo thành tam giác. P(tam giác vuông)? | 11/19 | geo | XS20 |
| **XSS321** | Đường chéo khối lập phương | Chọn 2 đỉnh hình lập phương, biết đoạn nối không phải cạnh. P(là đường chéo khối)? | 1/4 | geo | XS20 |
| **XSS322** | Vuông cân trong lập phương | Chọn 3 đỉnh hình lập phương, biết được tam giác vuông. P(tam giác vuông cân)? | 1/2 | geo | XS20 |
| **XSS323** | Điểm xúc xắc trong hình tròn | Gieo 2 xúc xắc được điểm (a; b), biết a² + b² < 25. P(điểm nằm trên đường y = x)? | 3/13 | grid | XS20 |
| **XSS324** | Tâm và hai đỉnh lục giác | Chọn 2 đỉnh lục giác đều, cùng tâm O tạo tam giác (không suy biến). P(tam giác đều)? | 1/2 | geo | XS20 |
| **XSS325** | Tứ giác chứa tâm | Chọn 4 đỉnh bát giác đều, biết tứ giác chứa tâm ở bên trong. P(hình chữ nhật)? | 3/19 | geo | XS20 |
| **XSS326** | Dây cung dài | Chọn 2 đỉnh đa giác đều 12 cạnh, biết dây nối không qua tâm. P(dây dài hơn cạnh tam giác đều nội tiếp)? | 1/5 | geo | XS20 |
| **XSS327** | Bát giác: vuông thì có cân? | Chọn 3 đỉnh bát giác đều, biết được tam giác vuông. P(tam giác vuông cân)? | 1/3 | geo | XS20 |
| **XSS328** | Góc 150 độ | Chọn 3 đỉnh đa giác đều 12 cạnh, biết tam giác tù. P(tam giác có một góc 150°)? | 1/10 | geo | XS20 |

## L20 · Bi vận dụng cao (XSS329 – XSS344) · 75 – 160 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS329** | Bi đầu và bi cuối | Hộp 4 đỏ 4 xanh, rút lần lượt đến hết. P(bi đầu tiên và bi cuối cùng đều đỏ)? | 3/14 | urn | XS22 |
| **XSS330** | Ít nhất hai đỏ | Hộp 5 đỏ 5 xanh, rút 4 bi, biết có ít nhất 2 bi đỏ. P(đúng 2 bi đỏ)? | 20/31 | urn | XS20 |
| **XSS331** | Đến khi trùng màu | Hộp có 3 màu, mỗi màu 2 bi. Rút lần lượt đến khi có 2 bi cùng màu. P(cần đúng 4 lần)? | 2/5 | urn | XS22 |
| **XSS332** | Tổng chia hết cho 3 | Rút 3 bi từ 10 bi đánh số 1 đến 10. P(tổng ba số chia hết cho 3)? | 7/20 | urn | XS10 |
| **XSS333** | Ba số tăng dần | Rút 3 lần có hoàn lại từ 5 bi số 1 đến 5. P(số sau luôn lớn hơn số trước)? | 2/25 | urn | XS10 |
| **XSS334** | Có vàng thì đủ màu? | Hộp 4 đỏ 3 xanh 2 vàng, rút 3 bi, biết có ít nhất 1 bi vàng. P(đủ ba màu)? | 24/49 | urn | XS20 |
| **XSS335** | Đỏ áp đảo | Hộp 6 đỏ 4 xanh, rút 5 bi. P(số bi đỏ nhiều hơn số bi xanh)? | 31/42 | urn | XS11 |
| **XSS336** | Ai rút đỏ trước? | Hộp 2 đỏ 3 xanh. A, B lần lượt rút không hoàn lại (A trước), ai được đỏ trước thắng. P(A thắng)? | 3/5 | urn | XS22 |
| **XSS337** | Hộp bí ẩn ba bi | Hộp 3 bi, số bi đỏ là 0, 1, 2, 3 như nhau. Rút có hoàn lại 2 lần đều đỏ. P(cả 3 bi đều đỏ)? | 9/14 | urn | XS26 |
| **XSS338** | Lần thứ ba cũng đỏ? | Như trên: đã rút 2 lần đều đỏ. P(lần rút thứ ba cũng đỏ)? | 6/7 | urn | XS26 |
| **XSS339** | Đúng hai màu | Hộp 5 đỏ 4 xanh 3 trắng, rút 3 bi. P(có đúng hai màu)? | 29/44 | urn | XS11 |
| **XSS340** | Tổng chẵn thì cùng lẻ? | Rút lần lượt 2 bi từ 9 bi số 1 đến 9, biết tổng chẵn. P(cả hai số lẻ)? | 5/8 | urn | XS20 |
| **XSS341** | Chia bi vào ba hộp | Chia ngẫu nhiên 3 đỏ, 3 xanh vào 3 hộp, mỗi hộp 2 bi. P(hộp nào cũng có 1 đỏ 1 xanh)? | 2/5 | urn | XS10 |
| **XSS342** | Hộp nào cũng đủ màu | Chia 9 bi (3 đỏ, 3 xanh, 3 vàng) vào 3 hộp, mỗi hộp 3 bi. P(hộp nào cũng đủ 3 màu)? | 9/70 | urn | XS10 |
| **XSS343** | Màu nào hết trước? | Hộp 3 đỏ 2 xanh, rút lần lượt đến khi hết hẳn một màu. P(màu xanh hết trước)? | 3/5 | urn | XS30 |
| **XSS344** | Bi cuối cùng bất biến | Hộp 5 đỏ 4 xanh. Mỗi lần lấy 2 bi: cùng màu thì bỏ vào 1 đỏ, khác màu thì bỏ vào 1 xanh. Bi cuối cùng màu gì? | Đỏ (chắc chắn) | urn | XS30 |

## L21 · Xếp chỗ – toa tàu (XSS345 – XSS360) · 75 – 160 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS345** | Nam nữ xen kẽ | 3 nam, 3 nữ ngồi ngẫu nhiên vào dãy 6 ghế. P(nam nữ ngồi xen kẽ)? | 1/10 | cards | XS12 |
| **XSS346** | Ba gia đình | 3 gia đình, mỗi nhà 2 người, ngồi ngẫu nhiên vào dãy 6 ghế. P(ai cũng ngồi cạnh người nhà)? | 1/15 | cards | XS12 |
| **XSS347** | Mỗi toa hai người | 6 hành khách, mỗi người chọn ngẫu nhiên 1 trong 3 toa tàu. P(mỗi toa đúng 2 người)? | 10/81 | cards | XS10 |
| **XSS348** | Toa nào cũng có khách | 5 hành khách, mỗi người chọn ngẫu nhiên 1 trong 3 toa. P(toa nào cũng có người)? | 50/81 | cards | XS11 |
| **XSS349** | Bốn người bốn toa | 4 hành khách, mỗi người chọn ngẫu nhiên 1 trong 4 toa. P(mỗi toa đúng 1 người)? | 3/32 | cards | XS10 |
| **XSS350** | Toa 1 trống | 5 hành khách chọn ngẫu nhiên 1 trong 3 toa. Biết toa 1 trống: P(toa 2 cũng trống)? | 1/32 | cards | XS20 |
| **XSS351** | Hai dãy ghế đối diện | Hai dãy ghế đối diện, mỗi dãy 3 ghế; 3 nam 3 nữ ngồi ngẫu nhiên. P(nam nào cũng đối diện nữ)? | 2/5 | cards | XS12 |
| **XSS352** | Bốn cặp quanh bàn tròn | 4 cặp vợ chồng ngồi ngẫu nhiên quanh bàn tròn 8 ghế. P(không cặp nào ngồi cạnh nhau)? | 31/105 | geo | XS13 |
| **XSS353** | Không ai ngồi cạnh ai | Dãy 10 ghế, 4 người chọn ngẫu nhiên 4 ghế. P(không có 2 người nào ngồi cạnh nhau)? | 1/6 | cards | XS12 |
| **XSS354** | Ba ghế không kề trên bàn tròn | Chọn 3 trong 10 ghế quanh bàn tròn. P(không có 2 ghế nào kề nhau)? | 5/12 | geo | XS12 |
| **XSS355** | A trước B trước C | 5 học sinh A, B, C, D, E xếp hàng ngẫu nhiên. P(A đứng trước B và B đứng trước C)? | 1/6 | cards | XS12 |
| **XSS356** | Biết A trước B | 5 học sinh xếp hàng, biết A đứng trước B. P(A đứng đầu hàng)? | 2/5 | cards | XS20 |
| **XSS357** | Ba lớp, sáu bạn | 3 lớp, mỗi lớp 2 bạn, ngồi ngẫu nhiên vào dãy 6 ghế. P(không 2 bạn cùng lớp ngồi cạnh nhau)? | 1/3 | cards | XS13 |
| **XSS358** | Hai toa bốn chỗ | 8 người xếp ngẫu nhiên vào 2 toa, mỗi toa 4 chỗ. P(An và Bình cùng toa)? | 3/7 | cards | XS10 |
| **XSS359** | Thang máy năm tầng | 4 người vào thang máy, mỗi người ra ngẫu nhiên ở 1 trong 5 tầng. P(4 người ra ở 4 tầng khác nhau)? | 24/125 | cards | XS10 |
| **XSS360** | An ngồi một mình | 5 hành khách chọn 3 toa; biết toa nào cũng có người. P(An ở một toa chỉ có mình An)? | 7/25 | cards | XS20 |

## L22 · Đa hành động (XSS361 – XSS376) · 75 – 160 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS361** | Xúc xắc quyết định số bi | Gieo xúc xắc được k rồi rút k bi từ hộp 4 đỏ 3 xanh. P(k bi rút ra đều đỏ)? | 1/6 | tree | XS24 |
| **XSS362** | Toàn đỏ thì xúc xắc ra mấy? | Như trên, biết k bi rút ra đều đỏ. P(xúc xắc ra 1)? | 4/7 | tree | XS25 |
| **XSS363** | Chẵn hộp I, lẻ hộp II | Xúc xắc chẵn: rút từ hộp I (3 đỏ 2 xanh), lẻ: hộp II (1 đỏ 4 xanh), rút lần lượt 2 bi. Biết bi thứ hai đỏ: P(bi thứ nhất đỏ)? | 3/8 | tree | XS26 |
| **XSS364** | Số ngửa quyết định số bi | Tung 2 xu được k ngửa, rồi rút k + 1 bi từ hộp 3 đỏ 3 xanh. P(có ít nhất 1 bi đỏ)? | 61/80 | tree | XS24 |
| **XSS365** | Có đỏ thì hai xu ngửa? | Như trên, biết có ít nhất 1 bi đỏ. P(cả hai xu đều ngửa)? | 19/61 | tree | XS25 |
| **XSS366** | Xúc xắc pha màu hộp | Gieo xúc xắc được k; hộp có k bi đỏ và 6 − k bi xanh. Rút 1 bi được đỏ: P(k = 6)? | 2/7 | tree | XS25 |
| **XSS367** | Chọn hộp, chuyển, rồi rút | Xúc xắc 1–4: chuyển 1 bi từ I (2 đỏ 1 xanh) sang II (1 đỏ 2 xanh), 5–6: chuyển ngược lại; rút 1 bi từ hộp nhận. P(đỏ)? | 17/36 | tree | XS26 |
| **XSS368** | Đỏ gieo xúc xắc, xanh tung xu | Rút 1 bi (2 đỏ 2 xanh): đỏ thì gieo xúc xắc, xanh thì tung xu; ra 6 hoặc ngửa là thắng. Biết thắng: P(đã rút đỏ)? | 1/4 | tree | XS25 |
| **XSS369** | Xanh thì thêm hai xanh | Hộp 3 đỏ 2 xanh: rút 1 bi, đỏ thì bỏ ra ngoài, xanh thì trả lại kèm 2 bi xanh; rút lần hai được xanh. P(lần một xanh)? | 16/37 | tree | XS25 |
| **XSS370** | Đúng một ngửa | Gieo xúc xắc được k rồi tung k đồng xu, được đúng 1 ngửa. P(k ≤ 2)? | 8/15 | tree | XS25 |
| **XSS371** | Hộp vàng hay hộp trắng? | Gieo 2 xúc xắc: tổng ≥ 10 rút từ hộp vàng (4 đỏ 1 xanh), ngược lại hộp trắng (1 đỏ 4 xanh). Được đỏ: P(tổng ≥ 10)? | 4/9 | tree | XS25 |
| **XSS372** | Biết m = 3 | Gieo xúc xắc được n, rồi chọn ngẫu nhiên m từ 1 đến n. Biết m = 3: P(n = 6)? | 10/57 | tree | XS25 |
| **XSS373** | Gieo hai lần lấy lớn nhất | Tung xu: ngửa thì gieo xúc xắc 2 lần lấy số lớn nhất, sấp thì gieo 1 lần. Kết quả là 6: P(đã ra ngửa)? | 11/17 | tree | XS25 |
| **XSS374** | Một hay hai xúc xắc? | Rút 1 bi (1 đỏ 2 xanh): đỏ thì gieo 2 xúc xắc, xanh thì gieo 1. Số chấm (tổng) bằng 4: P(rút đỏ)? | 1/5 | tree | XS25 |
| **XSS375** | Nhiệm vụ nào thất bại? | Bốc thăm 1 trong 3 nhiệm vụ, thành công 0,9; 0,6; 0,3. Biết An thất bại: P(An bốc nhiệm vụ 3)? | 7/12 | tree | XS25 |
| **XSS376** | Ra 6 được gieo thêm | Gieo xúc xắc; nếu ra 6 thì gieo thêm 1 lần và cộng điểm. Biết tổng điểm chẵn: P(lần đầu ra 6)? | 1/5 | tree | XS25 |

## L23 · Điều kiện dừng (XSS377 – XSS392) · 75 – 160 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS377** | Dừng trong ba lần | Gieo xúc xắc đến khi ra 6. Biết số lần gieo không quá 3: P(đúng 2 lần)? | 30/91 | tree | XS20 |
| **XSS378** | Dừng ở lần thứ tư | Tung xu đến khi được 2 lần ngửa. Biết dừng ở lần 4: P(lần 1 là ngửa)? | 1/3 | tree | XS20 |
| **XSS379** | Đủ hai đỏ ở lần bốn | Hộp 3 đỏ 3 xanh, rút lần lượt đến khi được 2 bi đỏ. P(dừng ở lần thứ 4)? | 3/10 | urn | XS22 |
| **XSS380** | Kết thúc trước lượt 5 | A, B lần lượt gieo xúc xắc (A trước), ai ra 6 trước thắng. Biết kết thúc trước lượt 5: P(A thắng)? | 6/11 | tree | XS20 |
| **XSS381** | Hai mặt giống nhau liền | Tung xu đến khi có 2 lần liên tiếp cùng mặt. P(dừng sau đúng 4 lần)? | 1/8 | tree | XS22 |
| **XSS382** | Phi tiêu tối đa bốn lần | Ném phi tiêu đến khi trúng (mỗi lần 0,4), tối đa 4 lần. Biết có trúng: P(trúng ngay lần 1)? | 125/272 | tree | XS25 |
| **XSS383** | Số lần rút là số chẵn | Rút có hoàn lại (2 đỏ 3 xanh) đến khi được đỏ. Biết số lần rút là chẵn: P(đúng 2 lần)? | 16/25 | tree | XS20 |
| **XSS384** | Hai phát trúng liền | Bắn đến khi trúng 2 phát liên tiếp hoặc hết 4 viên, mỗi phát trúng 0,6. P(dừng vì trúng 2 liên tiếp)? | 81/125 | tree | XS22 |
| **XSS385** | Tổng vượt 3 | Gieo xúc xắc đến khi tổng ≥ 4. Biết dừng ở lần 2: P(lần đầu ra 1)? | 4/15 | tree | XS25 |
| **XSS386** | Dừng ở +2 hay −2? | Ngửa (2/3) +1 điểm, sấp −1; dừng khi đạt +2 hoặc −2. Biết dừng sau đúng 4 lần: P(dừng ở +2)? | 4/5 | tree | XS25 |
| **XSS387** | Đến khi gặp số chẵn | Rút lần lượt từ 6 bi số 1 đến 6 đến khi gặp số chẵn. Biết cần ít nhất 2 lần: P(cần đúng 3 lần)? | 3/10 | urn | XS20 |
| **XSS388** | Vòng quay ba ô | Vòng quay A (1/2), B (1/3), C (1/6); quay đến khi ra C. Biết quay đúng 3 lần: P(có ít nhất 1 lần A)? | 21/25 | tree | XS20 |
| **XSS389** | C thắng ngay vòng đầu? | A, B, C lần lượt gieo xúc xắc, ai ra 6 trước thắng. Biết C thắng: P(C thắng ở lượt đầu của C)? | 91/216 | tree | XS25 |
| **XSS390** | Đỏ lần hai ở lần năm | Rút có hoàn lại (1 đỏ 2 xanh) đến khi được đỏ lần thứ hai. P(dừng ở lần 5)? | 32/243 | tree | XS18 |
| **XSS391** | Ba lần thất bại rồi | Mỗi lần thử thành công 0,2, độc lập. Biết 3 lần đầu đều thất bại: P(thành công trong 2 lần tiếp)? | 0,36 | tree | XS23 |
| **XSS392** | Đỏ hay hai vàng liền? | Rút có hoàn lại (1 đỏ 1 xanh 1 vàng); dừng khi rút được đỏ hoặc 2 lần liên tiếp vàng. P(dừng vì đỏ)? | 4/5 | tree | XS30 |

## L24 · Cây vận dụng cao (XSS393 – XSS408) · 90 – 175 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS393** | Ba đồng xu, tung lại | Ba xu: chuẩn, hai mặt ngửa, hai mặt sấp. Chọn 1, tung ra ngửa; tung lại đồng đó. P(lại ngửa)? | 5/6 | tree | XS26 |
| **XSS394** | Hai xét nghiệm trái ngược | Bệnh 2 %. Test A: nhạy 0,9, dương giả 0,1; test B: nhạy 0,8, dương giả 0,05. A dương, B âm: P(bệnh)? | 36/967 ≈ 0,037 | tree | XS27 |
| **XSS395** | Ngày kia mưa thì mai? | Hôm nay mưa; mưa thì mai mưa 0,6, tạnh thì mai mưa 0,2. Biết ngày kia mưa: P(ngày mai mưa)? | 9/11 | tree | XS25 |
| **XSS396** | Hai sản phẩm cùng lô | Dây chuyền I (60 %) lỗi 3 %, II (40 %) lỗi 5 %. Lấy 2 sản phẩm cùng một dây chuyền, cả 2 lỗi. P(dây chuyền II)? | 27/77 | tree | XS26 |
| **XSS397** | Ba trạm trung chuyển | Tín hiệu qua 3 trạm, mỗi trạm lật bit với xác suất 0,1. P(tín hiệu nhận được đúng)? | 0,756 | tree | XS22 |
| **XSS398** | Tin đồn qua ba người | A kể B, B kể C; mỗi lần kể đúng 0,8, sai thì đảo nghĩa. Sự thật "có" hay "không" như nhau. C nghe "có": P(sự thật là có)? | 0,68 | tree | XS27 |
| **XSS399** | Thắng hai ván liên tiếp | Ai thắng 2 ván liên tiếp trước là vô địch; A thắng mỗi ván 0,6. P(A vô địch)? | 63/95 | tree | XS30 |
| **XSS400** | Ba tù nhân | 3 tù nhân, 1 người được tha. Cai ngục nói với A: "B sẽ bị xử". P(A được tha)? | 1/3 | tree | XS28 |
| **XSS401** | Hộp hai bi bí ẩn | Hộp 2 bi, mỗi bi đỏ hoặc xanh (1/2), độc lập. Rút có hoàn lại 3 lần đều đỏ: P(cả 2 bi đều đỏ)? | 4/5 | tree | XS26 |
| **XSS402** | Kéo dài không đổi cuộc chơi | Gieo xúc xắc: 1, 2 thắng; 3 thua; 4, 5, 6 gieo lại. Biết trò chơi kéo dài ít nhất 3 lượt: P(thắng)? | 2/3 | tree | XS28 |
| **XSS403** | Đỏ thì sang hộp kia | Rút từ hộp I (2 đỏ 1 xanh): đỏ thì bỏ sang hộp II (1 đỏ 2 xanh) rồi rút từ II, xanh thì rút tiếp từ I. P(lần hai đỏ)? | 2/3 | tree | XS24 |
| **XSS404** | Lần hai đỏ thì lần một? | Như trên, biết lần rút thứ hai được đỏ. P(lần một rút xanh)? | 1/2 | tree | XS25 |
| **XSS405** | Kiến trên tứ diện | Kiến ở đỉnh A của tứ diện, mỗi bước sang 1 trong 3 đỉnh còn lại. P(sau 5 bước về A)? | 20/81 | tree | XS30 |
| **XSS406** | Tổng số ngửa là 2 | An và Bình mỗi người tung 2 xu. Biết tổng số ngửa là 2: P(mỗi người đúng 1 ngửa)? | 2/3 | tree | XS20 |
| **XSS407** | Sinh đến khi có con trai | Mỗi gia đình sinh đến khi có con trai, tối đa 3 con. Tỉ lệ con trai trong toàn bộ trẻ em? | 1/2 | tree | XS28 |
| **XSS408** | Có hòa thì sao? | Mỗi ván A thắng 0,5, hòa 0,2, thua 0,3; dừng khi A thắng 2 ván hoặc thua 2 ván. P(A thắng chung cuộc)? | 175/256 | tree | XS30 |

## L25 · Hay – lạ – độc đáo (XSS409 – XSS424) · 75 – 170 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS409** | Xúc xắc không bắc cầu | Xúc xắc A: 2 2 4 4 9 9; B: 1 1 6 6 8 8; C: 3 3 5 5 7 7. A thắng B 5/9, B thắng C 5/9. P(C thắng A)? | 5/9 | grid | XS30 |
| **XSS410** | Hành khách mất vé | n hành khách lên máy bay n ghế; người đầu mất vé ngồi bừa, người sau ngồi đúng ghế nếu còn. P(người cuối đúng ghế)? | 1/2 | cards | XS30 |
| **XSS411** | Trùng sinh nhật với bạn | Lớp 23 người. P(có người trùng ngày sinh với chính bạn)? | ≈ 0,059 | curve | XS13 |
| **XSS412** | Đồng xu trên nền gạch | Ném đồng xu bán kính 1 lên nền gạch ô vuông cạnh 4. P(đồng xu nằm gọn trong một ô)? | 1/4 | square | XS30 |
| **XSS413** | Đếm cá trong hồ | Đánh dấu 50 con cá rồi thả lại. Lần sau bắt 40 con thấy 8 con có dấu. Ước lượng số cá trong hồ? | 250 | sim | XS05 |
| **XSS414** | Chuỗi dài là bình thường | Tung xu 20 lần. P(có ít nhất 4 lần liên tiếp cùng mặt)? | ≈ 0,768 | tree | XS30 |
| **XSS415** | Đoán lá đỏ | Lật dần bộ bài, bạn được hô "đỏ" đúng một lần trước một lá. Chiến thuật tốt nhất thắng với xác suất? | 1/2 | cards | XS30 |
| **XSS416** | Ba chiếc mũ | 3 người đội mũ đỏ/xanh ngẫu nhiên, thấy mũ người khác, được đoán hoặc bỏ qua. Cả đội thắng nếu có người đúng và không ai sai. Chiến thuật tốt nhất? | 3/4 | tree | XS30 |
| **XSS417** | Bốn tù nhân, bốn hộp | 4 tù nhân, 4 hộp chứa tên ngẫu nhiên; mỗi người mở 2 hộp tìm tên mình. Chiến thuật đi theo vòng: P(ai cũng tìm thấy)? | 5/12 | cards | XS30 |
| **XSS418** | Penney ba đồng xu | Tung xu liên tục. P("sấp ngửa ngửa" xuất hiện trước "ngửa ngửa ngửa")? | 7/8 | sim | XS30 |
| **XSS419** | Hai hộp diêm | Mỗi túi có 1 hộp 2 que, mỗi lần lấy ngẫu nhiên 1 túi. Khi thấy một hộp rỗng: P(hộp kia cũng rỗng)? | 3/8 | tree | XS30 |
| **XSS420** | Xếp hàng không có tiền thối | 2 người cầm tờ 10 nghìn, 2 người cầm tờ 20 nghìn xếp hàng mua vé 10 nghìn; quầy không có tiền lẻ. P(không ai phải chờ)? | 1/3 | cards | XS30 |
| **XSS421** | Bốn điểm trên nửa đường tròn | Chọn 4 điểm ngẫu nhiên trên đường tròn. P(cả 4 cùng nằm trên một nửa đường tròn)? | 1/2 | geo | XS30 |
| **XSS422** | Que gãy làm đôi | Bẻ que tại một điểm ngẫu nhiên. P(đoạn dài gấp ít nhất 2 lần đoạn ngắn)? | 2/3 | geo | XS30 |
| **XSS423** | Nghịch lý xe buýt | Xe buýt cách nhau 10 phút hoặc 20 phút (xen kẽ). Bạn đến bến ngẫu nhiên. P(rơi vào khoảng 20 phút)? | 2/3 | geo | XS28 |
| **XSS424** | Lớp 30 người, tháng sinh | Lớp có 30 học sinh. P(có ít nhất 2 bạn sinh cùng tháng)? | 1 (chắc chắn) | grid | XS13 |

## L26 · Mẹo đếm – đối xứng (XSS425 – XSS440) · 60 – 150 s

| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **XSS425** | Đủ sáu mặt trong sáu lần | Gieo 6 con xúc xắc. P(xuất hiện đủ 6 mặt)? | 5/324 | grid | XS09 |
| **XSS426** | Mỗi người một lá át | Chia bộ bài 52 lá cho 4 người, mỗi người 13 lá. P(mỗi người có đúng 1 lá át)? | 2197/20825 ≈ 0,105 | cards | XS10 |
| **XSS427** | Cùng màu hay khác màu? | Rút 2 lá từ bộ bài 52 lá. P(hai lá khác màu)? | 26/51 | cards | XS07 |
| **XSS428** | Tổng ba xúc xắc lớn hơn 10 | Gieo 3 xúc xắc. P(tổng số chấm lớn hơn 10)? | 1/2 | grid | XS09 |
| **XSS429** | Cao nhất cạnh thấp nhất | 10 bạn xếp hàng ngẫu nhiên. P(bạn cao nhất đứng cạnh bạn thấp nhất)? | 1/5 | cards | XS12 |
| **XSS430** | Tích chia hết cho 6 | Gieo 3 xúc xắc. P(tích số chấm chia hết cho 6)? | 133/216 | grid | XS15 |
| **XSS431** | Tích chia hết cho 4 | Chọn 3 số khác nhau từ 1 đến 20. P(tích chia hết cho 4)? | 53/76 | grid | XS15 |
| **XSS432** | Chia kẹo | 10 viên kẹo giống nhau chia cho 3 bạn, mọi cách chia đồng khả năng. P(bạn nào cũng có kẹo)? | 6/11 | grid | XS10 |
| **XSS433** | Ước chính phương | Chọn ngẫu nhiên một ước dương của 360. P(ước đó là số chính phương)? | 1/6 | grid | XS07 |
| **XSS434** | Đúng một lá đúng chỗ | Xếp ngẫu nhiên 5 lá thư vào 5 phong bì. P(có đúng 1 lá đúng địa chỉ)? | 3/8 | cards | XS13 |
| **XSS435** | Tập con có tổng chẵn | Chọn ngẫu nhiên một tập con của {1; 2; 3; 4; 5}. P(tổng các phần tử là số chẵn)? | 1/2 | grid | XS30 |
| **XSS436** | A là tập con của B | Chọn ngẫu nhiên 2 tập con A, B của {1; 2; 3}. P(A ⊂ B)? | 27/64 | grid | XS30 |
| **XSS437** | Số này chia hết số kia | Gieo 2 xúc xắc được a, b. P(a là ước của b)? | 7/18 | grid | XS09 |
| **XSS438** | Bốn xúc xắc sát nhau | Gieo 4 xúc xắc. P(số lớn nhất và nhỏ nhất hơn kém nhau không quá 1)? | 19/324 | grid | XS09 |
| **XSS439** | Hai ô trên bàn cờ | Chọn 2 ô của bàn cờ 8 × 8. P(cùng màu và không cùng hàng, cùng cột)? | 25/63 | grid | XS07 |
| **XSS440** | Monty Hall bốn cửa | 4 cửa, 1 có xe. Bạn chọn 1, người dẫn mở 2 cửa có dê. Đổi sang cửa còn lại: P(trúng xe)? | 3/4 | cards | XS28 |
