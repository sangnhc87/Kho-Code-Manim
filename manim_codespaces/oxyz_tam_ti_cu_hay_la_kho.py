# -*- coding: utf-8 -*-
"""
THẦY NGUYỄN VĂN SANG — OXYZ: TÂM TỈ CỰ, BÀI TOÁN HAY–LẠ–KHÓ
Colab nhẹ: tải tệp .py lên rồi chạy bằng runpy (hướng dẫn bên dưới).
15 bài, mỗi bài có đề và LỜI GIẢI.
Không dùng phương trình tổng quát/tham số đường thẳng, phương trình mặt
phẳng hoặc phương trình mặt cầu. Đoạn thẳng chỉ dùng tỉ số chia đoạn
0≤t≤1; mặt tọa độ chỉ dùng định nghĩa tọa độ; mặt tam giác của tứ diện
được xét bằng tổ hợp vectơ và bất đẳng thức, không lập phương trình mặt.
Kiến thức: vectơ Oxyz, độ dài, tích vô hướng, hoàn thành bình phương,
Cauchy (u²+v²≥(u+v)²/2), tọa độ điểm chia đoạn, trọng tâm tam giác/tứ diện.
Không gọi một điểm là 'tâm tỉ cự' khi tổng trọng số bằng không.
Không áp dụng đồng nhất thức bình phương cho tổng khoảng cách thường.

CHON_BAI=[]: đủ; ['B11']: thử bài tam giác; ['INTRO','B01']: thử nền tảng.
CHE_DO='preview'/'standard'/'final': 480p/720p/1080p.
python file.py --check: chỉ kiểm chứng toán, không cài/render.
Đầu ra: MP4 có mục lục, SRT/VTT, ZIP mã nguồn. Có cache audio/render.
Hình thật trong ThreeDScene; không dùng camera xoay cho trang trí.
API: Manim Community 0.19.0 (Cairo), nguồn github.com/ManimCommunity/manim.

CODESPACES (bộ ZIP kèm setup_codespaces.sh và render.sh):
- Lần đầu: bash setup_codespaces.sh
- Render: bash render.sh oxyz final
- MP4 ở /tmp/manim-video-output, ngoài repo; thêm thư mục vào Explorer để tải.
- Cài một lần cho cùng môi trường; rebuild/xóa Codespace cần cài lại.

CÁCH CHẠY NHẸ GIAO DIỆN COLAB:
1. Mở notebook mới trên Colab, dùng runtime do Google cung cấp.
2. Bảng Files (biểu tượng thư mục) > Upload, chọn tệp .py này.
3. Trong MỘT ô mã ngắn, chạy:
   import runpy
   _ = runpy.run_path('/content/oxyz_tam_ti_cu_hay_la_kho.py', run_name='__main__')
4. Chờ thông báo HOÀN TẤT rồi bấm Tải video MP4. Không có trình phát.
Không cần dán gần 1.000 dòng mã vào trình soạn thảo của trình duyệt.
Cài đặt/render/ghép phim đều ghi log trên runtime; chỉ in mốc từng chương.
Chỉ mở một notebook đang render. Không dùng runtime kết nối máy cá nhân.
Cache dùng lại được nếu runtime và các file /content vẫn còn.
Đóng tab không bảo đảm Colab tiếp tục chạy; chế độ này không giữ phiên
bằng JavaScript. Nó giảm phần hiển thị, không bảo đảm máy mát 100%.

"""
import os,sys,json,math,hashlib,asyncio,subprocess,textwrap,shutil,zipfile,concurrent.futures
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
def norm2(a):return dot(a,a)
def weighted_center(case):
    S=sum(case['weights'])
    if abs(S)<1e-12:return None
    return [sum(w*p[j] for w,p in zip(case['weights'],case['anchors'].values()))/S for j in range(3)]
def constant_K(case):
    I=weighted_center(case)
    if I is None:return None
    return sum(w*norm2(p) for w,p in zip(case['weights'],case['anchors'].values()))-sum(case['weights'])*norm2(I)
def objective(case,M):
    if case.get('kind')=='vector':
        v=[sum(w*(p[j]-M[j]) for w,p in zip(case['weights'],case['anchors'].values())) for j in range(3)]
        return math.sqrt(norm2(v))
    return sum(w*norm2(sub(M,p)) for w,p in zip(case['weights'],case['anchors'].values()))

CASES=[
 {'id':'B01','title':'Trạm trung chuyển có ba trọng số','anchors':{'A':[4,0,0],'B':[0,4,0],'C':[0,0,4]},'weights':[1,2,1],'constraint':'free','start':[-1,1,3],'opt':[1,2,1],'value':40,'K':40},
 {'id':'B02','title':'Có hệ số âm vẫn có cực tiểu','anchors':{'A':[2,0,0],'B':[0,2,0],'C':[0,0,2]},'weights':[2,3,-1],'constraint':'free','start':[2,1,1],'opt':[1,1.5,-.5],'value':2,'K':2},
 {'id':'B03','title':'Một biểu thức có giá trị lớn nhất bằng 0','anchors':{'A':[2,0,0],'B':[0,2,0],'C':[0,0,2]},'weights':[1,-2,-2],'constraint':'free','start':[1,1,1],'opt':[-2/3,4/3,4/3],'value':0,'K':0,'maximize':True},
 {'id':'B04','title':'Tham số làm đổi cả bản chất bài toán','anchors':{'A':[-1,0,0],'B':[1,0,0],'O':[0,0,0]},'weights':[1,1,1],'constraint':'free','start':[2,1,1],'opt':[0,0,0],'value':2,'K':2,'parameter':True},
 {'id':'B05','title':'Chọn trục nào để chi phí thấp nhất?','anchors':{'A':[4,0,0],'B':[0,2,0],'C':[0,0,6]},'weights':[1,1,1],'constraint':'axes','start':[2,0,0],'opt':[0,0,2],'value':44,'K':112/3},
 {'id':'B06','title':'Tối ưu độ dài một tổng vectơ có dấu','anchors':{'A':[2,0,0],'B':[0,4,0],'C':[0,0,4]},'weights':[2,-1,3],'constraint':'oxy','start':[0,1,0],'opt':[1,-1,0],'value':12,'kind':'vector'},
 {'id':'B07','title':'Ràng buộc cách đều: chỉ cần khai triển tọa độ','anchors':{'A':[-2,0,0],'B':[4,0,0],'C':[0,3,6]},'weights':[1,1,2],'constraint':'equal','start':[1,-1,1],'opt':[1,1.5,3],'value':65,'K':64},
 {'id':'B08','title':'Điểm trên đoạn: tỉ số chia đoạn và tâm tỉ cự','anchors':{'P':[1,2,3],'Q':[3,4,1]},'weights':[1,3],'constraint':'segment','domain':{'A':[0,0,0],'B':[4,4,0]},'start':[.5,.5,0],'opt':[3,3,0],'value':20,'K':9},
 {'id':'B09','title':'Bẫy nghiệm ở ngoài đoạn thẳng','anchors':{'P':[6,6,2],'Q':[4,4,0]},'weights':[1,1],'constraint':'segment','domain':{'A':[0,0,0],'B':[4,4,0]},'start':[1,1,0],'opt':[4,4,0],'value':12,'K':6},
 {'id':'B10','title':'Trong hình hộp: tìm cả nhỏ nhất và lớn nhất','anchors':{'P':[4,-2,3],'Q':[2,0,1]},'weights':[1,1],'constraint':'box','start':[1,1.5,.5],'opt':[2,0,1],'value':12,'K':6,'max_point':[0,3,0],'max_value':64},
 {'id':'B11','title':'Trong tam giác: hình chiếu không hợp lệ','anchors':{'P':[4,4,3],'Q':[2,2,1]},'weights':[1,1],'constraint':'triangle','domain':{'O':[0,0,0],'A':[4,0,0],'B':[0,4,0]},'start':[1,1,0],'opt':[2,2,0],'value':18,'K':6,'aux':{'J':[3,3,0]}},
 {'id':'B12','title':'Tứ diện và ràng buộc trên một mặt tam giác','anchors':{'O':[0,0,0],'A':[4,0,0],'B':[0,4,0],'C':[0,0,4]},'weights':[1,1,1,1],'constraint':'tetra_face','start':[2,1,1],'opt':[4/3,4/3,4/3],'value':112/3,'K':36},
 {'id':'B13','title':'Bài ngược: thiết kế một điểm để cực tiểu tại đích','anchors':{'A':[1,0,0],'B':[0,1,0],'C':[4,3,6]},'weights':[2,3,1],'constraint':'free','start':[2,1,2],'opt':[1,1,1],'value':48,'K':48,'hidden':['C'],'given_center':True},
 {'id':'B14','title':'Tổng khoảng cách khác tổng bình phương','anchors':{'A':[0,0,0],'B':[4,0,0]},'weights':[1,1],'constraint':'free','start':[1,1,1],'opt':[2,0,0],'value':8,'K':8,'compare_lengths':True},
 {'id':'B15','title':'Tổng trọng số bằng 0: không được chia!','anchors':{'A':[0,0,0],'B':[2,0,0]},'weights':[1,-1],'constraint':'free','start':[0,1,1],'opt':[0,1,1],'value':-4,'zero_sum':True},
]


def validate_math():
    import random
    rnd=random.Random(2403)
    for c in CASES:
        I=weighted_center(c);S=sum(c['weights'])
        for _ in range(50):
            M=[rnd.uniform(-6,6) for _ in range(3)]
            F=objective(c,M)
            if I is not None:
                rhs=abs(S)*math.sqrt(norm2(sub(M,I))) if c.get('kind')=='vector' else S*norm2(sub(M,I))+constant_K(c)
                assert math.isclose(F,rhs,rel_tol=1e-10,abs_tol=1e-9),(c['id'],F,rhs)
        assert math.isclose(objective(c,c['opt']),c['value'],abs_tol=1e-9),c['id']
        if 'K' in c:assert math.isclose(constant_K(c),c['K'],abs_tol=1e-9),c['id']
        if c['constraint']=='segment':
            for t in [i/100 for i in range(101)]:assert objective(c,[4*t,4*t,0])>=c['value']-1e-9
        if c['constraint']=='axes':
            for j in range(3):
                for t in [i/10 for i in range(-80,81)]:
                    M=[0,0,0];M[j]=t;assert objective(c,M)>=c['value']-1e-9
        if c['constraint']=='triangle':
            for x in [i/10 for i in range(41)]:
                for y in [i/10 for i in range(41)]:
                    if x+y<=4+1e-9:assert objective(c,[x,y,0])>=18-1e-9
        if c['constraint']=='box':
            for _ in range(1000):
                M=[rnd.uniform(0,2),rnd.uniform(0,3),rnd.uniform(0,1)]
                assert 12-1e-9<=objective(c,M)<=64+1e-9
            assert objective(c,c['max_point'])==64
        if c['constraint']=='tetra_face':
            for _ in range(300):
                u=rnd.random();v=rnd.random()*(1-u);w=1-u-v
                assert objective(c,[4*u,4*v,4*w])>=112/3-1e-9
        if c['constraint']=='equal':
            for _ in range(100):
                M=[1,rnd.uniform(-4,4),rnd.uniform(-4,6)]
                assert norm2(sub(M,c['anchors']['A']))==norm2(sub(M,c['anchors']['B']))
                assert objective(c,M)>=65-1e-9
    for mu in [-5,-2,0,3]:
        c=json.loads(json.dumps(CASES[3]));c['weights']=[1,1,mu]
        for M in [[0,0,0],[1,2,3],[-2,1,4]]:assert objective(c,M)==2+(2+mu)*norm2(M)
    c=CASES[14]
    for M in [[-10,3,5],[0,2,-3],[3,-2,5],[12,0,0]]:assert objective(c,M)==4*M[0]-4
    print('KIỂM CHỨNG: 15 bài; đồng nhất thức có dấu; cực trị và ràng buộc: đạt.')


