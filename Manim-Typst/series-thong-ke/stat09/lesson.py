"""STAT09: grouped median for high-school statistics. Pure, testable Python.
The grouped median is an interpolation estimate, not the exact raw median.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose, isfinite
from statistics import median
from stat01.lesson import SCORES
from stat07.lesson import CLASSES, FREQ, CUM, ASYM, ASYM_FREQ, PCLASSES, PFREQ, PRACTICE, Interval


def grouped_median(classes, counts):
    """Estimate median using N/2 and linear interpolation in the median class.

    Half-open classes must be consecutive. For an exact cumulative boundary,
    select the next nonempty class; its lower boundary gives the same median.
    """
    if len(classes) != len(counts) or not counts:
        raise ValueError('Intervals and frequencies must have equal nonzero length')
    if any(not isfinite(float(v)) or v < 0 or isinstance(v, bool) or int(v) != v for v in counts):
        raise ValueError('Frequencies must be finite nonnegative integers')
    for a, b in zip(classes, classes[1:]):
        if not isclose(a.right, b.left, rel_tol=0, abs_tol=1e-12):
            raise ValueError('Grouped median requires adjacent, nonoverlapping intervals')
    n = sum(counts)
    if n <= 0:
        raise ValueError('No observations')
    target = n / 2
    before = 0
    for idx, (interval, f) in enumerate(zip(classes, counts)):
        if before + f > target:
            return MedianEstimate(n, target, idx, before, f, interval.left, interval.width,
                                  interval.left + (target-before)*interval.width/f)
        before += f
    raise ValueError('Median class could not be determined')


@dataclass(frozen=True)
class MedianEstimate:
    n: int
    rank: float
    class_index: int
    before: int
    frequency: int
    lower: float
    width: float
    value: float


RAW_MEDIAN = median(SCORES)
MAIN = grouped_median(CLASSES, FREQ)
ALTERNATIVE = grouped_median(ASYM, ASYM_FREQ)
EXERCISE = grouped_median(PCLASSES, PFREQ)
EXERCISE_RAW = median(PRACTICE)
BOUND_CLASSES = (Interval(0, 2),Interval(2, 4),Interval(4, 6),Interval(6, 8))
BOUND_COUNTS = (4,6,7,3)
BOUND = grouped_median(BOUND_CLASSES,BOUND_COUNTS)

CHAPTERS = (
    'TRUNG VỊ GỐC VÀ CÂU HỎI KHI GHÉP NHÓM',
    'TẦN SỐ TÍCH LŨY VÀ VỊ TRÍ TRUNG VỊ',
    'XÁC ĐỊNH ĐÚNG LỚP CHỨA TRUNG VỊ',
    'NỘI SUY TRONG LỚP TRUNG VỊ',
    'ĐƯỜNG TẦN SỐ TÍCH LŨY VÀ MÔ HÌNH DIỆN TÍCH',
    'ĐỔI RANH GIỚI LỚP: ĐỘ NHẠY CỦA ƯỚC LƯỢNG',
    'TRƯỜNG HỢP BIÊN VÀ CÁC LỖI DỄ MẮC',
    'BÀI TẬP TỔNG HỢP VÀ TƯ DUY THỐNG KÊ',
)

@dataclass(frozen=True)
class Beat:
    chapter: int
    step: int
    title: str
    thesis: str
    voice: str
    duration: float = 31.0

ROWS = [
 [
 ('Từ 40 điểm số đã quen','Trung vị chính xác của dữ liệu gốc bằng 7.', 'Trong các video trước, chúng ta theo dõi bốn mươi điểm kiểm tra giả lập của một lớp. Nếu giữ từng điểm và sắp theo thứ tự tăng dần, hai vị trí giữa là vị trí hai mươi và hai mươi mốt. Cả hai đều là điểm bảy, nên trung vị chính xác bằng bảy. Nhưng nếu chỉ nhận được một bảng tần số ghép nhóm, ta không còn biết cụ thể điểm ở hai vị trí ấy là bao nhiêu.'),
 ('Bốn lớp và bốn tần số','Các tần số là 6, 18, 14, 2.', 'Bảng ghép nhóm chia điểm số thành bốn khoảng liên tiếp: từ bốn đến dưới sáu, sáu đến dưới tám, tám đến dưới mười, và mười đến dưới mười hai. Tần số lần lượt là sáu, mười tám, mười bốn và hai. Ta vẫn biết cả lớp có bốn mươi học sinh. Tuy nhiên, trong lớp từ sáu đến dưới tám, từng học sinh đạt sáu hay bảy đã không còn được phân biệt.'),
 ('Vì sao không lấy trung điểm?','Trung điểm 7 không tự động là trung vị ghép nhóm.', 'Một nhầm lẫn phổ biến là nhìn lớp đông nhất hoặc nhìn lớp ở giữa rồi lấy ngay trung điểm của khoảng. Cách đó không dựa trên vị trí tích lũy của một nửa mẫu. Trung vị khác số trung bình và khác mốt: nó gắn với thứ tự của dữ liệu, không dựa vào tổng có trọng số và cũng không chỉ tìm lớp đông nhất. Vì vậy ta cần biết có bao nhiêu quan sát đã xuất hiện trước mỗi lớp.'),
 ('Đặt câu hỏi nghiên cứu','Trung vị gốc và trung vị nội suy có nhất thiết bằng nhau?', 'Hãy dự đoán: từ bảng chỉ có bốn lớp và bốn tần số, liệu ta có tìm lại đúng trung vị bảy hay không? Câu trả lời là không nhất thiết. Ta sẽ dùng giả thiết phân bố đều bên trong lớp chứa trung vị để nội suy một giá trị đại diện. Đây là phép ước lượng theo mô hình. Hãy quan sát từng bước thay vì ghi nhớ ngay công thức; chính các đoạn tần số tích lũy sẽ giải thích phép chia trong công thức.'),
 ],
 [
 ('Bắt đầu tích lũy từ lớp đầu','Tần số tích lũy lần lượt 6, 24, 38, 40.', 'Ta cộng dồn sáu học sinh ở lớp thứ nhất, được sáu. Thêm mười tám học sinh ở lớp thứ hai, tổng tăng lên hai mươi bốn. Cộng tiếp mười bốn được ba mươi tám; thêm hai cuối cùng là bốn mươi. Dãy sáu, hai mươi bốn, ba mươi tám, bốn mươi không giảm vì mỗi bước chỉ cộng một tần số không âm. Đây là cầu nối từ bảng tần số sang trung vị ghép nhóm.'),
 ('Vị trí giữa của 40 quan sát','n chia 2 bằng 20.', 'Với bốn mươi quan sát, hai vị trí giữa là hai mươi và hai mươi mốt khi dữ liệu chưa ghép nhóm. Trong công thức nội suy của bảng ghép nhóm, ta sử dụng mức tích lũy n chia hai, tức hai mươi, để xác định nơi đường tích lũy đạt một nửa tổng mẫu. Hãy ghi rõ ý nghĩa của con số hai mươi: đó là số quan sát tích lũy mục tiêu, không phải điểm số và cũng không phải tần số của một lớp.'),
 ('Sáu chưa đủ, hai mươi bốn vượt qua','6 nhỏ hơn 20; 20 nhỏ hơn 24.', 'Sau lớp thứ nhất, chỉ có sáu quan sát, chưa đạt đến một nửa. Sau lớp thứ hai, đã có hai mươi bốn quan sát, vượt mức hai mươi. Vậy vị trí trung vị nằm bên trong lớp thứ hai. Ta không cần đếm tuần tự tất cả bốn mươi điểm và cũng không cần biết điểm cụ thể của học sinh thứ hai mươi. Chỉ cần so sánh hai mốc tích lũy bao quanh mức hai mươi.'),
 ('Đọc bảng như đường đi qua mốc','Lớp chứa trung vị là lớp thứ hai.', 'Em hãy nhìn một đường ngang ở độ cao hai mươi trên biểu đồ tích lũy. Đường này cắt đoạn tăng từ sáu đến hai mươi bốn, tương ứng lớp từ sáu đến dưới tám. Đây chính là lớp trung vị. Nếu chọn lớp có tần số lớn nhất mà không kiểm tra tích lũy, đôi khi tình cờ đúng, nhưng quy tắc đó không tổng quát. Từ đây ta đã tìm được lớp cần nội suy, chưa tìm được giá trị cuối cùng.'),
 ],
 [
 ('Đánh dấu lớp [6;8)','Cận dưới L bằng 6; độ rộng h bằng 2.', 'Cả lớp trung vị được tô nổi bật trên trục điểm từ sáu đến dưới tám. Ranh giới trái là sáu và ranh giới phải là tám, nên độ rộng lớp bằng hai. Hãy phân biệt rõ độ rộng lớp với tần số mười tám: một đại lượng đo theo điểm số, đại lượng kia là số học sinh. Khi nội suy, ta cần cả hai loại đơn vị, vì phải biến số quan sát tích lũy thành độ dài trong khoảng điểm.'),
 ('Mốc trước lớp trung vị','Có 6 quan sát trước lớp trung vị.', 'Trước khi đi vào lớp từ sáu đến dưới tám, ta đã tích lũy đúng sáu quan sát. Mốc này thường được ký hiệu bằng tần số tích lũy trước lớp trung vị. Không được lấy hai mươi bốn, vì đó là số tích lũy sau khi đi hết lớp đang xét. Nếu nhầm mốc trước và mốc sau, hiệu trong tử số trở nên âm hoặc bằng không sai chỗ, khiến kết quả nội suy không hợp lý.'),
 ('Tần số của lớp trung vị','Lớp [6;8) chứa 18 quan sát.', 'Mười tám là số quan sát nằm trong lớp đang chứa mức tích lũy hai mươi. Ta cần đi thêm từ sáu lên hai mươi, tức mười bốn quan sát tính từ đầu lớp. Do đó mười bốn trên mười tám là tỷ phần của lớp mà mô hình nội suy giả định phải đi qua. Trên hình, phần tô màu bên trong cột trung vị chiếm mười bốn phần mười tám diện tích của lớp, không phải mười bốn phần bốn mươi.'),
 ('Bốn đại lượng, một phép nội suy','L=6; N trước=6; f=18; h=2.', 'Tóm lại, để tính trung vị ghép nhóm ta chỉ cần xác định đúng bốn thông tin từ bảng: cận dưới lớp trung vị, tần số tích lũy trước lớp, tần số riêng của lớp, và độ rộng lớp. Ngoài ra, mức một nửa mẫu là hai mươi. Hãy dừng video và tự chỉ ra năm con số ấy trên hình, trước khi công thức tổng quát xuất hiện. Nếu không xác định được lớp trung vị, chưa nên thế số vào công thức.'),
 ],
 [
 ('Đi qua 14 trong 18 quan sát','Tỷ lệ nội suy là 14/18.', 'Từ mốc tích lũy sáu ở đầu lớp, ta phải đi tới mốc hai mươi. Số quan sát cần vượt qua trong lớp là hai mươi trừ sáu, bằng mười bốn. So với cả lớp có mười tám quan sát, tỷ lệ là mười bốn phần mười tám. Nếu giả sử tần số được trải đều theo chiều ngang của lớp, tỷ lệ số lượng cũng chính là tỷ lệ chiều dài trong khoảng từ sáu đến tám.'),
 ('Biến tỷ lệ thành độ dài','Đoạn cộng thêm bằng 14/18 nhân 2.', 'Lớp trung vị rộng hai điểm. Lấy mười bốn chia mười tám rồi nhân với hai, ta được khoảng một phẩy năm năm sáu điểm. Vạch trung vị đi từ cận trái sáu sang phải đúng độ dài này. Trong hình động, vạch sẽ tiến dần qua lớp khi diện tích tích lũy tăng từ sáu lên hai mươi. Đây là trực giác hình học cho phép nội suy tuyến tính, không phải một phép chia ngẫu nhiên.'),
 ('Hoàn tất tính trung vị','M_e xấp xỉ 7,56.', 'Lấy sáu cộng với mười bốn phần mười tám nhân hai, ta được bảy phẩy năm năm năm lặp, làm tròn khoảng bảy phẩy năm sáu. Giá trị nằm bên trong lớp từ sáu đến tám nên phù hợp với kiểm tra phạm vi. Kết quả khác trung vị chính xác bằng bảy của dữ liệu gốc. Hai giá trị không mâu thuẫn: một bên dùng toàn bộ quan sát, bên kia dùng mô hình nội suy của bảng ghép nhóm.'),
 ('Viết công thức tổng quát','M_e ≈ L + (n/2 − N trước)h/f.', 'Nếu lớp trung vị có cận dưới L, độ rộng h, tần số f, và có N quan sát tích lũy trước lớp, công thức ước lượng là L cộng với n chia hai trừ N, rồi chia cho f và nhân h. Công thức chỉ có ý nghĩa khi chọn đúng lớp chứa mốc n chia hai. Hãy thử thay lại các số của ví dụ và kiểm tra đơn vị: phần cộng thêm phải có đơn vị giống điểm số, không phải số người.'),
 ],
 [
 ('Dựng đường tích lũy','Các điểm tích lũy: (4,0),(6,6),(8,24),(10,38),(12,40).', 'Bây giờ ta không nhìn bốn cột riêng lẻ nữa, mà nối các điểm tần số tích lũy theo ranh giới trên của từng lớp. Khởi đầu tại bốn với tần số tích lũy bằng không, rồi đến sáu, hai mươi bốn, ba mươi tám và bốn mươi khi trục ngang lần lượt là sáu, tám, mười và mười hai. Đường gấp khúc giúp ta thấy cả vị trí và tốc độ tăng trong mỗi khoảng.'),
 ('Đường ngang tại n/2','Mức 20 cắt đoạn nối (6,6) với (8,24).', 'Ta kẻ đường ngang qua độ cao hai mươi. Nó cắt đúng đoạn tăng từ mốc sáu quan sát ở điểm sáu đến mốc hai mươi bốn quan sát ở điểm tám. Không có đoạn nào khác chứa độ cao hai mươi. Điều đó diễn đạt lại phép tìm lớp trung vị bằng ngôn ngữ hình học: trước mốc này tích lũy còn thiếu, sau mốc này đã vượt qua một nửa tổng số học sinh.'),
 ('Hạ đường vuông góc xuống trục','Hoành độ giao điểm là khoảng 7,56.', 'Từ giao điểm của đường ngang mức hai mươi với đường tích lũy, hãy hạ xuống trục điểm. Hoành độ đọc được xấp xỉ bảy phẩy năm sáu. Đây cũng là kết quả của phép nội suy mười bốn phần mười tám trên đoạn dài hai. Quan sát đường thẳng và công thức đại số đưa về cùng một kết quả vì ta đều dùng giả thiết biến thiên tuyến tính bên trong lớp.'),
 ('Hiểu đúng giả thiết hình học','Đoạn thẳng là một mô hình xấp xỉ.', 'Đồ thị tích lũy dạng đoạn thẳng giữa hai biên lớp không có nghĩa dữ liệu gốc phân bố đều thật sự. Nếu học sinh trong lớp từ sáu đến tám chủ yếu đạt bảy, đồ thị tích lũy chính xác từ điểm rời rạc sẽ có những bậc nhảy. Việc nối thẳng chỉ dùng để ước lượng khi bảng ghép nhóm đã che khuất các giá trị riêng. Vì vậy phải dùng ký hiệu xấp xỉ và diễn đạt kết quả có điều kiện mô hình.'),
 ],
 [
 ('Thay ranh giới, giữ nguyên dữ liệu','Bảng mới: 6, 8, 18, 8; tổng vẫn 40.', 'Ta làm thí nghiệm mà không thay đổi một điểm kiểm tra nào, chỉ dời ranh giới chia lớp. Bốn khoảng mới lần lượt là từ bốn đến dưới sáu, sáu đến dưới bảy, bảy đến dưới chín, và chín đến dưới mười một. Tần số chuyển thành sáu, tám, mười tám và tám. Tổng vẫn là bốn mươi. Sự thay đổi này giúp ta kiểm tra một vấn đề quan trọng: trung vị nội suy có phụ thuộc cách ghép nhóm hay không.'),
 ('Lớp trung vị mới','Các tích lũy mới: 6, 14, 32, 40.', 'Với cách ghép nhóm mới, tần số tích lũy lần lượt là sáu, mười bốn, ba mươi hai và bốn mươi. Mức một nửa mẫu bằng hai mươi nằm giữa mười bốn và ba mươi hai, nên lớp trung vị mới là từ bảy đến dưới chín. Mốc trước lớp bằng mười bốn, tần số lớp bằng mười tám, cận dưới bảy và độ rộng hai. Hãy đặt cạnh lớp trung vị của bảng cũ để thấy chúng không giống nhau.'),
 ('Nội suy lại với bảng mới','M_e mới ≈ 7,67.', 'Dùng công thức: bảy cộng hai mươi trừ mười bốn, chia mười tám rồi nhân hai. Phần cộng thêm bằng hai phần ba, cho kết quả gần bảy phẩy sáu bảy. Trong khi đó bảng cũ cho gần bảy phẩy năm sáu. Cả hai đều là ước lượng từ những bảng khác nhau, và đều khác trung vị gốc bằng bảy. Không thể nói trung vị thật đã thay đổi, bởi dữ liệu từng học sinh vẫn giữ nguyên.'),
 ('Bài học về sai số do ghép nhóm','Ước lượng phụ thuộc cách chia lớp.', 'Thí nghiệm này dạy chúng ta không quá tin vào số chữ số thập phân của giá trị nội suy. Đề có bảng nào, ta phải dùng đúng bảng ấy và ghi chú phương pháp xấp xỉ. Nếu có dữ liệu gốc, trung vị trực tiếp đáng tin hơn. Khi cần so sánh hai lớp học, nên cân nhắc giữ cùng cách chia nhóm để biểu đồ và các số đại diện không trở nên khó so sánh hoặc vô tình gây hiểu sai.'),
 ],
 [
 ('Mức n/2 rơi đúng ranh giới','Ví dụ tích lũy đạt đúng 10 ở cuối lớp [2;4).', 'Không phải bài nào mức n chia hai cũng nằm bên trong một lớp. Xét hai mươi quan sát có bốn lớp với tần số bốn, sáu, bảy và ba. Hai lớp đầu tích lũy đúng mười, tức một nửa mẫu. Theo mô hình nội suy, ranh giới chung ở điểm bốn là vị trí trung vị ước lượng. Nếu chọn lớp bên trái, ta nội suy đến cuối lớp; nếu chọn lớp bên phải, ta bắt đầu ngay tại đầu lớp, đều ra bốn.'),
 ('Không nhầm tần số với tích lũy','20 thuộc đoạn tích lũy 6→24, không phải f=20.', 'Trong ví dụ chính, n chia hai bằng hai mươi, nhưng không có lớp nào mang tần số hai mươi. Lớp trung vị có tần số mười tám, còn hai mươi là mức tích lũy mục tiêu. Nếu lấy hai mươi làm mẫu số trong công thức, hoặc lấy hai mươi bốn làm tích lũy trước lớp, kết quả dễ nằm ngoài khoảng. Hãy lần lượt viết riêng n, tần số lớp và tần số tích lũy trước lớp, tránh dùng ký hiệu giống nhau.'),
 ('Lớp rộng không đều vẫn dùng nội suy','Độ rộng h phải lấy riêng của lớp trung vị.', 'Nếu các lớp có độ rộng khác nhau nhưng khoảng vẫn liên tiếp và tần số được đếm đúng, công thức trung vị ghép nhóm vẫn nội suy bằng độ rộng của lớp chứa trung vị. Không lấy độ rộng của lớp đầu và cũng không thay tần số bằng chiều cao cột histogram. Trường hợp các lớp khác độ rộng sẽ được trình bày rõ bằng một trục có các đoạn dài ngắn khác nhau, để học sinh nhìn thấy phần nhân h xuất phát từ đâu.'),
 ('Ba phép kiểm trước kết luận','Đúng lớp, đúng tích lũy trước lớp, kết quả nằm trong lớp.', 'Trước khi chốt đáp án, em hãy thực hiện ba phép kiểm. Đầu tiên lớp được chọn thực sự bao quanh mức n chia hai. Thứ hai tần số tích lũy trong tử số là tổng trước lớp, không phải sau lớp. Cuối cùng giá trị ước lượng phải nằm trong khoảng của lớp trung vị. Nếu không thỏa, cần tính lại trước khi kết luận. Cũng phải cảnh giác với bảng có tổng tần số bằng không hoặc lớp chồng lấn.'),
 ],
 [
 ('Bài tập: 20 thời lượng học tập','Bảng tần số là 5, 7, 6, 2.', 'Hãy tự tính trung vị ghép nhóm của bộ hai mươi thời lượng học tập trong video trước. Bốn lớp là từ hai đến dưới bốn, bốn đến dưới sáu, sáu đến dưới tám, và tám đến dưới mười. Các tần số tương ứng năm, bảy, sáu và hai. Em có thể tạm dừng video: tìm n chia hai, viết dãy tần số tích lũy rồi xác định lớp trung vị. Đừng vội dùng số trung bình năm phẩy năm đã tính ở tập trước.'),
 ('Tìm lớp trung vị của bài luyện','Tích lũy: 5,12,18,20; lớp [4;6).', 'Với hai mươi quan sát, mốc một nửa mẫu là mười. Tần số tích lũy đi qua các mức năm, mười hai, mười tám, hai mươi. Vì năm nhỏ hơn mười và mười nhỏ hơn mười hai, lớp chứa trung vị là từ bốn đến dưới sáu. Ta có cận trái bốn, độ rộng hai, tần số lớp bảy, và tần số tích lũy trước lớp bằng năm. Tất cả dữ kiện đều đọc trực tiếp từ bảng.'),
 ('Nội suy và kiểm chứng','M_e ≈ 5,43; trung vị dữ liệu gốc = 5.', 'Thay vào công thức, ta có bốn cộng mười trừ năm chia bảy rồi nhân hai, bằng năm phẩy bốn hai tám, gần năm phẩy bốn ba. Trung vị chính xác từ hai mươi thời lượng ban đầu bằng năm. Sự khác biệt nhắc lại rằng nội suy dùng giả thiết phân bố đều trong lớp. Hãy kiểm tra giá trị năm phẩy bốn ba nằm giữa bốn và sáu, đúng lớp đã chọn, rồi ghi rõ đây là kết quả ước lượng.'),
 ('Tự kiểm tra và chuyển sang bài mới','Đúng thứ tự: tích lũy → lớp → bốn đại lượng → nội suy.', 'Kết thúc video, hãy ghi lại một quy trình có thể áp dụng cho bất kỳ bảng ghép nhóm phù hợp nào: kiểm tổng tần số, tìm mốc n chia hai, xác định lớp chứa trung vị, đọc cận trái và độ rộng, lấy tần số tích lũy trước lớp cùng tần số của lớp, rồi nội suy. Nếu còn dữ liệu gốc, đối chiếu để hiểu độ xấp xỉ. Ở tập sau, chúng ta sẽ tiếp tục với các tứ phân vị của mẫu số liệu ghép nhóm.'),
 ],
]

BEATS = tuple(Beat(ch+1, j+1, *entry) for ch, rows in enumerate(ROWS) for j, entry in enumerate(rows))

def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==32
    assert all(len(row)==4 for row in ROWS)
    assert len(set(b.title for b in BEATS))==32
    assert all(len(b.voice.split()) >= 65 for b in BEATS)
    assert sum(b.duration for b in BEATS)==992
    assert isclose(RAW_MEDIAN,7)
    assert tuple(CUM)==(6,24,38,40)
    assert (MAIN.class_index, MAIN.before, MAIN.frequency)==(1,6,18)
    assert isclose(MAIN.value,68/9)
    assert (ALTERNATIVE.class_index, ALTERNATIVE.before, ALTERNATIVE.frequency)==(2,14,18)
    assert isclose(ALTERNATIVE.value,23/3)
    assert isclose(EXERCISE.value,38/7)
    assert EXERCISE_RAW==5
    assert isclose(BOUND.value,4)
    return True

if __name__=='__main__':
    print('STAT09_LESSON_OK',validate(),'beats',len(BEATS),'words',sum(len(b.voice.split()) for b in BEATS))
