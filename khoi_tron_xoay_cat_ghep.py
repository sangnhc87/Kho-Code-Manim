# =====================================================================
# GOOGLE COLAB — DÁN TOÀN BỘ VÀO MỘT Ô RỒI CHẠY
# 12 BÀI TOÁN TỐI ƯU: KHỐI TRÒN XOAY & CẮT GHÉP HÌNH
# Giọng Nam tiếng Việt · Footer: Thầy Nguyễn Văn Sang
# =====================================================================

import os
import sys
import re
import json
import math
import time
import asyncio
import hashlib
import subprocess
import textwrap
import shutil
import zipfile
from pathlib import Path

# ======================== 1. CẤU HÌNH ================================

TEN_THAY    = "Thầy Nguyễn Văn Sang"
GIONG_DOC   = "vi-VN-NamMinhNeural"
TOC_DO_DOC  = "-5%"

# Để [] để dựng toàn bộ 12 bài.
# Thử riêng từng bài: CHON_BAI = ["B01"] hoặc ["B01","B02"]
CHON_BAI = []

CHIEU_RONG = 1280
CHIEU_CAO  = 720
FPS        = 15

HIEN_VIDEO        = True
TU_DONG_TAI_VIDEO = False

if Path("/content").exists():
    ROOT = Path("/content/Khoi_Tron_Xoay_Thay_Sang")
else:
    ROOT = (
        (Path(__file__).resolve().parent / "Khoi_Tron_Xoay_Thay_Sang")
        if "__file__" in globals()
        else (Path.cwd() / "Khoi_Tron_Xoay_Thay_Sang")
    )

ROOT.mkdir(parents=True, exist_ok=True)
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(exist_ok=True)

os.environ["DEBIAN_FRONTEND"]               = "noninteractive"
os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"


def run_log(command, logfile, cwd=None):
    logfile = Path(logfile)
    with logfile.open("w", encoding="utf-8") as f:
        result = subprocess.run(
            [str(x) for x in command],
            cwd=cwd, stdout=f, stderr=subprocess.STDOUT, text=True,
        )
    if result.returncode != 0:
        print(logfile.read_text(encoding="utf-8", errors="replace")[-18000:])
        raise RuntimeError(
            "Lenh chay that bai. Nhat ky duoc luu tai:\n" + str(logfile)
        )


def probe_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error",
         "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1",
         str(path)],
        capture_output=True, text=True, check=True,
    )
    value = float(result.stdout.strip())
    if not math.isfinite(value) or value <= 0:
        raise RuntimeError("Tep am thanh/video khong co thoi luong hop le.")
    return value


# ======================== 2. CAI DAT =================================

print("BUOC 1/5 - Cai moi truong Manim, LaTeX, FFmpeg va giong doc.")

marker = ROOT / "environment_019_v3.ok"

if Path("/content").exists() and not marker.exists():
    run_log(["apt-get", "update", "-qq"], ROOT / "apt_update.log")
    run_log(
        ["apt-get", "install", "-y", "-qq",
         "ffmpeg", "pkg-config", "python3-dev",
         "libcairo2-dev", "libpango1.0-dev",
         "texlive-latex-base", "texlive-latex-recommended",
         "texlive-latex-extra", "texlive-fonts-recommended",
         "texlive-science", "dvisvgm",
         "fonts-dejavu-core", "fonts-noto-core"],
        ROOT / "apt_install.log",
    )
    run_log(
        [sys.executable, "-m", "pip", "install", "-q",
         "manim==0.19.0", "edge-tts", "nest_asyncio"],
        ROOT / "pip_install.log",
    )
    run_log(
        [sys.executable, "-c",
         "import manim, edge_tts; print(manim.__version__)"],
        ROOT / "environment_check.log",
    )
    marker.write_text("OK", encoding="utf-8")

# ======================== 3. DU LIEU BAI GIANG =======================

def T(text, voice=None):
    return {"kind": "text", "text": text,
            "voice": voice if voice is not None else text}

def M(tex, voice):
    return {"kind": "math", "text": tex, "voice": voice}

def P(title, *rows):
    return {"title": title, "rows": list(rows)}

LESSONS = []

def Q(code, section, title, diagram, *pages):
    LESSONS.append({
        "id": code, "section": section, "title": title,
        "diagram": diagram,
        "intro": {"voice": section + ". " + title + "."},
        "pages": list(pages),
    })

# =========================================================
# BAI 1: Tru noi tiep hinh non
# =========================================================
Q(
    "B01", "BAI 1",
    "Hinh tru noi tiep hinh non ban kinh R, chieu cao H", "cylinder_cone",
    P(
        "Thiet lap bien va quan he dong dang",
        T("Hinh non co ban kinh day R va chieu cao H.",
          "Hình nón có bán kính đáy R và chiều cao H. Ta nội tiếp một hình trụ có bán kính r và chiều cao h vào trong hình nón. Tìm r và h để thể tích trụ lớn nhất."),
        M(r"0<r<R,\quad 0<h<H",
          "Gọi r là bán kính đáy trụ, h là chiều cao trụ. Cả hai đều phải dương và nhỏ hơn kích thước hình nón."),
        M(r"\frac{r}{R}=\frac{H-h}{H}\quad\Longrightarrow\quad h=H\!\left(1-\frac{r}{R}\right)",
          "Tam giác cắt dọc hình nón và hình trụ đồng dạng nhau. Do đó tỉ số r trên R bằng H trừ h trên H. Suy ra h bằng H nhân một trừ r trên R."),
    ),
    P(
        "Lap va toi uu ham the tich",
        M(r"V(r)=\pi r^2 h=\frac{\pi H}{R}\,r^2(R-r)",
          "Thể tích trụ bằng pi r bình phương nhân h. Thay h vào được V bằng pi H trên R nhân r bình phương nhân R trừ r."),
        M(r"V'(r)=\frac{\pi Hr}{R}(2R-3r)",
          "Lấy đạo hàm theo r và rút r chung được r nhân hai R trừ ba r."),
        M(r"V'=0\iff r=\frac{2R}{3},\quad h=\frac{H}{3}",
          "Đạo hàm bằng không khi r bằng hai R trên ba. Thay lại được h bằng H trên ba."),
        M(r"\boxed{V_{\max}=\frac{4\pi R^2 H}{27}}",
          "Thể tích lớn nhất bằng bốn pi R bình phương H trên hai mươi bảy. Đây là kết quả kinh điển cần ghi nhớ."),
    ),
    P(
        "Nhan xet ti le toi uu",
        M(r"r_*=\frac{2}{3}R,\quad h_*=\frac{1}{3}H",
          "Khi thể tích lớn nhất, bán kính trụ chiếm hai phần ba bán kính nón, chiều cao trụ chiếm một phần ba chiều cao nón."),
        M(r"\frac{V_{\max}}{V_{\text{non}}}=\frac{4}{9}",
          "Tỉ số thể tích trụ lớn nhất trên thể tích hình nón bằng bốn phần chín. Nghĩa là trụ chiếm bốn phần chín nón."),
    ),
)

# =========================================================
# BAI 2: Non noi tiep hinh cau
# =========================================================
Q(
    "B02", "BAI 2",
    "Hinh non noi tiep hinh cau ban kinh R", "cone_sphere",
    P(
        "Bieu dien kich thuoc theo h",
        T("Hinh cau ban kinh R; hinh non co dinh va day nam tren cau.",
          "Cho hình cầu bán kính R. Nội tiếp vào cầu một hình nón có đỉnh và đường tròn đáy nằm trên mặt cầu. Tìm kích thước nón có thể tích lớn nhất."),
        M(r"h=R+x,\quad 0<x\leq R,\quad r^2=R^2-x^2",
          "Gọi x là khoảng cách từ tâm cầu đến đáy nón. Chiều cao nón bằng R cộng x. Từ phương trình cầu, bán kính đáy bình phương bằng R bình phương trừ x bình phương."),
        M(r"V(x)=\frac{\pi}{3}(R-x)(R+x)^2",
          "Thể tích nón sau khi phân tích nhân tử."),
    ),
    P(
        "Toi uu va nghiem",
        M(r"V'(x)=\frac{\pi}{3}(R+x)(R-3x)",
          "Đạo hàm, rút nhân tử chung R cộng x và rút gọn."),
        M(r"V'=0\iff x=\frac{R}{3}",
          "Trong miền xét, R cộng x luôn dương. Đạo hàm bằng không khi x bằng R trên ba."),
        M(r"\boxed{h_*=\frac{4R}{3},\quad r_*=\frac{2\sqrt{2}\,R}{3},\quad V_{\max}=\frac{8\pi R^3}{27}}",
          "Chiều cao tối ưu bằng bốn R trên ba, bán kính đáy bằng hai căn hai nhân R trên ba, thể tích lớn nhất bằng tám pi R lập phương trên hai mươi bảy."),
    ),
    P(
        "Ti le so voi the tich cau",
        M(r"\frac{V_{\max}}{V_{\text{cau}}}=\frac{8\pi R^3/27}{4\pi R^3/3}=\frac{2}{9}",
          "Tỉ số thể tích nón lớn nhất trên thể tích cầu bằng hai phần chín."),
        T("Chieu cao toi uu gap 4/3 lan ban kinh cau.",
          "Chiều cao tối ưu gấp bốn phần ba lần bán kính cầu, vượt qua đường kính theo một phần ba bán kính."),
    ),
)

