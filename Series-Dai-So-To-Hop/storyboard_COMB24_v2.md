# COMB24 V2 — SỐ CATALAN, ĐƯỜNG ĐI DYCK VÀ NGUYÊN LÝ PHẢN XẠ

**Dạng:** 48 nhịp, 8 chương, bố cục hai cột; nguồn toán và thuyết minh đồng bộ.

**Kiểm chứng:** n từ 0 đến 7; phản xạ là song ánh, kiểm thử ballot và Narayana riêng.

**Ký hiệu:** `C_k^n` có n ở trên, k ở dưới, theo quy ước của người dùng.

## Lộ trình chuyển động và lập luận

### 01. 01 · DÃY NGOẶC ĐÚNG VÀ CATALAN

**Mô hình:** Năm đường đúng đi cùng năm dãy ngoặc; vẽ hình từng đường.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Ngoặc mở, ngoặc đóng — Đúng toàn cục chưa đủ; phải đúng từng tiền tố. | `n=3,quad C_3=5` |
| 2 | Chuyển ngoặc thành độ cao — Dãy ngoặc đúng tương ứng đường đi không âm. | `"(" = U, quad ")" = D` |
| 3 | Năm dãy đúng với ba cặp — Có năm cấu trúc, không phải sáu giai thừa. | `C_3=5` |
| 4 | Từ ba lên bốn cặp — Dãy 1, 1, 2, 5, 14, 42 là Catalan. | `C_0=1, C_1=1, C_2=2, C_3=5` |
| 5 | Vì sao phải giữ ràng buộc? — Cân bằng tổng không bảo đảm cân bằng tiền tố. | `h_t=U_t-D_t` |
| 6 | Vấn đề trung tâm của tập — Catalan bằng tất cả trừ số đường sai. | `C_n=C_n^(2n)-N_("sai")` |

**Mạch lời giảng:**
- **1. Ngoặc mở, ngoặc đóng:** Hãy tưởng tượng chúng ta có ba ngoặc mở và ba ngoặc đóng giống nhau. Nếu chỉ kiểm tra tổng số ngoặc ở cuối, nhiều dãy sai vẫn lọt qua. Một dãy ngoặc đúng đòi hỏi ở mọi vị trí đọc từ trái sang phải, số ngoặc đóng không vượt số ngoặc mở. Điều kiện theo từng tiền tố ấy chính là chiếc cầu nối sang mô hình đường đi, nơi mỗi bước có thể được kiểm tra trực quan.
- **2. Chuyển ngoặc thành độ cao:** Ta đổi mỗi ngoặc mở thành một bước lên và mỗi ngoặc đóng thành một bước xuống. Đọc dãy ngoặc từ trái sang phải sẽ tạo một đường gấp khúc. Chiều cao tại một vị trí bằng số ngoặc mở trừ số ngoặc đóng đã đọc. Dãy đúng khi và chỉ khi đường này bắt đầu ở không, kết thúc ở không và không lần nào đi xuống phía dưới đường cơ sở. Ta đã biến một điều kiện chữ thành một hình có thể quan sát.
- **3. Năm dãy đúng với ba cặp:** Hãy xem năm dãy ngoặc đúng của ba cặp. Mỗi dãy tạo ra một đường đi có dáng khác nhau: có dãy nhấp nhô thấp, có dãy lên cao rồi mới hạ xuống. Tất cả đều giữ cân bằng tiền tố. Khi đổi chỗ các ngoặc giống nhau, chúng ta không tạo ra một kết quả mới. Vì vậy số cấu trúc đúng là năm, một con số nhỏ nhưng mở đầu cho một họ số tổ hợp nổi tiếng.
- **4. Từ ba lên bốn cặp:** Khi tăng số cặp ngoặc, số lời giải không tăng như hai mũ n và cũng không phải n giai thừa. Nếu có không cặp nào, ta quy ước chỉ có một dãy rỗng. Một cặp có một cách, hai cặp có hai cách, ba cặp có năm cách, bốn cặp có mười bốn cách và năm cặp có bốn mươi hai cách. Đây là các số Catalan; nhiệm vụ của chúng ta không phải ghi nhớ mà phải hiểu vì sao chúng xuất hiện.
- **5. Vì sao phải giữ ràng buộc?:** Ví dụ một dãy có tổng số ngoặc mở và đóng bằng nhau nhưng ký tự đầu là ngoặc đóng. Ngay lập tức ta gặp một dấu đóng chưa có dấu mở tương ứng, nên dãy sai. Trên hình, bước đầu tiên nằm dưới trục và được tô đỏ. Hãy quan sát các đoạn bị loại: không thể cứu một tiền tố đã sai chỉ bằng cách thêm ngoặc mở ở phía sau. Đây là điểm mà phép đếm trực tiếp dễ bị nhầm.
- **6. Vấn đề trung tâm của tập:** Nếu quên điều kiện tiền tố, việc đếm rất đơn giản: chọn n vị trí đặt bước lên trong tổng cộng hai n vị trí. Kết quả là tổ hợp chập n của hai n. Nhưng không phải tất cả những lựa chọn đó tương ứng dãy ngoặc đúng. Chúng ta cần hiểu số đường sai và tìm một cách đếm chúng thật khéo. Nguyên lý phản xạ ở chương sau sẽ thực hiện chính xác bước còn thiếu.