def T(text,voice,pause=0):return {'kind':'text','text':text,'voice':voice,'pause':pause}
def M(tex,voice,gold=False):return {'kind':'math','text':tex,'voice':voice,'gold':gold}
def P(title,rows,action='none'):return {'title':title,'rows':rows,'action':action}

INTRO=[
 P('Ta biết gì trước khi bắt đầu?',[
  T('Chỉ dùng tọa độ điểm, vectơ, độ dài và tích vô hướng.','Chào các em. Hôm nay ta học tâm tỉ cự và các bài toán cực trị trong O x y z. Chỉ cần tọa độ điểm, vectơ, độ dài, tích vô hướng và hoàn thành bình phương.'),
  M(r'\overrightarrow{AB}=(x_B-x_A;\ y_B-y_A;\ z_B-z_A)','Tọa độ vectơ A B bằng tọa độ B trừ tọa độ A theo từng thành phần.'),
  M(r'AB^2=(x_B-x_A)^2+(y_B-y_A)^2+(z_B-z_A)^2','Bình phương khoảng cách là tổng bình phương ba độ chênh tọa độ.'),
  T('Không dùng phương trình đường thẳng, mặt phẳng hay mặt cầu.','Không cần công thức phương trình đường thẳng, mặt phẳng hoặc mặt cầu. Khi điểm nằm trên đoạn, ta chỉ dùng tỉ số chia đoạn.')
 ]),
 P('Tâm tỉ cự là trung bình có trọng số',[
  M(r'S=\sum_iw_i\ne0,\quad\overrightarrow{OI}=\frac{\sum_iw_i\overrightarrow{OA_i}}S','Đặt S là tổng trọng số và yêu cầu S khác không. Tọa độ I là trung bình có trọng số của tọa độ các điểm.'),
  M(r'x_I=\frac{\sum_iw_ix_i}S,\quad y_I=\frac{\sum_iw_iy_i}S,\quad z_I=\frac{\sum_iw_iz_i}S','Tính riêng từng tọa độ bằng tổng trọng số nhân tọa độ, rồi chia S.'),
  M(r'\sum_iw_i\overrightarrow{IA_i}=\vec0','Từ định nghĩa suy ra tổng các vectơ xuất phát ở I, nhân trọng số, bằng vectơ không.'),
  T('Có trọng số âm thì tâm có thể nằm ngoài hình của các điểm.','Các trọng số không nhất thiết đều dương. Nếu có trọng số âm, I có thể nằm ngoài tam giác hoặc tứ diện của các điểm.')
 ],'center'),
 P('Chứng minh đồng nhất thức trung tâm',[
  M(r'\overrightarrow{MA_i}=\overrightarrow{MI}+\overrightarrow{IA_i}','Phân tích vectơ M A i thành vectơ M I cộng vectơ I A i.'),
  M(r'MA_i^2=MI^2+IA_i^2+2\overrightarrow{MI}\cdot\overrightarrow{IA_i}','Khai triển bình phương độ dài bằng tích vô hướng. Không được bỏ số hạng tích vô hướng trước khi cộng các trọng số.'),
  M(r'\sum_iw_iMA_i^2=S\,MI^2+\sum_iw_iIA_i^2','Nhân trọng số và cộng. Số hạng hỗn hợp triệt tiêu vì tổng trọng số nhân vectơ I A i bằng không.'),
  M(r'\boxed{F(M)=S\,MI^2+K}', 'Vậy tổng bình phương có trọng số được gom thành S nhân M I bình cộng một hằng số K.',True)
 ],'center'),
 P('Dấu của S và cách tính K',[
  M(r'K=\sum_iw_i\lVert\overrightarrow{OA_i}\rVert^2-S\lVert\overrightarrow{OI}\rVert^2','Để tính K nhanh, lấy tổng trọng số nhân bình phương độ dài O A i, trừ S nhân O I bình.'),
  M(r'S>0:\ \min F=K\iff M=I','Nếu M được tự do và S dương, giá trị nhỏ nhất là K, chỉ đạt khi M trùng I.'),
  M(r'S<0:\ \max F=K\iff M=I','Nếu S âm, kết luận đổi thành giá trị lớn nhất. Không được cứ thấy tâm tỉ cự là tìm nhỏ nhất.'),
  T('Có ràng buộc: tìm điểm hợp lệ gần hoặc xa I nhất.','Nếu M có ràng buộc, I chưa chắc hợp lệ. Ta phải tìm điểm trong miền cho phép gần hoặc xa I nhất, và kiểm tra điều kiện dấu bằng.')
 ])
]

# Bổ sung kiến thức dùng cho bài tam giác: chứng minh bằng chia đoạn,
# không mặc định học sinh đã biết tọa độ barycentric.
INTRO.extend([
 P('Vì sao có thể dùng ba hệ số trong một tam giác?',[
  T('Chọn D trên BC và M trên AD; trường hợp M = A xét riêng.', 'Với M trong tam giác A B C và khác A, tia A M gặp đoạn B C tại D. Đặt s bằng B D trên B C và t bằng A M trên A D; cả hai từ không tới một.'),
  M(r'\overrightarrow{OD}=(1-s)\overrightarrow{OB}+s\overrightarrow{OC}', 'Công thức chia đoạn B C cho vectơ O D bằng một trừ s nhân O B cộng s nhân O C.'),
  M(r'\overrightarrow{OM}=(1-t)\overrightarrow{OA}+t\overrightarrow{OD}', 'Áp dụng lại công thức chia đoạn trên A D.'),
  M(r'u=1-t,\quad v=t(1-s),\quad w=ts\Rightarrow u+v+w=1', 'Thay vào, được ba hệ số không âm u, v, w có tổng bằng một. Nếu M là A thì dùng một, không, không.')
 ]),
 P('Hai công cụ nhỏ cho những bài khó',[
  M(r'\overrightarrow{OM}=u\overrightarrow{OA}+v\overrightarrow{OB}+w\overrightarrow{OC}', 'Vậy mọi điểm trong tam giác có biểu diễn này, với hệ số không âm và tổng bằng một. Ngược lại, các hệ số như vậy dựng được điểm bằng hai lần chia đoạn.'),
  M(r'a^2+b^2\ge\frac{(a+b)^2}{2}\quad(=\iff a=b)', 'Tổng hai bình phương ít nhất bằng bình phương tổng chia hai, vì hiệu hai vế là một nửa bình phương a trừ b.'),
  M(r'a^2+b^2+c^2\ge\frac{(a+b+c)^2}{3}', 'Tương tự, tổng ba bình phương ít nhất bằng bình phương tổng chia ba. Hiệu hai vế là một phần ba tổng bình phương ba hiệu từng đôi.'),
  M(r'\begin{aligned}3(a^2+b^2+c^2)&-(a+b+c)^2\\&=(a-b)^2+(b-c)^2+(c-a)^2\end{aligned}', 'Đẳng thức này chứng minh bất đẳng thức ba số. Dấu bằng khi và chỉ khi a bằng b bằng c.')
 ])
])

