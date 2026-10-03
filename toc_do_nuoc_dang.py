# ======================================================================
#  1 Ô COLAB DUY NHẤT — DÁN VÀO VÀ CHẠY
#  10 BÀI TOÁN TỐC ĐỘ THAY ĐỔI: TỐC ĐỘ NƯỚC DÂNG
#  Giọng Nam tiếng Việt · Footer: Thầy Nguyễn Văn Sang
# ======================================================================
# Lý do sửa so với phiên bản cũ:
#   - Bỏ manim-voiceover (không ổn định trên Colab): dùng edge-tts trực tiếp
#   - Bỏ ThreeDScene + Surface (API thay đổi, crash với always_redraw)
#   - Dùng Cairo renderer + hình 2D minh hoạ (nhanh, ổn định)
#   - Caching audio (chạy lại không mất thời gian tổng hợp giọng)
# ======================================================================

import os, sys, json, math, time, asyncio, hashlib, shutil, zipfile, textwrap, subprocess
from pathlib import Path

# ─────────────── CẤU HÌNH ───────────────
TEN_THAY   = "Thầy Nguyễn Văn Sang"
GIONG_DOC  = "vi-VN-NamMinhNeural"
TOC_DO     = "-5%"

# Chỉ dựng một số bài để thử: CHON_BAI = ["B01","B02"]
# Để trống để dựng toàn bộ 10 bài:
CHON_BAI = []

CHIEU_RONG = 1280
CHIEU_CAO  = 720
FPS        = 15
HIEN_VIDEO = True

if Path("/content").exists():
    ROOT = Path("/content/NuocDang_ThayNguyenVanSang")
else:
    ROOT = Path.cwd() / "NuocDang_ThayNguyenVanSang"

ROOT.mkdir(parents=True, exist_ok=True)
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(exist_ok=True)

os.environ["DEBIAN_FRONTEND"] = "noninteractive"
os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"


def run_log(cmd, logfile, cwd=None):
    logfile = Path(logfile)
    with logfile.open("w", encoding="utf-8") as f:
        r = subprocess.run([str(x) for x in cmd], cwd=cwd,
                           stdout=f, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        print(logfile.read_text(encoding="utf-8", errors="replace")[-16000:])
        raise RuntimeError("Lệnh thất bại — xem log: " + str(logfile))


def probe_dur(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    v = float(r.stdout.strip())
    if not math.isfinite(v) or v <= 0:
        raise RuntimeError("File không có thời lượng hợp lệ: " + str(path))
    return v


# ─────────────── BƯỚC 1: CÀI ĐẶT ───────────────
print("BƯỚC 1/5 — Cài môi trường Manim, LaTeX, FFmpeg, giọng đọc.")

marker = ROOT / "env_ok_v4.txt"
if Path("/content").exists() and not marker.exists():
    run_log(["apt-get", "update", "-qq"], ROOT / "apt_update.log")
    run_log(["apt-get", "install", "-y", "-qq",
             "ffmpeg", "pkg-config", "python3-dev",
             "libcairo2-dev", "libpango1.0-dev",
             "texlive-latex-base", "texlive-latex-recommended",
             "texlive-latex-extra", "texlive-fonts-recommended",
             "texlive-science", "dvisvgm",
             "fonts-dejavu-core", "fonts-noto-core"],
            ROOT / "apt_install.log")
    run_log([sys.executable, "-m", "pip", "install", "-q",
             "manim==0.19.0", "edge-tts", "nest_asyncio"],
            ROOT / "pip_install.log")
    run_log([sys.executable, "-c",
             "import manim, edge_tts; print(manim.__version__)"],
            ROOT / "env_check.log")
    marker.write_text("OK", encoding="utf-8")

# ─────────────── DỮ LIỆU 10 BÀI TOÁN ───────────────

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


# ── BÀI 1 ──────────────────────────────────────────────────────────────
Q("B01","BÀI 1","Tốc độ nước dâng trong Bể hình trụ đứng","tru_dung",
  P("Mô hình hình học & Công thức tổng quát",
    T("Bể nước hình trụ đứng có bán kính đáy R. Nước được bơm vào với lưu lượng không đổi v.",
      "Cho một bể nước hình trụ đứng có bán kính đáy là R. Nước được bơm vào bể với lưu lượng không đổi là v. Tìm tốc độ nước dâng trong bể."),
    T("Kí hiệu h(t) là mực nước, S(h) là diện tích mặt thoáng tại cao độ h.",
      "Kí hiệu h là mực nước tại thời điểm t, S h là diện tích mặt thoáng của nước tại cao độ h."),
    M(r"V(t) = \int_0^{h(t)} S(z) dz \Rightarrow v = V'(t) = S(h) \cdot h'(t)",
      "Thể tích nước bằng tích phân của tiết diện mặt thoáng. Lấy đạo hàm hai vế theo thời gian, ta có lưu lượng v bằng S nhân với tốc độ nước dâng h phẩy."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Do bể có hình trụ đứng, diện tích mặt thoáng luôn bằng diện tích đáy.",
      "Vì bể nước là hình trụ đứng, nên mặt thoáng của nước luôn là hình tròn có bán kính bằng bán kính đáy R, không phụ thuộc vào chiều cao h."),
    M(r"r = R\ (\text{const}) \Rightarrow S(h) = \pi r^2 = \pi R^2",
      "Do đó, bán kính mặt thoáng r luôn bằng R. Suy ra diện tích mặt thoáng S bằng Pi nhân R bình phương."),
    T("Diện tích mặt thoáng là một hằng số, dẫn đến tốc độ nước dâng cũng là hằng số.",
      "Do diện tích mặt thoáng là một hằng số, nên tốc độ nước dâng trong bể cũng là một hằng số."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Thay S(h) vào phương trình v = S(h) * h', ta tính được tốc độ nước dâng:",
      "Thay công thức diện tích mặt thoáng vào phương trình đạo hàm, ta tính được tốc độ nước dâng h phẩy như sau."),
    M(r"v = \pi R^2 \cdot h' \Rightarrow h' = \frac{v}{\pi R^2}",
      "Lưu lượng v bằng Pi R bình phương nhân h phẩy. Rút ra h phẩy bằng v chia cho Pi nhân R bình phương."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v}{\pi R^2} }",
      "Kết luận: Tốc độ nước dâng trong bể hình trụ đứng là một hằng số, bằng lưu lượng bơm chia cho diện tích đáy của bể."),
  ),
)

# ── BÀI 2 ──────────────────────────────────────────────────────────────
Q("B02","BÀI 2","Tốc độ dâng trong Phễu nón đỉnh hướng xuống","non_xuong",
  P("Mô hình hình học & Công thức tổng quát",
    T("Phễu hình nón, bán kính miệng R, chiều cao H, đỉnh hướng xuống. Lưu lượng v.",
      "Cho một chiếc phễu hình nón có bán kính miệng là R, chiều cao là H, đỉnh hướng xuống dưới. Nước chảy vào phễu với lưu lượng v. Tìm tốc độ nước dâng theo chiều cao h."),
    T("Cắt nón bởi mặt phẳng qua trục, áp dụng định lý Talet.",
      "Cắt hình nón bởi mặt phẳng qua trục đối xứng, ta được mặt cắt là một tam giác cân. Áp dụng định lý Ta-lét để tìm bán kính mặt nước."),
    M(r"\frac{r}{R} = \frac{h}{H} \Rightarrow r = R\frac{h}{H}",
      "Theo định lý Ta-lét, tỉ số bán kính r chia R bằng h chia H. Suy ra bán kính mặt thoáng r bằng R nhân h chia H."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Mặt thoáng là hình tròn bán kính r thay đổi theo chiều cao mực nước h.",
      "Mặt thoáng của nước là một hình tròn có bán kính r phụ thuộc vào chiều cao h."),
    M(r"S(h) = \pi r^2 = \pi \left(R\frac{h}{H}\right)^2 = \pi \frac{R^2}{H^2} h^2",
      "Diện tích mặt thoáng S h bằng Pi nhân r bình phương, thay r vào ta được Pi nhân R bình trên H bình nhân h bình phương."),
    T("Khi nước càng dâng cao, diện tích mặt thoáng càng lớn.",
      "Ta thấy diện tích mặt thoáng tỉ lệ thuận với bình phương chiều cao h, nên khi nước càng dâng cao thì mặt thoáng càng lớn."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Thay S(h) vào phương trình v = S(h) * h':",
      "Thay công thức diện tích S h vừa tính được vào phương trình lưu lượng v bằng S nhân h phẩy."),
    M(r"v = \left(\pi \frac{R^2}{H^2} h^2\right) \cdot h' \Rightarrow h' = \frac{v}{\pi \frac{R^2}{H^2} h^2}",
      "Lưu lượng v bằng Pi nhân R bình trên H bình nhân h bình, tất cả nhân với h phẩy. Từ đó rút h phẩy ra."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v H^2}{\pi R^2 h^2} }",
      "Kết luận: Tốc độ nước dâng tỉ lệ nghịch với bình phương mực nước h. Tức là nước dâng càng ngày càng chậm lại."),
  ),
)

