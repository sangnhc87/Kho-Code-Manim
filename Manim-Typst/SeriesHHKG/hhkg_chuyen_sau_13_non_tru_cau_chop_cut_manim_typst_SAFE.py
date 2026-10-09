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
# HHKG CHUYEN SAU 13 - NON, TRU, CAU, CHOP CUT
# Manim Community + MathTypst SAFE | Standalone 100%
# Muc tieu: 12-14 phut, it canh nhung moi canh co chieu sau.
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
# PALETTE
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

# Fixed 3D view. No ambient rotation: stable hidden/visible reading and faster render.
VIEW_PHI = 67 * DEGREES
VIEW_THETA = -54 * DEGREES
VIEW_ZOOM = 0.98

# Left geometry area center
GC = np.array([-2.55, 0.00, -0.18])

# ==========================================================
# TYPOGRAPHY + TYPST SAFETY
# ==========================================================
def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


_FORBIDDEN_TYPST_WORDS = {"sect", "intersect", "angle"}


def validate_typst_expr(s):
    words = set(s.replace("(", " ").replace(")", " ").replace(",", " ").split())
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(
            f"Forbidden Typst math token(s) {bad} in {s!r}. "
            "Use inter for intersection and hat(...) for plane angles."
        )
    if "/" in s:
        raise ValueError(f"Slash fraction forbidden in HHKG MathTypst: {s!r}. Use frac(..., ...).")
    return s


def mty(s, size=38, color=INK):
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
        {"text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC, "pitch": PITCH, "engine": "edge-tts"},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
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
    fc = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[m]", "-ar", "48000", "-ac", "2", "-t", f"{video_duration:.3f}", str(out_wav)],
        check=True,
    )


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)],
        check=True,
    )

# ==========================================================
# 3D VISUAL GRAMMAR FOR SOLIDS OF REVOLUTION
# ==========================================================
def solid(a, b, color=EDGE, width=4.0, opacity=0.94):
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def aux(a, b, color=CYAN, width=3.6, opacity=0.92, dash=0.10):
    return DashedLine(a, b, color=color, stroke_width=width, stroke_opacity=opacity, dash_length=dash, dashed_ratio=0.56)


def face(*points, color=BLUE, opacity=0.10):
    return Polygon(*points, fill_color=color, fill_opacity=opacity, stroke_width=0)


def low_surface(func, u_range, v_range, color=BLUE, opacity=0.10, resolution=(10, 24)):
    surf = Surface(func, u_range=u_range, v_range=v_range, resolution=resolution)
    surf.set_fill(color, opacity=opacity)
    surf.set_stroke(color, width=0.35, opacity=0.20)
    return surf


def sphere_surface(center, radius, color=BLUE, opacity=0.08):
    c = np.array(center, dtype=float)
    return low_surface(
        lambda u, v: c + radius * np.array([math.sin(u)*math.cos(v), math.sin(u)*math.sin(v), math.cos(u)]),
        [0, PI], [0, TAU], color=color, opacity=opacity, resolution=(12, 24)
    )


def cone_surface(base_center, radius, height, color=PURPLE, opacity=0.08):
    c = np.array(base_center, dtype=float)
    return low_surface(
        lambda u, v: c + np.array([(1-u)*radius*math.cos(v), (1-u)*radius*math.sin(v), u*height]),
        [0, 1], [0, TAU], color=color, opacity=opacity, resolution=(9, 24)
    )


def cylinder_surface(center, radius, height, color=CYAN, opacity=0.08):
    c = np.array(center, dtype=float)
    return low_surface(
        lambda u, v: c + np.array([radius*math.cos(v), radius*math.sin(v), (u-0.5)*height]),
        [0, 1], [0, TAU], color=color, opacity=opacity, resolution=(5, 24)
    )


def frustum_surface(base_center, R, r, height, color=ORANGE, opacity=0.09):
    c = np.array(base_center, dtype=float)
    return low_surface(
        lambda u, v: c + np.array([((1-u)*R+u*r)*math.cos(v), ((1-u)*R+u*r)*math.sin(v), u*height]),
        [0, 1], [0, TAU], color=color, opacity=opacity, resolution=(8, 24)
    )


def horizontal_rim(center, radius, color=EDGE, width=3.3, hidden_color=DIM):
    """Front half solid, back half dashed for the fixed camera azimuth."""
    c = np.array(center, dtype=float)
    th = VIEW_THETA
    f = ParametricFunction(
        lambda t: c + radius*np.array([math.cos(t), math.sin(t), 0.0]),
        t_range=[th-PI/2, th+PI/2], color=color, stroke_width=width,
    )
    b0 = ParametricFunction(
        lambda t: c + radius*np.array([math.cos(t), math.sin(t), 0.0]),
        t_range=[th+PI/2, th+3*PI/2], color=hidden_color, stroke_width=max(2.1, width-0.7),
    )
    b = DashedVMobject(b0, num_dashes=16, dashed_ratio=0.52)
    b.set_opacity(0.72)
    return VGroup(f, b)


