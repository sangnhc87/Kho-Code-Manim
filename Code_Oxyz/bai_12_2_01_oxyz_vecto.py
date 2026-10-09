#!/usr/bin/env python3
"""Bài 12.2.01 — Oxyz, vectơ, tích vô hướng, tích có hướng.
GitHub Actions: video=bai120201; operation=kiem-tra-hinh hoặc render-video.
Không lưu MP4 trong repo, không mở trình phát. --check không cần Manim.
Mỗi câu hỏi có lời giải, lời giảng tiếng Việt, phụ đề và chương MP4.
Tích có hướng là phần mở rộng: học sau khi hiểu vectơ và tích vô hướng.
"""
import os,sys,json,math,hashlib,asyncio,subprocess,textwrap,shutil,zipfile
from pathlib import Path
TEN_THAY='Thầy Nguyễn Văn Sang'
GIONG_DOC='vi-VN-NamMinhNeural'
TOC_DO_DOC='-5%'
CHE_DO='final'
CHON_BAI=[]
# Chế độ Colab/Codespaces nhẹ: chỉ log ngắn theo chương; xong bấm nút tải MP4.
# Không nhúng video, không tự phát hoặc tự tải; giữ chất lượng CHE_DO.
CHI_CHAY_TREN_CLOUD=True
MANIM_VERSION='0.19.0'
PRESETS={'preview':(854,480,15),'standard':(1280,720,24),'final':(1920,1080,30)}


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a):return math.sqrt(dot(a,a))
def T(text,voice=None,pause=0):return {'kind':'text','text':text,'voice':voice or text,'pause':pause}
def M(tex,voice,gold=False):return {'kind':'math','text':tex,'voice':voice,'gold':gold}
def P(title,*rows,pose='base'):return {'title':title,'rows':list(rows),'action':pose}
def model(points,vectors=(),edges=(),faces=(),poses=('base',),**kw):
    return {'points':points,'vectors':list(vectors),'edges':list(edges),'faces':list(faces),'poses':list(poses),**kw}
def chapter(id,title,visual,*pages):return {'id':id,'title':title,'model':visual,'pages':list(pages)}