### 02. 02 · ĐƯỜNG ĐI DYCK TRÊN LƯỚI

**Mô hình:** Vẽ năm đường Dyck trên lưới với độ cao đo được.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Đường Dyck là gì? — Đường Dyck mã hóa ngoặc đúng. | `U=+1,quad D=-1` |
| 2 | Mở cây lựa chọn — Cắt nhánh sai sớm tránh liệt kê thừa. | `C_3=5` |
| 3 | Cùng một kết quả, hai ngôn ngữ — Đây là một song ánh tự nhiên. | `L=UUDUDD` |
| 4 | Các đường bị loại — Chỉ cần biết lần vi phạm đầu tiên. | `h_t=-1` |
| 5 | Tập tất cả đường cân bằng — Cần loại đúng 15 đường sai. | `C_3^6=20,quad C_3=5` |
| 6 | Hình vuông và đường chéo — Mô hình lưới vuông và ngoặc là tương đương. | `(0,0) -> (n,n)` |

**Mạch lời giảng:**
- **1. Đường Dyck là gì?:** Một đường Dyck là dãy hai n bước, gồm đúng n bước lên và n bước xuống, nhưng không bao giờ có tổng độ cao âm. Khi xem hình, học sinh có thể kéo theo đầu bút từ trái sang phải và quan sát chỉ số độ cao từng bước. Nếu đường chạm trục, nó vẫn hợp lệ; chỉ bước xuống dưới trục mới vi phạm. Quy ước này giúp phân biệt đường Dyck với bài toán lá phiếu nghiêm ngặt sẽ xuất hiện sau.
- **2. Mở cây lựa chọn:** Ta mở một cây lựa chọn từng bước. Ở gốc, nếu đi xuống, chiều cao âm ngay, vì thế nhánh ấy bị loại tức thì. Tại độ cao dương, có thể lên hoặc xuống, miễn là không dùng quá n bước mỗi loại. Mỗi nhánh hoàn chỉnh kết thúc ở độ cao không tương ứng một đường Dyck. Cách dựng từng nhánh này cũng giống quy hoạch động: ta chỉ lưu những trạng thái còn hợp lệ.
- **3. Cùng một kết quả, hai ngôn ngữ:** Một cấu trúc ngoặc như mở mở đóng mở đóng đóng được ánh xạ thành lên lên xuống lên xuống xuống. Ánh xạ có thể đảo lại từng bước nên không mất thông tin. Mỗi dãy ngoặc đúng cho đúng một đường Dyck, và mỗi đường Dyck cho đúng một dãy ngoặc đúng. Trong tổ hợp, một phép ghép tương ứng một-một như vậy gọi là song ánh, rất mạnh vì biến phép đếm của đối tượng khó thành phép đếm của đối tượng dễ.
- **4. Các đường bị loại:** Trong nhóm đường sai, đánh dấu thời điểm đầu tiên chiều cao bằng âm một. Vì đường bắt đầu tại không và thay đổi từng đơn vị, lần đầu xuống âm luôn phải xuống đúng âm một. Trước thời điểm đó đường vẫn ở mức không hoặc dương. Bước đánh dấu tạo điểm mốc rất rõ ràng để dựng một phép biến đổi có thể đảo ngược, thay vì cố đếm hàng loạt hình gấp khúc khác nhau.
- **5. Tập tất cả đường cân bằng:** Với ba bước lên và ba bước xuống, ta chỉ cần chọn vị trí của ba bước lên trong sáu vị trí, có hai mươi dãy. Sơ đồ hiển thị cả năm đường tốt và mười lăm đường sai. Đếm từng đường sai bằng mắt không hiệu quả khi n tăng, nhưng chúng đều có một đặc điểm chung là từng chạm mức âm một. Chúng ta sắp biến đặc điểm đó thành một phép đếm tổ hợp đơn giản.
- **6. Hình vuông và đường chéo:** Một cách vẽ khác đưa mỗi bước lên thành bước dọc và mỗi bước xuống thành bước ngang trên lưới vuông. Đường đi từ góc dưới trái đến điểm n phẩy n phải ở một phía của đường chéo chính. Đây vẫn là cùng một điều kiện tiền tố, chỉ thay đổi hệ tọa độ. Ở các bài toán đường đi có chướng ngại hoặc ranh giới, mô hình lưới đặc biệt hữu ích vì có thể dùng song ánh và nguyên lý phản xạ.

