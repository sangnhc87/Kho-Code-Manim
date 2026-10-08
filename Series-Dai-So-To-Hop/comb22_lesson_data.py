"""COMB22: independent combinatorial DP models, teaching data and validations."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product, permutations
from math import comb, factorial
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
CHAPTERS = [
 ('grid','01 · QUY HOẠCH ĐỘNG TỪ ĐƯỜNG ĐI'),
 ('obstacle','02 · ĐƯỜNG ĐI CÓ CHƯỚNG NGẠI'),
 ('tiling','03 · BÀI TOÁN LÁT GẠCH VÀ TRUY HỒI'),
 ('binary','04 · DÃY NHỊ PHÂN TRÁNH 11'),
 ('automaton','05 · MÁY TRẠNG THÁI TRÁNH 101'),
 ('bitmask','06 · DP BITMASK VÀ BÀI TOÁN PHÂN CÔNG'),
 ('matrix','07 · MA TRẬN CHUYỂN TRẠNG THÁI'),
 ('capstone','08 · OLYMPIC: BA RÀNG BUỘC ĐỒNG THỜI'),
]
CHAPTER_LABELS = dict(CHAPTERS)

@dataclass(frozen=True)
class Beat:
    section: str
    state: int
    heading: str
    lines: tuple[str, str, str]
    takeaway: str
    narration: str
    formula: str
    min_seconds: float

BEATS=[]
FORMULAS={}

def add(section, rows):
    assert len(rows)==6, section
    for j,(heading, bullets, takeaway, expression, narration) in enumerate(rows):
        assert len(bullets)==3
        key=f'{section}_{j}'
        FORMULAS[key]=expression
        BEATS.append(Beat(section,j,heading,tuple(bullets),takeaway,narration,key,28.0))


def grid_table(right, up, blocked=()):
    if right<0 or up<0: raise ValueError('Dimensions must be nonnegative')
    banned=set(blocked)
    a=[[0]*(up+1) for _ in range(right+1)]
    for i in range(right+1):
        for j in range(up+1):
            if (i,j) in banned: continue
            if i==0 and j==0:a[i][j]=1
            else:a[i][j]=(a[i-1][j] if i else 0)+(a[i][j-1] if j else 0)
    return a

def paths_bruteforce(right,up,blocked=()):
    from itertools import combinations
    count=0
    for ups in combinations(range(right+up),up):
        x=y=0
        if (x,y) in blocked:continue
        good=True
        for t in range(right+up):
            if t in ups:y+=1
            else:x+=1
            if (x,y) in blocked:good=False;break
        count+=int(good)
    return count

def tilings(n):
    if n<0:raise ValueError('n>=0')
    dp=[0]*(n+2);dp[0]=1
    for k in range(1,n+1):dp[k]=dp[k-1]+(dp[k-2] if k>=2 else 0)
    return dp[n]

def tilings_direct(n):
    if n==0:return [()]
    if n<0:return []
    return [(1,)+t for t in tilings_direct(n-1)]+[(2,)+t for t in tilings_direct(n-2)]

def no11_states(n):
    if n<0:raise ValueError('n>=0')
    z,o=1,0
    for _ in range(n):z,o=z+o,z
    return z,o

def no11_bruteforce(n):
    return sum(all(not (s[i]==s[i+1]==1) for i in range(n-1)) for s in product((0,1),repeat=n))

def automaton_next(state,bit,pattern='101'):
    if not pattern or any(ch not in '01' for ch in pattern):raise ValueError('binary pattern required')
    s=pattern[:state]+str(bit)
    if s.endswith(pattern):return None
    for k in range(len(pattern)-1,-1,-1):
        if s.endswith(pattern[:k]):return k
    return 0

def pattern_dp(n,pattern='101',ones=None,last=None):
    if n<0:raise ValueError('n>=0')
    if ones is not None and ones<0:return 0
    states={(0,0,None):1}
    for _ in range(n):
        nxt=defaultdict(int)
        for (q,k,prev),v in states.items():
            for bit in (0,1):
                ns=automaton_next(q,bit,pattern)
                if ns is None:continue
                if ones is not None and k+bit>ones:continue
                nxt[ns,k+bit,bit]+=v
        states=nxt
    return sum(v for (q,k,prev),v in states.items() if (ones is None or k==ones) and (last is None or prev==last))

def pattern_bruteforce(n,pattern='101',ones=None,last=None):
    return sum(pattern not in ''.join(map(str,s)) and (ones is None or sum(s)==ones) and (last is None or (bool(s) and s[-1]==last)) for s in product((0,1),repeat=n))

def pattern_rows(n,pattern='101'):
    q=[1]+[0]*(len(pattern)-1)
    result=[tuple(q)]
    for _ in range(n):
        new=[0]*len(q)
        for state,v in enumerate(q):
            for bit in (0,1):
                nxt=automaton_next(state,bit,pattern)
                if nxt is not None:new[nxt]+=v
        q=new;result.append(tuple(q))
    return result

def bitmask_derangements(n):
    if n<0:raise ValueError('n>=0')
    dp=[0]*(1<<n);dp[0]=1
    for mask in range(1<<n):
        row=mask.bit_count()
        if row==n:continue
        for col in range(n):
            if not (mask>>col)&1 and col!=row:dp[mask|1<<col]+=dp[mask]
    return dp[-1]

def bitmask_layers(n):
    dp=[0]*(1<<n);dp[0]=1
    for mask in range(1<<n):
        row=mask.bit_count()
        if row==n:continue
        for col in range(n):
            if not ((mask>>col)&1) and col!=row:dp[mask|1<<col]+=dp[mask]
    return [sum(v for mask,v in enumerate(dp) if mask.bit_count()==k) for k in range(n+1)]

def matrix_multiply(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def matrix_power(n):
    if n<0:raise ValueError('n>=0')
    a=[[1,1],[1,0]];p=[[1,0],[0,1]]
    for _ in range(n):p=matrix_multiply(p,a)
    return p

def circular_no11(n):
    if n<1:raise ValueError('n>=1')
    p=matrix_power(n)
    return p[0][0]+p[1][1]

def circular_no11_direct(n):
    return sum(all(not(s[i] and s[(i+1)%n]) for i in range(n)) for s in product((0,1),repeat=n))
add('grid', [
 ('Từ một bài toán đường đi', ('Đi từ O(0;0) đến P(4;3)', 'Mỗi bước: phải hoặc lên', 'Cần đếm các lộ trình khác nhau'), 'Một đường đi là một dãy lựa chọn.', 'N=C_3^7=35', 'Hãy hình dung một chú kiến đứng ở góc trái dưới của lưới ô vuông. Kiến cần đi đến đỉnh có tọa độ bốn, ba; mỗi bước chỉ được sang phải hoặc đi lên. Liệt kê từng đường đi sẽ rất dài. Chúng ta cần một quy luật đếm được từng phần nhỏ, sau đó dùng các kết quả đã biết để tạo ra kết quả lớn hơn. Đó chính là trực giác đầu tiên về quy hoạch động.'),
 ('Đếm số cách tới mỗi đỉnh', ('Một đỉnh nhận đường đi từ đâu?', 'Chỉ từ bên trái hoặc phía dưới', 'Gọi f(i,j) là số đường tới đỉnh đó'), 'Định nghĩa đúng trạng thái trước khi tính.', 'f_(i,j) >= 0', 'Thay vì đếm những lộ trình dài từ đầu đến cuối, ta hỏi có bao nhiêu cách để tới một đỉnh trung gian. Mọi đường hợp lệ đến đỉnh này phải kết thúc bằng một bước sang phải từ đỉnh bên trái, hoặc một bước lên từ đỉnh bên dưới. Hai trường hợp không trùng nhau. Khi đặt tên cho số cách đến mỗi đỉnh, chúng ta đã biến bài toán lớn thành nhiều bài toán nhỏ có liên hệ rõ ràng.'),
 ('Hệ thức chuyển trạng thái', ('Đi tới (i;j) bằng hai hướng', 'Hai tập đường đi không trùng nhau', 'Cộng số cách của hai đỉnh trước'), 'Điều quan trọng là hai trường hợp rời nhau.', 'f_(i,j)=f_(i-1,j)+f_(i,j-1)', 'Tại ô đang sáng, các mũi tên cho thấy hai nguồn đi vào. Nếu bước cuối cùng là sang phải, phần đường đi trước đó kết thúc ở ô bên trái. Nếu bước cuối cùng là đi lên, ta xuất phát từ ô ngay bên dưới. Vì hai bước cuối khác nhau nên không có đường nào bị tính hai lần. Từ đây xuất hiện công thức truy hồi, phần cốt lõi của quy hoạch động trên lưới.'),
 ('Điều kiện đầu và thứ tự tính', ('Tại O có đúng một đường rỗng', 'Ngoài lưới coi số cách bằng 0', 'Tính từ góc dưới trái tiến dần lên'), 'Thiếu điều kiện đầu thì truy hồi chưa đủ.', 'f_(0,0)=1', 'Công thức truy hồi chỉ có ý nghĩa khi chúng ta biết số cách ở điểm xuất phát. Có đúng một cách bắt đầu ở O mà chưa bước lần nào, đó là đường rỗng. Những tọa độ âm nằm ngoài bảng được quy ước có không cách. Nhờ điều kiện đầu ấy, ta điền các ô theo thứ tự để mỗi khi cần một giá trị, giá trị phía trước đã được tính và lưu. Đây là điểm khác biệt giữa công thức và một thuật toán thực thi.'),
 ('Điền bảng như tam giác Pascal', ('Bắt đầu ở các cạnh biên', 'Mỗi ô là tổng hai ô liền trước', 'Giá trị tự lan tới góc đích'), 'Quy hoạch động tái sử dụng kết quả.', 'f_(4,3)=35', 'Khi từng số xuất hiện trên các đỉnh của lưới, thầy cô và học sinh sẽ nhận thấy một cấu trúc rất quen: mỗi số được hình thành bằng tổng hai số bên cạnh. Cách làm này gần với tam giác Pascal, nhưng giờ ý nghĩa của mỗi hệ số là số đường đến một vị trí. Những đường đi chung phần đầu không còn phải được liệt kê lại nhiều lần. Thuật toán chỉ lưu và cập nhật mỗi trạng thái một lần.'),
 ('Kiểm chứng bằng tổ hợp', ('Mỗi đường có đúng bảy bước', 'Chọn ba bước đi lên', 'So sánh DP với công thức tổ hợp'), 'Hai cách đếm phải khớp nhau.', 'f_(4,3)=C_3^7=35', 'Ta có thể kiểm chứng bảng quy hoạch động bằng một phép đếm hoàn toàn khác. Mọi lộ trình đến đích gồm bốn bước sang phải và ba bước đi lên, tổng cộng bảy vị trí. Chỉ cần quyết định ba vị trí dành cho bước đi lên, bốn vị trí còn lại tự động là bước sang phải. Vì thế số cách là tổ hợp chập ba của bảy. Kết quả bằng ba mươi lăm đúng như ô cuối của bảng, tạo một kiểm chứng độc lập.'),
])

add('obstacle', [
 ('Khi xuất hiện chướng ngại', ('Vẫn đi từ (0;0) tới (4;3)', 'Cấm đi qua đỉnh (2;1)', 'Không phải mọi lộ trình đều hợp lệ'), 'Thay đổi nhỏ ở điều kiện, đổi cách đếm.', 'N_("hợp lệ")=35-N_("qua chặn")', 'Lần này lưới giữ nguyên nhưng một đỉnh ở giữa được tô đỏ. Chú kiến tuyệt đối không được đi qua đỉnh hai, một. Nếu chỉ áp dụng công thức chọn ba bước lên trong bảy bước, ta sẽ đếm cả những đường xuyên qua điểm cấm. Quy hoạch động tỏ ra hữu ích vì điều kiện mới chỉ cần được đưa vào đúng trạng thái của ô bị chặn, thay vì kiểm tra lại từng đường đi hoàn chỉnh.'),
 ('Điều kiện tại ô bị chặn', ('Đỉnh màu đỏ không được đi qua', 'Đặt số cách tới đây bằng 0', 'Mọi ô phía sau cập nhật theo nó'), 'Trạng thái cấm có giá trị bằng không.', 'f_(2,1)=0', 'Quan sát ô đỏ. Dù có những cách di chuyển từ O đến vị trí ấy, bài toán quy định không được sử dụng chúng. Vì vậy ta gán giá trị trạng thái bằng không, không áp dụng truy hồi thông thường tại ô đỏ. Mọi ô kế tiếp vẫn lấy tổng từ hai ô trước nhưng nếu một nguồn là điểm cấm thì nguồn đó đóng góp bằng không. Chỉ một thay đổi cục bộ đã tự động loại tất cả lộ trình không hợp lệ.'),
 ('Bảng giá trị tự động cập nhật', ('Giữ nguyên quy tắc cộng từ hai hướng', 'Bỏ mọi đường dẫn qua ô cấm', 'Đọc số ở đỉnh cuối bảng'), 'DP xử lý điều kiện cục bộ rất tự nhiên.', 'f_(4,3)=17', 'Chúng ta lại tô sáng các ô theo thứ tự từ trái sang phải và từ dưới lên trên. Trước ô cấm, giá trị vẫn giống trường hợp bình thường. Tại ô cấm xuất hiện số không. Sau vị trí ấy, nhiều con số giảm vì một phần lộ trình đã bị loại từ trước. Kết quả cuối bảng là mười bảy. Điều quan trọng không phải chỉ ở đáp số, mà ở cách các điều kiện được truyền đúng qua từng trạng thái.'),
 ('Đếm đường phải đi qua điểm cấm', ('Tách đường thành O tới Q', 'Tiếp từ Q tới đích', 'Dùng quy tắc nhân cho hai đoạn'), 'Đếm phần bù giúp tự kiểm tra DP.', 'N_("qua Q")=C_1^3 C_2^4=18', 'Để chắc chắn đáp số mười bảy là đúng, ta thử cách đếm phần bù. Một đường đi qua Q với tọa độ hai, một được chia duy nhất thành hai đoạn: từ O tới Q và từ Q tới đích. Đoạn đầu có ba bước với một bước lên, nên có ba cách. Đoạn sau có bốn bước, hai bước lên, nên có sáu cách. Ghép hai đoạn theo quy tắc nhân, thu được mười tám đường bị cấm.'),
 ('Hai cách giải cùng đáp số', ('Tổng cộng có 35 lộ trình', 'Có 18 lộ trình qua Q', 'Số hợp lệ là 35 trừ 18'), 'Đếm bù và DP bổ sung cho nhau.', '35-18=17', 'Phần bù cho ba mươi lăm trừ mười tám bằng mười bảy. Đây là đáp số đã tìm được bằng bảng quy hoạch động. Hai phương pháp độc lập trùng kết quả không phải là một sự ngẫu nhiên: cả hai đều phân chia chính xác tập lộ trình theo điều kiện có đi qua Q hay không. Ta cũng thấy một tiêu chuẩn chọn phương pháp: ít điểm cấm thì đếm bù có thể gọn, nhiều vật cản phức tạp thì DP thường linh hoạt hơn.'),
 ('Tổng quát nhiều ô bị cấm', ('Với mỗi ô cấm đặt f bằng 0', 'Không cần viết công thức mới', 'Độ phức tạp theo số đỉnh lưới'), 'Thiết kế trạng thái tốt giúp mở rộng dễ.', 'T=O((a+1)(b+1))', 'Nếu có năm, mười hoặc hàng trăm đỉnh không thể đi qua, ta chỉ cần thêm các vị trí đó vào tập cấm. Hệ thức ở các ô hợp lệ hoàn toàn không thay đổi. Với một lưới có a cộng một cột và b cộng một hàng, số trạng thái cần xử lý tỉ lệ với số đỉnh. Vì thế quy hoạch động tránh sự bùng nổ của việc liệt kê tất cả các đường đi. Đây là ví dụ rất rõ về lợi ích thuật toán.'),
])
add('tiling', [
 ('Lát một dải dài sáu ô', ('Gạch loại một ô hoặc hai ô', 'Không chồng, không để khoảng trống', 'Thứ tự đặt các viên có ý nghĩa'), 'Chọn viên đầu hay viên cuối đều được.', 'f_6=13', 'Một sàn gồm sáu ô liên tiếp cần được phủ kín bằng hai loại viên: viên ngắn chiếm một ô và viên dài chiếm hai ô. Mỗi cách lát được phân biệt theo dãy độ dài các viên, không phải theo màu sơn của chúng. Nếu thử dựng từng cách, học sinh sẽ thấy số trường hợp tăng nhanh. Ta hãy coi độ dài cần phủ là trạng thái và tìm một quy tắc xuất phát từ viên đặt ở cuối cùng.'),
 ('Phân chia theo viên cuối', ('Viên cuối dài một ô', 'Hoặc viên cuối dài hai ô', 'Hai trường hợp rời nhau'), 'Bài toán tự rút về chiều dài ngắn hơn.', 'f_n=f_(n-1)+f_(n-2)', 'Hình động làm hiện ra một viên dài một ô ở cuối dải. Khi bỏ viên đó, phần trước phải là một cách lát hợp lệ của dải dài n trừ một. Tương tự, nếu viên cuối dài hai ô, phần đầu còn n trừ hai ô. Hai khả năng không giao nhau và bao phủ mọi cách lát. Do đó số cách lát dải dài n bằng tổng của hai giá trị đã được tính ở những độ dài nhỏ hơn.'),
 ('Điều kiện khởi đầu', ('Dải rỗng có một cách lát', 'Dải một ô có một cách lát', 'Dãy bắt đầu từ 1, 1'), 'Đường truy hồi cần hai mốc ban đầu.', 'f_0=f_1=1', 'Cần lưu ý rằng dải không có ô vẫn có đúng một cách lát: không đặt viên nào. Nếu ta đặt f không bằng không, công thức truy hồi sẽ không cho ra kết quả đúng ở các độ dài sau. Với dải một ô thì duy nhất viên loại một. Hai giá trị đầu bằng một xác định toàn bộ dãy. Đây là lý do phải phát biểu điều kiện ban đầu trước khi viết chương trình hoặc tạo bảng quy hoạch động.'),
 ('Điền từng số Fibonacci', ('f2 = 2; f3 = 3', 'f4 = 5; f5 = 8', 'f6 = 13 cách lát'), 'Fibonacci xuất hiện từ một lựa chọn cuối.', '1,1,2,3,5,8,13', 'Bây giờ mỗi bước hình động sẽ ghép hai số trước thành một số mới. Ta thu được lần lượt một, một, hai, ba, năm, tám, mười ba. Đó chính là một dạng đánh chỉ số của dãy Fibonacci. Sự xuất hiện của Fibonacci không phải do may mắn, mà do cấu trúc của bài toán: bất kỳ phương án hoàn chỉnh nào cũng có thể được chia theo hai kiểu viên cuối với độ dài giảm lần lượt một và hai.'),
 ('So sánh đệ quy và DP', ('Đệ quy đơn giản tính trùng nhiều lần', 'DP lưu một giá trị cho mỗi độ dài', 'Có thể dùng chỉ hai biến nhớ'), 'Thời gian tuyến tính thay cho phân nhánh.', 'T(n)=O(n)', 'Nếu dùng đệ quy không ghi nhớ, khi tính f sáu ta lại tính f năm và f bốn, rồi những nhánh này tiếp tục gọi nhiều giá trị chung. Một cây đệ quy đẹp về mặt toán học nhưng gây lặp việc. Quy hoạch động tính mỗi f đúng một lần và lưu lại. Thậm chí vì công thức chỉ cần hai số trước, ta có thể viết thuật toán dùng hai biến. Đây là cơ hội để phân biệt chứng minh truy hồi với hiệu quả của cách thực thi.'),
 ('Mở rộng ba loại bước', ('Cho phép thêm viên dài ba ô', 'Cần xét ba dạng viên cuối', 'Truy hồi có ba số hạng'), 'Số loại lựa chọn quyết định bậc truy hồi.', 'g_n=g_(n-1)+g_(n-2)+g_(n-3)', 'Nếu nhà sản xuất bổ sung viên phủ ba ô, lập luận theo viên cuối vẫn hoạt động. Mỗi cách lát phải kết thúc bằng viên một ô, hai ô hoặc ba ô. Ba nhóm phương án rời nhau, từ đó xuất hiện truy hồi ba số hạng. Để áp dụng đúng ở những n nhỏ, ta quy ước số cách lát dải âm bằng không và dải rỗng bằng một. Sự mở rộng này cho thấy phương pháp quan trọng hơn việc ghi nhớ một công thức Fibonacci cụ thể.'),
])

add('binary', [
 ('Dãy nhị phân tránh hai số một liền nhau', ('Mỗi vị trí nhận 0 hoặc 1', 'Cấm xuất hiện cặp 11', 'Không thể dùng trực tiếp 2 mũ n'), 'Điều kiện phụ thuộc ký tự trước.', 'N_6=21', 'Ta xét các dãy gồm sáu chữ số, mỗi chữ số bằng không hoặc một. Nếu không có ràng buộc sẽ có sáu mươi tư dãy, nhưng lần này không cho phép hai chữ số một đứng sát nhau. Lựa chọn tại một vị trí phụ thuộc vào chữ số vừa đặt, vì vậy quy tắc nhân đơn giản không còn đủ. Hãy nhìn hai loại dãy dựa theo ký tự kết thúc để tìm một trạng thái ghi nhớ ngắn gọn.'),
 ('Chia trạng thái theo ký tự cuối', ('a_n: dãy hợp lệ kết thúc 0', 'b_n: dãy hợp lệ kết thúc 1', 'Hai nhóm rời nhau'), 'Trạng thái phải lưu thông tin cần thiết.', 'N_n=a_n+b_n', 'Một dãy hợp lệ kết thúc bằng không có thể được tạo từ bất kỳ dãy hợp lệ độ dài n trừ một, vì thêm không không bao giờ tạo ra cặp một một. Ngược lại, dãy kết thúc bằng một chỉ có thể được nối tiếp từ dãy kết thúc bằng không. Ta không cần nhớ toàn bộ lịch sử trước đó; chỉ ký tự cuối là đủ để quyết định bước tiếp theo có hợp lệ hay không.'),
 ('Công thức chuyển hai trạng thái', ('Kết thúc 0 nhận từ cả hai trạng thái', 'Kết thúc 1 chỉ nhận từ trạng thái 0', 'Cập nhật đồng thời hai biến'), 'Một lựa chọn cấm trở thành cạnh bị loại.', 'a_n=a_(n-1)+b_(n-1),quad b_n=a_(n-1)', 'Trong sơ đồ, mũi tên xanh từ cả hai trạng thái đều hướng về trạng thái cuối bằng không. Chỉ có một mũi tên hợp lệ đi tới trạng thái cuối bằng một, đó là từ dãy trước kết thúc bằng không. Mũi tên từ một sang một được tô đỏ và loại khỏi phép đếm. Bằng cách này, việc đếm các dãy có ràng buộc chuyển thành cập nhật hai con số qua từng độ dài.'),
 ('Bảng từ độ dài một tới sáu', ('Khởi đầu bằng cặp trạng thái (1;0)', 'Mỗi bước sinh một dòng giá trị mới', 'Kết quả độ dài sáu bằng 21'), 'Không liệt kê đủ 64 dãy mới có đáp số.', 'N_6=13+8=21', 'Bắt đầu với dãy rỗng thuộc trạng thái có thể nối số không, ta lần lượt thêm một vị trí. Mỗi hàng của bảng chỉ chứa hai con số, thay vì hàng chục hoặc hàng trăm dãy riêng lẻ. Ở độ dài sáu, số dãy kết thúc bằng không là mười ba, còn kết thúc bằng một là tám. Cộng lại có hai mươi mốt dãy thỏa điều kiện. Ta có thể dùng chương trình sinh hết dãy nhỏ để xác nhận.'),
 ('Fibonacci xuất hiện lần nữa', ('Tổng Nn = N(n−1) + N(n−2)', 'Cùng cấu trúc như bài lát gạch', 'Khác câu chuyện nhưng cùng truy hồi'), 'Tương đồng truy hồi tạo cầu nối bài toán.', 'N_n=N_(n-1)+N_(n-2)', 'Nếu loại bỏ trạng thái trung gian, ta nhận thấy tổng số dãy hợp lệ độ dài n bằng số ở độ dài n trừ một cộng với số ở độ dài n trừ hai. Đây là Fibonacci một lần nữa. Lát gạch và dãy nhị phân tưởng như khác nhau, nhưng có thể xây dựng một đối ứng: mỗi viên dài hai ô tương ứng với khối ký tự một theo sau bởi không, còn viên một ô tương ứng với ký tự không. Điều quan trọng là nhận diện cấu trúc lựa chọn chung.'),
 ('Kiểm tra bằng chia theo đầu dãy', ('Bắt đầu 0: còn bài toán n−1', 'Bắt đầu 10: còn bài toán n−2', 'Không có lựa chọn đầu nào khác'), 'Phân hoạch đúng cho một chứng minh độc lập.', 'N_n=N_(n-1)+N_(n-2)', 'Có thể chứng minh truy hồi mà không sử dụng trạng thái ký tự cuối. Mỗi dãy hợp lệ hoặc bắt đầu bằng không, hoặc bắt đầu bằng một. Nếu bắt đầu bằng không, phần còn lại là một dãy hợp lệ có n trừ một chữ số. Nếu bắt đầu bằng một và còn vị trí tiếp theo, chữ số kế bắt buộc bằng không, tạo tiền tố một không. Đó là trường hợp có n trừ hai vị trí tự do. Hai loại tiền tố tách biệt, khép kín cách đếm.'),
])

add('automaton', [
 ('Tránh một mẫu dài ba ký tự', ('Cấm xuất hiện chuỗi 101', 'Chỉ nhớ ký tự cuối là chưa đủ', 'Cần theo dõi một phần mẫu'), 'Trạng thái ghi nhớ tiền tố phù hợp.', 'P="101"', 'Bây giờ ta thay điều kiện cấm cặp một một bằng một mẫu dài hơn: không được xuất hiện liên tiếp các ký tự một, không, một. Để biết thêm một chữ số có tạo ra mẫu cấm hay không, ký tự cuối thôi chưa chắc đủ. Chẳng hạn tiền tố một không rất nguy hiểm nếu ký tự mới là một. Vì vậy ta thiết kế một máy trạng thái ghi nhớ phần cuối của dãy đang trùng với tiền tố của mẫu bị cấm.'),
 ('Ba trạng thái của mẫu 101', ('q0: chưa giữ được tiền tố', 'q1: đang có hậu tố 1', 'q2: đang có hậu tố 10'), 'Chỉ lưu hậu tố hữu ích nhất.', 'Q={q_0,q_1,q_2}', 'Trạng thái không có nghĩa là toàn bộ dãy đã xây dựng, mà chỉ là thông tin ngắn nhất cần biết để tiếp tục. Với mẫu một không một, ta dùng ba trạng thái: không có hậu tố liên quan, có hậu tố một, và có hậu tố một không. Mỗi lần thêm ký tự, ta giữ hậu tố dài nhất vẫn là tiền tố của mẫu cấm. Nhờ đó nhiều dãy khác nhau có thể gộp chung một trạng thái mà vẫn đếm chính xác.'),
 ('Vẽ các cung chuyển hợp lệ', ('Từ q2 thêm 1 sẽ tạo 101', 'Cung bị cấm được tô đỏ', 'Các cung còn lại chuyển sang q0,q1,q2'), 'Bỏ đúng cung cấm, không bỏ nhầm dãy.', 'delta(q_2,1)="cấm"', 'Quan sát trạng thái q hai tương ứng với hậu tố một không. Nếu thêm một, ba ký tự cuối thành một không một nên đường chuyển đó bị loại ngay lập tức. Nhưng thêm không sẽ quay về trạng thái không vì hậu tố của dãy mới không khớp tiền tố mẫu cấm. Từ q một thêm không đi tới q hai, còn thêm một vẫn giữ hậu tố một. Sơ đồ các cung cho ta một thuật toán kiểm tra từng bước, không cần xét mọi chuỗi hoàn chỉnh.'),
 ('Quy hoạch động trên máy trạng thái', ('dp[t][q] đếm tiền tố dài t', 'Bắt đầu tại q0 với số cách 1', 'Phân phối số cách dọc theo các cung'), 'Đếm đường trên đồ thị trạng thái.', 'dp_(t+1,q)=sum_(p to q)dp_(t,p)', 'Từ trạng thái khởi đầu q không có một dãy rỗng, ta chuyển số cách sang các trạng thái kế tiếp theo từng ký tự được phép. Nếu hai cung khác nhau cùng kết thúc tại một trạng thái, số lượng của chúng được cộng lại. Về bản chất, đây là bài toán đếm đường đi trên một đồ thị định hướng rất nhỏ. Mỗi lớp thời gian tương ứng với một ký tự mới. Số trạng thái chỉ bằng ba dù độ dài chuỗi tăng lên hàng trăm.'),
 ('Dãy dài sáu có 37 cách', ('Tính đủ ba trạng thái ở bước sáu', 'Tổng số đếm bằng 37', 'Đối chiếu với liệt kê nhị phân'), 'Một máy trạng thái xử lý vô số độ dài.', 'N_6=37', 'Khi đến độ dài sáu, cộng số cách của ba trạng thái ta được ba mươi bảy. Chúng ta có thể kiểm thử bằng chương trình duyệt cả sáu mươi tư dãy nhị phân rồi gạch bỏ những dãy chứa mẫu một không một. Cả hai cách phải trùng nhau. Điều đáng học ở đây là cách thiết kế trạng thái có thể mở rộng cho bất kỳ mẫu cấm hữu hạn nào, không chỉ đúng bài toán đang minh họa.'),
 ('Nhiều mẫu cấm và độ dài lớn', ('Ghép trạng thái vào một máy tự động', 'Chỉ cần lưu tiền tố có ích', 'Dùng ma trận khi độ dài rất lớn'), 'DP trạng thái là nền của nhiều bài Olympic.', 'v_(t+1)=M v_t', 'Nếu cấm đồng thời hai hoặc ba mẫu ký tự, chúng ta phải xây một máy trạng thái lớn hơn, nhưng tư tưởng không đổi: mỗi trạng thái cho biết phần hậu tố còn hữu ích để kiểm tra các mẫu. Sau khi có bảng chuyển, việc đếm trở thành phép lặp chuyển trạng thái. Với độ dài vài triệu, ta thậm chí có thể đưa phép lặp ấy vào ma trận và tính lũy thừa nhanh. Đây là cầu nối sang kỹ thuật của chương kế tiếp.'),
])
add('bitmask', [
 ('Phân công bốn người cho bốn việc', ('Mỗi người nhận đúng một việc', 'Không ai nhận việc cùng số thứ tự', 'Đổi vai trò tạo kết quả mới'), 'Ràng buộc trên một hoán vị tạo bài toán DP.', 'N=9', 'Có bốn học sinh và bốn nhiệm vụ khác nhau. Mỗi người phải nhận đúng một nhiệm vụ và mỗi nhiệm vụ chỉ giao cho một người. Ngoài ra, người thứ i không được nhận nhiệm vụ thứ i. Nếu không có điều kiện cấm, ta có hai mươi bốn hoán vị. Nhưng khi danh sách nhiệm vụ tăng, cách liệt kê trở nên quá dài. Quy hoạch động với mặt nạ bit cho phép ghi nhớ tập nhiệm vụ đã sử dụng.'),
 ('Mặt nạ bit đại diện cho tập đã chọn', ('Bốn bit biểu diễn bốn nhiệm vụ', 'Bit 1 nghĩa là nhiệm vụ đã dùng', 'Ví dụ 0101 là hai nhiệm vụ'), 'Tập hợp có thể mã hóa bằng một số nguyên.', '0 <= mask < 2^4', 'Hãy tưởng tượng bốn chiếc công tắc đại diện cho bốn nhiệm vụ. Công tắc bật nghĩa là nhiệm vụ đó đã được giao. Trạng thái không cần nhớ thứ tự các nhiệm vụ trước đây giao cho ai, vì người đang xét được xác định bằng số bit một trong mặt nạ. Cùng một tập nhiệm vụ đã dùng có thể đạt tới bằng nhiều cách; ta cộng số cách ấy và lưu vào cùng một ô DP.'),
 ('Bước chuyển sang người tiếp theo', ('Đã có k bit 1 thì xét người k+1', 'Chỉ chọn nhiệm vụ có bit 0', 'Bỏ lựa chọn trùng chỉ số bị cấm'), 'Mỗi phép chuyển bật đúng một bit.', 'dp_(mask+2^j) += dp_(mask)', 'Tại một mặt nạ cụ thể, số bit đang bật cho biết chúng ta đã phân công xong bao nhiêu người. Với người tiếp theo, ta duyệt từng nhiệm vụ chưa được sử dụng. Nếu nhiệm vụ ấy trùng chỉ số người, cung chuyển bị tô đỏ và không thực hiện. Nếu hợp lệ, ta bật bit tương ứng để tạo mặt nạ mới và cộng thêm số cách đang có. Công thức cập nhật này là trái tim của quy hoạch động theo tập con.'),
 ('Tính lớp trạng thái theo số bit', ('Bắt đầu dp[0000] bằng 1', 'Lần lượt tới các lớp có 1,2,3,4 bit', 'Cùng một mặt nạ cộng các đường đi'), 'Quy hoạch động tránh tính lặp tập đã dùng.', 'dp[0000]=1', 'Các mặt nạ được chia thành từng lớp theo số bit một. Lớp đầu là mặt nạ không, biểu thị chưa giao nhiệm vụ nào. Chỉ từ những trạng thái có một bit ta mới sinh trạng thái có hai bit, rồi đến ba và bốn bit. Bằng cách cập nhật theo lớp, ta luôn biết số cách của trạng thái cũ trước khi dùng nó. Nhiều trình tự phân công khác nhau có thể dẫn đến cùng mặt nạ, và phép cộng trong DP giữ lại toàn bộ chúng.'),
 ('Đọc kết quả và kiểm chứng', ('Mặt nạ cuối 1111 dùng đủ việc', 'Giá trị nhận được là 9', 'Đối chiếu bằng liệt kê 24 hoán vị'), 'Mặt nạ đủ bit là trạng thái đích.', 'dp[1111]=9', 'Khi cả bốn bit đều bật, bốn nhiệm vụ đã được sử dụng đúng một lần. Số cách tại mặt nạ cuối là chín. Kết quả này đúng bằng số hoán vị không điểm cố định của bốn phần tử, một bài đã gặp khi học phép đếm phần bù. Kiểm chứng bằng cách liệt kê các hoán vị nhỏ giúp chúng ta phân biệt rõ thuật toán DP là một cách tổ chức tính toán, còn nội dung toán học vẫn là đếm đúng và không trùng.'),
 ('Khi số người tăng lên', ('Có 2 mũ n trạng thái mặt nạ', 'Mỗi trạng thái thử tối đa n việc', 'Tận dụng cấu trúc điều kiện phân công'), 'Bitmask DP là công cụ mạnh cho n vừa.', 'T(n)=O(n 2^n)', 'Nếu tăng từ bốn lên mười hoặc mười lăm người với các điều kiện cấm khác nhau, ta vẫn sử dụng một mô hình mặt nạ bit tương tự. Số trạng thái là hai mũ n, và từ mỗi trạng thái có tối đa n lựa chọn mới, nên thuật toán có bậc thời gian n nhân hai mũ n. Cách này vẫn là hàm mũ, nhưng thường hiệu quả hơn rất nhiều so với việc duyệt n giai thừa cách phân công và kiểm tra từng cách.'),
])

add('matrix', [
 ('Từ hai trạng thái tới ma trận', ('Nhắc lại dãy tránh 11', 'Hai số đếm: kết thúc 0 hoặc 1', 'Mỗi bước chỉ cộng các nguồn hợp lệ'), 'Chuyển trạng thái là phép biến đổi tuyến tính.', 'v_(n+1)=M v_n', 'Ở chương này ta quay lại dãy nhị phân không có hai chữ số một kề nhau, nhưng đổi ngôn ngữ mô tả. Hai trạng thái kết thúc bằng không và kết thúc bằng một được đặt thành một vectơ. Các phép cộng tạo ra trạng thái mới có thể viết bằng một ma trận hai nhân hai. Việc nhân ma trận ở đây không phải hình thức phức tạp vô cớ; nó ghi đúng những mũi tên đã có trong sơ đồ trạng thái.'),
 ('Ma trận chuyển của điều kiện cấm 11', ('Sang trạng thái 0 từ 0 và 1', 'Sang trạng thái 1 chỉ từ 0', 'Hệ số ma trận là số cung hợp lệ'), 'Mỗi phần tử ma trận mang ý nghĩa đếm.', 'M=mat(1,1;1,0)', 'Nếu viết các trạng thái theo thứ tự kết thúc bằng không rồi bằng một, hàng đầu của ma trận có hai hệ số một, vì đều có thể thêm không. Hàng thứ hai có một và không, vì chỉ được thêm một khi trạng thái cũ kết thúc bằng không. Phần tử bằng không thể hiện trực tiếp cung cấm một nối một. Học sinh có thể so sánh ma trận với đồ thị bên cạnh để thấy mỗi con số xuất phát từ một quy tắc hợp lệ cụ thể.'),
 ('Lũy thừa ma trận là nhiều bước', ('Một bước: nhân với M', 'n bước: nhân với M mũ n', 'Có thể bình phương nhanh để tính n lớn'), 'Ma trận nén toàn bộ truy hồi.', 'v_n=M^n v_0', 'Sau hai bước, ta nhân M hai lần; sau n bước là lũy thừa thứ n của M. Ma trận lũy thừa gộp tất cả những chuỗi chuyển trạng thái qua nhiều tầng thời gian. Nếu n rất lớn, chẳng hạn một triệu, ta không cần lặp từng bước. Thuật toán bình phương nhanh chỉ cần số phép nhân ma trận tăng theo logarit của n. Đây là lý do mô hình ma trận đặc biệt hữu ích trong các bài toán tổ hợp với độ dài rất lớn.'),
 ('Điều kiện xếp trên vòng tròn', ('Vị trí cuối cũng kề vị trí đầu', 'Đếm chu trình trạng thái khép kín', 'Sử dụng tổng các phần tử đường chéo'), 'Điều kiện vòng cần khép trạng thái đầu cuối.', 'N_n=tr(M^n)', 'Một chi tiết làm bài toán khó hơn là xếp các chữ số quanh một vòng tròn có đánh dấu vị trí, tức các vị trí được phân biệt. Lúc này vị trí cuối kề với vị trí đầu, nên dãy tránh một một trên hàng thẳng chưa đủ. Có thể mô tả một cấu hình hợp lệ bằng một chu trình dài n trên đồ thị trạng thái. Số chu trình bắt đầu và kết thúc tại cùng trạng thái được ghi trên đường chéo của ma trận lũy thừa, nên ta lấy vết ma trận.'),
 ('Vòng tám vị trí có 47 cách', ('Ma trận M có hai trạng thái', 'Tính lũy thừa M mũ tám', 'Lấy vết bằng 47'), 'Không đồng nhất chu trình với hoán vị quay.', 'tr(M^8)=47', 'Ta áp dụng phép nhân ma trận tới bậc tám. Tổng hai phần tử trên đường chéo bằng bốn mươi bảy. Đây là số dãy nhị phân trên tám vị trí được đánh số quanh vòng, sao cho không có hai số một kề nhau, kể cả cặp ở hai đầu. Xin lưu ý rất quan trọng: ta chưa chia cho tám để gộp các cấu hình khác nhau bởi phép quay. Nếu coi phép quay là cùng một cách, bài toán đã trở thành đếm quỹ đạo và cần xử lý riêng.'),
 ('Kiểm tra bằng cách chọn các vị trí 1', ('Có thể đếm theo số chữ số 1', 'Không đặt hai vị trí 1 kề trên vòng', 'Cộng các mức k hợp lệ'), 'Kiểm tra độc lập giúp tin vào ma trận.', 'N_8=1+8+20+16+2=47', 'Một cách kiểm tra khác là chia theo số lượng chữ số một. Với tám vị trí quanh vòng và không cho phép hai vị trí một kề nhau, số cách tương ứng với không, một, hai, ba, bốn chữ số một lần lượt là một, tám, hai mươi, mười sáu và hai. Tổng cộng được bốn mươi bảy. Kết quả trùng với vết của ma trận M mũ tám. Sự trùng khớp này chứng tỏ công thức ma trận thật sự đếm các cấu hình cần tìm.'),
])

add('capstone', [
 ('Bài toán Olympic ba điều kiện', ('Dãy nhị phân dài đúng 10', 'Có đúng bốn chữ số 1', 'Tránh 101 và kết thúc bằng 0'), 'Mỗi điều kiện cần thông tin trạng thái phù hợp.', 'N=48', 'Bài toán cuối cùng kết hợp ba ràng buộc xuất hiện ở nhiều kỹ thuật trước đó. Ta cần đếm các dãy nhị phân dài mười, chứa đúng bốn chữ số một, không xuất hiện mẫu một không một và có chữ số cuối bằng không. Nếu chỉ dùng một truy hồi Fibonacci hoặc chỉ lấy một hệ số tổ hợp thì chưa đủ. Ta phải mô tả được đồng thời độ dài, số chữ số một đã dùng và trạng thái của máy tránh mẫu.'),
 ('Thiết kế trạng thái ba chiều', ('i: đã điền bao nhiêu vị trí', 'k: đã dùng bao nhiêu chữ số 1', 'q: hậu tố liên quan tới 101'), 'Đủ thông tin để ra quyết định kế tiếp.', 'dp[i,k,q]', 'Ta đặt dp của i, k và q là số tiền tố hợp lệ có i chữ số, trong đó có đúng k chữ số một, và máy tránh mẫu đang ở trạng thái q. Hai tiền tố khác nhau cùng có ba thông số ấy sẽ có cùng những lựa chọn hợp lệ ở bước tiếp theo. Bởi vậy chúng có thể được gộp số lượng vào một ô. Đây chính là tiêu chuẩn quan trọng nhất của thiết kế quy hoạch động: trạng thái phải ghi đủ thông tin, nhưng không cần giữ phần lịch sử thừa.'),
 ('Chuyển khi thêm số không', ('Độ dài tăng thêm một', 'Số lượng chữ số 1 không đổi', 'Máy chuyển theo cung ghi 0'), 'Cập nhật chỉ dọc cung hợp lệ.', 'dp[i+1,k,q_0]+=dp[i,k,q]', 'Nếu thêm chữ số không, độ dài mới tăng thêm một nhưng số chữ số một đã dùng vẫn giữ nguyên. Ta nhìn vào máy trạng thái để biết q mới là gì, sau đó cộng số cách vào ô tương ứng. Nếu mẫu cấm chưa hình thành, bước chuyển được giữ lại. Màn hình sẽ làm nổi bật các cung mang nhãn không, đồng thời đổi vị trí ô DP đang sáng. Chỉ một công thức cập nhật đơn giản có thể xử lý rất nhiều tiền tố.'),
 ('Chuyển khi thêm số một', ('Độ dài tăng một, k tăng một', 'Bỏ cung tạo mẫu 101', 'Không cho k vượt quá bốn'), 'Ràng buộc đếm và mẫu cấm làm việc đồng thời.', 'dp[i+1,k+1,q_1]+=dp[i,k,q]', 'Nếu chữ số được thêm là một, bộ đếm k tăng lên một. Tuy nhiên, không phải từ trạng thái nào ta cũng được thêm một. Từ q hai, thao tác ấy lập tức tạo mẫu một không một và phải bị cấm. Ngoài ra, nếu đã dùng đủ bốn chữ số một thì không được thêm một nữa. Như vậy hai loại điều kiện độc lập đã được đưa vào đúng bước chuyển, giúp loại phương án sai sớm thay vì tạo rồi kiểm tra ở cuối.'),
 ('Điều kiện cuối bằng không', ('Chỉ đọc lớp i bằng mười', 'Giữ các ô k bằng bốn', 'Lấy những đường có bước cuối là 0'), 'Trạng thái kết thúc quyết định kết quả.', 'N=sum_q dp_(10,4,q,0)', 'Sau khi điền xong vị trí thứ mười, ta chỉ lấy những trạng thái có đúng bốn chữ số một. Nhưng bài toán còn đòi hỏi chữ số cuối là không, vì thế cần lọc thêm theo bước chuyển cuối hoặc lưu thêm một cờ cho ký tự cuối. Có thể làm điều đó ngay khi cập nhật lớp cuối cùng. Những trường hợp đúng mẫu và đúng số một nhưng kết thúc bằng một vẫn phải bị loại. Đây là điểm học sinh thường quên khi ghép nhiều điều kiện.'),
 ('Kết quả và hai cách kiểm chứng', ('Thuật toán đếm được 48 dãy', 'Duyệt toàn bộ 2 mũ 10 dãy để đối chiếu', 'Kết luận về thiết kế trạng thái'), 'Quy hoạch động là phép đếm có tổ chức.', 'N=48', 'Bảng quy hoạch động cho đáp số bốn mươi tám. Để kiểm tra độc lập, ta có thể liệt kê toàn bộ một nghìn không trăm hai mươi bốn dãy nhị phân dài mười, rồi lần lượt lọc điều kiện có bốn số một, không chứa mẫu một không một và kết thúc bằng không. Chương trình trực tiếp cũng thu được bốn mươi tám. Khép lại tập này, điều quan trọng nhất không phải một con số, mà là quy trình: nhận diện thông tin cần nhớ, thiết kế trạng thái, mô tả bước chuyển và kiểm tra điều kiện kết thúc.'),
])


def validate():
    assert len(CHAPTERS)==8 and len(BEATS)==48 and len(FORMULAS)==48
    assert len(set(b.narration for b in BEATS))==48
    assert [BEATS[i].section for i in range(0,48,6)]==[x[0] for x in CHAPTERS]
    for i,b in enumerate(BEATS):
        assert b.state==i%6 and len(b.lines)==3
        assert len(b.narration.split())>=50, (i,len(b.narration.split()))
        assert b.formula in FORMULAS
    assert sum(b.min_seconds for b in BEATS)>=1200
    assert grid_table(4,3)[4][3]==paths_bruteforce(4,3)==comb(7,3)==35
    assert grid_table(4,3,{(2,1)})[4][3]==paths_bruteforce(4,3,{(2,1)})==17
    assert 35-comb(3,1)*comb(4,2)==17
    for n in range(12):assert tilings(n)==len(tilings_direct(n))
    for n in range(14):assert sum(no11_states(n))==no11_bruteforce(n)
    for n in range(1,13):assert pattern_dp(n)==pattern_bruteforce(n)
    assert pattern_dp(6)==37
    for n in range(1,6):
        assert bitmask_derangements(n)==sum(all(i!=p[i] for i in range(n)) for p in permutations(range(n)))
    assert bitmask_derangements(4)==9
    for n in range(1,11):assert circular_no11(n)==circular_no11_direct(n)
    assert circular_no11(8)==47
    assert pattern_dp(10,ones=4,last=0)==pattern_bruteforce(10,ones=4,last=0)==48
    return True

if __name__=='__main__':
    print('COMB22_VALID',validate(),'words',sum(len(b.narration.split()) for b in BEATS))