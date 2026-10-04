# -*- coding: utf-8 -*-
"""
THẦY NGUYỄN VĂN SANG
TỐC ĐỘ NƯỚC DÂNG — 12 MÔ HÌNH 3D, LẤY DIỆN TÍCH MẶT THOÁNG LÀM GỐC
Colab nhẹ: tải tệp .py lên rồi chạy bằng runpy (hướng dẫn bên dưới).
Không giới hạn 10 phút: ưu tiên đề, hình, lập luận, ví dụ và luyện tập.
Đầu ra: một MP4 có mục lục, SRT/VTT và ZIP mã nguồn.

CHE_DO: preview (480p/15fps), standard (720p/24fps), final (1080p/30fps).
CHON_BAI: [] = đủ 12 bài + nền tảng + tổng kết; ['B08'] = thử trụ ngang.
Lệnh python file.py --check chỉ kiểm chứng toán, không cài hoặc render.

Hình thật trong ThreeDScene; mặt thoáng luôn nằm ngang trong hệ tọa độ 3D.
Mực nước mô phỏng theo V(h(t)) = V(h0) + Q t, KHÔNG cho h tăng tuyến tính
trong các bể có diện tích mặt thoáng thay đổi. Góc nhìn từ trên là hình 2D
phụ trợ, đúng tỷ lệ từng mô hình, không thay thế mô hình 3D chính.
Công thức dạy học chủ đạo: Q = A(h) h'(t), h'(t) = Q / A(h).
Đẳng thức V'(h)=A(h) chỉ phục vụ kiểm chứng và điều khiển hình động.

Giả thiết: nước gần như tĩnh, mặt thoáng phẳng/nằm ngang; bể cứng;
Q không đổi; không rò/rút nước, không vật chiếm chỗ, không tràn; bỏ qua cổ
bình/lỗ bơm nhỏ. Bình cầu/ellipsoid/bồn ngang có lỗ bơm và thông khí.
Lưu lượng là m³/s; kích thước m; tốc độ có cả m/s và cm/s khi tính số.
Không áp dụng biểu thức hữu hạn tại các điểm A(h)=0.

Môi trường: Manim Community 0.19.0, Cairo, Edge TTS, FFmpeg, LaTeX.
API nguồn: https://github.com/ManimCommunity/manim/tree/v0.19.0/manim

CODESPACES (bộ ZIP kèm setup_codespaces.sh và render.sh):
- Lần đầu: bash setup_codespaces.sh
- Render: bash render.sh nuoc final
- MP4 ở /tmp/manim-video-output, ngoài repo; thêm thư mục vào Explorer để tải.
- Cài một lần cho cùng môi trường; rebuild/xóa Codespace cần cài lại.

CÁCH CHẠY NHẸ GIAO DIỆN COLAB:
1. Mở notebook mới trên Colab, dùng runtime do Google cung cấp.
2. Bảng Files (biểu tượng thư mục) > Upload, chọn tệp .py này.
3. Trong MỘT ô mã ngắn, chạy:
   import runpy
   _ = runpy.run_path('/content/toc_do_nuoc_dang_3d_dien_tich_mat_thoang.py', run_name='__main__')
4. Chờ thông báo HOÀN TẤT rồi bấm Tải video MP4. Không có trình phát.
Không cần dán gần 1.000 dòng mã vào trình soạn thảo của trình duyệt.
Cài đặt/render/ghép phim đều ghi log trên runtime; chỉ in mốc từng chương.
Chỉ mở một notebook đang render. Không dùng runtime kết nối máy cá nhân.
Cache dùng lại được nếu runtime và các file /content vẫn còn.
Đóng tab không bảo đảm Colab tiếp tục chạy; chế độ này không giữ phiên
bằng JavaScript. Nó giảm phần hiển thị, không bảo đảm máy mát 100%.

"""
import os, sys, json, math, wave, hashlib, asyncio, subprocess, textwrap, shutil, zipfile
from pathlib import Path

TEN_THAY='Thầy Nguyễn Văn Sang'
GIONG_DOC='vi-VN-NamMinhNeural'
TOC_DO_DOC='-5%'
CHE_DO='standard'
CHON_BAI=[]
# Chế độ Colab/Codespaces nhẹ: chỉ log ngắn theo chương; xong bấm nút tải MP4.
# Không nhúng video, không tự phát hoặc tự tải; giữ chất lượng CHE_DO.
CHI_CHAY_TREN_CLOUD=True
MANIM_VERSION='0.19.0'
PRESETS={'preview':(854,480,15),'standard':(1280,720,24),'final':(1920,1080,30)}

# ========================== TOÁN / HÌNH HỌC ==========================
# Cùng một nguồn cho A(h), V(h), mực nước, hình mặt thoáng và đáp án số.
MODELS=[
 {'id':'B01','kind':'cylinder','title':'Bể trụ đứng','p':{'R':1.,'H':3.},'Q':.06,'h':1.2,'practice_h':2.,'practice_Q':.09},
 {'id':'B02','kind':'box','title':'Bể hộp chữ nhật','p':{'a':3.,'b':2.,'H':2.},'Q':.12,'h':.8,'practice_h':1.5,'practice_Q':.18},
 {'id':'B03','kind':'cone_down','title':'Nón đỉnh hướng xuống','p':{'R':2.,'H':4.},'Q':.04,'h':2.,'practice_h':1.,'practice_Q':.04},
 {'id':'B04','kind':'sphere','title':'Bình cầu có lỗ thông khí','p':{'R':2.,'H':4.},'Q':.08,'h':1.,'practice_h':3.,'practice_Q':.08},
 {'id':'B05','kind':'hemisphere','title':'Bát bán cầu, miệng hướng lên','p':{'R':2.,'H':2.},'Q':.06,'h':1.,'practice_h':2.,'practice_Q':.06},
 {'id':'B06','kind':'pyramid','title':'Chóp vuông đỉnh hướng xuống','p':{'a':4.,'H':3.},'Q':.08,'h':1.5,'practice_h':1.,'practice_Q':.08},
 {'id':'B07','kind':'trough','title':'Máng lăng trụ tam giác cân','p':{'b':3.,'L':6.,'H':2.},'Q':.12,'h':1.,'practice_h':1.5,'practice_Q':.12},
 {'id':'B08','kind':'horizontal','title':'Bồn trụ đặt nằm ngang','p':{'R':1.5,'L':5.,'H':3.},'Q':.09,'h':.6,'practice_h':1.5,'practice_Q':.09},
 {'id':'B09','kind':'frustum','title':'Nón cụt loe rộng lên trên','p':{'r0':1.,'r1':2.,'H':3.},'Q':.08,'h':1.5,'practice_h':.75,'practice_Q':.08},
 {'id':'B10','kind':'frustum','title':'Nón cụt thu hẹp lên trên','p':{'r0':2.,'r1':1.,'H':3.},'Q':.08,'h':1.5,'practice_h':2.25,'practice_Q':.08},
 {'id':'B11','kind':'ellipsoid','title':'Bình ellipsoid, trục đứng','p':{'a':2.,'b':1.5,'c':2.,'H':4.},'Q':.06,'h':1.,'practice_h':3.,'practice_Q':.06},
 {'id':'B12','kind':'hourglass','title':'Bình thắt cổ ở giữa','p':{'H':4.,'rmin':1.,'c':2.,'alpha':.25},'Q':.05,'h':2.,'practice_h':1.,'practice_Q':.05},
]


def footprint(model,h):
    """(shape, x-halfwidth, y-halfwidth), ngang XY; trụ ngang có trục dọc X."""
    k=model['kind'];p=model['p'];H=p['H'];h=max(0,min(H,h))
    if k=='cylinder':return 'ellipse',p['R'],p['R']
    if k=='box':return 'rectangle',p['a']/2,p['b']/2
    if k=='cone_down':r=p['R']*h/H;return 'ellipse',r,r
    if k in ('sphere','hemisphere'):
        r=math.sqrt(max(0,h*(2*p['R']-h)));return 'ellipse',r,r
    if k=='pyramid':s=p['a']*h/H/2;return 'rectangle',s,s
    if k=='trough':return 'rectangle',p['L']/2,p['b']*h/H/2
    if k=='horizontal':return 'rectangle',p['L']/2,math.sqrt(max(0,h*(2*p['R']-h)))
    if k=='frustum':r=p['r0']+(p['r1']-p['r0'])*h/H;return 'ellipse',r,r
    if k=='ellipsoid':
        f=math.sqrt(max(0,1-((h-p['c'])/p['c'])**2))
        return 'ellipse',p['a']*f,p['b']*f
    if k=='hourglass':r=p['rmin']+p['alpha']*(h-p['c'])**2;return 'ellipse',r,r
    raise ValueError(k)


def surface_boundary(model,h,samples=160):
    """Mặt thoáng NGANG z=h; không dựng ellipse trong hệ màn hình.

    Trụ ngang: hình chữ nhật dài L, rộng 2sqrt(h(2R-h)).
    Bình cầu: đường tròn x²+y²=h(2R-h), tâm (0,0,h).
    """
    H=model['p']['H']
    if not 0<=h<=H:raise ValueError('Mực nước nằm ngoài bể')
    shape,a,b=footprint(model,h)
    if shape=='rectangle':return [(-a,-b,h),(a,-b,h),(a,b,h),(-a,b,h)]
    return [(a*math.cos(2*math.pi*j/samples),b*math.sin(2*math.pi*j/samples),h) for j in range(samples)]


def curved_wall_point(model,u,theta):
    """Tham số góc u cho cầu/ellipsoid; tham số độ cao cho dạng khác."""
    p=model['p'];k=model['kind']
    if k in ('sphere','hemisphere'):
        r=p['R']*math.sin(u);z=p['R']*(1-math.cos(u))
        return (r*math.cos(theta),r*math.sin(theta),z)
    if k=='ellipsoid':
        return (p['a']*math.sin(u)*math.cos(theta),p['b']*math.sin(u)*math.sin(theta),p['c']*(1-math.cos(u)))
    _,a,b=footprint(model,u)
    return (a*math.cos(theta),b*math.sin(theta),u)


def wall_parameter(model,h):
    k=model['kind'];p=model['p']
    if k in ('sphere','hemisphere'):return math.acos(max(-1,min(1,1-h/p['R'])))
    if k=='ellipsoid':return math.acos(max(-1,min(1,1-h/p['c'])))
    return h


def wall_normal(model,h,theta):
    """Pháp tuyến ra ngoài để xét nét thấy/khuất trên mặt lồi."""
    k=model['kind'];p=model['p'];_,a,b=footprint(model,h)
    c=math.cos(theta);t=math.sin(theta)
    if k in ('sphere','hemisphere'):return (a*c,a*t,h-p['R'])
    if k=='ellipsoid':return (a*c/p['a']**2,b*t/p['b']**2,(h-p['c'])/p['c']**2)
    if k=='cone_down':slope=p['R']/p['H']
    elif k=='frustum':slope=(p['r1']-p['r0'])/p['H']
    elif k=='hourglass':slope=2*p['alpha']*(h-p['c'])
    else:slope=0
    return (c,t,-slope)


def area(model,h):
    shape,a,b=footprint(model,h)
    return math.pi*a*b if shape=='ellipse' else 4*a*b


def volume(model,h):
    k=model['kind'];p=model['p'];H=p['H'];h=max(0,min(H,h))
    if k=='cylinder':return math.pi*p['R']**2*h
    if k=='box':return p['a']*p['b']*h
    if k=='cone_down':return math.pi*p['R']**2*h**3/(3*H**2)
    if k in ('sphere','hemisphere'):return math.pi*h*h*(p['R']-h/3)
    if k=='pyramid':return p['a']**2*h**3/(3*H**2)
    if k=='trough':return p['b']*p['L']*h*h/(2*H)
    if k=='horizontal':
        R=p['R'];w=math.sqrt(max(0,h*(2*R-h)))
        angle=math.acos(max(-1,min(1,(R-h)/R)))
        return p['L']*(R*R*angle-(R-h)*w)
    if k=='frustum':
        r0=p['r0'];slope=(p['r1']-r0)/H
        return math.pi*(r0*r0*h+r0*slope*h*h+slope*slope*h**3/3)
    if k=='ellipsoid':return math.pi*p['a']*p['b']*(h*h/p['c']-h**3/(3*p['c']**2))
    if k=='hourglass':
        # ∫ π[rmin + α(z-c)^2]^2 dz, exact polynomial antiderivative.
        r=p['rmin'];al=p['alpha'];c=p['c']
        primitive=lambda z:r*r*z+2*r*al*(z-c)**3/3+al*al*(z-c)**5/5
        return math.pi*(primitive(h)-primitive(0))
    raise ValueError(k)