### 03. 03 · NGUYÊN LÝ PHẢN XẠ

**Mô hình:** Biến đường sai UDDUUD thành DUUUUD bằng phản xạ tiền tố đầu tiên chạm -1.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Chọn đường sai bất kỳ — Mốc đầu tiên làm phép biến đổi duy nhất. | `h_t=-1` |
| 2 | Phản xạ đoạn đầu — Mỗi đường sai cho một đường mới xác định. | `U -> D, quad D -> U` |
| 3 | Đếm số bước sau phản xạ — Đường sai biến thành lựa chọn n+1 vị trí U. | `N_("sai")=C_(n+1)^(2n)` |
| 4 | Chứng minh đảo ngược — Phản xạ là song ánh, không mất hay trùng. | `N_("sai") = C_(n+1)^(2n)` |
| 5 | Áp dụng cho n bằng 3 — 20 trừ 15 chỉ còn 5 đường tốt. | `C_3 = 20-15=5` |
| 6 | Dùng lại trong bài lá phiếu — Phản xạ rất mạnh nhưng phải đúng ranh giới. | `C_(n+1)^(2n)` |

**Mạch lời giảng:**
- **1. Chọn đường sai bất kỳ:** Chọn một đường đi sai bất kỳ với n bước lên và n bước xuống. Ta đi dọc từ đầu và đánh dấu lần đầu tiên đường chạm mức âm một. Có thể đường này còn xuống sâu hơn về sau, nhưng không ảnh hưởng. Chỉ đoạn tiền tố đến mốc đầu tiên mới được thay đổi. Đây là điều kiện quan trọng: nếu tự chọn một chỗ phản xạ bất kỳ, chúng ta có thể đếm trùng hoặc không thể đảo phép biến đổi.
- **2. Phản xạ đoạn đầu:** Ta lật tất cả các bước lên thành xuống và các bước xuống thành lên trong đoạn tiền tố được đánh dấu. Vì tiền tố cũ kết thúc ở âm một, sau khi lật nó kết thúc ở dương một. Toàn bộ đường mới không nhất thiết là Dyck, nhưng điều đó không quan trọng: ta đang chuyển đối tượng sai thành một dãy bước có số lượng lên và xuống thay đổi. Phần phía sau mốc được giữ nguyên, giúp dễ truy vết phép biến đổi.
- **3. Đếm số bước sau phản xạ:** Trước phản xạ, tiền tố đi từ không đến âm một nên có đúng một bước xuống nhiều hơn bước lên. Khi đổi loại tất cả bước trong tiền tố, tổng số bước lên của cả dãy tăng một còn số bước xuống giảm một. Như vậy đường mới có n cộng một bước lên và n trừ một bước xuống, trong tổng hai n vị trí. Không còn ràng buộc tiền tố nào phải thỏa khi đếm tập đường mới.
- **4. Chứng minh đảo ngược:** Để khẳng định đây là song ánh, cần biết cách đi ngược. Một dãy gồm n cộng một bước lên và n trừ một bước xuống kết thúc ở độ cao hai, nên chắc chắn có lúc chạm mức dương một. Hãy tìm lần đầu tiên nó chạm dương một và lật lại chính tiền tố đó. Ta thu được đường cân bằng đã từng chạm âm một. Hai phép biến đổi đảo nhau, vì thế không có đường sai nào bị bỏ hoặc bị tính hai lần.
- **5. Áp dụng cho n bằng 3:** Trong trường hợp ba cặp bước, nhóm tất cả có hai mươi đường. Nhóm sai được ghép một-một với các dãy gồm bốn bước lên và hai bước xuống. Có tổ hợp chập bốn của sáu, tức mười lăm dãy như vậy. Lấy hai mươi trừ mười lăm cho kết quả năm. Quan trọng hơn, phép tính này không phụ thuộc vào việc ta đã liệt kê năm đường tốt bằng mắt ở chương đầu; nó là một chứng minh tổng quát có thể áp dụng cho mọi n.
- **6. Dùng lại trong bài lá phiếu:** Nguyên lý phản xạ không chỉ dùng để tính Catalan. Khi một con đường phải luôn nằm một phía của đường biên, ta thường có thể ghép những đường vượt biên với một tập đường dễ đếm bằng cách phản xạ tại lần vi phạm đầu tiên. Tuy nhiên, nếu đề bài yêu cầu nằm phía trên một cách nghiêm ngặt, chạm biên cũng bị cấm; khi đó điểm mốc thay đổi. Học sinh cần đọc đúng dấu bất đẳng thức trước khi áp dụng kỹ thuật này.

### 04. 04 · CHỨNG MINH CÔNG THỨC CATALAN