# ── BÀI 3 ──────────────────────────────────────────────────────────────
Q("B03","BÀI 3","Tốc độ dâng trong Khối cầu (Bình cầu)","khoi_cau",
  P("Mô hình hình học & Công thức tổng quát",
    T("Bình chứa hình cầu bán kính R. Đổ nước vào với lưu lượng v không đổi.",
      "Cho một bình chứa hình cầu có bán kính là R. Nước được bơm vào bình với lưu lượng không đổi là v. Tìm tốc độ nước dâng tại mực nước h."),
    T("Gọi r là bán kính mặt thoáng tại chiều cao h (0 < h < 2R). Khoảng cách tới tâm là |R-h|.",
      "Gọi r là bán kính của mặt thoáng tại độ cao h tính từ đáy bình, h lớn hơn 0 và nhỏ hơn 2 R. Khoảng cách từ mặt nước tới tâm mặt cầu là trị tuyệt đối của R trừ h."),
    M(r"r^2 + (R-h)^2 = R^2 \Rightarrow r^2 = R^2 - (R-h)^2",
      "Áp dụng định lý Pi-ta-go cho tam giác vuông tạo bởi tâm mặt cầu và mặt thoáng, ta có r bình cộng R trừ h tất cả bình bằng R bình phương."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Khai triển hằng đẳng thức để tìm bình phương bán kính mặt thoáng.",
      "Ta khai triển hằng đẳng thức để tính giá trị bình phương của bán kính mặt thoáng r."),
    M(r"r^2 = R^2 - (R^2 - 2Rh + h^2) = 2Rh - h^2",
      "Từ phương trình trên, r bình phương bằng 2 R h trừ h bình phương."),
    M(r"S(h) = \pi r^2 = \pi (2Rh - h^2)",
      "Diện tích mặt thoáng S h bằng Pi nhân r bình, thay vào ta được Pi nhân mở ngoặc 2 R h trừ h bình phương đóng ngoặc."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Từ hệ thức v = S(h) * h', ta có tốc độ dâng nước là:",
      "Thay biểu thức diện tích S h vừa tính vào hệ thức lưu lượng cơ bản, ta tính được tốc độ nước dâng h phẩy."),
    M(r"v = \pi (2Rh - h^2) \cdot h' \Rightarrow h' = \frac{v}{\pi(2Rh - h^2)}",
      "Lưu lượng v bằng Pi nhân 2 R h trừ h bình nhân h phẩy. Từ đó suy ra biểu thức của h phẩy."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v}{\pi h(2R - h)} }",
      "Kết luận: Tốc độ nước dâng đạt giá trị nhỏ nhất khi mặt thoáng qua tâm mặt cầu, tức là tại h bằng R."),
  ),
)

# ── BÀI 4 ──────────────────────────────────────────────────────────────
Q("B04","BÀI 4","Hình chóp tứ giác đều đỉnh hướng xuống","chop_deu",
  P("Mô hình hình học & Công thức tổng quát",
    T("Bể hình chóp tứ giác đều đỉnh hướng xuống, cạnh đáy a, chiều cao H.",
      "Cho một bể chứa hình chóp tứ giác đều, đỉnh hướng xuống dưới. Cạnh đáy là a, chiều cao bể là H. Bơm nước lưu lượng v."),
    T("Mặt thoáng là hình vuông cạnh x. Dùng định lý Talet trong thiết diện qua trục.",
      "Do bể là hình chóp tứ giác đều, mặt thoáng của nước luôn là một hình vuông có cạnh là x. Áp dụng định lý Ta-lét trong thiết diện qua trục để tìm x."),
    M(r"\frac{x}{a} = \frac{h}{H} \Rightarrow x = a\frac{h}{H}",
      "Theo định lý Ta-lét, tỉ số x chia a bằng h chia H. Suy ra độ dài cạnh mặt thoáng x bằng a nhân h chia H."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Diện tích mặt thoáng hình vuông bằng bình phương độ dài cạnh.",
      "Diện tích của mặt thoáng nước hình vuông được tính bằng bình phương độ dài cạnh của nó."),
    M(r"S(h) = x^2 = \left(a\frac{h}{H}\right)^2 = \frac{a^2}{H^2}h^2",
      "Diện tích S h bằng x bình phương. Thay x vào ta được a bình chia H bình, nhân với h bình phương."),
    T("Diện tích mặt thoáng cũng tỉ lệ thuận với bình phương mực nước h.",
      "Giống như hình nón đỉnh hướng xuống, diện tích mặt thoáng của chóp tứ giác đều cũng tỉ lệ thuận với bình phương của chiều cao h."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Sử dụng công thức liên hệ v = S(h) * h', ta suy ra:",
      "Áp dụng phương trình liên hệ giữa lưu lượng, diện tích mặt thoáng và tốc độ nước dâng, ta tính được tốc độ h phẩy."),
    M(r"v = \left(\frac{a^2}{H^2}h^2\right) \cdot h' \Rightarrow h' = \frac{v}{\frac{a^2}{H^2}h^2}",
      "Lưu lượng v bằng a bình chia H bình nhân h bình, tất cả nhân h phẩy. Từ đó rút h phẩy ra."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v H^2}{a^2 h^2} }",
      "Kết luận: Tốc độ nước dâng trong chóp tứ giác đều tỉ lệ nghịch với bình phương độ cao, nước dâng càng lúc càng chậm."),
  ),
)

# ── BÀI 5 ──────────────────────────────────────────────────────────────
Q("B05","BÀI 5","Máng lăng trụ tam giác đều (Bể máng)","mang_tam_giac",
  P("Mô hình hình học & Công thức tổng quát",
    T("Máng nước dài L. Mặt cắt là tam giác cân đỉnh hướng xuống, miệng rộng a, cao H.",
      "Cho một máng nước dài L. Mặt cắt ngang của máng là một tam giác cân có đỉnh hướng xuống, độ rộng miệng máng là a, chiều cao máng là H."),
    T("Mặt thoáng là hình chữ nhật chiều dài L, chiều rộng x thay đổi theo h.",
      "Mặt thoáng của nước trong máng luôn là một hình chữ nhật có chiều dài cố định là L và chiều rộng x thay đổi theo chiều cao h."),
    M(r"\frac{x}{a} = \frac{h}{H} \Rightarrow x = a\frac{h}{H}",
      "Áp dụng định lý Ta-lét trên mặt cắt ngang tam giác, ta có x bằng a nhân h chia H."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Diện tích mặt thoáng là diện tích hình chữ nhật kích thước L và x.",
      "Diện tích mặt thoáng của máng nước được tính bằng tích của chiều dài máng và bề rộng mặt nước."),
    M(r"S(h) = x \cdot L = \left(a\frac{h}{H}\right) L = \frac{a L}{H} h",
      "Diện tích S h bằng x nhân L. Thay x vào, ta được công thức là a nhân L chia H, tất cả nhân với h."),
    T("Khác với hình nón, diện tích mặt thoáng ở đây chỉ tỉ lệ bậc nhất với h.",
      "Ở bài toán lăng trụ tam giác, diện tích mặt thoáng chỉ tỉ lệ bậc nhất với chiều cao h, không phải bậc hai."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Thay vào công thức v = S(h) * h', ta có:",
      "Ta thay biểu thức diện tích mặt thoáng vừa tính được vào phương trình lưu lượng cơ bản."),
    M(r"v = \left(\frac{a L}{H} h\right) \cdot h' \Rightarrow h' = \frac{v}{\frac{a L}{H} h}",
      "Lưu lượng v bằng a nhân L chia H nhân h, tất cả nhân với h phẩy. Rút h phẩy ra."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v H}{a L h} }",
      "Kết luận: Tốc độ nước dâng trong máng lăng trụ tam giác tỉ lệ nghịch với bậc nhất của chiều cao h."),
  ),
)