def height_from_volume(model,V):
    lo=0.;hi=model['p']['H'];V=max(0,min(volume(model,hi),V))
    for _ in range(52):
        mid=(lo+hi)/2
        if volume(model,mid)<V:lo=mid
        else:hi=mid
    return (lo+hi)/2


def rise(model,h,Q=None):
    a=area(model,h)
    if a<=0:raise ValueError('A(h)=0: không có tốc độ hữu hạn tại mức này.')
    return (model['Q'] if Q is None else Q)/a


def validate_math():
    """Independent finite differences, Simpson integrals, inversion, example answers."""
    expected=[.06/math.pi,.02,.04/math.pi,.08/(3*math.pi),.06/(3*math.pi),.02,
              .12/9,.0075,.08/(2.25*math.pi),.08/(2.25*math.pi),.06/(2.25*math.pi),.05/math.pi]
    practice=[.09/math.pi,.03,.16/math.pi,.08/(3*math.pi),.06/(4*math.pi),.045,
              .12/13.5,.006,.08/(1.5625*math.pi),.08/(1.5625*math.pi),.06/(2.25*math.pi),.05/(1.5625*math.pi)]
    for m,e,ep in zip(MODELS,expected,practice):
        H=m['p']['H'];eps=H*1e-5
        assert math.isclose(rise(m,m['h']),e,rel_tol=1e-12),m['id']
        assert math.isclose(rise(m,m['practice_h'],m['practice_Q']),ep,rel_tol=1e-12),m['id']
        for fraction in [.08,.2,.43,.5,.71,.93]:
            h=H*fraction
            dvdh=(volume(m,h+eps)-volume(m,h-eps))/(2*eps)
            assert math.isclose(dvdh,area(m,h),rel_tol=2e-7), (m['id'],h,dvdh,area(m,h))
            inv=height_from_volume(m,volume(m,h))
            assert abs(inv-h)<1e-10,(m['id'],h,inv)
            # Check d/dt h(t)=Q/A(h) along the SAME trajectory used by animation.
            dt=1e-4
            va=volume(m,h)
            dhdt=(height_from_volume(m,va+m['Q']*dt)-height_from_volume(m,va-m['Q']*dt))/(2*dt)
            assert math.isclose(dhdt,rise(m,h),rel_tol=2e-6),(m['id'],h,dhdt)
        # Independent numerical area integration, away from singular end slopes.
        stop=.83*H;n=1000;dx=stop/n
        integral=dx/3*(area(m,0)+area(m,stop)+sum((4 if i%2 else 2)*area(m,i*dx) for i in range(1,n)))
        assert math.isclose(integral,volume(m,stop),rel_tol=4e-5),(m['id'],integral,volume(m,stop))
    sphere=MODELS[3];horizontal=MODELS[7];neck=MODELS[11]
    assert rise(sphere,2)<rise(sphere,1) and math.isclose(rise(sphere,1),rise(sphere,3))
    assert rise(horizontal,1.5)<rise(horizontal,.6)
    assert rise(neck,2)>rise(neck,1) and math.isclose(rise(neck,1),rise(neck,3))
    assert area(MODELS[8],.75)<area(MODELS[8],2.25)
    assert area(MODELS[9],.75)>area(MODELS[9],2.25)
    print('KIỂM CHỨNG: 12 diện tích mặt thoáng, V′(h)=A(h), quỹ đạo nước dâng và 24 đáp số: đạt.')


def validate_geometry():
    for model in MODELS:
        H=model['p']['H'];p=model['p'];k=model['kind']
        for f in [.1,.25,.5,.75,.9]:
            h=f*H;points=surface_boundary(model,h,192)
            assert all(abs(v[2]-h)<1e-12 for v in points)
            polygon_area=abs(sum(x[0]*y[1]-y[0]*x[1] for x,y in zip(points,points[1:]+points[:1])))/2
            assert math.isclose(polygon_area,area(model,h),rel_tol=2e-4),model['id']
            if k in ('sphere','hemisphere'):
                for x,y,z in points:assert math.isclose(x*x+y*y+(z-p['R'])**2,p['R']**2,rel_tol=1e-12)
            if k=='ellipsoid':
                for x,y,z in points:assert math.isclose((x/p['a'])**2+(y/p['b'])**2+((z-p['c'])/p['c'])**2,1,rel_tol=1e-12)
            if k=='horizontal':
                for x,y,z in points:assert math.isclose(y*y+(z-p['R'])**2,p['R']**2,rel_tol=1e-12)
            if k not in ('box','pyramid','trough','horizontal'):
                u=wall_parameter(model,h)
                for theta in [.2,1.4,2.7,4.5]:
                    x,y,z=curved_wall_point(model,u,theta)
                    assert math.isclose(z,h,abs_tol=1e-10)
                    _,a,b=footprint(model,h)
                    assert math.isclose((x/a)**2+(y/b)**2,1,rel_tol=1e-12)
                    # Normal is perpendicular to both shell tangents.
                    eps=1e-6
                    def difference(a,b):return [(x-y)/(2*eps) for x,y in zip(a,b)]
                    du=difference(curved_wall_point(model,u+eps,theta),curved_wall_point(model,u-eps,theta))
                    dt=difference(curved_wall_point(model,u,theta+eps),curved_wall_point(model,u,theta-eps))
                    n=wall_normal(model,h,theta)
                    assert abs(sum(x*y for x,y in zip(n,du)))<1e-6
                    assert abs(sum(x*y for x,y in zip(n,dt)))<1e-6
    print('HÌNH HỌC: 12 biên mặt thoáng; mặt cầu/ellipsoid; trụ ngang; pháp tuyến: đạt.')


# ========================== KỊCH BẢN GIẢNG ==========================
def T(text,voice,pause=0):return {'kind':'text','text':text,'voice':voice,'pause':pause}
def M(tex,voice,gold=False,pause=0):return {'kind':'math','text':tex,'voice':voice,'gold':gold,'pause':pause}
def P(title,rows,action='none'):return {'title':title,'rows':rows,'action':action}

THEORY=[
 P('Một lưu lượng, nhiều nhịp nước dâng',[
  T('Bơm đều không có nghĩa là mực nước dâng đều.', 'Chào các em. Nếu bơm nước đều vào nhiều loại bình, có phải mực nước đều tăng như nhau không? Hãy nhìn hình ba chiều và mặt thoáng nhìn từ trên.'),
  T('Lớp nước mới trải trên một diện tích đang thay đổi.', 'Cùng một lượng nước, mặt thoáng rộng thì lớp nước mới mỏng; mặt thoáng hẹp thì lớp nước mới dày.'),
  M(r'\Delta V\approx A(h)\,\Delta h','Với một lớp nước rất mỏng, thể tích tăng xấp xỉ diện tích mặt thoáng nhân độ dày lớp nước.'),
  T('Mặt thoáng là bề mặt nằm ngang tiếp xúc với không khí.', 'Diện tích cần dùng là diện tích mặt thoáng nằm ngang. Không phải diện tích đáy, cũng không phải diện tích thành bể.')
 ],'slice'),
 P('Từ lớp nước mỏng tới tốc độ tức thời',[
  M(r'Q=\frac{\mathrm dV}{\mathrm dt},\qquad A(h)=\frac{\mathrm dV}{\mathrm dh}', 'Q là lưu lượng theo thể tích, tính bằng mét khối mỗi giây. A của h là diện tích thiết diện ngang tại mức nước h.'),
  M(r'\frac{\mathrm dV}{\mathrm dt}=\frac{\mathrm dV}{\mathrm dh}\frac{\mathrm dh}{\mathrm dt}=A(h)\,h^{\prime}(t)', 'Theo quy tắc đạo hàm hàm hợp, lưu lượng bằng diện tích mặt thoáng nhân tốc độ mực nước dâng.'),
  M(r'\boxed{h^{\prime}(t)=\frac{Q}{A(h)}}','Đây là công thức trung tâm của cả video: tốc độ nước dâng bằng lưu lượng chia diện tích mặt thoáng.',True),
  M(r'\frac{\mathrm{m^3/s}}{\mathrm{m^2}}=\mathrm{m/s}', 'Kiểm tra đơn vị: mét khối mỗi giây chia mét vuông là mét mỗi giây. Lưu lượng và tốc độ dâng là hai đại lượng khác nhau.')
 ],'highlight'),
 P('Định nghĩa chiều cao và điều kiện mô hình',[
  T('Mực nước được đo thẳng đứng từ điểm thấp nhất của bể.', 'Trong mọi bài, h được đo theo phương thẳng đứng từ điểm thấp nhất của bể, không đo dọc theo thành nghiêng.'),
  T('Nước gần như tĩnh; mặt thoáng nằm ngang; bể không biến dạng.', 'Ta giả sử nước gần như tĩnh, bể cứng, không có vật chiếm chỗ và không rò nước. Các bình kín có lỗ bơm và lỗ thông khí nhỏ.'),
  M(r'Q>0,\quad A(h)>0,\quad 0<h<H','Ta xét mực nước ở trong bể và có diện tích mặt thoáng dương. Không thay trực tiếp vào một điểm nhọn có diện tích bằng không.'),
  T('Hình động dùng thời gian bơm và thể tích thực.', 'Trong mô phỏng, mỗi khoảng thời gian vật lý bằng nhau được bơm cùng thể tích. Vì thế nước dâng không đều trong các bình loe hoặc thắt.')
 ],'fill'),
 P('Dự đoán nhanh trước khi tính',[
  M(r'Q\ \text{constant}:\quad h^{\prime}=\frac Q{A(h)}','Khi lưu lượng không đổi, diện tích mặt thoáng và tốc độ dâng biến thiên ngược nhau.'),
  M(r'h^{\prime\prime}(t)=-\frac{Q^2A^{\prime}(h)}{A(h)^3}','Lấy đạo hàm theo thời gian, gia tốc của mực nước bằng âm Q bình nhân đạo hàm diện tích, chia diện tích lũy thừa ba.'),
  M(r'A^{\prime}>0\Rightarrow h^{\prime\prime}<0,\qquad A^{\prime}<0\Rightarrow h^{\prime\prime}>0','Mặt thoáng rộng dần thì nước dâng chậm dần; mặt thoáng hẹp dần thì nước dâng nhanh dần.'),
  T('Mỗi bài: đề → mặt thoáng → tốc độ → diễn giải → tự luyện.', 'Bây giờ ta làm mười hai mô hình. Với mỗi bài, hãy nhận diện đúng mặt thoáng trước khi viết công thức.')
 ],'compare')
]