**Mô hình:** Phân 20 dãy cân bằng thành 5 hợp lệ và 15 bị loại, rút gọn hiệu tổ hợp.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Công thức hiệu hai tổ hợp — Đếm tốt bằng tất cả trừ phản xạ. | `C_n=C_n^(2n)-C_(n+1)^(2n)` |
| 2 | Rút gọn tỷ số — Catalan là tổ hợp chia cho n+1. | `C_n = C_n^(2n)/(n+1)` |
| 3 | Công thức Catalan — Một công thức, nhiều cấu trúc rời rạc. | `C_n=(2n)!/(n!(n+1)!)` |
| 4 | Kiểm tra các trường hợp biên — Không bỏ quên cấu trúc rỗng khi truy hồi. | `C_0=1, C_1=1, C_2=2` |
| 5 | Nhị thức Newton quay trở lại — Tổ hợp, Nhị thức Newton và Catalan kết nối nhau. | `(1+x)^(2n)` |
| 6 | Cảnh báo: không lẫn với số đường tùy ý — Xác định không gian tổng trước khi trừ. | `C_4^8=70,quad C_4=14` |

**Mạch lời giảng:**
- **1. Công thức hiệu hai tổ hợp:** Từ song ánh phản xạ, chúng ta có thể viết số Catalan bằng tổng số đường có n bước lên và n bước xuống trừ số đường sai. Biểu thức là hiệu của hai hệ số tổ hợp liên tiếp, chứ chưa phải công thức dạng phân số nổi tiếng. Hãy dừng ở đây để học sinh tự dự đoán rằng hai số hạng rất gần nhau có thể rút gọn đẹp. Phép biến đổi tiếp theo chỉ là đại số, còn phần quan trọng nhất của chứng minh đã nằm trong song ánh.
- **2. Rút gọn tỷ số:** Xét tỷ số của hai tổ hợp chập n cộng một và chập n cùng bậc hai n. Sau khi rút gọn giai thừa, tỷ số bằng n chia n cộng một. Do đó hiệu của chúng chính là một phần trên n cộng một lần tổ hợp chập n của hai n. Biểu thức rất gọn này có vẻ kỳ lạ vì phép chia luôn cho số nguyên; lời giải bằng phản xạ đã chứng minh tính nguyên ấy theo một ý nghĩa tổ hợp rõ ràng.
- **3. Công thức Catalan:** Viết tổ hợp bằng giai thừa ta được công thức quen thuộc của số Catalan: hai n giai thừa chia cho n giai thừa nhân n cộng một giai thừa. Khi n bằng bốn, kết quả là mười bốn; khi n bằng năm là bốn mươi hai. Công thức này xuất hiện ở rất nhiều bài toán mà thoạt nhìn không hề liên quan đến ngoặc hay đường đi. Ở phần tiếp theo, chúng ta sẽ tìm ra vì sao những đối tượng ấy có chung số lượng.
- **4. Kiểm tra các trường hợp biên:** Những trường hợp nhỏ rất quan trọng khi thiết lập truy hồi. Nếu không có cặp ngoặc nào, ta vẫn có một dãy rỗng hợp lệ. Với một cặp chỉ có duy nhất một dãy, còn hai cặp có hai dãy lồng nhau hoặc đặt cạnh nhau. Nếu tự ý lấy Catalan không bằng không, các công thức nhân và tổng ở chương truy hồi sẽ sai ngay. Trong lập trình kiểm thử cũng vậy, phải cho số hạng đầu tiên giá trị đúng.
- **5. Nhị thức Newton quay trở lại:** Video mười bảy và mười tám đã dạy chúng ta rằng hệ số của x mũ n trong một lũy thừa nhị thức là tổ hợp chập n. Ở đây cùng một hệ số xuất hiện vì cần chọn vị trí của n bước lên. Tuy nhiên điều kiện tiền tố làm phép đếm không còn là nhị thức Newton đơn thuần. Chúng ta phải dùng phản xạ để lọc chính xác phần hợp lệ. Đây là ví dụ đẹp về việc hai kỹ thuật tổ hợp bổ trợ cho nhau.
- **6. Cảnh báo: không lẫn với số đường tùy ý:** Nếu học sinh nói có hai khả năng ở mỗi bước rồi lấy hai mũ tám, đó là số tất cả dãy tám ký tự lên xuống không giới hạn số bước lên và xuống. Nhưng bài Dyck yêu cầu đúng bốn bước lên và bốn bước xuống, nên không gian tổng chỉ có tổ hợp chập bốn của tám, bằng bảy mươi. Sau đó mới áp điều kiện không âm để còn mười bốn. Xác định sai tổng ban đầu là một lỗi phổ biến trong những bài đếm có ràng buộc.

### 05. 05 · SONG ÁNH: CÂY VÀ ĐA GIÁC