# =========================================================
# BAI 3: Tru noi tiep hinh cau - the tich lon nhat
# =========================================================
Q(
    "B03", "BAI 3",
    "Hinh tru noi tiep hinh cau ban kinh R: the tich lon nhat", "cylinder_sphere",
    P(
        "Quan he r va h qua phuong trinh cau",
        T("Tim tru noi tiep cau ban kinh R co the tich lon nhat.",
          "Cho hình cầu bán kính R. Nội tiếp vào cầu một hình trụ thẳng đứng sao cho các đường tròn hai đáy nằm trên mặt cầu. Tìm bán kính và chiều cao để thể tích trụ lớn nhất."),
        M(r"r^2+\!\left(\frac{h}{2}\right)^2=R^2\Rightarrow r^2=R^2-\frac{h^2}{4}",
          "Bán kính cầu, bán kính trụ và nửa chiều cao lập thành tam giác vuông. Suy ra r bình phương bằng R bình phương trừ h bình phương trên bốn."),
        M(r"V(h)=\pi h\!\left(R^2-\frac{h^2}{4}\right),\quad 0<h<2R",
          "Thể tích trụ bằng pi h nhân R bình phương trừ h bình phương trên bốn."),
    ),
    P(
        "Toi uu ham mot bien",
        M(r"V'(h)=\pi\!\left(R^2-\frac{3h^2}{4}\right)=0\iff h_*=\frac{2R}{\sqrt{3}}",
          "Đạo hàm bằng không khi h tối ưu bằng hai R trên căn ba."),
        M(r"r_*=R\sqrt{\frac{2}{3}}",
          "Thay h vào, bán kính tối ưu bằng R nhân căn hai phần ba."),
        M(r"\boxed{V_{\max}=\frac{4\sqrt{3}\,\pi R^3}{9}}",
          "Thể tích lớn nhất bằng bốn căn ba pi R lập phương trên chín."),
    ),
    P(
        "Kiem tra va so sanh",
        M(r"\frac{V_{\max}}{V_{\text{cau}}}=\frac{\sqrt{3}}{3}\approx57{,}7\%",
          "Trụ lớn nhất chiếm khoảng năm mươi bảy phẩy bảy phần trăm thể tích cầu."),
        T("Ti so chieu cao va duong kinh: h/2r = 1/can hai.",
          "Ở cấu hình tối ưu, chiều cao trụ chia hai lần bán kính bằng một trên căn hai."),
    ),
)

# =========================================================
# BAI 4: Cat to bia hinh vuong canh a tao hop khong nap
# =========================================================
Q(
    "B04", "BAI 4",
    "Cat to bia hinh vuong canh a tao hop chu nhat khong nap", "open_box",
    P(
        "Lap ham the tich",
        T("Cat bon goc vuong canh x, gap len tao hop khong nap.",
          "Từ tờ bìa hình vuông cạnh a, cắt bỏ bốn hình vuông nhỏ ở bốn góc, mỗi góc cạnh x. Gập bốn mặt bên lên tạo hộp hình hộp chữ nhật không nắp. Tìm x để thể tích lớn nhất."),
        M(r"0<x<\frac{a}{2},\quad l=a-2x,\quad h=x",
          "Điều kiện x dương và nhỏ hơn a trên hai để hộp có ý nghĩa. Đáy hộp là hình vuông cạnh a trừ hai x, chiều cao bằng x."),
        M(r"V(x)=x(a-2x)^2",
          "Thể tích bằng x nhân a trừ hai x bình phương."),
    ),
    P(
        "Dao ham va nghiem toi uu",
        M(r"V'(x)=(a-2x)(a-6x)",
          "Đạo hàm bằng a trừ hai x nhân a trừ sáu x. Dùng quy tắc tích và rút nhân tử."),
        M(r"V'=0\iff x=\frac{a}{6}\quad\left(\text{nghiem }x=\frac{a}{2}\text{ loai}\right)",
          "Nghiệm x bằng a trên hai loại vì hộp bẹp. Nghiệm cần lấy là x bằng a trên sáu."),
        M(r"\boxed{x_*=\frac{a}{6},\quad V_{\max}=\frac{2a^3}{27}}",
          "Cắt cạnh x bằng a trên sáu. Thể tích lớn nhất bằng hai a lập phương trên hai mươi bảy."),
    ),
    P(
        "Nhan xet quan trong",
        T("Dao ham duong truoc a/6, am sau: cuc dai.",
          "Đạo hàm dương khi x nhỏ hơn a trên sáu và âm sau, xác nhận cực đại."),
        M(r"h_*=\frac{a}{6}=\frac{l_*}{4}",
          "Chiều cao hộp tối ưu bằng một phần tư cạnh đáy. Đây là dấu hiệu nhận biết cấu hình tối ưu."),
        M(r"\frac{V_{\max}}{a^3}=\frac{2}{27}\approx7{,}4\%",
          "Thể tích hộp lớn nhất chiếm khoảng bảy phẩy bốn phần trăm thể tích khối lập phương cạnh a."),
    ),
)

# =========================================================
# BAI 5: Tru noi tiep cau - dien tich xung quanh lon nhat
# =========================================================
Q(
    "B05", "BAI 5",
    "Hinh tru noi tiep cau R: dien tich xung quanh lon nhat", "lateral_cylinder_sphere",
    P(
        "Lap ham dien tich xung quanh",
        T("Tim tru noi tiep cau R co dien tich xung quanh lon nhat.",
          "Cho hình cầu bán kính R. Tìm hình trụ nội tiếp cầu sao cho diện tích xung quanh lớn nhất."),
        M(r"r^2+\frac{h^2}{4}=R^2\Rightarrow r=\sqrt{R^2-\frac{h^2}{4}}",
          "Ràng buộc hình học từ bài ba: r bình phương cộng h bình phương trên bốn bằng R bình phương."),
        M(r"S(h)=2\pi rh=2\pi h\sqrt{R^2-\frac{h^2}{4}},\quad 0<h<2R",
          "Diện tích xung quanh bằng hai pi r h, thay r vào được hàm một biến theo h."),
    ),
    P(
        "Toi uu bang binh phuong",
        M(r"[S(h)]^2=\pi^2\!\left(4R^2 h^2-h^4\right)",
          "Bình phương diện tích để tránh căn thức. Tối đa S tương đương tối đa bình phương S."),
        M(r"\frac{d}{dh}[S^2]=4\pi^2 h(2R^2-h^2)=0\Rightarrow h_*=R\sqrt{2}",
          "Đạo hàm bình phương bằng không cho h tối ưu bằng R căn hai."),
        M(r"r_*=\frac{R}{\sqrt{2}},\qquad\boxed{S_{\max}=2\pi R^2}",
          "Bán kính tối ưu bằng R trên căn hai. Diện tích xung quanh lớn nhất bằng hai pi R bình phương."),
    ),
    P(
        "So sanh voi dien tich cau",
        M(r"\frac{S_{\max}}{S_{\text{cau}}}=\frac{2\pi R^2}{4\pi R^2}=\frac{1}{2}",
          "Diện tích xung quanh trụ lớn nhất bằng một nửa diện tích mặt cầu."),
        T("Ti le toi uu: h = can hai nhan R, r = R chia can hai.",
          "Ở cấu hình tối ưu, chiều cao bằng căn hai lần bán kính cầu và bán kính trụ bằng bán kính cầu chia căn hai."),
    ),
)