def build_lessons():
    lessons = [
chapter('C01','Từ hình không gian đến bộ ba tọa độ',
 model({'O':[0,0,0],'M':[3,2,3],'H':[3,2,0],'X':[3,0,0],'Y':[0,2,0],'Z':[0,0,3]},
       vectors=[['O','M','gold']],edges=[['M','H','dash'],['H','X','dash'],['H','Y','dash'],['M','Z','dash']],
       poses=('base','components'),components='M'),
 P('Lộ trình tự học',
   T('Nhìn hình → hiểu bản chất → tính toán → tự giải.', 'Chào các em. Đây là bài đầu tiên của chuyên đề tọa độ không gian. Ta sẽ học hệ trục, tọa độ điểm và vectơ, tích vô hướng, rồi mở rộng đến tích có hướng. Mỗi ví dụ đều có lời giải. Các em chưa cần biết phương trình đường thẳng, mặt phẳng hay mặt cầu.'),
   T('Dừng video khi có câu hỏi; xem lời giải sau.', 'Khi gặp bài tập, hãy dừng video, viết dữ kiện và thử làm. Khi xem lời giải, đối chiếu cả cách lập luận, không chỉ kết quả. Màu xanh biểu diễn vectơ thứ nhất, màu ngọc biểu diễn vectơ thứ hai, màu vàng nhấn mạnh kết quả.'),
   T('Hình phối cảnh không bảo toàn góc trên màn hình.', 'Hình bên trái là mô hình ba chiều được chiếu lên màn hình. Hai đường vuông góc trong không gian có thể không trông vuông góc trên ảnh. Ta kiểm chứng bằng mô hình toán học và ký hiệu góc vuông, không đo góc trực tiếp trên màn hình.')),
 P('Hệ trục vuông góc và cùng đơn vị',
   M(r'Ox\perp Oy,\quad Oy\perp Oz,\quad Oz\perp Ox', 'Ba trục tọa độ đôi một vuông góc, cùng gốc O và cùng đơn vị độ dài. Mô hình trong video cũng dùng cùng một tỉ lệ trên cả ba trục.'),
   M(r'\vec i=(1;0;0),\ \vec j=(0;1;0),\ \vec k=(0;0;1)', 'Vectơ i, j, k là ba vectơ đơn vị theo chiều dương của các trục x, y, z. Trong phần tích có hướng, ta dùng hệ trục thuận, theo quy tắc bàn tay phải.'),
   M(r'M(x;y;z)\iff\overrightarrow{OM}=x\vec i+y\vec j+z\vec k', 'Tọa độ điểm M chính là ba hệ số của vectơ O M theo ba vectơ đơn vị. Đọc x trước, y sau, z cuối. Tọa độ có dấu, không phải lúc nào cũng là độ dài dương.',True),pose='components'),
 P('Ví dụ 1 · Đọc tọa độ và hình chiếu',
   M(r'M(3;2;3)', 'Điểm M có tọa độ ba, hai, ba. Từ gốc, đi ba đơn vị theo chiều dương x, hai đơn vị theo chiều dương y, rồi ba đơn vị theo chiều dương z.'),
   M(r'H_{Oxy}=(3;2;0),\quad H_{Ox}=(3;0;0)', 'Hình chiếu vuông góc lên mặt phẳng tọa độ O x y giữ x và y, cho z bằng không. Hình chiếu lên trục O x giữ x, cho y và z bằng không. Ta đang dùng hình học của hệ trục, chưa cần phương trình mặt phẳng.'),
   M(r'H_{Oyz}=(0;2;3),\quad H_{Oxz}=(3;0;3)', 'Tương tự, lên O y z thì cho x bằng không. Lên O x z thì cho y bằng không. Em hãy tự chỉ vị trí hai hình chiếu còn lại trên hình.',True),pose='components')),
chapter('C02','Vectơ: hướng, độ dài và phép trừ tọa độ',
 model({'O':[0,0,0],'A':[1,-1,2],'B':[4,1,3],'U':[3,2,1]},vectors=[['A','B','blue'],['O','U','cyan']],edges=[['O','A','dash'],['O','B','dash']],poses=('base','components'),components='U'),
 P('Một vectơ có thể tịnh tiến',
   M(r'\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}', 'Theo quy tắc ba điểm, O A cộng A B bằng O B. Vì thế A B bằng O B trừ O A. Hai vectơ bằng nhau khi cùng hướng và cùng độ dài; không cần cùng điểm đặt.'),
   M(r'A(x_A;y_A;z_A),\quad B(x_B;y_B;z_B)', 'Ghi rõ tọa độ điểm đầu A và điểm cuối B trước khi trừ.'),
   M(r'\overrightarrow{AB}=(x_B-x_A;y_B-y_A;z_B-z_A)', 'Tọa độ vectơ bằng tọa độ điểm cuối trừ tọa độ điểm đầu. Cả ba thành phần đều theo cùng thứ tự này.',True)),
 P('Ví dụ 2 · Hai chiều của đoạn thẳng',
   M(r'A(1;-1;2),\quad B(4;1;3)', 'Cho A một, âm một, hai; B bốn, một, ba. Tính vectơ A B, vectơ B A và độ dài A B. Hãy dừng video để làm.',gold=False),
   M(r'\overrightarrow{AB}=(4-1;1-(-1);3-2)=(3;2;1)', 'Lấy B trừ A. Thành phần y là một trừ âm một, bằng hai, không phải bằng không.'),
   M(r'\overrightarrow{BA}=(-3;-2;-1)=-\overrightarrow{AB}', 'Đổi chiều đoạn thẳng làm đổi dấu tất cả các thành phần.'),
   M(r'AB=\sqrt{3^2+2^2+1^2}=\sqrt{14}', 'Độ dài là căn tổng bình phương ba thành phần, suy ra căn mười bốn. Hai vectơ ngược chiều vẫn có cùng độ dài.',True)),
 P('Phân biệt điểm và vectơ',
   T('Điểm là vị trí; vectơ là độ dời có hướng.', 'Cặp hình bên trái biểu diễn cùng một độ dời ba, hai, một. Mũi tên A B và mũi tên O U bằng nhau, dù đặt ở hai nơi khác nhau. Đừng biến tọa độ một điểm thành một vectơ mà quên nói vectơ từ đâu đến đâu.'),
   M(r'\vec u=(a;b;c),\quad |\vec u|=\sqrt{a^2+b^2+c^2}', 'Công thức độ dài áp dụng cho mọi vectơ trong hệ trục vuông góc cùng đơn vị.'),
   M(r'|\vec u|=0\iff\vec u=\vec0', 'Vectơ không là vectơ có độ dài bằng không. Nó không có hướng xác định. Đây là điều kiện cần nhớ khi tính góc hoặc xét cùng phương.',True),pose='components')),
chapter('C03','Cộng vectơ, nhân số và quy tắc hình bình hành',
 model({'O':[0,0,0],'U':[3,0,1],'V':[0,2,1],'S':[3,2,2]},vectors=[['O','U','blue'],['O','V','cyan'],['U','S','cyan'],['O','S','gold']],edges=[['V','S','solid']],faces=[['O','U','S','V']],poses=('base','sum','parallelogram'),aliases={'parallelogram':{'O':'A','U':'B','V':'D','S':'C'}}),
 P('Cộng và nhân theo từng thành phần',
   M(r'\vec u=(a;b;c),\quad\vec v=(d;e;f)', 'Hai vectơ có ba thành phần. Phép cộng được thực hiện độc lập trên từng trục.'),
   M(r'\vec u+\vec v=(a+d;b+e;c+f)', 'Cộng x với x, y với y, z với z. Trong hình, ghép đuôi vectơ thứ hai vào đầu vectơ thứ nhất; vectơ tổng đi từ điểm xuất phát đến điểm kết thúc.',True),
   M(r'\lambda\vec u=(\lambda a;\lambda b;\lambda c)', 'Nhân số lambda vào tất cả thành phần. Nếu lambda dương thì giữ chiều, nếu âm thì ngược chiều; độ dài được nhân với trị tuyệt đối của lambda.'),pose='sum'),
 P('Ví dụ 3 · Tổ hợp tuyến tính',
   M(r'\vec u=(3;0;1),\quad\vec v=(0;2;1)', 'Với hai vectơ trên hình, hãy tính tổng, hiệu và hai u trừ ba v.'),
   M(r'\vec u+\vec v=(3;2;2),\quad\vec u-\vec v=(3;-2;0)', 'Tổng là ba, hai, hai. Hiệu là ba, âm hai, không. Hiệu không phải độ dài trừ độ dài.'),
   M(r'2\vec u-3\vec v=(6;0;2)-(0;6;3)=(6;-6;-1)', 'Nhân từng vectơ với hệ số trước, rồi mới trừ. Kết quả sáu, âm sáu, âm một.',True),pose='sum'),
 P('Ví dụ 4 · Tìm đỉnh hình bình hành',
   M(r'A(0;0;0),\ B(3;0;1),\ D(0;2;1)', 'Cho ba đỉnh A, B, D. Tìm C để A B C D, đúng theo thứ tự đó, là hình bình hành.'),
   M(r'\overrightarrow{AC}=\overrightarrow{AB}+\overrightarrow{AD}', 'Đường chéo xuất phát từ A bằng tổng hai cạnh xuất phát từ A.'),
   M(r'C=B+D-A=(3;2;2)', 'Theo từng tọa độ, C bằng B cộng D trừ A, được ba, hai, hai. Kiểm tra B C bằng A D và D C bằng A B.'),
   T('Thứ tự tên đỉnh quyết định công thức.', 'Nếu đổi thứ tự đỉnh, điểm cần tìm có thể khác. Đừng học công thức ba điểm cộng trừ mà bỏ qua hai cạnh cùng xuất phát từ đâu.'),pose='parallelogram')),
chapter('C04','Trung điểm, trọng tâm và cùng phương',
 model({'A':[0,0,0],'B':[4,0,2],'C':[1,3,1],'I':[2,0,1],'G':[5/3,1,1]},edges=[['A','B','solid'],['B','C','solid'],['C','A','solid'],['C','I','dash']],faces=[['A','B','C']],poses=('base',)),
 P('Ví dụ 5 · Trung điểm và trọng tâm',
   M(r'A(0;0;0),\ B(4;0;2),\ C(1;3;1)', 'Tìm trung điểm I của A B và trọng tâm G của tam giác A B C. Hãy dừng để tự làm.'),
   M(r'\overrightarrow{OI}=\tfrac12(\overrightarrow{OA}+\overrightarrow{OB})', 'Trung điểm có vectơ vị trí là trung bình cộng hai vectơ vị trí hai đầu mút. Do đó tọa độ cũng là trung bình cộng.'),
   M(r'I(2;0;1)', 'Ta được trung điểm I hai, không, một.',True)),
 P('Giải thích công thức trọng tâm',
   M(r'\overrightarrow{CG}=\tfrac23\overrightarrow{CI}', 'Trọng tâm chia trung tuyến theo tỉ lệ C G trên C I bằng hai phần ba.'),
   M(r'\overrightarrow{OG}=\overrightarrow{OC}+\tfrac23(\overrightarrow{OI}-\overrightarrow{OC})', 'Viết O G bằng O C cộng C G, rồi thay C G bằng hai phần ba của O I trừ O C.'),
   M(r'\overrightarrow{OG}=\tfrac13(\overrightarrow{OA}+\overrightarrow{OB}+\overrightarrow{OC})', 'Thay công thức trung điểm, rút gọn được trung bình cộng ba vectơ vị trí.'),
   M(r'G\left(\tfrac53;1;1\right)', 'Vậy G có tọa độ năm phần ba, một, một. Đây là kết quả có lý do từ trung tuyến, không chỉ là công thức thuộc lòng.',True)),
 P('Ví dụ 6 · Cùng phương, không chia cho số không',
   M(r'\vec u=(2;0;-1),\quad\vec v=(m;0;3)', 'Tìm m để u và v cùng phương. Hai vectơ đều khác vectơ không. Thành phần giữa bằng không, nên cách chia tỉ số từng tọa độ dễ dẫn tới phép chia không xác định.'),
   M(r'\vec v=\lambda\vec u\Rightarrow(m;0;3)=(2\lambda;0;-\lambda)', 'Cách chắc chắn là đặt v bằng lambda u.'),
   M(r'-\lambda=3\Rightarrow\lambda=-3\Rightarrow m=-6', 'Từ thành phần z, lambda bằng âm ba. Từ thành phần x, m bằng âm sáu. Hai vectơ ngược hướng.',True),
   M(r'\vec v=-3\vec u\Rightarrow\vec u\times\vec v=\vec0', 'Sau khi học tích có hướng, ta có thêm phép kiểm tra: tích có hướng bằng vectơ không. Hiện tại, hệ thức v bằng âm ba u đã đủ chứng minh.'))),
chapter('C05','Tích vô hướng: từ góc đến tọa độ',
 model({'O':[0,0,0],'U':[3,0,0],'V':[2,2,1],'H':[2,0,0]},vectors=[['O','U','blue'],['O','V','cyan']],edges=[['V','H','dash']],poses=('base','projection'),projection=['U','V'],angle=['U','V']),
 P('Bản chất hình học',
   M(r'\vec u\cdot\vec v=|\vec u|\,|\vec v|\cos\theta', 'Tích vô hướng của hai vectơ khác không bằng tích độ dài nhân cô sin góc giữa chúng. Góc từ không đến một trăm tám mươi độ. Kết quả là một số, có thể dương, bằng không hoặc âm.',True),
   M(r'\theta\in[0;\pi],\quad\vec u\ne\vec0,\ \vec v\ne\vec0', 'Điều kiện khác vectơ không cần để nói đến góc. Tích vô hướng vẫn được định nghĩa nếu một vectơ bằng không, và khi đó bằng không.'),
   M(r'\ell_{\vec u}(\vec v)=|\vec v|\cos\theta,\quad\vec u\cdot\vec v=|\vec u|\ell_{\vec u}(\vec v)', 'Đặt hai vectơ cùng gốc. Hình chiếu có dấu của v lên chiều u bằng độ dài v nhân cô sin góc. Vì thế tích vô hướng đo mức độ hai vectơ cùng chiều theo phương u.',False),pose='projection'),
 P('Vì sao cộng ba tích tọa độ?',
   M(r'\vec i\cdot\vec i=\vec j\cdot\vec j=\vec k\cdot\vec k=1', 'Ba vectơ cơ sở đều có độ dài một, nên tích vô hướng với chính nó bằng một.'),
   M(r'\vec i\cdot\vec j=\vec j\cdot\vec k=\vec k\cdot\vec i=0', 'Ba trục vuông góc, nên mọi tích giữa hai vectơ cơ sở khác nhau đều bằng không.'),
   M(r'\vec u=(a;b;c),\ \vec v=(d;e;f)\Rightarrow\vec u\cdot\vec v=ad+be+cf', 'Khai triển bằng tính phân phối. Các tích chéo đều bằng không, chỉ còn a d cộng b e cộng c f.',True)),
 P('Các tính chất dùng khi biến đổi',
   M(r'\vec u\cdot\vec v=\vec v\cdot\vec u', 'Tích vô hướng có tính giao hoán. Đổi thứ tự hai vectơ vẫn giữ nguyên số kết quả.'),
   M(r'\vec u\cdot(\vec v+\vec w)=\vec u\cdot\vec v+\vec u\cdot\vec w', 'Tích vô hướng phân phối đối với phép cộng. Nhờ đó ta khai triển bình phương độ dài tổng và hiệu.'),
   M(r'(\lambda\vec u)\cdot\vec v=\lambda(\vec u\cdot\vec v),\quad\vec u\cdot\vec u=|\vec u|^2', 'Hệ số số thực có thể đưa ra ngoài tích. Tích một vectơ với chính nó bằng bình phương độ dài.',True)),
 P('Công cụ tính góc và vuông góc',
   M(r'\cos\theta=\dfrac{ad+be+cf}{\sqrt{a^2+b^2+c^2}\sqrt{d^2+e^2+f^2}}', 'Chia tích vô hướng cho tích hai độ dài để tính cô sin góc. Kiểm tra hai mẫu số khác không trước khi dùng.'),
   M(r'\vec u,\vec v\ne\vec0:\quad\vec u\perp\vec v\iff\vec u\cdot\vec v=0', 'Với hai vectơ khác không, vuông góc khi và chỉ khi tích vô hướng bằng không.'),
   T('Dương: góc nhọn. Âm: góc tù. Không: góc vuông.', 'Dấu của tích vô hướng cho biết góc nhọn, tù hay vuông. Khi góc bằng không hoặc một trăm tám mươi độ, hai vectơ cùng hoặc ngược hướng.'))),
chapter('C06','Tính góc và giải điều kiện vuông góc',
 model({'O':[0,0,0],'U':[1,1,0],'V':[1,0,1],'W':[-1,0,-1]},vectors=[['O','U','blue'],['O','V','cyan']],poses=('base','obtuse'),alternate=['O','W'],angle=['U','V']),
 P('Ví dụ 7 · Một góc đẹp trong không gian',
   M(r'\vec u=(1;1;0),\quad\vec v=(1;0;1)', 'Tính góc giữa u một, một, không và v một, không, một. Hãy tính tích vô hướng và hai độ dài riêng biệt.'),
   M(r'\vec u\cdot\vec v=1,\quad|\vec u|=|\vec v|=\sqrt2', 'Tích vô hướng bằng một. Hai độ dài đều bằng căn hai.'),
   M(r'\cos\theta=\frac1{\sqrt2\sqrt2}=\frac12\Rightarrow\theta=60^\circ', 'Cô sin góc bằng một phần hai, nên góc giữa hai vectơ bằng sáu mươi độ. Hình chiếu trên màn hình không nhất thiết tạo góc sáu mươi độ.',True)),
 P('Đổi chiều một vectơ thì góc thay đổi',
   M(r'\vec w=-\vec v=(-1;0;-1)', 'Giữ u, đảo chiều v thành w. Ta sẽ nhìn thấy mũi tên vàng theo chiều đối diện.'),
   M(r'\vec u\cdot\vec w=-1\Rightarrow\cos\varphi=-\tfrac12', 'Tích vô hướng đổi dấu thành âm một, cô sin bằng âm một phần hai.'),
   M(r'\varphi=120^\circ', 'Góc mới bằng một trăm hai mươi độ, không phải sáu mươi. Không lấy trị tuyệt đối tích vô hướng khi đề hỏi góc giữa hai vectơ.',True),pose='obtuse'),
 P('Ví dụ 8 · Tìm tham số',
   M(r'\vec a=(m;2;-1),\quad\vec b=(1;-1;2)', 'Tìm m để a và b vuông góc. Cả hai đều khác vectơ không với mọi m vì a có thành phần thứ hai bằng hai, b có thành phần thứ nhất bằng một.'),
   M(r'\vec a\cdot\vec b=m-2-2=m-4', 'Nhân các thành phần tương ứng rồi cộng, được m trừ bốn.'),
   M(r'\vec a\perp\vec b\iff m-4=0\iff m=4', 'Điều kiện vuông góc cho m bằng bốn. Thay lại, bốn trừ hai trừ hai bằng không.',True))),
chapter('C07','Tích vô hướng giải tam giác và độ dài',
 model({'A':[0,0,0],'B':[1,1,0],'C':[1,0,1]},edges=[['A','B','solid'],['A','C','solid'],['B','C','solid']],faces=[['A','B','C']],vectors=[['A','B','blue'],['A','C','cyan']],poses=('base',),angle=['B','C']),
 P('Độ dài tổng: phải giữ hạng chéo',
   M(r'|\vec u+\vec v|^2=(\vec u+\vec v)\cdot(\vec u+\vec v)', 'Bình phương độ dài bằng tích vô hướng của vectơ với chính nó. Khai triển như bình phương một tổng.'),
   M(r'|\vec u+\vec v|^2=|\vec u|^2+2\vec u\cdot\vec v+|\vec v|^2', 'Hạng chéo bằng hai lần tích vô hướng. Chỉ khi vuông góc, hạng chéo mới bằng không.',True),
   M(r'|\vec u-\vec v|^2=|\vec u|^2-2\vec u\cdot\vec v+|\vec v|^2', 'Với hiệu, hạng chéo đổi sang dấu trừ. Đây là cầu nối giữa vectơ và định lý cô sin.')),
 P('Ví dụ 9 · Nhận dạng tam giác',
   M(r'A(0;0;0),\quad B(1;1;0),\quad C(1;0;1)', 'Xét tam giác A B C. Hãy tính ba cạnh và góc B A C. Góc tại A phải dùng hai vectơ cùng xuất phát từ A.'),
   M(r'\overrightarrow{AB}=(1;1;0),\quad\overrightarrow{AC}=(1;0;1)', 'Hai vectơ cạnh tại A chính là u và v của ví dụ vừa rồi.'),
   M(r'AB=AC=\sqrt2,\quad\overrightarrow{BC}=(0;-1;1)\Rightarrow BC=\sqrt2', 'Ba cạnh đều bằng căn hai. Vì ba điểm không thẳng hàng, đây là tam giác đều.'),
   M(r'\cos\widehat{BAC}=\frac{1}{2}\Rightarrow\widehat{BAC}=60^\circ', 'Tích vô hướng của A B và A C bằng một, tích độ dài bằng hai. Góc tại A bằng sáu mươi độ, khớp với kết luận tam giác đều.',True)),
 P('Ví dụ 10 · Suy ra độ dài không cần tọa độ',
   M(r'|\vec u|=3,\quad|\vec v|=2,\quad\theta=60^\circ', 'Cho u dài ba, v dài hai, góc sáu mươi độ. Tính độ dài hai u trừ v. Bài này không cần gán tọa độ.'),
   M(r'\vec u\cdot\vec v=3\cdot2\cdot\tfrac12=3', 'Tích vô hướng bằng ba.'),
   M(r'\begin{aligned}|2\vec u-\vec v|^2&=4|\vec u|^2-4\vec u\cdot\vec v+|\vec v|^2\\&=36-12+4=28\end{aligned}', 'Khai triển đúng hệ số: bốn lần bình phương u, trừ bốn lần tích vô hướng, cộng bình phương v. Bằng ba mươi sáu trừ mười hai cộng bốn, được hai mươi tám.'),
   M(r'|2\vec u-\vec v|=2\sqrt7', 'Độ dài không âm, nên lấy căn dương. Kết quả hai căn bảy.',True))),
chapter('C08','Hình chiếu vectơ và khoảng cách sơ cấp',
 model({'O':[0,0,0],'U':[1,1,0],'V':[3,1,2],'H':[2,2,0]},vectors=[['O','U','blue'],['O','V','cyan'],['O','H','gold']],edges=[['V','H','dash']],poses=('base','projection'),projection=['U','V']),
 P('Ví dụ 11 · Tìm chân chiếu bằng tích vô hướng',
   M(r'\vec u=(1;1;0),\quad\overrightarrow{OV}=(3;1;2)', 'Tìm hình chiếu H của V lên đường qua O có hướng u. Ta chỉ dùng hệ thức vectơ, chưa học phương trình đường thẳng.'),
   M(r'\overrightarrow{OH}=t\vec u,\quad\overrightarrow{HV}=\overrightarrow{OV}-t\vec u', 'Vì H nằm theo phương u từ O, đặt O H bằng t u. Vectơ H V bằng O V trừ O H.'),
   M(r'\overrightarrow{HV}\cdot\vec u=0\Rightarrow4-2t=0\Rightarrow t=2', 'H V vuông góc u. Nhân vô hướng cho phương trình bốn trừ hai t bằng không, suy ra t bằng hai.'),
   M(r'H(2;2;0),\quad HV=\sqrt{1^2+(-1)^2+2^2}=\sqrt6', 'Chân chiếu H hai, hai, không. Vectơ H V một, âm một, hai, nên khoảng cách V H bằng căn sáu.',True),pose='projection'),
 P('Vì sao chân chiếu cho khoảng cách ngắn nhất?',
   M(r'\overrightarrow{OQ}=s\vec u:\quad VQ^2=VH^2+HQ^2\ge VH^2', 'Với bất kỳ Q trên phương u qua O, tam giác V H Q vuông ở H. Định lý Py ta go cho V Q bình phương bằng V H bình phương cộng H Q bình phương. Vì thế khoảng cách nhỏ nhất tại H.'),
   M(r'\operatorname{proj}_{\vec u}\vec v=\frac{\vec v\cdot\vec u}{|\vec u|^2}\vec u\quad(\vec u\ne\vec0)', 'Công thức tổng quát của hình chiếu vectơ: tích vô hướng chia bình phương độ dài hướng chiếu, rồi nhân với hướng chiếu. Kết quả là một vectơ, khác với hình chiếu có dấu là một số.',True),
   T('Nếu hệ số âm, chân chiếu ở phía ngược chiều.', 'Hệ số t có thể âm. Khi đó chân chiếu ở phía ngược chiều dương của u. Không thay t bằng trị tuyệt đối; làm vậy sẽ dời chân chiếu sang một điểm khác.'),pose='projection')),
chapter('C09','Mở rộng: tích có hướng và quy tắc bàn tay phải',
 model({'O':[0,0,0],'U':[2,0,0],'V':[0,2,0],'S':[2,2,0],'N':[0,0,3],'R':[0,0,-3]},vectors=[['O','U','blue'],['O','V','cyan']],edges=[['U','S','solid'],['V','S','solid']],faces=[['O','U','S','V']],poses=('base','normal','reverse'),normal=['O','N'],reverse=['O','R'],angle=['U','V']),
 P('Một phép toán trả về vectơ',
   T('Tích vô hướng → số. Tích có hướng → vectơ.', 'Từ đây là phần mở rộng. Tích có hướng của u và v là một vectơ vuông góc cả hai vectơ. Ta dùng ký hiệu u nhân có hướng v. Đừng nhầm với tích vô hướng, vốn trả về một số.'),
   M(r'\vec n=\vec u\times\vec v,\quad\vec n\perp\vec u,\quad\vec n\perp\vec v', 'Khi u và v không cùng phương, tích có hướng khác vectơ không, vuông góc với cả hai. Hình minh họa mũi tên vàng có hướng pháp tuyến, đã thu ngắn để bố cục rõ; độ lớn thật luôn tính bằng công thức.'),
   M(r'|\vec u\times\vec v|=|\vec u|\,|\vec v|\sin\theta', 'Độ lớn tích có hướng bằng tích hai độ dài nhân sin góc, cũng chính là diện tích hình bình hành dựng trên hai vectơ.',True),pose='normal'),
 P('Hướng do thứ tự quyết định',
   M(r'\vec i\times\vec j=\vec k,\quad\vec j\times\vec k=\vec i,\quad\vec k\times\vec i=\vec j', 'Trong hệ trục thuận, thứ tự tuần hoàn i, j, k cho kết quả dương. Quy tắc bàn tay phải: cuộn các ngón từ vectơ thứ nhất sang vectơ thứ hai theo góc nhỏ hơn một trăm tám mươi độ, ngón cái chỉ hướng tích có hướng.'),
   M(r'\vec v\times\vec u=-(\vec u\times\vec v)', 'Đổi thứ tự hai vectơ thì đổi hướng kết quả. Trên hình, mũi tên đảo từ phía dương sang phía âm z.',True),
   M(r'\vec u,\vec v\ne\vec0:\quad\vec u\times\vec v=\vec0\iff\vec v=\lambda\vec u', 'Tích có hướng bằng vectơ không khi hai vectơ phụ thuộc tuyến tính. Nếu cả hai khác không, điều đó nghĩa là cùng phương. Nếu có vectơ không, tích cũng bằng không và không có hướng pháp tuyến xác định.'),pose='reverse'),
 P('Công thức tọa độ, chú ý thành phần giữa',
   M(r'\vec u=(a;b;c),\quad\vec v=(d;e;f)', 'Ghi tọa độ theo cùng thứ tự x, y, z.'),
   M(r'\vec u\times\vec v=(bf-ce;\ cd-af;\ ae-bd)', 'Thành phần x bằng b f trừ c e, thành phần y bằng c d trừ a f, thành phần z bằng a e trừ b d. Thành phần giữa rất hay sai dấu.',True),
   M(r'\begin{vmatrix}\vec i&\vec j&\vec k\\a&b&c\\d&e&f\end{vmatrix}', 'Có thể dùng bảng định thức để nhớ, nhưng học sinh chưa học định thức chỉ cần công thức tọa độ và cách kiểm tra vuông góc. Khai triển hàng đầu có dấu cộng, trừ, cộng.'))),
chapter('C10','Tính tích có hướng và kiểm tra bằng hình học',
 model({'O':[0,0,0],'U':[1,2,0],'V':[0,1,2],'S':[1,3,2],'N':[2,-1,.5]},vectors=[['O','U','blue'],['O','V','cyan']],edges=[['U','S','solid'],['V','S','solid']],faces=[['O','U','S','V']],poses=('base','normal'),normal=['O','N']),
 P('Ví dụ 12 · Tính và kiểm chứng',
   M(r'\vec u=(1;2;0),\quad\vec v=(0;1;2)', 'Tính tích có hướng của hai vectơ. Sau đó kiểm tra kết quả có vuông góc cả hai hay không.'),
   M(r'\vec u\times\vec v=(2\cdot2-0\cdot1;0\cdot0-1\cdot2;1\cdot1-2\cdot0)', 'Lần lượt thay vào ba thành phần, chú ý phần y là không trừ hai.'),
   M(r'\vec n=(4;-2;1)', 'Kết quả bốn, âm hai, một.',True),
   M(r'\vec n\cdot\vec u=4-4=0,\quad\vec n\cdot\vec v=-2+2=0', 'Nhân vô hướng với u và v đều bằng không. Hai phép kiểm tra này giúp bắt lỗi dấu hoặc thứ tự.',False),pose='normal'),
 P('Kiểm tra độ lớn độc lập',
   M(r'|\vec n|^2=16+4+1=21', 'Bình phương độ dài kết quả bằng hai mươi mốt.'),
   M(r'|\vec u|^2=5,\quad|\vec v|^2=5,\quad\vec u\cdot\vec v=2', 'Hai vectơ ban đầu đều có bình phương độ dài bằng năm và tích vô hướng bằng hai.'),
   M(r'\begin{aligned}|\vec u\times\vec v|^2&=|\vec u|^2|\vec v|^2-(\vec u\cdot\vec v)^2\\&=25-4=21\end{aligned}', 'Đẳng thức La grăng cho cùng kết quả hai mươi mốt. Nó xuất phát từ sin bình phương cộng cô sin bình phương bằng một. Phép kiểm tra độc lập này còn giúp tính diện tích khi không cần hướng.',True),pose='normal')),
chapter('C11','Diện tích tam giác và thể tích tứ diện',
 model({'A':[0,0,0],'B':[2,0,0],'C':[0,3,0],'D':[1,1,4],'H':[1,1,0],'N':[0,0,2.8]},edges=[['A','B','solid'],['B','C','solid'],['C','A','dash'],['D','A','solid'],['D','B','solid'],['D','C','solid'],['D','H','dash']],faces=[['A','B','C']],poses=('base','normal','volume'),normal=['A','N'],height=['D','H']),
 P('Ví dụ 13 · Diện tích trong không gian',
   M(r'A(0;0;0),\quad B(2;0;0),\quad C(0;3;0)', 'Tính diện tích tam giác A B C bằng tích có hướng. Hai vectơ cạnh phải có chung điểm đầu A.'),
   M(r'\overrightarrow{AB}=(2;0;0),\quad\overrightarrow{AC}=(0;3;0)', 'Hai cạnh theo chiều x và y, độ dài hai và ba.'),
   M(r'\overrightarrow{AB}\times\overrightarrow{AC}=(0;0;6)', 'Tích có hướng hướng dương z và có độ dài sáu. Mũi tên minh họa hướng đã thu ngắn, không dùng để đo độ lớn.'),
   M(r'S_{ABC}=\tfrac12|\overrightarrow{AB}\times\overrightarrow{AC}|=3', 'Diện tích tam giác bằng một nửa diện tích hình bình hành, nên bằng ba đơn vị diện tích.',True),pose='normal'),
 P('Ví dụ 14 · Đáy, chiều cao và thể tích',
   M(r'D(1;1;4),\quad H(1;1;0),\quad DH=4', 'Thêm D một, một, bốn. Đáy A B C nằm trong mặt phẳng tọa độ O x y. H một, một, không là chân chiếu của D, nên chiều cao bằng bốn.'),
   M(r'V_{ABCD}=\tfrac13S_{ABC}\cdot DH=\tfrac13\cdot3\cdot4=4', 'Thể tích tứ diện bằng một phần ba diện tích đáy nhân chiều cao, được bốn.',True),
   M(r'\overrightarrow{AD}=(1;1;4),\quad(\overrightarrow{AB}\times\overrightarrow{AC})\cdot\overrightarrow{AD}=24', 'Tích hỗn hợp bằng tích vô hướng của pháp tuyến đáy với vectơ A D. Sáu nhân bốn bằng hai mươi bốn.'),pose='volume'),
 P('Công thức tổng quát và ý nghĩa hệ số',
   M(r'V_{ABCD}=\frac16\left|(\overrightarrow{AB}\times\overrightarrow{AC})\cdot\overrightarrow{AD}\right|', 'Tổng quát, thể tích tứ diện bằng một phần sáu trị tuyệt đối tích hỗn hợp. Tích hỗn hợp có dấu theo hướng, nhưng thể tích phải không âm.',True),
   T('Hình hộp: hệ số một. Tứ diện: hệ số một phần sáu.', 'Tích có hướng cho diện tích hình bình hành. Nhân với thành phần chiều cao cho thể tích hình hộp. Tam giác đáy chỉ bằng một nửa hình bình hành; khối chóp lại nhân một phần ba. Vì thế tứ diện có hệ số một phần sáu.'),
   M(r'(\overrightarrow{AB}\times\overrightarrow{AC})\cdot\overrightarrow{AD}=0\Rightarrow V=0', 'Nếu tích hỗn hợp bằng không, khối suy biến. Nếu A B C không thẳng hàng thì điều này nói D cùng mặt phẳng với A B C. Không được gọi đó là tứ diện có thể tích dương.'),pose='volume')),
chapter('C12','Bài tổng hợp: diện tích nghiêng và điểm đồng phẳng',
 model({'A':[1,0,1],'B':[2,2,1],'C':[1,1,3],'D':[2,3,3],'N':[3, -1, 1.5]},edges=[['A','B','solid'],['B','D','solid'],['D','C','solid'],['C','A','solid'],['B','C','dash']],faces=[['A','B','D','C']],vectors=[['A','B','blue'],['A','C','cyan']],poses=('base','normal'),normal=['A','N']),
 P('Ví dụ 15 · Diện tích một tam giác nghiêng',
   M(r'A(1;0;1),\quad B(2;2;1),\quad C(1;1;3)', 'Tam giác lần này nghiêng trong không gian. Tính diện tích, sau đó tìm t để D hai, ba, t cùng mặt phẳng với A B C. Không cần biết phương trình mặt phẳng.'),
   M(r'\overrightarrow{AB}=(1;2;0),\quad\overrightarrow{AC}=(0;1;2)', 'Luôn trừ A khỏi B và C. Đây chính là cặp vectơ đã tính ở ví dụ mười hai.'),
   M(r'\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(4;-2;1)', 'Vectơ vuông góc mặt phẳng chứa tam giác là bốn, âm hai, một.'),
   M(r'S_{ABC}=\frac{\sqrt{21}}2', 'Độ dài n bằng căn hai mươi mốt. Chia hai, được diện tích căn hai mươi mốt trên hai.',True),pose='normal'),
 P('Ví dụ 16 · Cùng mặt phẳng bằng tích hỗn hợp',
   M(r'D(2;3;t)\Rightarrow\overrightarrow{AD}=(1;3;t-1)', 'Viết vectơ A D bằng một, ba, t trừ một.'),
   M(r'\vec n\cdot\overrightarrow{AD}=4-6+(t-1)=t-3', 'Lấy tích vô hướng với n, được t trừ ba. Vì tam giác A B C không suy biến, D cùng mặt phẳng khi và chỉ khi tích này bằng không.'),
   M(r't-3=0\Rightarrow t=3', 'Suy ra t bằng ba.',True),
   M(r't=3:\quad\overrightarrow{AD}=\overrightarrow{AB}+\overrightarrow{AC}', 'Kiểm tra lại bằng hình bình hành: một, ba, hai bằng một, hai, không cộng không, một, hai. D chính là đỉnh thứ tư của hình bình hành A B D C, nên chắc chắn đồng phẳng.'))),
chapter('C13','Tự luyện có lời giải · Từ cơ bản đến tổng hợp',
 model({'O':[0,0,0],'A':[1,2,0],'B':[3,0,2],'I':[2,1,1],'U':[1,0,1],'V':[0,2,0],'S':[1,2,1]},edges=[['A','B','solid'],['U','S','solid'],['V','S','solid']],vectors=[['O','U','blue'],['O','V','cyan']],faces=[['O','U','S','V']],poses=('base',)),
 P('Bài 17 · Điểm và vectơ',
   M(r'A(1;2;0),\quad B(3;0;2)', 'Bài tự luyện một. Tính A B, độ dài A B và trung điểm I. Dừng video và làm trong khoảng một phút.',False),
   T('Tự giải trước khi xem bước tiếp theo.', 'Gợi ý: điểm cuối trừ điểm đầu, căn tổng bình phương, rồi trung bình cộng tọa độ.',pause=8)),
 P('Lời giải bài 17',
   M(r'\overrightarrow{AB}=(2;-2;2)', 'Ba trừ một bằng hai, không trừ hai bằng âm hai, hai trừ không bằng hai.'),
   M(r'AB=\sqrt{4+4+4}=2\sqrt3', 'Căn mười hai bằng hai căn ba.'),
   M(r'I\left(\frac{1+3}2;\frac{2+0}2;\frac{0+2}2\right)=(2;1;1)', 'Trung điểm I hai, một, một. Các em có thể kiểm tra vectơ A I bằng vectơ I B.',True)),
 P('Bài 18 · Góc và diện tích',
   M(r'\vec u=(1;0;1),\quad\vec v=(0;2;0)', 'Tính góc giữa u và v, rồi diện tích hình bình hành trên hai vectơ. Hãy dừng video để tự làm.'),
   T('Góc dùng tích vô hướng; diện tích dùng tích có hướng.', 'Trước hết xác định u chấm v, sau đó tính u nhân có hướng v. Không nhầm số với vectơ.',pause=8)),
 P('Lời giải bài 18',
   M(r'\vec u\cdot\vec v=0,\quad|\vec u|=\sqrt2,\quad|\vec v|=2', 'Hai vectơ đều khác không và tích vô hướng bằng không.'),
   M(r'\theta=90^\circ', 'Vậy góc giữa hai vectơ bằng chín mươi độ.'),
   M(r'\vec u\times\vec v=(-2;0;2)\Rightarrow S=2\sqrt2', 'Tích có hướng âm hai, không, hai. Độ lớn bằng hai căn hai, cũng là diện tích hình bình hành. Kiểm tra bằng tích hai cạnh vuông góc: căn hai nhân hai.',True)),
 P('Bài 19 · Công thức tổng quát',
   M(r'|\vec u|=2,\quad|\vec v|=3,\quad\vec u\cdot\vec v=-3', 'Cho độ dài u bằng hai, v bằng ba, tích vô hướng âm ba. Tính góc, độ dài tổng và diện tích tam giác dựng trên hai vectơ. Hãy tự giải rồi xem lời giải.'),
   T('Kiểm tra dấu của góc và hệ số một phần hai.', 'Góc sẽ tù vì tích vô hướng âm. Diện tích tam giác phải bằng một nửa diện tích hình bình hành.',pause=8)),
 P('Lời giải bài 19 · Góc và độ dài',
   M(r'\cos\theta=\frac{-3}{2\cdot3}=-\frac12\Rightarrow\theta=120^\circ', 'Cô sin bằng âm một phần hai, góc một trăm hai mươi độ.'),
   M(r'|\vec u+\vec v|^2=4+9+2(-3)=7', 'Bình phương độ dài tổng bằng bốn cộng chín trừ sáu, được bảy.'),
   M(r'|\vec u+\vec v|=\sqrt7', 'Độ dài tổng bằng căn bảy.',True)),
 P('Lời giải bài 19 · Diện tích',
   M(r'|\vec u\times\vec v|^2=4\cdot9-(-3)^2=27', 'Dùng đẳng thức La grăng: ba mươi sáu trừ chín bằng hai mươi bảy.'),
   M(r'S_{\triangle}=\tfrac12\sqrt{27}=\frac{3\sqrt3}{2}', 'Diện tích tam giác bằng ba căn ba trên hai.',True),
   M(r'\tfrac12\cdot2\cdot3\sin120^\circ=\frac{3\sqrt3}{2}', 'Kiểm tra theo công thức nửa tích hai cạnh nhân sin góc xen giữa, cũng được cùng kết quả.'))),
chapter('C14','Chốt kiến thức và sửa lỗi thường gặp',
 model({'O':[0,0,0],'U':[2,0,0],'V':[0,2,0],'S':[2,2,0],'N':[0,0,2]},vectors=[['O','U','blue'],['O','V','cyan']],edges=[['U','S','solid'],['V','S','solid']],faces=[['O','U','S','V']],poses=('base','normal'),normal=['O','N']),
 P('Sơ đồ lựa chọn công cụ',
   T('Vị trí, trung điểm, trọng tâm → tọa độ.', 'Nếu đề hỏi vị trí điểm, hãy dùng phép trừ tọa độ, trung điểm hoặc trọng tâm. Viết hệ thức vectơ trước để chọn đúng thứ tự điểm.'),
   T('Góc, vuông góc, bình phương độ dài → tích vô hướng.', 'Nếu hỏi góc, vuông góc hoặc bình phương độ dài, ưu tiên tích vô hướng. Nhớ điều kiện khác vectơ không khi tính góc.'),
   T('Pháp tuyến, diện tích, thể tích → tích có hướng.', 'Nếu cần một vectơ vuông góc hai hướng, diện tích hoặc thể tích, dùng tích có hướng rồi tích hỗn hợp. Tích có hướng thuộc phần mở rộng, có thể ôn sau khi phần cơ bản đã chắc.')),
 P('Những lỗi phải tự kiểm tra',
   M(r'\overrightarrow{AB}=B-A,\quad\overrightarrow{BA}=A-B', 'Lỗi đầu tiên là trừ ngược điểm. Luôn nói thành lời: điểm cuối trừ điểm đầu.'),
   M(r'|\vec u+\vec v|^2=|\vec u|^2+|\vec v|^2+2\vec u\cdot\vec v', 'Lỗi thứ hai là cộng độ dài thay vì cộng vectơ. Đẳng thức này không đúng nói chung. Muốn tính độ dài tổng, bình phương rồi dùng tích vô hướng.'),
   M(r'\vec u\cdot\vec v\in\mathbb R,\quad\vec u\times\vec v\in\mathbb R^3', 'Lỗi thứ ba là nhầm kiểu kết quả. Tích vô hướng là số; tích có hướng là vectơ ba thành phần.'),
   M(r'S_\triangle=\tfrac12|\vec u\times\vec v|,\quad V_{\rm tetra}=\tfrac16|(\vec u\times\vec v)\cdot\vec w|', 'Lỗi cuối là quên hệ số một phần hai hoặc một phần sáu, hay quên trị tuyệt đối khi tính thể tích.',True),pose='normal'),
 P('Em đã sẵn sàng cho bài tiếp theo',
   T('Giải thích được công thức bằng hình học.', 'Trước khi chuyển bài, em hãy tự giải thích vì sao tọa độ vectơ là điểm cuối trừ điểm đầu; vì sao tích vô hướng tính góc; vì sao độ lớn tích có hướng là diện tích hình bình hành.'),
   T('Làm lại ba bài tự luyện mà không nhìn lời giải.', 'Làm lại các bài mười bảy, mười tám, mười chín trên giấy. Nếu còn sai dấu, trở lại đúng chương trong mục lục. Video có phụ đề và các chương để em tự học từng phần.'),
   T('Bài 12.2.02: từ vectơ pháp tuyến đến mặt phẳng.', 'Trong bài tiếp theo, ta dùng vectơ pháp tuyến đã hiểu ở đây để xây dựng phương trình mặt phẳng. Cảm ơn các em đã học cùng thầy Nguyễn Văn Sang.')))
]
    variants={
        'C04':{'parallel':model({'O':[0,0,0],'U':[2,0,-1],'V':[-6,0,3]},vectors=[['O','U','blue'],['O','V','cyan']])},
        'C06':{'perp':model({'O':[0,0,0],'U':[4,2,-1],'V':[1,-1,2]},vectors=[['O','U','blue'],['O','V','cyan']],angle=['U','V'])},
        'C07':{'length':model({'O':[0,0,0],'U':[3,0,0],'V':[1,math.sqrt(3),0],'S':[5,-math.sqrt(3),0]},vectors=[['O','U','blue'],['O','V','cyan'],['O','S','gold']],angle=['U','V'])},
        'C13':{
            'points':model({'O':[0,0,0],'A':[1,2,0],'B':[3,0,2],'I':[2,1,1]},edges=[['A','B','solid']]),
            'orthogonal':model({'O':[0,0,0],'U':[1,0,1],'V':[0,2,0],'S':[1,2,1]},vectors=[['O','U','blue'],['O','V','cyan']],edges=[['U','S','solid'],['V','S','solid']],faces=[['O','U','S','V']],angle=['U','V']),
            'obtuse_sum':model({'O':[0,0,0],'U':[2,0,0],'V':[-1.5,3*math.sqrt(3)/2,0],'S':[.5,3*math.sqrt(3)/2,0]},vectors=[['O','U','blue'],['O','V','cyan'],['O','S','gold']],edges=[['U','S','solid'],['V','S','solid']],faces=[['O','U','S','V']],angle=['U','V'])}}
    for lesson in lessons:
        if lesson['id'] in variants:
            lesson['model']['variants']=variants[lesson['id']]
            lesson['model']['poses']+=list(variants[lesson['id']])
    lessons[3]['pages'][-1]['action']='parallel'
    lessons[5]['pages'][-1]['action']='perp'
    lessons[6]['pages'][-1]['action']='length'
    for i,page in enumerate(lessons[12]['pages']):
        page['action']='points' if i<2 else 'orthogonal' if i<4 else 'obtuse_sum'
    return lessons


