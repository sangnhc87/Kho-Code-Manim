# SANG MATH · COMB24 V2 · CATALAN, DYCK VÀ NGUYÊN LÝ PHẢN XẠ

## Bản thuyết minh đồng bộ

Số nhịp: 48 · 8 chương · TTS=off
Tổng thời lượng dự kiến: 1445.2 giây.
Lời giảng bên dưới là nội dung đầy đủ được đưa vào tổng hợp giọng đọc; không cắt tùy ý.


## 01 · DÃY NGOẶC ĐÚNG VÀ CATALAN

### Nhịp 01 · 00:00 · Ngoặc mở, ngoặc đóng

Hãy tưởng tượng chúng ta có ba ngoặc mở và ba ngoặc đóng giống nhau. Nếu chỉ kiểm tra tổng số ngoặc ở cuối, nhiều dãy sai vẫn lọt qua. Một dãy ngoặc đúng đòi hỏi ở mọi vị trí đọc từ trái sang phải, số ngoặc đóng không vượt số ngoặc mở. Điều kiện theo từng tiền tố ấy chính là chiếc cầu nối sang mô hình đường đi, nơi mỗi bước có thể được kiểm tra trực quan.

**Trên màn hình:** Ba cặp ngoặc () | Mỗi tiền tố phải đủ ngoặc mở | Cuối dãy số mở bằng số đóng
**Ghi nhớ:** Đúng toàn cục chưa đủ; phải đúng từng tiền tố.

### Nhịp 02 · 00:30 · Chuyển ngoặc thành độ cao

Ta đổi mỗi ngoặc mở thành một bước lên và mỗi ngoặc đóng thành một bước xuống. Đọc dãy ngoặc từ trái sang phải sẽ tạo một đường gấp khúc. Chiều cao tại một vị trí bằng số ngoặc mở trừ số ngoặc đóng đã đọc. Dãy đúng khi và chỉ khi đường này bắt đầu ở không, kết thúc ở không và không lần nào đi xuống phía dưới đường cơ sở. Ta đã biến một điều kiện chữ thành một hình có thể quan sát.

**Trên màn hình:** Ngoặc mở: đi lên một đơn vị | Ngoặc đóng: đi xuống một đơn vị | Không bao giờ xuống dưới trục
**Ghi nhớ:** Dãy ngoặc đúng tương ứng đường đi không âm.

### Nhịp 03 · 01:00 · Năm dãy đúng với ba cặp

Hãy xem năm dãy ngoặc đúng của ba cặp. Mỗi dãy tạo ra một đường đi có dáng khác nhau: có dãy nhấp nhô thấp, có dãy lên cao rồi mới hạ xuống. Tất cả đều giữ cân bằng tiền tố. Khi đổi chỗ các ngoặc giống nhau, chúng ta không tạo ra một kết quả mới. Vì vậy số cấu trúc đúng là năm, một con số nhỏ nhưng mở đầu cho một họ số tổ hợp nổi tiếng.

**Trên màn hình:** ()()()  và  ()(()) | (())()  và  (()()) | ((()))  là trường hợp còn lại
**Ghi nhớ:** Có năm cấu trúc, không phải sáu giai thừa.

### Nhịp 04 · 01:30 · Từ ba lên bốn cặp

Khi tăng số cặp ngoặc, số lời giải không tăng như hai mũ n và cũng không phải n giai thừa. Nếu có không cặp nào, ta quy ước chỉ có một dãy rỗng. Một cặp có một cách, hai cặp có hai cách, ba cặp có năm cách, bốn cặp có mười bốn cách và năm cặp có bốn mươi hai cách. Đây là các số Catalan; nhiệm vụ của chúng ta không phải ghi nhớ mà phải hiểu vì sao chúng xuất hiện.

**Trên màn hình:** Ba cặp cho 5 dãy | Bốn cặp cho 14 dãy | Năm cặp cho 42 dãy
**Ghi nhớ:** Dãy 1, 1, 2, 5, 14, 42 là Catalan.

### Nhịp 05 · 02:00 · Vì sao phải giữ ràng buộc?

Ví dụ một dãy có tổng số ngoặc mở và đóng bằng nhau nhưng ký tự đầu là ngoặc đóng. Ngay lập tức ta gặp một dấu đóng chưa có dấu mở tương ứng, nên dãy sai. Trên hình, bước đầu tiên nằm dưới trục và được tô đỏ. Hãy quan sát các đoạn bị loại: không thể cứu một tiền tố đã sai chỉ bằng cách thêm ngoặc mở ở phía sau. Đây là điểm mà phép đếm trực tiếp dễ bị nhầm.