**Mô hình:** Vẽ ngũ giác và lục giác thật theo hình học, tam giác hóa không cắt nhau.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Tam giác hóa đa giác — Tam giác hóa (n+2) đỉnh được C_n cách. | `T_5=C_3=5` |
| 2 | Lục giác có 14 cách — Số Catalan đếm cách phân rã đa giác. | `T_6=C_4=14` |
| 3 | Cây nhị phân có thứ tự — Thứ tự của hai cây con không được tráo tùy ý. | `B_3=C_3=5` |
| 4 | Ngoặc hóa phép nhân — Số cách ngoặc hóa n+1 phần tử là C_n. | `B_3=5` |
| 5 | Giải thích cấu trúc chung — Các mô hình cùng chia được theo một lõi cấu trúc. | `C_(n+1)=sum_(i=0)^n C_i C_(n-i)` |
| 6 | Song ánh không phải chỉ trùng đáp số — Để chứng minh bằng song ánh cần tính khả nghịch. | `C_n=D_n=B_n` |

**Mạch lời giảng:**
- **1. Tam giác hóa đa giác:** Hãy xem một ngũ giác lồi. Muốn chia nó thành ba tam giác bằng các đường chéo không cắt nhau, ta phải chọn hai đường chéo thích hợp. Mặc dù bài toán không có dấu ngoặc, số cách là năm, bằng Catalan thứ ba. Trên màn hình, các đường chéo sẽ được vẽ theo từng phương án mà không làm biến dạng đa giác. Chúng ta có thể hỏi vì sao hai đối tượng hình học và đại số lại cho chung số lượng; câu trả lời nằm ở cách chia cấu trúc thành hai phần con.
- **2. Lục giác có 14 cách:** Với một lục giác lồi, có mười bốn cách chia thành bốn tam giác bằng các đường chéo không cắt nhau. Ta không cần liệt kê cùng lúc cả mười bốn hình quá nhỏ; video lần lượt giữ một cạnh gốc và đánh dấu tam giác kề cạnh ấy. Tam giác gốc tách phần còn lại thành hai đa giác độc lập. Mô hình ấy sẽ trở thành một phép nhân số cách ở hai phía, rồi cộng theo mọi vị trí có thể của đỉnh thứ ba.
- **3. Cây nhị phân có thứ tự:** Một cây nhị phân đầy đủ có mỗi nút trong đúng hai nhánh con. Khi các nhánh trái và phải được phân biệt, số hình dạng cây với n nút trong chính là Catalan thứ n. Ví dụ ba nút trong cho năm cấu trúc. Việc đảo cây con trái sang phải thường làm thay đổi cây, vì hai vị trí được gắn vai trò khác nhau. Đây là ví dụ quan trọng cho quy tắc: trước khi chia một phép đếm thành tích, phải nói rõ đối tượng có xét thứ tự hay không.
- **4. Ngoặc hóa phép nhân:** Cho bốn thừa số theo đúng thứ tự a, b, c, d. Nếu ta chỉ được đặt ngoặc để thay đổi trình tự thực hiện phép nhân mà không hoán đổi các thừa số, có năm cách ngoặc hóa đầy đủ. Mỗi cách tương ứng một cây nhị phân: phép nhân cuối cùng là nút gốc, hai nhóm con nằm bên trái và phải. Bằng cách chuyển giữa ngoặc và cây, học sinh thấy rõ song ánh chứ không chỉ ghi nhận một phép trùng số tình cờ.
- **5. Giải thích cấu trúc chung:** Đa giác, cây nhị phân và cách ngoặc hóa đều có một thao tác tách đầu tiên: chọn một tam giác gốc, một nút gốc hoặc phép nhân ngoài cùng. Sau khi chọn, bài toán còn lại phân thành hai phần độc lập. Số cách dựng hai phần cùng lúc là tích hai số Catalan nhỏ hơn; còn số vị trí tách khác nhau được cộng lại. Cấu trúc chung ấy chính là lý do các đối tượng rất khác nhau lại có cùng dãy số.
- **6. Song ánh không phải chỉ trùng đáp số:** Điều quan trọng của phương pháp song ánh là không đủ để tính vài số nhỏ rồi nói hai mô hình giống nhau. Ta cần có quy tắc biến đổi cụ thể từ một cấu trúc sang cấu trúc kia và một quy tắc đảo để khôi phục. Ví dụ đọc một cây theo hành trình quanh các cạnh có thể mã hóa thành chuỗi bước lên xuống. Khi mỗi bước mã hóa được giải thích rõ và có thể đảo, tính tương ứng một-một được chứng minh, nhờ đó số lượng bằng nhau với mọi kích thước.

### 06. 06 · TRUY HỒI VÀ HÀM SINH CATALAN

