from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time
import numpy as np

# ==========================================================
# HHKG CHUYEN SAU 08 - TY SO THE TICH NANG CAO - MANIM + TYPST SAFE
# Standalone 100% for GitHub Actions
#
# Visual grammar for the whole HHKG series:
#   - visible polyhedron edges: solid
#   - hidden polyhedron edges: dashed neutral
#   - auxiliary / projection lines: dashed accent
#   - fixed teaching camera inside each geometry scene
#   - mathematics only in MathTypst; prose in Text
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
config.background_color = "#08111F"

ROOT = Path.cwd()
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR = ROOT / "media"

# ==========================================================
# PREMIUM PALETTE
# ==========================================================
BG = "#08111F"
PANEL = "#0D1B2E"
PANEL_2 = "#10233C"
INK = "#F3F7FF"
MUTED = "#8EA7C2"
GRID = "#25415E"
BLUE = "#43C6F9"
CYAN = "#38E0CF"
GOLD = "#FFD84D"
GREEN = "#5CE58A"
RED = "#FF7373"
ORANGE = "#FF9B54"
PURPLE = "#B995FF"
EDGE = "#E7F0FF"
DIM = "#58718C"

# ==========================================================
# TYPOGRAPHY
# ==========================================================
def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


_FORBIDDEN_TYPST_WORDS = {"sect", "intersect", "angle"}


def validate_typst_expr(s):
    """Fail early on known-invalid Typst math tokens used in this series."""
    words = set(s.replace("(", " " ).replace(")", " " ).replace(",", " " ).split())
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(
            f"Forbidden Typst math token(s) {bad} in {s!r}. "
            "Use 'inter' for intersection and 'hat(...)' for plane angles."
        )
    if "/" in s:
        raise ValueError(
            f"Slash fraction is forbidden in HHKG MathTypst: {s!r}. Use frac(..., ...)."
        )
    return s


def mty(s, size=38, color=INK):
    """Math only. Text prose must use txt()."""
    s = validate_typst_expr(s)
    try:
        return MathTypst(s, font_size=size, color=color)
    except Exception as exc:
        raise RuntimeError(f"MathTypst failed for expression: {s!r}") from exc


def fit_width(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def fit_height(mob, height):
    if mob.height > height:
        mob.scale_to_fit_height(height)
    return mob


# ==========================================================
# AUDIO + MASTER TRACK
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
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError(f"Audio khong hop le: {path}")
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
                "    c=edge_tts.Communicate(text=text,voice=voice,rate=rate,pitch=pitch)\n"
                "    await c.save(out)\n"
                "asyncio.run(main())\n"
            )
            subprocess.run([sys.executable, "-c", code], check=True)
            validate_audio(out)
            return out
        except Exception as exc:
            last_err = exc
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

    filter_complex = (
        ";".join(filters)
        + ";"
        + "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", *inputs,
            "-filter_complex", filter_complex,
            "-map", "[m]",
            "-ar", "48000",
            "-ac", "2",
            "-t", f"{video_duration:.3f}",
            str(out_wav),
        ],
        check=True,
    )


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(video),
            "-i", str(audio),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(out),
        ],
        check=True,
    )


# ==========================================================
# 3D GEOMETRY
# ==========================================================
GEO_SCALE = 0.80
GEO_SHIFT = np.array([-1.78, -0.02, -0.08])
VIEW_PHI = 68 * DEGREES
VIEW_THETA = -54 * DEGREES
VIEW_ZOOM = 0.97


def L(x, y, z):
    """Logical geometry -> scene geometry."""
    return GEO_SCALE * np.array([float(x), float(y), float(z)]) + GEO_SHIFT