def validate_math():
    # Numerical checks verify actual geometry, cross-product signs and solved examples.
    assert sub([4,1,3],[1,-1,2])==[3,2,1]
    assert math.isclose(norm([3,2,1]),math.sqrt(14))
    assert dot([1,1,0],[1,0,1])==1
    assert dot([4,2,-1],[1,-1,2])==0
    assert cross([1,2,0],[0,1,2])==[4,-2,1]
    assert cross([2,0,0],[0,3,0])==[0,0,6]
    assert dot(cross([2,0,0],[0,3,0]),[1,1,4])/6==4
    assert dot([4,-2,1],[1,3,2])==0
    assert cross([1,0,1],[0,2,0])==[-2,0,2]
    for u,v in [([1,2,0],[0,1,2]),([1,0,1],[0,2,0]),([2,0,-1],[-6,0,3]),([-2,3,1],[4,-1,2])]:
        n=cross(u,v)
        assert abs(dot(n,u))<1e-10 and abs(dot(n,v))<1e-10
        assert math.isclose(dot(n,n),dot(u,u)*dot(v,v)-dot(u,v)**2,abs_tol=1e-10)
    lessons=build_lessons();assert len({l['id'] for l in lessons})==len(lessons)
    for l in lessons:
        m=l['model'];p=m['points']
        for a,b,col in m['vectors']+m['edges']:assert a in p and b in p and norm(sub(p[b],p[a]))>0
        if 'projection' in m:
            u,v=(p[n] for n in m['projection']);h=[dot(v,u)/dot(u,u)*x for x in u]
            assert abs(dot(sub(v,h),u))<1e-10
        if 'normal' in m:
            a,b=m['normal'];n=sub(p[b],p[a]);u=sub(p[m['vectors'][0][1]],p[m['vectors'][0][0]]) if m['vectors'] else sub(p['B'],p['A'])
            v=sub(p[m['vectors'][1][1]],p[m['vectors'][1][0]]) if m['vectors'] else sub(p['C'],p['A'])
            assert abs(dot(n,u))<1e-9 and abs(dot(n,v))<1e-9,(l['id'],n,u,v)
            assert dot(n,cross(u,v))>0
        for page in l['pages']:
            assert 1<=len(page['rows'])<=4 and page['action'] in m['poses']
            assert all(row['voice'].strip() for row in page['rows'])
    print(f"Kiểm chứng: {len(lessons)} chương, {sum(len(l['pages']) for l in lessons)} trang; 19 ví dụ/bài tập có lời giải; dấu tích có hướng, diện tích, thể tích, chân chiếu hợp lệ.")