PAGES={
'B01':[
 P('Đề bài • Một mô hình chi phí có trọng số',[
  M(r'A(4;0;0),\ B(0;4;0),\ C(0;0;4)','Cho ba điểm A, B, C như trên. Các khoảng cách đo trong cùng một đơn vị.'),
  M(r'F=MA^2+2MB^2+MC^2','Một trạm M chịu chi phí bằng M A bình cộng hai M B bình cộng M C bình.'),
  T('Tìm vị trí trạm để chi phí nhỏ nhất, M tự do trong không gian.','Hãy tìm vị trí M và giá trị nhỏ nhất. Đây là mô hình chi phí bình phương, không phải tổng độ dài đường vận chuyển.'),
  T('Đặt trọng số đúng trước khi lấy trung bình tọa độ.','Trọng số của B là hai, nên không lấy trọng tâm thông thường của tam giác.')
 ]),
 P('Tính tâm và hằng số',[
  M(r'S=1+2+1=4>0','Tổng trọng số bằng bốn, dương.'),
  M(r'I=\left(\frac{4}{4};\frac{8}{4};\frac{4}{4}\right)=(1;2;1)','Tâm tỉ cự có tọa độ một, hai, một.'),
  M(r'K=16+2\cdot16+16-4(1^2+2^2+1^2)=40','Tổng trọng số nhân O A bình bằng sáu mươi bốn. Trừ bốn nhân sáu, được K bằng bốn mươi.'),
  M(r'F=4MI^2+40','Do đồng nhất thức đã chứng minh, F bằng bốn M I bình cộng bốn mươi.')
 ],'center'),
 P('Kết luận và điều kiện dấu bằng',[
  M(r'MI^2\ge0\quad\Rightarrow\quad F\ge40','Bình phương khoảng cách không âm, nên F không nhỏ hơn bốn mươi.'),
  M(r'F=40\iff MI=0\iff M=I','Dấu bằng xảy ra khi và chỉ khi M trùng I.'),
  M(r'\boxed{M(1;2;1),\quad F_{\min}=40}','Vị trí trạm duy nhất là một, hai, một. Chi phí nhỏ nhất là bốn mươi.',True),
  T('Giảm chi phí là đưa M về tâm có trọng số, không phải về O.','Quan sát M di chuyển tới I. Các khoảng cách riêng lẻ không nhất thiết đều giảm, nhưng tổng chi phí giảm tới mức nhỏ nhất.')
 ],'opt')],
'B02':[
 P('Đề bài • Đừng loại phương pháp chỉ vì hệ số âm',[
  M(r'A(2;0;0),\ B(0;2;0),\ C(0;0;2)','Cho ba điểm nằm trên các trục tọa độ, mỗi điểm cách gốc hai đơn vị.'),
  M(r'F=2MA^2+3MB^2-MC^2','Tìm giá trị nhỏ nhất của hai M A bình cộng ba M B bình trừ M C bình.'),
  T('M tự do; có một hệ số âm. F có bị chặn dưới không?','Biểu thức có hệ số âm. Các em hãy dự đoán có giá trị nhỏ nhất hay không. Dừng video nếu cần tự tính.',pause=4)
 ]),
 P('Tổng hệ số quyết định chiều cực trị',[
  M(r'S=2+3-1=4>0','Dù một hệ số âm, tổng hệ số vẫn bằng bốn và dương.'),
  M(r'I=\left(1;\frac32;-\frac12\right)','Tâm tỉ cự có tọa độ một, ba phần hai, âm một phần hai. I nằm ngoài tam giác A B C.'),
  M(r'K=(2+3-1)\cdot4-4\left(1+\frac94+\frac14\right)=2','Tổng trọng số nhân độ dài từ O bình là mười sáu. Trừ bốn nhân ba phẩy năm, được K bằng hai.'),
  M(r'F=4MI^2+2','F bằng bốn M I bình cộng hai.')
 ],'center'),
 P('Lời giải hoàn tất',[
  M(r'F\ge2,\qquad F=2\iff M=I','Vì S dương và M tự do, F không nhỏ hơn hai. Dấu bằng duy nhất tại I.'),
  M(r'\boxed{F_{\min}=2;\quad M\left(1;\frac32;-\frac12\right)}','Đáp số là hai, tại điểm có tọa độ một, ba phần hai, âm một phần hai.',True),
  T('Điều cần xét là S, không phải từng trọng số riêng lẻ.','Một hệ số âm không làm mất cực tiểu. Phải xét tổng hệ số và miền M được phép di chuyển.')
 ],'opt')],
'B03':[
 P('Đề bài • Một cực đại bất ngờ',[
  M(r'A(2;0;0),\ B(0;2;0),\ C(0;0;2)','Giữ ba điểm A, B, C ở các trục như bài trước.'),
  M(r'F=MA^2-2MB^2-2MC^2','M tự do. Tìm giá trị lớn nhất của M A bình trừ hai M B bình trừ hai M C bình.'),
  T('Có số hạng dương nhưng giá trị lớn nhất có thể bằng 0.','Hãy nhìn tổng các hệ số trước khi khai triển toàn bộ theo x, y, z.')
 ]),
 P('Tâm tỉ cự với tổng hệ số âm',[
  M(r'S=1-2-2=-3','Tổng hệ số bằng âm ba, nên ta chờ đợi một giá trị lớn nhất.'),
  M(r'I=\left(-\frac23;\frac43;\frac43\right)','Chia tổng tọa độ có trọng số cho âm ba, được I như trên.'),
  M(r'K=4-8-8-(-3)\cdot4=0','O I bình bằng bốn. Tính K bằng âm mười hai trừ âm mười hai, tức bằng không.'),
  M(r'F=-3MI^2\le0','Biểu thức bằng âm ba nhân M I bình, nên không bao giờ dương.')
 ],'center'),
 P('Cực đại và nhận xét',[
  M(r'F=0\iff M=I','Giá trị bằng không đạt được duy nhất khi M trùng I.'),
  M(r'\boxed{F_{\max}=0;\quad M\left(-\frac23;\frac43;\frac43\right)}','Giá trị lớn nhất bằng không, tại tâm vừa tìm.',True),
  T('Không có giá trị nhỏ nhất khi M tự do.','Nếu đi xa I vô hạn, âm ba M I bình tiến tới âm vô hạn. Vì vậy bài này không có giá trị nhỏ nhất.')
 ],'opt')],
'B04':[
 P('Đề bài • Phân loại theo tham số',[
  M(r'A(-1;0;0),\ B(1;0;0),\ O(0;0;0)','Cho A và B đối xứng qua gốc tọa độ.'),
  M(r'F_\mu=MA^2+MB^2+\mu MO^2','Với M tự do, phân loại cực trị của F theo tham số mu.'),
  T('Cần xét cả trường hợp tổng trọng số bằng 0.','Không bỏ qua giá trị mu làm tổng trọng số bằng không. Tại đó ta không được chia để tính tâm tỉ cự.')
 ]),
 P('Khai triển đủ để xử lý mọi tham số',[
  M(r'M(x;y;z),\quad MA^2=(x+1)^2+y^2+z^2','Đặt tọa độ M, viết khoảng cách tới A.'),
  M(r'MB^2=(x-1)^2+y^2+z^2','Khoảng cách tới B có dấu âm trong x trừ một.'),
  M(r'F_\mu=(2+\mu)(x^2+y^2+z^2)+2','Hai số hạng tuyến tính theo x triệt tiêu. Biểu thức chỉ còn hai cộng hai cộng mu nhân M O bình.'),
  M(r'F_\mu=(2+\mu)MO^2+2','Dạng này đúng với cả mu bằng âm hai, không cần chia cho tổng trọng số.')
 ],'center'),
 P('Hai trường hợp có cực trị duy nhất',[
  M(r'\mu>-2:\quad F_\mu\ge2,\quad F_\mu=2\iff M=O','Nếu mu lớn hơn âm hai, hệ số M O bình dương. Giá trị nhỏ nhất bằng hai, duy nhất tại O.'),
  M(r'\mu<-2:\quad F_\mu\le2,\quad F_\mu=2\iff M=O','Nếu mu nhỏ hơn âm hai, hệ số âm. Giá trị lớn nhất bằng hai, duy nhất tại O.'),
  T('Ở mỗi trường hợp, phía cực trị còn lại không bị chặn.','Với hệ số dương không có lớn nhất; với hệ số âm không có nhỏ nhất, vì M có thể đi xa vô hạn.')
 ],'opt'),
 P('Trường hợp suy biến không có tâm tỉ cự duy nhất',[
  M(r'\mu=-2:\quad F_\mu\equiv2','Mu bằng âm hai làm hệ số M O bình bằng không. F luôn bằng hai với mọi điểm M.'),
  M(r'\boxed{F_{\min}=F_{\max}=2;\quad \forall M}','Cả nhỏ nhất và lớn nhất đều bằng hai, mọi điểm M đều đạt.',True),
  T('S bằng 0 không tự động có nghĩa là không có cực trị.','Ở bài này tổng trọng số và tổng vectơ có trọng số đều bằng không, nên F là hằng số. Một bài tổng trọng số bằng không khác sẽ cho kết quả khác.')
 ],'constant')],
'B05':[
 P('Đề bài • M được chọn trên một trong ba trục',[
  M(r'A(4;0;0),\ B(0;2;0),\ C(0;0;6)','Cho ba điểm A, B, C trên ba trục với tọa độ như trên.'),
  M(r'F=MA^2+MB^2+MC^2','Tìm giá trị nhỏ nhất của tổng ba bình phương khoảng cách.'),
  T('M thuộc Ox hoặc Oy hoặc Oz; phải so sánh cả ba khả năng.','M được chọn trên một trong ba trục tọa độ. Không được tùy ý chọn một trục rồi kết luận cho cả bài.')
 ]),
 P('Gom về khoảng cách tới một điểm',[
  M(r'I\left(\frac43;\frac23;2\right),\quad S=3','Tâm là trọng tâm ba điểm, có tọa độ bốn phần ba, hai phần ba, hai.'),
  M(r'K=16+4+36-3\cdot\frac{56}{9}=\frac{112}{3}','Tính K bằng một trăm mười hai phần ba.'),
  M(r'F=3MI^2+\frac{112}{3}','Vậy ta tìm điểm trên ba trục gần I nhất, nhưng sẽ thực hiện bằng bình phương tọa độ.')
 ],'center'),
 P('Tính riêng trên từng trục, không dùng công thức khoảng cách tới đường',[
  M(r'M\in Ox:\ MI^2=\left(x-\frac43\right)^2+\frac{40}{9}\ge\frac{40}{9}','Trên O x, hai tọa độ còn lại bằng không. Bình phương khoảng cách nhỏ nhất khi x bằng bốn phần ba.'),
  M(r'M\in Oy:\ MI^2=\left(y-\frac23\right)^2+\frac{52}{9}\ge\frac{52}{9}','Trên O y, giá trị nhỏ nhất của M I bình là năm mươi hai phần chín.'),
  M(r'M\in Oz:\ MI^2=(z-2)^2+\frac{20}{9}\ge\frac{20}{9}','Trên O z, giá trị nhỏ nhất là hai mươi phần chín, nhỏ hơn cả hai trường hợp trước.')
 ],'axes'),
 P('So sánh và kết luận toàn bài',[
  M(r'F_{Ox,\min}=\frac{152}{3},\quad F_{Oy,\min}=\frac{164}{3},\quad F_{Oz,\min}=44','Thay lại vào F, ba giá trị nhỏ nhất lần lượt là một trăm năm mươi hai phần ba, một trăm sáu mươi bốn phần ba và bốn mươi bốn.'),
  M(r'\boxed{M(0;0;2),\quad F_{\min}=44}','Đáp án là điểm không, không, hai trên O z; giá trị nhỏ nhất bốn mươi bốn.',True),
  T('Trung bình tọa độ cho I; ràng buộc quyết định M.', 'Tâm I không thuộc trục nào. Ràng buộc khiến nghiệm tối ưu khác I.')
 ],'opt')],
'B06':[
 P('Đề bài • Đây là độ dài của tổng vectơ',[
  M(r'A(2;0;0),\ B(0;4;0),\ C(0;0;4)','Cho ba điểm như trên. M nằm trong mặt tọa độ O x y.'),
  M(r'L=\left\lVert2\overrightarrow{MA}-\overrightarrow{MB}+3\overrightarrow{MC}\right\rVert','Tìm nhỏ nhất của độ dài tổng vectơ hai M A trừ M B cộng ba M C.'),
  T('Không nhầm với 2MA² − MB² + 3MC².','Đây là độ dài của một tổng vectơ, không phải tổng các bình phương khoảng cách có dấu. Ta cần một đồng nhất thức vectơ khác.')
 ]),
 P('Rút gọn tổng vectơ trước khi lấy độ dài',[
  M(r'S=2-1+3=4,\qquad I(1;-1;3)','Tổng trọng số bằng bốn và tâm tỉ cự có tọa độ một, âm một, ba.'),
  M(r'2\overrightarrow{IA}-\overrightarrow{IB}+3\overrightarrow{IC}=\vec0','Từ định nghĩa tâm, tổng các vectơ xuất phát tại I bằng không.'),
  M(r'2\overrightarrow{MA}-\overrightarrow{MB}+3\overrightarrow{MC}=4\overrightarrow{MI}','Phân tích qua I. Các vectơ I A, I B, I C triệt tiêu, còn bốn vectơ M I.'),
  M(r'L=4MI','Lấy độ dài được L bằng bốn lần M I.')
 ],'center'),
 P('Dùng định nghĩa tọa độ trong Oxy',[
  M(r'M\in Oxy\Rightarrow M(x;y;0)','Điểm trong mặt tọa độ O x y có tọa độ đứng bằng không. Đây là tính chất tọa độ, không cần phương trình mặt phẳng tổng quát.'),
  M(r'MI^2=(x-1)^2+(y+1)^2+9\ge9','M I bình bằng hai bình phương không âm cộng chín, nên M I ít nhất bằng ba.'),
  M(r'MI=3\iff x=1,\ y=-1','Dấu bằng xảy ra đồng thời khi x bằng một và y bằng âm một.')
 ]),
 P('Kết luận độ dài, không kết luận bình phương',[
  M(r'\boxed{L_{\min}=12;\quad M(1;-1;0)}','Độ dài nhỏ nhất là mười hai, tại M có tọa độ một, âm một, không.',True),
  T('Nếu bài hỏi bình phương độ dài thì đáp số là 144.','Bài hỏi độ dài, nên đáp số là mười hai. Nếu hỏi bình phương của độ dài tổng vectơ, đáp số mới là một trăm bốn mươi bốn.'),
  T('Không dùng phương trình mặt phẳng hoặc công thức hình chiếu tổng quát.', 'Toàn bộ bước tối ưu chỉ dùng hai bình phương không âm.')
 ],'opt')],
'B07':[
 P('Đề bài • M cách đều hai điểm',[
  M(r'A(-2;0;0),\ B(4;0;0),\ C(0;3;6)','Cho ba điểm A, B, C như trên.'),
  M(r'MA=MB,\qquad F=MA^2+MB^2+2MC^2','M cách đều A và B. Tìm giá trị nhỏ nhất của M A bình cộng M B bình cộng hai M C bình.'),
  T('Chuyển điều kiện cách đều thành điều kiện về tọa độ.', 'Không gọi tên hay lập phương trình một mặt phẳng. Ta chỉ khai triển hai khoảng cách bằng nhau.')
 ]),
 P('Khai triển ràng buộc rồi tính tâm',[
  M(r'(x+2)^2+y^2+z^2=(x-4)^2+y^2+z^2','Bình phương hai khoảng cách bằng nhau. Hai số hạng y bình và z bình triệt tiêu.'),
  M(r'12x=12\quad\Rightarrow\quad x=1','Còn mười hai x bằng mười hai, nên hoành độ của mọi điểm hợp lệ là một.'),
  M(r'I\left(\frac12;\frac32;3\right),\quad S=4,\quad K=64','Tính tâm có trọng số một, một, hai: một phần hai, ba phần hai, ba. Hằng số K bằng sáu mươi bốn.'),
  M(r'F=4MI^2+64','Biểu thức trở thành bốn M I bình cộng sáu mươi bốn.')
 ],'center'),
 P('Hoành độ cố định, hai tọa độ còn lại tự do',[
  M(r'M(1;y;z),\quad MI^2=\frac14+\left(y-\frac32\right)^2+(z-3)^2','Thay hoành độ một. M I bình có số hạng cố định một phần tư và hai bình phương.'),
  M(r'MI^2\ge\frac14;\quad =\iff(y;z)=(\tfrac32;3)','Giá trị nhỏ nhất đạt khi y bằng ba phần hai và z bằng ba.'),
  M(r'F\ge4\cdot\frac14+64=65','Thay vào F được cận dưới sáu mươi lăm.')
 ]),
 P('Kiểm tra lại cả điều kiện đề bài',[
  M(r'\boxed{M\left(1;\frac32;3\right),\quad F_{\min}=65}','Đáp án là một, ba phần hai, ba; giá trị nhỏ nhất sáu mươi lăm.',True),
  M(r'MA^2=MB^2=9+\frac94+9=\frac{81}{4}','Thay tọa độ đáp án, khoảng cách bình phương tới A và B đều bằng tám mươi mốt phần tư.'),
  T('Tâm I không thỏa cách đều; không chọn I làm đáp án.', 'Tâm I có hoành độ một phần hai nên không thỏa điều kiện. Ta phải tối ưu trên các điểm có hoành độ một.')
 ],'opt')],
'B08':[
 P('Đề bài • M chỉ nằm trên một đoạn',[
  M(r'A(0;0;0),\ B(4;4;0),\ P(1;2;3),\ Q(3;4;1)','Cho đoạn A B và hai điểm P, Q trong không gian.'),
  M(r'M\in AB,\qquad F=MP^2+3MQ^2','M thuộc đoạn A B, kể cả hai đầu mút. Tìm nhỏ nhất của M P bình cộng ba M Q bình.'),
  T('M được chia đoạn theo tỉ số; không xét cả đường kéo dài.', 'Ta chỉ dùng tỉ số M A trên A B. Điều kiện t từ không đến một là bắt buộc.')
 ]),
 P('Tâm tỉ cự và tọa độ điểm chia đoạn',[
  M(r'I\left(\frac52;\frac72;\frac32\right),\quad K=14+3\cdot26-83=9','Tâm có tọa độ năm phần hai, bảy phần hai, ba phần hai. K bằng mười bốn cộng ba nhân hai mươi sáu, trừ tám mươi ba, được chín. Vậy F bằng bốn M I bình cộng chín.'),
  M(r't=\frac{AM}{AB}\in[0,1],\quad\overrightarrow{AM}=t\overrightarrow{AB}','Đặt t là tỉ số độ dài trên đoạn. Vì M thuộc đoạn nên vectơ A M cùng hướng với vectơ A B và bằng t lần.'),
  M(r'M(4t;4t;0),\quad 0\le t\le1','Suy ra tọa độ M là bốn t, bốn t, không. Đây là công thức điểm chia đoạn, không phải học phương trình đường thẳng.')
 ],'center'),
 P('Hoàn thành bình phương một biến',[
  M(r'MI^2=\left(4t-\frac52\right)^2+\left(4t-\frac72\right)^2+\frac94','Thay tọa độ M vào công thức khoảng cách.'),
  M(r'MI^2=32\left(t-\frac34\right)^2+\frac{11}{4}','Khai triển rồi hoàn thành bình phương, được ba mươi hai nhân t trừ ba phần tư bình cộng mười một phần tư.'),
  M(r'F=128\left(t-\frac34\right)^2+20','Thế vào F, được cận dưới hai mươi.'),
  M(r't_*=\frac34\in[0,1]','Tỉ số tối ưu ba phần tư nằm trong miền hợp lệ.')
 ]),
 P('Kết luận vị trí và giá trị',[
  M(r'\boxed{M(3;3;0),\quad F_{\min}=20}','Điểm tối ưu có tọa độ ba, ba, không. Giá trị nhỏ nhất bằng hai mươi.',True),
  M(r'AM:MB=3:1','M chia đoạn theo tỉ số ba trên một.'),
  T('Đã kiểm tra t trong đoạn và điều kiện dấu bằng.', 'Nếu bỏ kiểm tra miền t, các bài tiếp theo sẽ dẫn tới đáp án sai.')
 ],'opt')],
'B09':[
 P('Đề bài • Cùng đoạn, tâm ở vị trí khác',[
  M(r'A(0;0;0),\ B(4;4;0),\ P(6;6;2),\ Q(4;4;0)','Giữ đoạn A B, thay hai điểm P và Q.'),
  M(r'M\in AB,\qquad F=MP^2+MQ^2','Tìm nhỏ nhất tổng hai bình phương khoảng cách, với M chỉ thuộc đoạn A B.'),
  T('Nghiệm của bình phương tự do có thể nằm ngoài đoạn.', 'Không suy đoán rằng điểm gần tâm nhất luôn nằm bên trong đoạn.')
 ]),
 P('Tâm và bình phương có nghiệm ngoài miền',[
  M(r'I(5;5;1),\quad K=76+32-2\cdot51=6','Tâm là trung điểm P Q: năm, năm, một. Tính K bằng bảy mươi sáu cộng ba mươi hai trừ hai nhân năm mươi mốt, được sáu. Do đó F bằng hai M I bình cộng sáu.'),
  M(r'M(4t;4t;0),\quad t\in[0,1]','Dùng tỉ số chia đoạn, vẫn có t từ không đến một.'),
  M(r'MI^2=32\left(t-\frac54\right)^2+1','Khoảng cách bình phương được hoàn thành quanh t bằng năm phần tư.'),
  M(r'F=64\left(t-\frac54\right)^2+8','F bằng sáu mươi bốn nhân t trừ năm phần tư bình cộng tám.')
 ],'center'),
 P('Đầu mút mới là điểm tối ưu',[
  M(r'0\le t\le1\Rightarrow\left|t-\frac54\right|\ge\frac14','Trên đoạn từ không tới một, t gần năm phần tư nhất tại một. Khoảng cách ít nhất bằng một phần tư.'),
  M(r'F\ge64\cdot\frac1{16}+8=12','Cận dưới của F là mười hai.'),
  M(r'\boxed{t=1;\quad M=B(4;4;0);\quad F_{\min}=12}','Dấu bằng tại t bằng một, tức M là đầu mút B. Giá trị nhỏ nhất mười hai.',True),
  T('Không chọn t = 5/4: đó là điểm trên phần kéo dài.', 'Nghiệm tự do t bằng năm phần tư bị loại. Đáp án phải thỏa ràng buộc đoạn thẳng.')
 ],'opt')],
'B10':[
 P('Đề bài • M nằm trong một hình hộp tọa độ',[
  M(r'P(4;-2;3),\quad Q(2;0;1),\quad F=MP^2+MQ^2','Cho P và Q như trên. Tìm nhỏ nhất và lớn nhất của tổng hai bình phương khoảng cách.'),
  M(r'0\le x\le2,\quad0\le y\le3,\quad0\le z\le1','M có ba tọa độ trong các khoảng cho trước. Miền là một hình hộp, gồm cả mặt và cạnh.'),
  T('Tối ưu ba tọa độ riêng rẽ; không cần phương trình các mặt.', 'Các khoảng độc lập nên ta xét từng bình phương theo từng tọa độ.')
 ]),
 P('Gom về tâm và tách ba bình phương',[
  M(r'I(3;-1;2)','Tâm là trung điểm P Q, có tọa độ ba, âm một, hai.'),
  M(r'K=29+5-2(9+1+4)=6','Tính K bằng hai mươi chín cộng năm, trừ hai nhân mười bốn, được sáu.'),
  M(r'F=2\bigl[(x-3)^2+(y+1)^2+(z-2)^2\bigr]+6','Biểu thức tách thành ba bình phương độc lập.'),
  T('I nằm ngoài hình hộp ở cả ba tọa độ.', 'Tâm không hợp lệ. Ta không chọn I, mà chọn điểm trong hình hộp gần I nhất hoặc xa I nhất.')
 ],'center'),
 P('Tìm nhỏ nhất và ghi đủ dấu bằng',[
  M(r'(x-3)^2\ge1,\quad(y+1)^2\ge1,\quad(z-2)^2\ge1','Trên ba khoảng cho trước, các bình phương đều ít nhất bằng một.'),
  M(r'F\ge2(1+1+1)+6=12','Cộng các cận dưới được F ít nhất bằng mười hai.'),
  M(r'\boxed{F_{\min}=12;\quad M(2;0;1)}','Ba dấu bằng đồng thời khi x bằng hai, y bằng không, z bằng một.',True)
 ],'opt'),
 P('Tìm lớn nhất cũng bằng ba khoảng tọa độ',[
  M(r'(x-3)^2\le9,\quad(y+1)^2\le16,\quad(z-2)^2\le4','Các bình phương lớn nhất lần lượt là chín, mười sáu và bốn.'),
  M(r'F\le2(9+16+4)+6=64','Cộng các cận trên được sáu mươi bốn.'),
  M(r'\boxed{F_{\max}=64;\quad M(0;3;0)}','Ba dấu bằng đồng thời tại x không, y ba, z không. Đây là một đỉnh của hình hộp.',True)
 ],'max'),
 P('Vì sao không chỉ thử tám đỉnh ngay từ đầu?',[
  T('Cực đại ở một đỉnh trong bài này; cực tiểu không luôn ở đỉnh.', 'Ở bài này, cực tiểu tình cờ cũng là một đỉnh. Nếu tâm có tọa độ nằm giữa các khoảng, điểm gần nhất có thể ở mặt, cạnh hoặc bên trong.'),
  M(r'I(1;1;\tfrac12)\Rightarrow \min MI=0\iff M=I','Chẳng hạn một tâm một, một, một phần hai nằm bên trong hình hộp thì chính tâm là điểm gần nhất, không phải một đỉnh.'),
  T('Lời giải phải chứng minh cận và khả năng đạt đồng thời.', 'Tìm vài giá trị để dự đoán chưa đủ. Các cận tọa độ và dấu bằng đã chứng minh hoàn chỉnh cả hai cực trị.')
 ])],
'B11':[
 P('Đề bài • Điểm chỉ nằm trong tam giác',[
  M(r'O(0;0;0),\ A(4;0;0),\ B(0;4;0)','M thuộc tam giác O A B, kể cả cạnh và đỉnh.'),
  M(r'P(4;4;3),\ Q(2;2;1),\quad F=MP^2+MQ^2','Cho hai điểm P, Q. Tìm nhỏ nhất của tổng hai bình phương khoảng cách.'),
  T('Tâm và điểm cùng hai tọa độ ngang chưa chắc nằm trong tam giác.', 'Ràng buộc là cả tam giác, không phải toàn bộ mặt tọa độ O x y.')
 ]),
 P('Miền tọa độ và tâm tỉ cự',[
  M(r'M(x;y;0),\quad x\ge0,\ y\ge0,\ x+y\le4','Theo hình tam giác vuông, tọa độ đứng bằng không; hai tọa độ ngang không âm và tổng không quá bốn. Có thể suy ra bằng tỉ số chia đoạn trong tam giác.'),
  M(r'I(3;3;2),\quad K=41+17-2\cdot22=6','Tâm là trung điểm P Q, có tọa độ ba, ba, hai. O P bình bằng bốn mươi mốt, O Q bình bằng mười bảy, O I bình bằng hai mươi hai, nên K bằng sáu và F bằng hai M I bình cộng sáu.'),
  M(r'J(3;3;0):\quad3+3>4','Điểm J cùng hai tọa độ ngang với I nhưng tổng bằng sáu, nằm ngoài tam giác.'),
  T('Không chọn J làm đáp án; cần tối ưu trong miền thật.', 'Dừng lại ở J là một sai lầm. Ta cần một bất đẳng thức sử dụng điều kiện tổng x cộng y không quá bốn.')
 ],'outside'),
 P('Dùng một bất đẳng thức hai bình phương',[
  M(r'(x-3)^2+(y-3)^2\ge\frac{(x+y-6)^2}{2}','Theo bất đẳng thức tổng hai bình phương, vế trái ít nhất bằng bình phương tổng chia hai.'),
  M(r'x+y\le4\Rightarrow x+y-6\le-2\Rightarrow(x+y-6)^2\ge4','Vì tổng không quá bốn, tổng trừ sáu không quá âm hai, bình phương ít nhất bằng bốn.'),
  M(r'MI^2=(x-3)^2+(y-3)^2+4\ge2+4=6','Cộng độ chênh đứng bình phương là bốn, được M I bình ít nhất bằng sáu.'),
  M(r'F\ge2\cdot6+6=18','Suy ra F ít nhất bằng mười tám.')
 ],'center'),
 P('Điều kiện đạt đồng thời hai dấu bằng',[
  M(r'x-3=y-3,\quad x+y=4\Rightarrow x=y=2','Bất đẳng thức hai bình phương đạt dấu bằng khi x bằng y. Cận tổng đạt dấu bằng khi x cộng y bằng bốn.'),
  M(r'\boxed{M(2;2;0),\quad F_{\min}=18}','Vậy M là hai, hai, không; giá trị nhỏ nhất mười tám.',True),
  M(r'M\in AB,\quad AM=MB','Điểm này là trung điểm cạnh A B, hợp lệ trong tam giác.'),
  T('Giải bằng tọa độ và bất đẳng thức; không dùng khoảng cách tới mặt phẳng.', 'Từng bước chỉ cần tọa độ và hai bình phương. Đây là bài ràng buộc mà tâm không nằm trong miền.')
 ],'opt')],
'B12':[
 P('Đề bài • Từ tự do tới một mặt của tứ diện',[
  M(r'O(0;0;0),\ A(4;0;0),\ B(0;4;0),\ C(0;0;4)','Cho tứ diện O A B C có ba cạnh từ O bằng bốn và vuông góc từng đôi.'),
  M(r'F=MO^2+MA^2+MB^2+MC^2','Tìm nhỏ nhất của F khi M tự do, rồi khi M thuộc mặt tam giác A B C.'),
  T('Hai miền khác nhau sẽ cho hai đáp án khác nhau.', 'Đọc kỹ điều kiện M. Tâm tứ diện có thể hợp lệ cho bài tự do nhưng không nằm trên mặt tam giác yêu cầu.')
 ]),
 P('Trường hợp M tự do',[
  M(r'G(1;1;1),\quad K=48-4\cdot3=36','Trọng tâm bốn đỉnh là một, một, một. Hằng số K bằng ba mươi sáu.'),
  M(r'F=4MG^2+36','Tổng bốn bình phương bằng bốn M G bình cộng ba mươi sáu.'),
  M(r'\boxed{F_{\min}=36\iff M=G}\quad(M\in\mathbb R^3)','Với M tự do, nhỏ nhất bằng ba mươi sáu tại G.',True)
 ],'center'),
 P('Khi M thuộc tam giác ABC: dùng tổ hợp vectơ',[
  M(r'\overrightarrow{OM}=u\overrightarrow{OA}+v\overrightarrow{OB}+w\overrightarrow{OC}', 'Điểm trong tam giác A B C được biểu diễn bằng tổ hợp các vectơ tới ba đỉnh, với hệ số không âm có tổng bằng một.'),
  M(r'u,v,w\ge0,\quad u+v+w=1,\quad M(4u;4v;4w)','Do tọa độ ba đỉnh, tọa độ M lần lượt là bốn u, bốn v, bốn w.'),
  M(r'MG^2=(4u-1)^2+(4v-1)^2+(4w-1)^2','Viết M G bình bằng ba bình phương.'),
  M(r'MG^2\ge\frac{[4(u+v+w)-3]^2}{3}=\frac13','Tổng ba bình phương ít nhất bằng bình phương tổng chia ba. Tổng u v w bằng một nên cận dưới là một phần ba.')
 ]),
 P('Dấu bằng cho nghiệm ngay trong mặt tam giác',[
  M(r'4u-1=4v-1=4w-1\Rightarrow u=v=w=\frac13','Dấu bằng xảy ra khi ba số bằng nhau. Với tổng hệ số bằng một, mỗi hệ số bằng một phần ba.'),
  M(r'\boxed{M\left(\frac43;\frac43;\frac43\right),\quad F_{\min}=\frac{112}{3}}','M là trọng tâm tam giác A B C, có ba tọa độ bốn phần ba. Giá trị nhỏ nhất một trăm mười hai phần ba.',True),
  T('Không lập phương trình mặt ABC, cũng không dùng công thức khoảng cách.', 'Ta đã giải trên một mặt tam giác hoàn toàn bằng vectơ, tọa độ và bất đẳng thức. Không cần phương trình mặt phẳng.')
 ],'opt')],
'B13':[
 P('Đề bài ngược • Chọn C để đặt cực tiểu vào đúng vị trí',[
  M(r'A(1;0;0),\ B(0;1;0),\ I(1;1;1)','Cho A và B, muốn điểm cực tiểu duy nhất nằm ở I có tọa độ một, một, một.'),
  M(r'F=2MA^2+3MB^2+MC^2','Hãy tìm tọa độ C để F đạt nhỏ nhất tại I, với M tự do.'),
  T('C chưa biết: hình chỉ hiện C sau khi đã tìm được.', 'Đây là bài thiết kế ngược. Ta không tìm tâm từ các điểm đã biết, mà chọn một điểm để tâm nằm tại đích.')
 ]),
 P('Điều kiện cần và đủ từ tâm tỉ cự',[
  M(r'S=2+3+1=6>0','Tổng trọng số dương nên điểm cực tiểu duy nhất chính là tâm tỉ cự.'),
  M(r'2\overrightarrow{OA}+3\overrightarrow{OB}+\overrightarrow{OC}=6\overrightarrow{OI}','Muốn tâm là I, tổng tọa độ có trọng số phải bằng sáu lần tọa độ I.'),
  M(r'\overrightarrow{OC}=6\overrightarrow{OI}-2\overrightarrow{OA}-3\overrightarrow{OB}','Chuyển vế để tìm vectơ O C. Đây vừa là điều kiện cần, vừa là điều kiện đủ.')
 ],'center'),
 P('Tìm C theo ba tọa độ',[
  M(r'x_C=6-2=4,\quad y_C=6-3=3,\quad z_C=6','Tính riêng từng thành phần, được bốn, ba, sáu.'),
  M(r'\boxed{C(4;3;6)}','Điểm cần thiết kế là C có tọa độ bốn, ba, sáu.',True),
  M(r'\frac{(2;0;0)+(0;3;0)+(4;3;6)}6=(1;1;1)','Thay trở lại kiểm tra: tổng tọa độ có trọng số là sáu, sáu, sáu. Chia cho sáu, đúng bằng tọa độ của I.')
 ],'reveal'),
 P('Kiểm tra cả giá trị cực tiểu',[
  M(r'K=2+3+(16+9+36)-6\cdot3=48','Tổng trọng số nhân độ dài từ O bình là sáu mươi sáu. Trừ sáu nhân ba, được K bằng bốn mươi tám.'),
  M(r'F=6MI^2+48','Với C vừa tìm, F bằng sáu M I bình cộng bốn mươi tám.'),
  M(r'\boxed{F_{\min}=48\iff M=I}','Giá trị nhỏ nhất là bốn mươi tám, duy nhất tại đúng đích I.',True)
 ],'opt')],
'B14':[
 P('Đề bài • Hai hàm trông giống nhưng không cùng nghiệm',[
  M(r'A(0;0;0),\ B(4;0;0)','Cho A và B cách nhau bốn đơn vị trên O x.'),
  M(r'F=MA^2+MB^2,\qquad G=MA+MB','M tự do. Tìm nhỏ nhất của F và G, và tìm tất cả điểm đạt mỗi giá trị nhỏ nhất.'),
  T('Không bỏ sót yêu cầu tìm tất cả các điểm đạt dấu bằng.', 'Một hàm có điểm tối ưu duy nhất, hàm kia có vô số điểm tối ưu. Đừng dùng tâm tỉ cự cho sai loại biểu thức.')
 ]),
 P('Tổng bình phương: nghiệm duy nhất',[
  M(r'I(2;0;0),\qquad F=2MI^2+8','Tâm là trung điểm A B. Đồng nhất thức cho F bằng hai M I bình cộng tám.'),
  M(r'\boxed{F_{\min}=8\iff M=I(2;0;0)}','Nhỏ nhất của F là tám, duy nhất tại trung điểm.',True),
  T('Đây là loại biểu thức mà công cụ tâm tỉ cự xử lý trực tiếp.', 'Bởi vì các khoảng cách được bình phương, số hạng tích vô hướng mới triệt tiêu theo đồng nhất thức.')
 ],'center'),
 P('Tổng khoảng cách thường: dùng bất đẳng thức tam giác',[
  M(r'MA+MB\ge AB=4','Theo bất đẳng thức tam giác, tổng hai khoảng cách luôn ít nhất bằng bốn.'),
  M(r'MA+MB=AB\iff M\in AB','Dấu bằng khi và chỉ khi M thuộc đoạn A B, gồm cả hai đầu mút.'),
  M(r'\boxed{G_{\min}=4;\quad\forall M\in AB}','Nhỏ nhất của G là bốn; mọi điểm trên đoạn A B đều đạt.',True),
  T('Không chỉ có trung điểm: toàn bộ đoạn đều tối ưu cho G.', 'Hãy quan sát M chạy trên đoạn: tổng khoảng cách vẫn bằng bốn, trong khi tổng bình phương thay đổi.')
 ],'lengths'),
 P('Một điểm kiểm chứng sự khác nhau',[
  M(r'M(1;0;0):\quad MA=1,\quad MB=3','Chọn điểm M có hoành độ một trên đoạn.'),
  M(r'G=1+3=4,\qquad F=1^2+3^2=10>8','G đã nhỏ nhất bằng bốn, nhưng F bằng mười, lớn hơn cực tiểu tám.'),
  T('Không tự ý thêm hoặc bỏ bình phương trong bài cực trị.', 'Hai hàm cho hai tập điểm tối ưu khác nhau. Đây là một lỗi phương pháp thường gặp.')
 ])],
'B15':[
 P('Đề bài • Hai trọng số triệt tiêu',[
  M(r'A(0;0;0),\ B(2;0;0),\quad F=MA^2-MB^2','Cho A là gốc và B có hoành độ hai. Xét hiệu hai bình phương khoảng cách.'),
  T('Phần 1: M tự do. Phần 2: hoành độ M từ 0 đến 3.', 'Tìm cực trị khi M tự do. Sau đó tìm cực trị nếu hoành độ M từ không đến ba; hai tọa độ còn lại tùy ý.'),
  M(r'S=1-1=0','Tổng trọng số bằng không. Không có công thức tâm bằng chia tổng tọa độ cho S.')
 ]),
 P('Khai triển thay vì chia cho 0',[
  M(r'M(x;y;z):\quad F=x^2+y^2+z^2-[(x-2)^2+y^2+z^2]','Khai triển khoảng cách với tọa độ M. Hai phần y bình và z bình triệt tiêu.'),
  M(r'\boxed{F=4x-4}','F chỉ phụ thuộc hoành độ, bằng bốn x trừ bốn.',True),
  M(r'x\to+\infty\Rightarrow F\to+\infty,\quad x\to-\infty\Rightarrow F\to-\infty','Khi x đi ra dương vô hạn F đi ra dương vô hạn, và tương tự ở phía âm.'),
  T('M tự do: không có giá trị lớn nhất, cũng không có nhỏ nhất.', 'Vì không bị chặn ở cả hai phía, biểu thức không có cực trị toàn cục khi M tự do.')
 ],'linear'),
 P('Hoành độ bị chặn thì cực trị xuất hiện',[
  M(r'0\le x\le3\Rightarrow -4\le F=4x-4\le8','Trên khoảng hoành độ từ không đến ba, F nằm từ âm bốn đến tám.'),
  M(r'\boxed{F_{\min}=-4\iff M(0;y;z),\quad y,z\in\mathbb R}','Nhỏ nhất âm bốn tại mọi điểm có hoành độ không, hai tọa độ kia tùy ý.',True),
  M(r'\boxed{F_{\max}=8\iff M(3;y;z),\quad y,z\in\mathbb R}','Lớn nhất tám tại mọi điểm có hoành độ ba, hai tọa độ kia tùy ý.',True),
  T('Cực trị không duy nhất; phải nêu toàn bộ điểm đạt.', 'Không chỉ ghi một ví dụ điểm. Bài yêu cầu tất cả các điểm, và y z không tham gia vào biểu thức.')
 ],'linear_bound'),
 P('So sánh với bài tham số ở giá trị suy biến',[
  T('Cùng S = 0 nhưng một bài hằng số, một bài tuyến tính.', 'Ở bài tham số mu bằng âm hai, F là hằng số. Ở đây F là hàm tuyến tính của x. Hai tình huống đều có tổng trọng số bằng không.'),
  M(r'S=0:\quad F=-2\overrightarrow{OM}\cdot\sum_iw_i\overrightarrow{OA_i}+\sum_iw_iOA_i^2','Khai triển tổng có trọng số cho thấy, khi S bằng không, phần M O bình biến mất, còn phần tuyến tính và hằng số.'),
  T('Xét tổng vectơ có trọng số, không đoán chỉ từ tổng hệ số.', 'Nếu tổng vectơ có trọng số cũng bằng không, F là hằng số. Nếu không, M tự do sẽ làm F không bị chặn.')
 ])]
}