# ── BÀI 6 ──────────────────────────────────────────────────────────────
Q("B06","BÀI 6","Bồn nước hình trụ đặt nằm ngang","tru_ngang",
  P("Mô hình hình học & Công thức tổng quát",
    T("Bồn trụ nằm ngang, dài L, bán kính R. Đổ nước với lưu lượng v.",
      "Cho một bồn chứa hình trụ đặt nằm ngang, chiều dài bồn là L, bán kính đáy là R. Nước được bơm vào bồn với lưu lượng v."),
    T("Mặt thoáng là hình chữ nhật dài L, rộng x thay đổi. Khoảng cách mặt nước đến trục là |R-h|.",
      "Mặt thoáng của nước là hình chữ nhật có chiều dài cố định L và chiều rộng x. Khoảng cách từ trục đến mặt nước là trị tuyệt đối của R trừ h."),
    M(r"\left(\frac{x}{2}\right)^2 + (R-h)^2 = R^2 \Rightarrow x = 2\sqrt{R^2 - (R-h)^2}",
      "Áp dụng định lý Pi-ta-go trong mặt cắt tròn, bình phương nửa x cộng bình phương R trừ h bằng R bình. Rút x ra."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Rút gọn biểu thức của bề rộng mặt nước x.",
      "Ta khai triển và rút gọn căn thức để tìm biểu thức đơn giản nhất cho bề rộng mặt nước x."),
    M(r"x = 2\sqrt{R^2 - (R^2 - 2Rh + h^2)} = 2\sqrt{2Rh - h^2}",
      "Bề rộng x bằng hai lần căn bậc hai của 2 R h trừ h bình phương."),
    M(r"S(h) = x \cdot L = 2L \sqrt{2Rh - h^2}",
      "Diện tích mặt thoáng S h bằng x nhân L. Kết quả là 2 L nhân căn của 2 R h trừ h bình phương."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Thay S(h) vào phương trình v = S(h) * h', ta được:",
      "Thế diện tích mặt thoáng vào phương trình tính lưu lượng để tìm tốc độ dâng."),
    M(r"v = 2L \sqrt{2Rh - h^2} \cdot h' \Rightarrow h' = \frac{v}{2L \sqrt{2Rh - h^2}}",
      "Từ phương trình v bằng 2 L căn 2 R h trừ h bình nhân h phẩy, ta tìm được công thức của h phẩy."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v}{2L \sqrt{h(2R - h)}} }",
      "Kết luận: Tốc độ nước dâng đạt cực tiểu khi mặt nước qua trục bồn ngang, tương ứng lúc diện tích mặt thoáng lớn nhất."),
  ),
)

# ── BÀI 7 ──────────────────────────────────────────────────────────────
Q("B07","BÀI 7","Nửa mặt cầu (Bát nước hình bán cầu)","ban_cau",
  P("Mô hình hình học & Công thức tổng quát",
    T("Bát nước là nửa mặt cầu bán kính R, miệng nằm ngang. Bơm nước lưu lượng v.",
      "Cho một chiếc bát hình bán cầu ngửa có bán kính R, miệng bát nằm ngang. Nước được đổ vào bát với lưu lượng v."),
    T("Mặt thoáng là hình tròn bán kính r. Tại độ cao h (0 < h < R), khoảng cách đến tâm là R - h.",
      "Mặt thoáng của nước là một hình tròn có bán kính r. Tâm của mặt cầu cách mặt thoáng một đoạn bằng R trừ h."),
    M(r"r^2 + (R-h)^2 = R^2 \Rightarrow r^2 = R^2 - (R-h)^2",
      "Theo định lý Pi-ta-go trong tam giác vuông tạo bởi tâm mặt cầu và mặt phẳng nước, ta có r bình bằng R bình trừ đi R trừ h tất cả bình."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Bán kính mặt thoáng hoàn toàn tương tự bài toán khối cầu nguyên.",
      "Công thức tính bán kính mặt thoáng của bán cầu ngửa hoàn toàn giống phần nửa dưới của mặt cầu."),
    M(r"r^2 = 2Rh - h^2",
      "Bình phương bán kính r bằng 2 R h trừ h bình phương."),
    M(r"S(h) = \pi r^2 = \pi (2Rh - h^2)",
      "Diện tích mặt thoáng S h của nước trong bát là Pi nhân mở ngoặc 2 R h trừ h bình phương đóng ngoặc."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Từ hệ thức v = S(h) * h', tốc độ dâng nước h' là:",
      "Thay S h vào hệ thức v bằng S h nhân h phẩy để tìm được biểu thức tốc độ nước dâng."),
    M(r"v = \pi (2Rh - h^2) \cdot h' \Rightarrow h' = \frac{v}{\pi(2Rh - h^2)}",
      "Rút h phẩy từ biểu thức, ta được v chia cho Pi nhân 2 R h trừ h bình."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v}{\pi h(2R - h)} }",
      "Kết luận: Tốc độ nước dâng chậm dần khi nước càng đầy, vì mặt thoáng ngày càng phình to ra tới sát miệng bát."),
  ),
)

# ── BÀI 8 ──────────────────────────────────────────────────────────────
Q("B08","BÀI 8","Hình nón cụt đỉnh nhỏ (Cốc nước)","non_cut",
  P("Mô hình hình học & Công thức tổng quát",
    T("Cốc hình nón cụt, bán kính đáy r_1, bán kính miệng R_2, chiều cao cốc H.",
      "Một chiếc cốc hình nón cụt có đáy nhỏ quay xuống dưới, bán kính đáy r một, bán kính miệng R hai, chiều cao là H."),
    T("Bán kính mặt thoáng x tại chiều cao h thay đổi tuyến tính từ r_1 đến R_2.",
      "Bán kính mặt thoáng của nước tăng dần theo một hàm bậc nhất đối với chiều cao h từ r một tới R hai."),
    M(r"x = r_1 + \frac{R_2 - r_1}{H} \cdot h",
      "Theo định lý Ta-lét mở rộng, bán kính mặt thoáng x bằng r một cộng hiệu R hai trừ r một chia cho H, nhân với h."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Mặt thoáng là một hình tròn có bán kính x.",
      "Vì cốc là nón cụt, mặt thoáng của nước luôn là hình tròn với bán kính x vừa tìm được."),
    M(r"S(h) = \pi x^2 = \pi \left(r_1 + \frac{R_2 - r_1}{H} h\right)^2",
      "Diện tích mặt thoáng S h bằng Pi nhân x bình phương. Thay công thức x vào ta thu được biểu thức bình phương."),
    T("Tương tự hình nón, nhưng diện tích mặt thoáng không bắt đầu từ 0.",
      "Khác với hình nón nhọn, diện tích mặt thoáng ở đây không bằng 0 khi h bằng không vì đáy cốc có kích thước."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Từ công thức v = S(h) * h', tốc độ nước dâng là:",
      "Thay S h vào công thức cơ bản để tìm tốc độ nước dâng h phẩy."),
    M(r"v = \pi \left(r_1 + \frac{R_2 - r_1}{H} h\right)^2 \cdot h'",
      "Ta thiết lập được phương trình lưu lượng bằng diện tích nhân với tốc độ dâng."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v}{\pi \left(r_1 + \frac{R_2 - r_1}{H} h\right)^2} }",
      "Kết luận: Tốc độ nước dâng trong cốc nón cụt giảm dần khi h tăng, tương tự như nón nhọn nhưng giảm theo một hàm bậc hai dịch chuyển."),
  ),
)