SCENE_SOURCE=r'''
from manim import *
import numpy as np
import math,json,textwrap
from pathlib import Path
HERE=Path(__file__).resolve().parent
LESSONS=json.loads((HERE/'lessons.json').read_text(encoding='utf-8'))
SETTINGS=json.loads((HERE/'settings.json').read_text(encoding='utf-8'))
BG='#0B1120';PANEL='#0E1D34';INK='#EDF4FF';MUTED='#7A9ABF'
BLUE='#38BDF8';CYAN='#3ADEC8';GOLD='#FFD700';GREEN='#4ADE80';RED='#FF6B6B'
config.background_color=BG
config.pixel_width=SETTINGS['width'];config.pixel_height=SETTINGS['height'];config.frame_rate=SETTINGS['fps']
TMPL=TexTemplate();TMPL.add_to_preamble(r'\usepackage{amsmath}\usepackage{amssymb}')
def pt(x,y,z=0):return np.array([x,y,z],dtype=float)
def txt(s,size=24,color=INK,bold=False):
    return Text(s,font='DejaVu Sans',font_size=size,color=color,weight='BOLD' if bold else 'NORMAL',disable_ligatures=True)
def mtx(s,size=31,color=INK):return MathTex(s,font_size=size,color=color,tex_template=TMPL)
def fit(m,w,h=None):
    k=min(1,w/max(m.width,1e-9))
    if h is not None:k=min(k,h/max(m.height,1e-9))
    return m.scale(k)
def panel(w,h,center,fill=1):
    return RoundedRectangle(width=w,height=h,corner_radius=.15,fill_color=PANEL,fill_opacity=fill,
        stroke_color=MUTED,stroke_opacity=.23,stroke_width=1.2).move_to(center)

class VectorView:
    """True world geometry; one isotropic scale; screen-fixed labels only.
    Arc sampled in the span of its two vectors, never a screen Circle.
    Orthographic camera makes projected parallelism exact and stable.
    """
    def __init__(self,scene,data,pose='base'):
        self.scene=scene;data=data.get('variants',{}).get(pose,data);self.data=data;self.pose=pose
        self.points={k:np.array(v,dtype=float) for k,v in data['points'].items()}
        self.R=scene.camera.get_rotation_matrix()
        values=list(self.points.values())+[np.zeros(3)]
        cloud=np.array(values);lo=cloud.min(axis=0);hi=cloud.max(axis=0)
        self.axislo=np.minimum(lo-.35,-.5);self.axishi=np.maximum(hi+.55,1.7)
        samples=list(values)
        for a in range(3):
            for t in [self.axislo[a],self.axishi[a]]:
                p=np.zeros(3);p[a]=t;samples.append(p)
        projection=(self.R@np.array(samples).T).T[:,:2]
        mid=(projection.min(axis=0)+projection.max(axis=0))/2
        ext=projection.max(axis=0)-projection.min(axis=0)
        self.scale=min(4.55/max(ext[0],1e-8),3.4/max(ext[1],1e-8),1.3)
        self.offset=self.R.T@(pt(-3.78,.42)-pt(*mid)*self.scale)
        self.world=VGroup();self.labels=VGroup();self.used=[]
        self.make_axes()
        self.make_geometry()
    def worldpt(self,p):return self.offset+self.scale*np.array(p,dtype=float)
    def screenpt(self,p):
        q=self.R@self.worldpt(p);q[2]=0;return q
    def label(self,s,p,col=INK,size=22):
        q=self.screenpt(p);mob=mtx(s,size,col)
        best=None;cost=1e9
        for dx,dy in [(0,.24),(.25,.12),(-.25,.12),(.22,-.23),(-.22,-.23),(0,-.30),(.44,0),(-.44,0),(0,.48)]:
            c=q+pt(dx,dy)
            l,r=c[0]-mob.width/2,c[0]+mob.width/2;b,t=c[1]-mob.height/2,c[1]+mob.height/2
            penalty=100*max(0,-6.55-l)+100*max(0,r+1.02)+100*max(0,t-2.35)+100*max(0,-1.62-b)
            for ll,rr,bb,tt in self.used:
                penalty+=1000*max(0,min(r,rr)-max(l,ll)+.08)*max(0,min(t,tt)-max(b,bb)+.08)
            if penalty<cost:best=(c,(l,r,b,t));cost=penalty
        c,box=best;mob.move_to(c);self.used.append(box);self.labels.add(mob)
    def edge(self,a,b,col=MUTED,dash=False,width=2):
        a=self.worldpt(a);b=self.worldpt(b)
        return DashedLine(a,b,color=col,stroke_width=width,dash_length=.085) if dash else Line(a,b,color=col,stroke_width=width)
    def arrow(self,a,b,col):
        a=self.worldpt(a);b=self.worldpt(b);length=np.linalg.norm(b-a)
        return Arrow3D(start=a,end=b,color=col,thickness=.014,height=min(.17,length*.19),base_radius=.045,resolution=12)
    def make_axes(self):
        cols=[BLUE,CYAN,RED]
        for axis in range(3):
            a=np.zeros(3);b=np.zeros(3);a[axis]=self.axislo[axis];b[axis]=self.axishi[axis]
            self.world.add(self.arrow(a,b,cols[axis]).set_opacity(.48))
            self.label(['x','y','z'][axis],b,cols[axis],24)
            unit=np.zeros(3);unit[axis]=1
            d=np.zeros(3);d[(axis+1)%3]=.055
            self.world.add(self.edge(unit-d,unit+d,cols[axis],width=2))
        origin_label=self.data.get('aliases',{}).get(self.pose,{}).get('O','O')
        if 'A' in self.points and np.linalg.norm(self.points['A'])<1e-9:origin_label='A=O'
        self.label(origin_label,np.zeros(3),MUTED,20)
    def make_geometry(self):
        d=self.data;p=self.points
        for face in d['faces']:
            self.world.add(Polygon(*[self.worldpt(p[k]) for k in face],fill_color=BLUE,fill_opacity=.12,stroke_width=0))
        for a,b,kind in d['edges']:
            self.world.add(self.edge(p[a],p[b],MUTED,kind=='dash',2))
        vectors=list(d['vectors'])
        if self.pose=='normal':vectors.append([*d['normal'],'gold'])
        if self.pose=='reverse':vectors.append([*d['reverse'],'gold'])
        if self.pose=='obtuse':vectors.append([*d['alternate'],'gold'])
        if self.pose=='volume' and 'normal' in d:vectors.append([*d['normal'],'gold'])
        for a,b,col in vectors:
            self.world.add(self.arrow(p[a],p[b],{'blue':BLUE,'cyan':CYAN,'gold':GOLD}.get(col,INK)))
        hidden=set()
        for key in ['normal','reverse','alternate']:
            if key in d:hidden.add(d[key][1])
        visible=set(p)-hidden
        visible.update(v[1] for v in vectors)
        if self.pose=='base' and 'projection' in d:visible.discard('H')
        for name in sorted(visible):
            if name=='O' or (name=='A' and np.linalg.norm(p[name])<1e-9):continue
            col=GOLD if name in {'N','R','H','I','G','S'} else INK
            self.world.add(Dot3D(self.worldpt(p[name]),radius=.043,color=col,resolution=(6,12)))
            self.label(d.get('aliases',{}).get(self.pose,{}).get(name,name),p[name],col)
        if self.pose=='components' and 'components' in d:
            q=p[d['components']];path=[np.zeros(3),pt(q[0],0,0),pt(q[0],q[1],0),q]
            for a,b,col in zip(path,path[1:],[BLUE,CYAN,RED]):
                if np.linalg.norm(b-a)>1e-8:self.world.add(self.arrow(a,b,col));self.label(str(round(float(np.linalg.norm(b-a)),3)),(a+b)/2,col,19)
            self.labels.add(fit(mtx(r'\Delta x\quad\Delta y\quad\Delta z',24),4.7).move_to(pt(-3.78,-1.94)))
        if 'angle' in d and self.pose not in ['obtuse','reverse']:
            a,b=d['angle'];origin=p.get('O',p.get('A',np.zeros(3)))
            self.arc(origin,p[a]-origin,p[b]-origin)
        if self.pose=='obtuse':
            a,b=d['angle'];o=p['O'];self.arc(o,p[a]-o,p[d['alternate'][1]]-o)
        if self.pose=='projection':
            u,v=(p[k] for k in d['projection']);h=np.dot(v,u)/np.dot(u,u)*u
            self.world.add(self.edge(v,h,GOLD,True,2.5),self.arrow(np.zeros(3),h,GOLD))
            self.right_angle(h,u,v-h)
            if 'H' not in visible:
                self.world.add(Dot3D(self.worldpt(h),radius=.04,color=GOLD,resolution=(6,12)));self.label('H',h,GOLD)
        if self.pose=='volume':
            a,b=d['height'];self.world.add(self.edge(p[a],p[b],GOLD,True,3))
            self.right_angle(p[b],p[a]-p[b],p['B']-p['A'])
        note='Ba trục cùng đơn vị • Nét đứt: đường phụ'
        if self.pose in ['normal','reverse','volume']:note='Mũi tên pháp tuyến biểu diễn hướng, đã thu ngắn'
        self.labels.add(fit(txt(note,15,MUTED),5.4,.4).move_to(pt(-3.78,-2.56)))
        self.labels.add(fit(txt('Phối cảnh 3D • Không đo góc trên màn hình',14,MUTED),5.4,.4).move_to(pt(-3.78,-2.89)))
    def arc(self,o,u,v):
        if np.linalg.norm(u)<1e-9 or np.linalg.norm(v)<1e-9:return
        e=u/np.linalg.norm(u);f=v/np.linalg.norm(v);c=np.clip(np.dot(e,f),-1,1);theta=math.acos(c)
        if theta<1e-7 or abs(theta-math.pi)<1e-7:return
        w=(f-c*e)/math.sin(theta);radius=min(np.linalg.norm(u),np.linalg.norm(v))*.27
        points=[self.worldpt(o+radius*(e*math.cos(t)+w*math.sin(t))) for t in np.linspace(0,theta,65)]
        arc=VMobject(color=GOLD,stroke_width=2.3);arc.set_points_as_corners(points);self.world.add(arc)
        if abs(c)<1e-8:self.right_angle(o,u,v)
        else:self.label(r'\theta',o+radius*1.35*(e*math.cos(theta/2)+w*math.sin(theta/2)),GOLD,20)
    def right_angle(self,o,u,v):
        if np.linalg.norm(u)<1e-9 or np.linalg.norm(v)<1e-9:return
        e=u/np.linalg.norm(u);f=v/np.linalg.norm(v)
        if abs(np.dot(e,f))>1e-7:raise ValueError('Ký hiệu góc vuông đặt vào góc không vuông')
        r=min(.24,np.linalg.norm(u)*.19,np.linalg.norm(v)*.19)
        points=[self.worldpt(o+r*e),self.worldpt(o+r*(e+f)),self.worldpt(o+r*f)]
        mark=VMobject(color=GOLD,stroke_width=2.4);mark.set_points_as_corners(points);self.world.add(mark)

class VectorLesson(ThreeDScene):
    lesson_id='C01'
    def construct(self):
        lesson=next(l for l in LESSONS if l['id']==self.lesson_id);self.events=[]
        self.set_camera_orientation(phi=65*DEGREES,theta=-48*DEGREES,focal_distance=1e9,zoom=1)
        self.camera.reset_rotation_matrix()
        title=fit(txt(lesson['title'],31,INK,True),12.9,.48).move_to(pt(0,3.5))
        subtitle=txt('BÀI 12.2.01 • OXYZ VÀ CÁC PHÉP TOÁN VECTƠ',16,BLUE).move_to(pt(0,3.07))
        left=panel(5.95,6.05,pt(-3.78,-.22),fill=0);right=panel(6.95,6.05,pt(2.92,-.22),fill=.98)
        footer=txt(SETTINGS['teacher'],19,MUTED).move_to(pt(-4.7,-3.74))
        rule=Line(pt(-6.7,-3.44),pt(6.7,-3.44),color=MUTED,stroke_width=1)
        self.add_fixed_in_frame_mobjects(title,subtitle,left,right,footer,rule)
        view=None;pose=None
        for pi,page in enumerate(lesson['pages']):
            if pose!=page['action']:
                new=VectorView(self,lesson['model'],page['action'])
                if view is not None:
                    self.play(FadeOut(view.world),FadeOut(view.labels),run_time=.35)
                    self.remove_fixed_in_frame_mobjects(view.labels);self.remove(view.world)
                self.add_fixed_in_frame_mobjects(new.labels);self.add(new.world)
                self.play(LaggedStart(*[FadeIn(m) for m in new.world],lag_ratio=.045),FadeIn(new.labels),run_time=1.2)
                view=new;pose=page['action']
            heading=fit(txt(page['title'],23,CYAN,True),6.15,.55).move_to(pt(-.19,2.48),aligned_edge=LEFT)
            counter=txt(f"Chương {lesson['order']}/{lesson['total']} • Trang {pi+1}/{len(lesson['pages'])}",14,MUTED).move_to(pt(4.7,-3.74))
            self.add_fixed_in_frame_mobjects(heading,counter);self.play(FadeIn(heading),run_time=.45)
            current=[];previous=None
            for ri,row in enumerate(page['rows']):
                if row['kind']=='math':mob=fit(mtx(row['text'],31,GOLD if row.get('gold') else INK),6.15,.94)
                else:
                    s=textwrap.fill(row['text'],width=41,break_long_words=False,break_on_hyphens=False)
                    mob=fit(txt(s,24),6.15,.92)
                mob.move_to(pt(-.19,1.55-ri*1.10),aligned_edge=LEFT)
                self.camera.add_fixed_in_frame_mobjects(mob)
                start=self.time;self.add_sound(row['audio'])
                if row['kind']=='math' and previous is not None:
                    copy=previous.copy();self.add_fixed_in_frame_mobjects(copy)
                    self.play(TransformMatchingTex(copy,mob),run_time=.9)
                    self.remove_fixed_in_frame_mobjects(copy)
                else:self.play(Write(mob) if row['kind']=='math' else FadeIn(mob,shift=UP*.08),run_time=.9)
                current.append(mob)
                if row['kind']=='math':previous=mob
                self.events.append({'start':start,'end':start+row['duration'],'text':row['voice']})
                self.wait(max(.15,row['duration']-(self.time-start))+.3)
                if row.get('gold'):self.play(Circumscribe(mob,color=GOLD,buff=.07),run_time=.8)
                if row.get('pause'):self.wait(row['pause'])
            self.wait(.9)
            self.play(*[FadeOut(m) for m in current+[heading,counter]],run_time=.45)
            self.remove_fixed_in_frame_mobjects(*current,heading,counter)
        (HERE/'events').mkdir(exist_ok=True)
        (HERE/'events'/(self.lesson_id+'.json')).write_text(json.dumps(self.events,ensure_ascii=False),encoding='utf-8')

class VectorAudit(ThreeDScene):
    lesson_id='C01';pose='base'
    def construct(self):
        lesson=next(l for l in LESSONS if l['id']==self.lesson_id)
        self.set_camera_orientation(phi=65*DEGREES,theta=-48*DEGREES,focal_distance=1e9,zoom=1)
        self.camera.reset_rotation_matrix()
        title=fit(txt(lesson['title'],31,INK,True),12.9,.48).move_to(pt(0,3.5))
        subtitle=txt('BÀI 12.2.01 • KIỂM TRA HÌNH TRƯỚC KHI RENDER',16,BLUE).move_to(pt(0,3.07))
        left=panel(5.95,6.05,pt(-3.78,-.22),fill=0);right=panel(6.95,6.05,pt(2.92,-.22),fill=.98)
        self.add_fixed_in_frame_mobjects(title,subtitle,left,right)
        view=VectorView(self,lesson['model'],self.pose);self.add(view.world);self.add_fixed_in_frame_mobjects(view.labels)
        page=next((p for p in lesson['pages'] if p['action']==self.pose),lesson['pages'][0])
        heading=fit(txt(page['title'],23,CYAN,True),6.15,.55).move_to(pt(-.19,2.48),aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(heading)
        for ri,row in enumerate(page['rows']):
            if row['kind']=='math':m=fit(mtx(row['text'],31,GOLD if row.get('gold') else INK),6.15,.94)
            else:m=fit(txt(textwrap.fill(row['text'],41,break_long_words=False),24),6.15,.92)
            m.move_to(pt(-.19,1.55-ri*1.10),aligned_edge=LEFT);self.add_fixed_in_frame_mobjects(m)
        self.wait(.1)
# LESSON_CLASSES

'''