# Each entry: geometry, numeric area, symbolic rate, interpretation, practice.
DETAILS={
 'B01':{
 'givens':r'R=1\,\mathrm m,\quad H=3\,\mathrm m,\quad Q=0.06\,\mathrm{m^3/s}',
 'question':'Tính tốc độ nước dâng khi mực nước cao 1,2 m.',
 'question_voice':'Bể trụ đứng bán kính một mét, cao ba mét. Bơm đều với lưu lượng không phẩy không sáu mét khối mỗi giây. Tính tốc độ dâng khi mực nước cao một phẩy hai mét.',
 'shape':'Mặt thoáng là hình tròn, bán kính không đổi.',
 'geometry':r'r(h)=R', 'geometry_voice':'Các thiết diện song song với đáy của trụ đứng có cùng bán kính R. Vì thế bán kính mặt thoáng không phụ thuộc vào mực nước.',
 'A':r'A(h)=\pi R^2','Avoice':'Diện tích mặt thoáng bằng pi R bình phương, là một hằng số.',
 'Anum':r'A(1.2)=\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac Q{\pi R^2}',
 'result':r'\boxed{h^{\prime}=\frac{0.06}{\pi}\,\mathrm{m/s}\approx1.910\,\mathrm{cm/s}}',
 'answer_voice':'Tốc độ bằng không phẩy không sáu trên pi mét mỗi giây, xấp xỉ một phẩy chín một không xăng ti mét mỗi giây.',
 'trend':'Diện tích mặt thoáng không đổi → nước dâng đều.',
 'trend_math':r'h(t)=h_0+\frac Q{\pi R^2}t',
 'trend_voice':'Trong bể trụ đứng, mực nước là hàm bậc nhất của thời gian. Cùng khoảng thời gian, mực nước tăng cùng một độ cao.',
 'pitfall':'Chỉ bể có thiết diện ngang không đổi mới dâng đều.',
 'practice':'Giữ bể; tăng lưu lượng lên 0,09 m³/s. Tốc độ mới?',
 'practice_voice':'Tự luyện: giữ nguyên bể và tăng lưu lượng lên không phẩy không chín mét khối mỗi giây. Tốc độ dâng có phụ thuộc mực nước không?',
 'practice_tex':r'\boxed{h^{\prime}=\frac{0.09}{\pi}\,\mathrm{m/s}\approx2.865\,\mathrm{cm/s}}',
 'practice_answer':'Không phụ thuộc mực nước. Chia lưu lượng mới cho pi được khoảng hai phẩy tám sáu năm xăng ti mét mỗi giây.'},
 'B02':{
 'givens':r'a=3,\ b=2,\ H=2\ (\mathrm m),\quad Q=0.12\,\mathrm{m^3/s}',
 'question':'Tính tốc độ dâng tại mực nước 0,8 m.',
 'question_voice':'Bể hộp chữ nhật dài ba mét, rộng hai mét, cao hai mét. Bơm đều không phẩy mười hai mét khối mỗi giây. Tính tốc độ dâng khi nước cao không phẩy tám mét.',
 'shape':'Mặt thoáng là hình chữ nhật, hai kích thước cố định.',
 'geometry':r'\ell=a,\quad w=b','geometry_voice':'Bề dài và bề rộng mặt thoáng bằng hai kích thước nằm ngang của bể. Chiều cao bể không phải một cạnh của mặt thoáng.',
 'A':r'A(h)=ab','Avoice':'Diện tích mặt thoáng bằng chiều dài nhân chiều rộng và không đổi.',
 'Anum':r'A(0.8)=3\cdot2=6\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac Q{ab}',
 'result':r'\boxed{h^{\prime}=0.02\,\mathrm{m/s}=2\,\mathrm{cm/s}}',
 'answer_voice':'Chia không phẩy mười hai cho sáu, được không phẩy không hai mét mỗi giây, tức hai xăng ti mét mỗi giây.',
 'trend':'Tăng kích thước mặt thoáng làm nước dâng chậm hơn.',
 'trend_math':r'A=ab=\text{constant}\quad\Rightarrow\quad h^{\prime}=\text{constant}',
 'trend_voice':'Mực nước dâng đều. Nếu cùng lưu lượng mà mặt thoáng rộng gấp đôi, tốc độ dâng giảm còn một nửa.',
 'pitfall':'Không dùng diện tích mặt đứng của bể để chia lưu lượng.',
 'practice':'Lưu lượng tăng thành 0,18 m³/s; giữ nguyên bể.',
 'practice_voice':'Tự luyện: với cùng bể, tăng lưu lượng lên không phẩy mười tám mét khối mỗi giây. Tính tốc độ dâng.',
 'practice_tex':r'\boxed{h^{\prime}=\frac{0.18}{6}=0.03\,\mathrm{m/s}=3\,\mathrm{cm/s}}',
 'practice_answer':'Diện tích vẫn bằng sáu mét vuông, nên tốc độ mới bằng ba xăng ti mét mỗi giây.'},
 'B03':{
 'givens':r'R=2,\ H=4\ (\mathrm m),\quad Q=0.04\,\mathrm{m^3/s}',
 'question':'Phễu nón đỉnh xuống: tính tốc độ khi nước cao 2 m.',
 'question_voice':'Phễu hình nón có đỉnh xuống dưới, miệng bán kính hai mét, cao bốn mét. Nước vào đều không phẩy không bốn mét khối mỗi giây. Tính tốc độ dâng ở mức hai mét.',
 'shape':'Mặt thoáng là hình tròn có bán kính tăng theo độ cao.',
 'geometry':r'\frac rR=\frac hH\quad\Rightarrow\quad r=\frac RHh','geometry_voice':'Trong thiết diện qua trục, hai tam giác đồng dạng. Bán kính mặt thoáng chia bán kính miệng bằng mực nước chia chiều cao phễu.',
 'A':r'A(h)=\pi\left(\frac RHh\right)^2','Avoice':'Mặt thoáng tròn nên diện tích là pi nhân bình phương bán kính vừa tìm. Diện tích tăng theo bình phương mực nước.',
 'Anum':r'r(2)=1\,\mathrm m,\qquad A(2)=\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac{QH^2}{\pi R^2h^2}',
 'result':r'\boxed{h^{\prime}=\frac{0.04}{\pi}\,\mathrm{m/s}\approx1.273\,\mathrm{cm/s}}',
 'answer_voice':'Tại h bằng hai, bán kính mặt nước là một mét. Tốc độ bằng không phẩy không bốn trên pi mét mỗi giây, khoảng một phẩy hai bảy ba xăng ti mét mỗi giây.',
 'trend':'Mặt thoáng rộng dần → nước dâng chậm dần.',
 'trend_math':r'A\propto h^2\quad\Rightarrow\quad h^{\prime}\propto\frac1{h^2}',
 'trend_voice':'Mực nước tăng gấp đôi thì diện tích mặt thoáng tăng bốn lần. Với cùng lưu lượng, tốc độ dâng giảm còn một phần tư.',
 'pitfall':'Bán kính cần dùng là bán kính mặt nước, không phải bán kính miệng.',
 'practice':'Ở mức nước 1 m, tốc độ bằng bao nhiêu lần tại 2 m?',
 'practice_voice':'Tự luyện: tính tốc độ ở mức một mét và so sánh với mức hai mét. Dừng video để tự giải nếu cần.',
 'practice_tex':r'\boxed{h^{\prime}(h=1)=\frac{0.16}{\pi}\,\mathrm{m/s}\approx5.093\,\mathrm{cm/s}}',
 'practice_answer':'Mức một mét có bán kính không phẩy năm mét. Diện tích là pi trên bốn, nên tốc độ khoảng năm phẩy không chín ba xăng ti mét mỗi giây, gấp bốn lần.'},
 'B04':{
 'givens':r'R=2\,\mathrm m,\quad Q=0.08\,\mathrm{m^3/s},\quad 0<h<4',
 'question':'Bình cầu: tính tốc độ ở mức h = 1 m và tìm mức dâng chậm nhất.',
 'question_voice':'Bình cầu bán kính hai mét, có lỗ bơm và thông khí. Bơm đều không phẩy không tám mét khối mỗi giây. Tính tốc độ ở mức một mét và tìm mức nước dâng chậm nhất.',
 'shape':'Mặt thoáng là hình tròn; tâm cầu cách đáy một bán kính.',
 'geometry':r'r^2+(h-R)^2=R^2\quad\Rightarrow\quad r^2=h(2R-h)','geometry_voice':'Khoảng cách thẳng đứng từ tâm cầu tới mặt nước là trị tuyệt đối của h trừ R. Pi ta go cho r bình bằng h nhân hai R trừ h.',
 'A':r'A(h)=\pi h(2R-h)','Avoice':'Diện tích mặt thoáng bằng pi nhân h nhân hai R trừ h. Nó tăng trước tâm, rồi giảm sau tâm.',
 'Anum':r'A(1)=3\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac Q{\pi h(2R-h)}',
 'result':r'\boxed{h^{\prime}(h=1)=\frac{0.08}{3\pi}\,\mathrm{m/s}\approx0.849\,\mathrm{cm/s}}',
 'answer_voice':'Ở mức một mét, diện tích mặt thoáng là ba pi mét vuông. Tốc độ khoảng không phẩy tám bốn chín xăng ti mét mỗi giây.',
 'trend':'Chậm dần tới tâm, rồi nhanh dần sau khi vượt tâm.',
 'trend_math':r'A(h)=\pi\bigl[R^2-(h-R)^2\bigr]\le\pi R^2',
 'trend_voice':'Diện tích mặt thoáng lớn nhất tại h bằng R. Vì lưu lượng cố định, đó là vị trí có tốc độ dâng nhỏ nhất. Không được nói nước luôn chậm dần trong cả bình cầu.',
 'pitfall':'Gần đáy và đỉnh, mô hình lý tưởng có A tiến về 0.',
 'practice':'Ở mức 3 m, tốc độ có bằng mức 1 m không?',
 'practice_voice':'Tự luyện: so sánh tốc độ ở mức ba mét với mức một mét. Hãy dùng tính đối xứng của mặt cầu.',
 'practice_tex':r'\boxed{A(3)=A(1)=3\pi;\quad h^{\prime}(h=3)=h^{\prime}(h=1)}',
 'practice_answer':'Hai mặt thoáng cách tâm một mét nên có cùng diện tích. Tốc độ ở hai mức bằng nhau, cùng khoảng không phẩy tám bốn chín xăng ti mét mỗi giây.'},
 'B05':{
 'givens':r'R=2\,\mathrm m,\quad Q=0.06\,\mathrm{m^3/s},\quad 0<h<2',
 'question':'Bát bán cầu: tính tốc độ ở mức h = 1 m.',
 'question_voice':'Bát bán cầu là nửa dưới của một mặt cầu bán kính hai mét, miệng nằm ngang hướng lên. Bơm đều không phẩy không sáu mét khối mỗi giây. Tính tốc độ ở mức một mét.',
 'shape':'Chỉ xét nửa dưới của hình cầu: mặt thoáng mở rộng tới miệng.',
 'geometry':r'r^2+(R-h)^2=R^2','geometry_voice':'Tâm của mặt cầu gốc nằm ở tâm miệng bát. Khoảng cách từ mặt nước tới tâm là R trừ h.' ,
 'A':r'A(h)=\pi h(2R-h),\quad 0<h\le R','Avoice':'Diện tích có công thức giống bình cầu, nhưng miền mực nước chỉ tới R. Vì thế diện tích tăng trong toàn bộ phần bên trong bát.',
 'Anum':r'A(1)=3\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac Q{\pi h(2R-h)}',
 'result':r'\boxed{h^{\prime}(h=1)=\frac{0.06}{3\pi}\,\mathrm{m/s}\approx0.637\,\mathrm{cm/s}}',
 'answer_voice':'Tốc độ tại mức một mét là không phẩy không sáu chia ba pi, khoảng không phẩy sáu ba bảy xăng ti mét mỗi giây.',
 'trend':'Dâng chậm dần; không có giai đoạn vượt tâm trong bát.',
 'trend_math':r'A^{\prime}(h)=2\pi(R-h)>0\quad(0<h<R)',
 'trend_voice':'Đạo hàm diện tích dương ở bên trong bát. Mực nước càng cao, mặt thoáng càng rộng và tốc độ dâng càng nhỏ.',
 'pitfall':'Đến miệng bát thì xét giới hạn trước khi tràn, không tiếp tục h > R.',
 'practice':'Tính giới hạn tốc độ khi nước tiến tới miệng bát.',
 'practice_voice':'Tự luyện: tính tốc độ ngay trước khi nước chạm miệng. Đây là giới hạn từ phía dưới, chưa xét nước tràn ra.',
 'practice_tex':r'\boxed{\lim_{h\to2^-}h^{\prime}=\frac{0.06}{4\pi}\,\mathrm{m/s}\approx0.477\,\mathrm{cm/s}}',
 'practice_answer':'Khi h tiến tới hai mét từ dưới, diện tích tiến tới bốn pi. Tốc độ tiến tới khoảng không phẩy bốn bảy bảy xăng ti mét mỗi giây.'},
 'B06':{
 'givens':r'a=4,\ H=3\ (\mathrm m),\quad Q=0.08\,\mathrm{m^3/s}',
 'question':'Chóp vuông đỉnh xuống: tính tốc độ ở mức 1,5 m.',
 'question_voice':'Bể hình chóp vuông đều, đỉnh hướng xuống, miệng cạnh bốn mét, cao ba mét. Bơm đều không phẩy không tám mét khối mỗi giây. Tính tốc độ tại một phẩy năm mét.',
 'shape':'Mặt thoáng là hình vuông; cạnh thay đổi theo mực nước.',
 'geometry':r'\frac{s(h)}a=\frac hH\quad\Rightarrow\quad s(h)=\frac aHh','geometry_voice':'Các thiết diện song song với miệng bể đồng dạng. Cạnh mặt nước chia cạnh miệng bằng h chia H.',
 'A':r'A(h)=s(h)^2=\frac{a^2h^2}{H^2}','Avoice':'Diện tích mặt thoáng là bình phương cạnh hình vuông. Không có hệ số một phần ba trong diện tích mặt thoáng.',
 'Anum':r's(1.5)=2\,\mathrm m,\quad A(1.5)=4\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac{QH^2}{a^2h^2}',
 'result':r'\boxed{h^{\prime}=\frac{0.08}{4}=0.02\,\mathrm{m/s}=2\,\mathrm{cm/s}}',
 'answer_voice':'Tại mức một phẩy năm mét, cạnh mặt thoáng là hai mét, diện tích bốn mét vuông. Tốc độ bằng hai xăng ti mét mỗi giây.',
 'trend':'Giống nón đỉnh xuống: tốc độ tỉ lệ nghịch với h².',
 'trend_math':r'h^{\prime}\propto h^{-2}',
 'trend_voice':'Dù mặt thoáng vuông thay vì tròn, diện tích vẫn tỉ lệ với h bình. Vì vậy nước dâng chậm dần giống nón đỉnh xuống.',
 'pitfall':'Một phần ba thuộc công thức thể tích chóp, không thuộc A(h).',
 'practice':'Tính tốc độ khi h = 1 m.',
 'practice_voice':'Tự luyện: trong cùng bể, tính tốc độ khi h bằng một mét. Cạnh mặt thoáng lúc này không phải hai mét.',
 'practice_tex':r'\boxed{A(1)=\frac{16}{9};\quad h^{\prime}=0.045\,\mathrm{m/s}=4.5\,\mathrm{cm/s}}',
 'practice_answer':'Cạnh bằng bốn phần ba, diện tích bằng mười sáu phần chín. Chia không phẩy không tám cho diện tích này được bốn phẩy năm xăng ti mét mỗi giây.'},
 'B07':{
 'givens':r'b=3,\ H=2,\ L=6\ (\mathrm m),\quad Q=0.12\,\mathrm{m^3/s}',
 'question':'Máng có tiết diện tam giác cân đỉnh xuống; tính tốc độ tại h = 1 m.',
 'question_voice':'Máng dài sáu mét, tiết diện ngang là tam giác cân đỉnh xuống, miệng rộng ba mét và sâu hai mét. Bơm đều không phẩy mười hai mét khối mỗi giây. Tính tốc độ ở mức một mét.',
 'shape':'Mặt thoáng là hình chữ nhật: dài cố định, rộng thay đổi.',
 'geometry':r'\frac{w(h)}b=\frac hH\quad\Rightarrow\quad w(h)=\frac bHh','geometry_voice':'Trong mặt cắt tam giác, dùng đồng dạng tìm bề rộng mặt nước bằng b nhân h chia H.' ,
 'A':r'A(h)=Lw(h)=\frac{bL}{H}h','Avoice':'Mặt thoáng nằm ngang là hình chữ nhật dài L, rộng w. Không dùng diện tích tam giác ở đầu máng làm mặt thoáng.' ,
 'Anum':r'w(1)=1.5\,\mathrm m,\quad A(1)=6\cdot1.5=9\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac{QH}{bLh}',
 'result':r'\boxed{h^{\prime}=\frac{0.12}{9}\,\mathrm{m/s}\approx1.333\,\mathrm{cm/s}}',
 'answer_voice':'Mặt thoáng rộng một phẩy năm mét, dài sáu mét, diện tích chín mét vuông. Tốc độ khoảng một phẩy ba ba ba xăng ti mét mỗi giây.',
 'trend':'Diện tích tăng theo h; tốc độ giảm theo 1/h.',
 'trend_math':r'A\propto h\quad\Rightarrow\quad h^{\prime}\propto h^{-1}',
 'trend_voice':'Mực nước gấp đôi làm bề rộng và diện tích gấp đôi, nên tốc độ giảm còn một nửa. Khác với nón, không giảm còn một phần tư.',
 'pitfall':'Đầu máng là tam giác; mặt thoáng nước là hình chữ nhật.',
 'practice':'Tính tốc độ ở mức h = 1,5 m.',
 'practice_voice':'Tự luyện: tính tốc độ khi nước cao một phẩy năm mét. Trước hết tìm bề rộng mặt thoáng mới.',
 'practice_tex':r'\boxed{A(1.5)=13.5;\quad h^{\prime}=\frac{0.12}{13.5}\,\mathrm{m/s}\approx0.889\,\mathrm{cm/s}}',
 'practice_answer':'Bề rộng là hai phẩy hai năm mét, diện tích mười ba phẩy năm mét vuông. Tốc độ khoảng không phẩy tám tám chín xăng ti mét mỗi giây.'},
 'B08':{
 'givens':r'R=1.5,\ L=5\ (\mathrm m),\quad Q=0.09\,\mathrm{m^3/s}',
 'question':'Bồn trụ ngang: tính tốc độ tại h = 0,6 m.',
 'question_voice':'Bồn trụ nằm ngang có bán kính một phẩy năm mét, dài năm mét. Bơm đều không phẩy không chín mét khối mỗi giây. Tính tốc độ khi nước cao không phẩy sáu mét tính từ đáy.' ,
 'shape':'Mặt thoáng là hình chữ nhật; bề rộng là một dây cung.',
 'geometry':r'\left(\frac w2\right)^2+(R-h)^2=R^2','geometry_voice':'Trong mặt cắt tròn vuông góc trục bồn, mặt nước tạo thành một dây cung. Nửa dây, khoảng cách tới tâm và bán kính tạo tam giác vuông.' ,
 'A':r'w=2\sqrt{h(2R-h)},\qquad A(h)=2L\sqrt{h(2R-h)}','Avoice':'Dây cung dài hai căn h nhân hai R trừ h. Nhân chiều dài bồn L ta được diện tích mặt thoáng hình chữ nhật.' ,
 'Anum':r'w(0.6)=2.4\,\mathrm m,\quad A(0.6)=12\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac Q{2L\sqrt{h(2R-h)}}',
 'result':r'\boxed{h^{\prime}=\frac{0.09}{12}=0.0075\,\mathrm{m/s}=0.75\,\mathrm{cm/s}}',
 'answer_voice':'Thay h bằng không phẩy sáu, dây cung dài hai phẩy bốn mét. Mặt thoáng mười hai mét vuông, tốc độ không phẩy bảy năm xăng ti mét mỗi giây.' ,
 'trend':'Chậm nhất khi mặt nước đi qua trục bồn.',
 'trend_math':r'h(2R-h)=R^2-(h-R)^2\le R^2','trend_voice':'Dây cung dài nhất khi mặt nước qua trục, tức h bằng R. Diện tích khi đó lớn nhất, nên tốc độ dâng nhỏ nhất. Trước trục chậm dần, sau trục nhanh dần.' ,
 'pitfall':'Không dùng πR²: đó là diện tích mặt tròn đứng ở đầu bồn.',
 'practice':'Tính tốc độ nhỏ nhất trong quá trình bơm.',
 'practice_voice':'Tự luyện: tìm tốc độ dâng nhỏ nhất. Hãy dùng diện tích mặt thoáng lớn nhất chứ không tối ưu trực tiếp một biểu thức phức tạp.' ,
 'practice_tex':r'\boxed{h=R=1.5;\ A_{\max}=2LR=15;\ h^{\prime}_{\min}=0.6\,\mathrm{cm/s}}',
 'practice_answer':'Mức nước bằng một phẩy năm mét, diện tích mặt thoáng bằng mười lăm mét vuông. Tốc độ nhỏ nhất là không phẩy sáu xăng ti mét mỗi giây.'},
 'B09':{
 'givens':r'r_0=1,\ r_1=2,\ H=3\ (\mathrm m),\quad Q=0.08\,\mathrm{m^3/s}',
 'question':'Nón cụt đáy nhỏ dưới: tính tốc độ tại h = 1,5 m.',
 'question_voice':'Bể nón cụt có bán kính đáy dưới một mét, miệng trên hai mét, cao ba mét. Bơm đều không phẩy không tám mét khối mỗi giây. Tính tốc độ ở mức một phẩy năm mét.' ,
 'shape':'Mặt thoáng tròn; bán kính nội suy tuyến tính theo độ cao.',
 'geometry':r'r(h)=r_0+\frac{r_1-r_0}{H}h','geometry_voice':'Thành bể thẳng trong thiết diện qua trục. Bán kính tăng tuyến tính từ bán kính đáy dưới tới bán kính miệng.' ,
 'A':r'A(h)=\pi\left(r_0+\frac{r_1-r_0}{H}h\right)^2','Avoice':'Diện tích mặt thoáng là pi nhân bình phương bán kính tại chính độ cao h.' ,
 'Anum':r'r(1.5)=1.5\,\mathrm m,\quad A(1.5)=2.25\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac{Q}{\pi[r_0+(r_1-r_0)h/H]^2}',
 'result':r'\boxed{h^{\prime}=\frac{0.08}{2.25\pi}\,\mathrm{m/s}\approx1.132\,\mathrm{cm/s}}',
 'answer_voice':'Tại mức một phẩy năm mét, bán kính cũng bằng một phẩy năm mét. Tốc độ khoảng một phẩy một ba hai xăng ti mét mỗi giây.' ,
 'trend':'Loe lên trên → diện tích tăng → tốc độ giảm.',
 'trend_math':r'r_1>r_0\quad\Rightarrow\quad A^{\prime}(h)>0','trend_voice':'Vì bán kính miệng lớn hơn bán kính đáy dưới, diện tích tăng với độ cao. Nước dâng chậm dần.' ,
 'pitfall':'Không thay bán kính cố định và không quên bán kính đáy dưới.',
 'practice':'Tính tốc độ khi h = 0,75 m.',
 'practice_voice':'Tự luyện: tính tốc độ khi mực nước không phẩy bảy năm mét. Đây là mức thấp hơn, nên hãy dự đoán nhanh hơn hay chậm hơn trước khi tính.' ,
 'practice_tex':r'\boxed{r=1.25;\quad h^{\prime}=\frac{0.08}{1.5625\pi}\,\mathrm{m/s}\approx1.630\,\mathrm{cm/s}}',
 'practice_answer':'Bán kính bằng một phẩy hai năm mét, tốc độ khoảng một phẩy sáu ba không xăng ti mét mỗi giây. Đúng như dự đoán, mức thấp dâng nhanh hơn.'},
 'B10':{
 'givens':r'r_0=2,\ r_1=1,\ H=3\ (\mathrm m),\quad Q=0.08\,\mathrm{m^3/s}',
 'question':'Nón cụt đáy lớn dưới: tính tốc độ tại h = 1,5 m.',
 'question_voice':'Đảo chiều nón cụt: bán kính đáy dưới hai mét, miệng trên một mét, cao ba mét. Lưu lượng vẫn không phẩy không tám mét khối mỗi giây. Tính tốc độ ở mức một phẩy năm mét.' ,
 'shape':'Mặt thoáng vẫn tròn, nhưng bán kính giảm khi h tăng.',
 'geometry':r'r(h)=2-\frac h3','geometry_voice':'Bán kính biến thiên tuyến tính từ hai xuống một mét, nên r của h bằng hai trừ h chia ba.' ,
 'A':r'A(h)=\pi\left(2-\frac h3\right)^2','Avoice':'Diện tích mặt thoáng bằng pi nhân hai trừ h trên ba, tất cả bình phương.' ,
 'Anum':r'r(1.5)=1.5\,\mathrm m,\quad A(1.5)=2.25\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac Q{\pi(2-h/3)^2}',
 'result':r'\boxed{h^{\prime}=\frac{0.08}{2.25\pi}\,\mathrm{m/s}\approx1.132\,\mathrm{cm/s}}',
 'answer_voice':'Ở đúng giữa bể, bán kính bằng một phẩy năm mét nên tốc độ giống nón cụt vừa rồi: khoảng một phẩy một ba hai xăng ti mét mỗi giây.' ,
 'trend':'Thu hẹp lên trên → diện tích giảm → tốc độ tăng.',
 'trend_math':r'A^{\prime}(h)=-\frac{2\pi}{3}\left(2-\frac h3\right)<0','trend_voice':'Diện tích mặt thoáng giảm theo độ cao trong toàn bể. Do đó nước dâng nhanh dần, ngược với bể loe lên.' ,
 'pitfall':'Hai bể có cùng diện tích ở một mức không có nghĩa là cùng xu hướng.',
 'practice':'Tính tốc độ khi h = 2,25 m.',
 'practice_voice':'Tự luyện: tính tốc độ ở mức hai phẩy hai năm mét. Bán kính nhỏ hơn, nên tốc độ phải lớn hơn tại giữa bể.' ,
 'practice_tex':r'\boxed{r=1.25;\quad h^{\prime}=\frac{0.08}{1.5625\pi}\,\mathrm{m/s}\approx1.630\,\mathrm{cm/s}}',
 'practice_answer':'Bán kính bằng một phẩy hai năm mét. Tốc độ khoảng một phẩy sáu ba không xăng ti mét mỗi giây, lớn hơn mức giữa bể.'},
 'B11':{
 'givens':r'a=2,\ b=1.5,\ c=2\ (\mathrm m),\quad Q=0.06\,\mathrm{m^3/s}',
 'question':'Ellipsoid có bán trục đứng c: tính tốc độ tại h = 1 m.',
 'question_voice':'Bình ellipsoid có hai bán trục ngang hai mét và một phẩy năm mét, bán trục đứng hai mét. Bơm đều không phẩy không sáu mét khối mỗi giây. Tính tốc độ tại h bằng một mét.' ,
 'shape':'Mặt thoáng là ellipse, không phải hình tròn.',
 'geometry':r'\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{(h-c)^2}{c^2}=1','geometry_voice':'Gốc chiều cao ở đáy bình nên tọa độ đứng so với tâm là h trừ c. Cắt ellipsoid bởi mặt phẳng ngang ta được phương trình ellipse.' ,
 'A':r'A(h)=\pi ab\left[1-\frac{(h-c)^2}{c^2}\right]','Avoice':'Hai bán trục ellipse đều nhân cùng căn của một trừ h trừ c bình trên c bình. Tích hai bán trục cho diện tích này.' ,
 'Anum':r'A(1)=\pi\cdot2\cdot1.5\cdot\frac34=2.25\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac{Q}{\pi ab[1-(h-c)^2/c^2]}',
 'result':r'\boxed{h^{\prime}=\frac{0.06}{2.25\pi}\,\mathrm{m/s}\approx0.849\,\mathrm{cm/s}}',
 'answer_voice':'Tại mức một mét, hệ số diện tích bằng ba phần tư, diện tích là hai phẩy hai năm pi. Tốc độ khoảng không phẩy tám bốn chín xăng ti mét mỗi giây.' ,
 'trend':'Chậm nhất ở mặt phẳng ngang qua tâm bình.',
 'trend_math':r'A(h)\le\pi ab\quad\text{with equality at }h=c','trend_voice':'Diện tích ellipse lớn nhất bằng pi a b khi h bằng c, tức mặt nước đi qua tâm ellipsoid. Ở đó tốc độ dâng nhỏ nhất.' ,
 'pitfall':'a, b, c là bán trục; không dùng nhầm độ dài cả trục.',
 'practice':'So sánh tốc độ tại h = 3 m và h = 1 m.',
 'practice_voice':'Tự luyện: tốc độ ở mức ba mét có bằng mức một mét không? Hãy xét tính đối xứng qua mặt phẳng ngang đi qua tâm.' ,
 'practice_tex':r'\boxed{A(3)=A(1)=2.25\pi;\quad h^{\prime}(h=3)=h^{\prime}(h=1)}',
 'practice_answer':'Hai mặt thoáng cách tâm một mét nên có cùng diện tích. Tốc độ bằng nhau, khoảng không phẩy tám bốn chín xăng ti mét mỗi giây.'},
 'B12':{
 'givens':r'H=4\,\mathrm m,\quad r(h)=1+\frac{(h-2)^2}{4},\quad Q=0.05\,\mathrm{m^3/s}',
 'question':'Bình thắt cổ: tính tốc độ tại h = 2 m và tìm nơi dâng nhanh nhất.',
 'question_voice':'Một bình tròn xoay cao bốn mét, bán kính tại độ cao h bằng một cộng h trừ hai bình phương chia bốn, tính bằng mét. Bơm đều không phẩy không năm mét khối mỗi giây. Tính tốc độ ở mức hai mét và tìm nơi dâng nhanh nhất.' ,
 'shape':'Mặt thoáng tròn; bán kính nhỏ nhất ở cổ bình.',
 'geometry':r'r(h)\ge1,\qquad r(h)=1\iff h=2','geometry_voice':'Bình hẹp nhất ở giữa, khi h bằng hai mét, bán kính bằng một mét. Phía dưới và phía trên cổ, bán kính đều lớn hơn.' ,
 'A':r'A(h)=\pi\left[1+\frac{(h-2)^2}{4}\right]^2','Avoice':'Mặt thoáng là hình tròn, nên diện tích bằng pi nhân bình phương hàm bán kính cho trước.' ,
 'Anum':r'A(2)=\pi\,\mathrm{m^2}',
 'rate':r'h^{\prime}=\frac{0.05}{\pi[1+(h-2)^2/4]^2}',
 'result':r'\boxed{h^{\prime}(h=2)=\frac{0.05}{\pi}\,\mathrm{m/s}\approx1.592\,\mathrm{cm/s}}',
 'answer_voice':'Ở cổ bình, diện tích bằng pi, tốc độ khoảng một phẩy năm chín hai xăng ti mét mỗi giây.' ,
 'trend':'Nhanh dần tới cổ; chậm dần sau cổ.',
 'trend_math':r'A(h)\ge\pi\quad\Rightarrow\quad h^{\prime}\le\frac{0.05}{\pi}',
 'trend_voice':'Diện tích nhỏ nhất ở cổ bình nên tốc độ dâng lớn nhất ở cổ. Kết luận ngược với bình cầu, nơi diện tích lớn nhất nằm ở giữa.' ,
 'pitfall':'Không kết luận dựa vào độ cao; hãy xét diện tích mặt thoáng.',
 'practice':'Tính tốc độ tại h = 1 m và so với tại cổ bình.',
 'practice_voice':'Tự luyện: tính tốc độ ở mức một mét, rồi so với tốc độ ở cổ. Bình đối xứng nên mức ba mét sẽ có cùng đáp án.' ,
 'practice_tex':r'\boxed{r(1)=1.25;\quad h^{\prime}=\frac{0.05}{1.5625\pi}\,\mathrm{m/s}\approx1.019\,\mathrm{cm/s}}',
 'practice_answer':'Bán kính một phẩy hai năm mét, tốc độ khoảng một phẩy không một chín xăng ti mét mỗi giây, nhỏ hơn tại cổ bình.'}
}