# =========================================================
# BAI 6: Non co dien tich xung quanh nho nhat, the tich cho truoc
# =========================================================
Q(
    "B06", "BAI 6",
    "Hinh non the tich V0 co dien tich xung quanh nho nhat", "cone_min_lateral",
    P(
        "Lap rang buoc va ham can toi uu",
        T("Cho hinh non co the tich co dinh V0. Tim non co dien tich xung quanh nho nhat.",
          "Bài toán: cho thể tích hình nón bằng V không đổi. Tìm bán kính r và chiều cao h để diện tích xung quanh nhỏ nhất."),
        M(r"V=\frac{\pi}{3}r^2 h=V_0\Rightarrow h=\frac{3V_0}{\pi r^2}",
          "Ràng buộc thể tích cho h bằng ba V không trên pi r bình phương."),
        M(r"S_{xq}=\pi r l=\pi r\sqrt{r^2+h^2}",
          "Đường sinh bằng căn r bình phương cộng h bình phương. Diện tích xung quanh bằng pi r l."),
    ),
    P(
        "Toi uu theo r",
        M(r"[S_{xq}]^2=\pi^2 r^4+\frac{9V_0^2}{r^2}",
          "Bình phương để tối ưu dễ hơn, bỏ hằng số."),
        M(r"\frac{d}{dr}[S^2]=4\pi^2 r^3-\frac{18V_0^2}{r^3}=0",
          "Cho đạo hàm bằng không, giải ra r lập phương sáu."),
        M(r"\boxed{h=r\sqrt{2}\Longleftrightarrow\frac{h}{r}=\sqrt{2}}",
          "Điều kiện tối ưu đơn giản và đẹp: chiều cao bằng bán kính nhân căn hai. Tỉ lệ h trên r bằng căn hai."),
    ),
    P(
        "Ket luan hinh hoc",
        T("Goc ban dinh toi uu: arctan(can hai) xap xi 54,74 do.",
          "Góc giữa đường sinh và trục bằng a rctang căn hai, xấp xỉ năm mươi bốn phẩy bảy mươi bốn độ."),
        M(r"l_*=\sqrt{3}\,r_*",
          "Đường sinh bằng căn ba lần bán kính ở cấu hình tối ưu."),
        T("Ket qua nay dung cho moi V0 > 0.",
          "Đây là tỉ lệ tối ưu, không phụ thuộc vào giá trị cụ thể của V không."),
    ),
)

# =========================================================
# BAI 7: Non ngoai tiep hinh cau - the tich nho nhat
# =========================================================
Q(
    "B07", "BAI 7",
    "Hinh non ngoai tiep hinh cau ban kinh r0: the tich nho nhat", "cone_circumscribe_sphere",
    P(
        "Rang buoc tu quan he tiep xuc",
        T("Hinh cau ban kinh r0 noi tiep hinh non. Tim non co the tich nho nhat.",
          "Cho hình cầu bán kính r không đổi. Bài toán: tìm hình nón ngoại tiếp hình cầu có thể tích nhỏ nhất."),
        M(r"r_0=\frac{Rh}{\sqrt{R^2+h^2}+R}\quad\text{(quan he tiep xuc)}",
          "Từ điều kiện cầu nội tiếp nón tiếp xúc mặt bên, bán kính cầu bằng R h chia căn R bình phương cộng h bình phương cộng R."),
        M(r"\text{Dat }t=\frac{h}{R}\Rightarrow V(t)=\frac{\pi r_0^3}{3}\cdot\frac{(\sqrt{t^2+1}+1)^3}{t^2}",
          "Đặt t bằng h trên R. Sau khi thay R vào V, thể tích là hàm của t với r không cố định."),
    ),
    P(
        "Tim nghiem toi uu",
        M(r"V'(t)=0\Rightarrow t=2\Rightarrow h=2R",
          "Giải đạo hàm bằng không, nghiệm là t bằng hai, tức h bằng hai R."),
        M(r"\boxed{h_*=4r_0,\quad R_*=2\sqrt{3}\,r_0,\quad V_{\min}=\frac{8\pi r_0^3}{3}}",
          "Chiều cao tối ưu bằng bốn r không, bán kính bằng hai căn ba r không, thể tích nhỏ nhất bằng tám pi r không lập phương trên ba."),
    ),
    P(
        "Ti le quan trong",
        M(r"\frac{V_{\min}}{V_{\text{cau}}}=\frac{8\pi r_0^3/3}{4\pi r_0^3/3}=2",
          "Thể tích nón nhỏ nhất ngoại tiếp cầu bằng đúng hai lần thể tích cầu. Đây là kết quả rất đẹp."),
        T("Goc ban dinh toi uu: arctan(1/2) xap xi 26,57 do.",
          "Góc bán đỉnh bằng a rctang một phần hai, xấp xỉ hai mươi sáu phẩy năm bảy độ."),
    ),
)

# =========================================================
# BAI 8: Tru noi tiep cau - tong dien tich mat lon nhat
# =========================================================
Q(
    "B08", "BAI 8",
    "Hinh tru noi tiep cau R: tong dien tich mat lon nhat", "total_cylinder_sphere",
    P(
        "Lap ham tong dien tich",
        T("Tim tru noi tiep cau R co tong dien tich mat lon nhat.",
          "Từ hình cầu bán kính R, tìm hình trụ nội tiếp có tổng diện tích toàn phần gồm hai đáy và xung quanh lớn nhất."),
        M(r"r^2+\frac{h^2}{4}=R^2,\quad h=2\sqrt{R^2-r^2}",
          "Ràng buộc hình học và biểu thức chiều cao theo r."),
        M(r"S(r)=2\pi r^2+4\pi r\sqrt{R^2-r^2},\quad 0<r<R",
          "Thay h vào tổng diện tích được hàm một biến theo r."),
    ),
    P(
        "Dao ham va nghiem",
        M(r"S'(r)=4\pi r+4\pi\!\left(\sqrt{R^2-r^2}-\frac{r^2}{\sqrt{R^2-r^2}}\right)=0",
          "Đạo hàm bằng tổng đạo hàm của hai hạng tử. Cho bằng không."),
        M(r"r_*=\frac{R}{\sqrt{2}},\quad h_*=R\sqrt{2}",
          "Nghiệm tối ưu r bằng R trên căn hai và h bằng R căn hai."),
        M(r"\boxed{S_{\max}=2\pi R^2(1+\sqrt{2})}",
          "Tổng diện tích lớn nhất bằng hai pi R bình phương nhân một cộng căn hai."),
    ),
    P(
        "Kiem tra",
        M(r"\frac{S_{\max}}{S_{\text{cau}}}=\frac{2\pi R^2(1+\sqrt{2})}{4\pi R^2}=\frac{1+\sqrt{2}}{2}\approx120{,}7\%",
          "Tổng diện tích mặt trụ lớn nhất vượt cả diện tích mặt cầu, đạt khoảng một trăm hai mươi phẩy bảy phần trăm."),
        T("Cau hinh toi uu nay trung voi bai dien tich xung quanh.",
          "Thú vị là cấu hình tối ưu của bài tám trùng với cấu hình tối ưu của bài năm."),
    ),
)

# =========================================================
# BAI 9: Lang tru tam giac deu noi tiep hinh non
# =========================================================
Q(
    "B09", "BAI 9",
    "Lang tru tam giac deu noi tiep hinh non R, H", "prism_cone",
    P(
        "Ban kinh day theo canh tam giac deu",
        T("Noi tiep lang tru tam giac deu vao hinh non ban kinh R chieu cao H.",
          "Cho hình nón bán kính R và chiều cao H. Nội tiếp vào hình nón một lăng trụ đứng đáy tam giác đều sao cho đáy dưới nội tiếp đáy nón và đỉnh đáy trên nằm trên mặt bên nón. Tìm cạnh tam giác đều để thể tích lớn nhất."),
        M(r"a\text{ la canh tam giac deu},\quad R_{\triangle}=\frac{a}{\sqrt{3}}",
          "Bán kính đường tròn ngoại tiếp tam giác đều cạnh a bằng a trên căn ba."),
        M(r"\frac{R_\triangle}{R}=\frac{H-h_{lp}}{H}\Rightarrow h_{lp}=H\!\left(1-\frac{a}{R\sqrt{3}}\right)",
          "Đồng dạng cho chiều cao lăng trụ theo a."),
    ),
    P(
        "Toi uu the tich lang tru",
        M(r"V(a)=\frac{\sqrt{3}}{4}a^2\cdot H\!\left(1-\frac{a}{R\sqrt{3}}\right)",
          "Thể tích lăng trụ bằng diện tích đáy nhân chiều cao."),
        M(r"V'(a)=\frac{\sqrt{3}Ha}{4}\!\left(2-\frac{3a}{R\sqrt{3}}\right)=0",
          "Đạo hàm bằng không khi hai trừ ba a trên R căn ba bằng không."),
        M(r"a_*=\frac{2R}{\sqrt{3}}=\frac{2\sqrt{3}}{3}R",
          "Cạnh tối ưu bằng hai R trên căn ba."),
        M(r"\boxed{V_{\max}=\frac{H R^2}{3\sqrt{3}}=\frac{\sqrt{3}\,HR^2}{9}}",
          "Thể tích lớn nhất bằng căn ba nhân H R bình phương trên chín."),
    ),
    P(
        "Chieu cao lang tru toi uu",
        M(r"h_{lp,*}=H\!\left(1-\frac{a_*}{R\sqrt{3}}\right)=\frac{H}{3}",
          "Chiều cao lăng trụ tối ưu bằng một phần ba chiều cao nón. Giống hệt bài một!"),
        T("Tat ca cac khoi noi tiep non toi uu deu co chieu cao bang H/3.",
          "Đây là tính chất chung: mọi khối nội tiếp hình nón đạt thể tích lớn nhất đều có chiều cao bằng một phần ba chiều cao nón."),
    ),
)