def command(args,log,cwd=None):
    with Path(log).open('w',encoding='utf-8') as f:
        result=subprocess.run([str(x) for x in args],cwd=cwd,stdout=f,stderr=subprocess.STDOUT,text=True)
    if result.returncode:
        raise RuntimeError('Lệnh thất bại. Log: '+str(log)+'\n'+Path(log).read_text(encoding='utf-8',errors='replace')[-10000:])


def duration(path):
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
        '-of','default=noprint_wrappers=1:nokey=1',str(path)],capture_output=True,text=True,check=True)
    value=float(r.stdout)
    if value<=0 or not math.isfinite(value):raise ValueError('Thời lượng không hợp lệ: '+str(path))
    return value


def setup(root):
    os.environ['DEBIAN_FRONTEND']='noninteractive'
    marker=root/'environment_019.ok'
    if is_colab() and not marker.exists():
        print('BƯỚC 1/5 — Cài môi trường 3D, LaTeX, tiếng Việt, FFmpeg...')
        command(['apt-get','update','-qq'],root/'apt_update.log')
        command(['apt-get','install','-y','-qq','ffmpeg','pkg-config','python3-dev',
            'libcairo2-dev','libpango1.0-dev','fonts-dejavu-core','fonts-noto-core',
            'texlive-latex-base','texlive-latex-recommended','texlive-latex-extra',
            'texlive-fonts-recommended','texlive-science','dvisvgm'],root/'apt_install.log')
        command([sys.executable,'-m','pip','install','-q','manim=='+MANIM_VERSION,
            'edge-tts>=7,<8','nest_asyncio','ipywidgets'],root/'pip_install.log')
        command([sys.executable,'-c','import manim,edge_tts;print(manim.__version__)'],root/'env_check.log')
        marker.write_text(MANIM_VERSION)
    remedy='Dùng workflow render-manim.yml: chọn video=bai120201. Xem hdsd.md trong gói GitHub Actions.'
    for name in ['ffmpeg','ffprobe','latex','dvisvgm']:
        if not shutil.which(name):raise RuntimeError('Thiếu '+name+'. '+remedy)
    r=subprocess.run([sys.executable,'-c','import manim,edge_tts,nest_asyncio;print(manim.__version__)'],capture_output=True,text=True)
    if r.returncode or r.stdout.strip()!=MANIM_VERSION:
        raise RuntimeError('Môi trường Python chưa sẵn sàng cho Manim '+MANIM_VERSION+'. '+remedy+'\n'+r.stderr[-1500:])