def meridian_circle(center, radius, color=DIM, width=1.9, opacity=0.55):
    c = np.array(center, dtype=float)
    return ParametricFunction(
        lambda t: c + radius*np.array([math.cos(t), 0.0, math.sin(t)]),
        t_range=[0, TAU], color=color, stroke_width=width, stroke_opacity=opacity,
    )


def axis_line(z0, z1, center_xy=None, color=DIM):
    if center_xy is None:
        center_xy = GC[:2]
    a = np.array([center_xy[0], center_xy[1], z0])
    b = np.array([center_xy[0], center_xy[1], z1])
    return aux(a, b, color=color, width=2.2, opacity=0.65, dash=0.08)


def right_angle_3d(vertex, u, v, size=0.24, color=GOLD, width=4.0):
    u = np.array(u, dtype=float); v = np.array(v, dtype=float)
    u /= np.linalg.norm(u); v /= np.linalg.norm(v)
    p1 = vertex + size*u
    p2 = vertex + size*(u+v)
    p3 = vertex + size*v
    return VGroup(solid(p1,p2,color,width), solid(p2,p3,color,width))


def angle_arc_3d(vertex, ray1, ray2, radius=0.40, color=GOLD, width=5.3):
    """Correct minor arc in the plane of the two actual rays."""
    u=np.array(ray1,dtype=float); v=np.array(ray2,dtype=float)
    u/=np.linalg.norm(u); v/=np.linalg.norm(v)
    dot=float(np.clip(np.dot(u,v),-1.0,1.0)); theta=math.acos(dot)
    w=v-dot*u; nw=np.linalg.norm(w)
    if nw<1e-9: raise ValueError("Collinear rays")
    w/=nw
    return ParametricFunction(
        lambda t: vertex + radius*(math.cos(t)*u + math.sin(t)*w),
        t_range=[0,theta], color=color, stroke_width=width,
    )