# =========================================================
# BAI 10: Tam kim loai hinh quat cuon thanh non - the tich lon nhat
# =========================================================
Q(
    "B10", "BAI 10",
    "Tam kim loai hinh quat ban kinh L cuon thanh hinh non: the tich lon nhat", "sector_cone",
    P(
        "Tu hinh quat den hinh non",
        T("Tam kim loai hinh quat ban kinh L, goc alpha. Cuon thanh hinh non.",
          "Cho tấm kim loại hình quạt bán kính L và góc ở tâm an pha, đơn vị radian. Cuộn tấm lại thành hình nón. Tìm an pha để thể tích hình nón lớn nhất."),
        M(r"l=L\text{ (duong sinh)},\quad r=\frac{L\alpha}{2\pi}",
          "Bán kính đáy nón bằng cung hình quạt chia hai pi, tức L an pha trên hai pi."),
        M(r"h=\sqrt{L^2-r^2}=L\sqrt{1-\frac{\alpha^2}{4\pi^2}}",
          "Chiều cao nón từ định lý Pythagoras."),
        M(r"V(\alpha)=\frac{L^3}{12\pi}\alpha^2\sqrt{4\pi^2-\alpha^2}",
          "Thể tích nón theo an pha."),
    ),
    P(
        "Toi uu theo alpha",
        M(r"[V(\alpha)]^2\propto\alpha^4(4\pi^2-\alpha^2)",
          "Tối đa V tương đương tối đa bình phương V. Cần tối đa f bằng an pha mũ bốn nhân bốn pi bình phương trừ an pha bình phương."),
        M(r"f'(\alpha)=2\alpha^3(8\pi^2-3\alpha^2)=0\Rightarrow\alpha^2=\frac{8\pi^2}{3}",
          "Cho đạo hàm bằng không, nghiệm là an pha bình phương bằng tám pi bình phương trên ba."),
        M(r"\alpha_*=\frac{2\pi\sqrt{6}}{3}\approx290{,}9°",
          "Góc tối ưu khoảng hai trăm chín mươi mốt độ."),
        M(r"\boxed{V_{\max}=\frac{2\sqrt{3}\,\pi L^3}{27},\quad r_*=\frac{\sqrt{6}}{3}L,\quad h_*=\frac{\sqrt{3}}{3}L}",
          "Thể tích lớn nhất bằng hai căn ba pi L lập phương trên hai mươi bảy. Bán kính đáy bằng L căn sáu trên ba, chiều cao bằng L căn ba trên ba."),
    ),
    P(
        "Kiem tra ti le",
        M(r"\frac{h_*}{r_*}=\frac{L\sqrt{3}/3}{L\sqrt{6}/3}=\frac{1}{\sqrt{2}}=\frac{\sqrt{2}}{2}",
          "Tỉ lệ chiều cao trên bán kính đáy bằng một trên căn hai, trùng với bài sáu về nón thể tích nhỏ nhất diện tích xung quanh cố định."),
        T("Phat hien: non cuon tu hinh quat toi uu cung thoa man h/r = 1/can hai.",
          "Đây là điều bất ngờ: cấu hình nón tối ưu từ hình quạt thỏa mãn tỉ lệ h trên r bằng một trên căn hai, giống bài sáu."),
    ),
)

# =========================================================
# BAI 11: Hinh vuong noi tiep tam giac deu
# =========================================================
Q(
    "B11", "BAI 11",
    "Hinh vuong noi tiep tam giac deu canh a: dien tich lon nhat", "square_equilateral",
    P(
        "Bieu dien canh vuong theo vi tri",
        T("Tam giac deu canh a. Hinh vuong co mot canh nam tren day tam giac.",
          "Cho tam giác đều cạnh a. Nội tiếp vào tam giác một hình vuông sao cho một cạnh nằm trên đáy. Tìm cạnh hình vuông."),
        M(r"h_{\triangle}=\frac{\sqrt{3}}{2}a,\quad x\text{ la canh hinh vuong}",
          "Chiều cao tam giác đều bằng căn ba trên hai nhân a. Gọi x là cạnh hình vuông."),
        M(r"\frac{a'}{a}=\frac{h_\triangle-x}{h_\triangle}\Rightarrow a'=a\!\left(1-\frac{2x}{\sqrt{3}a}\right)",
          "Tam giác phía trên hình vuông đồng dạng với tam giác ban đầu. Cạnh đáy tam giác nhỏ là a nhân một trừ hai x trên căn ba a."),
        M(r"a'=x\quad\text{(hai dinh tren cua vuong nam tren hai canh ben)}",
          "Hai đỉnh trên của vuông nằm trên hai cạnh bên, nên chiều rộng tam giác nhỏ bằng x."),
    ),
    P(
        "Giai ra canh vuong",
        M(r"x=a\!\left(1-\frac{2x}{\sqrt{3}a}\right)\Rightarrow x\!\left(1+\frac{2}{\sqrt{3}}\right)=a",
          "Giải phương trình tuyến tính theo x."),
        M(r"\boxed{x_*=\frac{a\sqrt{3}}{2+\sqrt{3}}=a(2\sqrt{3}-3)}",
          "Cạnh hình vuông bằng a nhân hai căn ba trừ ba. Đây là kết quả chính xác."),
        M(r"x_*\approx0{,}464\,a",
          "Giá trị số xấp xỉ không phẩy bốn sáu bốn lần cạnh tam giác."),
    ),
    P(
        "So sanh dien tich",
        M(r"S_{\text{vuong}}=x_*^2=a^2(21-12\sqrt{3})\approx0{,}215\,a^2",
          "Diện tích hình vuông bằng a bình phương nhân hai mươi mốt trừ mười hai căn ba, khoảng không phẩy hai một lăm a bình phương."),
        M(r"S_{\triangle}=\frac{\sqrt{3}}{4}a^2\approx0{,}433\,a^2",
          "Diện tích tam giác đều."),
        M(r"\frac{S_{\text{vuong}}}{S_{\triangle}}\approx49{,}7\%",
          "Hình vuông nội tiếp chiếm khoảng bốn mươi chín phẩy bảy phần trăm diện tích tam giác đều."),
    ),
)

