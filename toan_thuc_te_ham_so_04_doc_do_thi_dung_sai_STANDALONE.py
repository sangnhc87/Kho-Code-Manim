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
# 04. Doc do thi thuc te + dao ham + Dung/Sai (FILE NAY)
# 05. Tich phan: quang duong - the tich - luong tich luy
# 06. Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke tu du lieu
# 08. Tong hop Dung/Sai + tra loi ngan kieu TN THPT
#
# Nguyen tac dai han:
# - Uu tien mo hinh thuc te, ham tuong minh, do thi dong.
# - Han che toi da ham an.
# - Moi bai: quan sat -> doc dai luong -> phan tich do thi -> Dung/Sai -> ket luan.
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
        self.add_header_footer(title, "TÌNH HUỐNG", progress)
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

    def make_axes(self, xr, yr, xlen=6.9, ylen=5.0, shift=LEFT*2.6):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 26), mtx("y", 26))
        return ax, labels

    def tf_line(self, tag, statement, truth):
        tag_m = txt(tag, 24, GOLD, BOLD)
        if isinstance(statement, Mobject):
            s = statement
        else:
            s = txt(statement, 23, INK)
        chip = txt("ĐÚNG" if truth else "SAI", 22, GREEN if truth else RED, BOLD)
        chip_box = RoundedRectangle(width=1.15, height=0.48, corner_radius=0.12,
                                    stroke_color=GREEN if truth else RED, stroke_width=1.5,
                                    fill_color=GREEN if truth else RED, fill_opacity=0.10)
        chip_group = VGroup(chip_box, chip)
        chip.move_to(chip_box)
        row = VGroup(tag_m, s, chip_group).arrange(RIGHT, buff=0.18)
        return row

    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("TOÁN THỰC TẾ HÀM SỐ – VIDEO 04", 43, GOLD, BOLD),
            txt("ĐỌC ĐỒ THỊ + ĐẠO HÀM + CÂU ĐÚNG/SAI", 36, INK, BOLD),
            txt("Nhìn đúng đại lượng trước khi tính", 29, CYAN),
            VGroup(mtx(r"f", 35, BLUE), txt("không phải", 24, MUTED), mtx(r"f'", 35, ORANGE)).arrange(RIGHT, buff=0.18),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.30)
        self.play(FadeIn(g[0], shift=UP*0.15), run_time=0.6)
        self.play(FadeIn(g[1]), FadeIn(g[2]), Write(g[3]), FadeIn(g[4]), run_time=1.0)
        self.narrate(
            "Chào các em. Video này luyện một kỹ năng rất quan trọng của toán thực tế: đọc đúng đồ thị trước khi bấm máy hay lấy đạo hàm. Một đồ thị có thể biểu diễn nhiệt độ, lợi nhuận, quãng đường phanh, số xe trong bãi hoặc tốc độ thay đổi của một đại lượng. Những câu đúng sai thường không khó ở phép tính, mà khó ở chỗ người làm nhầm ý nghĩa của giá trị hàm với đạo hàm, nhầm cực đại với tốc độ thay đổi, hoặc quên rằng tại điểm gãy đạo hàm có thể không tồn tại.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Ba câu hỏi trước mọi đồ thị", "Đọc nghĩa trước – tính sau", "Mở đầu")
        steps = VGroup(
            bullet("Trục ngang là gì? Đơn vị gì? Miền thực tế ở đâu?", INK, 27, BLUE),
            bullet("Trục đứng là đại lượng gốc hay tốc độ thay đổi?", INK, 27, CYAN),
            bullet("Đồ thị đang tăng, giảm, nằm ngang hay có điểm gãy?", INK, 27, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.52).shift(UP*0.2)
        for s in steps:
            self.play(FadeIn(s, shift=RIGHT*0.12), run_time=0.4)
        self.narrate(
            "Trước một đồ thị, hãy tự hỏi ba câu. Trục ngang biểu diễn gì và miền thực tế là gì. Trục đứng là đại lượng gốc hay là tốc độ thay đổi của đại lượng đó. Cuối cùng, đồ thị đang tăng, giảm, nằm ngang hay có điểm gãy. Chỉ ba câu hỏi này đã loại được rất nhiều bẫy.",
            1.7,
        )

    def model1_temperature(self):
        self.show_problem(
            "Bài 1 – Nhiệt độ lò sấy",
            [
                txt("Trong 8 phút đầu, nhiệt độ được mô hình bởi", 27, INK),
                mtx(r"T(t)=20+8t-t^2,\qquad 0\le t\le 8", 40, GOLD),
                txt("Đơn vị: t tính bằng phút, T tính bằng độ C.", 25, MUTED),
                txt("Quan sát đồ thị và xét 4 mệnh đề Đúng/Sai.", 27, CYAN, BOLD),
            ],
            "Nhiệt độ của một lò sấy trong tám phút đầu được mô hình bằng một parabol. Đây là bài rất điển hình để phân biệt giá trị hàm với đạo hàm. Ta sẽ cho một điểm chạy theo thời gian, nhìn đường dóng xuống hai trục rồi mới đánh giá từng mệnh đề.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 1 – Nhiệt độ lò sấy", "Điểm quét theo thời gian", "1/5")
        ax, labels = self.make_axes((0,9,1),(15,40,5),xlen=6.8,ylen=4.9,shift=LEFT*2.7)
        curve = ax.plot(lambda x: 20+8*x-x*x, x_range=[0,8], color=BLUE, stroke_width=4)
        t = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(),20+8*t.get_value()-t.get_value()**2), radius=0.075, color=GOLD))
        vline = always_redraw(lambda: DashedLine(ax.c2p(t.get_value(),15), dot.get_center(), color=MUTED, dash_length=0.10))
        hline = always_redraw(lambda: DashedLine(ax.c2p(0,20+8*t.get_value()-t.get_value()**2), dot.get_center(), color=MUTED, dash_length=0.10))
        formula = VGroup(
            mtx(r"T'(t)=8-2t",34,CYAN),
            mtx(r"T'(4)=0",34,GOLD),
            mtx(r"T(4)=36",38,GREEN),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.55).shift(UP*0.8)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(formula),run_time=1.0)
        self.play(FadeIn(dot),Create(vline),Create(hline),run_time=0.6)
        self.narrate_play(
            "Cho thời gian chạy từ không đến tám phút. Nhiệt độ tăng dần, đạt đỉnh ở phút thứ tư rồi giảm dần. Điểm cao nhất trên đồ thị cho nhiệt độ lớn nhất, còn hệ số góc của tiếp tuyến tại đó bằng không.",
            t.animate.set_value(8.0),min_time=5.0,
        )

        rows = VGroup(
            self.tf_line("a)", VGroup(mtx(r"T(2)=32",28,INK), txt("độ C",22,INK)).arrange(RIGHT,buff=0.12), True),
            self.tf_line("b)", VGroup(txt("Nhiệt độ lớn nhất là",22,INK),mtx(r"36",28,GOLD),txt("độ C tại",22,INK),mtx(r"t=4",28,GOLD)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("c)", VGroup(mtx(r"T'(6)<0",28,INK),txt("nên nhiệt độ đang giảm",22,INK)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("d)", mtx(r"T'(4)=36",28,INK), False),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30).to_edge(RIGHT,buff=0.25).shift(DOWN*1.20)
        fit_width(rows,6.25)
        self.play(FadeIn(rows),run_time=0.8)
        self.narrate(
            "Mệnh đề a đúng vì T của hai bằng ba mươi hai. Mệnh đề b đúng: nhiệt độ lớn nhất là ba mươi sáu độ tại phút thứ tư. Mệnh đề c đúng vì đạo hàm tại sáu âm, nên nhiệt độ đang giảm. Mệnh đề d sai rất điển hình: ba mươi sáu là giá trị T của bốn, còn T phẩy của bốn bằng không. Đừng đánh tráo đại lượng với tốc độ thay đổi của nó.",
            2.1,
        )

    def model2_profit(self):
        self.show_problem(
            "Bài 2 – Lợi nhuận theo giá bán",
            [
                txt("Lợi nhuận ước tính theo giá p được cho bởi", 27, INK),
                mtx(r"P(p)=900-2(p-70)^2,\qquad 50\le p\le 90",40,GOLD),
                txt("P tính bằng triệu đồng, p tính bằng nghìn đồng.",25,MUTED),
                txt("Đọc đồ thị trước khi kết luận về giá tối ưu.",27,CYAN,BOLD),
            ],
            "Một doanh nghiệp có mô hình lợi nhuận theo giá bán là một parabol quay xuống. Đây là dạng câu rất dễ xuất hiện trong bối cảnh thực tế: không hỏi trực tiếp tìm cực đại, mà đưa bốn nhận định về giá, lợi nhuận và xu hướng tăng giảm.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 2 – Lợi nhuận theo giá bán", "Giá thay đổi – điểm lợi nhuận chạy theo", "2/5")
        ax, labels = self.make_axes((50,95,10),(0,1000,200),xlen=6.9,ylen=5.0,shift=LEFT*2.7)
        curve = ax.plot(lambda p: 900-2*(p-70)**2, x_range=[50,90], color=BLUE, stroke_width=4)
        p = ValueTracker(50)
        dot = always_redraw(lambda: Dot(ax.c2p(p.get_value(),900-2*(p.get_value()-70)**2),radius=0.075,color=GOLD))
        tangent = always_redraw(lambda: ax.plot(
            lambda x: (900-2*(p.get_value()-70)**2) + (-4*(p.get_value()-70))*(x-p.get_value()),
            x_range=[max(50,p.get_value()-7),min(90,p.get_value()+7)],color=ORANGE,stroke_width=3
        ))
        info = VGroup(
            mtx(r"P'(p)=-4(p-70)",34,CYAN),
            mtx(r"P'(70)=0",34,GOLD),
            mtx(r"P_{\max}=900",37,GREEN),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.55).shift(UP*0.9)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(info),run_time=1.0)
        self.play(FadeIn(dot),Create(tangent),run_time=0.6)
        self.narrate_play(
            "Khi giá tăng từ năm mươi đến bảy mươi nghìn, điểm lợi nhuận đi lên và tiếp tuyến có hệ số góc dương. Qua mốc bảy mươi, tiếp tuyến đổi sang hệ số góc âm và lợi nhuận giảm. Mốc bảy mươi chính là điểm cân bằng của hai xu hướng.",
            p.animate.set_value(90),min_time=5.0,
        )

        rows = VGroup(
            self.tf_line("a)", mtx(r"P(60)=700",28,INK), True),
            self.tf_line("b)", VGroup(txt("Giá tối ưu là",22,INK),mtx(r"p=70",28,GOLD)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("c)", VGroup(mtx(r"P'(60)>0",28,INK),txt("nên tăng giá nhẹ quanh 60 làm P tăng",21,INK)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("d)", txt("Tăng giá từ 70 lên 75 làm lợi nhuận tăng",22,INK), False),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30).to_edge(RIGHT,buff=0.22).shift(DOWN*1.20)
        fit_width(rows,6.3)
        self.play(FadeIn(rows),run_time=0.8)
        self.narrate(
            "Mệnh đề a đúng vì P của sáu mươi bằng bảy trăm. Mệnh đề b đúng: đỉnh parabol ở p bằng bảy mươi và lợi nhuận tối đa bằng chín trăm triệu. Mệnh đề c đúng vì P phẩy tại sáu mươi dương; quanh mức giá này tăng giá một lượng nhỏ làm lợi nhuận tăng. Mệnh đề d sai vì bảy mươi đã là điểm cực đại, đi sang bảy mươi lăm thì lợi nhuận giảm.",
            2.0,
        )

    def model3_braking(self):
        self.show_problem(
            "Bài 3 – Quãng đường phanh và tốc độ",
            [
                txt("Một mô hình thử nghiệm cho quãng đường phanh",27,INK),
                mtx(r"d(v)=0.005v^2+0.3v,\qquad 20\le v\le100",40,GOLD),
                txt("d tính bằng mét, v tính bằng km/h.",25,MUTED),
                txt("Điểm khó: đọc ý nghĩa của đạo hàm theo đơn vị.",27,CYAN,BOLD),
            ],
            "Bài ba nói về quãng đường phanh theo tốc độ. Điểm quan trọng không chỉ là biết đồ thị tăng, mà còn hiểu đạo hàm d phẩy của v mang đơn vị mét trên mỗi ki lô mét trên giờ. Nó cho tốc độ tăng cục bộ của quãng đường phanh khi tốc độ xe thay đổi.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 3 – Quãng đường phanh", "Tiếp tuyến cho tốc độ thay đổi cục bộ", "3/5")
        ax, labels = self.make_axes((20,110,20),(0,90,20),xlen=6.9,ylen=5.0,shift=LEFT*2.7)
        curve = ax.plot(lambda v: 0.005*v*v+0.3*v, x_range=[20,100],color=BLUE,stroke_width=4)
        v = ValueTracker(30)
        def dval():
            vv=v.get_value(); return 0.005*vv*vv+0.3*vv
        def slope():
            return 0.01*v.get_value()+0.3
        dot=always_redraw(lambda: Dot(ax.c2p(v.get_value(),dval()),radius=0.075,color=GOLD))
        tang=always_redraw(lambda: ax.plot(lambda x: dval()+slope()*(x-v.get_value()),
                                           x_range=[max(20,v.get_value()-13),min(100,v.get_value()+13)],
                                           color=ORANGE,stroke_width=3))
        info=VGroup(
            mtx(r"d'(v)=0.01v+0.3",34,CYAN),
            mtx(r"d(60)=36",34,GOLD),
            mtx(r"d'(60)=0.9",34,GREEN),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.55).shift(UP*0.85)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(info),run_time=1.0)
        self.play(FadeIn(dot),Create(tang),run_time=0.6)
        self.narrate_play(
            "Khi tốc độ tăng, không chỉ quãng đường phanh tăng mà độ dốc của đồ thị cũng tăng. Điều đó có nghĩa là ở vùng tốc độ cao, thêm cùng một lượng tốc độ sẽ làm quãng đường phanh tăng nhiều hơn so với vùng tốc độ thấp.",
            v.animate.set_value(95),min_time=5.0,
        )

        rows=VGroup(
            self.tf_line("a)", VGroup(mtx(r"d(60)=36",28,INK),txt("m",22,INK)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("b)", VGroup(mtx(r"d'(60)=0.9",28,INK),txt("m/(km/h)",21,INK)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("c)", txt("Quanh 60 km/h, tăng 1 km/h làm d tăng xấp xỉ 0.9 m",21,INK), True),
            self.tf_line("d)", txt("Gấp đôi tốc độ thì quãng đường phanh cũng gấp đôi",21,INK), False),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30).to_edge(RIGHT,buff=0.20).shift(DOWN*1.25)
        fit_width(rows,6.35)
        self.play(FadeIn(rows),run_time=0.8)
        self.narrate(
            "Ba mệnh đề đầu đúng. Tại sáu mươi ki lô mét trên giờ, quãng đường phanh là ba mươi sáu mét và đạo hàm bằng không phẩy chín. Vì vậy tăng thêm một ki lô mét trên giờ ở gần mốc sáu mươi làm quãng đường phanh tăng xấp xỉ không phẩy chín mét. Mệnh đề cuối sai: do có thành phần bình phương, gấp đôi tốc độ không làm quãng đường phanh chỉ gấp đôi.",
            2.0,
        )

    def model4_parking_piecewise(self):
        self.show_problem(
            "Bài 4 – Số xe trong bãi theo thời gian",
            [
                txt("Một bãi xe được mô hình hóa bởi hàm nhiều công thức",27,INK),
                mtx(r"N(t)=\begin{cases}20+30t,&0\le t\le2\\80,&2<t\le4\\160-20t,&4<t\le7\end{cases}",37,GOLD),
                txt("t tính bằng giờ, N(t) là số xe.",25,MUTED),
                txt("Hãy đặc biệt chú ý hai điểm gãy t=2 và t=4.",27,CYAN,BOLD),
            ],
            "Đây là bài rất hợp để kiểm tra hiểu biết về hàm nhiều công thức. Hai giờ đầu xe vào nhanh, hai giờ tiếp theo số xe giữ nguyên, sau đó xe rời bãi. Đồ thị liên tục nhưng có điểm gãy, vì tốc độ thay đổi ở hai phía không giống nhau.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 4 – Bãi xe", "Đồ thị liên tục nhưng đạo hàm có thể không tồn tại", "4/5")
        ax, labels = self.make_axes((0,8,1),(0,100,20),xlen=6.9,ylen=5.0,shift=LEFT*2.7)
        s1=ax.plot(lambda x:20+30*x,x_range=[0,2],color=BLUE,stroke_width=4)
        s2=ax.plot(lambda x:80,x_range=[2,4],color=CYAN,stroke_width=4)
        s3=ax.plot(lambda x:160-20*x,x_range=[4,7],color=ORANGE,stroke_width=4)
        t=ValueTracker(0)
        def nval():
            tt=t.get_value()
            if tt<=2: return 20+30*tt
            if tt<=4: return 80
            return 160-20*tt
        dot=always_redraw(lambda: Dot(ax.c2p(t.get_value(),nval()),radius=0.075,color=GOLD))
        vline=always_redraw(lambda: DashedLine(ax.c2p(t.get_value(),0),dot.get_center(),color=MUTED,dash_length=0.10))
        breaks=VGroup(DashedLine(ax.c2p(2,0),ax.c2p(2,90),color=RED,dash_length=0.12),
                      DashedLine(ax.c2p(4,0),ax.c2p(4,90),color=RED,dash_length=0.12))
        info=VGroup(
            mtx(r"N'_-(2)=30",32,BLUE),
            mtx(r"N'_+(2)=0",32,CYAN),
            mtx(r"N'_-(2)\ne N'_+(2)",32,RED),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.48).shift(UP*0.85)
        self.play(Create(ax),FadeIn(labels),Create(s1),Create(s2),Create(s3),FadeIn(breaks),FadeIn(info),run_time=1.0)
        self.play(FadeIn(dot),Create(vline),run_time=0.6)
        self.narrate_play(
            "Điểm vàng đi qua ba giai đoạn. Từ không đến hai giờ, số xe tăng tuyến tính. Từ hai đến bốn giờ, đồ thị nằm ngang nên số xe không đổi. Sau bốn giờ, đồ thị đi xuống nên số xe giảm. Tại các điểm chuyển chế độ, đồ thị không bị đứt nhưng độ dốc đổi đột ngột.",
            t.animate.set_value(7.0),min_time=5.0,
        )

        rows=VGroup(
            self.tf_line("a)", mtx(r"N(1)=50",28,INK), True),
            self.tf_line("b)", txt("Từ giờ thứ 2 đến giờ thứ 4, số xe không đổi",21,INK), True),
            self.tf_line("c)", mtx(r"N'(3)=0",28,INK), True),
            self.tf_line("d)", mtx(r"N'(2)=0",28,INK), False),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30).to_edge(RIGHT,buff=0.22).shift(DOWN*1.23)
        fit_width(rows,6.2)
        self.play(FadeIn(rows),run_time=0.8)
        self.narrate(
            "Mệnh đề a đúng vì sau một giờ có năm mươi xe. Mệnh đề b đúng vì đoạn đồ thị từ hai đến bốn giờ nằm ngang. Mệnh đề c đúng vì bên trong đoạn nằm ngang, đạo hàm bằng không. Nhưng d sai: tại đúng t bằng hai, hệ số góc bên trái là ba mươi còn bên phải là không, nên đạo hàm tại điểm gãy không tồn tại. Liên tục không đồng nghĩa với khả vi.",
            2.1,
        )

    def model5_derivative_graph(self):
        self.show_problem(
            "Bài 5 – Chỉ cho đồ thị tốc độ thay đổi",
            [
                txt("Q(t) là lượng khách trong một khu dịch vụ.",27,INK),
                txt("Thay vì cho Q(t), đề cho trực tiếp",27,INK),
                mtx(r"Q'(t)=(t-2)(6-t),\qquad 0\le t\le8",40,GOLD),
                txt("Từ đồ thị Q'(t), hãy suy luận về Q(t).",27,CYAN,BOLD),
            ],
            "Bài cuối là mức khó hơn. Đề không cho đồ thị lượng khách Q mà cho đồ thị tốc độ thay đổi Q phẩy. Ta không cần tìm công thức Q. Chỉ cần đọc dấu của Q phẩy để biết Q đang tăng hay giảm, và tìm các thời điểm Q đạt cực trị.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 5 – Đồ thị Q'(t)", "Dấu của đạo hàm kể câu chuyện của Q", "5/5")
        ax, labels = self.make_axes((0,9,1),(-15,20,5),xlen=6.9,ylen=5.0,shift=LEFT*2.7)
        curve=ax.plot(lambda x:(x-2)*(6-x),x_range=[0,8],color=BLUE,stroke_width=4)
        axis0=Line(ax.c2p(0,0),ax.c2p(8,0),color=MUTED,stroke_width=2)
        t=ValueTracker(0)
        dot=always_redraw(lambda: Dot(ax.c2p(t.get_value(),(t.get_value()-2)*(6-t.get_value())),radius=0.075,color=GOLD))
        scan=always_redraw(lambda: DashedLine(ax.c2p(t.get_value(),-15),ax.c2p(t.get_value(),20),color=MUTED,dash_length=0.10))
        sign=VGroup(
            VGroup(mtx(r"Q'<0",28,RED),mtx(r"(0,2)",28,INK)).arrange(RIGHT,buff=0.12),
            VGroup(mtx(r"Q'>0",28,GREEN),mtx(r"(2,6)",28,INK)).arrange(RIGHT,buff=0.12),
            VGroup(mtx(r"Q'<0",28,RED),mtx(r"(6,8)",28,INK)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,buff=0.26).to_edge(RIGHT,buff=0.65).shift(UP*0.9)
        self.play(Create(ax),FadeIn(labels),Create(axis0),Create(curve),FadeIn(sign),run_time=1.0)
        self.play(FadeIn(dot),Create(scan),run_time=0.6)
        self.narrate_play(
            "Quét từ trái sang phải. Khi đồ thị Q phẩy nằm dưới trục ngang, Q đang giảm. Từ hai đến sáu, Q phẩy dương nên Q tăng. Sau sáu, Q phẩy âm trở lại nên Q lại giảm. Ta không hề cần biết Q có công thức cụ thể thế nào.",
            t.animate.set_value(8.0),min_time=5.0,
        )
        extrema=VGroup(
            VGroup(mtx(r"t=2",30,GOLD),txt("Q đổi giảm → tăng: cực tiểu",22,INK)).arrange(RIGHT,buff=0.12),
            VGroup(mtx(r"t=6",30,GOLD),txt("Q đổi tăng → giảm: cực đại",22,INK)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.35).shift(DOWN*0.25)
        self.play(FadeIn(extrema),run_time=0.7)

        rows=VGroup(
            self.tf_line("a)", VGroup(txt("Q giảm trên",21,INK),mtx(r"(0,2)",27,INK)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("b)", VGroup(mtx(r"t=2",27,INK),txt("là thời điểm Q đạt cực tiểu",21,INK)).arrange(RIGHT,buff=0.10), True),
            self.tf_line("c)", VGroup(mtx(r"Q'(4)>0",27,INK),txt("suy ra",21,INK),mtx(r"Q(4)>0",27,INK)).arrange(RIGHT,buff=0.10), False),
            self.tf_line("d)", VGroup(mtx(r"t=6",27,INK),txt("là thời điểm Q đạt cực đại",21,INK)).arrange(RIGHT,buff=0.10), True),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.28).to_edge(RIGHT,buff=0.15).shift(DOWN*1.45)
        fit_width(rows,6.4)
        self.play(FadeIn(rows),run_time=0.8)
        self.narrate(
            "Các mệnh đề a, b và d đều đúng theo bảng dấu của Q phẩy. Mệnh đề c sai rất tinh tế: Q phẩy của bốn dương chỉ nói rằng tại thời điểm đó Q đang tăng. Nó hoàn toàn không cho biết bản thân Q của bốn dương hay âm. Đây là một trong những kiểu đánh tráo đại lượng dễ gặp nhất khi đề cho đồ thị đạo hàm.",
            2.1,
        )

    def summary(self):
        self.clear_stage(); self.add_header_footer("Bản đồ xử lý câu Đúng/Sai từ đồ thị", "5 bước ngắn nhưng rất chắc", "Tổng kết")
        steps=VGroup(
            bullet("1. Đọc tên hai trục và đơn vị trước khi nhìn hình dạng.",INK,26,BLUE),
            bullet("2. Xác định đồ thị là f hay f'.",INK,26,CYAN),
            bullet("3. Giá trị hàm: đọc độ cao; đạo hàm: đọc độ dốc hoặc dấu.",INK,26,GOLD),
            bullet("4. Kiểm tra điểm gãy: liên tục chưa chắc có đạo hàm.",INK,26,ORANGE),
            bullet("5. Mỗi mệnh đề phải được dịch lại thành một câu toán học rõ ràng.",INK,26,GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34).shift(DOWN*0.05)
        for s in steps:
            self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.34)
        self.narrate(
            "Chốt lại năm bước. Đọc đúng trục và đơn vị. Xác định đang nhìn f hay f phẩy. Giá trị hàm được đọc bằng độ cao, còn đạo hàm liên quan đến độ dốc hoặc dấu. Tại điểm gãy phải kiểm tra riêng vì liên tục chưa chắc có đạo hàm. Và cuối cùng, hãy dịch mỗi nhận định về một câu toán học trước khi phán đúng hay sai.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Bài thử thách cuối video", "Một bẫy f và f' rất thường gặp", "Tổng kết")
        q=VGroup(
            txt("Biết đồ thị của",27,INK),
            mtx(r"v(t)=12-2t,\qquad 0\le t\le6",40,GOLD),
            txt("biểu diễn vận tốc của một vật, đơn vị m/s.",26,INK),
            txt("Xét hai nhận định:",27,CYAN,BOLD),
            VGroup(txt("A.",24,GOLD,BOLD),mtx(r"v(3)=6",30,INK)).arrange(RIGHT,buff=0.15),
            VGroup(txt("B.",24,GOLD,BOLD),mtx(r"v'(3)=6",30,INK)).arrange(RIGHT,buff=0.15),
        ).arrange(DOWN,buff=0.26)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate(
            "Bài cuối rất ngắn. V của t bằng mười hai trừ hai t là vận tốc. Tại t bằng ba, vận tốc bằng sáu mét trên giây nên A đúng. Nhưng đạo hàm của v là âm hai, mang ý nghĩa gia tốc. Vì vậy B sai. Một lần nữa, giá trị của hàm và tốc độ thay đổi của hàm là hai đại lượng khác nhau.",
            1.7,
        )
        ans=VGroup(self.tf_line("A",mtx(r"v(3)=6",29,INK),True),self.tf_line("B",mtx(r"v'(3)=6",29,INK),False)).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.7)
        self.play(FadeIn(ans),run_time=0.7)

        self.clear_stage(); self.add_header_footer("Kế hoạch series", "Video 05: tích phân trong bài toán thực tế", "Tổng kết")
        roadmap=VGroup(
            VGroup(mtx(r"01",30,MUTED),txt("Mô hình hóa + tối ưu một biến",25,MUTED)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"02",30,MUTED),txt("Hàm nhiều công thức: ngưỡng – phí – sức chứa",25,MUTED)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"03",30,MUTED),txt("Tốc độ – thời gian – năng suất – chi phí",25,MUTED)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"04",30,GOLD),txt("Đọc đồ thị thực tế + Đúng/Sai",25,GOLD,BOLD)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"05",30,CYAN),txt("Tích phân: quãng đường – lượng tích lũy – thể tích",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"06\to08",30,ORANGE),txt("Oxyz – xác suất thống kê – tổng hợp thi",25,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.27)
        fit_width(roadmap,11.6)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.1) for r in roadmap],lag_ratio=0.09),run_time=1.3)
        self.narrate(
            "Video tiếp theo sẽ nối rất tự nhiên từ đồ thị sang tích phân. Khi trục đứng là tốc độ, lưu lượng hay công suất, diện tích dưới đồ thị sẽ mang một ý nghĩa thực tế mới: quãng đường, lượng nước, điện năng hoặc tổng lượng tích lũy. Ta sẽ ưu tiên hình động và bài toán thực tế, không dùng hàm ẩn.",
            1.8,
        )

        self.clear_stage()
        end=VGroup(
            txt("ĐỌC ĐÚNG ĐẠI LƯỢNG – TRÁNH BẪY ĐÚNG/SAI",38,GOLD,BOLD),
            mtx(r"f\ \neq\ f'",44,CYAN),
            txt(TEN_THAY,22,MUTED),
        ).arrange(DOWN,buff=0.42)
        fit_width(end,11.8)
        self.play(FadeIn(end[0]),Write(end[1]),FadeIn(end[2]),run_time=0.9)
        self.narrate(
            "Nếu chỉ nhớ một điều sau video này, hãy nhớ rằng f và f phẩy kể hai câu chuyện khác nhau. Một cái cho giá trị của đại lượng, cái kia cho tốc độ thay đổi. Đọc đúng câu chuyện trước, phép tính sau đó thường rất ngắn.",
            1.5,
        )

    def construct(self):
        self.intro()
        self.model1_temperature()
        self.model2_profit()
        self.model3_braking()
        self.model4_parking_piecewise()
        self.model5_derivative_graph()
        self.summary()


def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_04_doc_do_thi_dung_sai_1080p"
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
    master_wav = ROOT / "master_narration_toan_thuc_te_ham_so_04.wav"
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