async def audio_all(lessons,root):
    import edge_tts
    folder=root/'audio_cache';folder.mkdir(exist_ok=True)
    rows=[r for les in lessons for page in les['pages'] for r in page['rows']]
    unique={r['voice']:None for r in rows};sem=asyncio.Semaphore(2)
    async def one(text):
        payload=json.dumps({'text':text,'voice':GIONG_DOC,'rate':TOC_DO_DOC,'pitch':'+0Hz','engine':'edge-tts'},sort_keys=True,ensure_ascii=False)
        digest=hashlib.sha256(payload.encode()).hexdigest();dest=folder/(digest+'.mp3')
        async with sem:
            if dest.exists():
                try:unique[text]=(str(dest),duration(dest));return
                except Exception:dest.unlink(missing_ok=True)
            error=None
            for attempt in range(5):
                part=folder/(digest+'.part.mp3')
                try:
                    await asyncio.wait_for(edge_tts.Communicate(text,voice=GIONG_DOC,rate=TOC_DO_DOC).save(str(part)),timeout=120)
                    dur=duration(part);part.replace(dest);unique[text]=(str(dest),dur);return
                except Exception as e:
                    error=e;part.unlink(missing_ok=True);await asyncio.sleep(2+attempt*3)
            raise RuntimeError('Chưa tạo được lời đọc. Chạy lại để sử dụng các đoạn đã cache.\n'+text[:150]+'\n'+str(error))
    await asyncio.gather(*(one(text) for text in unique))
    for row in rows:row['audio'],row['duration']=unique[row['voice']]
    return sum(r['duration'] for r in rows)