# ── BÀI 9 ──────────────────────────────────────────────────────────────
Q("B09","BÀI 9","Tốc độ dâng trong Phễu nón đỉnh hướng lên","non_len",
  P("Mô hình hình học & Công thức tổng quát",
    T("Bình hình nón đặt úp (đỉnh hướng lên), bán kính đáy R, chiều cao H. Bơm nước vào.",
      "Cho một bình chứa hình nón úp ngược, tức là đỉnh hướng lên trên và đáy lớn nằm dưới đất. Bán kính đáy R, chiều cao H."),
    T("Mặt thoáng tròn bán kính r. Phần chóp nón bên trên mặt nước có chiều cao (H - h).",
      "Phần không gian chưa có nước bên trên mặt thoáng là một hình nón nhỏ hơn với chiều cao là H trừ h."),
    M(r"\frac{r}{R} = \frac{H - h}{H} \Rightarrow r = R \left(1 - \frac{h}{H}\right)",
      "Theo định lý Ta-lét cho phần nón phía trên, tỉ số bán kính r chia R bằng H trừ h chia H. Rút r ra ta được công thức bậc nhất."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Mặt thoáng là hình tròn bán kính r thu hẹp dần khi nước dâng.",
      "Khi nước càng dâng lên cao, bán kính mặt thoáng r càng thu nhỏ lại."),
    M(r"S(h) = \pi r^2 = \pi R^2 \left(1 - \frac{h}{H}\right)^2",
      "Diện tích mặt thoáng S h bằng Pi r bình phương. Thay r vào ta được biểu thức chứa bình phương của 1 trừ h chia H."),
    T("Diện tích mặt thoáng S(h) là một hàm bậc hai nghịch biến theo h.",
      "Diện tích mặt thoáng của bình úp tỉ lệ nghịch với bình phương khoảng cách tới đỉnh, diện tích giảm dần về không khi h tiến tới H."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Thay S(h) vào phương trình v = S(h) * h', ta có tốc độ nước dâng:",
      "Sử dụng phương trình lưu lượng, ta tính được tốc độ dâng của nước trong bình nón úp."),
    M(r"v = \pi R^2 \left(1 - \frac{h}{H}\right)^2 \cdot h' \Rightarrow h' = \frac{v}{\pi R^2 \left(1 - \frac{h}{H}\right)^2}",
      "Thay S h vào, rút ra biểu thức tính h phẩy. Ta thấy mẫu số giảm dần khi h tăng."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v H^2}{\pi R^2 (H - h)^2} }",
      "Kết luận: Tốc độ nước dâng tăng dần và tiến ra vô cùng khi mực nước chạm đỉnh nón úp, do diện tích mặt thoáng co lại về 0."),
  ),
)

# ── BÀI 10 ─────────────────────────────────────────────────────────────
Q("B10","BÀI 10","Lăng trụ đứng đáy chữ nhật (Bể bơi)","chu_nhat",
  P("Mô hình hình học & Công thức tổng quát",
    T("Bể bơi hình lăng trụ đứng, đáy là hình chữ nhật kích thước a và b. Lưu lượng v.",
      "Cho một bể bơi hình lăng trụ đứng có đáy là hình chữ nhật kích thước a nhân b. Nước được bơm vào với lưu lượng v."),
    T("Kí hiệu h là mực nước, S(h) là diện tích mặt thoáng tại độ cao h.",
      "Kí hiệu h là mực nước tại thời điểm t. S h là diện tích mặt thoáng."),
    M(r"v = S(h) \cdot h'",
      "Giống như mọi khối hình khác, ta luôn có lưu lượng bơm vào bằng diện tích mặt thoáng nhân với tốc độ dâng h phẩy."),
  ),
  P("Tính diện tích mặt thoáng S(h)",
    T("Vì thành bể thẳng đứng, diện tích mặt thoáng bằng diện tích đáy.",
      "Do thành của bể bơi hoàn toàn thẳng đứng, diện tích mặt thoáng của nước luôn cố định và bằng diện tích đáy hình chữ nhật."),
    M(r"S(h) = a \cdot b \ (\text{const})",
      "Diện tích S h bằng độ dài a nhân chiều rộng b, và hoàn toàn không phụ thuộc vào mực nước h."),
    T("Diện tích mặt thoáng là một hằng số.",
      "Mặt thoáng không bị thu hẹp hay phình to ra, nên diện tích S h là một hằng số cố định."),
  ),
  P("Tính tốc độ nước dâng & Kết luận",
    T("Thế S(h) vào phương trình v = S(h) * h', ta tính được tốc độ nước dâng:",
      "Thế biểu thức diện tích không đổi vào phương trình đạo hàm, ta tính được tốc độ nước dâng nhanh chóng."),
    M(r"v = (a \cdot b) \cdot h' \Rightarrow h' = \frac{v}{a \cdot b}",
      "Lưu lượng v bằng a nhân b nhân với h phẩy. Rút h phẩy bằng v chia cho tích a nhân b."),
    M(r"\boxed{ v_{\text{dang}} = h' = \frac{v}{ab} }",
      "Kết luận: Tốc độ nước dâng trong bể chữ nhật là hoàn toàn đồng đều và không thay đổi theo thời gian. Mực nước tăng tuyến tính."),
  ),
)


# ─────────────── CHỌN BÀI ───────────────
selected = [les for les in LESSONS if not CHON_BAI or les["id"] in CHON_BAI]
if not selected:
    raise RuntimeError("Không tìm thấy bài nào khớp CHON_BAI=" + str(CHON_BAI))
for i, les in enumerate(selected, 1):
    les["order"] = i
    les["total"] = len(selected)

# ─────────────── BƯỚC 2: GIỌNG ĐỌC ───────────────
print("\nBƯỚC 2/5 — Tạo giọng Nam và căn thời lượng.")

try:
    import nest_asyncio; nest_asyncio.apply()
except ImportError:
    pass
import edge_tts

async def make_mp3(text, path):
    comm = edge_tts.Communicate(text, GIONG_DOC, rate=TOC_DO)
    await comm.save(str(path))

def is_valid_mp3(p, txt):
    if not p.exists(): return False
    if p.stat().st_size < 1024: return False
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
                           capture_output=True, text=True, check=True)
        d = float(r.stdout.strip())
        # Vietnamese speaking rate: ~15-20 chars/sec. Min bound: 25 chars/sec
        # Allow small texts (like "Bài 1") to be very short, but at least 0.5s
        expected_min = min(0.5, len(txt) / 25.0)
        return d >= expected_min
    except:
        return False

def get_audio(text):
    key = hashlib.md5((GIONG_DOC + TOC_DO + text).encode()).hexdigest()
    mp3 = AUDIO_DIR / (key + ".mp3")
    wav = AUDIO_DIR / (key + ".wav")
    
    if wav.exists() and not is_valid_mp3(wav, text):
        wav.unlink()
    
    if not wav.exists():
        if mp3.exists() and not is_valid_mp3(mp3, text):
            mp3.unlink()
            
        if not mp3.exists():
            for attempt in range(3):
                try:
                    try:
                        asyncio.run(make_mp3(text, mp3))
                    except RuntimeError:
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(make_mp3(text, mp3))
                    if is_valid_mp3(mp3, text):
                        break
                except Exception as e:
                    print(f"Lỗi tải TTS (thử lại lần {attempt+1}): {e}")
                if mp3.exists():
                    mp3.unlink()
                time.sleep(1)
            else:
                raise RuntimeError(f"Lỗi: Không thể tải trọn vẹn âm thanh cho: '{text[:30]}...'")

        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-i", str(mp3),
            "-ar", "44100", "-ac", "2",
            str(wav)
        ], check=True)
    return wav