def build_lessons():
    lessons=[{'id':'INTRO','title':'Mặt thoáng quyết định tốc độ nước dâng',
              'model':dict(MODELS[8]),'pages':THEORY}]
    for model in MODELS:
        d=DETAILS[model['id']]
        pages=[
         P('Đề bài • Đọc hình và xác định đại lượng',[
          T(d['question'],d['question_voice']),
          M(d['givens'],'Các kích thước dùng đơn vị mét, lưu lượng dùng mét khối mỗi giây. Mực nước h đo thẳng đứng từ đáy.'),
          T(d['shape'],'Quan sát hình thật bên trái và góc nhìn từ trên. '+d['shape']),
          T('Tìm diện tích mặt thoáng tại đúng mức nước đang xét.','Trước khi tính tốc độ, hãy xác định hình dạng và kích thước mặt thoáng ở mức nước này.')
         ],'orient'),
         P('Diện tích mặt thoáng • Lập quan hệ hình học',[
          M(d['geometry'],d['geometry_voice']),
          M(d['A'],d['Avoice']),
          M(d['Anum'],'Thay kích thước và mực nước trong đề để tính diện tích mặt thoáng tại thời điểm cần xét.'),
          T(d['pitfall'],'Chú ý: '+d['pitfall'])
         ],'highlight'),
         P('Tốc độ tức thời • Thay số và kiểm tra đơn vị',[
          M(r'Q=A(h)\,h^{\prime}(t)','Lưu lượng bằng diện tích mặt thoáng nhân tốc độ mực nước dâng.'),
          M(d['rate'],'Chia hai vế cho diện tích mặt thoáng dương, ta được công thức tốc độ.'),
          M(d['result'],d['answer_voice'],True),
          M(r'1\,\mathrm{m/s}=100\,\mathrm{cm/s}','Đổi từ mét mỗi giây sang xăng ti mét mỗi giây phải nhân một trăm. Không nhầm với đổi đơn vị lưu lượng.')
         ],'level'),
         P('Nước dâng nhanh hay chậm? • Quan sát theo thời gian',[
          T(d['trend'],d['trend_voice']),
          M(d['trend_math'],'Quan hệ trên thể hiện rõ kết luận vừa nêu.'),
          T('Mỗi giây vật lý được bơm cùng một thể tích nước.','Quan sát lượt bơm: thời gian vật lý tăng đều, nhưng độ cao chỉ tăng đều khi diện tích mặt thoáng không đổi.'),
          T('So sánh mặt thoáng và tốc độ ở các mức khác nhau.','Đối chiếu mặt thoáng nhìn từ trên với số đo diện tích và tốc độ. Mặt thoáng rộng hơn thì mực nước dâng chậm hơn.')
         ],'fill'),
         P('Tự luyện • Dừng video rồi đối chiếu lời giải',[
          T(d['practice'],d['practice_voice'],pause=7),
          M(d['practice_tex'],d['practice_answer'],True),
          T('Cách giải: hình mặt thoáng → diện tích → Q/A.','Dù đổi mực nước hay lưu lượng, cách giải vẫn là xác định mặt thoáng, tính diện tích rồi chia lưu lượng cho diện tích đó.')
         ],'practice')
        ]
        lessons.append({'id':model['id'],'title':model['title'],'model':model,'pages':pages})
    lessons.append({'id':'END','title':'Tổng kết • Một công thức, nhiều mô hình',
        'model':dict(MODELS[11]),'pages':[
         P('Phân loại theo diện tích mặt thoáng',[
          T('Không đổi: trụ đứng, hộp chữ nhật.','Trụ đứng và hộp chữ nhật có mặt thoáng không đổi nên nước dâng đều.'),
          T('Tăng dần: nón đỉnh xuống, chóp, máng, bể loe.','Nón đỉnh xuống, chóp vuông, máng tam giác, bán cầu và bể loe có mặt thoáng tăng dần nên nước dâng chậm dần.'),
          T('Có cực trị: cầu, trụ ngang, ellipsoid, bình thắt cổ.','Bình cầu, trụ ngang và ellipsoid dâng chậm nhất ở giữa. Bình thắt cổ lại dâng nhanh nhất ở cổ.'),
          M(r'\boxed{h^{\prime}(t)=Q/A(h)}','Chỉ một công thức, nhưng hình dạng mặt thoáng quyết định toàn bộ sự khác nhau.',True)
         ],'compare'),
         P('Nếu vừa bơm vào vừa rút ra?',[
          M(r'Q_{\rm net}=Q_{\rm in}-Q_{\rm out}', 'Nếu có dòng vào và dòng ra, trước hết tính lưu lượng thuần bằng dòng vào trừ dòng ra.'),
          M(r'\boxed{h^{\prime}=\frac{Q_{\rm in}-Q_{\rm out}}{A(h)}}','Tốc độ mực nước bằng lưu lượng thuần chia diện tích mặt thoáng.',True),
          M(r'Q_{\rm in}>Q_{\rm out}:h^{\prime}>0;\quad Q_{\rm in}<Q_{\rm out}:h^{\prime}<0','Lưu lượng thuần dương thì nước dâng, âm thì nước hạ. Nếu hai lưu lượng bằng nhau, mức nước đứng yên.'),
          T('Lưu lượng thay đổi: không suy ra xu hướng chỉ từ diện tích.','Khi lưu lượng thuần thay đổi theo thời gian hoặc độ cao, phải xét cả lưu lượng và diện tích. Kết luận nhanh chậm ở các bài trước giả sử lưu lượng không đổi.')
         ]),
         P('Ba lỗi cần tránh',[
          T('Nhầm mặt thoáng với đáy, thành bể hoặc tiết diện đứng.','Lỗi thứ nhất là chọn nhầm diện tích. Trụ nằm ngang và máng tam giác cho thấy mặt cắt ở đầu bể không phải mặt thoáng.'),
          T('Nhầm lưu lượng thể tích với tốc độ mực nước.','Lỗi thứ hai là nhầm mét khối mỗi giây với mét mỗi giây. Luôn kiểm tra đơn vị.'),
          T('Bỏ qua miền mực nước, điểm nhọn và thời điểm tràn.','Lỗi thứ ba là bỏ qua miền vật lý. Ở điểm diện tích bằng không, không có tốc độ hữu hạn theo mô hình này; đến miệng bể cần xét chuyện tràn.'),
          T('Hãy nhìn mặt thoáng trước khi viết công thức.','Các em hãy luyện thói quen nhìn mặt thoáng trước khi viết công thức. Khi hình được hiểu đúng, lời giải sẽ ngắn và rõ ràng.')
         ],'highlight')
    ]})
    return lessons

