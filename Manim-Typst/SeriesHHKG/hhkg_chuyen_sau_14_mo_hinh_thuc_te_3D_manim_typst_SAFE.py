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
# HHKG CHUYEN SAU 14 - MO HINH THUC TE 3D
# Manim Community + MathTypst SAFE | Standalone 100%
# Muc tieu: 12-14 phut, 5 mo hinh thuc te, dung hinh chuan va giai den noi den chon.
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

# ==========================================================
# EXTRA REAL-WORLD SOLID HELPERS
# ==========================================================
def hemisphere_surface(base_center, radius, color=BLUE, opacity=0.09):
    c = np.array(base_center, dtype=float)
    return low_surface(
        lambda u, v: c + radius*np.array([math.sin(u)*math.cos(v), math.sin(u)*math.sin(v), math.cos(u)]),
        [0, PI/2], [0, TAU], color=color, opacity=opacity, resolution=(8, 24)
    )


def cone_surface_down(base_center, radius, height, color=ORANGE, opacity=0.09):
    c = np.array(base_center, dtype=float)
    return low_surface(
        lambda u, v: c + np.array([(1-u)*radius*math.cos(v), (1-u)*radius*math.sin(v), -u*height]),
        [0, 1], [0, TAU], color=color, opacity=opacity, resolution=(8, 24)
    )