def timestamp(s,sep=','):
    ms=max(0,round(s*1000));h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000)
    return f'{h:02d}:{m:02d}:{sec:02d}{sep}{ms:03d}'


def captions(events,stem):
    chunks=[]
    for event in events:
        parts=[];words=event['text'].split();buffer=[]
        for word in words:
            if len(' '.join(buffer+[word]))>84 and buffer:parts.append(' '.join(buffer));buffer=[]
            buffer.append(word)
        if buffer:parts.append(' '.join(buffer))
        count=sum(len(p.split()) for p in parts);start=event['start']
        for p in parts:
            end=start+(event['end']-event['start'])*len(p.split())/count
            chunks.append((start,end,textwrap.fill(p,width=44,break_long_words=False)));start=end
    srt=[];vtt=['WEBVTT\n']
    for i,(start,end,text) in enumerate(chunks,1):
        srt.append(f'{i}\n{timestamp(start)} --> {timestamp(end)}\n{text}\n')
        vtt.append(f'{timestamp(start,".")} --> {timestamp(end,".")}\n{text}\n')
    stem.with_suffix('.srt').write_text('\n'.join(srt),encoding='utf-8')
    stem.with_suffix('.vtt').write_text('\n'.join(vtt),encoding='utf-8')



def scene_code(lessons):
    classes='\n'.join(f"class C_{s['id']}(VectorLesson):\n    lesson_id={s['id']!r}\n" for s in lessons)
    return SCENE_SOURCE.replace('# LESSON_CLASSES',classes)


