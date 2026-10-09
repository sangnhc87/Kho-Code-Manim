from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time

# ==========================================================
# SERIES ROADMAP - TOAN THUC TE / CT GDPT 2018
# 01. Mo hinh hoa + toi uu mot bien
# 02. Ham nhieu cong thuc: gia, phi, nguong, suc chua
# 03. Toc do - thoi gian - nang suat - chi phi
# 04. Doc do thi thuc te + dao ham + Dung/Sai
# 05. Tich phan trong bai toan thuc te
# 06. Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke tu du lieu
# 08. Tong hop Dung/Sai + tra loi ngan
# 09. Toan thuc te phan hoa cao: tham so, bien nguyen, dieu kien ngam
# 10. THAM SO LAM PHUONG AN TOI UU THAY DOI (FILE NAY)
# 11. Mo hinh nguoc: suy tham so tu du lieu quan sat
#
# Nguyen tac series:
# - Uu tien bai toan thuc te, ham tuong minh, mo hinh hoa.
# - Han che toi da ham an.
# - MathTex chi chua toan; tieng Viet dung Text.
# - Co do thi/hinh dong phuc vu lap luan.
# - File standalone 100%, khong phu thuoc module noi bo.
# ==========================================================

TEN_THAY = "Thầy Nguyễn Văn Sang"
GIONG_DOC = "vi-VN-NamMinhNeural"
TOC_DO_DOC = "-5%"
PITCH = "+0Hz"

FINAL_WIDTH = 1920
FINAL_HEIGHT = 1080
FINAL_FPS = 30

config.pixel_width = FINAL_WIDTH
config.pixel_height = FINAL_HEIGHT
config.frame_rate = FINAL_FPS
config.background_color = "#0B1120"

ROOT = Path.cwd()
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR = ROOT / "media"

BG = "#0B1120"
PANEL = "#0E1D34"
INK = "#EDF4FF"
MUTED = "#7A9ABF"
BLUE = "#38BDF8"
CYAN = "#3ADEC8"
GOLD = "#FFD700"
GREEN = "#4ADE80"
RED = "#FF6B6B"
ORANGE = "#FB923C"
PURPLE = "#C084FC"

