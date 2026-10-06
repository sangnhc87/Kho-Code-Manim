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
# 02. Ham nhieu cong thuc: gia, phi, nguong, suc chua (FILE NAY)
# 03. Toc do - thoi gian - nang suat - chi phi
# 04. Doc do thi thuc te + dao ham + Dung/Sai
# 05. Tich phan: quang duong - the tich - luong tich luy
# 06. Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke tu du lieu
# 08. Tong hop Dung/Sai + tra loi ngan kieu TN THPT
#
# Nguyen tac dai han:
# - Uu tien mo hinh thuc te, ham tuong minh, do thi dong.
# - Han che toi da ham an.
# - Moi bai: de bai -> mo hinh -> diem gay -> giai tung mien -> so sanh -> ket luan.
# ==========================================================

# ==========================================================
# SYSTEM CONFIG
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

# ==========================================================
# COLORS
# ==========================================================
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

# ==========================================================
# LATEX / TEXT HELPERS
# ==========================================================
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
        self.add_header_footer(title, "BÀI TOÁN THỰC TẾ", progress)
        panel = make_panel(12.3, 5.15).shift(DOWN * 0.08)
        self.play(FadeIn(panel), run_time=0.45)
        group = VGroup()
        for item in content:
            if isinstance(item, Mobject):
                mob = item
            else:
                mob = fit_width(txt(item, 27, INK), 11.1)
            group.add(mob)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(panel)
        fit_width(group, 11.15)
        for mob in group:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.28)
        self.narrate(voice, 1.8)

    def make_axes(self, xr, yr, xlen=6.8, ylen=5.2, shift=LEFT*2.7, x_numbers=True, y_numbers=True):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2},
            x_axis_config={"include_numbers": x_numbers, "font_size": 20},
            y_axis_config={"include_numbers": y_numbers, "font_size": 20},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 27), mtx("y", 27))
        return ax, labels

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("TOÁN THỰC TẾ – HÀM SỐ, PHẦN 02", 45, GOLD, BOLD),
            txt("HÀM NHIỀU CÔNG THỨC: GIÁ – PHÍ – NGƯỠNG – SỨC CHỨA", 34, INK, BOLD),
            mtx(r"f(x)=\begin{cases}f_1(x),&x\in I_1\\f_2(x),&x\in I_2\end{cases}", 40, CYAN),
            txt("Điểm gãy không phải lỗi của mô hình – đó chính là dữ kiện thực tế.", 26, MUTED),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.28)
        fit_width(g, 12.1)
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.6)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), FadeIn(g[4]), run_time=1.2)
        self.narrate(
            "Chào các em. Ở phần hai của series toán thực tế, ta học một ý rất quan trọng: trong đời sống, một quy tắc thường chỉ đúng trong một khoảng. Qua một ngưỡng, giá, phí, công suất, thuế hoặc sức chứa có thể đổi cách tính. Vì vậy hàm số tự nhiên trở thành hàm nhiều công thức. Mấu chốt không phải đạo hàm thật dài, mà là tìm đúng điểm gãy, giải từng miền, rồi so sánh các ứng viên.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Tư duy cốt lõi", "Mọi bài hôm nay đều đi theo cùng một quy trình", "Mở đầu")
        steps = VGroup(
            bullet("Bước 1. Xác định biến và miền thực tế.", INK, 27, BLUE),
            bullet("Bước 2. Tìm các ngưỡng làm quy tắc thay đổi.", INK, 27, CYAN),
            bullet("Bước 3. Viết hàm đúng trên từng khoảng.", INK, 27, GREEN),
            bullet("Bước 4. Tối ưu hoặc giải phương trình trên từng khoảng.", INK, 27, ORANGE),
            bullet("Bước 5. Kiểm tra điểm gãy và so sánh kết quả.", INK, 27, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).shift(DOWN*0.05)
        for s in steps:
            self.play(FadeIn(s, shift=RIGHT*0.15), run_time=0.34)
        self.narrate(
            "Năm bước này quan trọng hơn mọi công thức cụ thể. Đặc biệt, điểm gãy phải được kiểm tra riêng. Nhiều bài thi được thiết kế để nghiệm đạo hàm nằm ở một nhánh, nhưng đáp án thật lại nằm ngay tại ngưỡng chuyển công thức.",
            1.8,
        )

    # ======================================================
    # MODEL 1 - PROGRESSIVE BILLING
    # ======================================================
    def model1_progressive_bill(self):
        self.show_problem(
            "Mô hình 1 – Giá lũy tiến theo bậc",
            [
                "Một dịch vụ tính phí theo lượng sử dụng x như sau:",
                mtx(r"0\le x\le50:\ 2", 32, BLUE),
                mtx(r"50<x\le100:\ 3", 32, CYAN),
                mtx(r"x>100:\ 4", 32, ORANGE),
                "Đơn giá tính theo nghìn đồng cho mỗi đơn vị trong từng bậc.",
                "Lập hàm tổng tiền T(x), rồi tính T(130) và tìm x nếu T(x)=310.",
            ],
            "Mô hình đầu tiên là một biểu giá lũy tiến minh họa. Chú ý: khi vượt sang bậc mới, chỉ phần vượt ngưỡng chịu đơn giá mới. Vì vậy ta phải cộng số tiền của các bậc trước, chứ không được lấy đơn giá cuối nhân toàn bộ lượng sử dụng.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 1", "Xây hàm từ chi phí tích lũy", "1/5")
        deriv = VGroup(
            mtx(r"T(x)=\begin{cases}2x,&0\le x\le50\\100+3(x-50),&50<x\le100\\250+4(x-100),&x>100\end{cases}", 38, INK),
            mtx(r"=\begin{cases}2x,&0\le x\le50\\3x-50,&50<x\le100\\4x-150,&x>100\end{cases}", 38, GOLD),
        ).arrange(DOWN, buff=0.48).shift(UP*0.25)
        fit_width(deriv, 11.3)
        self.play(Write(deriv[0]), run_time=1.1)
        self.narrate(
            "Ở bậc hai, năm mươi đơn vị đầu đã tốn một trăm nghìn, nên phần còn lại mới nhân ba. Ở bậc ba, một trăm đơn vị đầu đã tốn hai trăm năm mươi nghìn, nên chỉ phần vượt một trăm mới nhân bốn. Đây là chỗ học sinh rất hay viết sai.",
            1.8,
        )
        self.play(Write(deriv[1]), run_time=0.9)

        self.clear_stage(); self.add_header_footer("Mô hình 1", "Đồ thị liên tục nhưng đổi độ dốc tại các ngưỡng", "1/5")
        ax, labels = self.make_axes((0,151,25),(0,500,100),xlen=7.2,ylen=5.1,shift=LEFT*2.7)
        g1=ax.plot(lambda x:2*x,x_range=[0,50],color=BLUE,stroke_width=5)
        g2=ax.plot(lambda x:3*x-50,x_range=[50,100],color=CYAN,stroke_width=5)
        g3=ax.plot(lambda x:4*x-150,x_range=[100,150],color=ORANGE,stroke_width=5)
        x=ValueTracker(0)
        def T(v):
            if v<=50:return 2*v
            if v<=100:return 3*v-50
            return 4*v-150
        M=always_redraw(lambda:Dot(ax.c2p(x.get_value(),T(x.get_value())),radius=0.075,color=GOLD))
        v50=DashedLine(ax.c2p(50,0),ax.c2p(50,100),color=MUTED,dash_length=0.12)
        v100=DashedLine(ax.c2p(100,0),ax.c2p(100,250),color=MUTED,dash_length=0.12)
        formulas=VGroup(
            mtx(r"T(130)=4\cdot130-150=370", 35, GOLD),
            mtx(r"T(x)=310", 35, INK),
            mtx(r"4x-150=310", 34, CYAN),
            mtx(r"\boxed{x=115}", 40, GREEN),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.30).shift(UP*0.3)
        fit_width(formulas,5.8)
        self.play(Create(ax),FadeIn(labels),Create(g1),Create(g2),Create(g3),Create(v50),Create(v100),FadeIn(M),FadeIn(formulas),run_time=1.2)
        self.narrate_play(
            "Cho điểm vàng chạy qua cả ba bậc. Đồ thị không bị đứt vì tổng tiền phải được cộng dồn liên tục, nhưng độ dốc tăng từ hai lên ba rồi lên bốn. Với một trăm ba mươi đơn vị, tổng tiền là ba trăm bảy mươi nghìn.",
            x.animate.set_value(130),min_time=4.6,
        )
        self.narrate_play(
            "Nếu tổng tiền bằng ba trăm mười nghìn, ta nhìn thấy mức này đã vượt hai trăm năm mươi nên chắc chắn x lớn hơn một trăm. Vì vậy chỉ giải nhánh cuối: bốn x trừ một trăm năm mươi bằng ba trăm mười, suy ra x bằng một trăm mười lăm.",
            x.animate.set_value(115),min_time=4.5,
        )

    # ======================================================
    # MODEL 2 - FIXED THRESHOLD FEE
    # ======================================================
    def model2_threshold_fee(self):
        self.show_problem(
            "Mô hình 2 – Phí phát sinh sau một ngưỡng",
            [
                "Một mô hình lợi nhuận trước phí của cơ sở sản xuất là:",
                mtx(r"P_0(q)=-q^2+100q-500,\qquad 0\le q\le80", 38, GOLD),
                "Nếu sản lượng vượt 40 đơn vị, cơ sở phải chịu một khoản phí giả định:",
                mtx(r"E(q)=300+10(q-40)", 36, ORANGE),
                "Tìm sản lượng làm lợi nhuận sau phí lớn nhất.",
                "Mức phí chỉ là dữ liệu toán học minh họa, không phải quy định thực tế.",
            ],
            "Mô hình hai cho thấy một khoản phí kích hoạt sau ngưỡng có thể làm thay đổi hoàn toàn đáp án tối ưu. Nếu không có phí, parabol lợi nhuận đạt đỉnh tại năm mươi. Nhưng vượt bốn mươi lại làm xuất hiện một khoản chi phí mới.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 2", "Điểm gãy có thể thắng cả nghiệm đạo hàm", "2/5")
        piece = VGroup(
            mtx(r"P(q)=\begin{cases}-q^2+100q-500,&0\le q\le40\\-q^2+90q-400,&40<q\le80\end{cases}", 39, INK),
            mtx(r"P_1'(q)=100-2q>0\quad(0\le q\le40)", 34, BLUE),
            mtx(r"\max P_1=P_1(40)=1900", 35, GOLD),
            mtx(r"P_2'(q)=90-2q=0\iff q=45", 34, CYAN),
            mtx(r"P_2(45)=1625", 35, GREEN),
            mtx(r"\boxed{q_{\mathrm{opt}}=40}", 42, GOLD),
        ).arrange(DOWN,buff=0.25)
        fit_width(piece,11.5)
        self.play(FadeIn(piece[0]),run_time=0.8)
        self.narrate(
            "Ta viết lợi nhuận sau phí thành hai công thức. Nhánh đầu giữ nguyên. Nhánh sau lấy lợi nhuận cũ trừ ba trăm và trừ thêm mười cho mỗi đơn vị vượt bốn mươi. Bây giờ tối ưu từng nhánh độc lập.",
            1.7,
        )
        for mob in piece[1:]: self.play(FadeIn(mob,shift=UP*0.05),run_time=0.38)
        self.narrate(
            "Trên nhánh đầu, lợi nhuận vẫn đang tăng nên tốt nhất ở đúng q bằng bốn mươi, cho một nghìn chín trăm. Nhánh sau có cực đại tại q bằng bốn mươi lăm nhưng chỉ cho một nghìn sáu trăm hai mươi lăm. Vậy đáp án toàn cục lại chính là điểm gãy bốn mươi.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 2", "Đồ thị nhảy xuống khi phí được kích hoạt", "2/5")
        ax,labels=self.make_axes((0,81,10),(0,2201,500),xlen=7.0,ylen=5.0,shift=LEFT*2.7)
        f1=ax.plot(lambda q:-q*q+100*q-500,x_range=[5.2,40],color=BLUE,stroke_width=5)
        f2=ax.plot(lambda q:-q*q+90*q-400,x_range=[40.05,80],color=CYAN,stroke_width=5)
        p40=Dot(ax.c2p(40,1900),radius=0.09,color=GOLD)
        p45=Dot(ax.c2p(45,1625),radius=0.08,color=GREEN)
        open40=Circle(radius=0.085,color=CYAN,stroke_width=3).move_to(ax.c2p(40,1600)).set_fill(BG,opacity=1)
        guide=DashedLine(ax.c2p(40,0),ax.c2p(40,2000),color=MUTED,dash_length=0.12)
        note=VGroup(
            mtx(r"P(40)=1900",34,GOLD),
            mtx(r"\lim_{q\to40^+}P(q)=1600",32,CYAN),
            mtx(r"P(45)=1625",32,GREEN),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.35)
        self.play(Create(ax),FadeIn(labels),Create(f1),Create(f2),Create(guide),FadeIn(p40),FadeIn(open40),FadeIn(p45),FadeIn(note),run_time=1.2)
        self.narrate(
            "Trên đồ thị, khoản phí cố định ba trăm tạo ra một cú nhảy xuống ngay sau q bằng bốn mươi. Đỉnh của nhánh sau vẫn tồn tại, nhưng nó thấp hơn giá trị ở sát trước ngưỡng. Đây là kiểu bài mà chỉ giải phương trình đạo hàm bằng không sẽ rất dễ chọn sai.",
            2.0,
        )

    # ======================================================
    # MODEL 3 - OVERTIME KINK
    # ======================================================
    def model3_overtime(self):
        self.show_problem(
            "Mô hình 3 – Chi phí làm thêm giờ tạo điểm gãy",
            [
                "Doanh thu khi sản xuất q đơn vị:",
                mtx(r"R(q)=120q-q^2,\qquad 0\le q\le60", 38, GOLD),
                "Chi phí đơn vị thường là 20; sau 30 sản phẩm phải làm thêm giờ với chi phí 50 cho mỗi sản phẩm vượt ngưỡng.",
                mtx(r"C(q)=\begin{cases}20q,&0\le q\le30\\600+50(q-30),&30<q\le60\end{cases}", 36, CYAN),
                "Tìm q để lợi nhuận lớn nhất.",
            ],
            "Khác với mô hình trước, chi phí ở đây không nhảy đột ngột. Nó liên tục tại ba mươi, nhưng độ dốc thay đổi vì sau ba mươi sản phẩm phải trả chi phí làm thêm giờ cao hơn. Ta sẽ thấy điểm tối ưu nằm trên nhánh thứ hai, rất gần điểm gãy.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 3", "Tối ưu từng nhánh rồi so sánh", "3/5")
        calc=VGroup(
            mtx(r"P(q)=R(q)-C(q)",36,GOLD),
            mtx(r"P(q)=\begin{cases}100q-q^2,&0\le q\le30\\70q-q^2+900,&30<q\le60\end{cases}",38,INK),
            mtx(r"P_1'(q)=100-2q>0\Rightarrow \max P_1=P_1(30)=2100",32,BLUE),
            mtx(r"P_2'(q)=70-2q=0\Rightarrow q=35",34,CYAN),
            mtx(r"P_2(35)=2125",36,GREEN),
            mtx(r"\boxed{q_{\mathrm{opt}}=35,\quad P_{\max}=2125}",40,GOLD),
        ).arrange(DOWN,buff=0.28)
        fit_width(calc,11.6)
        for mob in calc:self.play(FadeIn(mob,shift=UP*0.05),run_time=0.38)
        self.narrate(
            "Lợi nhuận nhánh đầu là một trăm q trừ q bình phương. Trên đoạn đến ba mươi, nó vẫn tăng nên tốt nhất tại ba mươi, được hai nghìn một trăm. Nhánh sau là bảy mươi q trừ q bình phương cộng chín trăm, có đỉnh tại ba mươi lăm và cho hai nghìn một trăm hai mươi lăm. Vì vậy phương án tối ưu là ba mươi lăm sản phẩm.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 3", "Liên tục tại ngưỡng nhưng đạo hàm đổi đột ngột", "3/5")
        ax,labels=self.make_axes((0,61,10),(0,2301,500),xlen=7.0,ylen=5.0,shift=LEFT*2.7)
        p1=ax.plot(lambda q:100*q-q*q,x_range=[0,30],color=BLUE,stroke_width=5)
        p2=ax.plot(lambda q:70*q-q*q+900,x_range=[30,60],color=CYAN,stroke_width=5)
        q=ValueTracker(10)
        def P(v): return 100*v-v*v if v<=30 else 70*v-v*v+900
        M=always_redraw(lambda:Dot(ax.c2p(q.get_value(),P(q.get_value())),radius=0.075,color=GOLD))
        p30=Dot(ax.c2p(30,2100),radius=0.08,color=ORANGE)
        p35=Dot(ax.c2p(35,2125),radius=0.09,color=RED)
        info=VGroup(mtx(r"P(30)=2100",34,ORANGE),mtx(r"P(35)=2125",36,GOLD),txt("Điểm gãy không nhất thiết là tối ưu.",24,MUTED)).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.3)
        self.play(Create(ax),FadeIn(labels),Create(p1),Create(p2),FadeIn(M),FadeIn(p30),FadeIn(p35),FadeIn(info),run_time=1.1)
        self.narrate_play(
            "Cho điểm vàng chạy qua ngưỡng ba mươi. Đồ thị không nhảy, vì chi phí được nối liên tục. Tuy nhiên sau ngưỡng, đường cong lập tức bớt dốc do chi phí cận biên tăng mạnh. Điểm tối ưu dịch sang ba mươi lăm, chỉ cao hơn điểm gãy một chút.",
            q.animate.set_value(35),min_time=4.8,
        )

    # ======================================================
    # MODEL 4 - DISCOUNT + FIXED CAMPAIGN FEE
    # ======================================================
    def model4_discount_campaign(self):
        self.show_problem(
            "Mô hình 4 – Giảm giá làm tăng nhu cầu nhưng kích hoạt phí chiến dịch",
            [
                "Giá gốc là 100 nghìn đồng/sản phẩm. Giảm x nghìn đồng thì:",
                mtx(r"p(x)=100-x,\qquad q(x)=40+2x,\qquad 0\le x\le20", 36, GOLD),
                "Chi phí sản xuất là 30 nghìn đồng/sản phẩm.",
                "Nếu x>10, phải trả thêm phí chiến dịch cố định 500 nghìn đồng.",
                "Tìm mức giảm x làm lợi nhuận lớn nhất.",
            ],
            "Bài bốn kết hợp ba yếu tố rất thực tế: giảm giá làm giá bán giảm, nhu cầu tăng, và nếu giảm sâu hơn một ngưỡng thì doanh nghiệp phải mua thêm gói truyền thông. Khoản phí cố định này tạo một bước nhảy trong hàm lợi nhuận.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 4", "Đừng đạo hàm trước khi viết đúng hàm lợi nhuận", "4/5")
        algebra=VGroup(
            mtx(r"P_0(x)=(p-30)q=(70-x)(40+2x)",34,INK),
            mtx(r"P_0(x)=2800+100x-2x^2",36,CYAN),
            mtx(r"P(x)=\begin{cases}2800+100x-2x^2,&0\le x\le10\\2300+100x-2x^2,&10<x\le20\end{cases}",37,GOLD),
            mtx(r"P'(x)=100-4x>0\qquad(0\le x\le20)",34,BLUE),
            mtx(r"\max_{[0,10]}P=P(10)=3600",34,GREEN),
            mtx(r"\max_{(10,20]}P=P(20)=3500",34,ORANGE),
            mtx(r"\boxed{x_{\mathrm{opt}}=10}",42,GOLD),
        ).arrange(DOWN,buff=0.22)
        fit_width(algebra,11.7)
        for mob in algebra:self.play(FadeIn(mob,shift=UP*0.05),run_time=0.34)
        self.narrate(
            "Nếu chưa có phí chiến dịch, lợi nhuận là giá bán trừ chi phí đơn vị, nhân số lượng bán được. Ta thu được hai nghìn tám trăm cộng một trăm x trừ hai x bình phương. Khi x vượt mười, chỉ việc trừ thêm năm trăm. Đạo hàm của phần parabol vẫn dương trên toàn miền từ không đến hai mươi, nên mỗi nhánh đều tăng. Nhưng do cú nhảy phí, nhánh thứ hai dù tăng đến x bằng hai mươi vẫn chỉ đạt ba nghìn năm trăm, thấp hơn ba nghìn sáu trăm tại x bằng mười.",
            2.3,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 4", "Một bước nhảy có thể biến điểm ngưỡng thành đáp án", "4/5")
        ax,labels=self.make_axes((0,21,5),(2500,3801,250),xlen=7.0,ylen=5.0,shift=LEFT*2.7)
        g1=ax.plot(lambda x:2800+100*x-2*x*x,x_range=[0,10],color=BLUE,stroke_width=5)
        g2=ax.plot(lambda x:2300+100*x-2*x*x,x_range=[10.05,20],color=CYAN,stroke_width=5)
        d10=Dot(ax.c2p(10,3600),radius=0.09,color=GOLD)
        o10=Circle(radius=0.085,color=CYAN,stroke_width=3).move_to(ax.c2p(10,3100)).set_fill(BG,opacity=1)
        d20=Dot(ax.c2p(20,3500),radius=0.08,color=GREEN)
        x=ValueTracker(0)
        def P(v): return 2800+100*v-2*v*v if v<=10 else 2300+100*v-2*v*v
        M=always_redraw(lambda:Dot(ax.c2p(x.get_value(),P(x.get_value())),radius=0.065,color=ORANGE))
        info=VGroup(mtx(r"P(10)=3600",35,GOLD),mtx(r"P(20)=3500",35,GREEN),txt("Tăng trong từng nhánh ≠ tăng trên toàn miền",24,MUTED)).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.25)
        self.play(Create(ax),FadeIn(labels),Create(g1),Create(g2),FadeIn(d10),FadeIn(o10),FadeIn(d20),FadeIn(M),FadeIn(info),run_time=1.1)
        self.narrate_play(
            "Đây là hình ảnh rất đáng nhớ. Trong từng đoạn, lợi nhuận đều tăng. Nhưng ngay sau x bằng mười, phí chiến dịch làm đồ thị rơi xuống năm trăm. Vì thế không thể kết luận hàm tăng trên toàn miền chỉ bằng dấu đạo hàm của từng công thức. Điểm vàng chạy đến mười chính là vị trí tối ưu toàn cục.",
            x.animate.set_value(10),min_time=5.0,
        )

    # ======================================================
    # MODEL 5 - CAPACITY KINK OPTIMUM
    # ======================================================
    def model5_capacity(self):
        self.show_problem(
            "Mô hình 5 – Sức chứa biến điểm gãy thành điểm tối ưu",
            [
                "Một địa điểm có tối đa 120 chỗ. Nếu giá vé là p nghìn đồng thì nhu cầu dự kiến:",
                mtx(r"d(p)=260-2p,\qquad 30\le p\le120", 38, GOLD),
                "Số vé thực bán không thể vượt sức chứa:",
                mtx(r"q(p)=\min\{120,260-2p\}", 38, CYAN),
                "Tìm giá vé làm doanh thu lớn nhất.",
            ],
            "Mô hình cuối cùng dùng hàm min, một kiểu rất tự nhiên trong thực tế. Nhu cầu có thể lớn nhưng địa điểm chỉ có một trăm hai mươi chỗ. Vì vậy trước một mức giá nào đó, doanh thu bị giới hạn bởi sức chứa; sau mức ấy, doanh thu bị giới hạn bởi nhu cầu.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 5", "Tìm điểm gãy từ phương trình nhu cầu = sức chứa", "5/5")
        deriv=VGroup(
            mtx(r"260-2p=120\iff p=70",38,GOLD),
            mtx(r"R(p)=\begin{cases}120p,&30\le p\le70\\p(260-2p),&70<p\le120\end{cases}",39,INK),
            mtx(r"R_1'(p)=120>0",34,BLUE),
            mtx(r"R_2'(p)=260-4p<0\qquad(p>70)",34,CYAN),
            mtx(r"\boxed{p_{\mathrm{opt}}=70,\quad R_{\max}=8400}",42,GOLD),
        ).arrange(DOWN,buff=0.30)
        fit_width(deriv,11.4)
        for mob in deriv:self.play(FadeIn(mob,shift=UP*0.05),run_time=0.38)
        self.narrate(
            "Điểm gãy xuất hiện khi nhu cầu vừa đúng bằng sức chứa: hai trăm sáu mươi trừ hai p bằng một trăm hai mươi, nên p bằng bảy mươi. Trước bảy mươi, bán đủ một trăm hai mươi vé nên doanh thu bằng một trăm hai mươi p và tăng. Sau bảy mươi, doanh thu bằng p nhân hai trăm sáu mươi trừ hai p; trên miền p lớn hơn bảy mươi, đạo hàm đã âm nên doanh thu giảm. Vì vậy đỉnh nằm đúng tại điểm gãy.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 5", "Không có R'(70)=0 nhưng 70 vẫn là tối ưu", "5/5")
        ax,labels=self.make_axes((30,121,15),(3000,9001,1000),xlen=7.0,ylen=5.0,shift=LEFT*2.7)
        r1=ax.plot(lambda p:120*p,x_range=[30,70],color=BLUE,stroke_width=5)
        r2=ax.plot(lambda p:p*(260-2*p),x_range=[70,120],color=CYAN,stroke_width=5)
        p=ValueTracker(30)
        def R(v): return 120*v if v<=70 else v*(260-2*v)
        M=always_redraw(lambda:Dot(ax.c2p(p.get_value(),R(p.get_value())),radius=0.075,color=GOLD))
        peak=Dot(ax.c2p(70,8400),radius=0.095,color=RED)
        label=mtx(r"(70,8400)",30,RED).next_to(peak,UP+RIGHT,buff=0.08)
        card=VGroup(txt("Điểm cực đại do đổi cơ chế",25,GOLD,BOLD),mtx(r"R'_-(70)>0,\qquad R'_+(70)<0",34,CYAN)).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.3)
        self.play(Create(ax),FadeIn(labels),Create(r1),Create(r2),FadeIn(M),FadeIn(peak),FadeIn(label),FadeIn(card),run_time=1.1)
        self.narrate_play(
            "Cho giá vé tăng dần. Khi còn bán hết chỗ, doanh thu đi lên theo một đoạn thẳng. Đúng tại bảy mươi, cơ chế thay đổi. Từ đó nhu cầu giảm đủ nhanh để doanh thu quay đầu đi xuống. Điểm cực đại này không cần đạo hàm bằng không; nó được tạo bởi sự đổi công thức của mô hình.",
            p.animate.set_value(105),min_time=5.0,
        )
        self.narrate_play(
            "Kéo điểm trở lại bảy mươi. Đây là một thông điệp rất quan trọng cho câu trả lời ngắn: ngoài nghiệm đạo hàm bằng không, luôn phải kiểm tra biên miền và mọi điểm gãy của hàm nhiều công thức.",
            p.animate.set_value(70),min_time=4.3,
        )

    # ======================================================
    # EXAM STRATEGY + SUMMARY
    # ======================================================
    def summary(self):
        self.clear_stage(); self.add_header_footer("Chiến lược làm nhanh", "Hàm nhiều công thức trong câu Đúng/Sai và trả lời ngắn", "Tổng kết")
        board=VGroup(
            VGroup(mtx(r"1",30,GOLD),txt("Tìm ngưỡng trước khi đạo hàm.",26,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"2",30,GOLD),txt("Viết công thức tích lũy đúng, tránh tính lại từ đầu mỗi bậc.",26,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"3",30,GOLD),txt("Tối ưu riêng từng khoảng theo đúng miền.",26,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"4",30,GOLD),txt("Liệt kê: nghiệm đạo hàm, biên, điểm gãy, điểm nhảy.",26,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"5",30,GOLD),txt("So sánh giá trị cuối cùng rồi mới kết luận thực tế.",26,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.36)
        fit_width(board,11.6)
        for row in board:self.play(FadeIn(row,shift=RIGHT*0.1),run_time=0.34)
        self.narrate(
            "Nếu gặp một bài nhiều công thức trong đề thi, hãy làm theo checklist này. Tìm ngưỡng trước. Viết đúng hàm trên từng khoảng. Tối ưu riêng. Sau đó gom tất cả ứng viên gồm nghiệm đạo hàm, đầu mút, điểm gãy và điểm nhảy. Cuối cùng mới so sánh. Cách làm này rất chắc và tránh được hầu hết bẫy.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài thử thách 30 giây", "Tự dừng video trước khi xem lời giải", "Tổng kết")
        q=VGroup(
            txt("Một kho có chi phí vận hành:",27,INK),
            mtx(r"C(x)=\begin{cases}40x+200,&0\le x\le20\\1000+25(x-20),&20<x\le50\end{cases}",38,GOLD),
            mtx(r"R(x)=80x",38,CYAN),
            txt("Tìm x làm lợi nhuận lớn nhất.",28,INK,BOLD),
        ).arrange(DOWN,buff=0.30)
        fit_width(q,11.2)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate(
            "Bài thử thách: doanh thu là tám mươi x. Chi phí có hai công thức như trên. Hãy dừng video và tự tìm x tối ưu. Chú ý kiểm tra xem chi phí tại ngưỡng hai mươi có liên tục hay không.",
            1.6,
        )
        self.wait(1.0)
        sol=VGroup(
            mtx(r"P_1(x)=40x-200",34,BLUE),
            mtx(r"P_2(x)=55x-500",34,CYAN),
            mtx(r"P_1(20)=600,\qquad P_2(20^+)=600",33,INK),
            mtx(r"P_2'(x)=55>0",33,GREEN),
            mtx(r"\boxed{x=50}",42,GOLD),
        ).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.55)
        self.play(FadeIn(sol),run_time=0.8)
        self.narrate(
            "Lời giải rất ngắn. Nhánh đầu cho lợi nhuận bốn mươi x trừ hai trăm. Nhánh sau cho năm mươi lăm x trừ năm trăm. Hai nhánh nối liên tục tại hai mươi, và cả hai đều tăng. Vì vậy lợi nhuận lớn nhất ở biên phải x bằng năm mươi.",
            1.6,
        )

        self.clear_stage(); self.add_header_footer("Kế hoạch series", "Bài tiếp theo: tốc độ – thời gian – năng suất – chi phí", "Tổng kết")
        roadmap=VGroup(
            VGroup(mtx(r"01",30,MUTED),txt("Mô hình hóa + tối ưu một biến",25,MUTED)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"02",30,GOLD),txt("Hàm nhiều công thức: ngưỡng – phí – sức chứa",25,GOLD,BOLD)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"03",30,CYAN),txt("Tốc độ – thời gian – năng suất – chi phí",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"04",30,BLUE),txt("Đọc đồ thị thực tế + câu Đúng/Sai",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"05",30,GREEN),txt("Tích phân trong các đại lượng tích lũy",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"06\to08",30,ORANGE),txt("Oxyz – xác suất thống kê – tổng hợp thi",25,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30)
        fit_width(roadmap,11.6)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.1) for r in roadmap],lag_ratio=0.10),run_time=1.4)
        self.narrate(
            "Phần hai kết thúc ở đây. Video tiếp theo sẽ gom các bài tốc độ, thời gian, năng suất và chi phí, nơi những biểu thức dạng a chia x cộng b x xuất hiện rất tự nhiên. Series vẫn giữ nguyên nguyên tắc: bài toán thực tế trước, mô hình tường minh, đồ thị trực quan và hạn chế tối đa hàm ẩn.",
            1.9,
        )

        self.clear_stage()
        end=VGroup(
            txt("ĐIỂM GÃY CŨNG LÀ MỘT ỨNG VIÊN CỰC TRỊ",38,GOLD,BOLD),
            mtx(r"\boxed{f'(x)=0\quad+\quad x\in\partial D\quad+\quad x=x_{\mathrm{break}}}",37,CYAN),
            txt(TEN_THAY,22,MUTED),
        ).arrange(DOWN,buff=0.42)
        self.play(FadeIn(end[0]),Write(end[1]),FadeIn(end[2]),run_time=1.0)
        self.narrate(
            "Chốt lại bằng một câu: trong bài toán thực tế, nghiệm đạo hàm bằng không chỉ là một nhóm ứng viên. Biên miền và điểm gãy có thể mới là nơi đạt tối ưu. Hiểu điều đó, các bài hàm nhiều công thức sẽ trở nên rất sáng sủa.",
            1.6,
        )

    def construct(self):
        self.intro()
        self.model1_progressive_bill()
        self.model2_threshold_fee()
        self.model3_overtime()
        self.model4_discount_campaign()
        self.model5_capacity()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_02_ham_nhieu_cong_thuc_1080p"
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
    master_wav = ROOT / "master_narration_toan_thuc_te_ham_so_02.wav"
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