total_items = sum(1 + len(les["pages"]) for les in selected)
done = 0

for les in selected:
    intro = les["intro"]
    wav = get_audio(intro["voice"])
    intro["audio"] = str(wav); intro["duration"] = probe_dur(wav)
    done += 1
    for pi, page in enumerate(les["pages"]):
        full_text = " ".join(r["voice"] for r in page["rows"])
        wav = get_audio(full_text)
        page["audio"] = str(wav)
        dur = probe_dur(wav)
        total_len = max(1, sum(len(r["voice"]) for r in page["rows"]))
        for ri, row in enumerate(page["rows"]):
            row["duration"] = dur * (len(row["voice"]) / total_len)
        done += 1
        if done % 15 == 0 or done == total_items:
            print(f"  Đã chuẩn bị {done} / {total_items} đoạn lời đọc.")
print(f"  Đã chuẩn bị đủ {total_items} đoạn lời đọc.")

# ─────────────── SCENE SOURCE ───────────────
SCENE_SRC = r'''
from manim import *
from pathlib import Path
import json, math, textwrap
import numpy as np

HERE = Path(__file__).resolve().parent

with open(HERE / "settings.json", encoding="utf-8") as _f:
    SETTINGS = json.load(_f)
with open(HERE / "lessons.json", encoding="utf-8") as _f:
    DATA = json.load(_f)

BG    = "#0b1120"
PANEL = "#0e1d34"
INK   = "#EDF4FF"
MUTED = "#7A9ABF"
BLUE  = "#38BDF8"
CYAN  = "#3ADEC8"
GOLD  = "#FFD700"
GREEN = "#4ADE80"
RED   = "#FF6B6B"
PINK  = "#F472B6"

config.background_color = BG
config.pixel_width  = SETTINGS["width"]
config.pixel_height = SETTINGS["height"]
config.frame_rate   = SETTINGS["fps"]

FONT = "DejaVu Sans"
TMPL = TexTemplate()
TMPL.add_to_preamble(r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{xcolor}")


def txt(s, size=26, color=INK, bold=False):
    return Text(s, font=FONT, font_size=size, color=color,
                weight="BOLD" if bold else "NORMAL",
                disable_ligatures=True, line_spacing=0.8)

def mtx(s, size=30, color=INK):
    return MathTex(s, font_size=size, color=color, tex_template=TMPL)

def fit(mob, w=None, h=None):
    factors = [1.0]
    if w and mob.width  > 0: factors.append(w / mob.width)
    if h and mob.height > 0: factors.append(h / mob.height)
    mob.scale(min(factors)); return mob

def pt(x, y): return np.array([float(x), float(y), 0.0])

def seg(a, b, color=BLUE, sw=3, dashed=False):
    cls = DashedLine if dashed else Line
    return cls(pt(*a), pt(*b), color=color, stroke_width=sw)

def poly(pts, color=BLUE, op=0.16):
    return Polygon(*[pt(*p) for p in pts], color=color,
                   stroke_width=3, fill_color=color, fill_opacity=op)

def arc_mob(cx, cy, r, color=BLUE, sw=2, op=0.1):
    c = Circle(radius=r, color=color, stroke_width=sw,
               fill_color=color, fill_opacity=op)
    c.move_to(pt(cx, cy)); return c


def make_diagram(kind, t=0):
    g = VGroup()
    def pt(x,y): return np.array([x,y,0])
    def ell(x, y, w, h, col, fill=False, o=0.2):
        return Ellipse(width=w, height=h, stroke_color=col, stroke_width=2,
                       fill_color=col if fill else None, fill_opacity=o if fill else 0).move_to(pt(x,y))
    def dash(p1, p2, c=GRAY): return DashedLine(pt(*p1), pt(*p2), dash_length=0.1, color=c, stroke_width=2)
    def seg(p1, p2, c=WHITE): return Line(pt(*p1), pt(*p2), color=c, stroke_width=2)
    def pol(pts, col, o=0.2): return Polygon(*[pt(*p) for p in pts], stroke_width=0, fill_color=col, fill_opacity=o)
    
    h_max = 2.4
    w_max = 2.4
    h_water = 0.4 + 1.6 * t
    
    if kind == "tru_dung":
        w = 2.0; h = h_max; hw = h_water
        wb = pol([(-w/2, 0), (w/2, 0), (w/2, hw), (-w/2, hw)], BLUE, 0.4)
        we = ell(0, hw, w, 0.4, BLUE, True, 0.6)
        we_base = ell(0, 0, w, 0.4, BLUE, True, 0.4)
        g.add(wb, we_base, we)
        g.add(seg((-w/2, 0), (-w/2, h)), seg((w/2, 0), (w/2, h)))
        g.add(ell(0, h, w, 0.4, WHITE, False))
        g.add(Arc(radius=w/2, start_angle=PI, angle=PI, color=WHITE, stroke_width=2).stretch_to_fit_height(0.4).move_to(pt(0,0)))
        g.add(DashedVMobject(Arc(radius=w/2, start_angle=0, angle=PI, color=GRAY, stroke_width=2).stretch_to_fit_height(0.4).move_to(pt(0,0)), num_dashes=15).set_style(stroke_opacity=0.5))
        g.add(DoubleArrow(pt(-w/2-0.5, 0), pt(-w/2-0.5, hw), buff=0, color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.15))
        g.add(txt("h", 18, YELLOW).move_to(pt(-w/2-0.8, hw/2)))
        g.add(txt("v", 22, BLUE_C, True).move_to(pt(0, h+0.8)))
        g.add(Arrow(pt(0, h+0.6), pt(0, hw+0.1), color=BLUE_C, buff=0))
        
    elif kind == "non_xuong":
        h = h_max; R = 1.6; hw = h_water; rw = R * hw / h
        wb = pol([(0,0), (-rw, hw), (rw, hw)], BLUE, 0.4)
        we = ell(0, hw, 2*rw, 0.3 * (rw/R), BLUE, True, 0.6)
        g.add(wb, we)
        g.add(seg((0,0), (-R, h)), seg((0,0), (R, h)))
        g.add(ell(0, h, 2*R, 0.3, WHITE, False))
        g.add(DoubleArrow(pt(-R-0.5, 0), pt(-R-0.5, hw), buff=0, color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.15))
        g.add(txt("h", 18, YELLOW).move_to(pt(-R-0.8, hw/2)))
        g.add(Arrow(pt(0, h+0.6), pt(0, hw+0.1), color=BLUE_C, buff=0))

    elif kind == "khoi_cau":
        R = 1.4; hw = h_water * (2*R / h_max); rw = math.sqrt(abs(2*R*hw - hw**2))
        pts = []
        for a in np.linspace(PI, 2*PI, 30): pts.append((R*math.cos(a), R*math.sin(a)+R))
        for a in np.linspace(0, PI, 30):
            y = R*math.sin(a)+R
            if y <= hw: pts.append((R*math.cos(a), y))
        pts = [(x, y) for x,y in pts if y <= hw]
        if hw < 2*R:
            pts.append((rw, hw)); pts.append((-rw, hw))
        wb = pol(pts, BLUE, 0.4)
        we = ell(0, hw, 2*rw, 0.3*(rw/R) if R>0 else 0.1, BLUE, True, 0.6)
        g.add(wb, we)
        g.add(Circle(radius=R, color=WHITE, stroke_width=2).move_to(pt(0, R)))
        g.add(DashedVMobject(ell(0, R, 2*R, 0.4, GRAY, False), num_dashes=20))
        g.add(DoubleArrow(pt(-R-0.5, 0), pt(-R-0.5, hw), buff=0, color=YELLOW, stroke_width=2, max_tip_length_to_length_ratio=0.15))
        g.add(txt("h", 18, YELLOW).move_to(pt(-R-0.8, hw/2)))
        g.add(Arrow(pt(0, 2*R+0.6), pt(0, hw+0.1), color=BLUE_C, buff=0))

    elif kind == "chop_deu":
        h = h_max; a = 2.0; hw = h_water; aw = a * hw / h
        A = (-a/2 - 0.5, h); B = (a/2 - 0.5, h); C = (a/2 + 0.5, h); D = (-a/2 + 0.5, h)
        Aw = (-aw/2 - 0.5*(hw/h), hw); Bw = (aw/2 - 0.5*(hw/h), hw); Cw = (aw/2 + 0.5*(hw/h), hw); Dw = (-aw/2 + 0.5*(hw/h), hw)
        g.add(pol([(0,0), Aw, Bw, Cw], BLUE, 0.5))
        g.add(pol([Aw, Bw, Cw, Dw], BLUE, 0.7))
        g.add(seg((0,0), A), seg((0,0), B), seg((0,0), C), dash((0,0), D))
        g.add(seg(A,B), seg(B,C), seg(C,D), seg(D,A), dash(D,A))
        g.add(DoubleArrow(pt(-1.8, 0), pt(-1.8, hw), buff=0, color=YELLOW, stroke_width=2))
        g.add(txt("h", 18, YELLOW).move_to(pt(-2.1, hw/2)))
        g.add(Arrow(pt(0, h+0.6), pt(0, hw+0.1), color=BLUE_C, buff=0))
        
    elif kind == "mang_tam_giac":
        L = 2.5; h = h_max; a = 1.6; hw = h_water; aw = a * hw / h
        dy = 0.8
        F0 = (0,0); Fl = (-a/2, h); Fr = (a/2, h)
        B0 = (L, dy); Bl = (L-a/2, h+dy); Br = (L+a/2, h+dy)
        Fw_l = (-aw/2, hw); Fw_r = (aw/2, hw)
        Bw_l = (L-aw/2, hw+dy); Bw_r = (L+aw/2, hw+dy)
        ratio = hw/h; Bw_0 = (L*ratio, dy*ratio)
        g.add(pol([F0, Fw_r, Bw_r, Bw_0], BLUE, 0.4))
        g.add(pol([Fw_l, Fw_r, Bw_r, Bw_l], BLUE, 0.7))
        g.add(seg(F0, Fl), seg(F0, Fr), seg(Fl, Fr), seg(Fr, Br), seg(Fl, Bl), seg(Br, Bl))
        g.add(dash(F0, B0), dash(B0, Bl), dash(B0, Br))
        g.add(Arrow(pt(L/2, h+dy+0.6), pt(L/2, hw+dy/2+0.1), color=BLUE_C, buff=0))
        g.add(DoubleArrow(pt(-a/2-0.4, 0), pt(-a/2-0.4, hw), buff=0, color=YELLOW))
        
    elif kind == "tru_ngang":
        L = 2.2; R = 1.2; hw = h_water * (2*R / h_max); dy = 0.6
        rw = math.sqrt(abs(2*R*hw - hw**2)); h_shift_L = R - hw
        pts_front = []
        for ang in np.linspace(0, 2*PI, 40):
            y = R - R*math.cos(ang); x = R*math.sin(ang)
            if y <= hw: pts_front.append((x, y))
        if len(pts_front) > 1:
            pL = pts_front[0]; pR = pts_front[-1]
            pL_back = (pL[0]+L, pL[1]+dy); pR_back = (pR[0]+L, pR[1]+dy)
            g.add(pol(pts_front, BLUE, 0.5))
            g.add(pol([pL, pR, pR_back, pL_back], BLUE, 0.7))
        g.add(Circle(radius=R, color=WHITE).move_to(pt(0, R)))
        g.add(DashedVMobject(ell(L, R+dy, 2*R, 2*R, WHITE, False), num_dashes=20))
        g.add(seg((0,0), (L, dy)), seg((0, 2*R), (L, 2*R+dy)), seg((R, R), (R+L, R+dy)), seg((-R, R), (-R+L, R+dy)))
        g.add(DoubleArrow(pt(-R-0.4, 0), pt(-R-0.4, hw), buff=0, color=YELLOW))
        
    elif kind == "ban_cau":
        R = 1.6; hw = h_water * (R / h_max); rw = math.sqrt(abs(2*R*hw - hw**2))
        pts = []
        for a in np.linspace(PI, 2*PI, 30): pts.append((R*math.cos(a), R*math.sin(a)+R))
        for a in np.linspace(0, PI, 30):
            y = R*math.sin(a)+R
            if y <= hw: pts.append((R*math.cos(a), y))
        pts = [(x, y) for x,y in pts if y <= hw]
        if hw < R:
            pts.append((rw, hw)); pts.append((-rw, hw))
        g.add(pol(pts, BLUE, 0.5))
        g.add(ell(0, hw, 2*rw, 0.3*(rw/R), BLUE, True, 0.6))
        g.add(Arc(radius=R, start_angle=PI, angle=PI, color=WHITE).move_to(pt(0,R/2)))
        g.add(ell(0, R, 2*R, 0.4, WHITE, False))
        g.add(DoubleArrow(pt(-R-0.5, 0), pt(-R-0.5, hw), buff=0, color=YELLOW))
        
    elif kind == "non_cut":
        h = h_max; r_bot = 0.8; r_top = 1.6; hw = h_water; rw = r_bot + (r_top - r_bot) * hw / h
        g.add(pol([(-r_bot, 0), (r_bot, 0), (rw, hw), (-rw, hw)], BLUE, 0.5))
        g.add(ell(0, hw, 2*rw, 0.3*(rw/r_top), BLUE, True, 0.6))
        g.add(ell(0, 0, 2*r_bot, 0.3*(r_bot/r_top), BLUE, True, 0.4))
        g.add(seg((-r_bot, 0), (-r_top, h)), seg((r_bot, 0), (r_top, h)))
        g.add(ell(0, h, 2*r_top, 0.4, WHITE, False))
        g.add(ell(0, 0, 2*r_bot, 0.3*(r_bot/r_top), WHITE, False))
        g.add(DoubleArrow(pt(-r_top-0.5, 0), pt(-r_top-0.5, hw), buff=0, color=YELLOW))
        
    elif kind == "non_len":
        h = h_max; R = 1.6; hw = h_water; rw = R * (h - hw) / h
        g.add(pol([(-R, 0), (R, 0), (rw, hw), (-rw, hw)], BLUE, 0.5))
        g.add(ell(0, hw, 2*rw, 0.3*(rw/R) if R>0 else 0.1, BLUE, True, 0.6))
        g.add(ell(0, 0, 2*R, 0.3, BLUE, True, 0.4))
        g.add(seg((-R, 0), (0, h)), seg((R, 0), (0, h)))
        g.add(ell(0, 0, 2*R, 0.3, WHITE, False))
        g.add(DoubleArrow(pt(-R-0.5, 0), pt(-R-0.5, hw), buff=0, color=YELLOW))
        
    elif kind == "chu_nhat":
        w = 1.8; d = 1.0; dy = 0.5; dx = 0.8; h = h_max; hw = h_water
        F0 = (-w/2, 0); F1 = (w/2, 0); F2 = (w/2, h); F3 = (-w/2, h)
        B0 = (-w/2+dx, dy); B1 = (w/2+dx, dy); B2 = (w/2+dx, h+dy); B3 = (-w/2+dx, h+dy)
        Fw0 = (-w/2, hw); Fw1 = (w/2, hw)
        Bw0 = (-w/2+dx, hw+dy); Bw1 = (w/2+dx, hw+dy)
        g.add(pol([F0, F1, Fw1, Fw0], BLUE, 0.4))
        g.add(pol([F1, B1, Bw1, Fw1], BLUE, 0.5))
        g.add(pol([Fw0, Fw1, Bw1, Bw0], BLUE, 0.7))
        g.add(seg(F0, F1), seg(F1, F2), seg(F2, F3), seg(F3, F0))
        g.add(seg(F1, B1), seg(B1, B2), seg(F2, B2))
        g.add(seg(F3, B3), seg(B2, B3))
        g.add(dash(F0, B0), dash(B0, B1), dash(B0, B3))
        g.add(DoubleArrow(pt(-w/2-0.4, 0), pt(-w/2-0.4, hw), buff=0, color=YELLOW))
        
    else:
        g.add(txt("Hình minh hoạ", 28, BLUE, True))
        
    g.move_to(ORIGIN); fit(g, w=3.7, h=3.6)
    return g



class LectureBase(Scene):
    lesson = None

    def speak(self, item, anim=None):
        start = float(self.time)
        dur   = float(item["duration"])
        if "audio" in item:
            self.add_sound(item["audio"])
        self.events.append({"start": start, "end": start+dur, "text": item["voice"]})
        reveal = 0.0
        if anim is not None:
            reveal = min(0.6, max(0.25, dur*0.25))
            self.play(anim, run_time=reveal)
        self.wait(max(0.1, dur - reveal))

    def row_mob(self, row):
        if row["kind"] == "math":
            mob = mtx(row["text"], 30)
            if r"\boxed" in row["text"]:
                mob.set_color(GOLD)
        else:
            wrapped = textwrap.fill(row["text"], width=54,
                                    break_long_words=False, break_on_hyphens=False)
            mob = txt(wrapped, 25, INK)
        fit(mob, w=7.7, h=1.14)
        return mob

    def construct(self):
        q = self.lesson
        self.events = []

        top_bar = Rectangle(width=14.3, height=0.09, stroke_width=0,
                              fill_color=BLUE, fill_opacity=1).move_to(UP*3.96)
        section_lbl = txt(q["section"], 18, CYAN, True)
        fit(section_lbl, w=11.5)
        section_lbl.move_to(pt(-6.55, 3.54), aligned_edge=LEFT)
        title_lbl = txt(q["title"], 30, INK, True)
        fit(title_lbl, w=12.9, h=0.54)
        title_lbl.move_to(pt(-6.55, 3.0), aligned_edge=LEFT)
        idx_lbl = txt(f"{q['order']:02d}/{q['total']:02d}", 18, MUTED).move_to(pt(6.22, 3.54))
        lp = RoundedRectangle(width=4.15, height=5.65, corner_radius=0.14,
                               stroke_color="#2A3D5C", stroke_width=1,
                               fill_color=PANEL, fill_opacity=1).move_to(pt(-4.75,-0.34))
        rp = RoundedRectangle(width=8.65, height=5.65, corner_radius=0.14,
                               stroke_color="#2A3D5C", stroke_width=1,
                               fill_color=PANEL, fill_opacity=1).move_to(pt(1.92,-0.34))
        lh = txt("MINH HOẠ HÌNH HỌC", 20, BLUE, True).move_to(pt(-4.75, 2.03))
        note = txt("Hình minh hoạ — không theo tỉ lệ", 15, MUTED)
        fit(note, w=3.7); note.move_to(pt(-4.75, -2.5))
        flow = txt("Mô hình → Hàm số → Tối ưu", 15, CYAN)
        fit(flow, w=3.7); flow.move_to(pt(-4.75, -2.85))
        footer_line = seg((-6.65,-3.38),(6.65,-3.38), "#304665", 1)
        footer_txt  = txt(SETTINGS["teacher"], 22, GOLD, True).move_to(pt(0,-3.69))

        self.add(top_bar, section_lbl, title_lbl, idx_lbl,
                  lp, rp, lh, note, flow, footer_line, footer_txt)

        diagram = make_diagram(q["diagram"], 0)
        diagram.move_to(pt(-4.75, -0.22))
        self.speak(q["intro"], FadeIn(diagram, shift=UP*0.08))

        current = None
        pages   = q["pages"]

        for pi, page in enumerate(pages):
            if current is not None:
                mlist = list(current)
                if mlist:
                    self.play(FadeOut(Group(*mlist)), run_time=0.25)
                self.remove(*mlist)
                self.wait(0.35)

            ph = txt(page["title"], 23, CYAN, True)
            fit(ph, w=7.15, h=0.48)
            ph.move_to(pt(-1.95, 2.03), aligned_edge=LEFT)
            pc = txt(f"{pi+1}/{len(pages)}", 15, MUTED).move_to(pt(5.73, 2.03))
            pd = seg((-1.95, 1.65),(5.83, 1.65), "#304665", 1)
            current = VGroup(ph, pc, pd)
            self.play(FadeIn(current), run_time=0.25)

            if pi == len(pages)-1:
                tgt = make_diagram(q["diagram"], 1)
                tgt.move_to(pt(-4.75, -0.22))
                self.play(Transform(diagram, tgt), run_time=0.9)

            rows = VGroup(*[self.row_mob(row) for row in page["rows"]])
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
            fit(rows, w=7.7, h=4.0)
            rows.move_to(pt(-1.93, 1.28), aligned_edge=UL)

            self.add_sound(page["audio"])
            for data, mob in zip(page["rows"], rows):
                self.speak(data, FadeIn(mob, shift=UP*0.04))
                current.add(mob)
            self.wait(0.55)

        self.wait(1.0)
        mlist = list(self.mobjects)
        if mlist:
            self.play(FadeOut(Group(*mlist)), run_time=0.35)
        self.clear()

        ev_path = HERE / "events" / (q["id"] + ".json")
        ev_path.parent.mkdir(exist_ok=True)
        ev_path.write_text(json.dumps(self.events, ensure_ascii=False, indent=2),
                           encoding="utf-8")


for lesson in DATA:
    cname = "B_" + lesson["id"]
    globals()[cname] = type(cname, (LectureBase,),
                            {"lesson": lesson, "__module__": __name__})
'''