# =========================================================
# BAI 12: Non noi tiep tru - dien tich xung quanh nho nhat
# =========================================================
Q(
    "B12", "BAI 12",
    "Hinh non noi tiep hinh tru R,H: dien tich xung quanh nho nhat", "cone_in_cylinder",
    P(
        "Rang buoc hinh hoc",
        T("Noi tiep hinh non vao hinh tru co ban kinh R va chieu cao H. Tim non co dien tich xung quanh nho nhat.",
          "Cho hình trụ bán kính R và chiều cao H cố định. Nội tiếp một hình nón vào trụ sao cho đáy nón nằm trên đáy trụ, đỉnh nón trên mặt nắp trụ và tất cả đường tròn đáy nón tiếp xúc mặt bên trụ. Tìm nón có diện tích xung quanh nhỏ nhất."),
        M(r"r=R,\quad 0<h\leq H,\quad l=\sqrt{R^2+h^2}",
          "Vì đường tròn đáy tiếp xúc mặt bên trụ, bán kính nón bằng R. Đường sinh bằng căn R bình phương cộng h bình phương."),
        M(r"S_{xq}=\pi R\sqrt{R^2+h^2}",
          "Diện tích xung quanh hình nón bằng pi R nhân căn R bình phương cộng h bình phương."),
    ),
    P(
        "Phan tich bai toan",
        T("Ham S tang theo h: cuc tieu tai h nho nhat.",
          "Hàm diện tích xung quanh tăng theo h vì căn thức tăng. Để nhỏ nhất, chọn h nhỏ nhất có thể."),
        T("Neu khong co rang buoc them: h tien ve 0, non suy bien.",
          "Nếu không có ràng buộc thêm, khi h tiến về không thì nón suy biến thành đĩa phẳng và diện tích xung quanh tiến về không."),
        M(r"\text{Voi rang buoc }h=H:\quad S_{xq}=\pi R\sqrt{R^2+H^2}",
          "Với ràng buộc h bằng H, nón chiếm đầy hình trụ. Diện tích xung quanh bằng pi R căn R bình phương cộng H bình phương."),
    ),
    P(
        "Bai toan phu hop hon: tim non V cho truoc, S xq nho nhat",
        T("Khi the tich no co dinh V0, khong rang buoc r = R, bai toan co nghiem dep.",
          "Khi không ràng buộc bán kính và chiều cao mà chỉ cố định thể tích V không, điều kiện tối ưu là h trên r bằng căn hai."),
        M(r"\frac{h}{r}=\sqrt{2}\Rightarrow l=r\sqrt{3}",
          "Đây là kết quả đã chứng minh ở bài sáu: tỉ số chiều cao trên bán kính bằng căn hai, và đường sinh bằng căn ba lần bán kính."),
        M(r"\boxed{\text{Goc ban dinh }=\arctan\!\left(\frac{1}{\sqrt{2}}\right)\approx35{,}26°}",
          "Góc bán đỉnh của nón tối ưu bằng a rctang một trên căn hai, xấp xỉ ba mươi lăm phẩy hai sáu độ."),
    ),
)

# ======================== 4. CHON BAI ================================

selected = [les for les in LESSONS if not CHON_BAI or les["id"] in CHON_BAI]

if not selected:
    raise RuntimeError(
        "Khong tim thay bai nao khop CHON_BAI = " + str(CHON_BAI)
        + ". Cac ma hop le: " + str([les["id"] for les in LESSONS])
    )

for order, les in enumerate(selected, 1):
    les["order"] = order
    les["total"] = len(selected)

# ======================== 5. TAO GIONG DOC ===========================

print("\nBUOC 2/5 - Tao giong nam va can thoi luong.")

try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

import edge_tts


async def make_audio(text, path):
    communicate = edge_tts.Communicate(text, GIONG_DOC, rate=TOC_DO_DOC)
    await communicate.save(str(path))


def get_or_create_audio(text, tag):
    key = hashlib.md5(
        (GIONG_DOC + TOC_DO_DOC + text).encode("utf-8")
    ).hexdigest()
    mp3_path = AUDIO_DIR / (key + ".mp3")
    if not mp3_path.exists():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(make_audio(text, mp3_path))
    return mp3_path


total_items = 0
for les in selected:
    total_items += 1
    for page in les["pages"]:
        total_items += len(page["rows"])

done_count = 0

for les in selected:
    intro = les["intro"]
    mp3 = get_or_create_audio(intro["voice"], les["id"] + "_intro")
    intro["audio"]    = str(mp3)
    intro["duration"] = probe_duration(mp3)
    done_count += 1

    for pi_, page in enumerate(les["pages"]):
        for ri_, row in enumerate(page["rows"]):
            mp3 = get_or_create_audio(row["voice"],
                                      f"{les['id']}_p{pi_}_r{ri_}")
            row["audio"]    = str(mp3)
            row["duration"] = probe_duration(mp3)
            done_count += 1

        if done_count % 20 == 0 or done_count == total_items:
            print(f"  Da chuan bi {done_count} / {total_items} doan loi doc.")

print(f"  Da chuan bi du {total_items} doan loi doc.")

# ======================== 5b. MA SCENE MANIM ==========================

