"""STAT18 - Lay mau, thien lech va mo phong. All populations are synthetic."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from math import sqrt
from random import Random

POPULATION = (1,)*400 + (0,)*600
N = len(POPULATION)
TRUE_P = sum(POPULATION)/N
VOLUNTARY_YES, VOLUNTARY_NO = 70,30
PRACTICE_YES, PRACTICE_N = 88,200
PRACTICE_CONVENIENCE_YES = 150


def sample(n:int, seed:int|None=None):
    if not isinstance(n,int) or isinstance(n,bool) or not 1 <= n <= N:
        raise ValueError('Sample size must be integer from 1 to population size')
    return tuple(Random(20261009+n if seed is None else seed).sample(POPULATION,n))


def estimate(values):
    values=tuple(values)
    if not values or any(v not in (0,1) or isinstance(v,bool) for v in values):
        raise ValueError('Expected nonempty binary response data')
    return sum(values)/len(values)


@lru_cache(maxsize=4)
def trials(n:int, count:int=300):
    if not 1<=n<=N or not 1<=count<=3000:raise ValueError('Invalid simulation')
    rng=Random(1800+n)
    return tuple(sum(rng.sample(POPULATION,n))/n for _ in range(count))


def sd_sample_proportion(n:int,p:float=TRUE_P,Npop:int=N):
    """Exact finite-population SD for a simple random sample without replacement."""
    if not (0<p<1 and 1<=n<=Npop):raise ValueError('Invalid parameters')
    return sqrt(p*(1-p)/n*(Npop-n)/(Npop-1))


def approx_interval(successes:int,n:int):
    """Pedagogical Wald interval. Warn about applicability; never a guarantee."""
    if not (isinstance(n,int) and n>0 and isinstance(successes,int) and 0<=successes<=n):
        raise ValueError('Invalid counts')
    p=successes/n
    se=sqrt(p*(1-p)/n)
    return p,max(0.,p-1.96*se),min(1.,p+1.96*se)


def percent(v:float, digits:int=0):
    return f'{v*100:.{digits}f}'.replace('.',',')+'%'


@dataclass(frozen=True)
class Beat:
    chapter:int
    step:int
    title:str
    thesis:str
    voice:str
    duration:float=38.0

CHAPTERS=(
    'TỪ QUẦN THỂ ĐẾN MẪU KHẢO SÁT',
    'CHỌN MẪU NGẪU NHIÊN VÀ THUẬN TIỆN',
    'TỰ NGUYỆN TRẢ LỜI VÀ THIÊN LỆCH',
    'MẪU NGẪU NHIÊN VẪN DAO ĐỘNG',
    'CỠ MẪU VÀ ĐỘ CHÍNH XÁC',
    'ƯỚC LƯỢNG VÀ KHOẢNG BẤT ĐỊNH',
    'MÔ PHỎNG VÀ KIỂM TRA CHẤT LƯỢNG',
    'BÀI TẬP TỔNG KẾT VÀ LỜI KẾT',
)
ROWS=[
[('Khảo sát một câu hỏi đúng', 'Một nghìn học sinh, một câu hỏi về lựa chọn A.',
'Giả sử một trường có một nghìn học sinh. Chúng ta muốn biết tỉ lệ bạn yêu thích phương án A trong một khảo sát giả lập. Điều ta quan tâm là toàn bộ học sinh, chứ không phải riêng các bạn có mặt trước cổng trường. Muốn đưa ra kết luận đáng tin, trước hết phải xác định rõ quần thể được hỏi và câu hỏi cần trả lời.'),
('Quần thể và tham số', 'Trong mô hình: 400 trên 1.000 bạn chọn A, tức 40%.',
'Trong quần thể mô phỏng, bốn trăm trên một nghìn học sinh lựa chọn A. Như vậy tỉ lệ thật là bốn mươi phần trăm. Trong khảo sát đời thực, con số thật thường chưa biết nên ta mới cần lấy mẫu. Ở video này, chúng ta biết trước đáp án của mô hình để kiểm tra xem các cách chọn mẫu có phản ánh được quần thể hay không.'),
('Mẫu và thống kê mẫu', 'Chọn một phần quần thể để ước lượng tỉ lệ chung.',
'Ta không phải lúc nào cũng hỏi được mọi học sinh. Một mẫu là tập hợp những đối tượng được chọn để khảo sát. Từ mẫu, ta tính tỉ lệ các bạn chọn A rồi dùng nó để ước lượng tỉ lệ trong quần thể. Hai khái niệm cần phân biệt là tỉ lệ thật của quần thể và tỉ lệ quan sát được từ mẫu.'),
('Chất lượng hơn số lượng đơn thuần', 'Mẫu phải được chọn phù hợp với quần thể đích.',
'Một mẫu gồm rất nhiều người chưa chắc đã đại diện. Nếu chỉ hỏi thành viên một câu lạc bộ yêu thích phương án A thì kết quả có thể lệch so với cả trường. Vì vậy, câu hỏi đầu tiên không phải lấy bao nhiêu người, mà là chọn ai, từ đâu và bằng cách nào. Đây là tư tưởng xuyên suốt bài học cuối của series.' )],
[('Lấy mẫu ngẫu nhiên đơn', 'Mỗi nhóm gồm n học sinh có cơ hội chọn như nhau.',
'Đối với lấy mẫu ngẫu nhiên đơn không hoàn lại, mọi nhóm gồm cùng một số học sinh có khả năng được chọn như nhau. Ta có thể đánh số toàn bộ một nghìn bạn và dùng bộ sinh số ngẫu nhiên để rút ra danh sách. Cách làm này giảm nguy cơ ưu tiên vô tình cho một nhóm nhất định, nhưng vẫn cần khung danh sách đầy đủ và thu thập câu trả lời đúng.'),
('Một mẫu ngẫu nhiên hai mươi bạn', 'Ví dụ mô phỏng: 7 trên 20 bạn chọn A, được 35%.',
'Máy tính vừa lấy ngẫu nhiên hai mươi học sinh trong quần thể mô phỏng, không lặp lại. Có bảy bạn chọn A nên tỉ lệ mẫu bằng ba mươi lăm phần trăm. Giá trị này không đúng bằng bốn mươi phần trăm của quần thể. Sự sai khác không có nghĩa chọn mẫu sai: đó có thể là dao động ngẫu nhiên hoàn toàn bình thường.'),
('Mẫu ngẫu nhiên tám mươi bạn', 'Ví dụ khác: 37 trên 80 bạn chọn A, được 46,25%.',
'Một lần rút mẫu ngẫu nhiên gồm tám mươi bạn cho kết quả ba mươi bảy bạn chọn A. Tỉ lệ mẫu là bốn mươi sáu phẩy hai lăm phần trăm. Dù kích thước lớn hơn, kết quả lần này lại cách xa mốc bốn mươi phần trăm hơn mẫu hai mươi vừa xem. Cỡ mẫu lớn hơn giúp giảm dao động về lâu dài, nhưng không đảm bảo từng lần rút gần đáp án hơn.'),
('Lấy mẫu thuận tiện khác gì?', 'Hỏi nhóm dễ tiếp cận không phải rút ngẫu nhiên.',
'Khi chỉ hỏi những người đứng gần cổng, hoặc những bạn thuộc lớp đang phụ trách, ta đang chọn mẫu thuận tiện. Cách chọn này nhanh nhưng không bảo đảm cơ hội được chọn của mọi học sinh như nhau. Nếu các nhóm có sở thích khác nhau thì chênh lệch có thể xuất hiện ngay trong cơ chế tuyển chọn. Không được xem số phiếu lớn là bằng chứng tự động về tính đại diện.')],
[('Khảo sát tự nguyện', 'Ai chủ động trả lời có thể khác người không trả lời.',
'Giả sử ta đăng liên kết khảo sát trong một nhóm mạng xã hội. Những bạn quan tâm mạnh đến phương án A có thể hào hứng tham gia hơn. Nếu bảy mươi trong một trăm người tự nguyện trả lời chọn A, ta thu được bảy mươi phần trăm. Con số này mô tả những người đã trả lời, không phải ước lượng đáng tin cho toàn bộ một nghìn học sinh.'),
('Đặt hai tỉ lệ cạnh nhau', 'Quần thể 40%; người tự nguyện trả lời 70%.',
'Hai thanh tỉ lệ đang cho thấy bốn mươi phần trăm trong quần thể mô phỏng và bảy mươi phần trăm ở nhóm tự nguyện. Chênh lệch ba mươi điểm phần trăm xuất phát từ cách chọn và phản hồi của mẫu giả định. Đây là minh họa có chủ ý về thiên lệch, không phải dự đoán chính xác mức thiên lệch của mọi khảo sát trực tuyến.'),
('Không phản hồi cũng nguy hiểm', 'Người vắng mặt có thể mang ý kiến khác.',
'Ngay cả khi ban đầu chúng ta chọn đúng danh sách ngẫu nhiên, một số người được mời có thể không trả lời. Nếu nhóm không phản hồi có ý kiến khác với nhóm đã trả lời, ước lượng sau cùng sẽ lệch. Cần ghi nhận số người được mời, số người phản hồi và cân nhắc đặc điểm của những người vắng mặt. Không thể mặc nhiên coi im lặng là một phương án trả lời.'),
('Phân biệt hai loại sai lệch', 'Dao động do ngẫu nhiên khác thiên lệch có hệ thống.',
'Kết quả ba mươi lăm phần trăm từ mẫu ngẫu nhiên hai mươi bạn có thể chỉ là dao động lấy mẫu. Nhưng bảy mươi phần trăm từ khảo sát tự nguyện có nguy cơ thiên lệch có hệ thống. Tăng số lượng trả lời có thể làm giảm dao động ngẫu nhiên nhưng không tự sửa sự thiên lệch trong cách chọn người. Hiểu sự khác nhau này giúp ta không đặt niềm tin sai chỗ.')],
[('Rút mẫu nhiều lần', 'Cùng một quần thể nhưng mỗi lần kết quả khác nhau.',
'Hãy tưởng tượng thực hiện ba trăm lần lấy mẫu ngẫu nhiên hai mươi học sinh từ đúng quần thể một nghìn bạn. Mỗi lần trả các thẻ về quần thể trước lần rút tiếp theo, và trong từng mẫu không chọn trùng học sinh. Các tỉ lệ nhận được thay đổi: có mẫu dưới bốn mươi phần trăm, có mẫu trên bốn mươi phần trăm. Đây là dao động lấy mẫu.'),
('Biểu đồ phân bố kết quả', 'Những tỉ lệ mẫu tập trung gần 40% nhưng không trùng nhau.',
'Các cột biểu đồ mô tả số lần xuất hiện của từng khoảng tỉ lệ qua ba trăm mẫu giả lập. Đường thẳng đánh dấu bốn mươi phần trăm thật của quần thể. Ta thường thấy kết quả tập trung quanh mốc này nhưng vẫn có những lần thấp hơn hoặc cao hơn đáng kể. Biểu đồ là kết quả của một mô phỏng có hạt giống ngẫu nhiên cố định để tái lập được.'),
('Mẫu lớn hơn sẽ ra sao?', 'So ba trăm mẫu n = 20 với n = 80.',
'Bây giờ thực hiện cùng số lần rút, nhưng mỗi mẫu có tám mươi học sinh. Các cột kết quả thường gọn hơn quanh bốn mươi phần trăm. Đây mới là cách đúng để đánh giá lợi ích của cỡ mẫu: so sánh nhiều lần rút, không chỉ so một mẫu hai mươi với một mẫu tám mươi. Mẫu lớn giúp độ dao động điển hình nhỏ hơn.'),
('Kết luận từ mô phỏng', 'Một lần rút khác trung bình của rất nhiều lần rút.',
'Nếu nhìn riêng một kết quả, ta có thể nhầm tưởng mẫu lớn hơn lại kém. Nhưng xét toàn bộ ba trăm lần, độ phân tán của nhóm tám mươi nhìn chung nhỏ hơn nhóm hai mươi. Trong thống kê, cần phân biệt kết quả cụ thể và xu hướng lặp lại của một phương pháp. Mô phỏng giúp quan sát tính ngẫu nhiên thay vì chỉ học thuộc công thức.')],
[('Khái niệm sai số chuẩn', 'Cỡ mẫu tăng giúp độ dao động điển hình giảm.',
'Với tỷ lệ chọn A, ta quan tâm mức độ các tỉ lệ mẫu phân tán quanh giá trị quần thể. Một đại lượng đo độ dao động ấy gọi là độ lệch chuẩn của tỉ lệ mẫu, thường gọi sai số chuẩn khi bàn về ước lượng. Nó nhỏ đi khi kích thước mẫu tăng, nếu cách lấy mẫu không đổi và các điều kiện thống kê được giữ đúng.'),
('Công thức với mẫu không hoàn lại', 'Hiệu chỉnh quần thể hữu hạn khi rút không hoàn lại.',
'Với lấy mẫu ngẫu nhiên đơn không hoàn lại trong quần thể hữu hạn, độ lệch chuẩn của tỉ lệ mẫu bằng căn của p nhân một trừ p chia n, rồi nhân thêm hệ số hiệu chỉnh hữu hạn. Khi n nhỏ so với một nghìn, hệ số hiệu chỉnh gần một. Chúng ta dùng biểu thức chính xác cho mô hình này, không trộn lẫn lấy mẫu hoàn lại và không hoàn lại.'),
('So sánh hai kích thước mẫu', 'Độ lệch chuẩn n = 80 nhỏ hơn n = 20.',
'Thay p bằng không phẩy bốn và quần thể gồm một nghìn học sinh vào công thức. Với n bằng hai mươi, độ lệch chuẩn khoảng mười phẩy tám lăm điểm phần trăm; với n bằng tám mươi, khoảng năm phẩy hai sáu điểm phần trăm. Khi cỡ mẫu gấp bốn lần, độ dao động giảm gần một nửa. Con số là đặc trưng lý thuyết của cách lấy mẫu được mô tả.'),
('Không nhầm độ chính xác với thiên lệch', 'Mẫu lớn chỉ phát huy khi thiết kế chọn mẫu hợp lý.',
'Nếu ta tăng số người tự nguyện trả lời từ một trăm lên năm trăm, nhưng nhóm hưởng ứng vẫn bị lệch về người thích A, kết quả vẫn có thể xa tỉ lệ quần thể. Công thức sai số chuẩn vừa học giả định thiết kế lấy mẫu ngẫu nhiên phù hợp. Dùng nó để tô vẽ mức chính xác cho một mẫu tự chọn là một lỗi suy luận rất nghiêm trọng.')],
[('Từ tỉ lệ mẫu đến ước lượng', 'Một mẫu n = 200 có 88 bạn chọn A: p mũ bằng 44%.',
'Hãy xét một mẫu ngẫu nhiên đơn khác gồm hai trăm học sinh. Có tám mươi tám bạn chọn A nên tỉ lệ mẫu bằng bốn mươi bốn phần trăm. Ta có thể dùng số này làm ước lượng điểm cho tỉ lệ của quần thể. Trong thực tế, chúng ta không thấy trực tiếp bốn mươi phần trăm thật, nên cần diễn đạt rõ rằng bốn mươi bốn phần trăm là giá trị ước lượng chứ không phải chân lý.'),
('Mô tả sự bất định', 'Một khoảng ước lượng không có nghĩa chắc chắn đúng.',
'Bởi vì mẫu được rút ngẫu nhiên, một mẫu khác có thể cho kết quả khác. Thay vì chỉ ghi con số bốn mươi bốn phần trăm, ta muốn bổ sung mức bất định. Khái niệm khoảng tin cậy giúp mô tả sự bất định theo một quy trình thống kê, nhưng cần các giả định và phương pháp phù hợp. Không thể nói rằng kết quả khảo sát đã chắc chắn đúng chỉ vì dùng ký hiệu chín mươi lăm phần trăm.'),
('Khoảng xấp xỉ minh họa', 'Công thức p mũ cộng trừ 1,96 lần sai số chuẩn ước lượng.',
'Để minh họa cấp phổ thông, ta dùng khoảng xấp xỉ dạng tỉ lệ mẫu cộng trừ một phẩy chín sáu lần sai số chuẩn ước lượng, tạm bỏ hiệu chỉnh quần thể hữu hạn ở phần trước. Mẫu hai trăm có tám mươi tám ý kiến A, nên khoảng minh họa xấp xỉ ba mươi bảy phẩy một đến năm mươi phẩy chín phần trăm. Đây là công thức gần đúng, và còn cần điều kiện chọn mẫu cũng như số lượt thành công thất bại đủ lớn.'),
('Đọc đúng ý nghĩa chín mươi lăm phần trăm', 'Mức tin cậy nói về quy trình lặp lại, không về một mẫu chắc chắn.',
'Nếu cùng một phương pháp lập khoảng được áp dụng cho nhiều mẫu độc lập, về lâu dài khoảng chín mươi lăm phần trăm các khoảng có thể bao phủ tỉ lệ thật, với điều kiện xấp xỉ và giả định phù hợp. Không nên diễn giải là tỉ lệ thật có chín mươi lăm phần trăm khả năng ngẫu nhiên nằm trong một khoảng đã tính. Đó là khác biệt quan trọng giữa độ tin cậy của phương pháp và sự chắc chắn về một kết quả.')],
[('Khảo sát lỗi có thể trông rất đẹp', 'Thanh 70% dài hơn không có nghĩa ước lượng tốt hơn.',
'Một biểu đồ có màu đẹp và nhiều người trả lời vẫn có thể khiến người xem hiểu sai nếu cơ chế lấy mẫu không đáng tin. Hãy nhìn thanh bảy mươi phần trăm của nhóm tự nguyện và thanh bốn mươi phần trăm của quần thể giả lập. Vẻ ngoài rất thuyết phục không làm mất đi sai lệch có hệ thống. Ta cần xem phần mô tả cách thu thập dữ liệu trước khi đánh giá kết luận.'),
('Nếu chỉ nhìn người phản hồi', 'Nhóm hưởng ứng thay đổi, kết quả công bố thay đổi.',
'Trong minh họa động, vị trí con trỏ sẽ di chuyển từ bảy mươi phần trăm của nhóm tự nguyện về mốc bốn mươi phần trăm của quần thể. Đó không phải là một phép điều chỉnh thống kê tự động có thể dùng ngoài đời. Hiệu ứng chỉ để nhìn thấy khoảng cách do thiên lệch lựa chọn. Muốn sửa khảo sát thật, cần xem lại khung chọn mẫu, cách mời và cơ chế không phản hồi.'),
('Bộ câu hỏi kiểm tra nguồn tin', 'Ai được hỏi? Chọn thế nào? Có ai vắng mặt?',
'Khi gặp một con số phần trăm trên mạng, hãy tự hỏi bốn điều. Quần thể đích là ai? Người tham gia được chọn theo phương pháp nào? Bao nhiêu người đã không phản hồi? Và câu hỏi có dẫn dắt câu trả lời không? Chỉ khi các điều đó được mô tả minh bạch, ta mới bắt đầu đánh giá kết quả có khả năng đại diện và có thể suy rộng hay không.'),
('Mô phỏng hỗ trợ, không thay dữ liệu thật', 'Mô phỏng là công cụ học cách suy luận thống kê.',
'Cả quần thể một nghìn học sinh và những mẫu đang xem đều được tạo giả lập. Nhờ biết giá trị quần thể, ta quan sát được đặc điểm của dao động và thiên lệch. Nhưng mô phỏng không biến một cuộc khảo sát thật bị lỗi thành hợp lệ, cũng không chứng minh kết quả học sinh ngoài đời. Hãy dùng mô phỏng để hiểu phương pháp, rồi áp dụng kỹ thuật lấy mẫu đúng vào dữ liệu thật.')],
[('Bài tập: hai cuộc khảo sát', 'Cùng 200 người: ngẫu nhiên 88 A, thuận tiện 150 A.',
'Đến phần luyện tập cuối. Một trường giả lập có một nghìn học sinh. Cuộc khảo sát thứ nhất rút ngẫu nhiên hai trăm bạn, trong đó tám mươi tám chọn A. Cuộc khảo sát thứ hai cũng hỏi hai trăm người nhưng lấy thuận tiện ở nhóm quan tâm A và có một trăm năm mươi người chọn. Em hãy tính hai tỉ lệ rồi đánh giá phương pháp nào đáng dùng để suy rộng toàn trường.'),
('Tính tỉ lệ của từng mẫu', 'Viết công thức tỉ lệ: số bạn chọn A chia cho cỡ mẫu.',
'Trước tiên, đừng so sánh ngay các thanh màu. Hãy tự lấy số người chọn A chia cho hai trăm ở từng khảo sát. Ghi kết quả theo phần trăm. Sau đó suy nghĩ vì sao hai mẫu có cùng số người nhưng tỉ lệ rất khác. Điều quan trọng không chỉ là phép chia đúng, mà còn là cách con số đã được tạo ra.'),
('Giải bài toán và đối chiếu', 'Ngẫu nhiên 44%; thuận tiện 75%; chọn khảo sát ngẫu nhiên.',
'Khảo sát ngẫu nhiên cho tám mươi tám chia hai trăm, bằng bốn mươi bốn phần trăm. Khảo sát thuận tiện cho một trăm năm mươi chia hai trăm, bằng bảy mươi lăm phần trăm. Để ước lượng tỉ lệ của cả trường, cách chọn ngẫu nhiên phù hợp hơn nếu danh sách và việc phản hồi được bảo đảm. Mẫu thuận tiện không thể dùng để suy rộng chỉ vì có đúng hai trăm người.'),
('Khép lại series: tư duy từ dữ liệu', 'Thu thập đúng, biểu diễn rõ, tính đúng và kết luận có giới hạn.',
'Qua toàn bộ series thống kê, chúng ta đã đi từ thu thập dữ liệu, bảng và biểu đồ đến trung bình, trung vị, độ phân tán, số liệu ghép nhóm, tương quan và cuối cùng là lấy mẫu. Công thức giúp tính toán, hình ảnh giúp nhận ra quy luật, nhưng chất lượng kết luận phụ thuộc vào nguồn dữ liệu và các giả định. Hãy luôn hỏi dữ liệu đến từ đâu trước khi tin một con số. Cảm ơn các em đã đồng hành cùng Thầy Nguyễn Văn Sang.')]
]
BEATS=tuple(Beat(i+1,j+1,*row) for i,ch in enumerate(ROWS) for j,row in enumerate(ch))

def validate():
    assert N==1000 and sum(POPULATION)==400 and TRUE_P==.4
    assert len(CHAPTERS)==len(ROWS)==8 and all(len(c)==4 for c in ROWS)
    assert len(BEATS)==32 and len({b.title for b in BEATS})==32
    assert all(len(b.voice.split())>=49 for b in BEATS)
    assert all(b.duration==38.0 for b in BEATS)
    assert sum(sample(20))==7 and sum(sample(80))==37 and sum(sample(200))==88
    assert len(trials(20))==len(trials(80))==300
    assert sd_sample_proportion(80)<sd_sample_proportion(20)
    return True

if __name__=='__main__':
    print('STAT18_LESSON',validate(),len(BEATS),'words:',sum(len(x.voice.split()) for x in BEATS))
