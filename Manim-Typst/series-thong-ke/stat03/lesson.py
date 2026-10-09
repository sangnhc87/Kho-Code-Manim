"""STAT03: mean, median, mode. Pure-Python statistical source of truth.
Synthetic data only. No Manim dependency. Vietnamese narration keyed to 32 beats.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from statistics import mean, median, multimode
from stat01.lesson import SCORES, FREQUENCY

N = len(SCORES)
SORTED = tuple(sorted(SCORES))
SUM = sum(SCORES)
MEAN = mean(SCORES)
MEDIAN = median(SCORES)
MODES = tuple(multimode(SCORES))
BASE = (5, 6, 6, 7, 7, 7, 8, 8, 9)  # independent: minutes of practice
CHANGED = BASE[:-1] + (27,)
TRIMMED_EXAMPLE = (1, 1, 2, 3, 4, 9)
TRANSFORMED = tuple(x+2 for x in SCORES)
WEIGHTED_SUM = sum(value * count for value, count in FREQUENCY.items())

CHAPTERS = (
    'BA CON SỐ KỂ BA CÂU CHUYỆN',
    'SỐ TRUNG BÌNH – ĐIỂM CÂN BẰNG',
    'TRUNG VỊ – GIÁ TRỊ Ở GIỮA',
    'MỐT – GIÁ TRỊ PHỔ BIẾN NHẤT',
    'NGOẠI LỆ KÉO TRUNG BÌNH',
    'CHỌN CHỈ SỐ THEO CÂU HỎI',
    'KHI TOÀN BỘ DỮ LIỆU THAY ĐỔI',
    'BÀI TOÁN NGƯỢC VÀ TỔNG KẾT',
)

@dataclass(frozen=True)
class Beat:
    chapter: int
    step: int
    title: str
    thesis: str
    voice: str
    duration: float = 25.0

# Narrative pacing: explain -> invite prediction -> animate -> check.
ROWS = [
 [
  ('Một bộ số, ba câu hỏi','40 điểm chỉ là điểm khởi đầu.',
   'Chúng ta tiếp tục với bốn mươi điểm kiểm tra giả lập của hai tập trước. Nhìn các điểm từ bốn đến mười, em thử trả lời ba câu hỏi khác nhau: điểm chung của lớp khoảng bao nhiêu, điểm nằm giữa danh sách là mấy, và điểm nào xuất hiện thường xuyên nhất? Ba câu hỏi ấy sẽ dẫn đến ba số đặc trưng.'),
  ('Đếm đúng trước khi tính','40 quan sát; tổng các điểm bằng 284.',
   'Ta giữ nguyên danh sách điểm đã thu thập. Bảng tần số cho thấy điểm bảy xuất hiện mười lần, còn điểm bốn và mười mỗi điểm hai lần. Điều đầu tiên phải kiểm tra là tổng số quan sát bằng bốn mươi. Khi cộng toàn bộ điểm, ta được hai trăm tám mươi bốn. Hai con số này sẽ phục vụ phép tính trung bình.'),
  ('Ba cách kể về trung tâm','Trung bình, trung vị, mốt trả lời khác nhau.',
   'Một số duy nhất không thể kể hết câu chuyện về dữ liệu. Số trung bình dùng tất cả giá trị và cân bằng tổng. Trung vị dựa vào vị trí chính giữa sau khi sắp xếp. Mốt dựa vào số lần xuất hiện. Trong ví dụ này chúng gần nhau, nhưng điều đó không có nghĩa ba khái niệm luôn giống nhau.'),
  ('Dữ liệu minh họa, không phải điểm thật','Cần hiểu ngữ cảnh trước khi kết luận.',
   'Đây là các điểm được tạo riêng để dạy học, không phải dữ liệu cá nhân của học sinh. Khi tính số đặc trưng từ số liệu thực, hãy kiểm tra nguồn, đơn vị và cỡ mẫu. Một giá trị trung bình cao không tự động chứng minh mọi học sinh đều đạt kết quả cao. Ta phải hiểu ý nghĩa của từng chỉ số.'),
 ],
 [
  ('Trung bình như chia đều','Chia tổng 284 cho 40 quan sát.',
   'Giả sử có thể gom toàn bộ điểm thành một tổng rồi chia đều cho bốn mươi học sinh. Mỗi người sẽ nhận cùng một giá trị bằng tổng chia cho số quan sát. Đó chính là cách hiểu trực quan của số trung bình cộng. Trên màn hình, các cột điểm đóng góp vào tổng nhưng không cần có cùng chiều cao.'),
  ('Đếm bằng bảng tần số','Tính 4×2 + 5×4 + … + 10×2.',
   'Nếu một điểm xuất hiện nhiều lần, ta không cần cộng đi cộng lại từng giá trị. Ta lấy mỗi giá trị nhân với tần số tương ứng, rồi cộng các tích. Với điểm bảy, đóng góp là bảy nhân mười bằng bảy mươi. Lưu ý tần số là trọng số, không phải một số cộng thêm vào giá trị điểm.'),
  ('Tính ra 7,1','Số trung bình có thể không thuộc dữ liệu gốc.',
   'Tổng có trọng số là hai trăm tám mươi bốn và tổng tần số là bốn mươi. Do đó số trung bình bằng bảy phẩy một. Không học sinh nào nhất thiết phải có đúng điểm bảy phẩy một. Trung bình là đại lượng đại diện cho dữ liệu, chứ không bắt buộc là một quan sát thực sự xuất hiện.'),
  ('Tính chất điểm cân bằng','Các độ lệch có dấu cộng lại bằng 0.',
   'Tưởng tượng mỗi điểm tạo ra một lực kéo trên trục số. Những điểm nhỏ hơn bảy phẩy một nằm phía trái, những điểm lớn hơn nằm phía phải. Tại vị trí trung bình, tổng các độ lệch có dấu bằng không. Đó là lý do số trung bình còn được gọi là điểm cân bằng của phân bố.'),
 ],
 [
  ('Sắp xếp rồi tìm giữa','Trung vị dựa trên thứ tự, không dựa tổng.',
   'Để tìm trung vị, bước đầu tiên là sắp xếp dữ liệu không giảm. Việc đổi vị trí không thay đổi những giá trị đã quan sát. Bây giờ ta không cộng tất cả điểm mà chỉ nhìn vào vị trí chính giữa. Chính cách xác định bằng vị trí khiến trung vị có tính chất khác số trung bình.'),
  ('Bốn mươi là số chẵn','Hai vị trí giữa là 20 và 21.',
   'Với bốn mươi giá trị đã sắp xếp, không có một vị trí duy nhất ở giữa. Hai vị trí trung tâm là vị trí thứ hai mươi và hai mươi mốt. Ta lấy trung bình cộng của hai giá trị tại hai vị trí ấy. Cần phân biệt chỉ số vị trí với giá trị điểm ghi trên thẻ.'),
  ('Trung vị của lớp bằng 7','Vị trí 20 và 21 đều nhận điểm 7.',
   'Quan sát hai thẻ chính giữa, cả hai đều mang giá trị bảy. Bởi vậy trung vị của lớp bằng bảy. Em có thể kiểm tra nhanh bằng tần số tích lũy: đến điểm sáu có mười bốn quan sát, đến điểm bảy đã có hai mươi bốn. Hai vị trí giữa chắc chắn thuộc nhóm điểm bảy.'),
  ('Khi số quan sát là lẻ','Dữ liệu 9 giá trị: lấy giá trị thứ 5.',
   'Nếu chỉ có chín giá trị, sau khi sắp xếp, trung vị là giá trị tại vị trí thứ năm. Với bộ thời gian luyện tập giả lập gồm năm, sáu, sáu, bảy, bảy, bảy, tám, tám, chín phút, giá trị thứ năm bằng bảy. Vậy trung vị bằng bảy mà không cần tính tổng toàn bộ chín số.'),
 ],
 [
  ('Tìm mốt bằng tần số','Điểm có tần số lớn nhất là mốt.',
   'Mốt là giá trị xuất hiện nhiều lần nhất. Ta nhìn biểu đồ tần số của bốn mươi điểm, cột điểm bảy cao nhất với mười quan sát. Vì không có cột nào cao bằng nó nên bảy là mốt duy nhất của bộ dữ liệu. Định nghĩa mốt dựa trên tần số, không dựa trên giá trị lớn nhất.'),
  ('Mốt không phải điểm lớn nhất','Điểm 10 chỉ xuất hiện hai lần.',
   'Một nhầm lẫn phổ biến là cho rằng mốt phải là điểm cao nhất. Nhưng điểm mười chỉ xuất hiện hai lần, trong khi điểm bảy xuất hiện tới mười lần. Mốt phản ánh giá trị phổ biến nhất. Trong nhiều tình huống, đây là thông tin hữu ích nếu ta muốn biết lựa chọn hoặc đặc điểm nào thường gặp.'),
  ('Có thể có nhiều mốt','Hai cột cùng cao nhất tạo hai mốt.',
   'Ta xét một bộ dữ liệu minh họa khác gồm hai, hai, ba, ba, bốn. Số hai và số ba cùng xuất hiện hai lần, nhiều hơn các giá trị khác. Vì vậy bộ dữ liệu có hai mốt. Không phải mẫu số liệu nào cũng có đúng một mốt. Khi các tần số đều bằng nhau, cần nói rõ quy ước nhận diện mốt.'),
  ('Mốt dùng được cho dữ liệu phân loại','Môn học yêu thích cũng có thể có mốt.',
   'Điểm đặc biệt của mốt là có thể dùng với dữ liệu phân loại. Chẳng hạn, nếu môn Toán được nhiều học sinh chọn là yêu thích nhất, Toán là mốt của bảng khảo sát ấy. Không thể lấy trung bình cộng các tên môn học. Do đó, trước khi chọn một số đặc trưng, ta phải biết dữ liệu là số hay là nhóm phân loại.'),
 ],
 [
  ('Chín thời lượng luyện tập','Ban đầu: trung bình 7, trung vị 7, mốt 7.',
   'Chúng ta đổi sang một bộ dữ liệu giả lập độc lập về thời gian luyện tập, tính bằng phút. Chín quan sát lần lượt là năm, sáu, sáu, bảy, bảy, bảy, tám, tám, chín. Tổng bằng sáu mươi ba, trung bình bằng bảy. Giá trị ở giữa là bảy, và bảy cũng xuất hiện nhiều nhất.'),
  ('Một giá trị bị kéo ra xa','Thay 9 phút thành 27 phút.',
   'Bây giờ hãy theo dõi chấm ngoài cùng bên phải. Tôi kéo thời lượng chín phút thành hai mươi bảy phút, còn tám quan sát khác giữ nguyên. Chấm trung bình lập tức dịch sang phải, bởi tổng của dữ liệu tăng thêm mười tám. Hãy dự đoán vị trí trung vị trước khi đọc kết luận ở khung tiếp theo.'),
  ('Trung bình tăng, trung vị đứng yên','Trung bình 9, trung vị 7, mốt 7.',
   'Sau thay đổi, tổng bằng tám mươi mốt và trung bình bằng chín. Nhưng khi sắp xếp, giá trị thứ năm vẫn bằng bảy, nên trung vị không đổi. Tần số lớn nhất vẫn thuộc về bảy, vì vậy mốt cũng không đổi. Cảnh này cho thấy trung bình nhạy với một giá trị lớn bất thường hơn trung vị.'),
  ('Không phải ngoại lệ nào cũng là sai','Kiểm tra bối cảnh trước khi loại bỏ.',
   'Một quan sát khác biệt không nhất thiết là lỗi nhập liệu. Hai mươi bảy phút luyện tập có thể hoàn toàn có thật. Ta chỉ có thể quyết định cách xử lý sau khi biết cách đo, đối tượng và mục tiêu nghiên cứu. Không được tùy tiện xóa giá trị chỉ vì nó làm trung bình thay đổi nhiều.'),
 ],
 [
  ('Ba thước đo, ba mục đích','Trung bình dùng toàn bộ giá trị.',
   'Nếu cần một con số phản ánh mức tổng chung của dữ liệu định lượng, trung bình thường hữu ích. Trong bộ bốn mươi điểm kiểm tra, trung bình bằng bảy phẩy một. Vì dùng tổng của mọi quan sát, trung bình tận dụng nhiều thông tin, nhưng cũng nhạy với các giá trị cực lớn hoặc cực nhỏ.'),
  ('Khi dữ liệu có đuôi dài','Trung vị thường bền vững hơn.',
   'Với bộ thời gian luyện tập vừa kéo một giá trị từ chín lên hai mươi bảy, trung vị vẫn bằng bảy. Trung vị chủ yếu cho biết vị trí trung tâm theo thứ tự. Khi phân bố lệch hoặc có vài quan sát rất khác biệt, trung vị thường phản ánh một thời lượng điển hình phù hợp hơn.'),
  ('Khi hỏi điều gì phổ biến nhất','Mốt mô tả giá trị hay gặp.',
   'Nếu câu hỏi là điểm nào học sinh đạt nhiều nhất, mốt bằng bảy là đáp án trực tiếp. Với dữ liệu phân loại như chọn phương tiện đến trường, mốt có thể dùng được ngay cả khi không thể tính trung bình. Tuy vậy, cần xem có một mốt, nhiều mốt hay các tần số gần nhau.'),
  ('Một số không kể hết phân bố','Luôn xem kèm bảng hoặc biểu đồ.',
   'Hai lớp có thể cùng trung bình bảy nhưng phân bố rất khác nhau. Một lớp tập trung gần bảy, lớp khác gồm cả những điểm thấp và cao. Bởi vậy, số trung bình, trung vị và mốt chỉ tóm tắt một khía cạnh của dữ liệu. Chúng cần được đọc cùng biểu đồ và các số đo độ phân tán.'),
 ],
 [
  ('Cộng cùng một số vào mọi quan sát','Ba số đặc trưng đều tăng theo.',
   'Quay lại bốn mươi điểm kiểm tra minh họa. Hãy tưởng tượng mọi giá trị cùng tăng thêm hai đơn vị, chỉ như một phép biến đổi toán học, không phải một chính sách cộng điểm thực tế. Khi ấy toàn bộ phân bố chuyển sang phải hai đơn vị, không thay đổi thứ tự hay số lần xuất hiện của các giá trị.'),
  ('Trung bình tăng đúng hai','Từ 7,1 thành 9,1.',
   'Nếu mỗi giá trị tăng thêm hai, tổng của bốn mươi quan sát tăng thêm tám mươi. Lấy tổng mới chia cho bốn mươi, trung bình cũng tăng thêm hai, từ bảy phẩy một thành chín phẩy một. Đây là tính chất có thể chứng minh trực tiếp bằng tính chất phân phối của phép cộng và phép chia.'),
  ('Trung vị, mốt cũng tăng hai','Trung vị 9; mốt 9.',
   'Cộng cùng một số giữ nguyên thứ tự giữa các quan sát, vì vậy hai vị trí trung tâm tăng từ bảy lên chín và trung vị mới bằng chín. Các tần số không thay đổi, chỉ nhãn giá trị dịch thêm hai, nên mốt cũng từ bảy thành chín. Cả ba đại lượng thay đổi thống nhất.'),
  ('Nhân dữ liệu với số dương','Trung bình, trung vị, mốt cùng nhân.',
   'Nếu nhân tất cả giá trị với một số dương, thứ tự các quan sát vẫn được bảo toàn. Trung bình và trung vị được nhân với số ấy; các mốt cũng được biến đổi tương ứng. Với phép nhân số âm, thứ tự sẽ đảo ngược nên cần xử lý cẩn thận hơn. Ta sẽ giữ bài này trong phạm vi số nhân dương.'),
 ],
 [
  ('Tìm số còn thiếu từ trung bình','Năm giá trị có trung bình 7.',
   'Bài tự kiểm tra: năm quan sát có trung bình bằng bảy, trong đó đã biết bốn giá trị là năm, sáu, bảy và tám. Em hãy tìm quan sát còn thiếu. Đừng đoán ngay bằng mắt. Hãy nhớ định nghĩa trung bình: tổng tất cả quan sát chia cho số lượng quan sát.'),
  ('Tính tổng cần có','Tổng năm số phải bằng 35.',
   'Vì trung bình bằng bảy và có năm quan sát, tổng phải bằng năm nhân bảy, tức ba mươi lăm. Bốn số đã biết có tổng bằng hai mươi sáu. Ta lấy tổng cần có trừ tổng đã biết. Hãy thử tự tính trước khi hình động mở tấm thẻ cuối cùng.'),
  ('Đáp án là 9','Giá trị còn thiếu bằng 35 − 26 = 9.',
   'Thẻ cuối cùng mở ra số chín. Ta kiểm tra lại: năm cộng sáu cộng bảy cộng tám cộng chín bằng ba mươi lăm; chia năm đúng bằng bảy. Bài toán ngược như vậy thường xuất hiện trong đề kiểm tra. Nhớ rằng trung bình là điều kiện ràng buộc tổng của dữ liệu.'),
  ('Tổng kết ba đại lượng','Hiểu bản chất trước khi nhớ công thức.',
   'Chúng ta đã biết trung bình là điểm cân bằng của tổng, trung vị là vị trí ở giữa sau khi sắp xếp, và mốt là giá trị phổ biến nhất. Với bốn mươi điểm minh họa, ba kết quả lần lượt là bảy phẩy một, bảy và bảy. Hãy chọn đại lượng phù hợp câu hỏi, đồng thời quan sát toàn bộ phân bố.'),
 ]
]
BEATS = tuple(Beat(i+1,j+1,*entry) for i,chapter in enumerate(ROWS)
              for j,entry in enumerate(chapter))

def validate():
    assert len(SCORES)==40 and N==40
    assert SUM==WEIGHTED_SUM==284
    assert MEAN==7.1 and MEDIAN==7 and MODES==(7,)
    assert SORTED[19]==SORTED[20]==7
    assert mean(BASE)==median(BASE)==7 and multimode(BASE)==[7]
    assert mean(CHANGED)==9 and median(CHANGED)==7 and multimode(CHANGED)==[7]
    assert mean(TRANSFORMED)==9.1 and median(TRANSFORMED)==9 and multimode(TRANSFORMED)==[9]
    assert len(CHAPTERS)==8 and len(BEATS)==32
    assert all(b.chapter==i+1 and b.step==j+1 for i in range(8) for j,b in enumerate(BEATS[i*4:i*4+4]))
    assert all(len(b.voice.split())>=42 for b in BEATS)
    assert sum(b.duration for b in BEATS)>=780
    return True

if __name__=='__main__':
    print('STAT03 validation',validate(),'sum',SUM,'mean',MEAN,'median',MEDIAN,'mode',MODES)
