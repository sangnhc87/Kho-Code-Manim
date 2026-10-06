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
# 09. TOAN THUC TE PHAN HOA CAO: tham so, bien nguyen,
#     dieu kien ngam, du kien thua, diem gay (FILE NAY)
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
            txt("TOÁN THỰC TẾ PHÂN HÓA CAO – VIDEO 09", 44, GOLD, BOLD),
            txt("Tham số • biến nguyên • điểm gãy • điều kiện ngầm • dữ kiện thừa", 27, CYAN),
            mtx(r"\boxed{\text{model}\;\to\;\text{filter}\;\to\;\text{optimize}\;\to\;\text{interpret}}", 34, GREEN),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.32)
        fit_width(g, 12.0)
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.7)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), run_time=1.0)
        self.narrate(
            "Chào các em. Từ video này chúng ta bước sang chặng phân hóa cao. Đề bài sẽ dài hơn, có nhiều dữ kiện hơn, nhưng mục tiêu không phải tính toán nặng. Điều khó là lọc đúng dữ kiện, nhận ra biến nào phải nguyên, điểm nào là điểm gãy, điều kiện vật lý nào đang ẩn trong lời văn, và tham số nào làm phương án tối ưu thay đổi. Khi mô hình đúng, lời giải thường lại rất gọn.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Năm bộ lọc trước khi đạo hàm", "Đọc đề trước – tính sau", "Mở đầu")
        items = VGroup(
            bullet("Dữ kiện nào chỉ cộng một hằng số và không đổi vị trí tối ưu?", INK, 26, BLUE),
            bullet("Biến có bắt buộc là số nguyên hay bội của một đơn vị nào không?", INK, 26, CYAN),
            bullet("Có ngưỡng làm công thức thay đổi không?", INK, 26, GOLD),
            bullet("Có sức chứa, giới hạn vật lý hoặc điều kiện ngầm nào không?", INK, 26, ORANGE),
            bullet("Sau khi tối ưu liên tục, có phải kiểm tra lại phương án thực tế không?", INK, 26, GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        fit_width(items, 11.7)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT*0.12) for x in items], lag_ratio=0.09), run_time=1.5)
        self.narrate(
            "Trước khi đạo hàm, hãy chạy năm bộ lọc này. Có dữ kiện chỉ làm đồ thị tịnh tiến lên xuống. Có biến buộc phải nguyên. Có ngưỡng làm công thức đổi. Có sức chứa khiến mô hình toán thuần túy không còn phản ánh đúng thực tế. Và cuối cùng, nghiệm đẹp trên giấy chưa chắc là phương án được phép chọn ngoài đời.",
            2.0,
        )

    # ======================================================
    # CASE 1 - FIXED COST / REDUNDANT FOR ARGMIN
    # ======================================================
    def case1_fixed_cost(self):
        self.show_problem(
            "Bài 1 – Dữ kiện có thật nhưng không quyết định phương án",
            [
                "Một kho nhập hàng thành x lô mỗi tháng.",
                mtx(r"C(x)=12+0.5x+\frac{18}{x},\qquad x>0", 39, GOLD),
                "Đơn vị chi phí: triệu đồng.",
                "Số 12 là tiền thuê kho cố định, phải trả dù chọn x thế nào.",
                "Tìm số lô tối ưu và chi phí nhỏ nhất.",
            ],
            "Bài đầu tiên có một dữ kiện rất dễ làm học sinh mất tập trung: tiền thuê kho cố định mười hai triệu đồng. Khoản này là có thật và phải tính khi hỏi chi phí nhỏ nhất, nhưng nó không ảnh hưởng đến việc chọn bao nhiêu lô, vì nó không thay đổi theo x.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 1", "Một hằng số chỉ nâng đồ thị lên, không kéo cực tiểu sang trái hay phải", "1/5")
        ax = Axes(
            x_range=[1,12.5,1], y_range=[14,41,4], x_length=7.2, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":20},
        ).shift(LEFT*2.65+DOWN*0.05)
        labels = ax.get_axis_labels(mtx("x",26),mtx("C",26))
        c12 = ax.plot(lambda x:12+0.5*x+18/x, x_range=[1,12], color=BLUE, stroke_width=4)
        c20 = ax.plot(lambda x:20+0.5*x+18/x, x_range=[1,12], color=PURPLE, stroke_width=3)
        tracker = ValueTracker(2)
        dot = always_redraw(lambda: Dot(ax.c2p(tracker.get_value(),12+0.5*tracker.get_value()+18/tracker.get_value()),radius=0.075,color=GOLD))
        vline = DashedLine(ax.c2p(6,14), ax.c2p(6,30), color=GREEN, dash_length=0.10)
        side = VGroup(
            mtx(r"C'(x)=\frac12-\frac{18}{x^2}", 34, INK),
            mtx(r"C'(x)=0\iff x^2=36", 34, CYAN),
            mtx(r"\boxed{x=6}", 42, GOLD),
        ).arrange(DOWN,buff=0.32).to_edge(RIGHT,buff=0.45).shift(UP*0.55)
        self.play(Create(ax),FadeIn(labels),Create(c12),FadeIn(side),FadeIn(dot),run_time=1.1)
        self.narrate_play(
            "Điểm vàng chạy trên đồ thị chi phí. Ta thấy chi phí giảm rồi tăng và đạt đáy tại x bằng sáu. Đạo hàm cũng xác nhận ngay: một phần hai trừ mười tám trên x bình phương bằng không, nên x bằng sáu.",
            tracker.animate.set_value(10), min_time=4.5,
        )
        self.play(Create(vline),Create(c20),run_time=0.8)
        self.narrate(
            "Bây giờ giả sử tiền thuê kho tăng từ mười hai lên hai mươi triệu. Toàn bộ đồ thị chỉ dịch thẳng lên tám đơn vị. Điểm cực tiểu vẫn nằm tại x bằng sáu. Đây là một kỹ năng đọc dữ kiện: chi phí cố định ảnh hưởng giá trị tối thiểu, nhưng không ảnh hưởng phương án tối ưu nếu nó là bắt buộc trong mọi phương án.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Bài 1", "Tính đúng thứ đề hỏi", "1/5")
        sol = VGroup(
            mtx(r"x_{\mathrm{opt}}=6", 40, GOLD),
            mtx(r"C(6)=12+3+3", 37, INK),
            mtx(r"\boxed{C_{\min}=18}", 43, GREEN),
        ).arrange(DOWN,buff=0.38)
        self.play(FadeIn(sol),run_time=0.8)
        self.narrate(
            "Nếu đề chỉ hỏi số lô tối ưu, số mười hai có thể bỏ qua khi tối ưu. Nhưng khi đề hỏi chi phí nhỏ nhất, ta phải cộng nó trở lại. Tại x bằng sáu, hai phần biến đổi đều bằng ba, nên tổng chi phí là mười tám triệu đồng.",
            1.7,
        )

    # ======================================================
    # CASE 2 - HOTEL PARAMETER + INTEGER + BREAKPOINT
    # ======================================================
    def case2_hotel_parameter(self):
        self.show_problem(
            "Bài 2 – Phí m làm phương án tối ưu nhảy đột ngột",
            [
                "Khách sạn có 80 phòng. Mỗi lần tăng giá 50 nghìn đồng thì giảm 4 phòng thuê.",
                mtx(r"p(x)=0.90+0.05x", 36, CYAN),
                mtx(r"n(x)=80-4x,\qquad x\in\{0,1,\ldots,20\}", 36, CYAN),
                "Chi phí phục vụ mỗi phòng: 0,12 triệu đồng.",
                "Nếu thuê trên 60 phòng, khách sạn phải trả thêm m triệu đồng cho nhân sự.",
                "Tìm phương án tối ưu theo m.",
            ],
            "Bài hai gom ba lớp khó vào cùng một tình huống: x là số nguyên vì mức giá tăng theo từng nấc; có một ngưỡng sáu mươi phòng làm chi phí thay đổi; và tham số m có thể khiến phương án tối ưu nhảy từ một mức giá sang mức giá khác.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 2", "Xây hàm lợi nhuận trước – tối ưu sau", "2/5")
        model = VGroup(
            mtx(r"P_0(x)=(p(x)-0.12)n(x)", 34, INK),
            mtx(r"P_0(x)=(0.78+0.05x)(80-4x)", 34, CYAN),
            mtx(r"P_0(x)=62.4+0.88x-0.20x^2", 38, GOLD),
            mtx(r"n(x)>60\iff x\le4", 35, ORANGE),
            mtx(r"P_m(x)=\begin{cases}P_0(x)-m,&0\le x\le4,\\P_0(x),&5\le x\le20.\end{cases}", 37, GREEN),
        ).arrange(DOWN,buff=0.28)
        fit_width(model,11.7)
        self.play(LaggedStart(*[FadeIn(z) for z in model],lag_ratio=0.10),run_time=1.4)
        self.narrate(
            "Lợi nhuận trước phí bằng giá phòng trừ chi phí phục vụ, rồi nhân số phòng thuê. Rút gọn được parabol sáu mươi hai phẩy bốn cộng không phẩy tám tám x trừ không phẩy hai x bình phương. Nếu số phòng thuê trên sáu mươi, tương đương x không vượt quá bốn, ta trừ thêm m. Từ x bằng năm trở đi thì không còn khoản phí này.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Bài 2", "Biến nguyên: không lấy đỉnh parabol một cách máy móc", "2/5")
        ax = Axes(
            x_range=[0,10.5,1], y_range=[58,65,1], x_length=7.1, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":20},
        ).shift(LEFT*2.65+DOWN*0.05)
        labels = ax.get_axis_labels(mtx("x",26),mtx("P_0",26))
        curve = ax.plot(lambda x:62.4+0.88*x-0.2*x*x, x_range=[0,10], color=BLUE, stroke_width=4)
        int_pts = VGroup(*[
            Dot(ax.c2p(x,62.4+0.88*x-0.2*x*x),radius=0.055,color=CYAN) for x in range(0,11)
        ])
        p2 = Dot(ax.c2p(2,63.36),radius=0.085,color=GOLD)
        p5 = Dot(ax.c2p(5,61.8),radius=0.085,color=GREEN)
        side = VGroup(
            mtx(r"x_V=\frac{0.88}{0.40}=2.2", 34, INK),
            mtx(r"P_0(2)=63.36", 35, GOLD),
            mtx(r"P_0(5)=61.80", 35, GREEN),
        ).arrange(DOWN,buff=0.35).to_edge(RIGHT,buff=0.50).shift(UP*0.35)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(int_pts),FadeIn(side),FadeIn(p2),FadeIn(p5),run_time=1.1)
        self.narrate(
            "Đỉnh liên tục của parabol ở x bằng hai phẩy hai, nhưng x chỉ nhận số nguyên. Trong vùng phải trả phí, phương án tốt nhất là x bằng hai, cho lợi nhuận trước phí sáu mươi ba phẩy ba sáu triệu. Trong vùng không trả phí, vì đỉnh đã nằm bên trái x bằng năm, lợi nhuận giảm dần và phương án tốt nhất là ngay tại biên x bằng năm, được sáu mươi mốt phẩy tám triệu.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Bài 2", "Chỉ còn so sánh hai ứng viên", "2/5")
        compare = VGroup(
            mtx(r"P_m(2)=63.36-m", 39, GOLD),
            mtx(r"P_m(5)=61.80", 39, GREEN),
            mtx(r"63.36-m=61.80", 36, INK),
            mtx(r"\boxed{m=1.56}", 43, CYAN),
        ).arrange(DOWN,buff=0.34)
        self.play(FadeIn(compare),run_time=0.8)
        self.narrate(
            "Sau tất cả phần mô hình hóa, bài toán tham số chỉ còn là so sánh hai con số. Phương án x bằng hai cho sáu mươi ba phẩy ba sáu trừ m. Phương án x bằng năm cho sáu mươi mốt phẩy tám. Hai phương án hòa nhau khi m bằng một phẩy năm sáu triệu đồng.",
            1.7,
        )

        result = VGroup(
            mtx(r"m<1.56:\quad x=2", 34, GOLD),
            mtx(r"m=1.56:\quad x\in\{2,5\}", 34, CYAN),
            mtx(r"m>1.56:\quad x=5", 34, GREEN),
        ).arrange(DOWN,buff=0.30).shift(DOWN*0.15)
        detail = VGroup(
            VGroup(txt("x = 2:",24,GOLD,BOLD),mtx(r"p=1.00,\ n=72",31,GOLD)).arrange(RIGHT,buff=0.18),
            VGroup(txt("x = 5:",24,GREEN,BOLD),mtx(r"p=1.15,\ n=60",31,GREEN)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,buff=0.22).next_to(result,DOWN,buff=0.40)
        self.play(FadeIn(result),FadeIn(detail),run_time=0.9)
        self.narrate(
            "Nếu m nhỏ hơn một phẩy năm sáu, khách sạn chấp nhận trả phí và chọn x bằng hai, tức giá một triệu đồng, dự kiến thuê bảy mươi hai phòng. Nếu m lớn hơn ngưỡng, phương án tối ưu nhảy sang x bằng năm, giá một phẩy mười lăm triệu và đúng sáu mươi phòng. Tại ngưỡng, cả hai phương án cùng tối ưu.",
            2.0,
        )

    # ======================================================
    # CASE 3 - INTEGER FLEET
    # ======================================================
    def case3_integer_fleet(self):
        self.show_problem(
            "Bài 3 – Tối ưu đội xe nhưng nghiệm phải nguyên",
            [
                "Xe nhỏ chở 2 tấn, chi phí 1,8 triệu đồng/chuyến.",
                "Xe lớn chở 5 tấn, chi phí 3,7 triệu đồng/chuyến.",
                "Cần chở ít nhất 18 tấn, dùng không quá 6 xe và phải có ít nhất 1 xe nhỏ.",
                mtx(r"x,y\in\mathbb Z_{\ge0}", 36, CYAN),
                "Tìm phương án có chi phí nhỏ nhất.",
            ],
            "Bài ba là tối ưu tuyến tính nhưng có điều kiện nguyên. Nếu bỏ chữ nguyên, ta đang giải một bài khác. Cách an toàn là vẽ miền điều kiện rồi chỉ xét các điểm lưới nguyên thực sự khả thi.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 3", "Miền thực liên tục và các phương án nguyên là hai lớp khác nhau", "3/5")
        ax = Axes(
            x_range=[0,6.5,1], y_range=[0,6.5,1], x_length=6.2, y_length=5.4,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":20},
        ).shift(LEFT*2.75+DOWN*0.05)
        labels = ax.get_axis_labels(mtx("x",26),mtx("y",26))
        cap = ax.plot(lambda x:(18-2*x)/5, x_range=[0,6], color=ORANGE, stroke_width=3)
        num = ax.plot(lambda x:6-x, x_range=[0,6], color=BLUE, stroke_width=3)
        x1 = DashedLine(ax.c2p(1,0),ax.c2p(1,6),color=GREEN,dash_length=0.10)
        feasible = []
        for x in range(1,7):
            for y in range(0,7):
                if 2*x+5*y >= 18 and x+y <= 6:
                    feasible.append((x,y))
        dots = VGroup(*[Dot(ax.c2p(x,y),radius=0.065,color=CYAN) for x,y in feasible])
        opt = Dot(ax.c2p(4,2),radius=0.095,color=GOLD)
        side = VGroup(
            mtx(r"2x+5y\ge18", 33, ORANGE),
            mtx(r"x+y\le6", 33, BLUE),
            mtx(r"x\ge1", 33, GREEN),
            mtx(r"C=1.8x+3.7y", 36, GOLD),
        ).arrange(DOWN,buff=0.27).to_edge(RIGHT,buff=0.50).shift(UP*0.5)
        self.play(Create(ax),FadeIn(labels),Create(cap),Create(num),Create(x1),FadeIn(side),run_time=1.1)
        self.play(LaggedStart(*[FadeIn(d,scale=1.4) for d in dots],lag_ratio=0.08),run_time=1.5)
        self.play(FadeIn(opt,scale=1.5),run_time=0.5)
        self.narrate(
            "Hai đường biên tạo miền khả thi liên tục, nhưng phương án thật chỉ là các chấm lưới màu xanh. Ta không cần thử mọi cặp số. Với mỗi số xe lớn, chỉ cần chọn số xe nhỏ tối thiểu để đủ tải và kiểm tra giới hạn sáu xe.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Bài 3", "Quét theo số xe lớn", "3/5")
        rows = VGroup(
            mtx(r"y=2:\ x=4\Rightarrow C=14.6", 34, GOLD),
            mtx(r"y=3:\ x\ge2\Rightarrow C_{\min}=14.7", 34, INK),
            mtx(r"y=4:\ x\ge1\Rightarrow C_{\min}=16.6", 34, INK),
            mtx(r"y=5:\ x=1\Rightarrow C=20.3", 34, INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.12) for r in rows],lag_ratio=0.10),run_time=1.2)
        ans = VGroup(
            mtx(r"\boxed{(x,y)=(4,2)}", 42, GREEN),
            mtx(r"\boxed{C_{\min}=14.6}", 42, GOLD),
        ).arrange(DOWN,buff=0.30).next_to(rows,DOWN,buff=0.45)
        self.play(FadeIn(ans),run_time=0.7)
        self.narrate(
            "Với hai xe lớn, ta cần đúng bốn xe nhỏ và tổng cộng sáu xe, chi phí mười bốn phẩy sáu triệu. Với ba xe lớn, chỉ cần hai xe nhỏ nhưng chi phí đã là mười bốn phẩy bảy. Các trường hợp sau còn cao hơn. Vậy phương án tối ưu là bốn xe nhỏ và hai xe lớn.",
            1.8,
        )

    # ======================================================
    # CASE 4 - CAPACITY / HIDDEN PHYSICAL CONDITION
    # ======================================================
    def case4_tank_capacity(self):
        self.show_problem(
            "Bài 4 – Mô hình toán phải tôn trọng sức chứa vật lý",
            [
                "Một bể đang có 300 lít và chỉ chứa tối đa 500 lít.",
                mtx(r"r(t)=80-10t,\qquad 0\le t\le8", 39, GOLD),
                "r(t) là lưu lượng ròng, đơn vị lít/phút.",
                "Khi bể đầy, nước dư bị tràn ra ngoài.",
                "Hỏi bể đầy lần đầu lúc nào và đến phút thứ 8 đã tràn bao nhiêu lít?",
            ],
            "Bài bốn có một điều kiện vật lý rất dễ bị quên: bể không thể chứa quá năm trăm lít. Nếu chỉ lấy nguyên hàm và tin vào công thức, ta sẽ nhận được thể tích lớn hơn sức chứa, tức mô hình toán đã đi ra ngoài thực tế.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 4", "Trước khi chạm sức chứa: tích phân như bình thường", "4/5")
        raw = VGroup(
            mtx(r"V_*(t)=300+\int_0^t(80-10u)\,du", 37, INK),
            mtx(r"V_*(t)=300+80t-5t^2", 40, CYAN),
            mtx(r"V_*(t)=500", 36, GOLD),
            mtx(r"t^2-16t+40=0", 36, INK),
            mtx(r"t=8\pm2\sqrt6", 36, INK),
            mtx(r"\boxed{t_1=8-2\sqrt6\approx3.10}", 40, GOLD),
        ).arrange(DOWN,buff=0.24)
        fit_width(raw,11.4)
        self.play(LaggedStart(*[FadeIn(z) for z in raw],lag_ratio=0.10),run_time=1.5)
        self.narrate(
            "Nếu tạm thời bỏ giới hạn sức chứa, thể tích dự đoán là ba trăm cộng tám mươi t trừ năm t bình phương. Cho biểu thức này bằng năm trăm, ta được hai nghiệm tám cộng trừ hai căn sáu. Trong khoảng từ không đến tám chỉ nhận nghiệm khoảng ba phẩy mười phút. Đó là thời điểm bể đầy lần đầu.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài 4", "Đường cong dự đoán và thể tích thực tế không còn trùng nhau", "4/5")
        ax = Axes(
            x_range=[0,8.5,1], y_range=[280,650,50], x_length=7.3, y_length=5.1,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":18},
        ).shift(LEFT*2.65+DOWN*0.05)
        labels = ax.get_axis_labels(mtx("t",26),mtx("V",26))
        raw_curve = ax.plot(lambda t:300+80*t-5*t*t,x_range=[0,8],color=ORANGE,stroke_width=3)
        cap = Line(ax.c2p(0,500),ax.c2p(8,500),color=RED,stroke_width=3)
        t1 = 8-2*math.sqrt(6)
        actual1 = ax.plot(lambda t:300+80*t-5*t*t,x_range=[0,t1],color=GREEN,stroke_width=5)
        actual2 = Line(ax.c2p(t1,500),ax.c2p(8,500),color=GREEN,stroke_width=5)
        tracker = ValueTracker(0)
        def actual_v(t):
            return min(500,300+80*t-5*t*t)
        dot = always_redraw(lambda: Dot(ax.c2p(tracker.get_value(),actual_v(tracker.get_value())),radius=0.075,color=GOLD))
        side = VGroup(
            txt("Cam: mô hình chưa xét sức chứa",23,ORANGE),
            txt("Xanh: thể tích thật trong bể",23,GREEN),
            mtx(r"V(t)=\min\{500,V_*(t)\}",34,CYAN),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.35).shift(UP*0.50)
        self.play(Create(ax),FadeIn(labels),Create(raw_curve),Create(cap),Create(actual1),Create(actual2),FadeIn(side),FadeIn(dot),run_time=1.2)
        self.narrate_play(
            "Đường màu cam là thể tích mà công thức tích lũy dự đoán nếu bể vô hạn. Đường xanh mới là thể tích thật. Sau khoảng ba phẩy mười phút, bể đã đầy nên thể tích không thể tăng thêm; phần nước tiếp tục đi vào sẽ tràn ra ngoài.",
            tracker.animate.set_value(8), min_time=5.0,
        )

        self.clear_stage(); self.add_header_footer("Bài 4", "Lượng tràn = phần mô hình vượt quá sức chứa", "4/5")
        spill = VGroup(
            mtx(r"V_*(8)=300+80\cdot8-5\cdot8^2", 36, INK),
            mtx(r"V_*(8)=620", 38, CYAN),
            mtx(r"\text{spill}=620-500", 37, INK),
            mtx(r"\boxed{120\ \mathrm{L}}", 45, GOLD),
        ).arrange(DOWN,buff=0.34)
        self.play(FadeIn(spill),run_time=0.8)
        self.narrate(
            "Đến phút thứ tám, mô hình không giới hạn dự đoán sáu trăm hai mươi lít. Bể chỉ giữ được năm trăm, nên một trăm hai mươi lít là lượng đã tràn. Bài này cho thấy điều kiện sức chứa không phải chi tiết phụ; nó thay đổi chính hàm mô tả thực tế.",
            1.8,
        )

    # ======================================================
    # CASE 5 - FINAL EXAM STYLE COMBINED
    # ======================================================
    def case5_final_challenge(self):
        self.show_problem(
            "Bài 5 – Trả lời ngắn: sức chứa + giá rời rạc + chi phí cố định",
            [
                "Một buổi biểu diễn có tối đa 200 ghế.",
                mtx(r"d(p)=320-2p", 37, CYAN),
                "p tính bằng nghìn đồng và chỉ được chọn theo bội của 5.",
                "Chi phí phục vụ: 30 nghìn đồng/khách; phí thuê địa điểm cố định: 4 triệu đồng.",
                mtx(r"40\le p\le120,\qquad p\in5\mathbb Z", 36, GOLD),
                "Tìm giá vé tối ưu và lợi nhuận lớn nhất.",
            ],
            "Bài cuối tổng hợp bốn ý: nhu cầu phụ thuộc giá, sức chứa tạo một điểm gãy, giá bán là biến rời rạc theo bội của năm, và phí thuê địa điểm là chi phí cố định. Nếu không lọc từng lớp, biểu thức rất dễ bị viết sai.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Bước 1: sức chứa tạo hàm nhiều công thức", "5/5")
        model = VGroup(
            mtx(r"q(p)=\min\{200,320-2p\}", 39, GOLD),
            mtx(r"320-2p=200\iff p=60", 36, CYAN),
            mtx(r"P(p)=(p-30)q(p)-4000", 36, INK),
            mtx(r"P(p)=\begin{cases}200p-10000,&40\le p\le60,\\-2p^2+380p-13600,&60<p\le120.\end{cases}", 35, GREEN),
        ).arrange(DOWN,buff=0.30)
        fit_width(model,11.8)
        self.play(LaggedStart(*[FadeIn(z) for z in model],lag_ratio=0.10),run_time=1.4)
        self.narrate(
            "Số khách thật bằng giá trị nhỏ hơn giữa hai trăm ghế và nhu cầu. Điểm chuyển cơ chế là p bằng sáu mươi. Lợi nhuận bằng lãi trên mỗi khách nhân số khách rồi trừ bốn triệu phí cố định. Vì vậy ta được một hàm hai công thức.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Bước 2: tối ưu từng nhánh, rồi kiểm tra tính rời rạc", "5/5")
        ax = Axes(
            x_range=[40,121,10], y_range=[0,5.2,1], x_length=7.2, y_length=5.0,
            tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":18},
            y_axis_config={"include_numbers":True,"font_size":18},
        ).shift(LEFT*2.65+DOWN*0.05)
        labels = ax.get_axis_labels(mtx("p",26),mtx("P",26))
        # Profit in million VND for plotting: divide thousand-VND expression by 1000
        c1 = ax.plot(lambda p:(200*p-10000)/1000,x_range=[40,60],color=BLUE,stroke_width=4)
        c2 = ax.plot(lambda p:(-2*p*p+380*p-13600)/1000,x_range=[60,120],color=GREEN,stroke_width=4)
        grid_pts = VGroup(*[
            Dot(ax.c2p(p, ((200*p-10000) if p<=60 else (-2*p*p+380*p-13600))/1000), radius=0.045, color=CYAN)
            for p in range(40,121,5)
        ])
        best = Dot(ax.c2p(95,4.45),radius=0.09,color=GOLD)
        side = VGroup(
            mtx(r"P_1'(p)=200>0", 32, BLUE),
            mtx(r"P_2'(p)=-4p+380", 32, GREEN),
            mtx(r"P_2'(p)=0\iff p=95", 34, GOLD),
            mtx(r"95\in5\mathbb Z", 32, CYAN),
        ).arrange(DOWN,buff=0.27).to_edge(RIGHT,buff=0.42).shift(UP*0.45)
        self.play(Create(ax),FadeIn(labels),Create(c1),Create(c2),FadeIn(grid_pts),FadeIn(side),FadeIn(best),run_time=1.1)
        self.narrate(
            "Nhánh thứ nhất tăng nên tốt nhất tại p bằng sáu mươi. Nhánh thứ hai là parabol quay xuống, có đỉnh tại p bằng chín mươi lăm. Điều rất thuận lợi là chín mươi lăm đúng là một bội của năm, nên không cần làm tròn hay so sánh hai mức giá lân cận.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Bước 3: diễn giải phương án tối ưu", "5/5")
        sol = VGroup(
            mtx(r"p_{\mathrm{opt}}=95", 40, GOLD),
            mtx(r"q(95)=320-2\cdot95=130", 37, CYAN),
            mtx(r"P(95)=-2\cdot95^2+380\cdot95-13600", 34, INK),
            mtx(r"\boxed{P_{\max}=4450\ \text{(thousand)}}", 39, GREEN),
        ).arrange(DOWN,buff=0.31)
        fit_width(sol,11.2)
        self.play(FadeIn(sol),run_time=0.8)
        self.narrate(
            "Giá tối ưu là chín mươi lăm nghìn đồng. Khi đó nhu cầu là một trăm ba mươi khách, chưa chạm sức chứa hai trăm ghế, và lợi nhuận lớn nhất là bốn triệu bốn trăm năm mươi nghìn đồng. Phí thuê bốn triệu ảnh hưởng con số lợi nhuận nhưng không xuất hiện trong đạo hàm vì đó là một hằng số bắt buộc.",
            1.9,
        )

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_stage(); self.add_header_footer("Bản đồ tư duy của bài phân hóa cao", "Không tính nhiều hơn – lọc tốt hơn", "Tổng kết")
        g = VGroup(
            VGroup(mtx(r"C(x)+K",34,BLUE),txt("→ hằng số K không đổi vị trí cực trị",25,INK)).arrange(RIGHT,buff=0.23),
            VGroup(mtx(r"x\in\mathbb Z",34,CYAN),txt("→ kiểm tra nghiệm rời rạc",25,INK)).arrange(RIGHT,buff=0.23),
            VGroup(mtx(r"f(x)=\begin{cases}\cdots\end{cases}",34,GOLD),txt("→ luôn kiểm tra điểm gãy",25,INK)).arrange(RIGHT,buff=0.23),
            VGroup(mtx(r"\min\{M,g(x)\}",34,ORANGE),txt("→ sức chứa tạo điều kiện vật lý",25,INK)).arrange(RIGHT,buff=0.23),
            VGroup(mtx(r"P_m(x)",34,PURPLE),txt("→ so sánh ứng viên để tìm ngưỡng m",25,INK)).arrange(RIGHT,buff=0.23),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34)
        fit_width(g,11.8)
        for row in g:
            self.play(FadeIn(row,shift=RIGHT*0.12),run_time=0.34)
        self.narrate(
            "Năm bài hôm nay tạo thành năm mẫu rất quan trọng. Hằng số cố định không đổi vị trí cực trị. Biến nguyên buộc ta quay lại phương án rời rạc. Hàm nhiều công thức bắt buộc kiểm tra điểm gãy. Sức chứa tạo hàm min hoặc max. Và với tham số m, cách nhanh nhất thường là rút bài toán xuống còn vài ứng viên rồi so sánh trực tiếp.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài tự luyện ngắn", "Tự lọc dữ kiện trước khi bấm máy", "Tổng kết")
        q = VGroup(
            txt("Một dịch vụ có chi phí",27,INK),
            mtx(r"C(x)=8+\frac{50}{x}+2x,\qquad x>0",40,GOLD),
            txt("Trong đó 8 triệu là phí cố định bắt buộc.",25,MUTED),
            txt("Hãy tìm x tối ưu mà không cần đạo hàm phần hằng số.",26,INK),
        ).arrange(DOWN,buff=0.28)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate(
            "Bài tự luyện: chi phí bằng tám cộng năm mươi trên x cộng hai x. Tám triệu là phí cố định. Hãy bỏ nó sang một bên khi tìm phương án tối ưu, rồi dùng đạo hàm hoặc bất đẳng thức để tìm x.",
            1.5,
        )
        ans = VGroup(
            mtx(r"-\frac{50}{x^2}+2=0",34,INK),
            mtx(r"x^2=25",34,CYAN),
            mtx(r"\boxed{x=5}",42,GOLD),
        ).arrange(DOWN,buff=0.26).to_edge(RIGHT,buff=0.65).shift(DOWN*0.5)
        self.play(FadeIn(ans),run_time=0.7)
        self.narrate(
            "Đạo hàm phần biến đổi cho âm năm mươi trên x bình phương cộng hai bằng không. Suy ra x bằng năm. Nếu cần chi phí nhỏ nhất mới cộng lại tám triệu. Đây chính là tinh thần của cả video: không mang mọi dữ kiện vào phép tính nếu chúng không quyết định lựa chọn.",
            1.7,
        )

        self.clear_stage()
        end = VGroup(
            txt("VIDEO 09 – CHẶNG PHÂN HÓA CAO", 42, GOLD, BOLD),
            txt("Đề dài hơn nhưng lời giải có thể ngắn hơn", 28, CYAN),
            mtx(r"\boxed{\text{read}\to\text{filter}\to\text{model}\to\text{compare}}", 35, GREEN),
            txt("Video 10: bài thực tế có tham số và điều kiện tối ưu thay đổi theo miền.", 24, MUTED),
            txt(TEN_THAY, 21, MUTED),
        ).arrange(DOWN,buff=0.31)
        fit_width(end,12.0)
        self.play(FadeIn(end),run_time=0.9)
        self.narrate(
            "Video chín mở đầu chặng phân hóa cao. Các em hãy nhớ: đề dài không đồng nghĩa với phép tính dài. Khó nhất thường là nhận ra dữ kiện nào quyết định cấu trúc bài toán. Video tiếp theo sẽ đi sâu hơn vào tham số, nơi chính phương án tối ưu thay đổi khi tham số đi qua các ngưỡng khác nhau.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.case1_fixed_cost()
        self.case2_hotel_parameter()
        self.case3_integer_fleet()
        self.case4_tank_capacity()
        self.case5_final_challenge()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_09_phan_hoa_cao_1080p"
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
    master_wav = ROOT / "master_narration_video09.wav"
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
