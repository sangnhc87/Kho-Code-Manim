# ==========================================================
# STANDALONE MANIM LESSON - NO LOCAL MODULE DEPENDENCIES
# Generated for GitHub Actions
# ==========================================================
from manim import *
from pathlib import Path
import hashlib, json, subprocess, sys, time

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

def fit_width(mob, width=12.4):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob

def make_panel(width=12.2, height=5.4):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.18,
        fill_color=PANEL, fill_opacity=0.90,
        stroke_color=MUTED, stroke_opacity=0.22, stroke_width=1.5,
    )

def title_block(title, subtitle=None):
    t = fit_width(txt(title, 38, INK, BOLD), 12.0).to_edge(UP, buff=0.25)
    if subtitle:
        s = fit_width(txt(subtitle, 23, MUTED), 11.5).next_to(t, DOWN, buff=0.10)
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
    t = fit_width(txt(text, size, color), 10.9)
    return VGroup(d, t).arrange(RIGHT, buff=0.18, aligned_edge=UP)

def label_point(axes, x, y, name, color=CYAN, direction=UR):
    d = Dot(axes.c2p(x, y), radius=0.055, color=color)
    lab = mtx(name, 28, color).next_to(d, direction, buff=0.08)
    return VGroup(d, lab)

def math_row(lhs, rhs=None, color=INK, size=34, gap=0.20):
    if rhs is None:
        return mtx(lhs, size, color)
    return VGroup(mtx(lhs, size, color), mtx(rhs, size, color)).arrange(RIGHT, buff=gap)

def _audio_key(text):
    payload = json.dumps({
        "text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC,
        "pitch": PITCH, "engine": "edge-tts"
    }, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]

def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(out)

def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError(f"Audio không hợp lệ: {path}")
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
                "import asyncio\nimport edge_tts\n"
                f"text={text!r}\nout={str(out)!r}\nvoice={GIONG_DOC!r}\n"
                f"rate={TOC_DO_DOC!r}\npitch={PITCH!r}\n"
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
    raise RuntimeError(f"Edge TTS thất bại sau 3 lần: {last_err}")

def build_master_audio(events, video_duration, out_wav: Path):
    if not events:
        raise RuntimeError("Không có narration nào để ghép.")
    inputs, filters, labels = [], [], []
    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]adelay={ms}|{ms},aresample=48000[a{i}]")
        labels.append(f"[a{i}]")
    fc = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", fc, "-map", "[m]", "-ar", "48000", "-ac", "2",
        "-t", f"{video_duration:.3f}", str(out_wav)
    ], check=True)

def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)
    ], check=True)

class LessonBase(Scene):
    def setup(self):
        self.audio_events = []

    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def narrate_while(self, text, animation, min_hold=0.2):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        rt = min(max(0.8, dur * 0.62), 4.0)
        self.play(animation, run_time=rt)
        if dur > rt:
            self.wait(dur - rt + min_hold)
        else:
            self.wait(min_hold)
        return dur

    def clear_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.42)

    def add_header_footer(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, blocks, voice, progress):
        self.clear_stage()
        self.add_header_footer(title, "ĐỀ BÀI", progress)
        panel = make_panel(12.35, 5.25).shift(DOWN*0.12)
        self.play(FadeIn(panel), run_time=0.45)
        mobs = VGroup()
        for kind, content, *rest in blocks:
            if kind == "math":
                size = rest[0] if rest else 34
                color = rest[1] if len(rest) > 1 else GOLD
                mob = fit_width(mtx(content, size, color), 11.15)
            else:
                size = rest[0] if rest else 27
                color = rest[1] if len(rest) > 1 else INK
                weight = rest[2] if len(rest) > 2 else NORMAL
                mob = fit_width(txt(content, size, color, weight), 11.15)
            mobs.add(mob)
        mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(panel.get_center()).shift(UP*0.04)
        for mob in mobs:
            self.play(FadeIn(mob, shift=UP*0.05), run_time=0.28)
        self.narrate(voice, 2.0)
        return VGroup(panel, mobs)