**Mô hình:** Từ cặp ngoặc ngoài (A)B đến công thức truy hồi; tô sáng C0 tới C5.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Phân tích ngoặc đúng — Tách theo cặp ngoặc khớp đầu tiên. | `S=(A)B` |
| 2 | Nhân các lựa chọn — Hai phần độc lập tạo tích Catalan. | `C_i C_(n-1-i)` |
| 3 | Cộng mọi vị trí tách — Truy hồi Catalan xuất hiện từ phân rã duy nhất. | `C_n=sum_(i=0)^(n-1) C_i C_(n-1-i)` |
| 4 | Kiểm tra C4 — Truy hồi tái tạo đúng công thức tường minh. | `C_4=5+2+2+5=14` |
| 5 | Hàm sinh của Catalan — Hàm sinh mã hóa toàn bộ truy hồi. | `F(x)=1+x F(x)^2` |
| 6 | Cầu nối sang quy hoạch động — Một bài toán có nhiều cách giải bổ trợ nhau. | `C_(n+1)=sum_(i=0)^n C_i C_(n-i)` |

**Mạch lời giảng:**
- **1. Phân tích ngoặc đúng:** Một dãy ngoặc đúng khác rỗng luôn bắt đầu bằng dấu mở. Dấu đóng khớp với nó xác định duy nhất một đoạn bên trong A và đoạn còn lại B ở phía sau. Cả A và B đều là dãy ngoặc đúng; nếu một đoạn rỗng vẫn có đúng một lựa chọn. Nhờ cặp ngoặc khớp đầu tiên, chúng ta nhận được một phép phân rã duy nhất, không trùng lặp. Đây là chìa khóa để xây dựng truy hồi Catalan không cần nhắc đến phản xạ.
- **2. Nhân các lựa chọn:** Giả sử toàn bộ dãy có n cặp ngoặc và bên trong cặp đầu tiên có i cặp. Phần A được chọn theo Catalan thứ i, còn phần B chứa n trừ một trừ i cặp và có Catalan tương ứng. Vì sau khi chọn A, cách chọn B là độc lập, quy tắc nhân cho tích hai số. Hình sẽ chia dãy thành khối trong và khối sau, giúp học sinh thấy tại sao phép nhân xuất hiện và vì sao cần giữ dấu ngoặc khớp.
- **3. Cộng mọi vị trí tách:** Chúng ta chưa biết i bằng bao nhiêu. Nó có thể từ không cho đến n trừ một. Hai trường hợp có số cặp trong A khác nhau thì chắc chắn không trùng một dãy, vì cặp ngoặc khớp đầu tiên sẽ nằm ở vị trí khác nhau. Vì vậy quy tắc cộng cho tổng tất cả các tích vừa tìm được. Đây là truy hồi Catalan và cũng là một phương pháp tính trực tiếp bằng quy hoạch động, sử dụng những kết quả nhỏ để dựng kết quả lớn.
- **4. Kiểm tra C4:** Hãy thử n bằng bốn. Có bốn cách chọn số cặp ngoặc nằm bên trong cặp đầu tiên: không, một, hai hoặc ba. Số lời giải ở bốn trường hợp lần lượt là năm, hai, hai và năm. Tổng bằng mười bốn, đúng như công thức Catalan ở chương trước. Một điều đáng chú ý là các số hạng xuất hiện đối xứng, tương ứng đổi vai trò hai phần A và B. Tuy nhiên không phải lúc nào cũng được chia đôi vì A và B có vai trò phân biệt.
- **5. Hàm sinh của Catalan:** Từ tập 21, chúng ta đã biết cách đưa một dãy số vào hàm sinh. Đặt F của x bằng tổng các số Catalan nhân x mũ n. Dãy rỗng đóng góp một; dãy không rỗng có dạng cặp ngoặc ngoài, một dãy bên trong và một dãy phía sau. Hai dãy con cho tích F bình phương, còn cặp ngoặc ngoài làm tăng kích thước một nên thêm nhân tử x. Chúng ta thu được phương trình hàm sinh F bằng một cộng x F bình phương.
- **6. Cầu nối sang quy hoạch động:** Nếu chỉ dùng truy hồi đệ quy một cách ngây thơ, chương trình sẽ tính lại vô số kết quả giống nhau. Quy hoạch động lưu bảng C không đến C n rồi tính theo thứ tự tăng dần. Cách làm ấy được giới thiệu ở tập 22 với các mô hình đường đi và chuỗi nhị phân. Bây giờ ta thấy Catalan vừa có công thức đóng nhờ phản xạ, vừa có truy hồi nhờ phân rã, vừa có hàm sinh. Mỗi cách nhìn làm sáng tỏ một phần khác nhau của cấu trúc.

### 07. 07 · BÀI TOÁN LÁ PHIẾU NÂNG CAO