# ==========================================================
# MAIN SCENE
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)

    # ---------- audio ----------
    def narrate(self,text,min_visual_time=1.0):
        audio=create_audio(text); dur=probe_duration(audio)
        self.audio_events.append((self.time,audio)); self.wait(max(dur,min_visual_time)); return dur

    def narrate_play(self,text,*animations,min_time=1.0,rate_func=linear):
        audio=create_audio(text); dur=probe_duration(audio)
        self.audio_events.append((self.time,audio))
        self.play(*animations,run_time=max(dur,min_time),rate_func=rate_func); return dur

    # ---------- fixed UI ----------
    def clear_all(self):
        mobs=list(self.mobjects)
        if mobs: self.play(*[FadeOut(m) for m in mobs],run_time=0.28)
        self.clear()

    def add_header(self,title,subtitle,progress):
        series=txt("HHKG CHUYÊN SÂU · 13",15,BLUE,BOLD)
        series.to_edge(UP,buff=0.16).to_edge(LEFT,buff=0.30)
        title_m=fit_width(txt(title,29,INK,BOLD),8.9); title_m.next_to(series,DOWN,buff=0.045,aligned_edge=LEFT)
        sub_m=fit_width(txt(subtitle,17,MUTED),8.9); sub_m.next_to(title_m,DOWN,buff=0.045,aligned_edge=LEFT)
        accent=Line(series.get_left()+DOWN*0.13,series.get_left()+RIGHT*0.62+DOWN*0.13,color=GOLD,stroke_width=3.2)
        prog=txt(progress,15,MUTED,BOLD); prog.to_edge(UP,buff=0.20).to_edge(RIGHT,buff=0.32)
        rule=Line(LEFT*6.82,RIGHT*6.82,color=GRID,stroke_width=0.9,stroke_opacity=0.42).shift(UP*2.78)
        divider=Line(np.array([1.50,-2.83,0]),np.array([1.50,2.64,0]),color=GRID,stroke_width=1.0,stroke_opacity=0.42)
        teacher=txt(TEN_THAY,15,MUTED); teacher.to_edge(DOWN,buff=0.10).to_edge(LEFT,buff=0.30)
        hud=VGroup(series,title_m,sub_m,accent,prog,rule,divider,teacher)
        self.add_fixed_in_frame_mobjects(hud); return hud

    def card(self,kicker,title,items,accent=GOLD,height=5.25,auto_add=True):
        bg=Rectangle(width=5.12,height=height,fill_color=PANEL,fill_opacity=0.90,stroke_color=GRID,stroke_width=0.9,stroke_opacity=0.36).move_to(RIGHT*4.28+DOWN*0.03)
        spine=Line(bg.get_corner(UL)+RIGHT*0.12+DOWN*0.18,bg.get_corner(DL)+RIGHT*0.12+UP*0.18,color=accent,stroke_width=3.8,stroke_opacity=0.95)
        k=txt(kicker.upper(),14,accent,BOLD); k.move_to(bg.get_corner(UL)+RIGHT*0.36+DOWN*0.30,aligned_edge=LEFT)
        t=fit_width(txt(title,23,INK,BOLD),4.30); t.next_to(k,DOWN,buff=0.10,aligned_edge=LEFT)
        body=VGroup()
        for item in items:
            kind=item[0]
            if kind=="text": _,s,size,color,weight=item; mob=txt(s,size,color,weight)
            elif kind=="math": _,expr,size,color=item; mob=mty(expr,size,color)
            elif kind=="sep": mob=Line(LEFT*2.00,RIGHT*2.00,color=GRID,stroke_width=0.9,stroke_opacity=0.55)
            elif kind=="obj": mob=item[1]
            else: raise ValueError(kind)
            body.add(fit_width(mob,4.28))
        body.arrange(DOWN,aligned_edge=LEFT,buff=0.18); body.next_to(t,DOWN,buff=0.22,aligned_edge=LEFT); fit_height(body,height-1.45)
        group=VGroup(bg,spine,k,t,body)
        if auto_add: self.add_fixed_in_frame_mobjects(group)
        return group

    def takeaway(self,s):
        label=fit_width(txt(s,16,CYAN,BOLD),7.15); label.move_to(LEFT*2.55+DOWN*2.52)
        self.add_fixed_in_frame_mobjects(label); return label

    def add_label(self,name,pt,color=GOLD,off=(0.10,-0.10,0.05),size=21):
        lab=mty(name,size,color).move_to(pt+np.array(off,dtype=float)); self.add_fixed_orientation_mobjects(lab); return lab

    # ======================================================
    # 1. INTRO
    # ======================================================
    def intro(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        title=txt("HHKG CHUYÊN SÂU 13",45,GOLD,BOLD)
        sub=txt("NÓN · TRỤ · CẦU · CHÓP CỤT",32,INK,BOLD)
        line=txt("Không học bốn khối rời rạc — quy về mặt cắt qua trục",22,CYAN,BOLD)
        note=txt("Nội tiếp · ngoại tiếp · tiếp xúc · cực trị · công thức chóp cụt",21,MUTED)
        brand=txt(TEN_THAY,18,MUTED)
        VGroup(title,sub,line,note,brand).arrange(DOWN,buff=0.28)
        self.play(FadeIn(title,shift=UP*0.15),FadeIn(sub),run_time=0.85)
        self.play(FadeIn(line),FadeIn(note),FadeIn(brand),run_time=0.75)
        self.narrate(
            "Video mười ba mở chặng khối tròn. Thầy không muốn các em thuộc riêng một công thức cho nón, một công thức cho trụ rồi thêm vài công thức về cầu. Ý chính của cả video là mặt cắt qua trục. Khi cắt đúng, hình cầu trở thành đường tròn, hình trụ thành hình chữ nhật, hình nón thành tam giác cân và chóp cụt tròn xoay thành hình thang cân. Những quan hệ nội tiếp, tiếp xúc và thể tích khó nhìn trong không gian lập tức trở về hình học phẳng quen thuộc.",
            2.0,
        )

    # ======================================================
    # 2. AXIAL SECTION DICTIONARY
    # ======================================================
    def axial_dictionary(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Ngôn ngữ chung: mặt cắt qua trục","Hình 3D khó nhìn → bài toán phẳng có cấu trúc","1/8")

        # Three compact solids on the left: cone, cylinder, sphere.
        c1=GC+LEFT*2.0+DOWN*0.18; c2=GC+RIGHT*0.05+DOWN*0.18; c3=GC+RIGHT*2.02+DOWN*0.18
        cone=cone_surface(c1+DOWN*0.90,0.68,1.75,PURPLE,0.08)
        cone_rim=horizontal_rim(c1+DOWN*0.90,0.68,PURPLE,2.6)
        cone_sides=VGroup(solid(c1+DOWN*0.90+LEFT*0.68,c1+UP*0.85,PURPLE,2.8),solid(c1+DOWN*0.90+RIGHT*0.68,c1+UP*0.85,PURPLE,2.8))

        cyl=cylinder_surface(c2,0.62,1.75,CYAN,0.07)
        cyl_rims=VGroup(horizontal_rim(c2+UP*0.875,0.62,CYAN,2.5),horizontal_rim(c2+DOWN*0.875,0.62,CYAN,2.5))
        cyl_rect=VGroup(solid(c2+LEFT*0.62+DOWN*0.875,c2+LEFT*0.62+UP*0.875,CYAN,2.7),solid(c2+RIGHT*0.62+DOWN*0.875,c2+RIGHT*0.62+UP*0.875,CYAN,2.7))

        sph=sphere_surface(c3,0.88,BLUE,0.065)
        sph_eq=horizontal_rim(c3,0.88,BLUE,2.4)
        sph_mer=meridian_circle(c3,0.88,BLUE,2.2,0.70)

        self.play(FadeIn(cone),Create(cone_rim),Create(cone_sides),FadeIn(cyl),Create(cyl_rims),Create(cyl_rect),FadeIn(sph),Create(sph_eq),Create(sph_mer),run_time=1.2)
        self.card("Bản đồ","Một nhát cắt — ba hình phẳng",[
            ("text","Nón → tam giác cân",18,INK,BOLD),
            ("text","Trụ → hình chữ nhật",18,INK,BOLD),
            ("text","Cầu → đường tròn",18,INK,BOLD),
            ("sep",),
            ("text","Bài tiếp xúc: dùng tiếp tuyến và bán kính vuông góc.",16,MUTED,NORMAL),
            ("text","Bài nội tiếp: dùng Pythagore trong mặt cắt.",16,MUTED,NORMAL),
        ],accent=BLUE)
        self.narrate(
            "Mặt cắt qua trục là công cụ trung tâm. Với nón tròn xoay, ta được một tam giác cân có đáy bằng hai lần bán kính, chiều cao đúng bằng chiều cao nón và cạnh bên đúng bằng đường sinh. Với trụ, ta được hình chữ nhật kích thước hai r nhân h. Với cầu, bất kỳ mặt phẳng nào đi qua tâm cũng cho đường tròn lớn bán kính R. Vì vậy, nếu đề nói nội tiếp hoặc tiếp xúc, hãy ưu tiên vẽ mặt cắt qua trục trước khi viết công thức thể tích.",
            2.0,
        )
        self.takeaway("Mẫu nhận dạng: khối tròn khó → cắt qua trục → giải bài toán phẳng.")

    # ======================================================
    # 3. CONE INSCRIBED IN A SPHERE: 3-4-5 SECTION
    # ======================================================
    def cone_in_sphere(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Nón nội tiếp mặt cầu","Bán kính cầu 5, chiều cao nón 8 — tìm bán kính đáy và thể tích","2/8")

        O=GC+DOWN*0.10; Rd=1.52
        S=O+UP*Rd
        H=O+DOWN*(3/5*Rd)
        rd=4/5*Rd
        A=H+LEFT*rd; B=H+RIGHT*rd
        sph=sphere_surface(O,Rd,BLUE,0.07)
        equ=horizontal_rim(O,Rd,BLUE,2.4)
        mer=meridian_circle(O,Rd,BLUE,2.2,0.62)
        cone=cone_surface(H,rd,float(S[2]-H[2]),PURPLE,0.075)
        base=horizontal_rim(H,rd,PURPLE,3.0)
        triangle=VGroup(solid(S,A,GOLD,4.1),solid(S,B,GOLD,4.1),solid(A,B,CYAN,3.4),aux(S,H,GREEN,3.0),solid(O,A,BLUE,3.0))
        mark=right_angle_3d(H,O-H,A-H,size=0.16,color=GOLD,width=3.4)
        dots=VGroup(*[Dot3D(p,radius=0.045,color=GOLD) for p in [S,O,H,A]])
        self.play(FadeIn(sph),Create(equ),Create(mer),FadeIn(cone),Create(base),run_time=0.95)
        self.play(Create(triangle),FadeIn(dots),Create(mark),run_time=0.85)
        self.add_label("S",S,RED,(-0.12,0,0.11),19); self.add_label("O",O,GOLD,(0.10,0.02,0.02),18); self.add_label("H",H,GOLD,(0.10,-0.02,-0.04),18); self.add_label("A",A,GOLD,(-0.13,0,-0.03),18)

        self.card("Lời giải","Tam giác vuông OHA là nút khóa",[
            ("math","O A = 5",27,BLUE),
            ("math","S H = 8",27,GREEN),
            ("math","O H = 8-5 = 3",27,INK),
            ("math","H A = sqrt(5^2-3^2) = 4",29,CYAN),
            ("sep",),
            ("math","V = frac(1, 3) pi 4^2 8 = frac(128 pi, 3)",30,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Xét nón nội tiếp mặt cầu bán kính năm, đỉnh nón là một điểm trên mặt cầu và đường tròn đáy cũng nằm trên mặt cầu. Chiều cao nón bằng tám. Trong mặt cắt qua trục, O là tâm đường tròn, S là đỉnh nón, H là tâm đáy và A là một điểm trên đường tròn đáy. Vì S O bằng năm và S H bằng tám nên O H bằng ba. Tam giác O H A vuông tại H, O A bằng bán kính cầu là năm, do đó H A bằng bốn.",
            2.0,
        )
        self.narrate(
            "Vậy bán kính đáy nón bằng bốn. Thể tích bằng một phần ba pi nhân mười sáu nhân tám, tức một trăm hai mươi tám pi trên ba. Điều đáng nhớ không phải bộ số ba bốn năm, mà là cấu trúc tổng quát: nếu cầu bán kính R và nón nội tiếp có chiều cao h thì khoảng cách từ tâm cầu đến mặt đáy là trị tuyệt đối của R trừ h, rồi bán kính đáy được tìm bằng Pythagore trong tam giác tâm, tâm đáy và điểm trên đường tròn đáy.",
            2.0,
        )
        self.takeaway("Nội tiếp cầu: luôn tìm tam giác vuông chứa bán kính cầu và bán kính đáy.")

    # ======================================================
    # 4. SPHERE INSCRIBED IN A 3-4-5 CONE
    # ======================================================
    def sphere_in_cone(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 2 · Cầu nội tiếp nón","Nón có r=3, h=4, đường sinh 5 — tìm bán kính cầu và tỷ số thể tích","3/8")

        H=GC+DOWN*1.10; rd=1.22; hd=1.63; S=H+UP*hd
        A=H+LEFT*rd; B=H+RIGHT*rd
        rho_d=rd*0.5  # physical rho/r = 1.5/3
        I=H+UP*rho_d
        cone=cone_surface(H,rd,hd,PURPLE,0.075)
        rim=horizontal_rim(H,rd,PURPLE,3.0)
        sph=sphere_surface(I,rho_d,BLUE,0.10)
        sph_eq=horizontal_rim(I,rho_d,BLUE,2.4)
        triangle=VGroup(solid(S,A,GOLD,4.0),solid(S,B,GOLD,4.0),solid(A,B,CYAN,3.2),aux(S,H,GREEN,2.7))
        incircle=meridian_circle(I,rho_d,BLUE,3.0,0.92)
        self.play(FadeIn(cone),Create(rim),Create(triangle),FadeIn(sph),Create(sph_eq),Create(incircle),run_time=1.1)
        self.add_label("S",S,RED,(-0.12,0,0.10),19); self.add_label("I",I,GOLD,(0.10,0.02,0.02),18); self.add_label("H",H,GOLD,(0.10,0,-0.05),18)

        self.card("Lời giải","Bán kính cầu = bán kính nội tiếp tam giác trục",[
            ("math","l = sqrt(3^2+4^2) = 5",28,CYAN),
            ("math","rho = frac(r h, r+l)",30,INK),
            ("math","rho = frac(3 times 4, 3+5) = frac(3, 2)",30,GOLD),
            ("sep",),
            ("math","frac(V_S, V_C) = frac(4 rho^3, r^2 h)",27,INK),
            ("math","frac(V_S, V_C) = frac(3, 8)",32,GREEN),
        ],accent=BLUE)
        self.narrate(
            "Bây giờ đảo bài toán: một mặt cầu nội tiếp hình nón có bán kính đáy ba và chiều cao bốn. Đường sinh bằng năm. Mặt cắt qua trục là tam giác cân có đáy sáu, chiều cao bốn và hai cạnh bên bằng năm. Mặt cầu nội tiếp nón trở thành đường tròn nội tiếp tam giác này. Do đó bán kính cầu chính là bán kính nội tiếp của tam giác trục, hoàn toàn là bài hình học phẳng.",
            2.0,
        )
        self.narrate(
            "Diện tích tam giác trục bằng r nhân h. Nửa chu vi bằng r cộng l. Vì vậy rho bằng r h chia r cộng l. Thay r bằng ba, h bằng bốn và l bằng năm, ta được rho bằng ba phần hai. Tỷ số thể tích cầu trên nón rút gọn thành bốn rho lập phương chia r bình phương nhân h, kết quả bằng ba phần tám. Đây là một ví dụ điển hình: quan hệ tiếp xúc được xử lý ở mặt cắt, còn thể tích chỉ dùng ở bước cuối.",
            2.0,
        )
        self.takeaway("Tiếp xúc nón–cầu: mặt cắt trục biến thành đường tròn nội tiếp tam giác cân.")

    # ======================================================
    # 5. CYLINDER INSCRIBED IN A SPHERE: OPTIMIZATION
    # ======================================================
    def cylinder_in_sphere(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 3 · Trụ nội tiếp cầu — cực trị","Tìm hình trụ có thể tích lớn nhất trong mặt cầu bán kính R","4/8")

        O=GC+DOWN*0.10; Rd=1.55
        # draw the optimal cylinder: h = 2R/sqrt3; r = R*sqrt(2/3)
        hd=2*Rd/math.sqrt(3); rd=Rd*math.sqrt(2/3)
        sph=sphere_surface(O,Rd,BLUE,0.065)
        sph_eq=horizontal_rim(O,Rd,BLUE,2.4)
        mer=meridian_circle(O,Rd,BLUE,2.2,0.62)
        cyl=cylinder_surface(O,rd,hd,CYAN,0.09)
        rims=VGroup(horizontal_rim(O+UP*hd/2,rd,CYAN,2.8),horizontal_rim(O+DOWN*hd/2,rd,CYAN,2.8))
        rect=VGroup(
            solid(O+LEFT*rd+DOWN*hd/2,O+LEFT*rd+UP*hd/2,GOLD,3.6),
            solid(O+RIGHT*rd+DOWN*hd/2,O+RIGHT*rd+UP*hd/2,GOLD,3.6),
            solid(O+LEFT*rd+UP*hd/2,O+RIGHT*rd+UP*hd/2,GOLD,3.0),
            solid(O+LEFT*rd+DOWN*hd/2,O+RIGHT*rd+DOWN*hd/2,GOLD,3.0),
        )
        radius_line=solid(O,O+RIGHT*rd+UP*hd/2,BLUE,3.0)
        half_h=aux(O,O+UP*hd/2,GREEN,2.8)
        rseg=solid(O+UP*hd/2,O+RIGHT*rd+UP*hd/2,CYAN,2.8)
        mark=right_angle_3d(O+UP*hd/2,DOWN,RIGHT,size=0.14,color=GOLD,width=3.2)
        self.play(FadeIn(sph),Create(sph_eq),Create(mer),FadeIn(cyl),Create(rims),Create(rect),run_time=1.05)
        self.play(Create(radius_line),Create(half_h),Create(rseg),Create(mark),run_time=0.75)

        self.card("Cực trị","Một tam giác vuông quyết định toàn bộ",[
            ("math","r^2 + frac(h^2, 4) = R^2",29,CYAN),
            ("math","V(h) = pi (R^2-frac(h^2, 4)) h",27,INK),
            ("math","V'(h) = pi (R^2-frac(3 h^2, 4))",27,INK),
            ("math","h = frac(2 R, sqrt(3))",30,GOLD),
            ("math","r = R sqrt(frac(2, 3))",28,GREEN),
            ("math","V_m = frac(4 pi R^3, 3 sqrt(3))",29,GOLD),
        ],accent=CYAN)
        self.narrate(
            "Một hình trụ nội tiếp mặt cầu bán kính R. Trong mặt cắt qua trục, hình trụ trở thành hình chữ nhật nội tiếp đường tròn bán kính R. Nửa chiều cao hình trụ, bán kính đáy và bán kính cầu tạo thành tam giác vuông. Vì thế r bình cộng h bình trên bốn bằng R bình. Đây là ràng buộc hình học duy nhất cần giữ lại.",
            1.8,
        )
        self.narrate(
            "Thể tích trụ bằng pi r bình h. Thay r bình bằng R bình trừ h bình trên bốn, ta được một hàm theo h. Đạo hàm cho R bình trừ ba h bình trên bốn. Trong miền không suy biến, cực đại xảy ra khi h bằng hai R trên căn ba. Khi đó r bằng R căn hai phần ba và thể tích lớn nhất bằng bốn pi R lập phương chia ba căn ba. Ta không tối ưu trực tiếp trong không gian; mặt cắt trục đã biến bài toán thành một biến duy nhất.",
            2.2,
        )
        self.takeaway("Cực trị khối tròn: tìm ràng buộc 2D trước, rồi mới lập hàm thể tích.")

    # ======================================================
    # 6. FRUSTUM FORMULA FROM SIMILARITY
    # ======================================================
    def frustum_similarity(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 4 · Chóp cụt tròn xoay","Tự dựng công thức thể tích từ đồng dạng — không học thuộc mù","5/8")

        H0=GC+DOWN*1.18; Rd=1.48; rd=0.74; hd=1.32
        fr=frustum_surface(H0,Rd,rd,hd,ORANGE,0.09)
        rims=VGroup(horizontal_rim(H0,Rd,ORANGE,3.0),horizontal_rim(H0+UP*hd,rd,ORANGE,3.0))
        # Extended apex using similarity, numerical R=6,r=3,h=4 -> removed height x=4, total 8.
        apex=H0+UP*(2*hd)
        gen=VGroup(aux(H0+LEFT*Rd,apex,GOLD,2.8),aux(H0+RIGHT*Rd,apex,GOLD,2.8),axis_line(H0[2],apex[2],H0[:2],DIM))
        self.play(FadeIn(fr),Create(rims),Create(gen),run_time=1.0)
        self.add_label("S",apex,RED,(-0.10,0,0.10),18)

        self.card("Suy ra công thức","Kéo dài đường sinh tới đỉnh S",[
            ("math","frac(r, R) = frac(x, x+h)",28,CYAN),
            ("math","x = frac(r h, R-r)",29,INK),
            ("math","V = frac(pi h, 3) (R^2+R r+r^2)",31,GOLD),
            ("sep",),
            ("math","R=6, r=3, h=4",27,INK),
            ("math","V = 84 pi",33,GREEN),
        ],accent=ORANGE)
        self.narrate(
            "Với chóp cụt tròn xoay, thay vì nhớ ngay công thức dài, ta kéo dài hai đường sinh cho tới đỉnh S của nón lớn. Gọi x là chiều cao nón nhỏ bị cắt đi. Đồng dạng cho r trên R bằng x trên x cộng h, nên x bằng r h chia R trừ r. Thể tích chóp cụt bằng thể tích nón lớn trừ nón nhỏ. Thay x vào và rút gọn, ta nhận được pi h trên ba nhân R bình cộng R r cộng r bình.",
            2.1,
        )
        self.narrate(
            "Ví dụ đáy lớn bán kính sáu, đáy nhỏ bán kính ba và chiều cao chóp cụt bằng bốn. Thể tích là bốn pi trên ba nhân ba mươi sáu cộng mười tám cộng chín, tức tám mươi bốn pi. Với bộ số này, hiệu hai bán kính bằng ba và chiều cao bằng bốn, nên đường sinh chóp cụt bằng năm. Đây cũng là một cách kiểm tra hình: tam giác vuông tạo bởi chiều cao, hiệu hai bán kính và đường sinh phải nhất quán.",
            2.0,
        )
        self.takeaway("Chóp cụt: kéo dài về nón lớn → đồng dạng → hiệu hai thể tích.")

    # ======================================================
    # 7. SPHERE INSCRIBED IN A FRUSTUM: DEEP ELEGANT RESULT
    # ======================================================
    def sphere_in_frustum(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 5 · Cầu nội tiếp chóp cụt","Một kết quả đẹp: bán kính cầu là trung bình nhân của hai bán kính đáy","6/8")

        # Physical example R=9, r=4, h=12, rho=6, l=13. Display scaled.
        H0=GC+DOWN*1.23; Rd=1.45; rd=Rd*(4/9); hd=Rd*(12/9)
        rho_d=hd/2; I=H0+UP*rho_d
        fr=frustum_surface(H0,Rd,rd,hd,ORANGE,0.085)
        rims=VGroup(horizontal_rim(H0,Rd,ORANGE,3.0),horizontal_rim(H0+UP*hd,rd,ORANGE,3.0))
        sph=sphere_surface(I,rho_d,BLUE,0.11)
        eq=horizontal_rim(I,rho_d,BLUE,2.5)
        # axial trapezoid
        A=H0+LEFT*Rd; B=H0+RIGHT*Rd; C=H0+UP*hd+RIGHT*rd; D=H0+UP*hd+LEFT*rd
        trap=VGroup(solid(A,B,GOLD,3.6),solid(B,C,GOLD,3.6),solid(C,D,GOLD,3.6),solid(D,A,GOLD,3.6),aux(I,H0,GREEN,2.8))
        inc=meridian_circle(I,rho_d,BLUE,3.0,0.90)
        self.play(FadeIn(fr),Create(rims),FadeIn(sph),Create(eq),Create(trap),Create(inc),run_time=1.15)

        self.card("Kết quả đẹp","Mặt cắt trục là hình thang cân ngoại tiếp đường tròn",[
            ("math","l = R+r",28,CYAN),
            ("math","h^2 = l^2-(R-r)^2 = 4 R r",27,INK),
            ("math","h = 2 sqrt(R r)",29,GOLD),
            ("math","rho = frac(h, 2) = sqrt(R r)",30,GREEN),
            ("sep",),
            ("math","R=9, r=4",27,INK),
            ("math","l=13, h=12, rho=6",29,GOLD),
        ],accent=BLUE)
        self.narrate(
            "Bài cuối là một cấu hình đẹp và ít khi được khai thác đủ sâu. Một mặt cầu tiếp xúc với cả hai đáy và mặt bên của chóp cụt tròn xoay. Mặt cắt qua trục cho hình thang cân ngoại tiếp một đường tròn. Với tứ giác có đường tròn nội tiếp, tổng hai cạnh đối bằng nhau. Hai đáy của hình thang dài hai R và hai r, hai cạnh bên cùng bằng l, nên l bằng R cộng r.",
            2.0,
        )
        self.narrate(
            "Mặt khác, trong nửa hình thang, chiều cao h, hiệu hai bán kính R trừ r và đường sinh l tạo tam giác vuông. Vì vậy h bình bằng l bình trừ R trừ r tất cả bình. Thay l bằng R cộng r, ta được h bình bằng bốn R r. Do mặt cầu tiếp xúc hai đáy song song, đường kính cầu chính là h. Suy ra rho bằng căn R r. Nghĩa là bán kính cầu là trung bình nhân của hai bán kính đáy.",
            2.1,
        )
        self.narrate(
            "Với R bằng chín và r bằng bốn, ta có l bằng mười ba, h bằng mười hai và bán kính cầu bằng sáu. Bộ số bốn, chín, sáu không ngẫu nhiên: sáu chính là căn của ba mươi sáu. Đây là kiểu kết quả nên nhớ bằng cấu trúc chứng minh, không nhớ như một công thức lẻ. Chỉ cần quên điều kiện mặt cầu tiếp xúc đủ bốn mặt của hình thang trục thì công thức rho bằng căn R r không còn đúng.",
            2.0,
        )
        self.takeaway("Tiếp xúc đủ: dùng điều kiện tứ giác ngoại tiếp trước, Pythagore sau.")

    # ======================================================
    # 8. COMMON PITFALLS
    # ======================================================
    def pitfalls(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bốn lỗi dễ làm hỏng cả bài","Khối tròn ít công thức nhưng rất dễ gán sai quan hệ hình học","7/8")
        left=VGroup(
            VGroup(txt("01",15,RED,BOLD),txt("Cầu trong nón",18,INK,BOLD),txt("không có",17,MUTED),mty("rho = frac(h, 2)",23,RED)).arrange(RIGHT,buff=0.11),
            VGroup(txt("02",15,RED,BOLD),txt("Trụ trong cầu",18,INK,BOLD),txt("phải dùng",17,MUTED),mty("frac(h, 2)",23,CYAN),txt("trong tam giác vuông",17,MUTED)).arrange(RIGHT,buff=0.11),
            VGroup(txt("03",15,RED,BOLD),txt("Chóp cụt",18,INK,BOLD),txt("R, r là bán kính, không phải đường kính",17,MUTED)).arrange(RIGHT,buff=0.11),
            VGroup(txt("04",15,RED,BOLD),mty("rho = sqrt(R r)",23,GREEN),txt("chỉ đúng khi cầu tiếp xúc đủ các mặt",17,MUTED)).arrange(RIGHT,buff=0.11),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34).shift(LEFT*2.55+UP*0.10)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Tự kiểm tra","Trước khi bấm máy",[
            ("text","1. Mặt cắt qua trục đã đúng chưa?",17,INK,BOLD),
            ("text","2. Quan hệ vuông góc / tiếp xúc lấy từ đâu?",17,INK,BOLD),
            ("text","3. Đại lượng đang dùng là bán kính hay đường kính?",17,INK,BOLD),
            ("text","4. Công thức đặc biệt có đủ điều kiện không?",17,INK,BOLD),
        ],accent=RED)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.7)
        self.narrate(
            "Có bốn lỗi rất đáng tránh. Thứ nhất, mặt cầu nội tiếp nón không có bán kính bằng nửa chiều cao nón; điều đó chỉ đúng với cầu tiếp xúc hai mặt phẳng song song cách nhau đúng một đường kính. Trong nón, bán kính cầu phải được tìm từ đường tròn nội tiếp tam giác trục. Thứ hai, với trụ nội tiếp cầu, cạnh đứng của tam giác vuông là nửa chiều cao trụ chứ không phải toàn bộ h. Sai chỗ này thì cả ràng buộc và cực trị đều sai.",
            2.0,
        )
        self.narrate(
            "Thứ ba, công thức chóp cụt dùng hai bán kính R và r. Nếu đề cho đường kính thì phải chia đôi trước. Thứ tư, kết quả rho bằng căn R r rất đẹp nhưng có điều kiện mạnh: mặt cầu phải tiếp xúc cả hai đáy và mặt bên của chóp cụt. Không được thấy hai bán kính đáy rồi áp dụng ngay. Một cách tự kiểm tra tốt là luôn nói thành lời nguồn gốc của mỗi quan hệ: do Pythagore, do đồng dạng, do tiếp xúc hay do điều kiện tứ giác ngoại tiếp.",
            2.0,
        )

    # ======================================================
    # 9. SUMMARY
    # ======================================================
    def summary(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ phương pháp khối tròn","Năm bài — một ngôn ngữ chung: mặt cắt qua trục","8/8")
        left=VGroup(
            VGroup(txt("1",16,GOLD,BOLD),txt("Nón nội tiếp cầu",19,INK,BOLD),txt("→ Pythagore",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("2",16,GOLD,BOLD),txt("Cầu nội tiếp nón",19,INK,BOLD),txt("→ đường tròn nội tiếp",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("3",16,GOLD,BOLD),txt("Trụ nội tiếp cầu",19,INK,BOLD),txt("→ ràng buộc + cực trị",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("4",16,GOLD,BOLD),txt("Chóp cụt",19,INK,BOLD),txt("→ đồng dạng",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("5",16,GOLD,BOLD),txt("Cầu trong chóp cụt",19,INK,BOLD),txt("→ tứ giác ngoại tiếp",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.31).shift(LEFT*2.70+UP*0.05)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Chốt","Đừng bắt đầu bằng thể tích",[
            ("text","Bước 1: vẽ mặt cắt qua trục.",17,INK,BOLD),
            ("text","Bước 2: giải quan hệ dài / tiếp xúc trong 2D.",17,INK,BOLD),
            ("text","Bước 3: mới quay lại diện tích, thể tích hoặc cực trị.",17,INK,BOLD),
            ("sep",),
            ("math","rho = frac(r h, r+l)",27,CYAN),
            ("math","V_f = frac(pi h, 3) (R^2+R r+r^2)",26,GOLD),
            ("math","rho = sqrt(R r)",28,GREEN),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.7)
        self.narrate(
            "Video mười ba không nhằm gom thật nhiều công thức. Năm bài được chọn để tạo một bản đồ phương pháp. Nón nội tiếp cầu dùng tam giác vuông trong mặt cắt. Cầu nội tiếp nón dùng đường tròn nội tiếp tam giác. Trụ nội tiếp cầu dùng hình chữ nhật nội tiếp đường tròn rồi mới tối ưu. Chóp cụt dùng đồng dạng. Cầu nội tiếp chóp cụt dùng điều kiện tứ giác ngoại tiếp trước khi dùng Pythagore. Điểm chung là mọi quan hệ khó trong ba chiều đều được giải quyết ở mặt cắt qua trục.",
            2.2,
        )
        self.narrate(
            "Sang video mười bốn, ta giữ các công cụ này nhưng chuyển sang mô hình thực tế ba chiều: bồn chứa, phễu, mái vòm, ống trụ, khối ghép và bài toán vật liệu. Khi ấy việc chọn đúng mô hình và đơn vị sẽ quan trọng ngang với việc tính toán. Nếu nắm chắc video này, phần mô hình thực tế sẽ không còn là học thêm công thức mà chỉ là nhận dạng đúng cấu trúc.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.axial_dictionary()
        self.cone_in_sphere()
        self.sphere_in_cone()
        self.cylinder_in_sphere()
        self.frustum_similarity()
        self.sphere_in_frustum()
        self.pitfalls()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_13_non_tru_cau_chop_cut_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst) SAFE")
    print("Render policy: low-resolution 3D surfaces, fixed camera, no ambient rotation")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_13.wav"
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