TMPL = TexTemplate()
TMPL.add_to_preamble(r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{xcolor}
""")


def mtx(s, size=38, color=INK):
    return MathTex(s, font_size=size, color=color, tex_template=TMPL)


def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


def fit_width(mob, width=12.2):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def make_panel(width=12.2, height=5.3):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        fill_color=PANEL,
        fill_opacity=0.90,
        stroke_color=MUTED,
        stroke_opacity=0.22,
        stroke_width=1.5,
    )


def title_block(title, subtitle=None):
    t = fit_width(txt(title, 38, INK, BOLD), 12.0).to_edge(UP, buff=0.25)
    if subtitle:
        s = fit_width(txt(subtitle, 23, MUTED), 11.7).next_to(t, DOWN, buff=0.10)
        return VGroup(t, s)
    return VGroup(t)


def footer(page_text=""):
    left = txt(TEN_THAY, 19, MUTED)
    right = txt(page_text, 19, MUTED)
    left.to_edge(DOWN, buff=0.18).to_edge(LEFT, buff=0.38)
    right.to_edge(DOWN, buff=0.18).to_edge(RIGHT, buff=0.38)
    return VGroup(left, right)


def bullet(text, color=INK, size=27, dot_color=BLUE):
    d = Dot(radius=0.055, color=dot_color)
    t = txt(text, size, color)
    return VGroup(d, t).arrange(RIGHT, buff=0.18, aligned_edge=UP)


# ==========================================================
# TTS + MASTER AUDIO
# ==========================================================
def _audio_key(text):
    payload = json.dumps(
        {"text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC, "pitch": PITCH, "engine": "edge-tts"},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ], text=True).strip()
    return float(out)


def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError(f"Audio khong hop le: {path}")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], check=True)


def create_audio(text: str) -> Path:
    out = AUDIO_DIR / f"{_audio_key(text)}.mp3"
    if out.exists():
        try:
            validate_audio(out)
            return out
        except Exception:
            out.unlink(missing_ok=True)

    last_err = None
    for attempt in range(1, 4):
        try:
            code = (
                "import asyncio\n"
                "import edge_tts\n"
                f"text={text!r}\n"
                f"out={str(out)!r}\n"
                f"voice={GIONG_DOC!r}\n"
                f"rate={TOC_DO_DOC!r}\n"
                f"pitch={PITCH!r}\n"
                "async def main():\n"
                "    c=edge_tts.Communicate(text=text,voice=voice,rate=rate,pitch=pitch)\n"
                "    await c.save(out)\n"
                "asyncio.run(main())\n"
            )
            subprocess.run([sys.executable, "-c", code], check=True)
            validate_audio(out)
            return out
        except Exception as e:
            last_err = e
            out.unlink(missing_ok=True)
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"Edge TTS that bai sau 3 lan: {last_err}")


def build_master_audio(events, video_duration, out_wav: Path):
    if not events:
        raise RuntimeError("Khong co narration nao de ghep.")
    inputs, filters, labels = [], [], []
    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]adelay={ms}|{ms},aresample=48000[a{i}]")
        labels.append(f"[a{i}]")
    filter_complex = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[m]", "-ar", "48000", "-ac", "2",
        "-t", f"{video_duration:.3f}", str(out_wav)
    ], check=True)


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(out)
    ], check=True)


# ==========================================================
# LESSON
# ==========================================================
class SangLesson(Scene):
    def setup(self):
        self.audio_events = []

    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def narrate_play(self, text, *animations, min_time=1.0, rate_func=linear):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.play(*animations, run_time=max(dur, min_time), rate_func=rate_func)
        return dur

    def clear_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.42)

    def add_header_footer(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, content, voice, progress):
        self.clear_stage()
        self.add_header_footer(title, "BÀI TOÁN", progress)
        panel = make_panel(12.3, 5.15).shift(DOWN * 0.08)
        self.play(FadeIn(panel), run_time=0.45)
        group = VGroup()
        for item in content:
            if isinstance(item, Mobject):
                mob = item
            else:
                mob = fit_width(txt(item, 27, INK), 11.1)
            group.add(mob)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.27).move_to(panel)
        fit_width(group, 11.15)
        for mob in group:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.28)
        self.narrate(voice, 1.8)


    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("TOÁN THỰC TẾ PHÂN HÓA CAO – VIDEO 10", 43, GOLD, BOLD),
            txt("Tham số làm phương án tối ưu thay đổi", 31, CYAN),
            mtx(r"\boxed{m\longmapsto x^*(m)}", 42, GREEN),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.32)
        fit_width(g, 12.0)
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.7)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), run_time=1.0)
        self.narrate(
            "Chào các em. Video mười đi sâu vào một ý rất quan trọng của toán thực tế có tham số. Khi tham số m thay đổi, phương án tối ưu không nhất thiết thay đổi trơn tru. Có lúc nó đi liên tục, có lúc bị chặn ở biên, và đặc biệt khi biến phải nguyên thì phương án có thể nhảy đột ngột từ một giá trị sang giá trị khác. Mục tiêu hôm nay là học cách tìm các ngưỡng làm thay đổi quyết định.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Tư duy cốt lõi", "Không tối ưu lại từ đầu cho từng m", "Mở đầu")
        items = VGroup(
            VGroup(mtx(r"F(x,m)", 34, BLUE), txt("→ hàm mục tiêu phụ thuộc tham số", 25, INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"x^*(m)", 34, GOLD), txt("→ phương án tốt nhất ứng với m", 25, INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"m=m_0", 34, ORANGE), txt("→ ngưỡng khi hai ứng viên hòa nhau", 25, INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"x\in\mathbb Z", 34, CYAN), txt("→ phương án có thể nhảy theo bậc thang", 25, INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"x\in[a,b]", 34, GREEN), txt("→ nghiệm tự do có thể bị chặn tại biên", 25, INK)).arrange(RIGHT,buff=0.22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        fit_width(items, 11.8)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT*0.12) for r in items], lag_ratio=0.08), run_time=1.5)
        self.narrate(
            "Thay vì thay từng m rồi giải lại, ta tìm cấu trúc của nghiệm tối ưu. Nếu chỉ còn vài ứng viên, hãy so sánh trực tiếp. Nếu biến nguyên, tìm các điểm mà hai giá trị liên tiếp cho cùng lợi ích. Nếu nghiệm liên tục, hãy tìm nghiệm tự do rồi kiểm tra nó có nằm trong miền cho phép hay bị ép vào biên.",
            1.9,
        )

    # ======================================================
    # CASE 1 - THREE COMPETING PLANS
    # ======================================================
    def case1_three_plans(self):
        self.show_problem(
            "Bài 1 – Ba phương án cạnh tranh theo m",
            [
                "Một doanh nghiệp có ba phương án vận hành A, B, C.",
                "Lợi nhuận dự kiến, đơn vị triệu đồng, phụ thuộc chi phí thị trường m:",
                mtx(r"P_A(m)=72-4m", 36, GOLD),
                mtx(r"P_B(m)=66-2m", 36, CYAN),
                mtx(r"P_C(m)=56-m", 36, GREEN),
                "Với m không âm, hãy chọn phương án có lợi nhuận lớn nhất.",
            ],
            "Bài đầu tiên rất gọn nhưng chứa tư duy quan trọng nhất. Ta không cần đạo hàm. Mỗi phương án cho một đường thẳng theo m. Phương án tối ưu tại một giá trị m chính là đường nằm cao nhất. Các ngưỡng xảy ra khi hai đường ứng viên cắt nhau.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 1", "Nhìn phương án tối ưu như đường bao phía trên", "1/5")
        ax = Axes(
            x_range=[0,14,2], y_range=[35,75,5], x_length=7.0, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":20},
        ).shift(LEFT*2.6+DOWN*0.05)
        labels=ax.get_axis_labels(mtx("m",26),mtx("P",26))
        a=ax.plot(lambda m:72-4*m,x_range=[0,9],color=GOLD,stroke_width=4)
        b=ax.plot(lambda m:66-2*m,x_range=[0,14],color=CYAN,stroke_width=4)
        c=ax.plot(lambda m:56-m,x_range=[0,14],color=GREEN,stroke_width=4)
        tr=ValueTracker(0.5)
        vline=always_redraw(lambda: DashedLine(ax.c2p(tr.get_value(),35),ax.c2p(tr.get_value(),75),color=ORANGE,dash_length=0.10))
        dots=always_redraw(lambda: VGroup(
            Dot(ax.c2p(tr.get_value(),72-4*tr.get_value()),radius=0.055,color=GOLD),
            Dot(ax.c2p(tr.get_value(),66-2*tr.get_value()),radius=0.055,color=CYAN),
            Dot(ax.c2p(tr.get_value(),56-tr.get_value()),radius=0.055,color=GREEN),
        ))
        side=VGroup(
            mtx(r"P_A=P_B\iff m=3",32,GOLD),
            mtx(r"P_B=P_C\iff m=10",32,CYAN),
            mtx(r"\boxed{A\to B\to C}",39,GREEN),
        ).arrange(DOWN,buff=0.35).to_edge(RIGHT,buff=0.45).shift(UP*0.4)
        self.play(Create(ax),FadeIn(labels),Create(a),Create(b),Create(c),FadeIn(side),Create(vline),FadeIn(dots),run_time=1.2)
        self.narrate_play(
            "Khi m còn nhỏ, đường vàng của phương án A nằm cao nhất. Tăng m dần, ta đi qua ngưỡng m bằng ba, sau đó phương án B vượt lên. Đến m bằng mười, phương án C bắt đầu tốt hơn B. Điều cần nhìn là đường bao phía trên của ba đường lợi nhuận.",
            tr.animate.set_value(13), min_time=5.0,
        )

        self.clear_stage(); self.add_header_footer("Bài 1", "Kết luận theo miền tham số", "1/5")
        concl=VGroup(
            mtx(r"0\le m<3:\quad A",36,GOLD),
            mtx(r"m=3:\quad A,B",36,ORANGE),
            mtx(r"3<m<10:\quad B",36,CYAN),
            mtx(r"m=10:\quad B,C",36,ORANGE),
            mtx(r"m>10:\quad C",36,GREEN),
        ).arrange(DOWN,buff=0.28)
        self.play(FadeIn(concl),run_time=0.8)
        self.narrate(
            "Kết luận phải ghi cả trường hợp hòa. Trước ba chọn A. Tại ba, A và B cùng tối ưu. Từ ba đến mười chọn B. Tại mười, B và C hòa nhau. Sau mười chọn C. Đây là mẫu cơ bản nhất: tham số thay đổi làm phương án tối ưu chuyển từ ứng viên này sang ứng viên khác tại các giao điểm.",
            1.8,
        )

    # ======================================================
    # CASE 2 - CAPACITY PARAMETER
    # ======================================================
    def case2_capacity(self):
        self.show_problem(
            "Bài 2 – Sức chứa m quyết định mức giá tối ưu",
            [
                "Một sự kiện bán vé với giá p nghìn đồng.",
                mtx(r"d(p)=300-2p", 38, CYAN),
                "Địa điểm chỉ có m chỗ, với m dương.",
                mtx(r"0\le p\le150", 34, INK),
                mtx(r"q(p)=\min\{m,300-2p\}", 38, GOLD),
                mtx(r"R(p)=p\,q(p)", 38, GREEN),
                "Tìm giá vé tối ưu theo sức chứa m.",
            ],
            "Bài hai cho thấy một tham số vật lý là sức chứa có thể làm thay đổi hẳn chiến lược giá. Khi sức chứa nhỏ, doanh nghiệp cố tăng giá đến đúng lúc nhu cầu vừa bằng số ghế. Khi sức chứa đủ lớn, giới hạn vật lý không còn chi phối và ta quay về cực đại tự nhiên của đường cầu.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 2", "Điểm gãy thay đổi theo m", "2/5")
        model=VGroup(
            mtx(r"300-2p=m",34,INK),
            mtx(r"p_b=\frac{300-m}{2}",39,ORANGE),
            mtx(r"R(p)=\begin{cases}mp,&p\le p_b,\\p(300-2p),&p\ge p_b.\end{cases}",38,GOLD),
            mtx(r"p_0=75",39,CYAN),
        ).arrange(DOWN,buff=0.34)
        fit_width(model,11.2)
        self.play(FadeIn(model),run_time=0.8)
        self.narrate(
            "Điểm gãy xuất hiện khi nhu cầu đúng bằng sức chứa: ba trăm trừ hai p bằng m. Suy ra giá tại điểm gãy là ba trăm trừ m chia hai. Trước điểm này, bán hết m ghế nên doanh thu bằng m nhân p và tăng theo p. Sau điểm này, doanh thu bằng p nhân ba trăm trừ hai p, là một parabol có đỉnh tại p bằng bảy mươi lăm.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Bài 2", "Cho m chạy: giá tối ưu cũng chạy", "2/5")
        ax=Axes(
            x_range=[40,120,10], y_range=[0,12500,2000], x_length=7.2, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":19},
            y_axis_config={"include_numbers":True,"font_size":18},
        ).shift(LEFT*2.6+DOWN*0.05)
        labels=ax.get_axis_labels(mtx("p",25),mtx("R",25))
        mt=ValueTracker(80)
        def rev(p):
            m=mt.get_value()
            return p*min(m,max(0,300-2*p))
        curve=always_redraw(lambda: ax.plot(lambda p:rev(p),x_range=[40,120],color=BLUE,stroke_width=4))
        def pstar():
            m=mt.get_value()
            return (300-m)/2 if m<150 else 75
        opt=always_redraw(lambda: Dot(ax.c2p(pstar(),rev(pstar())),radius=0.085,color=GOLD))
        breakpoint=always_redraw(lambda: DashedLine(ax.c2p((300-mt.get_value())/2,0),ax.c2p((300-mt.get_value())/2,12500),color=ORANGE,dash_length=0.10))
        m_num=DecimalNumber(mt.get_value(),num_decimal_places=0,font_size=30,color=ORANGE)
        m_num.add_updater(lambda d:d.set_value(mt.get_value()))
        lab=VGroup(mtx(r"m=",27,ORANGE),m_num).arrange(RIGHT,buff=0.08).to_edge(RIGHT,buff=0.75).shift(UP*2.0)
        side=VGroup(
            mtx(r"m<150:\quad p^*(m)=\frac{300-m}{2}",32,GOLD),
            mtx(r"m\ge150:\quad p^*(m)=75",32,GREEN),
        ).arrange(DOWN,buff=0.35).to_edge(RIGHT,buff=0.32).shift(DOWN*0.6)
        fit_width(side,5.2)
        self.play(Create(ax),FadeIn(labels),FadeIn(curve),FadeIn(opt),Create(breakpoint),FadeIn(lab),FadeIn(side),run_time=1.1)
        self.narrate_play(
            "Khi sức chứa tăng từ tám mươi lên một trăm tám mươi, điểm gãy màu cam dịch sang trái. Điểm vàng là giá tối ưu. Ban đầu giá tối ưu đi cùng điểm gãy. Nhưng khi m đạt một trăm năm mươi, điểm gãy chạm đúng đỉnh tự nhiên p bằng bảy mươi lăm. Từ đó trở đi, tăng thêm sức chứa không còn làm giá tối ưu giảm nữa.",
            mt.animate.set_value(180), min_time=5.5,
        )

        self.clear_stage(); self.add_header_footer("Bài 2", "Công thức tối ưu theo sức chứa", "2/5")
        ans=VGroup(
            mtx(r"\boxed{p^*(m)=\begin{cases}\dfrac{300-m}{2},&0<m\le150,\\[4pt]75,&m\ge150.\end{cases}}",42,GOLD),
            txt("Sức chứa nhỏ: tăng ghế → hạ giá tối ưu.",25,CYAN),
            txt("Đủ 150 ghế: giới hạn sức chứa hết tác dụng lên giá tối ưu.",25,GREEN),
        ).arrange(DOWN,buff=0.34)
        fit_width(ans,11.8)
        self.play(FadeIn(ans),run_time=0.8)
        self.narrate(
            "Ta thu được một hàm tối ưu từng đoạn. Khi sức chứa chưa đến một trăm năm mươi, giá tối ưu là ba trăm trừ m chia hai. Khi sức chứa từ một trăm năm mươi trở lên, giá tối ưu giữ nguyên ở bảy mươi lăm. Đây là ví dụ điển hình của nghiệm tối ưu bị điều kiện thực tế chặn lại.",
            1.8,
        )

    # ======================================================
    # CASE 3 - INTEGER STAIRCASE
    # ======================================================
    def case3_integer_staircase(self):
        self.show_problem(
            "Bài 3 – Biến nguyên làm nghiệm tối ưu nhảy theo bậc thang",
            [
                "Một chiến dịch chọn x gói quảng cáo, mỗi gói là một đơn vị nguyên.",
                mtx(r"x\in\{0,1,2,3,4,5,6\}", 36, CYAN),
                mtx(r"R(x)=120x-10x^2", 37, GOLD),
                "Chi phí cho mỗi gói là m triệu đồng.",
                mtx(r"P_m(x)=(120-m)x-10x^2", 38, GREEN),
                "Tìm số gói tối ưu theo m.",
            ],
            "Bài ba là nơi tính rời rạc xuất hiện rất rõ. Nếu x được phép liên tục, nghiệm tối ưu sẽ trượt đều theo m. Nhưng x chỉ có thể là số nguyên từ không đến sáu. Vì vậy phương án tối ưu giữ nguyên trên một khoảng rồi nhảy sang số nguyên kế tiếp.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 3", "So sánh hai phương án liên tiếp", "3/5")
        deriv=VGroup(
            mtx(r"P_m(x+1)-P_m(x)",35,INK),
            mtx(r"=110-m-20x",38,CYAN),
            mtx(r"P_m(x+1)=P_m(x)\iff m=110-20x",38,GOLD),
            mtx(r"110,90,70,50,30,10",37,ORANGE),
        ).arrange(DOWN,buff=0.34)
        self.play(FadeIn(deriv),run_time=0.8)
        self.narrate(
            "Thay vì tính lợi nhuận của bảy phương án cho từng m, ta so sánh hai phương án liên tiếp. Hiệu P tại x cộng một trừ P tại x bằng một trăm mười trừ m trừ hai mươi x. Hai phương án hòa nhau khi m bằng một trăm mười trừ hai mươi x. Các ngưỡng xuất hiện đều cách nhau hai mươi.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Bài 3", "Các điểm nguyên chạy – phương án vàng nhảy bậc", "3/5")
        ax=Axes(
            x_range=[0,6.5,1], y_range=[-400,410,100], x_length=7.1, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":18},
        ).shift(LEFT*2.55+DOWN*0.05)
        labels=ax.get_axis_labels(mtx("x",25),mtx("P_m",25))
        mt=ValueTracker(0)
        def pv(x): return (120-mt.get_value())*x-10*x*x
        dots=always_redraw(lambda: VGroup(*[Dot(ax.c2p(x,pv(x)),radius=0.06,color=CYAN) for x in range(7)]))
        def bestx():
            vals=[pv(x) for x in range(7)]
            return max(range(7),key=lambda x:vals[x])
        best=always_redraw(lambda: Dot(ax.c2p(bestx(),pv(bestx())),radius=0.10,color=GOLD))
        stems=always_redraw(lambda: VGroup(*[Line(ax.c2p(x,0),ax.c2p(x,pv(x)),color=MUTED,stroke_width=1.5) for x in range(7)]))
        m_num=DecimalNumber(mt.get_value(),num_decimal_places=0,font_size=29,color=ORANGE)
        m_num.add_updater(lambda d:d.set_value(mt.get_value()))
        x_num=DecimalNumber(bestx(),num_decimal_places=0,font_size=34,color=GOLD)
        x_num.add_updater(lambda d:d.set_value(bestx()))
        mlab=VGroup(
            VGroup(mtx(r"m=",27,ORANGE),m_num).arrange(RIGHT,buff=0.08),
            VGroup(mtx(r"x^*=",31,GOLD),x_num).arrange(RIGHT,buff=0.08),
        ).arrange(DOWN,buff=0.18).to_edge(RIGHT,buff=0.75).shift(UP*1.4)
        self.play(Create(ax),FadeIn(labels),FadeIn(stems),FadeIn(dots),FadeIn(best),FadeIn(mlab),run_time=1.0)
        self.narrate_play(
            "Cho m tăng từ không đến một trăm hai mươi. Các chấm xanh là lợi nhuận của từng số gói nguyên. Chấm vàng luôn đánh dấu phương án tốt nhất. Em sẽ thấy nó không trượt liên tục mà nhảy từ sáu xuống năm, rồi bốn, ba, hai, một và cuối cùng về không khi chi phí mỗi gói quá cao.",
            mt.animate.set_value(120), min_time=6.2,
        )

        self.clear_stage(); self.add_header_footer("Bài 3", "Hàm quyết định dạng bậc thang", "3/5")
        ans=VGroup(
            mtx(r"0\le m<10:\ x^*=6",31,GOLD),
            mtx(r"10<m<30:\ x^*=5",31,INK),
            mtx(r"30<m<50:\ x^*=4",31,INK),
            mtx(r"50<m<70:\ x^*=3",31,INK),
            mtx(r"70<m<90:\ x^*=2",31,INK),
            mtx(r"90<m<110:\ x^*=1",31,INK),
            mtx(r"m>110:\ x^*=0",31,INK),
        ).arrange(DOWN,buff=0.20)
        self.play(FadeIn(ans),run_time=0.8)
        self.narrate(
            "Trên các khoảng giữa hai ngưỡng, số gói tối ưu là hằng số. Đúng tại một ngưỡng như m bằng năm mươi, hai số nguyên liên tiếp có thể cùng tối ưu. Đây là lý do bài có biến nguyên thường tạo ra một hàm quyết định dạng bậc thang.",
            1.7,
        )

    # ======================================================
    # CASE 4 - PIECEWISE PENALTY
    # ======================================================
    def case4_penalty(self):
        self.show_problem(
            "Bài 4 – Phí tăng ca m làm cực đại dính vào điểm gãy",
            [
                "Một xưởng chọn mức sản lượng q, với q không âm.",
                mtx(r"P_0(q)=-q^2+12q", 38, GOLD),
                "Nếu sản lượng vượt 4 đơn vị, mỗi đơn vị vượt phải chịu thêm m đơn vị chi phí.",
                mtx(r"P_m(q)=P_0(q)-m\max\{0,q-4\}", 38, CYAN),
                "Tìm sản lượng tối ưu theo m không âm.",
            ],
            "Bài bốn có một điểm gãy vật lý tại q bằng bốn. Trước ngưỡng không có phí tăng ca. Sau ngưỡng, độ dốc lợi nhuận giảm thêm m. Khi m đủ lớn, điểm cực đại không còn nằm bên phải mà bị kéo đúng về điểm gãy.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 4", "Tách hai miền trước khi đạo hàm", "4/5")
        model=VGroup(
            mtx(r"P_m(q)=\begin{cases}-q^2+12q,&0\le q\le4,\\-q^2+(12-m)q+4m,&q\ge4,\end{cases}",38,GOLD),
            mtx(r"P_1'(q)=-2q+12>0\quad(0\le q\le4)",32,CYAN),
            mtx(r"P_2'(q)=-2q+12-m",34,INK),
            mtx(r"q_0=\frac{12-m}{2}=6-\frac m2",37,GREEN),
        ).arrange(DOWN,buff=0.32)
        fit_width(model,11.6)
        self.play(FadeIn(model),run_time=0.9)
        self.narrate(
            "Trên đoạn từ không đến bốn, lợi nhuận tăng nên ứng viên tốt nhất của nhánh đầu là q bằng bốn. Sau bốn, đạo hàm bằng âm hai q cộng mười hai trừ m. Nghiệm tự do của nhánh sau là sáu trừ m chia hai. Nhưng nghiệm này chỉ hợp lệ nếu nó còn nằm bên phải bốn.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài 4", "Khi nghiệm tự do chạm điểm gãy", "4/5")
        ax=Axes(
            x_range=[0,8,1], y_range=[0,38,5], x_length=7.0, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":18},
        ).shift(LEFT*2.6+DOWN*0.05)
        labels=ax.get_axis_labels(mtx("q",25),mtx("P_m",25))
        mt=ValueTracker(0)
        def prof(q): return -q*q+12*q-mt.get_value()*max(0,q-4)
        curve=always_redraw(lambda: ax.plot(lambda q:prof(q),x_range=[0,8],color=BLUE,stroke_width=4))
        def qstar(): return max(4,6-mt.get_value()/2)
        dot=always_redraw(lambda: Dot(ax.c2p(qstar(),prof(qstar())),radius=0.09,color=GOLD))
        kink=DashedLine(ax.c2p(4,0),ax.c2p(4,38),color=ORANGE,dash_length=0.10)
        m_num=DecimalNumber(mt.get_value(),num_decimal_places=1,font_size=28,color=ORANGE)
        m_num.add_updater(lambda d:d.set_value(mt.get_value()))
        q_num=DecimalNumber(qstar(),num_decimal_places=1,font_size=32,color=GOLD)
        q_num.add_updater(lambda d:d.set_value(qstar()))
        lab=VGroup(
            VGroup(mtx(r"m=",26,ORANGE),m_num).arrange(RIGHT,buff=0.08),
            VGroup(mtx(r"q^*=",29,GOLD),q_num).arrange(RIGHT,buff=0.08),
        ).arrange(DOWN,buff=0.18).to_edge(RIGHT,buff=0.65).shift(UP*1.2)
        self.play(Create(ax),FadeIn(labels),FadeIn(curve),Create(kink),FadeIn(dot),FadeIn(lab),run_time=1.0)
        self.narrate_play(
            "Khi m bằng không, cực đại ở q bằng sáu. Tăng m, chấm vàng trượt dần sang trái. Đến m bằng bốn, nghiệm tự do chạm đúng q bằng bốn. Sau đó dù m tiếp tục tăng, phương án tối ưu không thể đi sang trái theo công thức nhánh hai; nó bị giữ lại tại điểm gãy q bằng bốn.",
            mt.animate.set_value(7), min_time=5.5,
        )

        self.clear_stage(); self.add_header_footer("Bài 4", "Nghiệm tối ưu bị kẹp bởi điều kiện", "4/5")
        ans=VGroup(
            mtx(r"6-\frac m2\ge4\iff m\le4",35,INK),
            mtx(r"\boxed{q^*(m)=\begin{cases}6-\dfrac m2,&0\le m\le4,\\4,&m\ge4.\end{cases}}",42,GOLD),
        ).arrange(DOWN,buff=0.42)
        fit_width(ans,11.5)
        self.play(FadeIn(ans),run_time=0.8)
        self.narrate(
            "Điều kiện sáu trừ m chia hai lớn hơn hoặc bằng bốn tương đương m không vượt quá bốn. Vì vậy trước ngưỡng bốn, nghiệm tối ưu giảm tuyến tính theo m. Từ m bằng bốn trở đi, nghiệm tối ưu bị khóa tại q bằng bốn. Đây là mô hình rất thường gặp khi có phí tăng ca, thuế vượt ngưỡng hoặc chi phí phụ sau một mức sản lượng.",
            1.8,
        )

    # ======================================================
    # CASE 5 - SPEED WITH PARAMETER AND BOUNDS
    # ======================================================
    def case5_speed_bounds(self):
        self.show_problem(
            "Bài 5 – Nghiệm tự do đẹp nhưng có thể bị chặn ở biên",
            [
                "Một xe giao hàng chọn tốc độ v trong giới hạn kỹ thuật:",
                mtx(r"60\le v\le180", 38, CYAN),
                "Chi phí quy đổi gồm thời gian và thành phần tăng theo tốc độ:",
                mtx(r"C_m(v)=\frac{360}{v}+\frac{m}{1000}v", 40, GOLD),
                mtx(r"m>0", 34, GREEN),
                "Tìm tốc độ tối ưu theo m.",
            ],
            "Bài cuối là một mẫu rất đẹp của tối ưu có miền giới hạn. Nếu bỏ giới hạn tốc độ, đạo hàm cho một nghiệm căn thức. Nhưng khi tham số m quá nhỏ hoặc quá lớn, nghiệm tự do đi ra ngoài đoạn cho phép. Khi đó đáp án phải nằm ở một trong hai biên kỹ thuật.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Nghiệm tự do trước – chiếu vào miền sau", "5/5")
        deriv=VGroup(
            mtx(r"C_m'(v)=-\frac{360}{v^2}+\frac{m}{1000}",35,INK),
            mtx(r"C_m'(v)=0\iff v_0=\sqrt{\frac{360000}{m}}",39,GOLD),
            mtx(r"v_0=180\iff m=\frac{100}{9}",34,CYAN),
            mtx(r"v_0=60\iff m=100",34,GREEN),
        ).arrange(DOWN,buff=0.33)
        self.play(FadeIn(deriv),run_time=0.8)
        self.narrate(
            "Đạo hàm cho nghiệm tự do v không bằng căn của ba trăm sáu mươi nghìn chia m. Ta tìm thời điểm nghiệm này chạm hai biên. Nó bằng một trăm tám mươi khi m bằng một trăm chia chín, và bằng sáu mươi khi m bằng một trăm. Hai giá trị này chia trục tham số thành ba miền.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Tốc độ tối ưu chạy rồi dính vào hai biên", "5/5")
        ax=Axes(
            x_range=[5,125,20], y_range=[50,190,20], x_length=7.2, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":19},
            y_axis_config={"include_numbers":True,"font_size":19},
        ).shift(LEFT*2.6+DOWN*0.05)
        labels=ax.get_axis_labels(mtx("m",25),mtx(r"v^*",25))
        curve1=ax.plot(lambda m:180,x_range=[5,100/9],color=GOLD,stroke_width=4)
        curve2=ax.plot(lambda m:math.sqrt(360000/m),x_range=[100/9,100],color=BLUE,stroke_width=4)
        curve3=ax.plot(lambda m:60,x_range=[100,125],color=GREEN,stroke_width=4)
        mt=ValueTracker(6)
        def vstar():
            m=mt.get_value(); v=math.sqrt(360000/m)
            return min(180,max(60,v))
        dot=always_redraw(lambda: Dot(ax.c2p(mt.get_value(),vstar()),radius=0.09,color=ORANGE))
        m_num=DecimalNumber(mt.get_value(),num_decimal_places=0,font_size=28,color=ORANGE)
        m_num.add_updater(lambda d:d.set_value(mt.get_value()))
        v_num=DecimalNumber(vstar(),num_decimal_places=1,font_size=31,color=GOLD)
        v_num.add_updater(lambda d:d.set_value(vstar()))
        lab=VGroup(
            VGroup(mtx(r"m=",26,ORANGE),m_num).arrange(RIGHT,buff=0.08),
            VGroup(mtx(r"v^*=",29,GOLD),v_num).arrange(RIGHT,buff=0.08),
        ).arrange(DOWN,buff=0.18).to_edge(RIGHT,buff=0.65).shift(UP*1.3)
        self.play(Create(ax),FadeIn(labels),Create(curve1),Create(curve2),Create(curve3),FadeIn(dot),FadeIn(lab),run_time=1.1)
        self.narrate_play(
            "Điểm cam cho thấy tốc độ tối ưu theo m. Khi m rất nhỏ, nghiệm tự do muốn vượt quá một trăm tám mươi nên tốc độ bị chặn ở biên trên. Trong miền giữa, tốc độ giảm theo căn một trên m. Khi m đạt một trăm, nghiệm chạm sáu mươi và sau đó bị giữ ở biên dưới.",
            mt.animate.set_value(120), min_time=5.5,
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Ba miền tham số – ba cơ chế tối ưu", "5/5")
        ans=VGroup(
            mtx(r"\boxed{v^*(m)=\begin{cases}180,&0<m\le\dfrac{100}{9},\\[5pt]\sqrt{\dfrac{360000}{m}},&\dfrac{100}{9}<m<100,\\[7pt]60,&m\ge100.\end{cases}}",40,GOLD),
            txt("Biên trên → nghiệm nội → biên dưới",27,CYAN,BOLD),
        ).arrange(DOWN,buff=0.38)
        fit_width(ans,11.6)
        self.play(FadeIn(ans),run_time=0.9)
        self.narrate(
            "Kết quả có ba miền rất rõ: biên trên, nghiệm nội, rồi biên dưới. Một lỗi phổ biến là chỉ viết căn ba trăm sáu mươi nghìn chia m rồi dừng lại. Trong bài thực tế, nghiệm toán học phải được kiểm tra lại với miền vận hành cho phép.",
            1.7,
        )

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_stage(); self.add_header_footer("Bản đồ tư duy Video 10", "Tìm ngưỡng thay đổi quyết định", "Tổng kết")
        g=VGroup(
            VGroup(mtx(r"F_i(m)=F_j(m)",34,GOLD),txt("→ ngưỡng đổi giữa hai phương án",25,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"x\in\mathbb Z",34,CYAN),txt("→ nghiệm tối ưu dạng bậc thang",25,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"\min\{m,d(p)\}",34,ORANGE),txt("→ tham số sức chứa tạo điểm gãy",25,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"\max\{0,x-a\}",34,PURPLE),txt("→ phí chỉ xuất hiện sau ngưỡng",25,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"x_0(m)\notin[a,b]",34,GREEN),txt("→ nghiệm thực tế nằm ở biên",25,INK)).arrange(RIGHT,buff=0.24),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34)
        fit_width(g,11.8)
        for row in g:self.play(FadeIn(row,shift=RIGHT*0.12),run_time=0.34)
        self.narrate(
            "Năm bài hôm nay cho năm cơ chế thay đổi nghiệm tối ưu. Hai phương án đổi chỗ khi giá trị của chúng bằng nhau. Biến nguyên tạo bậc thang. Sức chứa tạo điểm gãy di động. Phí sau ngưỡng có thể kéo cực đại về đúng điểm gãy. Và cuối cùng, nghiệm tự do có thể đi ra ngoài miền thực tế nên phải bị chặn ở biên.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài tự luyện", "Một câu ngắn để kiểm tra tư duy tham số", "Tổng kết")
        q=VGroup(
            txt("Hai phương án có chi phí",27,INK),
            mtx(r"C_A(m)=40+3m",38,GOLD),
            mtx(r"C_B(m)=52+m",38,CYAN),
            txt("Tìm miền m không âm để chọn phương án A rẻ hơn.",26,INK),
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate(
            "Bài tự luyện: phương án A có chi phí bốn mươi cộng ba m, phương án B là năm mươi hai cộng m. Hãy tìm ngưỡng hai phương án bằng nhau rồi xác định phía nào A rẻ hơn.",
            1.4,
        )
        ans=VGroup(
            mtx(r"40+3m<52+m",35,INK),
            mtx(r"2m<12",35,CYAN),
            mtx(r"\boxed{0\le m<6}",42,GOLD),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.65).shift(DOWN*0.5)
        self.play(FadeIn(ans),run_time=0.7)
        self.narrate(
            "Ta được hai m nhỏ hơn mười hai, nên m nhỏ hơn sáu. Vì m không âm, phương án A rẻ hơn khi m nằm từ không đến nhỏ hơn sáu. Tại m bằng sáu, hai phương án hòa nhau.",
            1.4,
        )

        self.clear_stage()
        end=VGroup(
            txt("VIDEO 10 – THAM SỐ & QUYẾT ĐỊNH TỐI ƯU",41,GOLD,BOLD),
            mtx(r"\boxed{m\ \text{changes}\ \Longrightarrow\ x^*(m)\ \text{may change regime}}",33,GREEN),
            txt("Video 11: dữ liệu thừa – mô hình ngược – suy tham số từ quan sát thực tế.",24,MUTED),
            txt(TEN_THAY,21,MUTED),
        ).arrange(DOWN,buff=0.32)
        fit_width(end,12.0)
        self.play(FadeIn(end),run_time=0.9)
        self.narrate(
            "Chốt lại: tham số không chỉ thay đổi giá trị cực đại hay cực tiểu. Nó có thể thay đổi chính quyết định tối ưu và cơ chế của bài toán. Khi gặp đề có m, hãy hỏi: các ứng viên nào đang cạnh tranh, ngưỡng nào làm chúng hòa nhau, và nghiệm tự do có còn thỏa điều kiện thực tế hay không. Video tiếp theo sẽ chuyển sang bài toán ngược: từ dữ liệu quan sát thực tế suy ra tham số của mô hình.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.case1_three_plans()
        self.case2_capacity()
        self.case3_integer_staircase()
        self.case4_penalty()
        self.case5_speed_bounds()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_10_tham_so_quyet_dinh_toi_uu_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_video10.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    print("\n============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


if __name__ == "__main__":
    render_full()