# ─────────────── CHUẨN BỊ THƯ MỤC RENDER ───────────────
settings = {
    "teacher": TEN_THAY, "voice": GIONG_DOC, "rate": TOC_DO,
    "width": CHIEU_RONG, "height": CHIEU_CAO, "fps": FPS,
}
sig = SCENE_SRC + json.dumps(selected, ensure_ascii=False, sort_keys=True) \
               + json.dumps(settings, ensure_ascii=False, sort_keys=True)
render_key = hashlib.sha256(sig.encode()).hexdigest()[:14]

WORK = ROOT / ("render_" + render_key)
WORK.mkdir(exist_ok=True)
(WORK / "events").mkdir(exist_ok=True)
CLIPS = WORK / "clips"; CLIPS.mkdir(exist_ok=True)
MEDIA = WORK / "media"; MEDIA.mkdir(exist_ok=True)

scene_file = WORK / "scene.py"
scene_file.write_text(SCENE_SRC, encoding="utf-8")
(WORK / "lessons.json").write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding="utf-8")
(WORK / "settings.json").write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")

compile(SCENE_SRC, str(scene_file), "exec")  # kiểm tra cú pháp trước

# ─────────────── BƯỚC 3: DỰNG VIDEO ───────────────
print("\nBƯỚC 3/5 — Dựng từng bài bằng Manim.")
print("Thư mục:", WORK)
print("Bài đã dựng sẽ được dùng lại nếu chạy lại trong cùng phiên.\n")