PAGES['B11'].insert(1,P('Tự suy ra miền tọa độ từ công thức chia đoạn',[
 M(r'\overrightarrow{OM}=u\overrightarrow{OA}+v\overrightarrow{OB}', 'Tam giác có một đỉnh là O, nên số hạng tới O bằng không. Hai hệ số của A và B không âm, tổng không quá một.'),
 M(r'u,v\ge0,\quad u+v\le1,\quad M(4u;4v;0)', 'Đặt hệ số tại đỉnh O là một trừ u trừ v. Tọa độ M là bốn u, bốn v, không.'),
 M(r'x=4u,\ y=4v\Rightarrow x,y\ge0,\quad x+y\le4', 'Suy ra hai tọa độ ngang không âm, tổng không quá bốn. Ngược lại, chia tọa độ cho bốn cho hai hệ số hợp lệ, nên điều kiện mô tả đúng cả tam giác.')
]))


def build_lessons():
    lessons=[{'id':'INTRO','title':'Tâm tỉ cự trong Oxyz • Nền tảng cần dùng','model':json.loads(json.dumps(CASES[0])),'pages':INTRO}]
    for c in CASES:lessons.append({'id':c['id'],'title':c['title'],'model':json.loads(json.dumps(c)),'pages':PAGES[c['id']]})
    lessons.append({'id':'END','title':'Tổng kết • Đúng tâm, đúng miền, đúng biểu thức','model':json.loads(json.dumps(CASES[10])),'pages':[
     P('Ba câu hỏi trước khi tìm cực trị',[
      M(r'F=\sum_iw_iMA_i^2,\quad S=\sum_iw_i','Đầu tiên xác định đúng loại biểu thức và tổng trọng số.'),
      T('S khác 0? Nếu có, tính I và K.', 'Nếu S khác không, tính tâm và hằng số. Nếu S bằng không, khai triển trực tiếp, không chia.'),
      T('M tự do hay thuộc một miền cho trước?', 'Tiếp theo kiểm tra miền M. Tâm ngoài miền không được dùng làm đáp án.'),
      T('Dấu bằng có đạt, có duy nhất hay không?', 'Cuối cùng kiểm tra dấu bằng, nêu đúng một điểm hay cả tập các điểm tối ưu.')
     ],'center'),
     P('Các công cụ phù hợp trình độ hiện tại',[
      T('Trục và mặt tọa độ: cố định các tọa độ bằng định nghĩa.', 'Trên trục, hai tọa độ bằng không. Trong mặt tọa độ, một tọa độ bằng không. Chỉ cần hoàn thành bình phương.'),
      T('Đoạn: tỉ số chia đoạn; hình hộp: từng khoảng tọa độ.', 'Trên đoạn, dùng tỉ số chia đoạn với miền từ không tới một. Trong hình hộp, tối ưu từng tọa độ riêng rẽ.'),
      T('Tam giác và tứ diện: tổ hợp vectơ, bất đẳng thức, dấu bằng.', 'Trong tam giác hoặc trên một mặt tứ diện, dùng hệ số không âm và tổng bằng một, rồi áp dụng bất đẳng thức bình phương.'),
      T('Không cần các phương trình hình học chưa học.', 'Không bài nào trong video đòi hỏi phương trình đường thẳng, mặt phẳng hoặc mặt cầu.')
     ],'opt')
    ]})
    return lessons