**Mô hình:** Chuyển trình tự công bố phiếu thành đường cao độ; so sánh ≥ và >.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Bài toán lá phiếu — Bất đẳng thức tiền tố là bài toán đường đi. | `p=5,quad q=3` |
| 2 | Tất cả thứ tự công bố — Cố định tổng phiếu trước khi áp điều kiện. | `C_3^8=56` |
| 3 | Không thua: cho phép hòa — Điều kiện không âm cho 28 kết quả. | `C_3^8-C_2^8=28` |
| 4 | Luôn dẫn trước nghiêm ngặt — Chặn chặt hơn còn 14 kết quả. | `(5-3)/(5+3) C_3^8=14` |
| 5 | Công thức tổng quát — Kiểm tra dấu > hay ≥ ở từng tiền tố. | `N_("chat")=(p-q)/(p+q) C_q^(p+q)` |
| 6 | Tổng quát nhờ phản xạ — Nguyên lý phản xạ là kỹ thuật chứ không phải mẹo. | `N_("yeu")=C_q^(p+q)-C_(q-1)^(p+q)` |

**Mạch lời giảng:**
- **1. Bài toán lá phiếu:** Giả sử ứng viên A nhận năm phiếu, ứng viên B nhận ba phiếu. Các lá phiếu có cùng tên ứng viên không phân biệt nhau, còn thứ tự công bố là điều cần đếm. Nếu A luôn không ít phiếu hơn B trong mọi thời điểm, hiệu A trừ B là một đường đi không âm. Nếu yêu cầu A luôn nhiều hơn B ngay sau từng phiếu, đường đi phải dương nghiêm ngặt. Hai điều kiện chỉ khác một dấu bằng nhưng có số kết quả khác nhau.
- **2. Tất cả thứ tự công bố:** Với năm phiếu A và ba phiếu B, số thứ tự công bố chưa có ràng buộc là tổ hợp chập ba của tám, bằng năm mươi sáu. Chúng ta không cần nhân thêm ba giai thừa hay năm giai thừa, vì các lá phiếu cùng tên ứng viên là giống nhau. Đây là một dạng hoán vị lặp đã học ở tập 10, giờ được kết hợp với điều kiện tiền tố để sinh ra một công thức lá phiếu nổi tiếng.
- **3. Không thua: cho phép hòa:** Trước tiên cho phép hai ứng viên hòa nhau ở một số thời điểm, nghĩa là A luôn không ít hơn B. Khi ấy đường đi không được xuống dưới trục, nhưng được chạm trục. Có năm bước lên và ba bước xuống, điểm cuối ở độ cao hai. Nguyên lý phản xạ cho hiệu giữa tổ hợp chập ba của tám và tổ hợp chập hai của tám. Ta được hai mươi tám cách, đúng một nửa tổng số thứ tự không ràng buộc trong trường hợp cụ thể này.
- **4. Luôn dẫn trước nghiêm ngặt:** Bây giờ tăng yêu cầu: sau mỗi lá phiếu đã công bố, A phải nhiều phiếu hơn B, kể cả những thời điểm giữa chừng. Ta không cho phép đường chạm lại trục sau bước đầu. Định lý lá phiếu nghiêm ngặt cho hệ số p trừ q chia p cộng q, nhân với số thứ tự tổng. Thay p bằng năm, q bằng ba thu được hai phần tám nhân năm mươi sáu, bằng mười bốn cách. Đây là kết quả khác rõ rệt với điều kiện cho phép hòa.
- **5. Công thức tổng quát:** Với p lớn hơn q, điều kiện A luôn dẫn trước nghiêm ngặt có công thức p trừ q chia p cộng q nhân tổ hợp chập q của p cộng q. Nếu chỉ yêu cầu A không thua, kết quả là hiệu của hai tổ hợp liên tiếp, hoặc viết lại bằng một tỷ số khác. Không được dùng nhầm công thức này cho trường hợp bằng phiếu, và khi p bằng q điều kiện dẫn trước nghiêm ngặt đến hết dãy là bất khả thi. Đây là ví dụ điển hình về việc một ràng buộc nhỏ thay đổi toàn bộ phép đếm.
- **6. Tổng quát nhờ phản xạ:** Khi quan sát trực tiếp hai lớp đường đi, học sinh sẽ thấy điều kiện không thua tương ứng nằm ở một phía của biên, còn điều kiện dẫn trước nghiêm ngặt không được trở lại biên sau lúc xuất phát. Trong cả hai tình huống, ta đếm những đường vi phạm bằng một phép phản xạ phù hợp. Mục tiêu của chương không phải thuộc hai công thức tách rời mà là nhận ra câu hỏi: đường nào bị cấm, vi phạm lần đầu ở đâu và phản xạ thế nào để tạo một song ánh.

### 08. 08 · OLYMPIC: ĐẾM ĐƯỜNG ĐI THEO ĐỈNH

**Mô hình:** Vẽ đường Dyck bậc 6, đánh dấu chính xác mỗi đỉnh UD.