def disk_face(center, radius, color=BLUE, opacity=0.10, resolution=48):
    c = np.array(center, dtype=float)
    pts = [c + radius*np.array([math.cos(t), math.sin(t), 0.0]) for t in np.linspace(0, TAU, resolution, endpoint=False)]
    return Polygon(*pts, fill_color=color, fill_opacity=opacity, stroke_width=0)

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
        series=txt("HHKG CHUYÊN SÂU · 14",15,BLUE,BOLD)
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
        title=txt("HHKG CHUYÊN SÂU 14",45,GOLD,BOLD)
        sub=txt("MÔ HÌNH THỰC TẾ 3D",32,INK,BOLD)
        line=txt("Bồn chứa · silo · mái vòm · ống thép · thiết kế tối ưu",22,CYAN,BOLD)
        note=txt("Mô hình đúng trước — công thức sau — đơn vị cuối cùng phải đúng",21,MUTED)
        brand=txt(TEN_THAY,18,MUTED)
        VGroup(title,sub,line,note,brand).arrange(DOWN,buff=0.28)
        self.play(FadeIn(title,shift=UP*0.15),FadeIn(sub),run_time=0.85)
        self.play(FadeIn(line),FadeIn(note),FadeIn(brand),run_time=0.75)
        self.narrate(
            "Video mười bốn chuyển toàn bộ công cụ hình học không gian sang mô hình thực tế. Điều khó nhất của bài toán kiểu này thường không phải phép tính. Khó nhất là đọc đúng vật thể, tách nó thành các khối quen thuộc, xác định phần nào cần tính thể tích, phần nào cần tính diện tích, rồi giữ đơn vị nhất quán. Thầy chọn năm mô hình đủ khác nhau: bồn chứa có mái bán cầu, silo có phễu nón, mái vòm cần ốp vật liệu, ống thép rỗng và một bài thiết kế lon tối ưu. Mỗi bài đều có một lỗi mô hình rất dễ mắc nếu chỉ nhìn công thức.",
            2.0,
        )

    # ======================================================
    # 2. MODELING WORKFLOW
    # ======================================================
    def modeling_workflow(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Quy trình mô hình hóa 3D","Bốn bước để tránh tính đúng một mô hình sai","1/7")
        steps=VGroup(
            VGroup(txt("01",16,GOLD,BOLD),txt("TÁCH KHỐI",20,INK,BOLD),txt("Nhận ra trụ, nón, bán cầu, vành khăn...",17,MUTED)).arrange(RIGHT,buff=0.14),
            VGroup(txt("02",16,GOLD,BOLD),txt("CHỌN ĐẠI LƯỢNG",20,INK,BOLD),txt("Thể tích? diện tích cong? vật liệu? khối lượng?",17,MUTED)).arrange(RIGHT,buff=0.14),
            VGroup(txt("03",16,GOLD,BOLD),txt("GIỮ ĐƠN VỊ",20,INK,BOLD),txt("Đổi hết về cùng hệ trước khi tính.",17,MUTED)).arrange(RIGHT,buff=0.14),
            VGroup(txt("04",16,GOLD,BOLD),txt("KIỂM TRA",20,INK,BOLD),txt("Kích thước, đơn vị và độ lớn có hợp lý không?",17,MUTED)).arrange(RIGHT,buff=0.14),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.38).shift(LEFT*2.65+UP*0.10)
        self.add_fixed_in_frame_mobjects(steps)
        self.card("Checklist","Trước khi thế số",[
            ("text","Thể tích → đơn vị khối.",18,INK,BOLD),
            ("text","Diện tích → đơn vị vuông.",18,INK,BOLD),
            ("text","Khối lượng = thể tích × khối lượng riêng.",17,INK,BOLD),
            ("sep",),
            ("math","m = rho V",28,CYAN),
            ("math","C = A c",28,GOLD),
        ],accent=BLUE)
        self.play(FadeIn(steps,shift=RIGHT*0.10),run_time=0.8)
        self.narrate(
            "Trước khi vào bài cụ thể, hãy khóa một quy trình. Bước một, tách vật thể thành những khối cơ bản. Bước hai, đọc đúng đại lượng cần tìm. Nếu hỏi sức chứa thì cần thể tích phần rỗng. Nếu hỏi sơn, tôn hay vật liệu phủ thì cần diện tích bề mặt thực sự được phủ, không phải toàn bộ diện tích của khối. Nếu hỏi khối lượng, ta phải nhân thể tích vật liệu với khối lượng riêng. Bước ba, đổi đơn vị trước khi nhân. Bước bốn, kiểm tra độ lớn. Một bồn vài mét mà cho ra vài chục lít chắc chắn là sai mô hình hoặc sai đơn vị.",
            2.0,
        )
        self.takeaway("Đừng tính ngay. Hãy trả lời trước: vật thể gồm những khối nào và phần nào thật sự được tính?")

    # ======================================================
    # 3. TANK: CYLINDER + HEMISPHERE
    # ======================================================
    def tank(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Bồn chứa có mái bán cầu","r = 2 m, thân trụ cao 5 m — tính sức chứa và chi phí phủ mặt trong","2/7")

        base=GC+DOWN*1.45; r=1.25; h=2.25; top=base+UP*h
        cyl=cylinder_surface(base+UP*h/2,r,h,CYAN,0.075)
        dome=hemisphere_surface(top,r,BLUE,0.095)
        rims=VGroup(horizontal_rim(base,r,CYAN,3.0),horizontal_rim(top,r,CYAN,2.7))
        sides=VGroup(solid(base+LEFT*r,top+LEFT*r,CYAN,3.3),solid(base+RIGHT*r,top+RIGHT*r,CYAN,3.3))
        axis=aux(base,top+UP*r,DIM,2.1,0.60,0.08)
        self.play(FadeIn(cyl),FadeIn(dome),Create(rims),Create(sides),Create(axis),run_time=1.10)

        card1=self.card("Mô hình","Trụ + nửa cầu, không đếm mặt tròn ở chỗ ghép",[
            ("math","V = pi r^2 h + frac(2, 3) pi r^3",28,CYAN),
            ("math","V = 20 pi + frac(16 pi, 3) = frac(76 pi, 3)",27,GOLD),
            ("math","V = 79.59",29,GREEN),
            ("sep",),
            ("math","A = 2 pi r h + 2 pi r^2 + pi r^2",25,INK),
            ("math","A = 32 pi = 100.53",27,CYAN),
        ],accent=BLUE)
        self.narrate(
            "Bồn thứ nhất gồm một thân trụ bán kính hai mét, cao năm mét, phía trên là một mái bán cầu cùng bán kính. Sức chứa là tổng thể tích thân trụ và nửa quả cầu. Phần tròn ở chỗ nối giữa trụ và mái không phải một bề mặt riêng của khoang chứa, nên tuyệt đối không cộng thêm diện tích hay thể tích ở đó. Ta được V bằng pi r bình h cộng hai phần ba pi r lập phương, tức bảy mươi sáu pi trên ba, xấp xỉ bảy mươi chín phẩy năm chín mét khối.",
            2.1,
        )
        self.narrate(
            "Bây giờ tính diện tích cần phủ lớp chống ăn mòn ở mặt trong, giả sử phủ thân trụ, mái bán cầu và đáy dưới. Diện tích là hai pi r h cộng hai pi r bình cộng pi r bình, bằng ba mươi hai pi, xấp xỉ một trăm phẩy năm ba mét vuông. Nếu dự trù tám phần trăm hao hụt thì diện tích vật liệu quy đổi là khoảng một trăm linh tám phẩy năm bảy mét vuông. Với đơn giá một trăm tám mươi nghìn đồng trên mét vuông, chi phí lý thuyết khoảng mười chín phẩy năm bốn triệu đồng.",
            2.1,
        )
        self.play(FadeOut(card1),run_time=0.30)
        self.card("Chi phí","Có 8% hao hụt vật liệu",[
            ("math","A_p = 1.08 times 32 pi = 108.57",27,INK),
            ("text","Đơn giá: 180 000 đồng/m²",17,MUTED,NORMAL),
            ("text","Chi phí ≈ 19,54 triệu đồng",19,GOLD,BOLD),
            ("sep",),
            ("text","Sai thường gặp: cộng thêm mặt tròn ở chỗ nối.",16,RED,BOLD),
        ],accent=GOLD)
        self.narrate("Chốt bài bồn chứa: sức chứa dùng thể tích hai khoang, còn chi phí phủ dùng đúng các mặt thật sự tiếp xúc với lớp phủ. Mặt tròn ở chỗ ghép giữa thân trụ và mái bán cầu là mặt nội bộ nên không được đếm thêm.",1.2)
        self.takeaway("Khối ghép: mặt chung ở bên trong không được tính như một bề mặt ngoài.")

    # ======================================================
    # 4. SILO: CYLINDER + CONICAL HOPPER
    # ======================================================
    def silo(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 2 · Silo có phễu nón","r = 3 m, thân trụ 8 m, phễu nón cao 4 m — sức chứa và khối lượng hạt","3/7")

        joint=GC+DOWN*0.85; r=1.28; hc=2.25; hh=1.05
        cyl_center=joint+UP*hc/2
        cyl=cylinder_surface(cyl_center,r,hc,GREEN,0.075)
        hopper=cone_surface_down(joint,r,hh,ORANGE,0.10)
        rims=VGroup(horizontal_rim(joint,r,GREEN,2.8),horizontal_rim(joint+UP*hc,r,GREEN,3.0))
        sides=VGroup(solid(joint+LEFT*r,joint+UP*hc+LEFT*r,GREEN,3.2),solid(joint+RIGHT*r,joint+UP*hc+RIGHT*r,GREEN,3.2),solid(joint+LEFT*r,joint+DOWN*hh,ORANGE,3.3),solid(joint+RIGHT*r,joint+DOWN*hh,ORANGE,3.3))
        axis=aux(joint+DOWN*hh,joint+UP*hc,DIM,2.0,0.55,0.08)
        self.play(FadeIn(cyl),FadeIn(hopper),Create(rims),Create(sides),Create(axis),run_time=1.10)

        self.card("Sức chứa","Cộng đúng hai khoang",[
            ("math","V_t = pi 3^2 8 = 72 pi",28,GREEN),
            ("math","V_n = frac(1, 3) pi 3^2 4 = 12 pi",28,ORANGE),
            ("math","V = 84 pi = 263.89",29,GOLD),
            ("sep",),
            ("math","m = 0.75 V = 63 pi",27,CYAN),
            ("math","m = 197.92",29,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Mô hình thứ hai là silo có thân trụ và phễu nón phía dưới. Bán kính ba mét, phần trụ cao tám mét, phần nón cao bốn mét. Thể tích phần trụ là bảy mươi hai pi. Thể tích phễu nón là một phần ba pi nhân chín nhân bốn, bằng mười hai pi. Tổng sức chứa là tám mươi bốn pi, xấp xỉ hai trăm sáu mươi ba phẩy tám chín mét khối.",
            2.0,
        )
        self.narrate(
            "Nếu loại hạt có khối lượng riêng biểu kiến bằng không phẩy bảy lăm tấn trên mét khối, khối lượng khi silo đầy là không phẩy bảy lăm nhân tám mươi bốn pi, tức sáu mươi ba pi tấn, xấp xỉ một trăm chín mươi bảy phẩy chín hai tấn. Đây là chỗ phải phân biệt khối lượng riêng biểu kiến của vật liệu rời với khối lượng riêng của chất rắn cấu tạo nên từng hạt. Trong bài toán sức chứa silo, đề thường cho trực tiếp giá trị biểu kiến để nhân với thể tích khoang chứa.",
            2.0,
        )
        self.takeaway("Sức chứa dùng thể tích rỗng; khối lượng hàng chứa = thể tích khoang × khối lượng riêng biểu kiến.")

    # ======================================================
    # 5. HEMISPHERICAL DOME: MATERIAL + PANELS
    # ======================================================
    def dome(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 3 · Mái vòm bán cầu","R = 6 m — ốp tấm ngoài, có 8% hao hụt vật liệu","4/7")

        c=GC+DOWN*1.15; R=1.65
        hemi=hemisphere_surface(c,R,PURPLE,0.11)
        rim=horizontal_rim(c,R,PURPLE,3.1)
        mer1=ParametricFunction(lambda t: c+R*np.array([math.cos(t),0,math.sin(t)]),t_range=[0,PI],color=GOLD,stroke_width=3.0)
        mer2=ParametricFunction(lambda t: c+R*np.array([0,math.cos(t),math.sin(t)]),t_range=[0,PI],color=CYAN,stroke_width=2.2,stroke_opacity=0.65)
        self.play(FadeIn(hemi),Create(rim),Create(mer1),Create(mer2),run_time=1.0)

        self.card("Vật liệu phủ","Chỉ tính mặt cong của mái",[
            ("math","A = 2 pi R^2",29,CYAN),
            ("math","A = 72 pi = 226.19",28,GOLD),
            ("math","A_p = 1.08 A = 244.29",27,INK),
            ("sep",),
            ("text","Mỗi tấm phủ được 1,5 m²",17,MUTED,NORMAL),
            ("text","Cần 163 tấm; chi phí 68,46 triệu đồng",17,GOLD,BOLD),
        ],accent=PURPLE)
        self.narrate(
            "Mô hình thứ ba là mái vòm bán cầu bán kính sáu mét. Vì đây là mái phủ phía trên công trình, ta chỉ tính diện tích mặt cong của bán cầu, không cộng diện tích hình tròn đáy. Diện tích mặt cong bằng hai pi R bình, tức bảy mươi hai pi, xấp xỉ hai trăm hai mươi sáu phẩy một chín mét vuông. Sau khi cộng tám phần trăm hao hụt do cắt ghép và mép nối, diện tích quy đổi khoảng hai trăm bốn mươi bốn phẩy hai chín mét vuông.",
            2.0,
        )
        self.narrate(
            "Mỗi tấm vật liệu phủ được một phẩy năm mét vuông, nên số tấm theo mô hình diện tích là hai trăm bốn mươi bốn phẩy hai chín chia một phẩy năm, rồi phải làm tròn lên vì không thể mua một phần tấm. Ta cần một trăm sáu mươi ba tấm. Nếu mỗi tấm giá bốn trăm hai mươi nghìn đồng thì chi phí vật liệu là sáu mươi tám phẩy bốn sáu triệu đồng. Trong thực tế, cách chia tấm còn phụ thuộc hình dạng tấm và sơ đồ ghép; bài toán ở đây đã gom ảnh hưởng ấy vào hệ số hao hụt tám phần trăm.",
            2.1,
        )
        self.takeaway("Bài vật liệu: xác định đúng bề mặt được phủ, rồi mới cộng hao hụt và làm tròn số lượng.")

    # ======================================================
    # 6. HOLLOW STEEL PIPE
    # ======================================================
    def pipe(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 4 · Ống thép rỗng","D ngoài 0,30 m, dày 0,02 m, dài 6 m — tính khối lượng ống","5/7")

        c=GC+DOWN*0.15; Ro=1.28; Ri=Ro*(0.13/0.15); hd=2.65
        outer=cylinder_surface(c,Ro,hd,BLUE,0.075)
        inner=cylinder_surface(c,Ri,hd,RED,0.055)
        top=c+UP*hd/2; bot=c+DOWN*hd/2
        rims=VGroup(horizontal_rim(top,Ro,BLUE,3.0),horizontal_rim(bot,Ro,BLUE,3.0),horizontal_rim(top,Ri,RED,2.4),horizontal_rim(bot,Ri,RED,2.4))
        cap_outer=disk_face(top,Ro,BLUE,0.18); cap_inner=disk_face(top+UP*0.002,Ri,BG,0.98)
        self.play(FadeIn(outer),FadeIn(inner),FadeIn(cap_outer),FadeIn(cap_inner),Create(rims),run_time=1.0)

        self.card("Vành khăn","Thể tích thép = trụ ngoài − trụ rỗng",[
            ("math","R = 0.15, r = 0.13, L = 6",27,CYAN),
            ("math","V = pi (R^2-r^2) L",29,INK),
            ("math","V = 0.0336 pi = 0.10556",27,GOLD),
            ("sep",),
            ("math","m = 7850 V",28,CYAN),
            ("math","m = 828.63",29,GOLD),
        ],accent=BLUE)
        self.narrate(
            "Mô hình thứ tư là một đoạn ống thép dài sáu mét, đường kính ngoài ba mươi xăng ti mét và chiều dày thành ống hai xăng ti mét. Trước tiên phải đổi từ đường kính sang bán kính. Bán kính ngoài là không phẩy mười lăm mét. Bán kính trong không phải không phẩy mười ba do đo trực tiếp từ đường kính, mà do lấy bán kính ngoài trừ chiều dày không phẩy không hai, nên đúng bằng không phẩy mười ba mét.",
            2.0,
        )
        self.narrate(
            "Thể tích thép là thể tích trụ ngoài trừ thể tích khoang rỗng: pi nhân R bình trừ r bình rồi nhân chiều dài. Kết quả bằng không phẩy không ba ba sáu pi, xấp xỉ không phẩy một không năm năm sáu mét khối. Với khối lượng riêng thép bảy nghìn tám trăm năm mươi ki lô gam trên mét khối, khối lượng đoạn ống xấp xỉ tám trăm hai mươi tám phẩy sáu ba ki lô gam. Sai lầm thường gặp nhất là trừ chiều dày khỏi đường kính thay vì khỏi bán kính.",
            2.1,
        )
        self.takeaway("Ống rỗng: đổi đường kính → bán kính, rồi dùng diện tích vành khăn nhân chiều dài.")

    # ======================================================
    # 7. OPTIMAL CLOSED CYLINDER CAN
    # ======================================================
    def optimal_can(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 5 · Thiết kế lon kín tối ưu","Thể tích cố định 250π cm³ — tìm r, h để dùng ít vật liệu nhất","6/7")

        c=GC+DOWN*0.10; rd=1.10; hd=2.20
        cyl=cylinder_surface(c,rd,hd,CYAN,0.09)
        rims=VGroup(horizontal_rim(c+UP*hd/2,rd,CYAN,3.0),horizontal_rim(c+DOWN*hd/2,rd,CYAN,3.0))
        sides=VGroup(solid(c+LEFT*rd+DOWN*hd/2,c+LEFT*rd+UP*hd/2,CYAN,3.2),solid(c+RIGHT*rd+DOWN*hd/2,c+RIGHT*rd+UP*hd/2,CYAN,3.2))
        rect=face(c+LEFT*rd+DOWN*hd/2,c+RIGHT*rd+DOWN*hd/2,c+RIGHT*rd+UP*hd/2,c+LEFT*rd+UP*hd/2,color=GOLD,opacity=0.05)
        caps=VGroup(disk_face(c+UP*hd/2,rd,CYAN,0.10),disk_face(c+DOWN*hd/2,rd,CYAN,0.10))
        self.play(FadeIn(cyl),FadeIn(caps),Create(rims),Create(sides),FadeIn(rect),run_time=1.0)

        card1=self.card("Tối ưu vật liệu","Lon kín: có cả hai đáy",[
            ("math","pi r^2 h = 250 pi",28,CYAN),
            ("math","h = frac(250, r^2)",28,INK),
            ("math","S(r) = 2 pi r^2 + frac(500 pi, r)",27,INK),
            ("math","S'(r) = 4 pi r - frac(500 pi, r^2)",26,CYAN),
            ("math","r^3 = 125",29,GOLD),
            ("math","r=5, h=10",31,GREEN),
        ],accent=GOLD)
        self.narrate(
            "Bài cuối là thiết kế một lon hình trụ kín có thể tích cố định hai trăm năm mươi pi xăng ti mét khối. Ta muốn dùng ít vật liệu nhất, nghĩa là tối thiểu diện tích toàn phần gồm hai đáy và mặt xung quanh. Từ pi r bình h bằng hai trăm năm mươi pi, suy ra h bằng hai trăm năm mươi chia r bình. Thay vào diện tích S bằng hai pi r bình cộng hai pi r h, ta được S của r bằng hai pi r bình cộng năm trăm pi chia r.",
            2.0,
        )
        self.narrate(
            "Đạo hàm theo r: S phẩy bằng bốn pi r trừ năm trăm pi chia r bình. Cho bằng không, ta có r lập phương bằng một trăm hai mươi lăm, nên r bằng năm xăng ti mét. Khi đó h bằng mười xăng ti mét. Kết quả có một ý nghĩa rất đẹp: với hình trụ kín thể tích cố định, cấu hình tối ưu thỏa h bằng hai r, tức chiều cao bằng đường kính đáy. Đây là kết quả cấu trúc, không phụ thuộc con số hai trăm năm mươi pi đã chọn.",
            2.1,
        )
        self.play(FadeOut(card1),run_time=0.30)
        self.card("Kết luận","Tỷ lệ tối ưu không phụ thuộc thể tích cụ thể",[
            ("math","h = 2 r",33,GOLD),
            ("math","S_m = 150 pi",29,CYAN),
            ("text","Với V cố định: lon tối ưu có chiều cao = đường kính.",17,INK,BOLD),
        ],accent=GREEN)
        self.narrate("Với số liệu cụ thể, diện tích nhỏ nhất là một trăm năm mươi pi xăng ti mét vuông. Nhưng kết quả đáng nhớ hơn là tỷ lệ h bằng hai r: hình trụ kín tối ưu có chiều cao đúng bằng đường kính đáy.",1.2)
        self.takeaway("Tối ưu thực tế: ràng buộc thể tích trước, rồi mới tối thiểu hóa diện tích vật liệu.")

    # ======================================================
    # 8. SUMMARY + PITFALLS
    # ======================================================
    def summary(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ mô hình thực tế 3D","Năm vật thể — năm lỗi mô hình khác nhau","7/7")
        left=VGroup(
            VGroup(txt("1",16,GOLD,BOLD),txt("Bồn ghép",19,INK,BOLD),txt("→ không đếm mặt chung",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("2",16,GOLD,BOLD),txt("Silo",19,INK,BOLD),txt("→ thể tích khoang × mật độ",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("3",16,GOLD,BOLD),txt("Mái vòm",19,INK,BOLD),txt("→ mặt cong + hao hụt",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("4",16,GOLD,BOLD),txt("Ống rỗng",19,INK,BOLD),txt("→ vành khăn × chiều dài",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("5",16,GOLD,BOLD),txt("Thiết kế tối ưu",19,INK,BOLD),txt("→ ràng buộc rồi đạo hàm",18,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.31).shift(LEFT*2.70+UP*0.05)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Chốt","Ba câu hỏi trước mọi công thức",[
            ("text","1. Phần nào của vật thể thật sự được tính?",17,INK,BOLD),
            ("text","2. Đại lượng cần là thể tích, diện tích hay khối lượng?",17,INK,BOLD),
            ("text","3. Đơn vị cuối cùng có đúng bậc không?",17,INK,BOLD),
            ("sep",),
            ("math","V = frac(76 pi, 3)",27,CYAN),
            ("math","m = 63 pi",27,GREEN),
            ("math","h = 2 r",29,GOLD),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.7)
        self.narrate(
            "Năm bài hôm nay cố ý không giống nhau. Bồn chứa dạy cách loại bỏ mặt chung bên trong khối ghép. Silo dạy phân biệt sức chứa với khối lượng hàng hóa. Mái vòm dạy chọn đúng diện tích mặt cong, thêm hao hụt và làm tròn số tấm. Ống thép dạy mô hình vành khăn và cẩn thận với đường kính, bán kính, chiều dày. Lon tối ưu dạy rằng bài toán thực tế có thể đi từ hình học sang hàm số và đạo hàm một cách tự nhiên.",
            2.1,
        )
        self.narrate(
            "Nếu chỉ nhớ công thức, bài thực tế rất dễ sai ngay từ dòng đầu. Nếu mô hình đúng, phần tính thường ngắn. Vì vậy trước mọi phép tính hãy tự hỏi ba câu: phần nào thật sự được tính, đại lượng cần thuộc loại thể tích, diện tích hay khối lượng, và đơn vị cuối cùng có đúng bậc hay không. Video mười lăm sẽ tiếp tục chặng mô hình ba chiều nhưng chuyển sang các khối ghép và bài toán tham số khó hơn, nơi một kích thước thay đổi làm chi phí, sức chứa hoặc diện tích thay đổi theo.",
            2.0,
        )

    def construct(self):
        self.intro()
        self.modeling_workflow()
        self.tank()
        self.silo()
        self.dome()
        self.pipe()
        self.optimal_can()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_14_mo_hinh_thuc_te_3D_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst) SAFE")
    print("Render policy: fixed camera, low-resolution surfaces, no ambient rotation")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_14.wav"
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