# ========================== MANIM 3D ==========================
# Common model functions are injected from the exact code above, not duplicated.
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
TMPL=TexTemplate();TMPL.add_to_preamble(r'\usepackage{amsmath}\usepackage{amssymb}\usepackage{bm}')
# MODEL_FUNCTIONS

def pt(x,y,z=0):return np.array([x,y,z],dtype=float)
def txt(s,size=24,color=INK,bold=False):
    return Text(s,font='DejaVu Sans',font_size=size,color=color,
                weight='BOLD' if bold else 'NORMAL',disable_ligatures=True)
def mtx(s,size=31,color=INK):return MathTex(s,font_size=size,color=color,tex_template=TMPL)
def fit(m,w,h=None):
    k=min(1,w/max(m.width,1e-9))
    if h is not None:k=min(k,h/max(m.height,1e-9))
    return m.scale(k)
def pane(w,h,center,fill=1):
    return RoundedRectangle(width=w,height=h,corner_radius=.15,fill_color=PANEL,
        fill_opacity=fill,stroke_color=MUTED,stroke_opacity=.25,stroke_width=1.2).move_to(center)
def shaded(m):return m.set_shade_in_3d(True)

class TankView:
    """World z is vertical. Screen placement uses inverse camera rotation."""
    def __init__(self,scene,model):
        self.scene=scene;self.model=model;self.p=model['p'];self.H=self.p['H'];self.kind=model['kind']
        self.capacity=volume(model,self.H)
        self.normal_Q=model['Q']
        self.clock=ValueTracker(volume(model,model['h'])/self.capacity)
        # Camera is fixed; object sits in its left visual column without fake geometry.
        rotation=scene.camera.generate_rotation_matrix()
        sample=[]
        for z in np.linspace(0,self.H,19):
            for x,y,_ in surface_boundary(model,float(z),64):sample.append(pt(x,y,z-self.H/2))
        projected=np.array(sample)@rotation.T
        # Equal scaling in all 3 dimensions, chosen by projected bounding box.
        self.scale=min(4.8/np.ptp(projected[:,0]),3.1/np.ptp(projected[:,1]))
        box_center=(projected.max(axis=0)+projected.min(axis=0))/2
        # Center the projected bounding box, not just the physical axis: cone and
        # frustum outlines are asymmetric in an oblique view.
        self.anchor=rotation.T@(pt(-3.9,.35,0)-self.scale*pt(box_center[0],box_center[1],0))
        self.wall=self.make_wall()
        self.water=VGroup();self.surface=VGroup();self.dimension=VGroup();self.stream=VGroup()
        self.world=VGroup(self.wall,self.water,self.surface,self.dimension,self.stream)
        self.inset=VGroup();self.hud=VGroup()
        self.last=None;self.time_origin=volume(model,model['h']);self.pouring=False
        self.height_label=mtx('h',21,GOLD)
        self.update(force=True)
        self.world.add_updater(lambda _:self.update())
        self.world.suspend_updating()
    def W(self,x,y,z):return self.anchor+self.scale*pt(x,y,z-self.H/2)
    def level(self):return height_from_volume(self.model,self.capacity*self.clock.get_value())
    def polygon(self,points,color=BLUE,opacity=.08,width=1):
        unique=[]
        for p in points:
            if not unique or np.linalg.norm(np.array(p)-np.array(unique[-1]))>1e-9:unique.append(p)
        if len(unique)>1 and np.linalg.norm(np.array(unique[0])-np.array(unique[-1]))<1e-9:unique.pop()
        if len(unique)<3:return VGroup()
        return shaded(Polygon(*[self.W(*p) for p in unique],color=color,stroke_width=width,
                       fill_color=color,fill_opacity=opacity))
    def ring(self,z,color=BLUE,opacity=1):
        shape,a,b=footprint(self.model,z)
        if shape=='rectangle':
            points=[(-a,-b,z),(a,-b,z),(a,b,z),(-a,b,z)]
            g=VGroup()
            # Rear-side edges are muted/dashed; foreground edges are solid.
            for i in range(4):
                p=points[i];q=points[(i+1)%4]
                view=self.scene.camera.generate_rotation_matrix()[2]
                eps=self.H*1e-5;lo=max(0,z-eps);hi=min(self.H,z+eps)
                _,al,bl=footprint(self.model,lo);_,ah,bh=footprint(self.model,hi)
                da=(ah-al)/(hi-lo);db=(bh-bl)/(hi-lo)
                mx=(p[0]+q[0])/2;my=(p[1]+q[1])/2
                normal=pt(np.sign(mx),0,-da) if abs(mx)>1e-9 else pt(0,np.sign(my),-db)
                near=np.dot(normal,view)>=0
                line=Line(self.W(*p),self.W(*q),color=color,stroke_width=1.8) if near else DashedLine(self.W(*p),self.W(*q),color=MUTED,dash_length=.08,stroke_width=1.1)
                g.add(shaded(line).set_opacity(opacity))
            return g
        g=VGroup();view=self.scene.camera.generate_rotation_matrix()[2]
        # Runs share their boundary vertex; no gaps where a visible arc changes.
        thetas=np.linspace(0,TAU,193)
        visible=[np.dot(wall_normal(self.model,z,float(t)),view)>=0 for t in thetas]
        start=0
        for stop in range(1,len(thetas)):
            if visible[stop]!=visible[start] or stop==len(thetas)-1:
                end=stop
                points=[self.W(a*np.cos(t),b*np.sin(t),z) for t in thetas[start:end+1]]
                if len(points)>1:
                    curve=VMobject(color=color if visible[start] else MUTED,stroke_width=1.9 if visible[start] else 1.0)
                    curve.set_points_as_corners(points)
                    if not visible[start]:curve=DashedVMobject(curve,num_dashes=max(2,int((end-start)/3)),dashed_ratio=.45)
                    g.add(shaded(curve).set_opacity(opacity))
                start=stop
        return g

    def quadric_outline(self):
        # Exact apparent contour: x=Dq, |q|=1, (D^-1 view).q=0.
        p=self.p;k=self.kind
        dims=np.array([p['a'],p['b'],p['c']]) if k=='ellipsoid' else np.array([p['R']]*3)
        center=np.array([0.,0.,p['c'] if k=='ellipsoid' else p['R']])
        view=self.scene.camera.generate_rotation_matrix()[2];n=view/dims;n/=np.linalg.norm(n)
        seed=np.array([0.,0.,1.]) if abs(n[2])<.9 else np.array([1.,0.,0.])
        e=np.cross(n,seed);e/=np.linalg.norm(e);f=np.cross(n,e)
        pts=[center+dims*(e*np.cos(t)+f*np.sin(t)) for t in np.linspace(0,TAU,257)]
        if k=='hemisphere':pts=[p for p in pts if p[2]<=self.H+1e-8]
        if k=='hemisphere':
            # Below-equator contour may consist of two runs; draw clipped spans.
            g=VGroup();run=[]
            allpts=[center+dims*(e*np.cos(t)+f*np.sin(t)) for t in np.linspace(0,TAU,257)]
            for pnt in allpts:
                if pnt[2]<=self.H+1e-8:run.append(self.W(*pnt))
                elif run:
                    if len(run)>1:g.add(VMobject(color=BLUE,stroke_width=2.1).set_points_as_corners(run))
                    run=[]
            if len(run)>1:g.add(VMobject(color=BLUE,stroke_width=2.1).set_points_as_corners(run))
            return g
        return shaded(VMobject(color=BLUE,stroke_width=2.1).set_points_as_corners([self.W(*p) for p in pts]))

    def make_wall(self):
        k=self.kind;H=self.H;p=self.p;g=VGroup();res=SETTINGS['wall_resolution']
        if k=='horizontal':
            R=p['R'];L=p['L']
            wall=Surface(lambda u,v:self.W(u,R*np.sin(v),R-R*np.cos(v)),
                u_range=[-L/2,L/2],v_range=[-PI,PI],resolution=(8,64),
                checkerboard_colors=[BLUE,BLUE],fill_opacity=.035,stroke_width=0)
            g.add(wall)
            for x in [-L/2,L/2]:
                ring=ParametricFunction(lambda t,x=x:self.W(x,R*np.sin(t),R-R*np.cos(t)),
                      t_range=[-PI,PI],color=BLUE,stroke_width=2)
                g.add(shaded(ring))
            view=self.scene.camera.generate_rotation_matrix()[2]
            tangent=math.atan2(view[2],view[1])
            for theta in [tangent,tangent+PI]:
                g.add(shaded(Line(self.W(-L/2,R*np.sin(theta),R-R*np.cos(theta)),
                                  self.W(L/2,R*np.sin(theta),R-R*np.cos(theta)),color=MUTED,stroke_width=1)))
        elif k in ('box','pyramid','trough'):
            # Four planes; apex/line at z=0 may be degenerate, use actual endpoints.
            _,a0,b0=footprint(self.model,0);_,a1,b1=footprint(self.model,H)
            low=[(-a0,-b0,0),(a0,-b0,0),(a0,b0,0),(-a0,b0,0)]
            high=[(-a1,-b1,H),(a1,-b1,H),(a1,b1,H),(-a1,b1,H)]
            for i in range(4):
                j=(i+1)%4
                g.add(self.polygon([low[i],low[j],high[j],high[i]],opacity=.05,width=.8))
                da=(a1-a0)/H;db=(b1-b0)/H;view=self.scene.camera.generate_rotation_matrix()[2]
                sx=np.sign(high[i][0]);sy=np.sign(high[i][1])
                near=max(np.dot(pt(sx,0,-da),view),np.dot(pt(0,sy,-db),view))>=0
                edge=Line(self.W(*low[i]),self.W(*high[i]),color=BLUE,stroke_width=2) if near else DashedLine(self.W(*low[i]),self.W(*high[i]),color=MUTED,stroke_width=1,dash_length=.08)
                g.add(shaded(edge))
            if a0*b0>1e-8:g.add(self.ring(0))
            g.add(self.ring(H))
        else:
            rounded=k in ('sphere','hemisphere','ellipsoid')
            uend=wall_parameter(self.model,H)
            # Angular latitude sampling avoids the large polar facets of uniform z.
            wall=Surface(lambda u,t:self.W(*curved_wall_point(self.model,u,t)),
                u_range=[1e-5,uend-1e-5],v_range=[0,TAU],resolution=(32,64),
                checkerboard_colors=[BLUE,BLUE],fill_opacity=.035,stroke_width=0)
            g.add(wall)
            if rounded:g.add(self.quadric_outline())
            else:
                # Actual generator at the silhouette of an axial straight/conic wall.
                view=self.scene.camera.generate_rotation_matrix()[2];az=math.atan2(view[1],view[0])
                rho=math.hypot(view[0],view[1])
                def tangent(z,sign):
                    slope=-wall_normal(self.model,z,0)[2]
                    t=az+sign*math.acos(max(-1,min(1,slope*view[2]/rho)))
                    return self.W(*curved_wall_point(self.model,z,t))
                for sign in [-1,1]:
                    g.add(shaded(ParametricFunction(lambda z,sign=sign:tangent(z,sign),
                        t_range=[0,H,.012],color=BLUE,stroke_width=2)))
            for z in [0.,H]:
                if area(self.model,z)>1e-8:g.add(self.ring(z))
        return g
    def water_body(self,h):
        k=self.kind;model=self.model;p=self.p;g=VGroup()
        if k=='horizontal':
            R=p['R'];L=p['L'];alpha=math.acos(max(-1,min(1,(R-h)/R)))
            g.add(Surface(lambda u,v:self.W(u,R*np.sin(v),R-R*np.cos(v)),
                u_range=[-L/2,L/2],v_range=[-alpha,alpha],resolution=(3,14),
                checkerboard_colors=[CYAN,CYAN],fill_opacity=.17,stroke_width=0))
            for x in [-L/2,L/2]:
                pts=[(x,R*np.sin(t),R-R*np.cos(t)) for t in np.linspace(-alpha,alpha,30)]
                g.add(self.polygon(pts,CYAN,.17,0))
        elif k in ('box','pyramid','trough'):
            _,a0,b0=footprint(model,0);_,a1,b1=footprint(model,h)
            bottom=[(-a0,-b0,0),(a0,-b0,0),(a0,b0,0),(-a0,b0,0)]
            top=[(-a1,-b1,h),(a1,-b1,h),(a1,b1,h),(-a1,b1,h)]
            for i in range(4):
                j=(i+1)%4
                g.add(self.polygon([bottom[i],bottom[j],top[j],top[i]],CYAN,.16,0))
            if a0*b0>0:g.add(self.polygon(bottom,CYAN,.10,0))
        else:
            uend=wall_parameter(model,h)
            if uend>1e-7:
                g.add(Surface(lambda u,t:self.W(*curved_wall_point(model,u,t)),
                    u_range=[1e-6,uend],v_range=[0,TAU],resolution=(16,48),
                    checkerboard_colors=[CYAN,CYAN],fill_opacity=.13,stroke_width=0))
            if area(model,0)>1e-10:g.add(self.free_surface(0,CYAN,.08))
        return g
    def free_surface(self,h,color=CYAN,opacity=.44):
        points=surface_boundary(self.model,h,192)
        if area(self.model,h)<1e-10:return VGroup()
        return self.polygon(points,color,opacity,2.3)
    def top_view(self,h):
        shape,a,b=footprint(self.model,h)
        dims=[footprint(self.model,z)[1:] for z in np.linspace(0,self.H,81)]
        maxa=max(t[0] for t in dims);maxb=max(t[1] for t in dims)
        scale=min(1.8/(2*maxa),1.25/(2*maxb))
        if shape=='ellipse':s=Ellipse(width=2*a*scale,height=2*b*scale,color=CYAN,
                                     fill_color=CYAN,fill_opacity=.35,stroke_width=2)
        else:s=Rectangle(width=2*a*scale,height=2*b*scale,color=CYAN,fill_color=CYAN,fill_opacity=.35,stroke_width=2)
        s.move_to(pt(-5.45,-2.48))
        return VGroup(s)
    def make_hud(self,h):
        vals=[(r'h=',h,r'\mathrm m'),(r'A=',area(self.model,h),r'\mathrm{m^2}'),
              (r'h^{\prime}=',100*rise(self.model,h),r'\mathrm{cm/s}')]
        g=VGroup()
        for i,(label,value,unit) in enumerate(vals):
            row=VGroup(mtx(label,20,MUTED),DecimalNumber(value,num_decimal_places=3,font_size=20,color=GOLD),mtx(unit,18,MUTED))
            row.arrange(RIGHT,buff=.09);fit(row,2.75,.35)
            row.move_to(pt(-2.86,-1.95-.43*i));g.add(row)
        return g
    def update(self,force=False):
        h=self.level()
        if not force and self.last is not None and abs(h-self.last)<1e-8:return
        self.last=h
        self.water.become(self.water_body(h));self.surface.become(VGroup(self.free_surface(h)))
        dx=max(max(footprint(self.model,float(z))[1:]) for z in np.linspace(0,self.H,65))+.25
        bottom=self.W(dx,0,0);upper=self.W(dx,0,h)
        d=VGroup(shaded(DashedLine(bottom,upper,color=GOLD,dash_length=.08,stroke_width=1.6)),
                 shaded(Line(bottom+LEFT*.07,bottom+RIGHT*.07,color=GOLD,stroke_width=1.2)),
                 shaded(Line(upper+LEFT*.07,upper+RIGHT*.07,color=GOLD,stroke_width=1.2)))
        self.dimension.become(d)
        # Billboard glyph h follows the true world-space vertical dimension.
        self.height_label.move_to((bottom+upper)/2+pt(.15,0,0))
        # Re-register changed glyph families; newly added decimal digits must also
        # remain screen-fixed rather than being projected as world-space objects.
        self.scene.camera.remove_fixed_in_frame_mobjects(self.inset,self.hud)
        self.inset.become(self.top_view(h));self.hud.become(self.make_hud(h))
        self.scene.camera.add_fixed_in_frame_mobjects(self.inset,self.hud)
        if self.pouring:
            jet=shaded(Line(self.W(0,0,self.H+.12),self.W(0,0,h+.01),color=CYAN,stroke_width=3)).set_opacity(.65)
            self.stream.become(VGroup(jet))
        else:self.stream.become(VGroup())
    def unfreeze(self):self.world.resume_updating()
    def freeze(self):self.world.suspend_updating()
    def move_to_level(self,h,seconds=2):
        upper=self.H if area(self.model,self.H)>1e-10 else .985*self.H
        h=max(.015*self.H,min(upper,h))
        self.unfreeze()
        self.scene.play(self.clock.animate.set_value(volume(self.model,h)/self.capacity),run_time=seconds,rate_func=smooth)
        self.freeze()
    def fill(self,seconds=11):
        self.move_to_level(.08*self.H,1)
        self.time_origin=volume(self.model,self.level())
        timevalue=DecimalNumber(0,num_decimal_places=1,font_size=18,color=GOLD)
        timer=VGroup(mtx(r'\Delta t=',19,MUTED),timevalue,mtx(r'\mathrm s',19,MUTED))
        timer.arrange(RIGHT,buff=.1).move_to(pt(-3.85,2.2))
        caption=txt('Thời gian bơm thực • phát nhanh',14,MUTED).move_to(pt(-3.85,2.46))
        self.scene.add_fixed_in_frame_mobjects(timer,caption)
        def update_timer(m):
            self.scene.camera.remove_fixed_in_frame_mobjects(timer)
            timevalue.set_value((volume(self.model,self.level())-self.time_origin)/self.model['Q'])
            timer.arrange(RIGHT,buff=.1).move_to(pt(-3.85,2.2))
            self.scene.camera.add_fixed_in_frame_mobjects(timer)
        timer.add_updater(update_timer)
        self.pouring=True;self.update(force=True);self.unfreeze()
        # Linear V fraction = constant volume/time, NOT constant dh/dt.
        self.scene.play(self.clock.animate.set_value(volume(self.model,.94*self.H)/self.capacity),
                        run_time=seconds,rate_func=linear)
        self.freeze();self.pouring=False;self.update(force=True);timer.clear_updaters()
        self.scene.play(FadeOut(timer),FadeOut(caption),run_time=.4)
        self.scene.remove_fixed_in_frame_mobjects(timer,caption)
    def highlight(self):
        h=self.level();highlight=self.free_surface(h,GOLD,.55)
        self.scene.play(Transform(self.surface,VGroup(highlight)),run_time=.8)
        self.scene.wait(1.2)
        self.scene.play(Transform(self.surface,VGroup(self.free_surface(h))),run_time=.8)
    def slice(self):
        h=self.level();dh=min(.07*self.H,self.H-h)
        upper=self.free_surface(h+dh,GOLD,.28)
        lo=volume(self.model,h);hi=volume(self.model,h+dh)
        badge=mtx(r'\Delta V\approx A(h)\,\Delta h',24,GOLD).move_to(pt(-3.8,2.2))
        self.scene.add_fixed_in_frame_mobjects(badge)
        self.scene.play(FadeIn(upper),run_time=.8);self.scene.wait(2)
        self.scene.play(FadeOut(upper),FadeOut(badge),run_time=.5)
        self.scene.remove_fixed_in_frame_mobjects(badge)

