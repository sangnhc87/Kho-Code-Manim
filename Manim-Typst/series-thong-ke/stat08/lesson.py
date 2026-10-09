"""STAT08: grouped mean, grouped mode; data source is the STAT07 table.
Pure Python. No Manim dependency. All results are calculated, not hardcoded.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isclose
from collections import Counter
from stat01.lesson import SCORES
from stat07.lesson import CLASSES, FREQ, ASYM, ASYM_FREQ, PRACTICE, PCLASSES, PFREQ, density


def estimate_mean(intervals, counts):
    if len(intervals) != len(counts) or not counts or sum(counts) <= 0:
        raise ValueError('Invalid grouped frequency table')
    if any(c < 0 or int(c) != c for c in counts):
        raise ValueError('Counts must be nonnegative integers')
    return sum(iv.midpoint * f for iv, f in zip(intervals, counts)) / sum(counts)


def modal_index(counts):
    if not counts or max(counts) <= 0 or counts.count(max(counts)) != 1:
        raise ValueError('The modal class is not unique')
    return counts.index(max(counts))


def interpolate_mode(intervals, counts):
    """Common equal-width grouped mode estimate (not an exact raw-data mode)."""
    if len(intervals) != len(counts) or not counts: raise ValueError('Invalid table')
    widths = [c.width for c in intervals]
    if not all(isclose(w, widths[0]) for w in widths):
        raise ValueError('Unequal class widths: use histogram densities, not this rule')
    i = modal_index(counts)
    fm = counts[i]
    fl = counts[i-1] if i else 0
    fr = counts[i+1] if i+1 < len(counts) else 0
    d1, d2 = fm-fl, fm-fr
    if d1 < 0 or d2 < 0 or d1+d2 <= 0: raise ValueError('Modal interpolation undefined')
    return intervals[i].left + intervals[i].width * d1/(d1+d2)


def density_modal_mode(intervals, counts):
    """Optional extension: linear interpolation of histogram frequency densities."""
    if len(intervals) != len(counts) or not counts: raise ValueError('Invalid table')
    ds = list(density(counts, intervals))
    if max(ds) <= 0 or ds.count(max(ds)) != 1: raise ValueError('No unique density modal class')
    i = ds.index(max(ds))
    left = ds[i-1] if i else 0
    right = ds[i+1] if i+1 < len(ds) else 0
    d1, d2 = ds[i]-left, ds[i]-right
    if d1+d2 <= 0: raise ValueError('Undefined interpolation')
    return intervals[i].left + intervals[i].width*d1/(d1+d2)

EXACT_MEAN=sum(SCORES)/len(SCORES)
EXACT_MODE=Counter(SCORES).most_common(1)[0][0]
GROUPED_MEAN=estimate_mean(CLASSES,FREQ)
GROUPED_MODE=interpolate_mode(CLASSES,FREQ)
ASYM_MEAN=estimate_mean(ASYM,ASYM_FREQ)
ASYM_MODE=density_modal_mode(ASYM,ASYM_FREQ)
PRACTICE_MEAN=estimate_mean(PCLASSES, PFREQ)
PRACTICE_MODE=interpolate_mode(PCLASSES, PFREQ)

CHAPTERS=(
  'TỪ DỮ LIỆU THÔ ĐẾN ĐẠI DIỆN CỦA LỚP',
  'SỐ TRUNG BÌNH CỦA MẪU GHÉP NHÓM',
  'CÁI GIÁ PHẢI TRẢ KHI GHÉP NHÓM',
  'ĐỔI CÁCH CHIA LỚP VÀ SO SÁNH ƯỚC LƯỢNG',
  'LỚP MỐT VÀ CÔNG THỨC NỘI SUY MỐT',
  'HISTOGRAM KHI ĐỘ RỘNG LỚP KHÁC NHAU',
  'BÀI TOÁN NGƯỢC VỚI TẦN SỐ CHƯA BIẾT',
  'TỰ LUYỆN VÀ TỔNG KẾT PHƯƠNG PHÁP',
)

@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=30.0

ROWS=[
 [
 ('Bốn mươi điểm số gốc','Mỗi học sinh là một quan sát, không phải một trung điểm lớp.', 'Trên màn hình là bốn mươi điểm kiểm tra giả lập chúng ta đã dùng từ đầu series. Nếu giữ toàn bộ điểm gốc, ta tính được trung bình chính xác. Nhưng khi bảng chỉ còn bốn khoảng và bốn tần số, những điểm cụ thể trong mỗi khoảng đã không còn được lưu. Vì vậy hôm nay ta sẽ tìm các số đặc trưng mang tính ước lượng của mẫu đã ghép nhóm.'),
 ('Thay từng nhóm bằng một đại diện','Trung điểm lớp: 5, 7, 9, 11.', 'Nhìn lớp từ bốn đến dưới sáu: ta tạm coi sáu quan sát trong lớp đều có giá trị năm, là trung điểm của khoảng. Với ba lớp còn lại, các trung điểm lần lượt là bảy, chín và mười một. Sự thay thế này giúp tính toán nhanh, nhưng không nói rằng mỗi học sinh thật sự đạt đúng trung điểm. Đây là mô hình xấp xỉ, không phải phép biến đổi giữ nguyên dữ liệu.'),
 ('Hai thông tin còn lại','Độ rộng lớp và tần số phải đi cùng nhau.', 'Mỗi cột có một khoảng trên trục số và một số lượng học sinh. Lớp đầu có sáu học sinh, lớp thứ hai mười tám, lớp thứ ba mười bốn và lớp cuối hai. Nếu chỉ dùng trung điểm mà quên tần số, ta đã xem bốn lớp quan trọng ngang nhau dù số học sinh rất khác nhau. Muốn tính trung bình ghép nhóm, phải nhân từng đại diện với số lần xuất hiện tương ứng.'),
 ('Dự đoán trước khi tính','Ước lượng nên nằm quanh các lớp đông nhất.', 'Chưa bấm máy tính, hãy dự đoán trung bình ghép nhóm nằm gần bảy hay gần mười một. Hai lớp giữa chứa ba mươi hai trên bốn mươi học sinh, nên kết quả không thể bị lớp cuối có hai học sinh chi phối như thể bốn lớp ngang nhau. Lát nữa, kết quả sẽ được kiểm chứng bằng một tổng có trọng số, và ta sẽ so với trung bình chính xác từ dữ liệu gốc.'),
 ],
 [
 ('Viết tổng có trọng số','6·5 + 18·7 + 14·9 + 2·11.', 'Ta thay sáu quan sát ở lớp đầu bằng sáu giá trị năm, mười tám quan sát của lớp thứ hai bằng mười tám giá trị bảy, tiếp tục cho lớp thứ ba và thứ tư. Khi cộng, ta thu được ba mươi, một trăm hai mươi sáu, một trăm hai mươi sáu và hai mươi hai. Tổng là ba trăm linh bốn. Đây là tổng điểm theo mô hình trung điểm lớp, chưa phải tổng điểm gốc.'),
 ('Chia cho tổng tần số','Trung bình ghép nhóm xấp xỉ 7,6.', 'Bước cuối cùng là chia tổng ba trăm linh bốn cho bốn mươi quan sát, được bảy phẩy sáu. Học sinh cần chú ý: mẫu số là tổng tần số chứ không phải số lớp. Nếu chia cho bốn, kết quả sẽ vô lý. Ta gắn dấu xấp xỉ vì một số quan sát thật đã bị thay bởi trung điểm lớp. Đây là công thức sẽ dùng trong các bài thống kê ghép nhóm.'),
 ('Rút ra công thức tổng quát','x̄ ≈ (m₁n₁+⋯+mₖnₖ)/n.', 'Giả sử có k lớp, mỗi lớp có trung điểm m và tần số n tương ứng. Ta hình dung mỗi lớp như một bó quan sát đặt ở vị trí trung điểm. Tổng có trọng số chia cho số quan sát sẽ cho trung bình ghép nhóm. Ở các lớp có cùng độ rộng hay khác độ rộng, công thức vẫn sử dụng trung điểm và tần số; không cần đổi sang mật độ tần số để tính số trung bình.'),
 ('Kiểm tra bằng máy và bằng mắt','7,6 nằm trong miền dữ liệu và gần lớp đông.', 'Kết quả bảy phẩy sáu nằm giữa trung điểm nhỏ nhất là năm và trung điểm lớn nhất là mười một, nên ít nhất không vi phạm ràng buộc hiển nhiên. Nó hơi lớn hơn bảy vì lớp từ tám đến dưới mười cũng khá đông. Nếu em tính ra giá trị vượt xa tất cả trung điểm, chắc chắn đã nhầm tổng trọng số hoặc mẫu số. Kiểm tra tính hợp lý quan trọng không kém thao tác bấm máy.'),
 ],
 [
 ('So với trung bình chính xác','Dữ liệu gốc: 7,1; ghép nhóm: 7,6.', 'Đây là điểm cốt lõi của bài học. Với bốn mươi điểm thực tế giả lập, tổng điểm là hai trăm tám mươi bốn, nên trung bình chính xác bằng bảy phẩy một. Còn khi dùng trung điểm lớp, ta được bảy phẩy sáu. Hai kết quả chênh nhau không phải do tính sai, mà do dữ liệu trong lớp đã bị thay thế bằng giá trị đại diện. Ta phải diễn đạt trung thực đây là một ước lượng.'),
 ('Vì sao sai lệch xuất hiện?','Mỗi điểm trong lớp không nhất thiết bằng trung điểm.', 'Trong lớp từ sáu đến dưới tám có tám điểm sáu và mười điểm bảy. Thay tất cả bằng bảy làm tổng điểm tăng so với các giá trị gốc. Tương tự, một lớp từ tám đến dưới mười có cả điểm tám và điểm chín. Trung điểm chín không giữ nguyên tổng thật. Vì vậy không thể kỳ vọng trung bình ghép nhóm luôn bằng trung bình gốc, dù bảng tần số đã đếm đủ bốn mươi học sinh.'),
 ('Một bảng – nhiều dữ liệu gốc','Không thể phục hồi duy nhất trung bình thật.', 'Hãy tưởng tượng trong mỗi khoảng ta chuyển các giá trị về gần đầu trái nhưng vẫn giữ đúng tần số. Sau đó thử chuyển chúng về gần đầu phải. Cả hai bộ dữ liệu đều cho bảng ghép nhóm giống hệt, nhưng tổng và số trung bình gốc lại khác nhau. Nghĩa là từ bảng ghép nhóm ta không đủ thông tin để biết chính xác trung bình ban đầu. Đó là mất mát thông tin, không phải lỗi của biểu đồ.'),
 ('Giữ dữ liệu gốc khi có thể','Ước lượng không thay thế được phép tính chính xác.', 'Nếu đề bài cung cấp toàn bộ số liệu rời rạc, ta nên tính trung bình trực tiếp từ chúng nếu cần độ chính xác. Nếu đề chỉ có bảng ghép nhóm, ta dùng công thức trung điểm và báo kết quả xấp xỉ. Trong các video sau về trung vị và tứ phân vị ghép nhóm, ý tưởng nội suy và giới hạn thông tin cũng sẽ xuất hiện. Phân biệt dữ liệu gốc với bảng tóm tắt là một thói quen thống kê tốt.'),
 ],
 [
 ('Đổi lớp, giữ nguyên người','Cách chia khác cho tần số 6–8–18–8.', 'Bây giờ ta đổi ranh giới các lớp thành từ bốn đến dưới sáu, sáu đến dưới bảy, bảy đến dưới chín, và chín đến dưới mười một. Không một điểm kiểm tra nào bị sửa, nhưng bảng tần số chuyển thành sáu, tám, mười tám, tám. Đây là cùng bốn mươi học sinh dưới một cách nhóm khác. Khi so sánh bảng, luôn kiểm tra ranh giới và độ rộng lớp thay vì chỉ so số đứng trên các cột.'),
 ('Trung điểm và trọng số mới','Trung điểm: 5; 6,5; 8; 10.', 'Cách ghép nhóm mới làm trung điểm lớp thay đổi. Lớp từ sáu đến dưới bảy rộng một, có trung điểm sáu phẩy năm. Lớp từ bảy đến dưới chín rộng hai, trung điểm tám. Bốn đại diện bây giờ là năm, sáu phẩy năm, tám, mười. Ta nhân chúng với các tần số mới rồi chia cho bốn mươi. Cùng dữ liệu gốc nhưng ước lượng sẽ thay đổi.'),
 ('So sánh hai ước lượng','7,60 khác 7,65; trung bình gốc vẫn 7,10.', 'Bảng đầu ước lượng trung bình bảy phẩy sáu. Bảng mới cho bảy phẩy sáu lăm, vì tổng trung điểm có trọng số bằng ba trăm linh sáu. Trong khi đó trung bình gốc vẫn bảy phẩy một, không đổi, bởi ta chưa sửa bất kỳ điểm nào. Do vậy có thể nói cách chia lớp ảnh hưởng tới số trung bình ghép nhóm. Nó không biến phép đo thực tế trở thành một giá trị khác.'),
 ('Không nên kết luận tùy tiện','Lớp hẹp không tự động cho kết quả chính xác hơn.', 'Thông thường các lớp đủ hẹp giúp giữ nhiều chi tiết hơn, nhưng chỉ thay một ranh giới hay thu hẹp một lớp không bảo đảm mọi ước lượng sẽ gần giá trị thật hơn. Cần nhìn toàn bộ bảng và mục đích thống kê. Trong ví dụ này, cả hai trung bình ghép nhóm đều lớn hơn trung bình thật. Điều nên ghi nhớ là công thức đúng với bảng nào thì chỉ phản ánh ước lượng dựa trên bảng ấy.'),
 ],
 [
 ('Lớp có tần số lớn nhất','Lớp mốt là [6;8), tần số 18.', 'Sau trung bình, ta chuyển sang mốt của dữ liệu ghép nhóm. Lớp từ sáu đến dưới tám có mười tám quan sát, nhiều nhất trong bốn lớp rộng bằng nhau, nên gọi là lớp mốt. Không được nói mốt của bảng ghép nhóm bằng mười tám: đó là tần số, không phải giá trị cần ước lượng. Cũng không được khẳng định ngay mốt bằng bảy chỉ vì bảy là trung điểm của lớp.'),
 ('Nhìn sang hai lớp kề','Chênh lệch tần số: 12 và 4.', 'Lớp trước có tần số sáu, lớp mốt mười tám và lớp sau mười bốn. Vì vậy độ vượt của lớp mốt so với bên trái là mười hai, còn so với bên phải là bốn. Nếu vẽ các cột histogram bằng nhau về độ rộng, đỉnh của lớp mốt nằm trong khoảng sáu đến tám. Quy tắc nội suy sẽ đặt vị trí mốt lệch về phía có cột lân cận cao hơn, chứ không mặc định ở chính giữa lớp.'),
 ('Nội suy mốt trong SGK','Mo ≈ L + [d₁/(d₁+d₂)]·h.', 'Với lớp mốt có cận trái L và độ rộng h, ta đặt d một bằng tần số lớp mốt trừ tần số lớp trước; d hai bằng tần số lớp mốt trừ tần số lớp sau. Công thức thường gặp trong bài học số liệu ghép nhóm lấy cận trái cộng tỉ lệ d một trên tổng d một cộng d hai, nhân độ rộng lớp. Công thức này cho một giá trị nội suy, không phải phép khôi phục chính xác mốt của dữ liệu gốc.'),
 ('Tính mốt nội suy','Mo ≈ 6 + 12/16·2 = 7,5.', 'Ở bài này cận trái lớp mốt là sáu, độ rộng hai. Ta có d một bằng mười hai, d hai bằng bốn. Lấy sáu cộng mười hai chia mười sáu rồi nhân hai, được bảy phẩy năm. Hãy so sánh: trung điểm lớp mốt là bảy; mốt nội suy là bảy phẩy năm; còn mốt của dữ liệu gốc là bảy. Ba khái niệm này không được viết như thể chúng hoàn toàn giống nhau.'),
 ],
 [
 ('Độ rộng lớp không đồng đều','Không chọn lớp mốt chỉ từ tần số thô.', 'Trong cách chia lớp mới, tần số sáu, tám, mười tám, tám tưởng như cho biết lớp thứ ba cao nhất. Nhưng lớp thứ hai chỉ rộng một, còn lớp thứ ba rộng hai. Vì vậy so sánh tần số tuyệt đối không phản ánh mật độ quan sát trên một đơn vị độ rộng. Ta cần histogram với chiều cao bằng tần số chia độ rộng lớp, để diện tích cột mới tỉ lệ với số quan sát.'),
 ('Mật độ tần số trên histogram','Mật độ: 3, 8, 9, 4.', 'Bốn mật độ lần lượt là ba, tám, chín và bốn. Lớp có mật độ cao nhất vẫn là từ bảy đến dưới chín trong ví dụ này, nhưng mức chênh so với lớp liền trước giờ chỉ còn một. Khi các lớp không cùng độ rộng, dùng công thức nội suy tần số như trường hợp các cột bằng nhau sẽ thiếu cơ sở. Đây là phần mở rộng để học sinh hiểu biểu đồ, không phải đổi công thức SGK một cách máy móc.'),
 ('Ước lượng theo mật độ','Một nội suy minh họa cho giá trị xấp xỉ 7,33.', 'Nếu dùng phép nội suy tuyến tính dựa trên chiều cao các cột mật độ, lớp từ bảy đến dưới chín có mật độ chín, lớp trước tám và lớp sau bốn. Độ chênh bên trái bằng một, bên phải bằng năm. Ta tạm ước lượng vị trí đỉnh bằng bảy cộng một phần sáu của độ rộng hai, tức xấp xỉ bảy phẩy ba ba. Đây chỉ là phương án mô hình hóa mở rộng, không nên nhầm với quy tắc bắt buộc của sách giáo khoa.'),
 ('Cảnh báo về lớp không đều','Nội suy mô hình phụ thuộc giả thiết và cách nhóm.', 'Mốt ước lượng từ histogram không đồng nghĩa mốt chính xác của dữ liệu gốc. Một dữ liệu có nhiều giá trị lặp có thể có mốt đúng tại một số nguyên, nhưng bảng ghép nhóm không giữ được thông tin đó. Với lớp có độ rộng không đều, muốn giải bài theo chuẩn SGK, trước hết kiểm tra đề có yêu cầu cách nội suy riêng hay không; nếu không, nêu rõ quy tắc mình sử dụng và bản chất xấp xỉ.'),
 ],
 [
 ('Bảng còn một tần số chưa biết','Các lớp lần lượt có 6, x, 14, 2 học sinh.', 'Một bài toán ngược có thể không cho sẵn toàn bộ bảng, mà để trống một tần số. Chẳng hạn bốn khoảng cũ có sáu, x, mười bốn và hai học sinh, tổng số học sinh vẫn bằng bốn mươi. Ta phải xác định x trước khi thay vào công thức trung bình hay nội suy mốt. Không nên thế đại số với một biến chưa có giá trị mà quên kiểm tổng tần số.'),
 ('Dựa vào tổng số quan sát','x = 40 − 6 − 14 − 2 = 18.', 'Lấy bốn mươi trừ sáu trừ mười bốn trừ hai, ta có x bằng mười tám. Hãy kiểm lại: sáu cộng mười tám cộng mười bốn cộng hai đúng bằng bốn mươi. Nếu x ra số âm hoặc không nguyên, bảng tần số đang có điều kiện không phù hợp. Sau khi điền x, lớp mốt và giá trị trung bình được tính như ví dụ ban đầu.'),
 ('Kiểm chứng lại bằng trung bình','Tổng có trọng số 304; ước lượng 7,6.', 'Thay x bằng mười tám, tổng đại diện trở lại ba trăm linh bốn. Chia cho bốn mươi được bảy phẩy sáu; lớp mốt vẫn là từ sáu đến dưới tám và mốt nội suy bảy phẩy năm. Nếu một bài cho trung bình ghép nhóm thay vì tổng tần số, ta có thể lập phương trình từ các trung điểm và tần số, nhưng luôn kiểm kết quả có nguyên và không âm hay không.'),
 ('Mẹo kiểm tra bài toán ngược','Tần số là số đếm nguyên không âm.', 'Trong các bài điền ô còn thiếu, nghiệm đại số có thể thỏa phương trình nhưng không hợp nghĩa thống kê. Một tần số không được là âm, không thể là số lẻ phẩy năm học sinh, và phải tạo ra tổng mẫu đúng. Ta cũng cần xác nhận khoảng lớp giữ nguyên, bởi đổi trung điểm làm phương trình thay đổi. Kiểm tra thực tế trước khi kết luận là thói quen cần thiết của mọi bài toán số liệu.'),
 ],
 [
 ('Tự luyện với 20 số liệu phút','Bảng tần số: 5, 7, 6, 2.', 'Đến phần luyện tập, hãy quan sát một bộ hai mươi thời lượng học tập giả lập, chia vào các lớp từ hai đến dưới bốn, bốn đến dưới sáu, sáu đến dưới tám, và tám đến dưới mười. Tần số tương ứng là năm, bảy, sáu và hai. Em hãy tạm dừng video, tự tính trung bình ghép nhóm, xác định lớp mốt và nội suy mốt trước khi xem lời giải.'),
 ('Tính trung bình của bài luyện','x̄ ≈ (5·3+7·5+6·7+2·9)/20 = 5,5.', 'Trung điểm của bốn lớp là ba, năm, bảy và chín. Nhân với tần số tương ứng, tổng có trọng số là mười lăm cộng ba mươi lăm cộng bốn mươi hai cộng mười tám, bằng một trăm mười. Chia cho hai mươi quan sát được năm phẩy năm phút. Đây là số trung bình của bảng đã ghép, không đồng nghĩa trung bình chính xác của từng thời lượng ghi trong dữ liệu gốc.'),
 ('Nội suy mốt của bài luyện','Lớp mốt [4;6), Mo ≈ 5,33 phút.', 'Tần số lớn nhất là bảy tại lớp từ bốn đến dưới sáu. Lớp trước có năm và lớp sau sáu, vì vậy d một bằng hai, d hai bằng một. Áp dụng công thức nội suy, bốn cộng hai phần ba nhân hai, thu được khoảng năm phẩy ba ba phút. Lưu ý không lấy tần số bảy làm mốt và cũng không lấy luôn trung điểm năm nếu đề yêu cầu công thức nội suy của dữ liệu ghép nhóm.'),
 ('Năm bước kết thúc STAT08','Lớp → trung điểm → trọng số → lớp mốt → nội suy.', 'Chúng ta đã thấy cùng một bảng có thể tạo ra hai loại đại diện khác nhau: trung bình được tính bằng trung điểm có trọng số, còn mốt ước lượng phụ thuộc lớp mốt và hai lớp kề. Khi độ rộng lớp không đều, phải xem lại cách so sánh bằng mật độ. Hãy ghi rõ những giá trị này là xấp xỉ, kiểm tổng tần số và giữ dữ liệu gốc nếu có thể. Video tiếp theo sẽ nghiên cứu trung vị ghép nhóm.'),
 ],
]
BEATS=tuple(Beat(ch+1, i+1, *row) for ch,chapter in enumerate(ROWS) for i,row in enumerate(chapter))

def validate():
    assert len(BEATS)==32 and len(CHAPTERS)==8
    assert len(SCORES)==40 and tuple(FREQ)==(6,18,14,2)
    assert isclose(EXACT_MEAN,7.1) and EXACT_MODE==7
    assert isclose(GROUPED_MEAN,7.6) and isclose(GROUPED_MODE,7.5)
    assert tuple(ASYM_FREQ)==(6,8,18,8)
    assert isclose(ASYM_MEAN,7.65) and isclose(ASYM_MODE,7+1/3)
    assert tuple(PFREQ)==(5,7,6,2)
    assert isclose(PRACTICE_MEAN,5.5) and isclose(PRACTICE_MODE,16/3)
    assert sum(b.duration for b in BEATS)==960
    assert all(len(b.voice.split())>=55 for b in BEATS)
    assert len({b.title for b in BEATS})==32
    return True

if __name__=='__main__':
    print('STAT08_LESSON_OK',validate(),'beats',len(BEATS),'words',sum(len(b.voice.split()) for b in BEATS))