**Trên màn hình:** Dãy )(()() có số ngoặc cân bằng | Nhưng ngay bước đầu xuống mức âm | Đường không hợp lệ bị tô đỏ
**Ghi nhớ:** Cân bằng tổng không bảo đảm cân bằng tiền tố.

### Nhịp 06 · 02:30 · Vấn đề trung tâm của tập

Nếu quên điều kiện tiền tố, việc đếm rất đơn giản: chọn n vị trí đặt bước lên trong tổng cộng hai n vị trí. Kết quả là tổ hợp chập n của hai n. Nhưng không phải tất cả những lựa chọn đó tương ứng dãy ngoặc đúng. Chúng ta cần hiểu số đường sai và tìm một cách đếm chúng thật khéo. Nguyên lý phản xạ ở chương sau sẽ thực hiện chính xác bước còn thiếu.

**Trên màn hình:** Tất cả các cách chọn n bước lên | Và n bước xuống là C(n,2n) | Phải loại đường xuống dưới trục
**Ghi nhớ:** Catalan bằng tất cả trừ số đường sai.


## 02 · ĐƯỜNG ĐI DYCK TRÊN LƯỚI

### Nhịp 07 · 03:00 · Đường Dyck là gì?

Một đường Dyck là dãy hai n bước, gồm đúng n bước lên và n bước xuống, nhưng không bao giờ có tổng độ cao âm. Khi xem hình, học sinh có thể kéo theo đầu bút từ trái sang phải và quan sát chỉ số độ cao từng bước. Nếu đường chạm trục, nó vẫn hợp lệ; chỉ bước xuống dưới trục mới vi phạm. Quy ước này giúp phân biệt đường Dyck với bài toán lá phiếu nghiêm ngặt sẽ xuất hiện sau.

**Trên màn hình:** Có n bước U và n bước D | Khởi đầu và kết thúc ở độ cao 0 | Mọi độ cao trung gian không âm
**Ghi nhớ:** Đường Dyck mã hóa ngoặc đúng.

### Nhịp 08 · 03:30 · Mở cây lựa chọn

Ta mở một cây lựa chọn từng bước. Ở gốc, nếu đi xuống, chiều cao âm ngay, vì thế nhánh ấy bị loại tức thì. Tại độ cao dương, có thể lên hoặc xuống, miễn là không dùng quá n bước mỗi loại. Mỗi nhánh hoàn chỉnh kết thúc ở độ cao không tương ứng một đường Dyck. Cách dựng từng nhánh này cũng giống quy hoạch động: ta chỉ lưu những trạng thái còn hợp lệ.

**Trên màn hình:** Tại độ cao 0 không được chọn D | Ở độ cao dương có thể U hoặc D | Đủ n bước mỗi loại thì dừng
**Ghi nhớ:** Cắt nhánh sai sớm tránh liệt kê thừa.

### Nhịp 09 · 04:00 · Cùng một kết quả, hai ngôn ngữ

Một cấu trúc ngoặc như mở mở đóng mở đóng đóng được ánh xạ thành lên lên xuống lên xuống xuống. Ánh xạ có thể đảo lại từng bước nên không mất thông tin. Mỗi dãy ngoặc đúng cho đúng một đường Dyck, và mỗi đường Dyck cho đúng một dãy ngoặc đúng. Trong tổ hợp, một phép ghép tương ứng một-một như vậy gọi là song ánh, rất mạnh vì biến phép đếm của đối tượng khó thành phép đếm của đối tượng dễ.

**Trên màn hình:** Dãy (()()) là ngoặc đúng | Đường UUDUDD tương ứng | Hai biểu diễn mã hóa cùng một đối tượng
**Ghi nhớ:** Đây là một song ánh tự nhiên.

### Nhịp 10 · 04:30 · Các đường bị loại

Trong nhóm đường sai, đánh dấu thời điểm đầu tiên chiều cao bằng âm một. Vì đường bắt đầu tại không và thay đổi từng đơn vị, lần đầu xuống âm luôn phải xuống đúng âm một. Trước thời điểm đó đường vẫn ở mức không hoặc dương. Bước đánh dấu tạo điểm mốc rất rõ ràng để dựng một phép biến đổi có thể đảo ngược, thay vì cố đếm hàng loạt hình gấp khúc khác nhau.

**Trên màn hình:** Nếu tiền tố âm lần đầu xuất hiện | Đánh dấu bước đầu tiên chạm mức −1 | Chúng ta có thể phản xạ tiền tố ấy
**Ghi nhớ:** Chỉ cần biết lần vi phạm đầu tiên.

### Nhịp 11 · 05:00 · Tập tất cả đường cân bằng

Với ba bước lên và ba bước xuống, ta chỉ cần chọn vị trí của ba bước lên trong sáu vị trí, có hai mươi dãy. Sơ đồ hiển thị cả năm đường tốt và mười lăm đường sai. Đếm từng đường sai bằng mắt không hiệu quả khi n tăng, nhưng chúng đều có một đặc điểm chung là từng chạm mức âm một. Chúng ta sắp biến đặc điểm đó thành một phép đếm tổ hợp đơn giản.

**Trên màn hình:** Không ràng buộc: C_n^(2n) | Với n=3: C_3^6 = 20 | Đường hợp lệ chỉ có 5
**Ghi nhớ:** Cần loại đúng 15 đường sai.

### Nhịp 12 · 05:30 · Hình vuông và đường chéo

Một cách vẽ khác đưa mỗi bước lên thành bước dọc và mỗi bước xuống thành bước ngang trên lưới vuông. Đường đi từ góc dưới trái đến điểm n phẩy n phải ở một phía của đường chéo chính. Đây vẫn là cùng một điều kiện tiền tố, chỉ thay đổi hệ tọa độ. Ở các bài toán đường đi có chướng ngại hoặc ranh giới, mô hình lưới đặc biệt hữu ích vì có thể dùng song ánh và nguyên lý phản xạ.

**Trên màn hình:** Quy ước U ↔ đi lên, D ↔ đi ngang | Đi từ (0,0) đến (n,n) | Không vượt đường chéo tương ứng
**Ghi nhớ:** Mô hình lưới vuông và ngoặc là tương đương.


## 03 · NGUYÊN LÝ PHẢN XẠ

### Nhịp 13 · 06:00 · Chọn đường sai bất kỳ

Chọn một đường đi sai bất kỳ với n bước lên và n bước xuống. Ta đi dọc từ đầu và đánh dấu lần đầu tiên đường chạm mức âm một. Có thể đường này còn xuống sâu hơn về sau, nhưng không ảnh hưởng. Chỉ đoạn tiền tố đến mốc đầu tiên mới được thay đổi. Đây là điều kiện quan trọng: nếu tự chọn một chỗ phản xạ bất kỳ, chúng ta có thể đếm trùng hoặc không thể đảo phép biến đổi.

**Trên màn hình:** Chạm −1 tại lần đầu tiên | Đánh dấu đoạn từ đầu đến mốc | Đoạn sau giữ nguyên
**Ghi nhớ:** Mốc đầu tiên làm phép biến đổi duy nhất.

### Nhịp 14 · 06:30 · Phản xạ đoạn đầu

Ta lật tất cả các bước lên thành xuống và các bước xuống thành lên trong đoạn tiền tố được đánh dấu. Vì tiền tố cũ kết thúc ở âm một, sau khi lật nó kết thúc ở dương một. Toàn bộ đường mới không nhất thiết là Dyck, nhưng điều đó không quan trọng: ta đang chuyển đối tượng sai thành một dãy bước có số lượng lên và xuống thay đổi. Phần phía sau mốc được giữ nguyên, giúp dễ truy vết phép biến đổi.

**Trên màn hình:** Trong tiền tố, đổi U thành D | Và đổi D thành U | Phần hậu tố không thay đổi
**Ghi nhớ:** Mỗi đường sai cho một đường mới xác định.

### Nhịp 15 · 07:00 · Đếm số bước sau phản xạ

Trước phản xạ, tiền tố đi từ không đến âm một nên có đúng một bước xuống nhiều hơn bước lên. Khi đổi loại tất cả bước trong tiền tố, tổng số bước lên của cả dãy tăng một còn số bước xuống giảm một. Như vậy đường mới có n cộng một bước lên và n trừ một bước xuống, trong tổng hai n vị trí. Không còn ràng buộc tiền tố nào phải thỏa khi đếm tập đường mới.

**Trên màn hình:** Ban đầu có n U và n D | Tiền tố có một D nhiều hơn U | Sau lật có n+1 U và n−1 D
**Ghi nhớ:** Đường sai biến thành lựa chọn n+1 vị trí U.

### Nhịp 16 · 07:30 · Chứng minh đảo ngược

Để khẳng định đây là song ánh, cần biết cách đi ngược. Một dãy gồm n cộng một bước lên và n trừ một bước xuống kết thúc ở độ cao hai, nên chắc chắn có lúc chạm mức dương một. Hãy tìm lần đầu tiên nó chạm dương một và lật lại chính tiền tố đó. Ta thu được đường cân bằng đã từng chạm âm một. Hai phép biến đổi đảo nhau, vì thế không có đường sai nào bị bỏ hoặc bị tính hai lần.

**Trên màn hình:** Đường mới kết thúc ở độ cao 2 | Tìm lần đầu đường mới chạm +1 | Lật lại đúng tiền tố tới +1
**Ghi nhớ:** Phản xạ là song ánh, không mất hay trùng.

### Nhịp 17 · 08:00 · Áp dụng cho n bằng 3

Trong trường hợp ba cặp bước, nhóm tất cả có hai mươi đường. Nhóm sai được ghép một-một với các dãy gồm bốn bước lên và hai bước xuống. Có tổ hợp chập bốn của sáu, tức mười lăm dãy như vậy. Lấy hai mươi trừ mười lăm cho kết quả năm. Quan trọng hơn, phép tính này không phụ thuộc vào việc ta đã liệt kê năm đường tốt bằng mắt ở chương đầu; nó là một chứng minh tổng quát có thể áp dụng cho mọi n.

**Trên màn hình:** Có 20 đường cân bằng | Đường phản xạ có 4 U và 2 D | Số đường sai là C_4^6 = 15
**Ghi nhớ:** 20 trừ 15 chỉ còn 5 đường tốt.

### Nhịp 18 · 08:30 · Dùng lại trong bài lá phiếu

Nguyên lý phản xạ không chỉ dùng để tính Catalan. Khi một con đường phải luôn nằm một phía của đường biên, ta thường có thể ghép những đường vượt biên với một tập đường dễ đếm bằng cách phản xạ tại lần vi phạm đầu tiên. Tuy nhiên, nếu đề bài yêu cầu nằm phía trên một cách nghiêm ngặt, chạm biên cũng bị cấm; khi đó điểm mốc thay đổi. Học sinh cần đọc đúng dấu bất đẳng thức trước khi áp dụng kỹ thuật này.

**Trên màn hình:** Đổi ranh giới cấm thành điểm phản xạ | Cặp đường được đếm qua số bước | Điều kiện nghiêm ngặt cần thay đổi mốc
**Ghi nhớ:** Phản xạ rất mạnh nhưng phải đúng ranh giới.


## 04 · CHỨNG MINH CÔNG THỨC CATALAN

### Nhịp 19 · 09:00 · Công thức hiệu hai tổ hợp

Từ song ánh phản xạ, chúng ta có thể viết số Catalan bằng tổng số đường có n bước lên và n bước xuống trừ số đường sai. Biểu thức là hiệu của hai hệ số tổ hợp liên tiếp, chứ chưa phải công thức dạng phân số nổi tiếng. Hãy dừng ở đây để học sinh tự dự đoán rằng hai số hạng rất gần nhau có thể rút gọn đẹp. Phép biến đổi tiếp theo chỉ là đại số, còn phần quan trọng nhất của chứng minh đã nằm trong song ánh.

**Trên màn hình:** Đường cân bằng: C_n^(2n) | Đường sai: C_(n+1)^(2n) | Đường tốt là phần còn lại
**Ghi nhớ:** Đếm tốt bằng tất cả trừ phản xạ.

### Nhịp 20 · 09:30 · Rút gọn tỷ số

Xét tỷ số của hai tổ hợp chập n cộng một và chập n cùng bậc hai n. Sau khi rút gọn giai thừa, tỷ số bằng n chia n cộng một. Do đó hiệu của chúng chính là một phần trên n cộng một lần tổ hợp chập n của hai n. Biểu thức rất gọn này có vẻ kỳ lạ vì phép chia luôn cho số nguyên; lời giải bằng phản xạ đã chứng minh tính nguyên ấy theo một ý nghĩa tổ hợp rõ ràng.

**Trên màn hình:** C_(n+1)^(2n) / C_n^(2n) = n/(n+1) | Lấy nhân tử chung C_n^(2n) | Thu được hệ số 1/(n+1)
**Ghi nhớ:** Catalan là tổ hợp chia cho n+1.

### Nhịp 21 · 10:00 · Công thức Catalan

Viết tổ hợp bằng giai thừa ta được công thức quen thuộc của số Catalan: hai n giai thừa chia cho n giai thừa nhân n cộng một giai thừa. Khi n bằng bốn, kết quả là mười bốn; khi n bằng năm là bốn mươi hai. Công thức này xuất hiện ở rất nhiều bài toán mà thoạt nhìn không hề liên quan đến ngoặc hay đường đi. Ở phần tiếp theo, chúng ta sẽ tìm ra vì sao những đối tượng ấy có chung số lượng.

**Trên màn hình:** C_n = (2n)!/[n!(n+1)!] | n=4 cho C4 =14 | n=5 cho C5 =42
**Ghi nhớ:** Một công thức, nhiều cấu trúc rời rạc.

### Nhịp 22 · 10:30 · Kiểm tra các trường hợp biên

Những trường hợp nhỏ rất quan trọng khi thiết lập truy hồi. Nếu không có cặp ngoặc nào, ta vẫn có một dãy rỗng hợp lệ. Với một cặp chỉ có duy nhất một dãy, còn hai cặp có hai dãy lồng nhau hoặc đặt cạnh nhau. Nếu tự ý lấy Catalan không bằng không, các công thức nhân và tổng ở chương truy hồi sẽ sai ngay. Trong lập trình kiểm thử cũng vậy, phải cho số hạng đầu tiên giá trị đúng.

**Trên màn hình:** C0=1 tương ứng đối tượng rỗng | C1=1 tương ứng duy nhất một cặp | C2=2 tương ứng hai cấu trúc
**Ghi nhớ:** Không bỏ quên cấu trúc rỗng khi truy hồi.

### Nhịp 23 · 11:00 · Nhị thức Newton quay trở lại

Video mười bảy và mười tám đã dạy chúng ta rằng hệ số của x mũ n trong một lũy thừa nhị thức là tổ hợp chập n. Ở đây cùng một hệ số xuất hiện vì cần chọn vị trí của n bước lên. Tuy nhiên điều kiện tiền tố làm phép đếm không còn là nhị thức Newton đơn thuần. Chúng ta phải dùng phản xạ để lọc chính xác phần hợp lệ. Đây là ví dụ đẹp về việc hai kỹ thuật tổ hợp bổ trợ cho nhau.

**Trên màn hình:** C_n^(2n) từ phép chọn vị trí | Catalan là một phần của các lựa chọn | Song ánh lọc ra những đường hợp lệ
**Ghi nhớ:** Tổ hợp, Nhị thức Newton và Catalan kết nối nhau.

### Nhịp 24 · 11:30 · Cảnh báo: không lẫn với số đường tùy ý

Nếu học sinh nói có hai khả năng ở mỗi bước rồi lấy hai mũ tám, đó là số tất cả dãy tám ký tự lên xuống không giới hạn số bước lên và xuống. Nhưng bài Dyck yêu cầu đúng bốn bước lên và bốn bước xuống, nên không gian tổng chỉ có tổ hợp chập bốn của tám, bằng bảy mươi. Sau đó mới áp điều kiện không âm để còn mười bốn. Xác định sai tổng ban đầu là một lỗi phổ biến trong những bài đếm có ràng buộc.

**Trên màn hình:** C4=14 là đường Dyck bậc 4 | Tổng đường 4 lên, 4 xuống là 70 | Không được lấy 2^8 làm mẫu số
**Ghi nhớ:** Xác định không gian tổng trước khi trừ.


## 05 · SONG ÁNH: CÂY VÀ ĐA GIÁC

### Nhịp 25 · 12:00 · Tam giác hóa đa giác

Hãy xem một ngũ giác lồi. Muốn chia nó thành ba tam giác bằng các đường chéo không cắt nhau, ta phải chọn hai đường chéo thích hợp. Mặc dù bài toán không có dấu ngoặc, số cách là năm, bằng Catalan thứ ba. Trên màn hình, các đường chéo sẽ được vẽ theo từng phương án mà không làm biến dạng đa giác. Chúng ta có thể hỏi vì sao hai đối tượng hình học và đại số lại cho chung số lượng; câu trả lời nằm ở cách chia cấu trúc thành hai phần con.

**Trên màn hình:** Vẽ một ngũ giác lồi | Nối hai đường chéo không cắt nhau | Có năm cách tam giác hóa
**Ghi nhớ:** Tam giác hóa (n+2) đỉnh được C_n cách.

### Nhịp 26 · 12:30 · Lục giác có 14 cách

Với một lục giác lồi, có mười bốn cách chia thành bốn tam giác bằng các đường chéo không cắt nhau. Ta không cần liệt kê cùng lúc cả mười bốn hình quá nhỏ; video lần lượt giữ một cạnh gốc và đánh dấu tam giác kề cạnh ấy. Tam giác gốc tách phần còn lại thành hai đa giác độc lập. Mô hình ấy sẽ trở thành một phép nhân số cách ở hai phía, rồi cộng theo mọi vị trí có thể của đỉnh thứ ba.

**Trên màn hình:** Sáu đỉnh: bốn tam giác | Các đường chéo không giao nhau | Kết quả là Catalan thứ tư
**Ghi nhớ:** Số Catalan đếm cách phân rã đa giác.

### Nhịp 27 · 13:00 · Cây nhị phân có thứ tự

Một cây nhị phân đầy đủ có mỗi nút trong đúng hai nhánh con. Khi các nhánh trái và phải được phân biệt, số hình dạng cây với n nút trong chính là Catalan thứ n. Ví dụ ba nút trong cho năm cấu trúc. Việc đảo cây con trái sang phải thường làm thay đổi cây, vì hai vị trí được gắn vai trò khác nhau. Đây là ví dụ quan trọng cho quy tắc: trước khi chia một phép đếm thành tích, phải nói rõ đối tượng có xét thứ tự hay không.

**Trên màn hình:** Một nút gốc, nhánh trái và nhánh phải | Thứ tự trái/phải có ý nghĩa | n nút trong cho C_n cây
**Ghi nhớ:** Thứ tự của hai cây con không được tráo tùy ý.

### Nhịp 28 · 13:30 · Ngoặc hóa phép nhân

Cho bốn thừa số theo đúng thứ tự a, b, c, d. Nếu ta chỉ được đặt ngoặc để thay đổi trình tự thực hiện phép nhân mà không hoán đổi các thừa số, có năm cách ngoặc hóa đầy đủ. Mỗi cách tương ứng một cây nhị phân: phép nhân cuối cùng là nút gốc, hai nhóm con nằm bên trái và phải. Bằng cách chuyển giữa ngoặc và cây, học sinh thấy rõ song ánh chứ không chỉ ghi nhận một phép trùng số tình cờ.

**Trên màn hình:** Bốn thừa số a, b, c, d | Giữ thứ tự các thừa số | Có năm cách đặt cặp ngoặc
**Ghi nhớ:** Số cách ngoặc hóa n+1 phần tử là C_n.

### Nhịp 29 · 14:00 · Giải thích cấu trúc chung

Đa giác, cây nhị phân và cách ngoặc hóa đều có một thao tác tách đầu tiên: chọn một tam giác gốc, một nút gốc hoặc phép nhân ngoài cùng. Sau khi chọn, bài toán còn lại phân thành hai phần độc lập. Số cách dựng hai phần cùng lúc là tích hai số Catalan nhỏ hơn; còn số vị trí tách khác nhau được cộng lại. Cấu trúc chung ấy chính là lý do các đối tượng rất khác nhau lại có cùng dãy số.

**Trên màn hình:** Chọn phép tách ở gốc | Hai nửa là các bài toán cùng loại | Số cách bằng tích, rồi cộng
**Ghi nhớ:** Các mô hình cùng chia được theo một lõi cấu trúc.

### Nhịp 30 · 14:30 · Song ánh không phải chỉ trùng đáp số

Điều quan trọng của phương pháp song ánh là không đủ để tính vài số nhỏ rồi nói hai mô hình giống nhau. Ta cần có quy tắc biến đổi cụ thể từ một cấu trúc sang cấu trúc kia và một quy tắc đảo để khôi phục. Ví dụ đọc một cây theo hành trình quanh các cạnh có thể mã hóa thành chuỗi bước lên xuống. Khi mỗi bước mã hóa được giải thích rõ và có thể đảo, tính tương ứng một-một được chứng minh, nhờ đó số lượng bằng nhau với mọi kích thước.

**Trên màn hình:** Phải xây dựng ánh xạ đi và về | Mỗi đối tượng tương ứng duy nhất | Ánh xạ phải bảo toàn cấu trúc
**Ghi nhớ:** Để chứng minh bằng song ánh cần tính khả nghịch.


## 06 · TRUY HỒI VÀ HÀM SINH CATALAN

### Nhịp 31 · 15:00 · Phân tích ngoặc đúng

Một dãy ngoặc đúng khác rỗng luôn bắt đầu bằng dấu mở. Dấu đóng khớp với nó xác định duy nhất một đoạn bên trong A và đoạn còn lại B ở phía sau. Cả A và B đều là dãy ngoặc đúng; nếu một đoạn rỗng vẫn có đúng một lựa chọn. Nhờ cặp ngoặc khớp đầu tiên, chúng ta nhận được một phép phân rã duy nhất, không trùng lặp. Đây là chìa khóa để xây dựng truy hồi Catalan không cần nhắc đến phản xạ.

**Trên màn hình:** Dãy không rỗng có dạng (A)B | A và B đều là dãy ngoặc đúng | A có i cặp, B có n−1−i cặp
**Ghi nhớ:** Tách theo cặp ngoặc khớp đầu tiên.

### Nhịp 32 · 15:30 · Nhân các lựa chọn

Giả sử toàn bộ dãy có n cặp ngoặc và bên trong cặp đầu tiên có i cặp. Phần A được chọn theo Catalan thứ i, còn phần B chứa n trừ một trừ i cặp và có Catalan tương ứng. Vì sau khi chọn A, cách chọn B là độc lập, quy tắc nhân cho tích hai số. Hình sẽ chia dãy thành khối trong và khối sau, giúp học sinh thấy tại sao phép nhân xuất hiện và vì sao cần giữ dấu ngoặc khớp.

**Trên màn hình:** A có i cặp: C_i lựa chọn | B có n−1−i cặp: C_(n−1−i) | Với i cố định: nhân hai số
**Ghi nhớ:** Hai phần độc lập tạo tích Catalan.

### Nhịp 33 · 16:00 · Cộng mọi vị trí tách

Chúng ta chưa biết i bằng bao nhiêu. Nó có thể từ không cho đến n trừ một. Hai trường hợp có số cặp trong A khác nhau thì chắc chắn không trùng một dãy, vì cặp ngoặc khớp đầu tiên sẽ nằm ở vị trí khác nhau. Vì vậy quy tắc cộng cho tổng tất cả các tích vừa tìm được. Đây là truy hồi Catalan và cũng là một phương pháp tính trực tiếp bằng quy hoạch động, sử dụng những kết quả nhỏ để dựng kết quả lớn.

**Trên màn hình:** i chạy từ 0 đến n−1 | Mỗi i là một trường hợp rời nhau | Cộng những tích tương ứng
**Ghi nhớ:** Truy hồi Catalan xuất hiện từ phân rã duy nhất.

### Nhịp 34 · 16:30 · Kiểm tra C4

Hãy thử n bằng bốn. Có bốn cách chọn số cặp ngoặc nằm bên trong cặp đầu tiên: không, một, hai hoặc ba. Số lời giải ở bốn trường hợp lần lượt là năm, hai, hai và năm. Tổng bằng mười bốn, đúng như công thức Catalan ở chương trước. Một điều đáng chú ý là các số hạng xuất hiện đối xứng, tương ứng đổi vai trò hai phần A và B. Tuy nhiên không phải lúc nào cũng được chia đôi vì A và B có vai trò phân biệt.

**Trên màn hình:** C4=C0C3+C1C2+C2C1+C3C0 | Các số là 5, 2, 2, 5 | Tổng bằng 14
**Ghi nhớ:** Truy hồi tái tạo đúng công thức tường minh.

### Nhịp 35 · 17:00 · Hàm sinh của Catalan

Từ tập 21, chúng ta đã biết cách đưa một dãy số vào hàm sinh. Đặt F của x bằng tổng các số Catalan nhân x mũ n. Dãy rỗng đóng góp một; dãy không rỗng có dạng cặp ngoặc ngoài, một dãy bên trong và một dãy phía sau. Hai dãy con cho tích F bình phương, còn cặp ngoặc ngoài làm tăng kích thước một nên thêm nhân tử x. Chúng ta thu được phương trình hàm sinh F bằng một cộng x F bình phương.

**Trên màn hình:** F(x)=Σ C_n x^n | Phân rã (A)B cho F=1+xF² | Giải nhánh phù hợp F(0)=1
**Ghi nhớ:** Hàm sinh mã hóa toàn bộ truy hồi.

### Nhịp 36 · 17:30 · Cầu nối sang quy hoạch động

Nếu chỉ dùng truy hồi đệ quy một cách ngây thơ, chương trình sẽ tính lại vô số kết quả giống nhau. Quy hoạch động lưu bảng C không đến C n rồi tính theo thứ tự tăng dần. Cách làm ấy được giới thiệu ở tập 22 với các mô hình đường đi và chuỗi nhị phân. Bây giờ ta thấy Catalan vừa có công thức đóng nhờ phản xạ, vừa có truy hồi nhờ phân rã, vừa có hàm sinh. Mỗi cách nhìn làm sáng tỏ một phần khác nhau của cấu trúc.

**Trên màn hình:** Truy hồi tính C_n từ các C nhỏ | Bảng giá trị tránh lặp tính toán | Công thức tường minh dùng để kiểm chứng
**Ghi nhớ:** Một bài toán có nhiều cách giải bổ trợ nhau.


## 07 · BÀI TOÁN LÁ PHIẾU NÂNG CAO

### Nhịp 37 · 18:00 · Bài toán lá phiếu

Giả sử ứng viên A nhận năm phiếu, ứng viên B nhận ba phiếu. Các lá phiếu có cùng tên ứng viên không phân biệt nhau, còn thứ tự công bố là điều cần đếm. Nếu A luôn không ít phiếu hơn B trong mọi thời điểm, hiệu A trừ B là một đường đi không âm. Nếu yêu cầu A luôn nhiều hơn B ngay sau từng phiếu, đường đi phải dương nghiêm ngặt. Hai điều kiện chỉ khác một dấu bằng nhưng có số kết quả khác nhau.

**Trên màn hình:** A nhận p phiếu, B nhận q phiếu | Các lá phiếu được công bố lần lượt | Theo dõi độ chênh lệch A−B
**Ghi nhớ:** Bất đẳng thức tiền tố là bài toán đường đi.

### Nhịp 38 · 18:30 · Tất cả thứ tự công bố

Với năm phiếu A và ba phiếu B, số thứ tự công bố chưa có ràng buộc là tổ hợp chập ba của tám, bằng năm mươi sáu. Chúng ta không cần nhân thêm ba giai thừa hay năm giai thừa, vì các lá phiếu cùng tên ứng viên là giống nhau. Đây là một dạng hoán vị lặp đã học ở tập 10, giờ được kết hợp với điều kiện tiền tố để sinh ra một công thức lá phiếu nổi tiếng.

**Trên màn hình:** Tổng tám phiếu | Chọn ba vị trí cho B | Có C_3^8=56 thứ tự
**Ghi nhớ:** Cố định tổng phiếu trước khi áp điều kiện.

### Nhịp 39 · 19:00 · Không thua: cho phép hòa

Trước tiên cho phép hai ứng viên hòa nhau ở một số thời điểm, nghĩa là A luôn không ít hơn B. Khi ấy đường đi không được xuống dưới trục, nhưng được chạm trục. Có năm bước lên và ba bước xuống, điểm cuối ở độ cao hai. Nguyên lý phản xạ cho hiệu giữa tổ hợp chập ba của tám và tổ hợp chập hai của tám. Ta được hai mươi tám cách, đúng một nửa tổng số thứ tự không ràng buộc trong trường hợp cụ thể này.

**Trên màn hình:** A−B luôn lớn hơn hoặc bằng 0 | Đường được phép chạm lại trục | Tính bằng hiệu hai tổ hợp
**Ghi nhớ:** Điều kiện không âm cho 28 kết quả.

### Nhịp 40 · 19:30 · Luôn dẫn trước nghiêm ngặt

Bây giờ tăng yêu cầu: sau mỗi lá phiếu đã công bố, A phải nhiều phiếu hơn B, kể cả những thời điểm giữa chừng. Ta không cho phép đường chạm lại trục sau bước đầu. Định lý lá phiếu nghiêm ngặt cho hệ số p trừ q chia p cộng q, nhân với số thứ tự tổng. Thay p bằng năm, q bằng ba thu được hai phần tám nhân năm mươi sáu, bằng mười bốn cách. Đây là kết quả khác rõ rệt với điều kiện cho phép hòa.

**Trên màn hình:** Sau phiếu đầu A phải dẫn trước | Mọi tiền tố đều có A>B | Không được chạm lại mức 0
**Ghi nhớ:** Chặn chặt hơn còn 14 kết quả.

### Nhịp 41 · 20:00 · Công thức tổng quát

Với p lớn hơn q, điều kiện A luôn dẫn trước nghiêm ngặt có công thức p trừ q chia p cộng q nhân tổ hợp chập q của p cộng q. Nếu chỉ yêu cầu A không thua, kết quả là hiệu của hai tổ hợp liên tiếp, hoặc viết lại bằng một tỷ số khác. Không được dùng nhầm công thức này cho trường hợp bằng phiếu, và khi p bằng q điều kiện dẫn trước nghiêm ngặt đến hết dãy là bất khả thi. Đây là ví dụ điển hình về việc một ràng buộc nhỏ thay đổi toàn bộ phép đếm.

**Trên màn hình:** p≥q cho phép hòa | p>q và dẫn trước nghiêm ngặt | Hai công thức không được tráo
**Ghi nhớ:** Kiểm tra dấu > hay ≥ ở từng tiền tố.

### Nhịp 42 · 20:30 · Tổng quát nhờ phản xạ

Khi quan sát trực tiếp hai lớp đường đi, học sinh sẽ thấy điều kiện không thua tương ứng nằm ở một phía của biên, còn điều kiện dẫn trước nghiêm ngặt không được trở lại biên sau lúc xuất phát. Trong cả hai tình huống, ta đếm những đường vi phạm bằng một phép phản xạ phù hợp. Mục tiêu của chương không phải thuộc hai công thức tách rời mà là nhận ra câu hỏi: đường nào bị cấm, vi phạm lần đầu ở đâu và phản xạ thế nào để tạo một song ánh.

**Trên màn hình:** Đường chạm biên được tính hoặc loại | Mốc phản xạ tùy dấu điều kiện | Biến bài đếm thành hiệu tổ hợp
**Ghi nhớ:** Nguyên lý phản xạ là kỹ thuật chứ không phải mẹo.


## 08 · OLYMPIC: ĐẾM ĐƯỜNG ĐI THEO ĐỈNH

### Nhịp 43 · 21:00 · Đếm theo số đỉnh

Đến đây số Catalan chỉ cho tổng số đường hợp lệ. Nhưng trong nhiều bài toán Olympic, đề bài còn yêu cầu một tham số phụ, chẳng hạn chính xác bao nhiêu lần đường đổi từ bước lên sang bước xuống. Mỗi lần xuất hiện liên tiếp hai bước U rồi D tạo một đỉnh. Hai đường có cùng số cặp bước nhưng số đỉnh khác nhau. Nếu phân loại theo số đỉnh, ta nhận được một tam giác số mới, tinh tế hơn số Catalan thông thường.

**Trên màn hình:** Một đỉnh là cặp bước UD | Không phải mọi Dyck có cùng số đỉnh | Chia đường Dyck thành các lớp rời nhau
**Ghi nhớ:** Các lớp tinh chỉnh của Catalan gọi là Narayana.

### Nhịp 44 · 21:30 · Ba cặp bước

Xét năm đường Dyck có ba bước lên. Một đường đi lên ba bước rồi xuống ba bước có đúng một đỉnh. Những đường chứa hai cặp chuyển U sang D có hai đỉnh. Cuối cùng đường lên xuống luân phiên có ba đỉnh. Khi nhóm lại, ta được một đường có một đỉnh, ba đường có hai đỉnh và một đường có ba đỉnh. Tổng một cộng ba cộng một trả lại năm, tức Catalan bậc ba.

**Trên màn hình:** UUUDDD có 1 đỉnh | UUDUDD có 2 đỉnh | UDUDUD có 3 đỉnh
**Ghi nhớ:** Số đỉnh là thống kê trên đường Dyck.

### Nhịp 45 · 22:00 · Công thức Narayana

Công thức Narayana phát biểu rằng số đường Dyck bậc n có đúng k đỉnh bằng tích tổ hợp chập k của n và tổ hợp chập k trừ một của n, rồi chia cho n. Đây là kết quả nâng cao: việc kiểm chứng bằng cách liệt kê không thay thế một chứng minh tổng quát, nhưng giúp học sinh hiểu ý nghĩa các thừa số. Trong video, ta dùng các nhóm đường nhỏ để kiểm chứng và giới thiệu công thức như một định lý sâu hơn của tổ hợp.

**Trên màn hình:** N(n,k) đếm đường bậc n có k đỉnh | N(n,k)=C_k^n C_(k−1)^n / n | Cộng theo k trả lại Catalan
**Ghi nhớ:** Narayana là dạng tinh chỉnh của Catalan.

### Nhịp 46 · 22:30 · Bài Olympic: n=6, k=3

Bài toán chính yêu cầu đếm các đường đi có sáu bước lên, sáu bước xuống, không bao giờ âm và có đúng ba đỉnh. Nếu chỉ dùng Catalan, ta sẽ tính cả một trăm ba mươi hai đường Dyck bậc sáu, nhưng đề bài đòi hỏi một lớp nhỏ hơn. Công thức Narayana cho phép lọc trực tiếp theo số đỉnh. Trước khi tính, hãy thử quan sát vài đường được tô xanh và vài đường có số đỉnh khác bị làm mờ.

**Trên màn hình:** Có 6 bước U và 6 bước D | Chỉ giữ đường có đúng 3 đỉnh | Dùng N(6,3) để tìm số cách
**Ghi nhớ:** Bài toán có hai ràng buộc độc lập về dạng đường.

### Nhịp 47 · 23:00 · Tính kết quả

Thay n bằng sáu và k bằng ba vào công thức Narayana, ta có tổ hợp chập ba của sáu bằng hai mươi, tổ hợp chập hai của sáu bằng mười lăm. Tích là ba trăm, chia cho sáu được năm mươi. Đây là đáp án của bài cuối tập. Điều cần nhớ không phải con số năm mươi mà là cách chuyển từ việc đếm tất cả Catalan sang đếm theo một đặc trưng phụ được chỉ định rõ.

**Trên màn hình:** C_3^6 = 20 | C_2^6 = 15 | Nhân rồi chia 6
**Ghi nhớ:** Có đúng 50 đường đạt yêu cầu.

### Nhịp 48 · 23:30 · Kiểm chứng và tổng kết

Để kiểm chứng đáp số, chương trình độc lập sinh tất cả đường Dyck bậc sáu rồi đếm số lần xuất hiện mẫu U D. Kết quả của lớp ba đỉnh đúng bằng năm mươi. Nếu cộng số đường thuộc mọi lớp từ một đến sáu đỉnh, ta thu lại một trăm ba mươi hai, bằng Catalan thứ sáu. Cả video đã đi từ ngoặc đúng đến phản xạ, công thức đóng, cây nhị phân, truy hồi, hàm sinh và công thức Narayana. Những góc nhìn đó tạo thành nền tảng cho bài toán tổ hợp Olympic.

**Trên màn hình:** Liệt kê độc lập xác nhận 50 đường | Tổng các lớp đỉnh là C6 =132 | Phản xạ, truy hồi và song ánh liên kết
**Ghi nhớ:** Catalan mở cửa đến nhiều định lý tổ hợp sâu.