| Nhịp | Nội dung lời giải | Công thức Typst |
|---|---|---|
| 1 | Đếm theo số đỉnh — Các lớp tinh chỉnh của Catalan gọi là Narayana. | `peaks(w)=#(UD)` |
| 2 | Ba cặp bước — Số đỉnh là thống kê trên đường Dyck. | `C_3=1+3+1=5` |
| 3 | Công thức Narayana — Narayana là dạng tinh chỉnh của Catalan. | `N(n,k)=C_k^n C_(k-1)^n/n` |
| 4 | Bài Olympic: n=6, k=3 — Bài toán có hai ràng buộc độc lập về dạng đường. | `N(6,3)=50` |
| 5 | Tính kết quả — Có đúng 50 đường đạt yêu cầu. | `N(6,3)=20*15/6=50` |
| 6 | Kiểm chứng và tổng kết — Catalan mở cửa đến nhiều định lý tổ hợp sâu. | `sum_(k=1)^6 N(6,k)=132` |

**Mạch lời giảng:**
- **1. Đếm theo số đỉnh:** Đến đây số Catalan chỉ cho tổng số đường hợp lệ. Nhưng trong nhiều bài toán Olympic, đề bài còn yêu cầu một tham số phụ, chẳng hạn chính xác bao nhiêu lần đường đổi từ bước lên sang bước xuống. Mỗi lần xuất hiện liên tiếp hai bước U rồi D tạo một đỉnh. Hai đường có cùng số cặp bước nhưng số đỉnh khác nhau. Nếu phân loại theo số đỉnh, ta nhận được một tam giác số mới, tinh tế hơn số Catalan thông thường.
- **2. Ba cặp bước:** Xét năm đường Dyck có ba bước lên. Một đường đi lên ba bước rồi xuống ba bước có đúng một đỉnh. Những đường chứa hai cặp chuyển U sang D có hai đỉnh. Cuối cùng đường lên xuống luân phiên có ba đỉnh. Khi nhóm lại, ta được một đường có một đỉnh, ba đường có hai đỉnh và một đường có ba đỉnh. Tổng một cộng ba cộng một trả lại năm, tức Catalan bậc ba.
- **3. Công thức Narayana:** Công thức Narayana phát biểu rằng số đường Dyck bậc n có đúng k đỉnh bằng tích tổ hợp chập k của n và tổ hợp chập k trừ một của n, rồi chia cho n. Đây là kết quả nâng cao: việc kiểm chứng bằng cách liệt kê không thay thế một chứng minh tổng quát, nhưng giúp học sinh hiểu ý nghĩa các thừa số. Trong video, ta dùng các nhóm đường nhỏ để kiểm chứng và giới thiệu công thức như một định lý sâu hơn của tổ hợp.
- **4. Bài Olympic: n=6, k=3:** Bài toán chính yêu cầu đếm các đường đi có sáu bước lên, sáu bước xuống, không bao giờ âm và có đúng ba đỉnh. Nếu chỉ dùng Catalan, ta sẽ tính cả một trăm ba mươi hai đường Dyck bậc sáu, nhưng đề bài đòi hỏi một lớp nhỏ hơn. Công thức Narayana cho phép lọc trực tiếp theo số đỉnh. Trước khi tính, hãy thử quan sát vài đường được tô xanh và vài đường có số đỉnh khác bị làm mờ.
- **5. Tính kết quả:** Thay n bằng sáu và k bằng ba vào công thức Narayana, ta có tổ hợp chập ba của sáu bằng hai mươi, tổ hợp chập hai của sáu bằng mười lăm. Tích là ba trăm, chia cho sáu được năm mươi. Đây là đáp án của bài cuối tập. Điều cần nhớ không phải con số năm mươi mà là cách chuyển từ việc đếm tất cả Catalan sang đếm theo một đặc trưng phụ được chỉ định rõ.
- **6. Kiểm chứng và tổng kết:** Để kiểm chứng đáp số, chương trình độc lập sinh tất cả đường Dyck bậc sáu rồi đếm số lần xuất hiện mẫu U D. Kết quả của lớp ba đỉnh đúng bằng năm mươi. Nếu cộng số đường thuộc mọi lớp từ một đến sáu đỉnh, ta thu lại một trăm ba mươi hai, bằng Catalan thứ sáu. Cả video đã đi từ ngoặc đúng đến phản xạ, công thức đóng, cây nhị phân, truy hồi, hàm sinh và công thức Narayana. Những góc nhìn đó tạo thành nền tảng cho bài toán tổ hợp Olympic.

## Quy trình nghiệm thu

1. Chạy kiểm thử trên toàn Series: `python -m unittest discover -s tests -v`.
2. Sinh công thức Typst, giọng đọc và phụ đề: `python scripts/prepare_comb24_v2.py --voice off`.
3. GitHub Actions render Scene `COMB24`, kiểm thời lượng và trích tám ảnh chương.
4. Duyệt hình học, tiếng Việt và công thức trước khi phát hành Full HD.

> Các ảnh storyboard là bản mô phỏng; chưa phải kết quả render Manim.