class WaterLesson(ThreeDScene):
    lesson_id='INTRO'
    def construct(self):
        lesson=next(s for s in LESSONS if s['id']==self.lesson_id)
        self.events=[]
        self.set_camera_orientation(phi=66*DEGREES,theta=-50*DEGREES,focal_distance=1e9,zoom=1)
        self.camera.reset_rotation_matrix()
        title=fit(txt(lesson['title'],33,INK,True),12.8,.5).move_to(pt(0,3.5))
        subtitle=txt('TỐC ĐỘ NƯỚC DÂNG • DIỆN TÍCH MẶT THOÁNG',16,BLUE).move_to(pt(0,3.07))
        # Left border has transparent fill: fixed-in-frame opaque plates would hide 3D objects.
        left=pane(5.95,6.08,pt(-3.77,-.23),fill=0)
        right=pane(6.95,6.08,pt(2.92,-.23),fill=.98)
        footer=txt(SETTINGS['teacher'],19,MUTED).move_to(pt(0,-3.74))
        rule=Line(pt(-6.7,-3.43),pt(6.7,-3.43),color=MUTED,stroke_width=1)
        self.add_fixed_in_frame_mobjects(title,subtitle,left,right,footer,rule)
        model=TankView(self,lesson['model']);self.model=model
        self.add(model.world)
        self.add_fixed_orientation_mobjects(model.height_label)
        self.add_fixed_in_frame_mobjects(model.inset,model.hud)
        inset_label=fit(txt('MẶT THOÁNG • NHÌN TỪ TRÊN',13,CYAN,True),2.65).move_to(pt(-5.25,-1.62))
        three_label=txt('MÔ HÌNH 3D • MẶT NƯỚC NẰM NGANG',14,BLUE).move_to(pt(-3.8,2.7))
        self.add_fixed_in_frame_mobjects(inset_label,three_label)
        for page_index,page in enumerate(lesson['pages']):
            if page['action']=='practice':
                model.model['Q']=model.model['practice_Q']
                model.move_to_level(model.model['practice_h'],1)
                model.update(force=True)
            heading=fit(txt(page['title'],23,CYAN,True),6.2,.65).move_to(pt(-.19,2.5),aligned_edge=LEFT)
            counter=txt(f"{lesson['order']:02d}/{lesson['total']:02d} • Trang {page_index+1}/{len(lesson['pages'])}",14,MUTED).move_to(pt(5.5,-3.74))
            self.add_fixed_in_frame_mobjects(heading,counter)
            self.play(FadeIn(heading),run_time=.5)
            current=[];old_eq=None
            for ri,row in enumerate(page['rows']):
                y=1.58-ri*1.10
                if row['kind']=='math':
                    color=GOLD if row.get('gold') else INK
                    mob=fit(mtx(row['text'],31,color),6.15,.94)
                else:
                    wrapped=textwrap.fill(row['text'],width=42,break_long_words=False,break_on_hyphens=False)
                    mob=fit(txt(wrapped,24),6.15,.92)
                mob.move_to(pt(-.19,y),aligned_edge=LEFT)
                self.camera.add_fixed_in_frame_mobjects(mob)
                start=self.time
                self.add_sound(row['audio'])
                if row['kind']=='math' and old_eq is not None:
                    # Keep the earlier line for a detailed solution, transform its copy.
                    transient=old_eq.copy();self.add_fixed_in_frame_mobjects(transient)
                    self.play(TransformMatchingTex(transient,mob),run_time=.9)
                    self.remove_fixed_in_frame_mobjects(transient)
                else:
                    self.play(Write(mob) if row['kind']=='math' else FadeIn(mob,shift=UP*.08),run_time=.9)
                if row['kind']=='math':old_eq=mob
                current.append(mob)
                self.events.append({'start':start,'end':start+row['duration'],'text':row['voice']})
                self.wait(max(.15,row['duration']-(self.time-start))+.25)
                if row.get('gold'):self.play(Circumscribe(mob,color=GOLD,buff=.07),run_time=.8)
                if row.get('pause',0):
                    prompt=txt('Dừng video để tự giải trước khi xem đáp án',15,MUTED).move_to(pt(3,-3.04))
                    self.add_fixed_in_frame_mobjects(prompt);self.wait(row['pause'])
                    self.remove(prompt);self.remove_fixed_in_frame_mobjects(prompt)
            self.visual_action(page['action'],lesson)
            self.wait(1)
            self.play(*[FadeOut(mob) for mob in current+[heading,counter]],run_time=.5)
            self.remove_fixed_in_frame_mobjects(*current,heading,counter)
            if page['action']=='practice':
                model.model['Q']=model.normal_Q
                model.update(force=True)
        self.model.freeze();self.model.world.clear_updaters(recursive=True)
        (HERE/'events').mkdir(exist_ok=True)
        (HERE/'events'/(self.lesson_id+'.json')).write_text(json.dumps(self.events,ensure_ascii=False),encoding='utf-8')
    def visual_action(self,action,lesson):
        model=self.model;m=lesson['model'];H=m['p']['H']
        if action=='orient':model.move_to_level(m['h'],2);model.highlight()
        elif action=='highlight':model.highlight()
        elif action=='level':model.move_to_level(m['h'],1.5)
        elif action=='fill':model.fill(12)
        elif action=='slice':model.slice()
        elif action=='compare':
            for h in [.22*H,.5*H,.78*H]:model.move_to_level(h,1.5);self.wait(1)
        elif action=='practice':
            model.highlight()
            self.wait(2)