SCENE_SOURCE = r'''
from manim import *
from pathlib import Path
import json
import math
import textwrap
import numpy as np

HERE = Path(__file__).resolve().parent

with open(HERE / "settings.json", encoding="utf-8") as _f:
    SETTINGS = json.load(_f)

with open(HERE / "lessons.json", encoding="utf-8") as _f:
    DATA = json.load(_f)

BG    = "#0B1220"
PANEL = "#0F1E35"
INK   = "#EDF4FF"
MUTED = "#8AA3BF"
BLUE  = "#4DA6FF"
CYAN  = "#3ADEC8"
GOLD  = "#FFD166"
GREEN = "#4ADE80"
RED   = "#FF6B6B"

config.background_color = BG
config.pixel_width  = SETTINGS["width"]
config.pixel_height = SETTINGS["height"]
config.frame_rate   = SETTINGS["fps"]

FONT = "DejaVu Sans"

TEMPLATE = TexTemplate()
TEMPLATE.add_to_preamble(
    r"\usepackage{amsmath}"
    r"\usepackage{amssymb}"
    r"\usepackage{xcolor}"
)


def text_mob(s, size=26, color=INK, bold=False):
    return Text(s, font=FONT, font_size=size, color=color,
                weight="BOLD" if bold else "NORMAL",
                disable_ligatures=True, line_spacing=0.8)


def math_mob(s, size=30, color=INK):
    return MathTex(s, font_size=size, color=color, tex_template=TEMPLATE)


def fit(mob, width=None, height=None):
    factors = [1.0]
    if width  is not None and mob.width  > 0: factors.append(width  / mob.width)
    if height is not None and mob.height > 0: factors.append(height / mob.height)
    mob.scale(min(factors))
    return mob


def pt(x, y): return np.array([float(x), float(y), 0.0])
def lbl(s, x, y, size=23, color=INK):
    return math_mob(s, size, color).move_to(pt(x, y))
def seg(a, b, color=BLUE, width=3, dashed=False):
    cls = DashedLine if dashed else Line
    return cls(pt(*a), pt(*b), color=color, stroke_width=width)
def poly(points, color=BLUE, opacity=0.16):
    return Polygon(*[pt(*p) for p in points], color=color,
                   stroke_width=3, fill_color=color, fill_opacity=opacity)


def make_diagram(kind, t=0):
    g = VGroup()

    if kind == "cylinder_cone":
        R, H = 2.2, 3.2
        r_draw = (0.55 + (2/3 - 0.55) * t) * R
        h_draw = H * (1 - r_draw / R)
        g.add(
            poly([(-R, -H/2), (R, -H/2), (0, H/2)], BLUE, 0.08),
            poly([(-r_draw, -H/2), (r_draw, -H/2),
                  (r_draw, -H/2+h_draw), (-r_draw, -H/2+h_draw)], GREEN, 0.28),
            seg((-R, -H/2), (R, -H/2), MUTED, 1.5),
            seg((0, -H/2), (0, H/2), MUTED, 1.5, True),
            lbl("R", R+0.3, -H/2, 22, GOLD),
            lbl("H", 0.3, 0, 22, GOLD),
            lbl("r", r_draw/2, -H/2+h_draw+0.32, 22, GREEN),
            lbl("h", r_draw+0.28, -H/2+h_draw/2, 22, GREEN),
        )

    elif kind == "cone_sphere":
        R = 2.0
        x_draw = (0.18 + (1/3 - 0.18) * t) * R
        r2 = max(R**2 - x_draw**2, 0.01)
        r_draw = math.sqrt(r2)
        h_draw = R + x_draw
        scale = 2.6 / h_draw
        rs, hs = r_draw * scale, h_draw * scale
        cy = -hs/2 + x_draw * scale
        g.add(
            Circle(radius=R*scale, color=BLUE,
                   stroke_width=2, fill_opacity=0.07, fill_color=BLUE
                   ).move_to(pt(0, cy)),
            poly([(-rs, -hs/2), (rs, -hs/2), (0, hs/2)], GREEN, 0.22),
            seg((0, -hs/2), (0, hs/2), MUTED, 1.5, True),
            Dot(pt(0, cy), radius=0.07, color=GOLD),
            lbl("R", R*scale*0.55, cy+0.25, 22, BLUE),
            lbl("h", 0.32, 0, 22, GREEN),
            lbl("r", rs/2, -hs/2-0.38, 22, GREEN),
        )

    elif kind == "cylinder_sphere":
        R = 2.2
        h_draw = (1.1 + (R*math.sqrt(2) - 1.1) * t) * 0.85
        r2 = max(R**2 - (h_draw/2)**2, 0.01)
        r_draw = math.sqrt(r2)
        g.add(
            Circle(radius=R, color=BLUE,
                   stroke_width=2, fill_opacity=0.07, fill_color=BLUE),
            poly([(-r_draw, -h_draw/2), (r_draw, -h_draw/2),
                  (r_draw,  h_draw/2), (-r_draw,  h_draw/2)], GREEN, 0.26),
            seg((0, 0), (r_draw, h_draw/2), GOLD, 2.5, True),
            lbl("R", r_draw*0.5+0.1, h_draw/4+0.18, 22, GOLD),
            lbl("r", r_draw/2, -h_draw/2-0.38, 22, GREEN),
            lbl("h", r_draw+0.32, 0, 22, GREEN),
        )

    elif kind == "open_box":
        a = 3.4
        x_draw = max(0.28 + (a/6 - 0.28) * t, 0.15)
        side = a - 2*x_draw
        g.add(
            poly([(-a/2, -a/2), (a/2, -a/2), (a/2, a/2), (-a/2, a/2)], MUTED, 0.06),
            poly([(-side/2, -side/2), (side/2, -side/2),
                  (side/2,  side/2), (-side/2,  side/2)], GREEN, 0.25),
            poly([(-a/2,-a/2),(-side/2,-a/2),(-side/2,-side/2),(-a/2,-side/2)], RED, 0.45),
            poly([( a/2,-a/2),( side/2,-a/2),( side/2,-side/2),( a/2,-side/2)], RED, 0.45),
            poly([(-a/2, a/2),(-side/2, a/2),(-side/2, side/2),(-a/2, side/2)], RED, 0.45),
            poly([( a/2, a/2),( side/2, a/2),( side/2, side/2),( a/2, side/2)], RED, 0.45),
            lbl("a", 0, -a/2-0.42, 22, GOLD),
            lbl("x", -a/2-0.32, -a/2+x_draw/2, 22, RED),
        )

    elif kind == "lateral_cylinder_sphere":
        R = 2.2
        h_draw = (0.9 + (R*math.sqrt(2) - 0.9) * t) * 0.82
        r2 = max(R**2 - (h_draw/2)**2, 0.01)
        r_draw = math.sqrt(r2)
        g.add(
            Circle(radius=R, color=BLUE,
                   stroke_width=2, fill_opacity=0.07, fill_color=BLUE),
            poly([(-r_draw, -h_draw/2), (r_draw, -h_draw/2),
                  (r_draw,  h_draw/2), (-r_draw,  h_draw/2)], CYAN, 0.22),
            lbl("S_{xq}", 0, 0, 26, CYAN),
            lbl("R", R*0.6, h_draw/4+0.1, 22, GOLD),
        )

    elif kind == "cone_min_lateral":
        h_over_r = 0.6 + (math.sqrt(2) - 0.6) * t
        r_c = 1.6
        h_c = r_c * h_over_r
        l_c = math.sqrt(r_c**2 + h_c**2)
        sc = 2.5 / l_c
        rs, hs = r_c*sc, h_c*sc
        g.add(
            poly([(-rs, -hs/2), (rs, -hs/2), (0, hs/2)], GREEN, 0.22),
            seg((0, -hs/2), (0, hs/2), MUTED, 1.5, True),
            seg((0, hs/2), (rs, -hs/2), GOLD, 3),
            lbl("l", rs/2+0.22, 0.12, 22, GOLD),
            lbl("r", rs/2, -hs/2-0.38, 22, GREEN),
            lbl("h", 0.32, 0, 22, GREEN),
        )

    elif kind == "cone_circumscribe_sphere":
        r0 = 0.85
        t_val = 0.45 + 1.55 * t   # goes toward t=2 means h/R=2
        R_c = r0 * (math.sqrt(t_val**2+1)+1) / t_val
        h_c = R_c * t_val
        sc = 2.6 / h_c
        rs, hs = R_c*sc, h_c*sc
        cy = -hs/2 + r0*sc
        g.add(
            poly([(-rs, -hs/2), (rs, -hs/2), (0, hs/2)], GREEN, 0.16),
            Circle(radius=r0*sc, color=BLUE,
                   stroke_width=2, fill_opacity=0.14, fill_color=BLUE
                   ).move_to(pt(0, cy)),
            seg((0, -hs/2), (0, hs/2), MUTED, 1.5, True),
            lbl("r_0", r0*sc+0.4, cy, 22, BLUE),
            lbl("R", rs/2, -hs/2-0.38, 22, GREEN),
            lbl("h", 0.32, 0, 22, GREEN),
        )

    elif kind == "total_cylinder_sphere":
        R = 2.2
        h_draw = (0.95 + (R*math.sqrt(2) - 0.95) * t) * 0.82
        r2 = max(R**2 - (h_draw/2)**2, 0.01)
        r_draw = math.sqrt(r2)
        g.add(
            Circle(radius=R, color=BLUE,
                   stroke_width=2, fill_opacity=0.07, fill_color=BLUE),
            poly([(-r_draw, -h_draw/2), (r_draw, -h_draw/2),
                  (r_draw,  h_draw/2), (-r_draw,  h_draw/2)], GREEN, 0.25),
            seg((-r_draw,  h_draw/2), (r_draw,  h_draw/2), CYAN, 5),
            seg((-r_draw, -h_draw/2), (r_draw, -h_draw/2), CYAN, 5),
            lbl("S_{tp}", 0, 0, 26, CYAN),
        )

    elif kind == "prism_cone":
        R = 2.0
        a_opt = 2*R/math.sqrt(3)
        a_draw = (0.75 + (a_opt/R - 0.75) * t) * R
        Rt = a_draw / math.sqrt(3)
        sc = 1.55 / R
        Rs, Rts = R*sc, Rt*sc
        angles = [math.pi/2 + 2*math.pi*k/3 for k in range(3)]
        pts_in = [(Rts*math.cos(a), Rts*math.sin(a)) for a in angles]
        g.add(
            Circle(radius=Rs, color=BLUE,
                   stroke_width=2, fill_opacity=0.07, fill_color=BLUE),
            poly(pts_in, GREEN, 0.28),
            lbl("R", Rs*0.55, Rs*0.38, 21, BLUE),
            lbl("a", Rts*0.55+0.1, -Rts*0.65, 21, GREEN),
        )

    elif kind == "sector_cone":
        L = 2.5
        alpha_opt = 2*math.pi*math.sqrt(2/3)
        alpha_draw = 1.4 + (alpha_opt - 1.4) * t
        alpha_draw = min(alpha_draw, 2*math.pi*0.98)
        arc_pts = [(L*0.9*math.cos(u), L*0.9*math.sin(u))
                   for u in np.linspace(0, alpha_draw, 72)]
        sector = [(0,0)] + arc_pts + [(0,0)]
        g.add(
            poly(sector, GOLD, 0.18),
            lbl("L", L*0.9*0.5, L*0.9*0.22, 22, GOLD),
            lbl(r"\alpha", L*0.9*0.3, 0.3, 22, GOLD),
        )

    elif kind == "square_equilateral":
        a = 3.2
        ht = a * math.sqrt(3) / 2
        x_exact = a * (2*math.sqrt(3) - 3)
        x_draw = max(0.28 + (x_exact - 0.28) * t, 0.22)
        g.add(
            poly([(-a/2, 0), (a/2, 0), (0, ht)], BLUE, 0.1),
            poly([(-x_draw/2, 0), (x_draw/2, 0),
                  (x_draw/2, x_draw), (-x_draw/2, x_draw)], GREEN, 0.32),
            lbl("a", 0, -0.42, 22, BLUE),
            lbl("x", x_draw/2+0.32, x_draw/2, 22, GREEN),
        )

    elif kind == "cone_in_cylinder":
        R, H = 2.0, 2.8
        h_draw = (0.6 + (1.0 - 0.6) * t) * H
        g.add(
            poly([(-R, -H/2), (R, -H/2), (R, H/2), (-R, H/2)], MUTED, 0.05),
            poly([(-R, -H/2), (R, -H/2), (0, -H/2+h_draw)], GREEN, 0.25),
            seg((-R, -H/2), (R, -H/2), BLUE, 2.5),
            seg((0, -H/2), (0, H/2), MUTED, 1.5, True),
            seg((0, -H/2+h_draw), (R, -H/2), GOLD, 2.5),
            lbl("R", R+0.32, -H/2+0.22, 22, GOLD),
            lbl("H", 0.32, 0, 22, GOLD),
            lbl("h", 0.32, -H/2+h_draw/2, 22, GREEN),
            lbl("l", R*0.6+0.1, -H/2+h_draw*0.45, 22, GOLD),
        )

    else:
        g.add(text_mob("Mo hinh hinh hoc", 28, BLUE, True))

    g.move_to(ORIGIN)
    fit(g, width=3.65, height=3.55)
    return g


class LectureBase(Scene):
    lesson = None

    def speak(self, item, animation=None):
        start    = float(self.time)
        duration = float(item["duration"])
        self.add_sound(item["audio"])
        self.events.append({"start": start,
                             "end":   start + duration,
                             "text":  item["voice"]})
        reveal = 0.0
        if animation is not None:
            reveal = min(0.55, max(0.2, duration * 0.2))
            self.play(animation, run_time=reveal)
        self.wait(max(0.05, duration - reveal) + 0.3)

    def row_mobject(self, row):
        if row["kind"] == "math":
            mob = math_mob(row["text"], 30)
            if r"\boxed" in row["text"]:
                mob.set_color(GOLD)
        else:
            wrapped = textwrap.fill(row["text"], width=53,
                                    break_long_words=False,
                                    break_on_hyphens=False)
            mob = text_mob(wrapped, 25, INK)
        fit(mob, width=7.65, height=1.12)
        return mob

    def construct(self):
        q = self.lesson
        self.events = []

        top = Rectangle(width=14.23, height=0.08, stroke_width=0,
                         fill_color=BLUE, fill_opacity=1).move_to(UP * 3.96)
        section = text_mob(q["section"], 18, CYAN, True)
        fit(section, width=11.5)
        section.move_to(pt(-6.57, 3.54), aligned_edge=LEFT)
        title = text_mob(q["title"], 32, INK, True)
        fit(title, width=12.85, height=0.52)
        title.move_to(pt(-6.57, 3.0), aligned_edge=LEFT)
        index = text_mob(f"{q['order']:02d}/{q['total']:02d}",
                          18, MUTED).move_to(pt(6.23, 3.54))
        left_panel = RoundedRectangle(
            width=4.12, height=5.64, corner_radius=0.15,
            stroke_color="#2A3D5C", stroke_width=1,
            fill_color=PANEL, fill_opacity=1).move_to(pt(-4.76, -0.33))
        right_panel = RoundedRectangle(
            width=8.6, height=5.64, corner_radius=0.15,
            stroke_color="#2A3D5C", stroke_width=1,
            fill_color=PANEL, fill_opacity=1).move_to(pt(1.91, -0.33))
        left_heading = text_mob("MO HINH HINH HOC", 20, BLUE, True
                                 ).move_to(pt(-4.76, 2.02))
        note = text_mob("Minh hoa - Khong theo ti le", 15, MUTED)
        fit(note, width=3.65)
        note.move_to(pt(-4.76, -2.47))
        flow = text_mob("Mo hinh -> Ham so -> Toi uu", 15, CYAN)
        fit(flow, width=3.65)
        flow.move_to(pt(-4.76, -2.82))
        footer_line = seg((-6.65, -3.38), (6.65, -3.38), "#304665", 1)
        footer = text_mob(SETTINGS["teacher"], 22, GOLD, True)
        footer.move_to(pt(0, -3.69))

        self.add(top, section, title, index,
                  left_panel, right_panel, left_heading,
                  note, flow, footer_line, footer)

        geometry = make_diagram(q["diagram"], 0)
        geometry.move_to(pt(-4.76, -0.2))
        self.speak(q["intro"], FadeIn(geometry, shift=UP * 0.08))

        current = None
        pages   = q["pages"]

        for page_index, page in enumerate(pages):
            if current is not None:
                all_m = list(current)
                if all_m:
                    self.play(FadeOut(Group(*all_m)), run_time=0.25)
                self.remove(*all_m)

            heading = text_mob(page["title"], 24, CYAN, True)
            fit(heading, width=7.1, height=0.48)
            heading.move_to(pt(-1.96, 2.02), aligned_edge=LEFT)
            count = text_mob(f"{page_index+1}/{len(pages)}",
                              15, MUTED).move_to(pt(5.72, 2.02))
            divider = seg((-1.96, 1.64), (5.82, 1.64), "#304665", 1)
            current = VGroup(heading, count, divider)
            self.play(FadeIn(current), run_time=0.25)

            if page_index == len(pages) - 1 and q["diagram"] != "method":
                target = make_diagram(q["diagram"], 1)
                target.move_to(pt(-4.76, -0.2))
                self.play(Transform(geometry, target), run_time=1.25)

            rows = VGroup(*[self.row_mobject(row) for row in page["rows"]])
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.27)
            fit(rows, width=7.65, height=3.95)
            rows.move_to(pt(-1.94, 1.27), aligned_edge=UL)

            for data, mob in zip(page["rows"], rows):
                self.speak(data, FadeIn(mob, shift=UP * 0.04))
                current.add(mob)
            self.wait(0.4)

        self.wait(0.7)
        all_m = list(self.mobjects)
        if all_m:
            self.play(FadeOut(Group(*all_m)), run_time=0.35)
        self.clear()

        ev_path = HERE / "events" / (q["id"] + ".json")
        ev_path.parent.mkdir(exist_ok=True)
        ev_path.write_text(
            json.dumps(self.events, ensure_ascii=False, indent=2),
            encoding="utf-8")


for lesson in DATA:
    cname = "B_" + lesson["id"]
    globals()[cname] = type(cname, (LectureBase,),
                            {"lesson": lesson, "__module__": __name__})
'''