def solid(a, b, color=EDGE, width=4.0, opacity=0.94):
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def hidden_edge(a, b, color=DIM, width=2.7, opacity=0.70, dash=0.11):
    return DashedLine(
        a, b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def aux(a, b, color=CYAN, width=3.7, opacity=0.90, dash=0.11):
    return DashedLine(
        a, b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def face(*points, color=BLUE, opacity=0.10, stroke=BLUE, stroke_width=0.0):
    return Polygon(
        *points,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=stroke_width,
        stroke_opacity=0.0 if stroke_width == 0 else 0.55,
    )


def right_angle_3d(vertex, u, v, size=0.30, color=GOLD, width=4.5):
    u = np.array(u, dtype=float)
    v = np.array(v, dtype=float)
    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)
    p1 = vertex + size * u
    p2 = vertex + size * (u + v)
    p3 = vertex + size * v
    return VGroup(
        solid(p1, p2, color=color, width=width),
        solid(p2, p3, color=color, width=width),
    )


def arc_basis(center, e1, e2, angle, radius=0.52, color=GOLD, width=6):
    e1 = np.array(e1, dtype=float)
    e2 = np.array(e2, dtype=float)
    e1 /= np.linalg.norm(e1)
    e2 /= np.linalg.norm(e2)
    return ParametricFunction(
        lambda t: center + radius * (math.cos(t) * e1 + math.sin(t) * e2),
        t_range=[0, angle],
        color=color,
        stroke_width=width,
    )


# ==========================================================
# SCENE
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)

    # ------------------------------------------------------
    # AUDIO
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # FIXED MASTER UI
    # ------------------------------------------------------
    def clear_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.30)
        self.clear()

    def add_header(self, title, subtitle, progress):
        series = txt("HHKG CHUYÊN SÂU · 08", 15, BLUE, BOLD)
        series.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.30)
        title_m = fit_width(txt(title, 29, INK, BOLD), 8.9)
        title_m.next_to(series, DOWN, buff=0.045, aligned_edge=LEFT)
        sub_m = fit_width(txt(subtitle, 17, MUTED), 8.9)
        sub_m.next_to(title_m, DOWN, buff=0.045, aligned_edge=LEFT)
        accent = Line(series.get_left()+DOWN*0.13, series.get_left()+RIGHT*0.62+DOWN*0.13,
                      color=GOLD, stroke_width=3.2)
        prog = txt(progress, 15, MUTED, BOLD)
        prog.to_edge(UP, buff=0.20).to_edge(RIGHT, buff=0.32)
        rule = Line(LEFT*6.82, RIGHT*6.82, color=GRID, stroke_width=0.9,
                    stroke_opacity=0.42).shift(UP*2.78)
        divider = Line(np.array([1.50,-2.83,0]), np.array([1.50,2.64,0]),
                       color=GRID, stroke_width=1.0, stroke_opacity=0.42)
        teacher = txt(TEN_THAY, 15, MUTED)
        teacher.to_edge(DOWN, buff=0.10).to_edge(LEFT, buff=0.30)
        hud = VGroup(series,title_m,sub_m,accent,prog,rule,divider,teacher)
        self.add_fixed_in_frame_mobjects(hud)
        return hud

    def card(self, kicker, title, items, accent=GOLD, height=5.25, auto_add=True):
        bg = Rectangle(width=5.12,height=height,fill_color=PANEL,fill_opacity=0.90,
                       stroke_color=GRID,stroke_width=0.9,stroke_opacity=0.36).move_to(RIGHT*4.28+DOWN*0.03)
        spine = Line(bg.get_corner(UL)+RIGHT*0.12+DOWN*0.18,
                     bg.get_corner(DL)+RIGHT*0.12+UP*0.18,
                     color=accent,stroke_width=3.8,stroke_opacity=0.95)
        k = txt(kicker.upper(),14,accent,BOLD)
        k.move_to(bg.get_corner(UL)+RIGHT*0.36+DOWN*0.30,aligned_edge=LEFT)
        t = fit_width(txt(title,23,INK,BOLD),4.30)
        t.next_to(k,DOWN,buff=0.10,aligned_edge=LEFT)
        body = VGroup()
        for item in items:
            kind = item[0]
            if kind == "text":
                _,s,size,color,weight = item; mob = txt(s,size,color,weight)
            elif kind == "math":
                _,expr,size,color = item; mob = mty(expr,size,color)
            elif kind == "sep":
                mob = Line(LEFT*2.00,RIGHT*2.00,color=GRID,stroke_width=0.9,stroke_opacity=0.55)
            elif kind == "obj":
                mob = item[1]
            else:
                raise ValueError(kind)
            body.add(fit_width(mob,4.28))
        body.arrange(DOWN,aligned_edge=LEFT,buff=0.18)
        body.next_to(t,DOWN,buff=0.22,aligned_edge=LEFT)
        fit_height(body,height-1.45)
        group = VGroup(bg,spine,k,t,body)
        if auto_add:
            self.add_fixed_in_frame_mobjects(group)
        return group

    def takeaway(self, text_s):
        label = fit_width(txt(text_s,16,CYAN,BOLD),7.15)
        label.move_to(LEFT*2.55+DOWN*2.52)
        self.add_fixed_in_frame_mobjects(label)
        return label

    def add_label(self, name, pt, color=GOLD, off=(0.10,-0.10,0.05), size=22):
        lab = mty(name,size,color).move_to(pt+np.array(off,dtype=float))
        self.add_fixed_orientation_mobjects(lab)
        return lab

    # ------------------------------------------------------
    # MODELS
    # ------------------------------------------------------
    def right_square_pyramid(self, dim=False):
        A=L(-2.0,-1.8,0); B=L(2.0,-1.8,0); C=L(2.0,2.0,0); D=L(-2.0,2.0,0); S=L(-2.0,-1.8,3.0)
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(solid(A,B,vc,vw,vo),solid(B,C,vc,vw,vo),solid(S,A,vc,vw,vo),solid(S,B,vc,vw,vo),solid(S,C,vc,vw,vo))
        hidden=VGroup(hidden_edge(C,D,DIM,2.6,0.68),hidden_edge(D,A,DIM,2.6,0.68),hidden_edge(S,D,DIM,2.6,0.68))
        base=face(A,B,C,D,color=BLUE,opacity=0.09,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def tetrahedron(self, dim=False):
        S=L(-0.5,-0.5,3.4); A=L(-2.3,-1.8,0); B=L(2.2,-1.8,0); C=L(0.7,2.0,0)
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(solid(S,A,vc,vw,vo),solid(S,B,vc,vw,vo),solid(S,C,vc,vw,vo),solid(A,B,vc,vw,vo),solid(A,C,vc,vw,vo))
        hidden=VGroup(hidden_edge(B,C,DIM,2.6,0.68))
        base=face(A,B,C,color=BLUE,opacity=0.08,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C]],Dot3D(S,radius=0.06,color=RED))
        return {"S":S,"A":A,"B":B,"C":C,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def centered_square_pyramid(self):
        A=L(-2.2,-2.0,0); B=L(2.2,-2.0,0); C=L(2.2,2.0,0); D=L(-2.2,2.0,0); S=L(0,0,3.8)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.08,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    # ======================================================

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        title = txt("HHKG CHUYÊN SÂU 08", 46, GOLD, BOLD)
        sub = txt("TỶ SỐ THỂ TÍCH NÂNG CAO", 35, INK, BOLD)
        line = txt("Ghép tỷ số · đổi đỉnh · tham số · trọng tâm · khối trung tâm", 23, CYAN, BOLD)
        note = txt("Không tính từng thể tích nếu có thể triệt tiêu bằng cấu trúc", 22, MUTED)
        brand = txt(TEN_THAY, 20, MUTED)
        g = VGroup(title, sub, line, note, brand).arrange(DOWN, buff=0.28)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g, shift=UP*0.10), run_time=1.0)
        self.narrate(
            "Video tám tiếp tục chặng thể tích nhưng đi vào những cấu hình mà một công thức đơn lẻ không còn đủ. "
            "Ta sẽ gặp ba điểm chia cạnh theo ba tỷ số khác nhau, một điểm nằm trên cạnh đáy và một điểm nằm trên cạnh bên, "
            "bài toán phải ghép qua hai khối trung gian, bài có tham số, bài cực trị rất ngắn, trọng tâm tứ diện và một cấu hình "
            "đẹp: sáu trung điểm tạo ra một khối tám mặt ở giữa. Mục tiêu là biến thể tích thành một đại lượng có thể tách, ghép "
            "và truyền tỷ số qua nhiều bước, thay vì tính từng khối từ đầu.",
            2.0,
        )

    # ======================================================
    # METHOD MAP
    # ======================================================
    def method_map(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_header("Bản đồ phương pháp", "5 câu hỏi trước khi đặt bút tính thể tích", "2/10")
        left = VGroup(
            txt("1. Hai khối có chung đáy không?", 23, INK, BOLD),
            txt("2. Hai đáy có chung chiều cao không?", 23, INK, BOLD),
            txt("3. Điểm có nằm trên cùng một đường thẳng qua mặt chuẩn?", 23, INK, BOLD),
            txt("4. Có thể chèn một khối trung gian để ghép tỷ số không?", 23, INK, BOLD),
            txt("5. Có cấu trúc đồng dạng, trọng tâm hay trung điểm không?", 23, INK, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.29).move_to(LEFT*2.20+UP*0.08)
        right = VGroup(
            mty("frac(V_1, V_2) = frac(S_1 h_1, S_2 h_2)", 27, CYAN),
            mty("frac(V_1, V_3) = frac(V_1, V_2) frac(V_2, V_3)", 27, GREEN),
            mty("frac(V_(S M N P), V_(S A B C)) = m n p", 27, GOLD),
            mty("V_R = V_T - V_P", 27, PURPLE),
        ).arrange(DOWN, buff=0.36).move_to(RIGHT*3.55+UP*0.10)
        self.add_fixed_in_frame_mobjects(left, right)
        self.play(FadeIn(left), FadeIn(right), run_time=0.9)
        self.narrate(
            "Trước một bài tỷ số thể tích nâng cao, hãy kiểm tra năm câu hỏi. Thứ nhất, hai khối có chung đáy hay không. "
            "Thứ hai, nếu không chung đáy thì các đáy có nằm trong cùng một mặt phẳng để dùng chung chiều cao hay không. "
            "Thứ ba, một điểm có đang chạy trên một đường thẳng đi qua mặt phẳng chuẩn hay không, vì khoảng cách đến mặt phẳng "
            "khi đó biến thiên tuyến tính. Thứ tư, nếu hai khối không so trực tiếp được, hãy chèn một khối trung gian. Cuối cùng, "
            "hãy tìm các cấu trúc mạnh như đồng dạng, trọng tâm và trung điểm. Năm câu hỏi này sẽ xuất hiện lặp lại trong toàn video.",
            2.0,
        )

    # ======================================================
    # 1. THREE UNEQUAL EDGE RATIOS
    # ======================================================
    def unequal_three_ratios(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 1 · Ba tỷ số khác nhau", "Không cần thiết diện song song, không cần đồng dạng", "3/10")
        G = self.tetrahedron()
        self.add(G["base"], G["edges"], G["dots"])
        for n in ["S","A","B","C"]:
            self.add_label(n, G[n], RED if n=="S" else GOLD)

        M = G["S"] + 3/5*(G["A"]-G["S"])
        N = G["S"] + 2/3*(G["B"]-G["S"])
        Pp = G["S"] + 4/5*(G["C"]-G["S"])
        small = VGroup(
            face(G["S"], M, N, color=GOLD, opacity=0.15),
            face(G["S"], N, Pp, color=GOLD, opacity=0.12),
            face(G["S"], Pp, M, color=GOLD, opacity=0.10),
            face(M, N, Pp, color=GOLD, opacity=0.25, stroke=GOLD, stroke_width=2.0),
        )
        accents = VGroup(
            solid(G["S"], M, GOLD, 5.0), solid(G["S"], N, CYAN, 5.0), solid(G["S"], Pp, GREEN, 5.0),
            Dot3D(M, radius=0.052, color=GOLD), Dot3D(N, radius=0.052, color=CYAN), Dot3D(Pp, radius=0.052, color=GREEN),
        )
        self.add(small, accents)
        for n,p,c in [("M",M,GOLD),("N",N,CYAN),("P",Pp,GREEN)]:
            self.add_label(n,p,c)

        self.card("TÍCH BA TỶ SỐ", "Ba điểm nằm trên ba cạnh cùng xuất phát từ S", [
            ("math", "frac(S M, S A) = frac(3, 5)", 27, GOLD),
            ("math", "frac(S N, S B) = frac(2, 3)", 27, CYAN),
            ("math", "frac(S P, S C) = frac(4, 5)", 27, GREEN),
            ("sep",),
            ("math", "frac(V_(S M N P), V_(S A B C)) = frac(3, 5) frac(2, 3) frac(4, 5)", 24, INK),
            ("math", "= frac(8, 25)", 36, GOLD),
            ("math", "frac(V_R, V_(S A B C)) = frac(17, 25)", 29, PURPLE),
        ], accent=GOLD)
        self.narrate(
            "Bài đầu tiên cố ý chọn ba tỷ số khác nhau. M trên SA với SM trên SA bằng ba phần năm, N trên SB với tỷ số hai phần ba, "
            "và P trên SC với tỷ số bốn phần năm. MNP không song song với ABC nên không hề có hai tứ diện đồng dạng. Tuy vậy công thức "
            "tích ba tỷ số vẫn đúng, vì nó xuất phát từ tính tuyến tính của định thức hoặc, trong ngôn ngữ hình học phổ thông, từ việc "
            "thay lần lượt ba đỉnh A, B, C bởi M, N, P trên ba tia cùng gốc S.",
            2.0,
        )
        self.narrate(
            "Ta nhân ba phần năm, hai phần ba và bốn phần năm, được tám phần hai mươi lăm. Phần còn lại của tứ diện chiếm mười bảy phần "
            "hai mươi lăm. Điểm quan trọng là không được đồng nhất công thức này với đồng dạng. Đồng dạng chỉ xuất hiện khi ba tỷ số bằng "
            "nhau; còn tích ba tỷ số hoạt động với ba tỷ số hoàn toàn khác nhau, miễn ba điểm nằm trên ba cạnh cùng phát ra từ một đỉnh.",
            1.8,
        )
        self.takeaway("Ba cạnh cùng đỉnh: nhân ba tỷ số, dù thiết diện MNP không song song đáy")

    # ======================================================
    # 2. BASE EDGE PARTITION
    # ======================================================
    def base_edge_partition(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 2 · Một điểm trên cạnh đáy", "M chia AB theo tỷ số 2 : 3", "4/10")
        G = self.tetrahedron()
        self.add(G["base"], G["edges"], G["dots"])
        for n in ["S","A","B","C"]:
            self.add_label(n, G[n], RED if n=="S" else GOLD)
        M = G["A"] + 2/5*(G["B"]-G["A"])
        self.add(Dot3D(M, radius=0.055, color=GOLD))
        self.add_label("M", M, GOLD)
        cut = face(G["S"], M, G["C"], color=PURPLE, opacity=0.28, stroke=PURPLE, stroke_width=2.0)
        am = solid(G["A"], M, GOLD, 5.0)
        mb = solid(M, G["B"], CYAN, 5.0)
        self.add(cut, am, mb)

        self.card("CHIA KHỐI", "Mặt SMC tách tứ diện thành hai phần", [
            ("math", "A M : M B = 2 : 3", 30, CYAN),
            ("math", "frac(S_(A M C), S_(B M C)) = frac(A M, M B)", 26, INK),
            ("math", "frac(V_(S A M C), V_(S B M C)) = frac(2, 3)", 27, GOLD),
            ("sep",),
            ("math", "V_T = 25 -> V_1 = 10, V_2 = 15", 27, GREEN),
        ], accent=PURPLE)
        self.narrate(
            "Bài hai thay đổi kiểu điểm. M không nằm trên cạnh bên từ S mà nằm trên cạnh đáy AB và chia AM trên MB bằng hai trên ba. "
            "Mặt phẳng SMC chia tứ diện thành hai tứ diện S A M C và S B M C. Hai khối có cùng chiều cao từ S xuống mặt phẳng ABC. "
            "Vì vậy tỷ số thể tích bằng tỷ số diện tích hai đáy AMC và BMC.",
            1.8,
        )
        self.narrate(
            "Hai tam giác AMC và BMC lại có chung chiều cao kẻ từ C xuống AB, nên tỷ số diện tích đúng bằng AM trên MB, tức hai trên ba. "
            "Vì thế hai thể tích cũng theo tỷ lệ hai trên ba. Nếu tổng thể tích bằng hai mươi lăm, hai phần lần lượt là mười và mười lăm. "
            "Mẫu nhận dạng rất quan trọng: một điểm chia một cạnh trong mặt đáy thường truyền nguyên tỷ số đoạn thẳng thành tỷ số diện tích, "
            "rồi từ diện tích truyền tiếp thành tỷ số thể tích.",
            2.0,
        )
        self.takeaway("Điểm trên cạnh đáy → tỷ số đoạn → tỷ số diện tích đáy → tỷ số thể tích")

    # ======================================================
    # 3. CHAIN THROUGH AN INTERMEDIATE TETRAHEDRON
    # ======================================================
    def chain_ratio(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 3 · Ghép tỷ số qua khối trung gian", "M thuộc AB, N thuộc SC — hai tỷ số không cùng đỉnh", "5/10")
        G = self.tetrahedron()
        self.add(G["base"], G["edges"], G["dots"])
        for n in ["S","A","B","C"]:
            self.add_label(n, G[n], RED if n=="S" else GOLD)
        M = G["A"] + 2/5*(G["B"]-G["A"])
        N = G["S"] + 3/4*(G["C"]-G["S"])
        self.add(Dot3D(M, radius=0.055, color=GOLD), Dot3D(N, radius=0.055, color=GREEN))
        self.add_label("M",M,GOLD); self.add_label("N",N,GREEN)
        target = VGroup(
            face(G["S"], G["A"], M, color=GOLD, opacity=0.16),
            face(G["S"], M, N, color=GOLD, opacity=0.18),
            face(G["S"], N, G["A"], color=GOLD, opacity=0.12),
            face(G["A"], M, N, color=GOLD, opacity=0.24, stroke=GOLD, stroke_width=2.0),
        )
        intermediate = face(G["S"], G["A"], M, G["C"], color=PURPLE, opacity=0.08)
        self.add(intermediate, target)

        self.card("GHÉP HAI BƯỚC", "Không so trực tiếp được thì chèn S.AMC", [
            ("math", "frac(A M, A B) = frac(2, 5)", 27, CYAN),
            ("math", "frac(S N, S C) = frac(3, 4)", 27, GREEN),
            ("math", "frac(V_(S A M N), V_(S A M C)) = frac(3, 4)", 25, INK),
            ("math", "frac(V_(S A M C), V_(S A B C)) = frac(2, 5)", 25, INK),
            ("sep",),
            ("math", "frac(V_(S A M N), V_(S A B C)) = frac(3, 10)", 31, GOLD),
        ], accent=PURPLE)
        self.narrate(
            "Bài ba là bước nâng cấp thật sự. M nằm trên AB nhưng N lại nằm trên SC, nên hai tỷ số AM trên AB và SN trên SC không cùng "
            "xuất phát từ một đỉnh. Ta không được nhảy ngay sang công thức tích ba tỷ số của bài một. Thay vào đó, chèn khối trung gian S A M C.",
            1.7,
        )
        self.narrate(
            "So S A M N với S A M C: chúng có chung mặt S A M, còn N và C nằm trên cùng đường SC đi qua S thuộc mặt S A M. Khoảng cách "
            "đến mặt S A M tỷ lệ với SN trên SC, nên tỷ số thể tích là ba phần tư. Tiếp theo, so S A M C với S A B C. Hai khối có chung "
            "mặt S A C, còn M và B nằm trên AB đi qua A thuộc mặt ấy, nên tỷ số bằng AM trên AB, tức hai phần năm. Nhân hai bước, ta được "
            "ba phần mười. Đây chính là kỹ thuật ghép tỷ số qua một khối trung gian.",
            2.2,
        )
        self.takeaway("Không so trực tiếp được → chèn khối trung gian rồi nhân các tỷ số liên tiếp")

    # ======================================================
    # 4. PARAMETER + EXTREMUM PREVIEW
    # ======================================================
    def dynamic_parameter(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 4 · Hai điểm động liên kết", "AM/AB = t và SN/SC = 1 − t", "6/10")
        G = self.tetrahedron()
        self.add(G["base"], G["edges"], G["dots"])
        for n in ["S","A","B","C"]:
            self.add_label(n, G[n], RED if n=="S" else GOLD)

        t = ValueTracker(0.15)
        M = always_redraw(lambda: Dot3D(G["A"]+t.get_value()*(G["B"]-G["A"]), radius=0.055, color=GOLD))
        N = always_redraw(lambda: Dot3D(G["S"]+(1-t.get_value())*(G["C"]-G["S"]), radius=0.055, color=GREEN))
        AM = always_redraw(lambda: solid(G["A"], G["A"]+t.get_value()*(G["B"]-G["A"]), GOLD, 5.0))
        SN = always_redraw(lambda: solid(G["S"], G["S"]+(1-t.get_value())*(G["C"]-G["S"]), GREEN, 5.0))
        def moving_tetra_faces():
            mm = G["A"] + t.get_value()*(G["B"]-G["A"])
            nn = G["S"] + (1-t.get_value())*(G["C"]-G["S"])
            return VGroup(
                face(G["S"], G["A"], mm, color=GOLD, opacity=0.10),
                face(G["S"], mm, nn, color=GOLD, opacity=0.15),
                face(G["S"], nn, G["A"], color=GOLD, opacity=0.10),
                face(G["A"], mm, nn, color=GOLD, opacity=0.22, stroke=GOLD, stroke_width=1.6),
            )
        target = always_redraw(moving_tetra_faces)
        self.add(target, AM, SN, M, N)

        read = always_redraw(lambda: VGroup(
            txt(f"t = {t.get_value():.2f}", 17, ORANGE, BOLD),
            txt(f"t(1-t) = {t.get_value()*(1-t.get_value()):.3f}", 17, GOLD, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.07).move_to(RIGHT*4.18+DOWN*1.98))
        self.add_fixed_in_frame_mobjects(read)

        self.card("THAM SỐ", "Tỷ số thể tích trở thành một hàm bậc hai", [
            ("math", "frac(A M, A B) = t", 27, CYAN),
            ("math", "frac(S N, S C) = 1-t", 27, GREEN),
            ("math", "frac(V_(S A M N), V_(S A B C)) = t times (1-t)", 25, INK),
            ("math", "t times (1-t) = frac(1, 4) - (t-frac(1, 2))^2", 24, GOLD),
            ("math", "t = frac(1, 2) -> frac(V_(S A M N), V_(S A B C)) = frac(1, 4)", 23, PURPLE),
        ], accent=ORANGE)
        self.narrate_play(
            "Bây giờ M chạy trên AB sao cho AM trên AB bằng t, còn N chạy trên SC theo tỷ số SN trên SC bằng một trừ t. "
            "Từ bài ba, tỷ số thể tích S A M N trên S A B C bằng tích t nhân một trừ t. Khi t tăng từ gần không đến gần một, "
            "một tỷ số tăng còn tỷ số kia giảm, nên thể tích phần được chọn không tăng đơn điệu.",
            t.animate.set_value(0.85), min_time=5.0
        )
        self.narrate_play(
            "Viết t nhân một trừ t thành một phần tư trừ bình phương của t trừ một phần hai. Bình phương luôn không âm, vì thế giá trị "
            "lớn nhất là một phần tư, đạt khi t bằng một phần hai. Đưa hai điểm về vị trí ấy, M là trung điểm AB và N là trung điểm SC. "
            "Đây là một ví dụ rất ngắn cho thấy tỷ số thể tích có thể biến một bài cực trị không gian thành một biểu thức đại số một biến.",
            t.animate.set_value(0.50), min_time=4.5
        )
        self.takeaway("Điểm động + tỷ số thể tích → thường tạo hàm rất đơn giản trước khi cần đạo hàm")

    # ======================================================
    # 5. TETRAHEDRON CENTROID
    # ======================================================
    def tetra_centroid(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 5 · Trọng tâm tứ diện", "Một điểm chia tứ diện thành bốn phần bằng nhau", "7/10")
        G0 = self.tetrahedron()
        A,B,C,D = G0["A"],G0["B"],G0["C"],G0["S"]
        self.add(G0["base"], G0["edges"], G0["dots"])
        for n,p in [("A",A),("B",B),("C",C),("D",D)]:
            self.add_label(n,p,RED if n=="D" else GOLD)
        K = (B+C+D)/3
        G = (A+B+C+D)/4
        ak = aux(A,K,CYAN,3.4,0.85)
        gdot = Dot3D(G, radius=0.065, color=GOLD)
        kdot = Dot3D(K, radius=0.052, color=CYAN)
        spokes = VGroup(*[solid(G,p,PURPLE,2.7,0.70) for p in [A,B,C,D]])
        self.add(ak,spokes,gdot,kdot)
        self.add_label("G",G,GOLD,off=(0.08,0.06,0.08))
        self.add_label("K",K,CYAN,off=(0.08,0.06,0.05))

        self.card("TRỌNG TÂM", "G nằm trên trung tuyến AK của tứ diện", [
            ("math", "A G : G K = 3 : 1", 29, CYAN),
            ("math", "frac(d(G,(B C D)), d(A,(B C D))) = frac(1, 4)", 24, INK),
            ("math", "frac(V_(G B C D), V_(A B C D)) = frac(1, 4)", 25, GOLD),
            ("sep",),
            ("math", "V_(G B C D) = V_(G A C D) = V_(G A B D) = V_(G A B C)", 21, GREEN),
            ("math", "= frac(1, 4) V_(A B C D)", 29, GOLD),
        ], accent=GOLD)
        self.narrate(
            "Một kết quả rất đẹp: trọng tâm G của tứ diện ABCD chia tứ diện thành bốn tứ diện có thể tích bằng nhau. Gọi K là trọng tâm "
            "mặt BCD. Trọng tâm tứ diện nằm trên trung tuyến AK và chia AG trên GK bằng ba trên một. Vì K thuộc mặt BCD, khoảng cách từ G "
            "đến mặt BCD chỉ bằng một phần tư khoảng cách từ A đến mặt ấy.",
            1.9,
        )
        self.narrate(
            "Hai tứ diện GBCD và ABCD có chung đáy BCD nên tỷ số thể tích bằng tỷ số chiều cao, tức một phần tư. Lập luận hoàn toàn tương tự "
            "cho ba mặt còn lại, nên bốn tứ diện quanh G đều chiếm một phần tư thể tích toàn khối. Đây là một tính chất nên nhớ như một định "
            "lý nhỏ, vì nó xuất hiện rất tự nhiên trong các bài trọng tâm, barycentric và Oxyz sau này.",
            2.0,
        )
        self.takeaway("Trọng tâm tứ diện → 4 tứ diện con bằng thể tích, mỗi khối bằng 1/4")

    # ======================================================
    # 6. MIDPOINT OCTAHEDRON
    # ======================================================
    def midpoint_octahedron(self):
        self.clear_all()
        self.set_camera_orientation(phi=69*DEGREES, theta=-54*DEGREES, zoom=0.96)
        self.add_header("Bài 6 · Sáu trung điểm — một khối tám mặt", "Tính thể tích phần trung tâm mà không cần công thức khối tám mặt", "8/10")
        G0 = self.tetrahedron()
        A,B,C,D = G0["A"],G0["B"],G0["C"],G0["S"]
        self.add(G0["base"],G0["edges"],G0["dots"])
        for n,p in [("A",A),("B",B),("C",C),("D",D)]:
            self.add_label(n,p,RED if n=="D" else GOLD)

        M1=(A+B)/2; M2=(A+C)/2; M3=(A+D)/2
        M4=(B+C)/2; M5=(B+D)/2; M6=(C+D)/2
        mids=[M1,M2,M3,M4,M5,M6]
        dots=VGroup(*[Dot3D(p,radius=0.050,color=GOLD) for p in mids])

        faces = VGroup(
            face(M1,M2,M4,color=PURPLE,opacity=0.20),
            face(M1,M3,M5,color=PURPLE,opacity=0.18),
            face(M2,M3,M6,color=PURPLE,opacity=0.16),
            face(M4,M5,M6,color=PURPLE,opacity=0.15),
            face(M1,M2,M3,color=GOLD,opacity=0.18),
            face(M1,M4,M5,color=GOLD,opacity=0.16),
            face(M2,M4,M6,color=GOLD,opacity=0.14),
            face(M3,M5,M6,color=GOLD,opacity=0.13),
        )
        pairs=[]
        for i in range(6):
            for j in range(i+1,6):
                if {i,j} in [{0,5},{1,4},{2,3}]:
                    continue
                pairs.append(solid(mids[i],mids[j],GOLD,2.6,0.78))
        self.add(faces,VGroup(*pairs),dots)

        self.card("KHỐI TRUNG TÂM", "Bốn góc bị cắt là bốn tứ diện đồng dạng tỷ số 1/2", [
            ("math", "k = frac(1, 2) -> k^3 = frac(1, 8)", 28, CYAN),
            ("math", "V_C = frac(1, 8) V_T", 27, INK),
            ("math", "4 V_C = frac(1, 2) V_T", 27, GREEN),
            ("sep",),
            ("math", "V_O = V_T - 4 V_C", 25, PURPLE),
            ("math", "V_O = frac(1, 2) V_T", 32, GOLD),
        ], accent=PURPLE)
        self.narrate(
            "Lấy trung điểm của cả sáu cạnh một tứ diện và nối chúng theo các mặt tam giác, ta thu được một khối tám mặt nằm ở giữa. "
            "Thoạt nhìn đây có vẻ là một khối hoàn toàn mới, nhưng ta không cần biết công thức thể tích của khối tám mặt. Hãy nhìn bốn góc "
            "của tứ diện ban đầu.",
            1.6,
        )
        self.narrate(
            "Tại mỗi đỉnh, ba trung điểm trên ba cạnh kề tạo ra một tứ diện nhỏ đồng dạng với tứ diện lớn theo tỷ số một phần hai. Vì thể tích "
            "tỷ lệ với lập phương tỷ số đồng dạng, mỗi tứ diện góc chiếm một phần tám. Có bốn góc nên tổng phần bị cắt chiếm bốn phần tám, tức "
            "một nửa. Phần trung tâm vì thế cũng bằng đúng một nửa thể tích tứ diện ban đầu. Kết quả này đúng với mọi tứ diện, không cần tứ diện đều.",
            2.1,
        )
        self.takeaway("Sáu trung điểm của mọi tứ diện → khối tám mặt trung tâm chiếm đúng 1/2 thể tích")

    # ======================================================
    # 7. REVERSE PARAMETER
    # ======================================================
    def reverse_parameter(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 7 · Bài ngược tìm tỷ số cạnh", "Biết tỷ số thể tích, tìm vị trí điểm M", "9/10")
        G=self.tetrahedron()
        self.add(G["base"],G["edges"],G["dots"])
        for n in ["S","A","B","C"]:
            self.add_label(n,G[n],RED if n=="S" else GOLD)
        x=2/5
        M=G["S"]+x*(G["A"]-G["S"])
        N=G["S"]+2/3*(G["B"]-G["S"])
        Pp=G["S"]+3/4*(G["C"]-G["S"])
        self.add(Dot3D(M,radius=0.052,color=GOLD),Dot3D(N,radius=0.052,color=CYAN),Dot3D(Pp,radius=0.052,color=GREEN))
        for n,p,c in [("M",M,GOLD),("N",N,CYAN),("P",Pp,GREEN)]:
            self.add_label(n,p,c)
        self.add(face(M,N,Pp,color=GOLD,opacity=0.26,stroke=GOLD,stroke_width=2.0))

        self.card("BÀI NGƯỢC","Thể tích cho trước tạo phương trình rất ngắn",[
            ("math","frac(S N, S B) = frac(2, 3)",25,CYAN),
            ("math","frac(S P, S C) = frac(3, 4)",25,CYAN),
            ("math","frac(V_(S M N P), V_(S A B C)) = frac(1, 5)",25,GOLD),
            ("math","x times frac(2, 3) times frac(3, 4) = frac(1, 5)",25,INK),
            ("math","frac(x, 2) = frac(1, 5)",29,INK),
            ("math","x = frac(S M, S A) = frac(2, 5)",33,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Bài cuối đảo chiều tư duy. N và P đã biết vị trí: SN trên SB bằng hai phần ba, SP trên SC bằng ba phần tư. M nằm trên SA nhưng "
            "chưa biết tỷ số x bằng SM trên SA. Đề bài cho thể tích S M N P bằng một phần năm thể tích tứ diện lớn. Thay thẳng vào định lý tích "
            "ba tỷ số, ta được x nhân hai phần ba nhân ba phần tư bằng một phần năm.",
            1.8,
        )
        self.narrate(
            "Hai phần ba nhân ba phần tư rút gọn thành một phần hai, nên x trên hai bằng một phần năm và x bằng hai phần năm. Những bài ngược "
            "kiểu này thường rất ngắn nếu nhận đúng cấu trúc, nhưng có thể trở nên dài nếu ta cố dựng chiều cao và tính từng thể tích riêng. "
            "Thông điệp của cả video là luôn hỏi: dữ kiện thể tích có thể chuyển ngược thành tỷ số cạnh nào?",
            1.9,
        )
        self.takeaway("Biết tỷ số thể tích → viết tích các tỷ số cạnh → giải ngược vị trí điểm")

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Tổng kết Video 08", "Tỷ số thể tích như một ngôn ngữ ghép — tách — truyền", "10/10")
        left=VGroup(
            txt("7 mẫu nhận dạng nâng cao",26,GOLD,BOLD),
            txt("• Ba tỷ số khác nhau vẫn nhân được nếu cùng đỉnh",19,INK),
            txt("• Điểm trên cạnh đáy truyền tỷ số qua diện tích",19,INK),
            txt("• Không so trực tiếp được → chèn khối trung gian",19,INK),
            txt("• Điểm động → tỷ số thể tích thành hàm một biến",19,INK),
            txt("• Trọng tâm → bốn tứ diện bằng nhau",19,INK),
            txt("• Sáu trung điểm → khối trung tâm bằng 1/2",19,INK),
            txt("• Bài ngược → từ V suy ra tỷ số cạnh",19,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.20).move_to(LEFT*2.25+UP*0.02)
        right=VGroup(
            mty("frac(V_(S M N P), V_(S A B C)) = m n p",26,CYAN),
            mty("frac(V_1, V_3) = frac(V_1, V_2) frac(V_2, V_3)",24,GREEN),
            mty("t times (1-t) = frac(1,4) - (t-frac(1,2))^2",22,GOLD),
            mty("V_(G B C D) = frac(1,4) V_(A B C D)",24,PURPLE),
            mty("V_O = frac(1,2) V_T",27,GOLD),
        ).arrange(DOWN,buff=0.30).move_to(RIGHT*3.65+UP*0.05)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left),FadeIn(right),run_time=0.9)
        self.narrate(
            "Video tám đã nâng tỷ số thể tích từ một công thức thành một ngôn ngữ. Ta có thể truyền tỷ số từ đoạn thẳng sang diện tích rồi sang "
            "thể tích, ghép qua một khối trung gian, biến điểm động thành hàm một biến, khai thác trọng tâm để chia tứ diện thành bốn phần bằng nhau, "
            "và dùng sáu trung điểm để nhận ra một khối tám mặt chiếm đúng một nửa thể tích. Những kết quả này đều dựa trên một nguyên tắc: đừng tính "
            "thể tích tuyệt đối nếu tỷ số có thể làm triệt tiêu những đại lượng không cần thiết.",
            2.1,
        )
        self.narrate(
            "Video chín sẽ kết thúc chặng C bằng một hướng khác: thể tích được suy ra từ khoảng cách và góc. Ta sẽ kết nối công thức thể tích với "
            "khoảng cách điểm đến mặt phẳng, góc giữa đường và mặt, góc nhị diện, diện tích hình chiếu và các bài ngược. Khi đó ba mảng tưởng tách rời "
            "là góc, khoảng cách và thể tích sẽ hợp lại thành một hệ thống duy nhất.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.method_map()
        self.unequal_three_ratios()
        self.base_edge_partition()
        self.chain_ratio()
        self.dynamic_parameter()
        self.tetra_centroid()
        self.midpoint_octahedron()
        self.reverse_parameter()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_08_ty_so_the_tich_nang_cao_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 08")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_08.wav"
    build_master_audio(scene.audio_events, duration, master_wav)

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