def render_scene(scene_cls, output_stem: str):
    config.media_dir = str(MEDIA_DIR)
    config.output_file = output_stem
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False
    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    scene = scene_cls()
    scene.render()
    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Không tìm thấy video Manim cuối: {video_path}")
    video_duration = probe_duration(video_path)
    master_wav = ROOT / f"{output_stem}_master.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)
    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    print("\n============================================================")
    print(f"VIDEO HOÀN CHỈNH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


# ==========================================================
# LESSON CONTENT
# ==========================================================

class SangLesson(LessonBase):
    def intro(self):
        self.clear_stage()
        g=VGroup(
            txt("THAM SỐ VÀ SỐ ĐIỂM NGUYÊN",48,INK,BOLD),
            mtx(r"m\ \longmapsto\ N(m)",44,GOLD),
            txt("Khi miền nghiệm chuyển động, số phương án thay đổi theo bậc thang",28,CYAN),
            txt(TEN_THAY,22,MUTED)
        ).arrange(DOWN,buff=0.28)
        self.play(FadeIn(g),run_time=1.0)
        self.narrate("Chào các em! Đây là video tổng hợp nâng cao của phần hệ bất phương trình. Ta vừa có tham số m làm miền nghiệm thay đổi, vừa yêu cầu các nghiệm phải nguyên. Điều thú vị là số điểm nguyên không thay đổi liên tục theo m. Nó giữ nguyên một thời gian rồi nhảy lên khi đường biên đi qua một lớp điểm lưới mới.",2.0)

        self.clear_stage(); self.add_header_footer("Hai lớp tư duy", "Hình học + số học rời rạc", "Mở đầu")
        g=VGroup(
            VGroup(txt("Lớp 1:",27,GOLD,BOLD),mtx(r"S(m)",36,BLUE),txt("là miền nghiệm phụ thuộc m",27,INK)).arrange(RIGHT,buff=0.20),
            VGroup(txt("Lớp 2:",27,GOLD,BOLD),mtx(r"S(m)\cap\mathbb Z^2",36,GREEN),txt("là các điểm nguyên cần đếm",27,INK)).arrange(RIGHT,buff=0.20),
            mtx(r"N(m)=\#\bigl(S(m)\cap\mathbb Z^2\bigr)",42,GOLD),
        ).arrange(DOWN,buff=0.48)
        self.play(FadeIn(g),run_time=0.9)
        self.narrate("Ta ký hiệu S của m là miền nghiệm thực. Còn N của m là số điểm nguyên thuộc miền đó. Dấu thăng ở đây có nghĩa là số phần tử của tập hợp.",1.4)

    def ex1(self):
        self.show_problem(
            "Ví dụ 1 – Công thức tam giác số",
            [
                ("text","Cho m là số nguyên không âm. Đếm nghiệm:",27,INK,BOLD),
                ("math",r"\begin{cases}x\ge0\\y\ge0\\x+y\le m\end{cases}",42,GOLD),
                ("math",r"x,y\in\mathbb Z",34,CYAN),
                ("text","Tìm m để hệ có đúng 21 nghiệm nguyên.",27,GREEN,BOLD),
            ],
            "Ví dụ một là mô hình nền tảng. Với m nguyên không âm, miền nghiệm là tam giác vuông. Ta sẽ đếm số điểm lưới theo từng hàng và rút ra một công thức tổng quát, sau đó giải ngược để tìm m.",
            "Ví dụ 1/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 1", "Từ tổng số học đến công thức", "Ví dụ 1/4")
        deriv = VGroup(
            mtx(r"y=0:\quad m+1",31,INK),
            mtx(r"y=1:\quad m",31,INK),
            mtx(r"\vdots",34,MUTED),
            mtx(r"y=m:\quad 1",31,INK),
            mtx(r"N(m)=1+2+\cdots+(m+1)",36,BLUE),
            mtx(r"N(m)=\frac{(m+1)(m+2)}2",42,GOLD),
        ).arrange(DOWN,buff=0.23)
        self.play(FadeIn(deriv),run_time=0.8)
        self.narrate("Ở hàng y bằng không có m cộng một điểm. Hàng tiếp theo có m điểm. Cứ như vậy đến hàng y bằng m chỉ còn một điểm. Tổng là một cộng hai đến m cộng một, nên N của m bằng m cộng một nhân m cộng hai chia hai.",1.9)
        solve=VGroup(
            mtx(r"\frac{(m+1)(m+2)}2=21",38,INK),
            mtx(r"(m+1)(m+2)=42",36,INK),
            mtx(r"m^2+3m-40=0",36,INK),
            mtx(r"(m-5)(m+8)=0",36,INK),
            mtx(r"\boxed{m=5}",44,GOLD)
        ).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.55)
        self.play(FadeIn(solve),run_time=0.9)
        self.narrate("Đặt N bằng hai mươi mốt, ta được phương trình bậc hai. Hai nghiệm là năm và âm tám, nhưng m không âm nên chỉ nhận m bằng năm.",1.4)

    def ex2(self):
        self.show_problem(
            "Ví dụ 2 – m là số thực",
            [
                ("text","Với m là số thực, đếm nghiệm nguyên không âm:",27,INK,BOLD),
                ("math",r"x+y\le m",42,GOLD),
                ("math",r"x,y\in\mathbb Z_{\ge0}",34,CYAN),
                ("text","Tìm m để có đúng 15 nghiệm nguyên.",27,GREEN,BOLD),
            ],
            "Lần này m là số thực. Vì x cộng y luôn là số nguyên, điều quyết định không phải chính m mà là phần nguyên dưới của m. Đây là nơi hàm sàn xuất hiện rất tự nhiên.",
            "Ví dụ 2/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Số điểm thay đổi theo bậc thang", "Ví dụ 2/4")
        g=VGroup(
            mtx(r"n=\lfloor m\rfloor",40,BLUE),
            mtx(r"x+y\le m\ \Longleftrightarrow\ x+y\le n",38,INK),
            mtx(r"N(m)=\frac{(n+1)(n+2)}2",42,GOLD),
        ).arrange(DOWN,buff=0.35).shift(UP*0.7)
        self.play(FadeIn(g),run_time=0.8)
        self.narrate("Đặt n bằng phần nguyên dưới của m. Vì x cộng y là số nguyên, điều kiện x cộng y không vượt quá m tương đương x cộng y không vượt quá n.",1.5)
        solve=VGroup(
            mtx(r"\frac{(n+1)(n+2)}2=15",36,INK),
            mtx(r"n=4",40,GOLD),
            mtx(r"\lfloor m\rfloor=4",38,BLUE),
            mtx(r"\boxed{4\le m<5}",44,GOLD)
        ).arrange(DOWN,buff=0.28).shift(DOWN*1.2)
        self.play(FadeIn(solve),run_time=0.8)
        self.narrate("Mười lăm điểm tương ứng n bằng bốn. Điều kiện phần nguyên dưới của m bằng bốn tương đương bốn nhỏ hơn hoặc bằng m và m nhỏ hơn năm. Ta thu được cả một khoảng giá trị của m, không chỉ một số.",1.8)

    def ex3(self):
        self.show_problem(
            "Ví dụ 3 – Công thức phụ thuộc chẵn lẻ",
            [
                ("text","Cho m là số nguyên không âm. Đếm nghiệm:",27,INK,BOLD),
                ("math",r"\begin{cases}2x+y\le m\\x\ge0\\y\ge0\end{cases}",42,GOLD),
                ("math",r"x,y\in\mathbb Z",34,CYAN),
                ("text","Tìm m để có đúng 16 nghiệm nguyên.",27,GREEN,BOLD),
            ],
            "Ví dụ ba khó hơn vì hệ số hai trước x làm số điểm phụ thuộc vào m chẵn hay lẻ. Ta sẽ tách hai trường hợp và thu được một hàm nhiều công thức.",
            "Ví dụ 3/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Vì sao phải tách chẵn – lẻ?", "Ví dụ 3/4")
        base=VGroup(
            mtx(r"0\le x\le\left\lfloor\frac m2\right\rfloor",38,BLUE),
            mtx(r"0\le y\le m-2x",38,ORANGE),
            mtx(r"N(m)=\sum_{x=0}^{\lfloor m/2\rfloor}(m-2x+1)",40,GOLD),
        ).arrange(DOWN,buff=0.32).shift(UP*0.75)
        self.play(FadeIn(base),run_time=0.8)
        self.narrate("Với mỗi x từ không đến phần nguyên của m chia hai, y có m trừ hai x cộng một giá trị, kể cả không. Vì giới hạn của x có phần nguyên, ta tách m chẵn và m lẻ.",1.7)
        cases=VGroup(
            mtx(r"m=2k:\quad N=(k+1)^2",40,BLUE),
            mtx(r"m=2k+1:\quad N=(k+1)(k+2)",40,GREEN),
        ).arrange(DOWN,buff=0.42).shift(DOWN*0.65)
        self.play(FadeIn(cases),run_time=0.8)
        self.narrate("Nếu m bằng hai k, tổng các số lẻ cho N bằng k cộng một tất cả bình phương. Nếu m bằng hai k cộng một, ta được tích k cộng một nhân k cộng hai.",1.5)
        solve = VGroup(
            mtx(r"N=16",34,INK),
            mtx(r"(k+1)^2=16\Rightarrow k=3",35,BLUE),
            mtx(r"m=2k=6",40,GOLD),
            mtx(r"(k+1)(k+2)=16",34,GREEN),
            VGroup(txt("Nhánh lẻ:",24,RED),mtx(r"\varnothing",34,RED)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.25)
        self.play(FadeIn(solve),run_time=0.8)
        self.narrate("Đặt N bằng mười sáu. Ở nhánh chẵn, k bằng ba nên m bằng sáu. Ở nhánh lẻ không có k nguyên không âm phù hợp. Vậy m bằng sáu.",1.5)

    def ex4(self):
        self.show_problem(
            "Ví dụ 4 – Dịch miền khỏi gốc tọa độ",
            [
                ("text","Cho m là số nguyên. Đếm nghiệm:",27,INK,BOLD),
                ("math",r"\begin{cases}x\ge1\\y\ge1\\x+y\le m\end{cases}",42,GOLD),
                ("math",r"x,y\in\mathbb Z",34,CYAN),
                ("text","Tìm m để có đúng 10 nghiệm nguyên.",27,GREEN,BOLD),
            ],
            "Ví dụ bốn là một miền tam giác giống ví dụ đầu nhưng bị dịch khỏi gốc tọa độ. Ta sẽ đổi biến để đưa nó về dạng quen thuộc.",
            "Ví dụ 4/4")
        self.clear_stage(); self.add_header_footer("Ví dụ 4", "Đổi biến để quay về tam giác chuẩn", "Ví dụ 4/4")
        sub=VGroup(
            mtx(r"u=x-1,\qquad v=y-1",40,BLUE),
            mtx(r"u,v\in\mathbb Z_{\ge0}",34,CYAN),
            mtx(r"u+v\le m-2",38,GOLD),
            mtx(r"N=\frac{(m-1)m}{2}",42,GOLD),
        ).arrange(DOWN,buff=0.30).shift(UP*0.45)
        self.play(FadeIn(sub),run_time=0.8)
        self.narrate("Đặt u bằng x trừ một và v bằng y trừ một. Khi đó u và v không âm, còn điều kiện tổng trở thành u cộng v không vượt quá m trừ hai. Công thức tam giác cho N bằng m trừ một nhân m chia hai.",1.7)
        solve=VGroup(
            mtx(r"\frac{m(m-1)}2=10",38,INK),
            mtx(r"m^2-m-20=0",36,INK),
            mtx(r"(m-5)(m+4)=0",36,INK),
            mtx(r"\boxed{m=5}",44,GOLD)
        ).arrange(DOWN,buff=0.26).shift(DOWN*1.45)
        self.play(FadeIn(solve),run_time=0.8)
        self.narrate("Giải phương trình ta được m bằng năm hoặc âm bốn. Điều kiện hệ có nghiệm nguyên với x y ít nhất bằng một loại nghiệm âm, nên m bằng năm.",1.4)


    def ex5_application(self):
        self.show_problem(
            "Ví dụ 5 – Ngưỡng ngân sách và số phương án",
            [
                ("text","Một kế hoạch dùng x gói A và y gói B, với:",27,INK,BOLD),
                ("math",r"2x+3y\le m",42,GOLD),
                ("math",r"x,y\in\mathbb Z_{\ge0}",34,CYAN),
                ("text","Tìm số nguyên nhỏ nhất m để có ít nhất 12 phương án.",27,GREEN,BOLD),
            ],
            "Ví dụ năm là một bài tham số mang ý nghĩa thực tế. Mỗi gói A tiêu tốn hai đơn vị ngân sách, mỗi gói B tiêu tốn ba đơn vị. Với ngân sách m nguyên, ta cần tìm ngưỡng nhỏ nhất để xuất hiện ít nhất mười hai phương án nguyên không âm.",
            "Ví dụ 5/5")
        self.clear_stage(); self.add_header_footer("Ví dụ 5", "Tìm ngưỡng bằng cách theo dõi N(m)", "Ví dụ 5/5")
        intro=VGroup(
            mtx(r"N(m)=\#\{(x,y)\in\mathbb Z_{\ge0}^2:2x+3y\le m\}",34,GOLD),
            txt("N(m) tăng theo bậc thang khi m tăng.",27,CYAN)
        ).arrange(DOWN,buff=0.35).shift(UP*1.0)
        self.play(FadeIn(intro),run_time=0.7)
        self.narrate("Vì m tăng thì miền nghiệm chỉ có thể rộng thêm, N của m là một hàm không giảm. Ta không cần thử mọi số từ đầu nếu đã biết ngưỡng đang nằm gần đâu; chỉ cần kiểm tra liên tiếp cho đến khi số phương án đạt yêu cầu.",1.6)
        table=VGroup(
            mtx(r"N(6)=7",32,INK),
            mtx(r"N(7)=8",32,INK),
            mtx(r"N(8)=10",32,INK),
            mtx(r"N(9)=12",36,GOLD),
        ).arrange(RIGHT,buff=0.55).shift(DOWN*0.15)
        self.play(FadeIn(table),run_time=0.8)
        self.narrate("Với m bằng sáu có bảy phương án. m bằng bảy có tám. m bằng tám có mười. Đến m bằng chín, số phương án vừa đạt mười hai. Vì N của m không giảm, đây chính là ngân sách nguyên nhỏ nhất cần tìm.",1.7)
        ans=mtx(r"\boxed{m_{\min}=9}",44,GOLD).shift(DOWN*1.4)
        self.play(Write(ans),run_time=0.5)
        self.narrate("Kết luận: m nhỏ nhất bằng chín. Bài này cho các em thấy một dạng câu hỏi rất thực tế: tìm ngưỡng nguồn lực tối thiểu để có đủ số phương án lựa chọn.",1.4)

        self.clear_stage(); self.add_header_footer("Kiểm tra riêng N(9)", "Quét theo số gói B", "Ví dụ 5/5")
        rows=VGroup(
            mtx(r"y=0:\ 0\le x\le4\Rightarrow5",30,INK),
            mtx(r"y=1:\ 0\le x\le3\Rightarrow4",30,INK),
            mtx(r"y=2:\ 0\le x\le1\Rightarrow2",30,INK),
            mtx(r"y=3:\ x=0\Rightarrow1",30,INK),
            mtx(r"5+4+2+1=12",38,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.22)
        self.play(FadeIn(rows),run_time=0.7)
        self.narrate("Để chắc chắn, ta kiểm tra N của chín. y bằng không cho năm giá trị x; y bằng một cho bốn; y bằng hai cho hai; y bằng ba chỉ có x bằng không. Tổng đúng bằng mười hai.",1.5)


    def step_behavior(self):
        self.clear_stage(); self.add_header_footer("Vì sao N(m) là hàm bậc thang?", "Miền chuyển động liên tục nhưng điểm lưới là rời rạc", "Mở rộng")
        g=VGroup(
            VGroup(mtx(r"m\uparrow",36,BLUE),txt("đường biên dịch chuyển liên tục",27,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"N(m)",36,GOLD),txt("chỉ tăng khi biên vượt qua điểm nguyên mới",27,INK)).arrange(RIGHT,buff=0.25),
            mtx(r"N(m^+)\ge N(m)",38,GREEN),
        ).arrange(DOWN,buff=0.42).shift(UP*0.35)
        self.play(FadeIn(g),run_time=0.8)
        self.narrate("Có một ý rất đẹp: miền nghiệm thay đổi liên tục khi m thay đổi, nhưng các điểm nguyên nằm rời rạc. Vì vậy có những khoảng m thay đổi mà chưa có điểm lưới mới nào được thêm vào, nên N của m giữ nguyên. Chỉ khi đường biên đi qua một hoặc nhiều điểm nguyên mới, N mới nhảy lên. Đó là lý do những bài tham số thực thường dẫn đến hàm đếm dạng bậc thang.",2.0)
        self.clear_stage(); self.add_header_footer("Hệ quả khi giải ngược", "Một số lượng có thể ứng với cả một khoảng m", "Mở rộng")
        h=VGroup(
            mtx(r"N(m)=15",40,GOLD),
            mtx(r"4\le m<5",42,BLUE),
            txt("Một giá trị N có thể tương ứng vô số giá trị thực của m.",27,CYAN)
        ).arrange(DOWN,buff=0.35)
        self.play(FadeIn(h),run_time=0.7)
        self.narrate("Vì N là bậc thang, khi m là số thực, phương trình N của m bằng một số cho trước thường không cho một điểm mà cho cả một khoảng. Ví dụ mười lăm điểm trong tam giác x cộng y không vượt quá m xảy ra với mọi m từ bốn đến nhỏ hơn năm. Đây là chỗ rất dễ mất điểm nếu ta chỉ giải như một phương trình thông thường.",2.0)

    def synthesis(self):
        self.clear_stage(); self.add_header_footer("Bản đồ tư duy", "Tham số + điểm nguyên", "Tổng kết")
        steps=VGroup(
            bullet("1. Tìm miền nghiệm S(m) và các ngưỡng hình học của m.",INK,27,BLUE),
            bullet("2. Chuyển sang điều kiện nguyên: dùng sàn, trần, chẵn – lẻ nếu cần.",INK,27,CYAN),
            bullet("3. Đếm theo hàng/cột hoặc biến đổi về tam giác chuẩn.",INK,27,GREEN),
            bullet("4. Lập N(m), có thể là hàm từng đoạn.",INK,27,ORANGE),
            bullet("5. Giải ngược điều kiện N(m)=N_0.",INK,27,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.35).shift(DOWN*0.1)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.35)
        self.narrate("Quy trình tổng hợp gồm năm bước. Xác định miền phụ thuộc m. Chuyển điều kiện sang ngôn ngữ số nguyên. Đếm. Lập hàm N của m, thường là hàm từng đoạn. Cuối cùng giải ngược số điểm theo yêu cầu đề bài.",1.8)

        self.clear_stage(); self.add_header_footer("Bài thử thách", "Một bài có phép trừ miền", "Tự luyện")
        q=VGroup(
            txt("Cho",27,INK),mtx(r"m\in\mathbb Z,\ m\ge2",34,CYAN),
            txt("Đếm các nghiệm nguyên không âm của",27,INK),
            mtx(r"2\le x+y\le m",42,GOLD),
            txt("và tìm m để có đúng 18 nghiệm.",27,GREEN,BOLD)
        ).arrange(DOWN,buff=0.24)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate("Bài thử thách: đếm điểm nguyên không âm nằm giữa hai đường x cộng y bằng hai và x cộng y bằng m. Một cách rất gọn là lấy số điểm trong tam giác lớn rồi trừ số điểm có x cộng y nhỏ hơn hai. Các em hãy thử tự xây dựng công thức N của m.",1.8)
        hint=VGroup(
            mtx(r"N(m)=\frac{(m+1)(m+2)}2-3",38,BLUE),
            mtx(r"N(m)=18",34,INK),
            mtx(r"\frac{(m+1)(m+2)}2=21",34,INK),
            mtx(r"\boxed{m=5}",42,GOLD)
        ).arrange(DOWN,buff=0.24).to_edge(RIGHT,buff=0.55)
        self.play(FadeIn(hint),run_time=0.8)
        self.narrate("Có ba điểm bị loại: không không, một không và không một. Vì vậy N bằng số tam giác đến m trừ ba. Đặt N bằng mười tám ta lại được tổng bằng hai mươi mốt, suy ra m bằng năm.",1.5)

    def outro(self):
        self.clear_stage()
        g=VGroup(
            txt("KẾT THÚC CHUYÊN ĐỀ",43,GOLD,BOLD),
            mtx(r"S(m)\ \longrightarrow\ S(m)\cap\mathbb Z^2\ \longrightarrow\ N(m)",40,BLUE),
            txt("Nhìn miền – hiểu ngưỡng – đếm có hệ thống.",29,CYAN),
            txt(TEN_THAY,22,MUTED)
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(g),run_time=0.9)
        self.narrate("Đến đây, các em đã đi từ miền nghiệm liên tục, sang hệ có tham số, rồi đến điểm nguyên và bài tổng hợp tham số với đếm nghiệm. Đây là nền rất tốt để học quy hoạch tuyến tính và các bài toán tối ưu rời rạc sau này.",1.7)

    def construct(self):
        self.intro(); self.ex1(); self.ex2(); self.ex3(); self.ex4(); self.ex5_application(); self.step_behavior(); self.synthesis(); self.outro()

if __name__ == "__main__":
    render_scene(SangLesson, "he_bpt_tham_so_diem_nguyen_1080p")