class GeometryAudit(ThreeDScene):
    model_id='B04'
    fraction=.5
    def construct(self):
        import copy
        lesson=next(s for s in LESSONS if s['id']==self.model_id)
        data=copy.deepcopy(lesson['model']);data['h']=self.fraction*data['p']['H']
        self.set_camera_orientation(phi=66*DEGREES,theta=-50*DEGREES,focal_distance=1e9,zoom=1)
        self.camera.reset_rotation_matrix()
        title=fit(txt(lesson['title']+' • Kiểm tra hình',31,INK,True),12.7,.5).move_to(pt(0,3.5))
        self.add_fixed_in_frame_mobjects(title)
        model=TankView(self,data);self.add(model.world)
        self.add_fixed_orientation_mobjects(model.height_label)
        self.add_fixed_in_frame_mobjects(model.inset,model.hud)
        note=txt('MẶT THOÁNG NẰM NGANG',17,CYAN,True).move_to(pt(-3.8,2.65))
        top=txt('NHÌN TỪ TRÊN',14,CYAN).move_to(pt(-5.4,-1.62))
        shape,a,b=footprint(data,data['h'])
        expr=r'A=\pi a_hb_h' if shape=='ellipse' else r'A=(2a_h)(2b_h)'
        lines=[mtx(r'h='+str(round(data['h'],4)),32),mtx(r'a_h='+str(round(a,4))+r',\ b_h='+str(round(b,4)),32),mtx(expr,32,GOLD)]
        if data['kind'] in ('sphere','hemisphere'):
            lines.insert(0,mtx(r'r^2=h(2R-h)',34,GOLD))
        if data['kind']=='horizontal':
            lines.insert(0,mtx(r'w=2\sqrt{h(2R-h)}',34,GOLD))
            lines[-1]=mtx(r'A=Lw',34,GOLD)
        if data['kind']=='ellipsoid':lines.insert(0,mtx(r'\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{(z-c)^2}{c^2}=1',30,GOLD))
        equations=VGroup(*lines).arrange(DOWN,buff=.5).move_to(pt(3,.5))
        for line in lines:fit(line,6.2,.85)
        self.add_fixed_in_frame_mobjects(note,top,equations)
        model.world.clear_updaters(recursive=True)
        self.wait(.1)