# ======================= HÌNH OXYZ THẬT TRONG 3D =======================
SCENE_SOURCE=r'''
from manim import *
import numpy as np
import math,json,textwrap
from pathlib import Path
HERE=Path(__file__).resolve().parent
LESSONS=json.loads((HERE/'lessons.json').read_text(encoding='utf-8'))
SETTINGS=json.loads((HERE/'settings.json').read_text(encoding='utf-8'))
BG='#0B1120';PANEL='#0E1D34';INK='#EDF4FF';MUTED='#7A9ABF'
BLUE='#38BDF8';CYAN='#3ADEC8';GOLD='#FFD700';GREEN='#4ADE80';RED='#FF6B6B';ORANGE='#FB923C'
config.background_color=BG
config.pixel_width=SETTINGS['width'];config.pixel_height=SETTINGS['height'];config.frame_rate=SETTINGS['fps']
TMPL=TexTemplate();TMPL.add_to_preamble(r'\usepackage{amsmath}\usepackage{amssymb}\usepackage{bm}')
# MODEL_FUNCTIONS

def pt(x,y,z=0):return np.array([x,y,z],dtype=float)
def txt(s,size=24,color=INK,bold=False):
    return Text(s,font='DejaVu Sans',font_size=size,color=color,weight='BOLD' if bold else 'NORMAL',disable_ligatures=True)
def mtx(s,size=31,color=INK):return MathTex(s,font_size=size,color=color,tex_template=TMPL)
def fit(m,w,h=None):
    k=min(1,w/max(m.width,1e-9))
    if h is not None:k=min(k,h/max(m.height,1e-9))
    return m.scale(k)
def shaded(m):return m.set_shade_in_3d(True)
def panel(w,h,center,fill=1):
    return RoundedRectangle(width=w,height=h,corner_radius=.15,fill_color=PANEL,fill_opacity=fill,
        stroke_color=MUTED,stroke_opacity=.23,stroke_width=1.2).move_to(center)

class CoordinateView:
    def __init__(self,scene,case):
        self.scene=scene;self.case=case;self.I=weighted_center(case)
        self.trackers=[ValueTracker(float(v)) for v in case['start']]
        self.show_center=case.get('given_center',False)
        self.show_opt=False;self.revealed=False;self.length_mode=False
        self.static_labels={};self.labels=VGroup();self.dynamic_labels=VGroup();self.hud=VGroup()
        self.saved_weights=list(case['weights'])
        points=list(case['anchors'].values())+list(case.get('domain',{}).values())
        points +=[case['start'],case['opt'],[0,0,0]]
        if self.I is not None:points.append(self.I)
        points+=list(case.get('aux',{}).values())
        if 'max_point' in case:points.append(case['max_point'])
        if case.get('parameter') or case.get('zero_sum'):points.extend([[-4,2,2],[4,-2,-2]])
        coords=np.array(points,dtype=float)
        self.lo=np.minimum(coords.min(0)-.7,[-1,-1,-1]);self.hi=np.maximum(coords.max(0)+.7,[3,3,3])
        rotation=scene.camera.generate_rotation_matrix()
        corners=np.array([[x,y,z] for x in [self.lo[0],self.hi[0]] for y in [self.lo[1],self.hi[1]] for z in [self.lo[2],self.hi[2]]])
        projected=corners@rotation.T
        self.scale=min(4.85/np.ptp(projected[:,0]),3.3/np.ptp(projected[:,1]))
        mid=(projected.max(0)+projected.min(0))/2
        self.anchor=rotation.T@(pt(-3.8,.45)-self.scale*pt(mid[0],mid[1],0))
        self.axes=VGroup();self.domain=VGroup();self.anchors=VGroup();self.extra=VGroup();self.links=VGroup()
        self.make_axes();self.make_domain();self.make_anchors()
        self.center_dot=VGroup();self.opt_dot=VGroup()
        self.moving=Dot3D(point=self.W(case['start']),radius=.065,color=CYAN,resolution=(8,16))
        self.world=VGroup(self.axes,self.domain,self.anchors,self.extra,self.links,self.center_dot,self.opt_dot,self.moving)
        self.last=None
        self.update(force=True)
        self.world.add_updater(lambda _:self.update())
        self.world.suspend_updating()
    def W(self,p):return self.anchor+self.scale*np.array(p,dtype=float)
    def M(self):return [t.get_value() for t in self.trackers]
    def make_axes(self):
        for j,symbol in enumerate(['x','y','z']):
            low=[0,0,0];high=[0,0,0];low[j]=self.lo[j];high[j]=self.hi[j]
            self.axes.add(shaded(DashedLine(self.W(low),self.W([0,0,0]),color=MUTED,dash_length=.09,stroke_width=1)))
            self.axes.add(Arrow3D(start=self.W([0,0,0]),end=self.W(high),thickness=.008,
                                 height=.13,base_radius=.04,color=MUTED,resolution=8))
            self.label(symbol,high,MUTED,preferred=pt(.1,.14))
        if 'O' not in self.case['anchors'] and 'O' not in self.case.get('domain',{}):
            self.label('O',[0,0,0],MUTED,preferred=pt(-.12,-.17))
    def label(self,name,p,color=INK,preferred=None):
        # Screen-fixed labels are anchored to the projection. Greedy placement
        # avoids label/label overlap while the camera remains fixed.
        point=self.scene.camera.project_points(np.array([self.W(p)]))[0]
        mob=mtx(name,21,color)
        offsets=[preferred] if preferred is not None else []
        offsets += [pt(.15,.19),pt(-.19,.17),pt(.18,-.18),pt(-.2,-.18),pt(.3,.03),pt(-.3,.02)]
        best=None;best_penalty=1e9
        for off in offsets:
            at=pt(point[0]+off[0],point[1]+off[1]);penalty=0
            for other in self.static_labels.values():
                if abs(at[0]-other.get_x())<(mob.width+other.width)/2+.05 and abs(at[1]-other.get_y())<(mob.height+other.height)/2+.03:penalty+=1
            if at[0] < -6.45 or at[0] > -1.03 or at[1]>2.45 or at[1]<-1.55:penalty+=4
            if penalty<best_penalty:best=at;best_penalty=penalty
        mob.move_to(best);self.static_labels[name]=mob;self.labels.add(mob)
        self.scene.camera.add_fixed_in_frame_mobjects(mob)
        return mob
    def edge(self,a,b,color=MUTED,width=1.6,dashed=False):
        if np.linalg.norm(self.W(a)-self.W(b))<1e-7:return VGroup()
        m=DashedLine(self.W(a),self.W(b),color=color,dash_length=.08,stroke_width=width) if dashed else Line(self.W(a),self.W(b),color=color,stroke_width=width)
        return shaded(m)
    def face(self,points,color=GREEN,opacity=.09):
        return shaded(Polygon(*[self.W(p) for p in points],stroke_width=0,fill_color=color,fill_opacity=opacity))
    def polyhedron(self,vertices,faces):
        g=VGroup();view=self.scene.camera.generate_rotation_matrix()[2]
        center=np.array(vertices).mean(0);visibility=[];edge_faces={}
        for fi,face in enumerate(faces):
            verts=np.array([vertices[i] for i in face]);normal=np.cross(verts[1]-verts[0],verts[2]-verts[0])
            if np.dot(normal,verts.mean(0)-center)<0:normal=-normal
            visibility.append(np.dot(normal,view)>=0)
            g.add(self.face(verts))
            for i,j in zip(face,face[1:]+face[:1]):edge_faces.setdefault(tuple(sorted((i,j))),[]).append(fi)
        for (i,j),neighbors in edge_faces.items():
            hidden=not any(visibility[k] for k in neighbors)
            g.add(self.edge(vertices[i],vertices[j],GREEN if not hidden else MUTED,1.7,hidden))
        return g
    def make_domain(self):
        k=self.case['constraint'];d=self.case.get('domain',{})
        if k=='segment':
            a=d['A'];b=d['B'];self.domain.add(self.edge(a,b,GREEN,4))
            for name,p in d.items():
                self.domain.add(Dot3D(point=self.W(p),radius=.045,color=GREEN,resolution=(6,10)));self.label(name,p,GREEN)
        elif k=='oxy':
            x0,x1=self.lo[0],self.hi[0];y0,y1=self.lo[1],self.hi[1]
            self.domain.add(self.face([[x0,y0,0],[x1,y0,0],[x1,y1,0],[x0,y1,0]],opacity=.055))
            for x in np.linspace(x0,x1,5):self.domain.add(self.edge([x,y0,0],[x,y1,0],GREEN,.7))
            for y in np.linspace(y0,y1,5):self.domain.add(self.edge([x0,y,0],[x1,y,0],GREEN,.7))
        elif k=='triangle':
            vertices=list(d.values());self.domain.add(self.face(vertices,opacity=.15))
            for a,b in zip(vertices,vertices[1:]+vertices[:1]):self.domain.add(self.edge(a,b,GREEN,2))
            for name,p in d.items():
                self.domain.add(Dot3D(point=self.W(p),radius=.045,color=GREEN,resolution=(6,10)));self.label(name,p,GREEN)
        elif k=='box':
            v=[[0,0,0],[2,0,0],[2,3,0],[0,3,0],[0,0,1],[2,0,1],[2,3,1],[0,3,1]]
            f=[[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
            self.domain.add(self.polyhedron(v,f))
        elif k=='tetra_face':
            v=list(self.case['anchors'].values());f=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]]
            self.domain.add(self.polyhedron(v,f));self.domain.add(self.face(v[1:],GREEN,.18))
    def make_anchors(self):
        self.anchors=VGroup()
        for (name,p),weight in zip(self.case['anchors'].items(),self.case['weights']):
            if name in self.case.get('hidden',[]) and not self.revealed:continue
            color=ORANGE if weight<0 else BLUE
            self.anchors.add(Dot3D(point=self.W(p),radius=.055,color=color,resolution=(8,12)))
            if name not in self.static_labels:self.label(name,p,color)
    def metric(self,M):
        return objective(self.case,M)
    def update(self,force=False):
        M=self.M();key=tuple(round(v,8) for v in M)+tuple(self.case['weights'])+(self.show_center,self.show_opt,self.length_mode)
        if not force and key==self.last:return
        self.last=key;self.moving.move_to(self.W(M))
        links=VGroup()
        for name,p in self.case['anchors'].items():
            if name in self.case.get('hidden',[]) and not self.revealed:continue
            links.add(self.edge(M,p,BLUE,1.3))
        if self.show_center and self.I is not None:links.add(self.edge(M,self.I,GOLD,2.1))
        self.links.become(links)
        # Dynamic screen families must be re-registered after changing glyphs.
        self.scene.camera.remove_fixed_in_frame_mobjects(self.dynamic_labels,self.hud)
        projected=self.scene.camera.project_points(np.array([self.W(M)]))[0]
        label=mtx('M',22,CYAN).move_to(pt(projected[0]+.13,projected[1]-.2))
        for other in self.static_labels.values():
            if abs(label.get_x()-other.get_x())<.25 and abs(label.get_y()-other.get_y())<.2:label.shift(DOWN*.26)
        self.dynamic_labels.become(VGroup(label))
        pieces=[mtx('M(',20,CYAN)]
        for i,v in enumerate(M):
            pieces.append(DecimalNumber(v,num_decimal_places=2,font_size=20,color=INK))
            if i<2:pieces.append(mtx(';',20,MUTED))
        pieces.append(mtx(')',20,CYAN));coords=VGroup(*pieces).arrange(RIGHT,buff=.055)
        fit(coords,5.2,.4);coords.move_to(pt(-3.8,-2.15))
        name='L' if self.case.get('kind')=='vector' else 'F'
        value=(mtx('?',25,GOLD) if self.case.get('hidden') and not self.revealed else DecimalNumber(self.metric(M),num_decimal_places=3,font_size=25,color=GOLD))
        result=VGroup(mtx(name+'=',25,GOLD),value).arrange(RIGHT,buff=.12).move_to(pt(-3.8,-2.68))
        hud=VGroup(coords,result)
        if self.case.get('compare_lengths'):
            val=sum(math.sqrt(norm2(sub(M,p))) for p in self.case['anchors'].values())
            line=VGroup(mtx('G=',22,GREEN),DecimalNumber(val,num_decimal_places=3,font_size=22,color=GREEN)).arrange(RIGHT,buff=.1).move_to(pt(-3.8,-3.1));hud.add(line)
        else:
            note=(mtx(r'\mu='+str(c['weights'][-1]),22,MUTED) if (c:=self.case).get('parameter') else txt('M luôn phải thỏa miền đang xét',14,MUTED)).move_to(pt(-3.8,-3.05));hud.add(note)
        self.hud.become(hud)
        self.scene.camera.add_fixed_in_frame_mobjects(self.dynamic_labels,self.hud)
    def unfreeze(self):self.world.resume_updating()
    def freeze(self):self.world.suspend_updating()
    def move(self,target,seconds=2):
        self.unfreeze()
        self.scene.play(*[t.animate.set_value(v) for t,v in zip(self.trackers,target)],run_time=seconds,rate_func=smooth)
        self.freeze()
    def center(self):
        if self.I is None:return
        self.show_center=True
        self.center_dot.become(VGroup(Dot3D(point=self.W(self.I),radius=.07,color=GOLD,resolution=(8,16))))
        name='G' if self.case['id']=='B12' else ('O' if self.case['id']=='B04' else 'I')
        if name not in self.static_labels:self.label(name,self.I,GOLD)
        self.scene.camera.add_fixed_in_frame_mobjects(self.labels);self.scene.add(self.labels)
        self.update(force=True)
    def optimum(self):
        self.center();self.move(self.case['opt'],3)
        self.show_opt=True
        self.opt_dot.become(VGroup(Dot3D(point=self.W(self.case['opt']),radius=.08,color=GOLD,resolution=(8,16))))
        self.update(force=True)
    def reveal(self):
        self.revealed=True;before=self.anchors
        new=VGroup()
        p=self.case['anchors']['C'];new.add(Dot3D(point=self.W(p),radius=.055,color=BLUE,resolution=(8,12)))
        self.anchors.add(new);self.label('C',p,BLUE)
        self.scene.camera.add_fixed_in_frame_mobjects(self.labels);self.scene.add(self.labels)
        self.scene.play(FadeIn(new),run_time=1);self.update(force=True)
    def outside(self):
        self.center()
        p=self.case['aux']['J']
        self.extra.add(Dot3D(point=self.W(p),radius=.055,color=RED,resolution=(8,12)))
        self.extra.add(self.edge(self.I,p,MUTED,1.4,True))
        self.label('J',p,RED);self.scene.camera.add_fixed_in_frame_mobjects(self.labels);self.scene.add(self.labels)
        self.scene.wait(2)

class OxyzLesson(ThreeDScene):
    lesson_id='INTRO'
    def construct(self):
        lesson=next(l for l in LESSONS if l['id']==self.lesson_id);self.events=[]
        self.set_camera_orientation(phi=65*DEGREES,theta=-48*DEGREES,focal_distance=1000,zoom=1)
        self.camera.reset_rotation_matrix()  # project labels with the NEW orientation before frame 1
        title=fit(txt(lesson['title'],32,INK,True),12.9,.48).move_to(pt(0,3.5))
        subtitle=txt('OXYZ • TÂM TỈ CỰ • VECTƠ VÀ BÌNH PHƯƠNG',16,BLUE).move_to(pt(0,3.07))
        left=panel(5.95,6.05,pt(-3.78,-.22),fill=0)
        right=panel(6.95,6.05,pt(2.92,-.22),fill=.98)
        footer=txt(SETTINGS['teacher'],19,MUTED).move_to(pt(0,-3.74))
        rule=Line(pt(-6.7,-3.44),pt(6.7,-3.44),color=MUTED,stroke_width=1)
        self.add_fixed_in_frame_mobjects(title,subtitle,left,right,footer,rule)
        model=CoordinateView(self,lesson['model']);self.model=model
        self.add(model.world)
        self.add_fixed_in_frame_mobjects(model.labels,model.dynamic_labels,model.hud)
        legend=fit(txt('Điểm đã cho • Tâm • Điểm M • Miền hợp lệ',14,MUTED),5.45).move_to(pt(-3.8,2.65))
        self.add_fixed_in_frame_mobjects(legend)
        if model.show_center:model.center()
        for pi,page in enumerate(lesson['pages']):
            if page['action']=='constant':
                model.case['weights']=[1,1,-2];model.I=None;model.show_center=False
                model.center_dot.become(VGroup());model.update(force=True)
            heading=fit(txt(page['title'],23,CYAN,True),6.15,.55).move_to(pt(-.19,2.48),aligned_edge=LEFT)
            counter=txt(f"{lesson['order']:02d}/{lesson['total']:02d} • Trang {pi+1}/{len(lesson['pages'])}",14,MUTED).move_to(pt(5.42,-3.74))
            self.add_fixed_in_frame_mobjects(heading,counter);self.play(FadeIn(heading),run_time=.5)
            current=[];previous=None
            for ri,row in enumerate(page['rows']):
                if row['kind']=='math':mob=fit(mtx(row['text'],31,GOLD if row.get('gold') else INK),6.15,.94)
                else:
                    s=textwrap.fill(row['text'],width=43,break_long_words=False,break_on_hyphens=False)
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
                if row.get('pause',0):self.wait(row['pause'])
            self.action(page['action'])
            self.wait(.9)
            self.play(*[FadeOut(mob) for mob in current+[heading,counter]],run_time=.5)
            self.remove_fixed_in_frame_mobjects(*current,heading,counter)
        model.world.clear_updaters(recursive=True)
        (HERE/'events').mkdir(exist_ok=True)
        (HERE/'events'/(self.lesson_id+'.json')).write_text(json.dumps(self.events,ensure_ascii=False),encoding='utf-8')
    def action(self,name):
        m=self.model;c=m.case
        if name=='center':m.center();self.wait(1.5)
        elif name=='opt':m.optimum();self.wait(1)
        elif name=='max':m.move(c['max_point'],3);self.wait(1)
        elif name=='outside':m.outside()
        elif name=='reveal':m.reveal()
        elif name=='axes':
            for p in [[4/3,0,0],[0,2/3,0],[0,0,2]]:
                # Move THROUGH the origin when switching axes: intermediate
                # coordinates must still satisfy the union-of-three-axes domain.
                m.move([0,0,0],1);m.move(p,1.4);self.wait(.8)
        elif name=='constant':
            c['weights']=[1,1,-2];m.I=None;m.show_center=False
            m.center_dot.become(VGroup());m.update(force=True)
            m.move([2,1,1],2);m.move([-1,2,1],2)
        elif name=='linear':m.move([-3,1,1],2);m.move([4,1,1],2)
        elif name=='linear_bound':m.move([0,1,1],2);m.move([3,1,1],2)
        elif name=='lengths':
            a=c['anchors']['A'];b=c['anchors']['B']
            line=m.edge(a,b,GOLD,4);m.extra.add(line)
            for x in [.5,3.4,1.]:m.move([x,0,0],2);self.wait(.8)

# LESSON_CLASSES
'''


