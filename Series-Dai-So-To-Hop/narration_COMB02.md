# LỜI GIẢNG TIẾNG VIỆT — COMB02: QUY TẮC NHÂN

> Văn bản dành cho giáo viên thu âm hoặc dùng TTS. Đây là kịch bản nội dung, **chưa nhúng giọng nói vào video**. Mốc thời gian phải căn lại sau khi có audio. Không mặc định độ dài Scene Manim bằng mốc lời giảng.

## Phần 1. Một lựa chọn rất quen thuộc

Hằng ngày, khi chọn trang phục, chúng ta thường thực hiện nhiều bước liên tiếp mà không để ý. Giả sử có ba chiếc áo khác nhau, kí hiệu A một, A hai và A ba; cùng với hai chiếc quần khác nhau, kí hiệu Q một và Q hai. Mỗi bộ trang phục cần đúng một chiếc áo và đúng một chiếc quần. Theo em, ta tạo được bao nhiêu bộ trang phục khác nhau? Hãy thử tự đếm trước khi chúng ta tìm cách tính nhanh.

## Phần 2. Quan sát đủ các trường hợp

Ta chọn chiếc áo A một trước. Chiếc áo này có thể đi cùng quần Q một hoặc quần Q hai, tạo ra hai bộ khác nhau. Với áo A hai, ta cũng có hai bộ. Tương tự, áo A ba cũng ghép được với hai chiếc quần. Đếm tất cả các bộ ta được hai cộng hai cộng hai, bằng sáu. Có một cách viết gọn hơn: vì có ba lựa chọn áo, và với mỗi chiếc áo đều có hai lựa chọn quần, ta có ba nhân hai bằng sáu bộ trang phục. Quan trọng là mỗi ô trong bảng chỉ ứng với một kết quả, nên không có bộ nào bị đếm hai lần.

## Phần 3. Sơ đồ cây: quan sát phép nhân xuất hiện

Hãy bắt đầu từ một điểm chung. Bước thứ nhất, chúng ta có ba nhánh ứng với ba chiếc áo. Từ mỗi nhánh áo, lại xuất hiện hai nhánh con ứng với hai chiếc quần. Như vậy cả cây có ba nhóm nhánh, mỗi nhóm gồm hai kết quả cuối cùng. Mỗi lá cây là một bộ trang phục xác định. Vì có ba nhóm và mỗi nhóm đều có hai lá, toàn bộ cây có sáu lá. Sơ đồ cây giúp chúng ta hiểu vì sao phép nhân xuất hiện khi thực hiện những lựa chọn liên tiếp.

## Phần 4. Phát biểu quy tắc nhân

Bây giờ ta tổng quát hóa. Giả sử một công việc gồm hai bước. Bước thứ nhất có m cách thực hiện. Với mỗi kết quả của bước thứ nhất, bước thứ hai có đúng n cách thực hiện. Khi đó số cách hoàn thành cả hai bước là m nhân n. Em hãy chú ý cụm từ **với mỗi kết quả**. Đó là điều kiện quan trọng để dùng ngay phép nhân m nhân n. Nếu số lựa chọn ở bước hai thay đổi theo kết quả bước một, ta cần phân trường hợp, chứ không thể nhân một cách máy móc.

## Phần 5. Mở rộng thêm chiếc mũ

Nếu mỗi bộ trang phục phải có thêm một chiếc mũ và chúng ta có hai chiếc mũ khác nhau thì sao? Bước một, chọn áo: ba cách. Bước hai, chọn quần: hai cách. Bước ba, chọn mũ: hai cách. Với mỗi bộ áo và quần, đều có hai mũ phù hợp để chọn. Theo quy tắc nhân, số cách chọn đủ ba món là ba nhân hai nhân hai, bằng mười hai. Cách lập luận này cũng áp dụng cho công việc gồm nhiều hơn hai bước, miễn là ở mỗi bước ta đếm đúng số lựa chọn tương ứng với những gì đã thực hiện trước đó.

## Phần 6. Một điều kiện làm thay đổi kết quả

Chúng ta trở lại ví dụ ba áo, hai quần, nhưng thêm điều kiện: áo A một không được mặc với quần Q hai. Nếu không có điều kiện, có sáu bộ. Bây giờ, cặp A một và Q hai bị gạch bỏ. Chỉ có một bộ không hợp lệ, nên còn sáu trừ một, bằng năm bộ. Đây là cách đếm bằng cách lấy tất cả trừ trường hợp bị cấm. Điều cần kiểm tra là ta chỉ loại đúng một cặp và không vô tình loại những bộ khác vẫn được phép sử dụng.

## Phần 7. Đếm lại theo từng nhánh

Có một cách khác để kiểm chứng số năm. Nếu chọn áo A một, ta chỉ được chọn quần Q một, tức một cách. Nếu chọn áo A hai, ta có thể chọn một trong hai quần. Nếu chọn áo A ba, cũng có hai cách. Ba trường hợp chọn áo tách biệt nhau, vì thế số bộ là một cộng hai cộng hai, bằng năm. Em thấy không, sau khi xuất hiện điều kiện cấm, số lựa chọn quần phụ thuộc vào chiếc áo đã chọn. Vì vậy, ta không thể tiếp tục khẳng định có ba nhân hai bằng sáu bộ hợp lệ. Ví dụ này giúp chúng ta sử dụng quy tắc nhân một cách chính xác hơn.

## Phần 8. So sánh với quy tắc cộng và luyện tập

Cuối cùng, hãy so sánh hai câu hỏi gần giống nhau. Nếu chỉ được chọn đúng một món, hoặc một áo hoặc một quần, có ba cộng hai bằng năm cách. Nhưng nếu bắt buộc chọn đủ một áo và một quần, có ba nhân hai bằng sáu cách. Quy tắc cộng thường áp dụng khi ta chọn một trong các phương án tách biệt. Quy tắc nhân áp dụng khi phải hoàn thành nhiều bước liên tiếp, với số lựa chọn ở từng bước đã được xác định đúng.

Trước khi kết thúc, em hãy thử bài toán sau: một bữa sáng gồm đúng một món ăn, một đồ uống và một loại trái cây. Có hai món ăn, ba đồ uống và hai loại trái cây để chọn. Có bao nhiêu cách chuẩn bị bữa sáng? Hãy tự tính. Vì có ba bước, với số cách lần lượt là hai, ba và hai, đáp án là hai nhân ba nhân hai bằng mười hai. Hẹn gặp lại ở tập tiếp theo, khi chúng ta sử dụng sơ đồ cây để liệt kê những kết quả có nhiều điều kiện hơn.