clip_paths, clip_durs = [], []

for idx, lesson in enumerate(selected, 1):
    code    = lesson["id"]
    cname   = "B_" + code
    out_mp4 = CLIPS / (cname + ".mp4")
    ev_file = WORK / "events" / (code + ".json")
    done_mk = WORK / (code + ".done")

    reusable = False
    if out_mp4.exists() and ev_file.exists() and done_mk.exists():
        try: probe_dur(out_mp4); reusable = True
        except: reusable = False

    if reusable:
        print(f"[{idx}/{len(selected)}] Dùng lại: {code} — {lesson['title']}")
    else:
        print(f"[{idx}/{len(selected)}] Đang dựng: {code} — {lesson['title']}")
        out_mp4.unlink(missing_ok=True); done_mk.unlink(missing_ok=True)
        t0 = time.time()
        run_log(
            [sys.executable, "-m", "manim",
             "--renderer", "cairo", "--format", "mp4",
             "--fps", str(FPS), "-r", f"{CHIEU_RONG},{CHIEU_CAO}",
             "--media_dir", str(MEDIA),
             "--progress_bar", "none", "--verbosity", "WARNING",
             "-o", cname, str(scene_file), cname],
            WORK / (f"render_{code}.log"), cwd=WORK,
        )
        candidates = [p for p in MEDIA.rglob(cname + ".mp4")
                      if "partial_movie_files" not in str(p)]
        if not candidates:
            raise RuntimeError("Không tìm thấy video của " + code
                               + "\nXem log: " + str(WORK / f"render_{code}.log"))
        rendered = max(candidates, key=lambda p: p.stat().st_mtime)
        shutil.copy2(rendered, out_mp4)
        if not ev_file.exists():
            raise RuntimeError("Thiếu file sự kiện phụ đề của " + code)
        d = probe_dur(out_mp4)
        done_mk.write_text("OK")
        print(f"    Xong {d/60:.1f} phút video | dựng {(time.time()-t0)/60:.1f} phút.")

    clip_paths.append(out_mp4)
    clip_durs.append(probe_dur(out_mp4))