# ======================= PIPELINE COLAB =======================
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
    remedy='Chạy bash setup_codespaces.sh, rồi bash render.sh oxyz hoặc bash render.sh nuoc.'
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
    import inspect
    common='\n\n'.join(inspect.getsource(fn) for fn in [dot,sub,norm2,weighted_center,constant_K,objective])
    classes='\n'.join(f"class C_{s['id']}(OxyzLesson):\n    lesson_id={s['id']!r}\n" for s in lessons)
    return SCENE_SOURCE.replace('# MODEL_FUNCTIONS',common).replace('# LESSON_CLASSES',classes)


def is_codespaces():
    return os.environ.get('CODESPACES','').lower()=='true'


def is_colab():
    return not is_codespaces() and sys.platform=='linux' and Path('/content').is_dir()


def is_github_actions():
    return os.environ.get('GITHUB_ACTIONS','').lower()=='true'


def require_render_environment():
    """Mặc định cho phép Codespaces/Colab, chặn vô tình render trên Mac."""
    if CHI_CHAY_TREN_CLOUD and not (is_codespaces() or is_colab() or is_github_actions()):
        raise RuntimeError('Hãy chạy trên Codespaces, Colab hoặc GitHub Actions. Lệnh --check vẫn chạy được trên máy cá nhân.')


