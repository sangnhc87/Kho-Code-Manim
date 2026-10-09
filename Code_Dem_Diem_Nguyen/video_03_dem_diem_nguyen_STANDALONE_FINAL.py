# ==========================================================
# VIDEO 03 - DEM SO DIEM NGUYEN TRONG MIEN NGHIEM
# STANDALONE - KHONG PHU THUOC FILE .PY NOI BO NAO
# GitHub Actions / Linux / Manim Community 0.21.0
# ==========================================================

from manim import *
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

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
MEDIA_DIR = ROOT / "media"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# PALETTE
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

# ==========================================================
# LATEX
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


def fit_width(mob, max_width=12.2):
    if mob.width > max_width:
        mob.scale_to_fit_width(max_width)
    return mob


def make_panel(width=12.3, height=5.45):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        fill_color=PANEL,
        fill_opacity=0.90,
        stroke_color=MUTED,
        stroke_opacity=0.25,
        stroke_width=1.5,
    )


def footer(progress=""):
    left = txt(TEN_THAY, 19, MUTED)
    right = txt(progress, 19, MUTED)
    left.to_edge(DOWN, buff=0.17).to_edge(LEFT, buff=0.38)
    right.to_edge(DOWN, buff=0.17).to_edge(RIGHT, buff=0.38)
    return VGroup(left, right)


def title_group(title, subtitle=None):
    t = fit_width(txt(title, 38, INK, BOLD), 12.1).to_edge(UP, buff=0.23)
    if subtitle:
        s = fit_width(txt(subtitle, 22, MUTED), 11.5).next_to(t, DOWN, buff=0.08)
        return VGroup(t, s)
    return VGroup(t)


def lattice_plane(xmax=10, ymax=7, width=7.2, height=5.2):
    plane = NumberPlane(
        x_range=[-0.5, xmax + 0.5, 1],
        y_range=[-0.5, ymax + 0.5, 1],
        x_length=width,
        y_length=height,
        background_line_style={
            "stroke_color": MUTED,
            "stroke_opacity": 0.20,
            "stroke_width": 1,
        },
        axis_config={"color": MUTED, "stroke_width": 2},
    )
    return plane


def lattice_dots(plane, predicate, xmax, ymax, color=CYAN, radius=0.055):
    dots = VGroup()
    coords = []
    for x in range(0, xmax + 1):
        for y in range(0, ymax + 1):
            if predicate(x, y):
                dots.add(Dot(plane.c2p(x, y), radius=radius, color=color))
                coords.append((x, y))
    return dots, coords

# ==========================================================
# AUDIO - MASTER TRACK
# ==========================================================

def _audio_key(text):
    payload = json.dumps(
        {
            "text": text,
            "voice": GIONG_DOC,
            "rate": TOC_DO_DOC,
            "pitch": PITCH,
            "engine": "edge-tts",
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1200:
        raise RuntimeError(f"Audio khong hop le: {path}")
    dur = probe_duration(path)
    if dur < 0.15:
        raise RuntimeError(f"Audio qua ngan: {path}")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
        check=True,
    )


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
                "    c=edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)\n"
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
        raise RuntimeError("Khong co narration de ghep.")

    inputs = []
    filters = []
    labels = []

    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]aresample=48000,adelay={ms}:all=1[a{i}]")
        labels.append(f"[a{i}]")

    fc = ";".join(filters) + ";" + "".join(labels) + (
        f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            *inputs,
            "-filter_complex",
            fc,
            "-map",
            "[m]",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-t",
            f"{video_duration:.3f}",
            str(out_wav),
        ],
        check=True,
    )


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out),
        ],
        check=True,
    )

# ==========================================================
# BASE SCENE
# ==========================================================