# ─────────────── BƯỚC 4: GHÉP & XUẤT ───────────────
print("\nBƯỚC 4/5 — Ghép MP4, xuất phụ đề và mục lục.")

concat_txt = WORK / "concat.txt"
concat_txt.write_text("\n".join("file '" + p.as_posix() + "'" for p in clip_paths) + "\n")
joined = WORK / "joined.mp4"
run_log(["ffmpeg", "-y", "-v", "warning",
         "-f", "concat", "-safe", "0", "-i", str(concat_txt),
         "-map", "0:v:0", "-map", "0:a:0",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
         "-movflags", "+faststart", str(joined)],
        WORK / "ffmpeg_concat.log")


def hms(s): n=max(0,int(s)); return f"{n//3600:02d}:{(n%3600)//60:02d}:{n%60:02d}"
def srt_ts(s):
    n=max(0,round(s*1000)); h,r=divmod(n,3600000); m,r=divmod(r,60000); sc,ms=divmod(r,1000)
    return f"{h:02d}:{m:02d}:{sc:02d},{ms:03d}"
def esc(s): return s.replace("\\","\\\\").replace("=","\\=").replace(";","\\;").replace("#","\\#")


meta = [";FFMETADATA1",
        "title=" + esc("Tối ưu Khối Tròn Xoay — " + TEN_THAY),
        "artist=" + esc(TEN_THAY)]
chapters, subtitles, offset = [], [], 0.0

for les, dur in zip(selected, clip_durs):
    ct = les["id"] + " — " + les["title"]
    meta += ["[CHAPTER]","TIMEBASE=1/1000",
             "START="+str(round(offset*1000)),
             "END="+str(round((offset+dur)*1000)),
             "title="+esc(ct)]
    chapters.append(hms(offset) + "  " + ct)
    events = json.loads((WORK/"events"/(les["id"]+".json")).read_text(encoding="utf-8"))
    for ev in events:
        parts = textwrap.wrap(ev["text"], width=86, break_long_words=False)
        weights = [max(1, len(p)) for p in parts]
        tw = sum(weights); spoken = ev["end"]-ev["start"]; used = 0
        for part, w in zip(parts, weights):
            b = offset + ev["start"] + spoken*used/tw; used += w
            subtitles.append((b, offset+ev["start"]+spoken*used/tw, part))
    offset += dur

suffix = "TOAN_BO" if not CHON_BAI else "_".join(CHON_BAI)
meta_file    = WORK / "meta.ffmeta"
final_video  = ROOT / f"MinMax_KhoiTronXoay_{suffix}.mp4"
final_srt    = ROOT / f"PhuDe_{suffix}.srt"
final_chap   = ROOT / f"MucLuc_{suffix}.txt"

meta_file.write_text("\n".join(meta)+"\n", encoding="utf-8")
run_log(["ffmpeg", "-y", "-v", "warning",
         "-i", str(joined), "-f", "ffmetadata", "-i", str(meta_file),
         "-map","0:v:0","-map","0:a:0","-map_metadata","1","-map_chapters","1",
         "-c","copy","-movflags","+faststart", str(final_video)],
        WORK / "ffmpeg_meta.log")

srt_lines = []
for i, (b, e, content) in enumerate(subtitles, 1):
    wrapped = textwrap.fill(content, width=48, break_long_words=False)
    srt_lines.append(f"{i}\n{srt_ts(b)} --> {srt_ts(e)}\n{wrapped}\n")
final_srt.write_text("\n".join(srt_lines), encoding="utf-8")
final_chap.write_text("\n".join(chapters)+"\n", encoding="utf-8")

# ─────────────── BƯỚC 5: HOÀN TẤT ───────────────
total_dur = probe_dur(final_video)
size_mb   = final_video.stat().st_size / 1024**2

print("\nBƯỚC 5/5 — HOÀN TẤT.")
print("=" * 68)
print("Video   :", final_video)
print("Thời lượng:", hms(total_dur))
print("Dung lượng:", f"{size_mb:.1f} MB")
print("Phụ đề :", final_srt)
print("Mục lục:", final_chap)
print("=" * 68)
print("\nMỤC LỤC:")
print("\n".join(chapters))

from IPython.display import display, HTML

try:
    from google.colab import files, output

    def _dl_video():    files.download(str(final_video))
    def _dl_srt():      files.download(str(final_srt))
    def _dl_chap():     files.download(str(final_chap))

    output.register_callback("sang2.video", _dl_video)
    output.register_callback("sang2.srt",   _dl_srt)
    output.register_callback("sang2.chap",  _dl_chap)

    display(HTML("""
    <div style="background:#0e1d34;color:#edf4ff;padding:18px;
        border-radius:12px;font-family:Arial,sans-serif;margin:14px 0;">
      <div style="font-size:20px;color:#FFD700;font-weight:bold;margin-bottom:8px;">
        Thầy Nguyễn Văn Sang — 10 Bài Toán Tốc Độ Nước Dâng
      </div>
      <p style="margin:4px 0 14px">Video đã dựng xong. Chọn tệp cần tải:</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;">
        <button style="padding:11px 18px;background:#2563eb;color:white;
               border:0;border-radius:8px;cursor:pointer;font-size:15px;"
          onclick="google.colab.kernel.invokeFunction('sang2.video',[],{})">
          ▶ Tải video MP4</button>
        <button style="padding:11px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang2.srt',[],{})">
          Tải phụ đề SRT</button>
        <button style="padding:11px 18px;border-radius:8px;cursor:pointer;"
          onclick="google.colab.kernel.invokeFunction('sang2.chap',[],{})">
          Tải mục lục</button>
      </div>
    </div>"""))

    if HIEN_VIDEO:
        try:
            import threading, functools
            from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
            from urllib.parse import quote
            class _H(SimpleHTTPRequestHandler):
                def log_message(self, *a): pass
            handler = functools.partial(_H, directory=str(ROOT))
            srv = ThreadingHTTPServer(("0.0.0.0", 0), handler)
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            port = srv.server_address[1]
            proxy = output.eval_js(f"google.colab.kernel.proxyPort({port})")
            video_url = proxy.rstrip("/") + "/" + quote(final_video.name)
            display(HTML(
                '<video controls preload="metadata" '
                'style="width:100%;max-width:1100px;border-radius:12px;background:#0b1120;" '
                f'src="{video_url}"></video>'))
        except Exception as e:
            print("Không mở được trình xem trước:", e)

except ImportError:
    print("Mở trực tiếp tệp MP4 theo đường dẫn đã in ở trên.")

print("\nQUAN TRỌNG: Tải tệp về máy trước khi kết thúc phiên Colab!")