def output_root(folder):
    override=os.environ.get('MANIM_OUTPUT_DIR')
    if override:return Path(override).expanduser().resolve()/folder
    if is_colab():return Path('/content')/folder
    if is_codespaces():return Path('/tmp/manim-video-output')/folder
    base=Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
    return base/'renders'/folder


def show_downloads(final,archive):
    """Chỉ hiển thị nút tải; không đọc/nhúng MP4, không tạo trình phát.

    files.download chỉ được gọi sau khi người dùng bấm một nút.
    Không có vòng lặp JavaScript, timer, keep-alive hay polling giao diện.
    """
    if is_codespaces():
        print('Video và cache nằm ngoài repo. Thêm thư mục kết quả vào Explorer bằng:')
        import shlex
        print('code --add '+shlex.quote(str(final.parent.parent)))
        print('Explorer > thư mục bài > chuột phải MP4 > Download. Không cần mở video.')
        print('Tải và kiểm tra xong: bash cleanup_outputs.sh để dọn dữ liệu tạm.')
        return
    if is_github_actions():
        print('Workflow sẽ tải MP4, phụ đề, mục lục và ZIP mã nguồn lên Actions artifact.')
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
    root=output_root('Oxyz_Tam_Ti_Cu')
    root.mkdir(exist_ok=True,parents=True);setup(root)
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
    def render_one(les):
        name='C_'+les['id'];clip=work/'clips'/(name+'.mp4');event=work/'events'/(les['id']+'.json')
        reusable=False
        if clip.exists() and event.exists():
            try:duration(clip);json.loads(event.read_text());reusable=True
            except Exception:pass
        if not reusable:
            command([sys.executable,'-m','manim','--renderer','cairo','--format','mp4',
                '--fps',fps,'-r',f'{width},{height}','--media_dir',work/'media'/name,'--progress_bar','none',
                '--verbosity','WARNING','-o',name,source,name],work/(name+'.log'),cwd=work)
            candidates=[p for p in (work/'media').rglob(name+'.mp4') if 'partial_movie_files' not in str(p)]
            if not candidates:raise RuntimeError('Không tìm thấy video '+name)
            shutil.copy2(max(candidates,key=lambda p:p.stat().st_mtime),clip)
        return name,reusable

    render_jobs=int(os.environ.get('MANIM_RENDER_JOBS','1'))
    if not 1<=render_jobs<=4:raise ValueError('MANIM_RENDER_JOBS phải nằm trong khoảng 1–4.')
    workers=min(render_jobs,len(lessons))
    print(f'BƯỚC 3/5 — Render từng bài Oxyz; tối đa {workers} bài song song, dùng lại bài đã hoàn tất...')
    reusable_by_name={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        pending={pool.submit(render_one,les):les for les in lessons}
        for future in concurrent.futures.as_completed(pending):
            name,reusable=future.result();les=pending[future];reusable_by_name[name]=reusable
            print(f"  {les['id']} — {les['title']}: {duration(work/'clips'/(name+'.mp4'))/60:.2f} phút {'(cache)' if reusable else ''}")

    clips=[];all_events=[];marks=[];offset=0
    for les in lessons:
        name='C_'+les['id'];clip=work/'clips'/(name+'.mp4');event=work/'events'/(les['id']+'.json')
        reusable=reusable_by_name[name]
        if not event.exists():raise RuntimeError('Thiếu mốc phụ đề '+name)
        dur=duration(clip);clips.append(clip);marks.append((offset,offset+dur,les['title']))
        for ev in json.loads(event.read_text(encoding='utf-8')):
            ev['start']+=offset;ev['end']+=offset;all_events.append(ev)
        offset+=dur
    print('BƯỚC 4/5 — Ghép MP4 và xuất phụ đề, mục lục...')
    concat=work/'concat.txt';concat.write_text('\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in clips)+'\n',encoding='utf-8')
    metadata=[';FFMETADATA1','title=Oxyz - Tâm tỉ cự - 15 bài hay lạ khó','artist='+TEN_THAY]
    for start,end,title in marks:
        escaped=title.replace('\\','\\\\').replace('=','\\=').replace(';','\\;').replace('#','\\#')
        metadata+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(start*1000)}',f'END={round(end*1000)}','title='+escaped]
    meta=work/'chapters.ffmeta';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
    final=root/'oxyz_tam_ti_cu_hay_la_kho.mp4'
    command(['ffmpeg','-y','-v','warning','-f','concat','-safe','0','-i',concat,'-i',meta,
             '-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy',
             '-movflags','+faststart',final],work/'ffmpeg_join.log')
    final_dur=duration(final)
    info=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(final)],check=True,capture_output=True,text=True).stdout)
    assert {'video','audio'}.issubset({s['codec_type'] for s in info['streams']}),'Video thiếu hình hoặc âm thanh.'
    captions(all_events,final.with_suffix(''))
    toc=root/'oxyz_tam_ti_cu_muc_luc.txt';toc.write_text('\n'.join(timestamp(a,'.')+'  '+title for a,b,title in marks),encoding='utf-8')
    archive=root/'oxyz_tam_ti_cu_ma_nguon.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in [source,work/'lessons.json',work/'settings.json',toc,final.with_suffix('.srt'),final.with_suffix('.vtt')]:z.write(p,p.name)
        if '__file__' in globals() and Path(__file__).is_file():z.write(__file__,Path(__file__).name)
        z.writestr('HUONG_DAN.txt','Tải tệp .py gốc lên Colab; dùng runpy.run_path để chạy trong một ô mã ngắn.\n'
            'CHON_BAI=["INTRO","B01"] để thử; [] để dựng toàn bộ.\n'
            'CHE_DO: preview, standard, final.\n'
            '15 bài đều có lời giải và điều kiện dấu bằng; không dùng phương trình đường/mặt/cầu.\n')
    print(f'BƯỚC 5/5 — HOÀN TẤT: {final_dur/60:.2f} phút, {width}×{height}, {fps} fps.')
    print('Video:',final);print('Mã nguồn:',archive)
    show_downloads(final,archive)


if __name__=='__main__':main()