def is_codespaces():
    return os.environ.get('CODESPACES','').lower()=='true'


def is_actions():
    return os.environ.get('GITHUB_ACTIONS','').lower()=='true'


def is_colab():
    return not is_codespaces() and sys.platform=='linux' and Path('/content').is_dir()


def require_render_environment():
    """Mặc định cho phép Codespaces/Colab, chặn vô tình render trên Mac."""
    if CHI_CHAY_TREN_CLOUD and not (is_codespaces() or is_colab() or is_actions()):
        raise RuntimeError('Hãy chạy trên GitHub Actions, Codespaces hoặc Colab. Lệnh --check vẫn chạy được trên máy cá nhân.')


def output_root(folder):
    override=os.environ.get('MANIM_OUTPUT_DIR')
    if override:return Path(override).expanduser().resolve()/folder
    if is_actions():return Path(os.environ.get('RUNNER_TEMP','/tmp'))/'manim-video-output'/folder
    if is_colab():return Path('/content')/folder
    if is_codespaces():return Path('/tmp/manim-video-output')/folder
    base=Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
    return base/'renders'/folder


def show_downloads(final,archive):
    """Chỉ hiển thị nút tải; không đọc/nhúng MP4, không tạo trình phát.

    files.download chỉ được gọi sau khi người dùng bấm một nút.
    Không có vòng lặp JavaScript, timer, keep-alive hay polling giao diện.
    """
    if is_actions():
        print('TẢI VỀ: trang lần chạy GitHub Actions > Artifacts > video đã xuất.')
        return
    if is_codespaces():
        print('Video và cache nằm ngoài repo. Thêm thư mục kết quả vào Explorer bằng:')
        import shlex
        print('code --add '+shlex.quote(str(final.parent.parent)))
        print('Explorer > thư mục bài > chuột phải MP4 > Download. Không cần mở video.')
        print('Tải và kiểm tra xong: bash cleanup_outputs.sh để dọn dữ liệu tạm.')
        return
    print('Video đã sẵn sàng. Bấm Tải video MP4; không cần mở xem trong Colab.')
    if not is_colab():return
    try:
        from google.colab import files
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError:
        print('Mở bảng Files bên trái Colab, tìm đường dẫn Video ở trên rồi chọn Download.')
        return
    buttons=[]
    for label,path in [('Tải video MP4',final),('Tải phụ đề SRT',final.with_suffix('.srt')),('Tải mã nguồn ZIP',archive)]:
        button=widgets.Button(description=label)
        button.on_click(lambda _,p=path:files.download(str(p)))
        buttons.append(button)
    display(widgets.HBox(buttons))


def geometry_previews(root):
    lessons=build_lessons()
    work=root/'geometry_check';work.mkdir(parents=True,exist_ok=True)
    (work/'lessons.json').write_text(json.dumps(lessons,ensure_ascii=False),encoding='utf-8')
    (work/'settings.json').write_text(json.dumps({'teacher':TEN_THAY,'width':1280,'height':720,'fps':15}),encoding='utf-8')
    names=[];classes=[]
    for lesson in lessons:
        for pose in lesson['model']['poses']:
            name='Audit_'+lesson['id']+'_'+pose;names.append(name)
            classes.append(f"class {name}(VectorAudit):\n    lesson_id={lesson['id']!r}\n    pose={pose!r}\n")
    source=work/'geometry_scene.py';source.write_text(scene_code(lessons)+'\n'+'\n'.join(classes),encoding='utf-8')
    command([sys.executable,'-m','manim','--renderer','cairo','--save_last_frame','--progress_bar','none',
        '--verbosity','WARNING','-r','1280,720','--media_dir',work/'media',source,*names],work/'geometry_render.log',cwd=work)
    from PIL import Image,ImageOps,ImageDraw
    thumbs=[]
    for name in names:
        found=list((work/'media').rglob(name+'*.png'))
        if not found:raise RuntimeError('Thiếu ảnh '+name)
        target=work/(name+'.png');shutil.copy2(found[-1],target)
        im=Image.open(target).convert('RGB');thumb=ImageOps.contain(im,(480,270))
        cell=Image.new('RGB',(480,294),'#0B1120');cell.paste(thumb,(0,0))
        ImageDraw.Draw(cell).text((8,276),name,fill='white');thumbs.append(cell)
    sheet=Image.new('RGB',(1440,294*math.ceil(len(thumbs)/3)),'#0B1120')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*480,(i//3)*294))
    sheet.save(work/'tong_hop_hinh.png')
    print(f'Đã render {len(names)} ảnh từ chính lớp VectorView của video:',work)


def main():
    global CHE_DO,CHON_BAI
    CHE_DO=os.environ.get('MANIM_QUALITY',CHE_DO)
    if 'MANIM_LESSONS' in os.environ:
        CHON_BAI=[x.strip() for x in os.environ['MANIM_LESSONS'].split(',') if x.strip()]
    validate_math()
    if '--check' in sys.argv:return
    require_render_environment()
    if CHE_DO not in PRESETS:raise ValueError('CHE_DO không hợp lệ.')
    width,height,fps=PRESETS[CHE_DO]
    lessons=build_lessons();known={s['id'] for s in lessons}
    if set(CHON_BAI)-known:raise ValueError('Mã bài không tồn tại: '+str(set(CHON_BAI)-known))
    if CHON_BAI:lessons=[s for s in lessons if s['id'] in CHON_BAI]
    for i,s in enumerate(lessons,1):s['order']=i;s['total']=len(lessons)
    root=output_root('Bai_12_2_01_Oxyz')
    root.mkdir(exist_ok=True,parents=True);setup(root)
    if '--geometry-preview' in sys.argv:
        geometry_previews(root);return
    print('BƯỚC 2/5 — Tạo lời giảng chi tiết và đo thời lượng...')
    import nest_asyncio
    nest_asyncio.apply()
    spoken=asyncio.run(audio_all(lessons,root))
    settings={'teacher':TEN_THAY,'width':width,'height':height,'fps':fps,'voice':GIONG_DOC,'rate':TOC_DO_DOC}
    code=scene_code(lessons)
    digest=hashlib.sha256((code+json.dumps(settings,sort_keys=True)+json.dumps(lessons,ensure_ascii=False,sort_keys=True)).encode()).hexdigest()[:16]
    work=root/('render_'+digest);work.mkdir(exist_ok=True);(work/'events').mkdir(exist_ok=True);(work/'clips').mkdir(exist_ok=True)
    source=work/'oxyz_scene.py';source.write_text(code,encoding='utf-8')
    (work/'lessons.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2),encoding='utf-8')
    (work/'settings.json').write_text(json.dumps(settings,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Lời giảng: {spoken/60:.1f} phút; video còn có hình động và khoảng tự giải. Không ép thời lượng.')
    print('BƯỚC 3/5 — Render từng bài Oxyz; dùng lại bài đã hoàn tất...')
    clips=[];all_events=[];marks=[];offset=0
    for les in lessons:
        name='C_'+les['id'];clip=work/'clips'/(name+'.mp4');event=work/'events'/(les['id']+'.json')
        reusable=False
        if clip.exists() and event.exists():
            try:duration(clip);json.loads(event.read_text());reusable=True
            except Exception:pass
        if not reusable:
            command([sys.executable,'-m','manim','--renderer','cairo','--format','mp4',
                '--fps',fps,'-r',f'{width},{height}','--media_dir',work/'media','--progress_bar','none',
                '--verbosity','WARNING','-o',name,source,name],work/(name+'.log'),cwd=work)
            candidates=[p for p in (work/'media').rglob(name+'.mp4') if 'partial_movie_files' not in str(p)]
            if not candidates:raise RuntimeError('Không tìm thấy video '+name)
            shutil.copy2(max(candidates,key=lambda p:p.stat().st_mtime),clip)
        if not event.exists():raise RuntimeError('Thiếu mốc phụ đề '+name)
        dur=duration(clip);clips.append(clip);marks.append((offset,offset+dur,les['title']))
        for ev in json.loads(event.read_text(encoding='utf-8')):
            ev['start']+=offset;ev['end']+=offset;all_events.append(ev)
        offset+=dur
        print(f"  {les['id']} — {les['title']}: {dur/60:.2f} phút {'(cache)' if reusable else ''}")
    print('BƯỚC 4/5 — Ghép MP4 và xuất phụ đề, mục lục...')
    concat=work/'concat.txt';concat.write_text('\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in clips)+'\n',encoding='utf-8')
    metadata=[';FFMETADATA1','title=Bài 12.2.01 - Oxyz, vectơ, tích vô hướng và tích có hướng','artist='+TEN_THAY]
    for start,end,title in marks:
        escaped=title.replace('\\','\\\\').replace('=','\\=').replace(';','\\;').replace('#','\\#')
        metadata+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(start*1000)}',f'END={round(end*1000)}','title='+escaped]
    meta=work/'chapters.ffmeta';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
    final=root/'bai_12_2_01_oxyz_vecto.mp4'
    command(['ffmpeg','-y','-v','warning','-f','concat','-safe','0','-i',concat,'-i',meta,
             '-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy',
             '-movflags','+faststart',final],work/'ffmpeg_join.log')
    final_dur=duration(final)
    info=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(final)],check=True,capture_output=True,text=True).stdout)
    assert {'video','audio'}.issubset({s['codec_type'] for s in info['streams']}),'Video thiếu hình hoặc âm thanh.'
    captions(all_events,final.with_suffix(''))
    toc=root/'bai_12_2_01_muc_luc.txt';toc.write_text('\n'.join(timestamp(a,'.')+'  '+title for a,b,title in marks),encoding='utf-8')
    archive=root/'bai_12_2_01_ma_nguon.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in [source,work/'lessons.json',work/'settings.json',toc,final.with_suffix('.srt'),final.with_suffix('.vtt')]:z.write(p,p.name)
        if '__file__' in globals() and Path(__file__).is_file():z.write(__file__,Path(__file__).name)
        z.writestr('HUONG_DAN.txt','Tải tệp .py gốc lên Colab; dùng runpy.run_path để chạy trong một ô mã ngắn.\n'
            'CHON_BAI=["C01","C02"] để thử; [] để dựng toàn bộ.\n'
            'CHE_DO: preview, standard, final.\n'
            'Bài 12.2.01: mọi bài tập đều có lời giải; tích có hướng là phần mở rộng.\n')
    print(f'BƯỚC 5/5 — HOÀN TẤT: {final_dur/60:.2f} phút, {width}×{height}, {fps} fps.')
    print('Video:',final);print('Mã nguồn:',archive)
    show_downloads(final,archive)


if __name__=='__main__':main()