settings = {
    "teacher": TEN_THAY, "voice": GIONG_DOC, "rate": TOC_DO_DOC,
    "width": CHIEU_RONG, "height": CHIEU_CAO, "fps": FPS,
}

signature_data = (
    SCENE_SOURCE
    + json.dumps(selected, ensure_ascii=False, sort_keys=True)
    + json.dumps(settings, ensure_ascii=False, sort_keys=True)
)
render_key = hashlib.sha256(
    signature_data.encode("utf-8")
).hexdigest()[:14]

WORK = ROOT / ("render_" + render_key)
WORK.mkdir(exist_ok=True)
(WORK / "events").mkdir(exist_ok=True)
CLIPS = WORK / "clips";  CLIPS.mkdir(exist_ok=True)
MEDIA = WORK / "media";  MEDIA.mkdir(exist_ok=True)

scene_file = WORK / "bai_giang.py"
scene_file.write_text(SCENE_SOURCE, encoding="utf-8")
(WORK / "lessons.json").write_text(
    json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8")
(WORK / "settings.json").write_text(
    json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")

compile(SCENE_SOURCE, str(scene_file), "exec")

# ======================== 6. DUNG VIDEO ==============================

print("\nBUOC 3/5 - Dung tung bai bang Manim.")
print("Thu muc lam viec:", WORK)
print("Neu chay lai trong cung phien, bai da xong se duoc dung lai.\n")

clip_paths     = []
clip_durations = []

for index, lesson in enumerate(selected, 1):
    code       = lesson["id"]
    class_name = "B_" + code
    output_clip = CLIPS / (class_name + ".mp4")
    event_file  = WORK / "events" / (code + ".json")
    done_file   = WORK / (code + ".done")

    reusable = False
    if output_clip.exists() and event_file.exists() and done_file.exists():
        try:
            probe_duration(output_clip)
            reusable = True
        except Exception:
            reusable = False

    if reusable:
        print(f"[{index}/{len(selected)}] Dung lai: {code} - {lesson['title']}")
    else:
        print(f"[{index}/{len(selected)}] Dang dung: {code} - {lesson['title']}")
        output_clip.unlink(missing_ok=True)
        done_file.unlink(missing_ok=True)
        started = time.time()
        run_log(
            [sys.executable, "-m", "manim",
             "--renderer", "cairo", "--format", "mp4",
             "--fps", str(FPS), "-r", f"{CHIEU_RONG},{CHIEU_CAO}",
             "--media_dir", str(MEDIA),
             "--progress_bar", "none", "--verbosity", "WARNING",
             "-o", class_name, str(scene_file), class_name],
            WORK / ("render_" + code + ".log"), cwd=WORK,
        )
        candidates = [p for p in MEDIA.rglob(class_name + ".mp4")
                      if "partial_movie_files" not in str(p)]
        if not candidates:
            raise RuntimeError(
                "Khong tim thay video cua " + code
                + ". Xem nhat ky trong " + str(WORK))
        rendered = max(candidates, key=lambda p: p.stat().st_mtime)
        shutil.copy2(rendered, output_clip)
        if not event_file.exists():
            raise RuntimeError("Thieu du lieu phu de cua " + code)
        duration = probe_duration(output_clip)
        done_file.write_text("OK", encoding="utf-8")
        print(f"    Xong {duration/60:.1f} phut video; "
              f"thoi gian dung {(time.time()-started)/60:.1f} phut.")

    clip_paths.append(output_clip)
    clip_durations.append(probe_duration(output_clip))

# ======================== 7. GHEP VA XUAT ============================

print("\nBUOC 4/5 - Ghep MP4, xuat phu de va muc luc.")

concat_file = WORK / "concat.txt"
concat_file.write_text(
    "\n".join("file '" + p.as_posix() + "'" for p in clip_paths) + "\n",
    encoding="utf-8")
joined = WORK / "joined.mp4"
run_log(
    ["ffmpeg", "-y", "-v", "warning",
     "-f", "concat", "-safe", "0", "-i", str(concat_file),
     "-map", "0:v:0", "-map", "0:a:0",
     "-c", "copy", "-movflags", "+faststart", str(joined)],
    WORK / "ffmpeg_concat.log")


def time_hms(s):
    n = max(0, int(s))
    return f"{n//3600:02d}:{(n%3600)//60:02d}:{n%60:02d}"


def time_srt(s):
    n = max(0, round(s*1000))
    h, r = divmod(n, 3600000)
    m, r = divmod(r, 60000)
    sc, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{sc:02d},{ms:03d}"


def esc_meta(s):
    return (s.replace("\\","\\\\").replace("=","\\=")
              .replace(";","\\;").replace("#","\\#").replace("\n"," "))


def split_caption(text, max_chars=86):
    parts, cur = [], []
    for word in text.split():
        cand = " ".join(cur + [word])
        if cur and len(cand) > max_chars:
            parts.append(" ".join(cur)); cur = [word]
        else:
            cur.append(word)
    if cur: parts.append(" ".join(cur))
    return parts


metadata = [";FFMETADATA1",
            "title=" + esc_meta("Toi uu Khoi Tron Xoay - " + TEN_THAY),
            "artist=" + esc_meta(TEN_THAY)]
chapter_text, subtitles, offset = [], [], 0.0

for lesson, dur in zip(selected, clip_durations):
    ct = lesson["id"] + " - " + lesson["title"]
    metadata.extend(["[CHAPTER]", "TIMEBASE=1/1000",
                      "START=" + str(round(offset*1000)),
                      "END="   + str(round((offset+dur)*1000)),
                      "title=" + esc_meta(ct)])
    chapter_text.append(time_hms(offset) + "  " + ct)
    events = json.loads(
        (WORK/"events"/(lesson["id"]+".json")).read_text(encoding="utf-8"))
    for ev in events:
        parts = split_caption(ev["text"])
        weights = [max(1, len(p)) for p in parts]
        total_w = sum(weights)
        if total_w == 0: continue
        spoken = ev["end"] - ev["start"]
        used = 0
        for part, w in zip(parts, weights):
            beg = offset + ev["start"] + spoken*used/total_w
            used += w
            subtitles.append((beg, offset+ev["start"]+spoken*used/total_w, part))
    offset += dur

metadata_file = WORK / "chapters.ffmetadata"
metadata_file.write_text("\n".join(metadata)+"\n", encoding="utf-8")
suffix = "TOAN_BO" if not CHON_BAI else "_".join(CHON_BAI)
final_video    = ROOT / ("Khoi_Tron_Xoay_" + suffix + ".mp4")
final_srt      = ROOT / ("Phu_de_"         + suffix + ".srt")
final_chapters = ROOT / ("Muc_luc_"        + suffix + ".txt")
final_script   = ROOT / ("Kich_ban_"       + suffix + ".txt")

run_log(
    ["ffmpeg", "-y", "-v", "warning",
     "-i", str(joined), "-f", "ffmetadata", "-i", str(metadata_file),
     "-map", "0:v:0", "-map", "0:a:0",
     "-map_metadata", "1", "-map_chapters", "1",
     "-c", "copy", "-movflags", "+faststart", str(final_video)],
    WORK / "ffmpeg_metadata.log")

srt_blocks = []
for i, (beg, end_, content) in enumerate(subtitles, 1):
    wrapped = textwrap.fill(content, width=46,
                             break_long_words=False, break_on_hyphens=False)
    srt_blocks.append(str(i)+"\n"+time_srt(beg)+" --> "+time_srt(end_)+"\n"+wrapped+"\n")
final_srt.write_text("\n".join(srt_blocks), encoding="utf-8")
final_chapters.write_text("\n".join(chapter_text)+"\n", encoding="utf-8")

script_parts = []
for lesson in selected:
    script_parts.append("\n"+"="*70+"\n"
                        +lesson["id"]+" - "+lesson["title"]+"\n"
                        +"="*70+"\n"+lesson["intro"]["voice"]+"\n")
    for page in lesson["pages"]:
        script_parts.append("\n["+page["title"]+"]\n")
        for row in page["rows"]:
            if row["kind"]=="math":
                script_parts.append("LaTeX: "+row["text"]+"\n")
            script_parts.append(row["voice"]+"\n")
final_script.write_text("".join(script_parts), encoding="utf-8")

source_zip = ROOT / ("Ma_nguon_" + suffix + ".zip")
with zipfile.ZipFile(source_zip, "w", compression=zipfile.ZIP_DEFLATED) as arc:
    arc.write(scene_file,          "bai_giang.py")
    arc.write(WORK/"lessons.json", "lessons.json")
    arc.write(WORK/"settings.json","settings.json")
    arc.write(final_srt,      final_srt.name)
    arc.write(final_chapters, final_chapters.name)
    arc.write(final_script,   final_script.name)
    arc.writestr("HUONG_DAN.txt",
                 "Bai giang Manim - Thay Nguyen Van Sang\n"
                 "Dan toan bo tep Colab vao mot o Google Colab de chay.\n")

# ======================== 8. HOAN TAT ================================

print("\nBUOC 5/5 - HOAN TAT.")
print("="*72)
print("Video:", final_video)
print("Thoi luong:", time_hms(probe_duration(final_video)))
print("Dung luong:", f"{final_video.stat().st_size/(1024**2):.1f} MB")
print("Phu de:", final_srt)
print("Muc luc:", final_chapters)
print("Ma nguon:", source_zip)
print("="*72)
print("\nMUC LUC")
print("\n".join(chapter_text))

from IPython.display import display, HTML

try:
    from google.colab import files, output

    def _dl_video():    files.download(str(final_video))
    def _dl_srt():      files.download(str(final_srt))
    def _dl_chapters(): files.download(str(final_chapters))
    def _dl_source():   files.download(str(source_zip))

    output.register_callback("sang.video",    _dl_video)
    output.register_callback("sang.srt",      _dl_srt)
    output.register_callback("sang.chapters", _dl_chapters)
    output.register_callback("sang.source",   _dl_source)

    display(HTML("""
    <div style="background:#101b31;color:#edf4ff;
        padding:18px;border-radius:12px;font-family:Arial;margin:14px 0;">
      <div style="font-size:20px;color:#ffd166;font-weight:bold;">
        Thay Nguyen Van Sang - Khoi Tron Xoay &amp; Cat Ghep Hinh
      </div>
      <p>Video da dung xong. Chon tep can tai ben duoi.</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;">
        <button style="padding:12px 18px;background:#2563eb;color:white;
               border:0;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.video',[],{})">
          &#9654; Tai video MP4</button>
        <button style="padding:12px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.srt',[],{})">
          Tai phu de SRT</button>
        <button style="padding:12px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.chapters',[],{})">
          Tai muc luc</button>
        <button style="padding:12px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang.source',[],{})">
          Tai ma nguon ZIP</button>
      </div>
    </div>
    """))

    if HIEN_VIDEO:
        try:
            import threading, functools
            from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
            from urllib.parse import quote
            class _Q(SimpleHTTPRequestHandler):
                def log_message(self, *a): pass
            handler = functools.partial(_Q, directory=str(ROOT))
            srv = ThreadingHTTPServer(("0.0.0.0", 0), handler)
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            port = srv.server_address[1]
            proxy = output.eval_js(f"google.colab.kernel.proxyPort({port})")
            video_url = proxy.rstrip("/") + "/" + quote(final_video.name)
            display(HTML(
                '<video controls preload="metadata" '
                'style="width:100%;max-width:1100px;'
                'border-radius:12px;background:#0b1222;" '
                'src="' + video_url + '"></video>'))
        except Exception as e:
            print("Khong mo duoc trinh xem truoc. Dung nut Tai video MP4.")
    if TU_DONG_TAI_VIDEO:
        files.download(str(final_video))

except ImportError:
    print("Mo truc tiep tep MP4 theo duong dan da in phia tren.")

print("\nQUAN TRONG: tai cac tep ve may truoc khi ket thuc phien Colab. "
      "Du lieu trong /content khong duoc luu vinh vien.")