class LessonBase(Scene):
    def setup(self):
        self.audio_events = []

    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def clear_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.38)

    def add_header_footer(self, title, subtitle, progress):
        h = title_group(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, blocks, voice, progress):
        self.clear_stage()
        self.add_header_footer(title, "ĐỀ BÀI", progress)

        panel = make_panel(12.35, 5.25).shift(DOWN * 0.12)
        self.play(FadeIn(panel), run_time=0.42)

        items = VGroup()
        for kind, content, size, color in blocks:
            if kind == "math":
                mob = fit_width(mtx(content, size, color), 11.0)
            else:
                mob = fit_width(txt(content, size, color), 11.0)
            items.add(mob)

        items.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        items.move_to(panel.get_center()).shift(UP * 0.03)

        for item in items:
            self.play(FadeIn(item, shift=UP * 0.05), run_time=0.24)

        self.narrate(voice, 2.0)

# ==========================================================
# LESSON
# ==========================================================

class SangLesson(LessonBase):

    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("ĐẾM SỐ ĐIỂM NGUYÊN TRONG MIỀN NGHIỆM", 45, INK, BOLD),
            mtx(r"(x,y)\in\mathbb Z^2", 44, GOLD),
            txt("Mỗi điểm nguyên là một phương án rời rạc", 29, CYAN),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.28)
        self.play(FadeIn(g), run_time=1.0)
        self.narrate(
            "Chào các em! Trong bài trước, miền nghiệm của hệ bất phương trình là một vùng liên tục trên mặt phẳng. Nhưng trong nhiều bài toán thực tế, x và y phải là số nguyên, chẳng hạn số xe, số sản phẩm hoặc số phương án. Hôm nay ta học cách đếm chính xác các điểm nguyên nằm trong miền nghiệm, từ rất dễ đến khó hơn.",
            2.0,
        )

        self.clear_stage()
        self.add_header_footer("1. Điểm nguyên là gì?", "Nhìn trên lưới tọa độ", "Mở đầu")
        plane = lattice_plane(6, 5, 7.0, 4.8).shift(LEFT * 1.8 + DOWN * 0.2)
        pts, _ = lattice_dots(plane, lambda x, y: True, 6, 5, MUTED, 0.045)
        sample = VGroup(
            Dot(plane.c2p(2, 3), radius=0.085, color=GOLD),
            mtx(r"(2,3)", 34, GOLD).next_to(plane.c2p(2, 3), UR, buff=0.12),
        )
        bad = VGroup(
            Dot(plane.c2p(2.5, 1.5), radius=0.075, color=RED),
            mtx(r"(2.5,1.5)", 31, RED).next_to(plane.c2p(2.5, 1.5), UR, buff=0.10),
        )
        note = VGroup(
            mtx(r"x\in\mathbb Z", 36, BLUE),
            mtx(r"y\in\mathbb Z", 36, BLUE),
            mtx(r"(x,y)\in\mathbb Z^2", 40, GOLD),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.7)
        self.play(Create(plane), FadeIn(pts), run_time=1.0)
        self.play(FadeIn(sample), FadeIn(note), run_time=0.6)
        self.narrate(
            "Điểm nguyên là điểm có cả hoành độ và tung độ đều là số nguyên. Ví dụ hai ba là điểm nguyên. Còn hai phẩy năm, một phẩy năm thì không. Khi đề yêu cầu nghiệm nguyên, ta không đếm mọi điểm của miền, mà chỉ đếm các nút lưới nằm trong miền đó.",
            1.8,
        )
        self.play(FadeIn(bad), run_time=0.4)
        self.narrate(
            "Vì vậy chiến lược của ta sẽ luôn có hai lớp: trước hết hiểu miền nghiệm hình học, sau đó mới lọc và đếm các điểm nguyên.",
            1.2,
        )

    def example1(self):
        self.show_problem(
            "Ví dụ 1 – Tam giác cơ bản",
            [
                ("text", "Đếm các nghiệm nguyên không âm của hệ:", 28, INK),
                ("math", r"\begin{cases}x\ge0\\y\ge0\\x+y\le4\end{cases}", 42, GOLD),
                ("math", r"x,y\in\mathbb Z", 35, CYAN),
            ],
            "Ví dụ một là bài cơ bản nhất. Ta đếm các cặp số nguyên không âm x y thỏa x cộng y không vượt quá bốn. Trước hết ta vẽ miền tam giác, sau đó quét từng hàng ngang.",
            "Ví dụ 1/5",
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 1", "Vẽ miền rồi quét từng hàng", "Ví dụ 1/5")
        plane = lattice_plane(5, 5, 6.6, 5.0).shift(LEFT * 2.4 + DOWN * 0.15)
        tri = Polygon(
            plane.c2p(0, 0),
            plane.c2p(4, 0),
            plane.c2p(0, 4),
            fill_color=BLUE,
            fill_opacity=0.18,
            stroke_color=BLUE,
            stroke_width=3,
        )
        dots, coords = lattice_dots(plane, lambda x, y: x + y <= 4, 4, 4, CYAN, 0.065)
        self.play(Create(plane), FadeIn(tri), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.04), run_time=1.2)
        self.narrate(
            "Miền nghiệm là tam giác có ba đỉnh không không, bốn không và không bốn. Bây giờ ta chỉ quan tâm các điểm lưới nguyên nằm trên hoặc bên trong tam giác. Vì các dấu đều có bằng, những điểm trên đường biên vẫn được tính.",
            1.8,
        )

        rows = VGroup(
            mtx(r"y=0:\ \#x=5", 30, INK),
            mtx(r"y=1:\ \#x=4", 30, INK),
            mtx(r"y=2:\ \#x=3", 30, INK),
            mtx(r"y=3:\ \#x=2", 30, INK),
            mtx(r"y=4:\ \#x=1", 30, INK),
            mtx(r"N=5+4+3+2+1=15", 39, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20).to_edge(RIGHT, buff=0.4)
        self.play(FadeIn(rows), run_time=0.8)
        self.narrate(
            "Quét theo y. Hàng y bằng không có năm giá trị x từ không đến bốn. Hàng y bằng một có bốn giá trị. Sau đó là ba, hai và một. Tổng là mười lăm điểm nguyên.",
            1.6,
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 1", "Rút ra công thức đếm nhanh", "Ví dụ 1/5")
        deriv = VGroup(
            mtx(r"0\le x\le4-y", 37, BLUE),
            mtx(r"\#x=(4-y)-0+1=5-y", 37, CYAN),
            mtx(r"N=\sum_{y=0}^{4}(5-y)", 40, GOLD),
            mtx(r"N=5+4+3+2+1=15", 42, GOLD),
        ).arrange(DOWN, buff=0.32)
        self.play(FadeIn(deriv), run_time=0.8)
        self.narrate(
            "Ta có thể viết chặt chẽ hơn. Với một y cố định, x chạy từ không đến bốn trừ y, nên số giá trị nguyên của x là năm trừ y. Cộng từ y bằng không đến bốn ta được đúng mười lăm.",
            1.6,
        )

    def example2(self):
        self.show_problem(
            "Ví dụ 2 – Dấu nghiêm ngặt",
            [
                ("text", "Đếm các nghiệm nguyên không âm:", 28, INK),
                ("math", r"2x+y<8", 44, GOLD),
                ("math", r"x,y\in\mathbb Z_{\ge0}", 35, CYAN),
            ],
            "Ví dụ hai có dấu nhỏ hơn nghiêm ngặt. Đây là nơi tính chất số nguyên giúp ta đơn giản hóa bài toán. Vì hai x cộng y luôn là số nguyên, điều kiện nhỏ hơn tám tương đương nhỏ hơn hoặc bằng bảy.",
            "Ví dụ 2/5",
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 2", "Đổi dấu nghiêm ngặt khi vế trái là số nguyên", "Ví dụ 2/5")
        key = VGroup(
            mtx(r"2x+y\in\mathbb Z", 38, BLUE),
            mtx(r"2x+y<8", 40, ORANGE),
            mtx(r"\Longleftrightarrow", 40, MUTED),
            mtx(r"2x+y\le7", 42, GOLD),
        ).arrange(DOWN, buff=0.24)
        self.play(FadeIn(key), run_time=0.7)
        self.narrate(
            "Đây là mẹo rất quan trọng. Một số nguyên nhỏ hơn tám thì lớn nhất chỉ có thể là bảy. Vì thế ta đổi ngay thành hai x cộng y nhỏ hơn hoặc bằng bảy. Sau đó bài toán lại trở về dạng quen thuộc.",
            1.6,
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 2", "Quét theo x", "Ví dụ 2/5")
        calc = VGroup(
            mtx(r"x=0:\ 0\le y\le7\Rightarrow8", 31, INK),
            mtx(r"x=1:\ 0\le y\le5\Rightarrow6", 31, INK),
            mtx(r"x=2:\ 0\le y\le3\Rightarrow4", 31, INK),
            mtx(r"x=3:\ 0\le y\le1\Rightarrow2", 31, INK),
            mtx(r"x\ge4:\ \varnothing", 31, RED),
            mtx(r"\boxed{N=8+6+4+2=20}", 42, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.play(FadeIn(calc), run_time=0.8)
        self.narrate(
            "Với x bằng không, y có tám giá trị từ không đến bảy. Với x bằng một có sáu giá trị. Sau đó là bốn và hai. Từ x bằng bốn trở đi thì hai x đã ít nhất bằng tám nên không còn nghiệm. Vậy có hai mươi điểm nguyên.",
            1.8,
        )

    def example3(self):
        self.show_problem(
            "Ví dụ 3 – Miền bị kẹp giữa hai đường",
            [
                ("text", "Đếm các nghiệm nguyên không âm của hệ:", 28, INK),
                ("math", r"\begin{cases}x+y\ge3\\x+2y\le8\end{cases}", 43, GOLD),
                ("math", r"x,y\in\mathbb Z_{\ge0}", 35, CYAN),
            ],
            "Ví dụ ba khó hơn vì miền nghiệm nằm giữa hai đường thẳng. Cách an toàn nhất là quét theo y. Với mỗi y, ta tìm cận dưới và cận trên của x rồi đếm số nguyên trong đoạn đó.",
            "Ví dụ 3/5",
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 3", "Lập cận dưới và cận trên", "Ví dụ 3/5")
        derive = VGroup(
            mtx(r"x+y\ge3\Rightarrow x\ge3-y", 36, BLUE),
            mtx(r"x+2y\le8\Rightarrow x\le8-2y", 36, ORANGE),
            mtx(r"x\ge0", 34, GREEN),
            mtx(r"\max(0,3-y)\le x\le8-2y", 40, GOLD),
        ).arrange(DOWN, buff=0.30)
        self.play(FadeIn(derive), run_time=0.8)
        self.narrate(
            "Điều kiện thứ nhất cho x ít nhất bằng ba trừ y. Điều kiện thứ hai cho x không vượt quá tám trừ hai y. Vì x còn phải không âm, cận dưới thật sự là số lớn hơn giữa không và ba trừ y.",
            1.8,
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 3", "Đếm từng hàng", "Ví dụ 3/5")
        rows = VGroup(
            mtx(r"y=0:\ 3\le x\le8\Rightarrow6", 29, INK),
            mtx(r"y=1:\ 2\le x\le6\Rightarrow5", 29, INK),
            mtx(r"y=2:\ 1\le x\le4\Rightarrow4", 29, INK),
            mtx(r"y=3:\ 0\le x\le2\Rightarrow3", 29, INK),
            mtx(r"y=4:\ x=0\Rightarrow1", 29, INK),
            mtx(r"\boxed{N=6+5+4+3+1=19}", 40, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.play(FadeIn(rows), run_time=0.8)
        self.narrate(
            "Ta xét lần lượt y bằng không đến bốn. Số giá trị x là sáu, năm, bốn, ba và một. Tổng bằng mười chín. Từ y bằng năm trở lên, cận trên tám trừ hai y đã âm nên không còn nghiệm không âm.",
            1.8,
        )

    def example4(self):
        self.show_problem(
            "Ví dụ 4 – Một bài toán thực tế",
            [
                ("text", "Một đội vận tải chọn x xe nhỏ và y xe lớn.", 27, INK),
                ("math", r"2x+3y\le12", 42, GOLD),
                ("math", r"x+y\ge3", 40, GOLD),
                ("math", r"x,y\in\mathbb Z_{\ge0}", 35, CYAN),
                ("text", "Hỏi có bao nhiêu phương án điều xe?", 28, GREEN),
            ],
            "Ví dụ bốn gắn với thực tế. x là số xe nhỏ, y là số xe lớn. Điều kiện hai x cộng ba y không vượt quá mười hai biểu diễn giới hạn nguồn lực, còn tổng số xe phải ít nhất là ba. Mỗi nghiệm nguyên không âm chính là một phương án điều xe.",
            "Ví dụ 4/5",
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 4", "Mỗi điểm nguyên là một phương án", "Ví dụ 4/5")
        rows = VGroup(
            mtx(r"y=0:\ 3\le x\le6\Rightarrow4", 30, INK),
            mtx(r"y=1:\ 2\le x\le4\Rightarrow3", 30, INK),
            mtx(r"y=2:\ 1\le x\le3\Rightarrow3", 30, INK),
            mtx(r"y=3:\ 0\le x\le1\Rightarrow2", 30, INK),
            mtx(r"y=4:\ x=0\Rightarrow1", 30, INK),
            mtx(r"\boxed{N=4+3+3+2+1=13}", 42, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.play(FadeIn(rows), run_time=0.8)
        self.narrate(
            "Quét theo số xe lớn y. Ta lần lượt có bốn, ba, ba, hai và một giá trị nguyên của x. Tổng cộng mười ba phương án. Đây là ý nghĩa thực tế của việc đếm điểm nguyên: mỗi điểm lưới là một kế hoạch rời rạc có thể thực hiện.",
            1.8,
        )

    def example5(self):
        self.show_problem(
            "Ví dụ 5 – Khi xuất hiện hàm sàn",
            [
                ("text", "Đếm các nghiệm nguyên không âm:", 28, INK),
                ("math", r"3x+2y\le10", 44, GOLD),
                ("math", r"x,y\in\mathbb Z_{\ge0}", 35, CYAN),
            ],
            "Ví dụ năm cho thấy vì sao hàm phần nguyên dưới xuất hiện tự nhiên. Nếu cố định y, cận trên của x là mười trừ hai y chia ba. Cận này thường không phải số nguyên, nên ta phải lấy số nguyên lớn nhất không vượt quá nó.",
            "Ví dụ 5/5",
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 5", "Từ phân số đến hàm sàn", "Ví dụ 5/5")
        deriv = VGroup(
            mtx(r"3x\le10-2y", 37, INK),
            mtx(r"x\le\frac{10-2y}{3}", 39, BLUE),
            mtx(r"x\le\left\lfloor\frac{10-2y}{3}\right\rfloor", 42, GOLD),
        ).arrange(DOWN, buff=0.34)
        self.play(FadeIn(deriv), run_time=0.8)
        self.narrate(
            "Sau khi chia cho ba, cận của x là một phân số. Vì x phải nguyên, giá trị lớn nhất của x chính là phần nguyên dưới của phân số đó. Đây không phải mẹo ghi nhớ, mà xuất phát trực tiếp từ yêu cầu x là số nguyên.",
            1.6,
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ 5", "Đếm đầy đủ", "Ví dụ 5/5")
        rows = VGroup(
            mtx(r"y=0:\ 0\le x\le3\Rightarrow4", 29, INK),
            mtx(r"y=1:\ 0\le x\le2\Rightarrow3", 29, INK),
            mtx(r"y=2:\ 0\le x\le2\Rightarrow3", 29, INK),
            mtx(r"y=3:\ 0\le x\le1\Rightarrow2", 29, INK),
            mtx(r"y=4:\ x=0\Rightarrow1", 29, INK),
            mtx(r"y=5:\ x=0\Rightarrow1", 29, INK),
            mtx(r"\boxed{N=4+3+3+2+1+1=14}", 40, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        self.play(FadeIn(rows), run_time=0.8)
        self.narrate(
            "Với y từ không đến năm, số giá trị x lần lượt là bốn, ba, ba, hai, một và một. Tổng bằng mười bốn. Đây là dạng bài mà dùng hàm sàn giúp ta không đếm nhầm khi cận chia không hết.",
            1.7,
        )

    def method_summary(self):
        self.clear_stage()
        self.add_header_footer("Chiến lược tổng quát", "Đếm có hệ thống, không đếm mò", "Tổng kết")
        steps = VGroup(
            VGroup(mtx(r"1", 34, GOLD), txt("Vẽ hoặc xác định chính xác miền nghiệm.", 27, INK)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"2", 34, GOLD), txt("Chọn quét theo hàng y hoặc cột x.", 27, INK)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"3", 34, GOLD), txt("Tìm cận dưới và cận trên của biến còn lại.", 27, INK)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"4", 34, GOLD), txt("Dùng phần nguyên khi cận không nguyên.", 27, INK)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"5", 34, GOLD), txt("Cộng số điểm của tất cả các hàng hoặc cột.", 27, INK)).arrange(RIGHT, buff=0.22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        self.play(FadeIn(steps), run_time=0.9)
        self.narrate(
            "Tóm lại, đừng cố đếm bằng mắt khi miền lớn. Hãy xác định miền, chọn một hướng quét, tìm cận dưới cận trên, dùng phần nguyên nếu cần, rồi cộng số điểm. Cách làm này vừa chắc chắn vừa dễ kiểm tra.",
            1.8,
        )

        self.clear_stage()
        self.add_header_footer("Ba lỗi rất hay gặp", "Tránh mất điểm đáng tiếc", "Tổng kết")
        errors = VGroup(
            VGroup(mtx(r"\times", 32, RED), txt("Quên điều kiện x, y phải nguyên.", 27, INK)).arrange(RIGHT, buff=0.20),
            VGroup(mtx(r"\times", 32, RED), txt("Bỏ sót các điểm nằm trên biên có dấu bằng.", 27, INK)).arrange(RIGHT, buff=0.20),
            VGroup(mtx(r"\times", 32, RED), txt("Dùng cận phân số mà không lấy phần nguyên.", 27, INK)).arrange(RIGHT, buff=0.20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        self.play(FadeIn(errors), run_time=0.7)
        self.narrate(
            "Ba lỗi thường gặp là quên điều kiện nguyên, bỏ sót điểm trên biên, và dùng trực tiếp một cận phân số. Chỉ cần kiểm tra ba điều này, các em tránh được phần lớn lỗi đếm.",
            1.5,
        )

    def practice(self):
        self.show_problem(
            "Bài tự luyện – Tổng hợp",
            [
                ("text", "Đếm các nghiệm nguyên không âm của hệ:", 28, INK),
                ("math", r"\begin{cases}x+2y\le10\\x+y\ge4\end{cases}", 43, GOLD),
                ("math", r"x,y\in\mathbb Z_{\ge0}", 35, CYAN),
            ],
            "Bài tự luyện cuối video. Các em hãy dừng video và thử quét theo y. Với mỗi y, điều kiện x cộng y ít nhất bằng bốn tạo cận dưới, còn x cộng hai y không vượt quá mười tạo cận trên.",
            "Tự luyện",
        )

        self.clear_stage()
        self.add_header_footer("Bài tự luyện", "Lời giải chi tiết", "Tự luyện")
        rows = VGroup(
            mtx(r"y=0:\ 4\le x\le10\Rightarrow7", 28, INK),
            mtx(r"y=1:\ 3\le x\le8\Rightarrow6", 28, INK),
            mtx(r"y=2:\ 2\le x\le6\Rightarrow5", 28, INK),
            mtx(r"y=3:\ 1\le x\le4\Rightarrow4", 28, INK),
            mtx(r"y=4:\ 0\le x\le2\Rightarrow3", 28, INK),
            mtx(r"y=5:\ x=0\Rightarrow1", 28, INK),
            mtx(r"\boxed{N=7+6+5+4+3+1=26}", 40, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        self.play(FadeIn(rows), run_time=0.9)
        self.narrate(
            "Lời giải: với y từ không đến năm, số giá trị x lần lượt là bảy, sáu, năm, bốn, ba và một. Tổng bằng hai mươi sáu. Bài này kết hợp cả cận dưới và cận trên, nên rất phù hợp để kiểm tra xem các em đã hiểu phương pháp quét hay chưa.",
            1.8,
        )

    def outro(self):
        self.clear_stage()
        g = VGroup(
            txt("CHỐT LẠI", 44, GOLD, BOLD),
            mtx(r"(x,y)\in S\cap\mathbb Z^2", 42, BLUE),
            txt("Miền nghiệm cho ta hình học; điều kiện nguyên biến nó thành bài toán đếm.", 27, CYAN),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.30)
        self.play(FadeIn(g), run_time=0.9)
        self.narrate(
            "Các em hãy nhớ: miền nghiệm cho ta bức tranh hình học, còn điều kiện nguyên biến bức tranh đó thành một tập hữu hạn các phương án rời rạc. Khi biết quét theo hàng hoặc cột, việc đếm trở nên rất có hệ thống. Hẹn gặp các em ở video tiếp theo.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.example1()
        self.example2()
        self.example3()
        self.example4()
        self.example5()
        self.method_summary()
        self.practice()
        self.outro()

# ==========================================================
# RENDER
# ==========================================================

def render_scene(scene_cls, output_stem):
    # Preflight: fail early, with clear messages.
    for cmd in ["ffmpeg", "ffprobe"]:
        try:
            subprocess.run([cmd, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except Exception as e:
            raise RuntimeError(f"Khong tim thay {cmd}: {e}")

    try:
        subprocess.run([sys.executable, "-c", "import edge_tts"], check=True)
    except Exception as e:
        raise RuntimeError(f"Chua cai edge-tts: {e}")

    config.media_dir = str(MEDIA_DIR)
    config.output_file = output_stem
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print("=" * 70)
    print("STANDALONE MANIM LESSON")
    print(f"Teacher : {TEN_THAY}")
    print(f"Voice   : {GIONG_DOC}")
    print(f"Rate    : {TOC_DO_DOC}")
    print(f"Pitch   : {PITCH}")
    print("No local Python module dependencies.")
    print("=" * 70)

    scene = scene_cls()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim: {video_path}")

    if len(scene.audio_events) == 0:
        raise RuntimeError("Render xong nhung khong co narration events.")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / f"{output_stem}_master.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)

    # Verify final audio/video streams.
    subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,codec_name,width,height,r_frame_rate",
            "-show_entries",
            "format=duration,size",
            "-of",
            "json",
            str(final_path),
        ],
        check=True,
    )

    print("\n" + "=" * 70)
    print(f"RENDERED: {video_path}")
    print(f"NARRATION SEGMENTS: {len(scene.audio_events)}")
    print(f"FINAL VIDEO WITH AUDIO: {final_path}")
    print(f"DURATION: {probe_duration(final_path):.2f} seconds")
    print("=" * 70)
    return final_path


if __name__ == "__main__":
    render_scene(SangLesson, "video_03_dem_diem_nguyen_1080p")