# LESSON_CLASSES
'''

# ========================== PIPELINE ==========================
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
    common='\n\n'.join(inspect.getsource(fn) for fn in [footprint,surface_boundary,curved_wall_point,wall_parameter,wall_normal,area,volume,height_from_volume,rise])
    classes='\n'.join(f"class C_{s['id']}(WaterLesson):\n    lesson_id={s['id']!r}\n" for s in lessons)
    return SCENE_SOURCE.replace('# MODEL_FUNCTIONS',common).replace('# LESSON_CLASSES',classes)


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
    for i,l in enumerate(lessons,1):l['order']=i;l['total']=len(lessons)
    work=root/'geometry_check';work.mkdir(parents=True,exist_ok=True)
    settings={'teacher':TEN_THAY,'width':1280,'height':720,'fps':15,'wall_resolution':64}
    (work/'lessons.json').write_text(json.dumps(lessons,ensure_ascii=False),encoding='utf-8')
    (work/'settings.json').write_text(json.dumps(settings),encoding='utf-8')
    names=[];classes=[]
    for model in MODELS:
        for tag,fraction in [('low',.25),('mid',.5),('high',.75)]:
            name='Audit_'+model['id']+'_'+tag;names.append(name)
            classes.append(f"class {name}(GeometryAudit):\n    model_id={model['id']!r}\n    fraction={fraction}\n")
    source=work/'geometry_scene.py';source.write_text(scene_code(lessons)+'\n'+'\n'.join(classes),encoding='utf-8')
    command([sys.executable,'-m','manim','--renderer','cairo','--save_last_frame','--progress_bar','none',
        '--verbosity','WARNING','-r','1280,720','--media_dir',work/'media',source,*names],work/'geometry_render.log',cwd=work)
    from PIL import Image,ImageOps,ImageDraw
    images=[]
    for name in names:
        candidates=list((work/'media').rglob(name+'*.png'))
        if not candidates:raise RuntimeError('Thiếu ảnh kiểm tra '+name)
        destination=work/(name+'.png');shutil.copy2(candidates[-1],destination);images.append(destination)
    sheet=Image.new('RGB',(1280,12*260),'#0B1120');draw=ImageDraw.Draw(sheet)
    for i,path in enumerate(images):
        thumbnail=ImageOps.contain(Image.open(path).convert('RGB'),(426,240))
        x=(i%3)*426;y=(i//3)*260;sheet.paste(thumbnail,(x,y));draw.text((x+8,y+240),path.stem,fill='white')
    sheet.save(work/'all_models_contact_sheet.png')
    print('Đã render 36 ảnh kiểm tra từ chính TankView của video:',work)


def main():
    global CHE_DO,CHON_BAI
    CHE_DO=os.environ.get('MANIM_QUALITY',CHE_DO)
    if 'MANIM_LESSONS' in os.environ:
        CHON_BAI=[x.strip() for x in os.environ['MANIM_LESSONS'].split(',') if x.strip()]
    validate_math()
    validate_geometry()
    if '--check' in sys.argv:return
    require_render_environment()
    if CHE_DO not in PRESETS:raise ValueError('CHE_DO không hợp lệ.')
    width,height,fps=PRESETS[CHE_DO]
    lessons=build_lessons();known={s['id'] for s in lessons}
    if set(CHON_BAI)-known:raise ValueError('Mã bài không tồn tại: '+str(set(CHON_BAI)-known))
    if CHON_BAI:lessons=[s for s in lessons if s['id'] in CHON_BAI]
    for i,s in enumerate(lessons,1):s['order']=i;s['total']=len(lessons)
    root=output_root('Nuoc_Dang_3D_Mat_Thoang')
    root.mkdir(exist_ok=True,parents=True);setup(root)
    if '--geometry-preview' in sys.argv:
        geometry_previews(root);return
    print('BƯỚC 2/5 — Chuẩn bị giọng nam tiếng Việt và đo thời lượng từng câu...')
    import nest_asyncio
    nest_asyncio.apply()
    spoken=asyncio.run(audio_all(lessons,root))
    settings={'teacher':TEN_THAY,'width':width,'height':height,'fps':fps,
              'voice':GIONG_DOC,'rate':TOC_DO_DOC,'wall_resolution':64}
    code=scene_code(lessons)
    digest=hashlib.sha256((code+json.dumps(settings,sort_keys=True)+json.dumps(lessons,ensure_ascii=False,sort_keys=True)).encode()).hexdigest()[:16]
    work=root/('render_'+digest);work.mkdir(exist_ok=True);(work/'events').mkdir(exist_ok=True);(work/'clips').mkdir(exist_ok=True)
    source=work/'water_scene.py';source.write_text(code,encoding='utf-8')
    (work/'lessons.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2),encoding='utf-8')
    (work/'settings.json').write_text(json.dumps(settings,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Lời giảng thuần: {spoken/60:.1f} phút; thêm hình động và khoảng tự luyện. Không ép tốc độ đọc.')
    print('BƯỚC 3/5 — Render 3D từng chương; giữ lại chương đã hoàn tất...')
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
    print('BƯỚC 4/5 — Ghép một MP4, tạo phụ đề và mục lục...')
    concat=work/'concat.txt';concat.write_text('\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in clips)+'\n',encoding='utf-8')
    metadata=[';FFMETADATA1','title=Tốc độ nước dâng - Diện tích mặt thoáng - 12 mô hình 3D','artist='+TEN_THAY]
    for start,end,title in marks:
        escaped=title.replace('\\','\\\\').replace('=','\\=').replace(';','\\;').replace('#','\\#')
        metadata+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(start*1000)}',f'END={round(end*1000)}','title='+escaped]
    meta=work/'chapters.ffmeta';meta.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
    final=root/'toc_do_nuoc_dang_3d_dien_tich_mat_thoang.mp4'
    command(['ffmpeg','-y','-v','warning','-f','concat','-safe','0','-i',concat,'-i',meta,
             '-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy',
             '-movflags','+faststart',final],work/'ffmpeg_join.log')
    final_dur=duration(final)
    info=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(final)],
                                   check=True,capture_output=True,text=True).stdout)
    assert {'video','audio'}.issubset({s['codec_type'] for s in info['streams']}),'Video thiếu hình hoặc âm thanh.'
    captions(all_events,final.with_suffix(''))
    toc=root/'toc_do_nuoc_dang_3d_muc_luc.txt'
    toc.write_text('\n'.join(timestamp(a,'.')+'  '+title for a,b,title in marks),encoding='utf-8')
    archive=root/'toc_do_nuoc_dang_3d_ma_nguon.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in [source,work/'lessons.json',work/'settings.json',toc,final.with_suffix('.srt'),final.with_suffix('.vtt')]:z.write(p,p.name)
        if '__file__' in globals() and Path(__file__).is_file():z.write(__file__,Path(__file__).name)
        z.writestr('HUONG_DAN.txt','Tải tệp .py gốc lên Colab; dùng runpy.run_path để chạy trong một ô mã ngắn.\n'
            'CHON_BAI=["B08"] để thử bồn trụ ngang. Để [] để dựng đủ.\n'
            'CHE_DO: preview, standard, final.\n'
            'Mã Scene và JSON trong ZIP ghi lại phiên render; đường audio thuộc phiên Colab đó.\n')
    print(f'BƯỚC 5/5 — HOÀN TẤT: {final_dur/60:.2f} phút, {width}×{height}, {fps} fps.')
    print('Video:',final);print('Mã nguồn:',archive)
    show_downloads(final,archive)


if __name__=='__main__':main()
