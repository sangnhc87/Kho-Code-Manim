from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time
import numpy as np

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
SMOKE_MEDIA_DIR = ROOT / "media_smoke"

BG = "#08111F"
PANEL = "#0C1A2D"
PANEL_2 = "#10233C"
INK = "#F3F7FF"
MUTED = "#8EA7C2"
GRID = "#284560"
BLUE = "#43C6F9"
CYAN = "#38E0CF"
GOLD = "#FFD84D"
GREEN = "#5CE58A"
RED = "#FF7373"
ORANGE = "#FF9B54"
PURPLE = "#B995FF"
EDGE = "#E7F0FF"
DIM = "#58718C"
FACE_COLORS = [BLUE, CYAN, PURPLE, ORANGE, GREEN, RED]

# ---------- typography ----------
def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)

_FORBIDDEN_TYPST_WORDS = {"sect", "intersect", "angle"}

def validate_typst_expr(s):
    words = set(s.replace("(", " ").replace(")", " ").replace(",", " ").replace(";", " ").split())
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(f"Forbidden Typst token(s) {bad} in {s!r}")
    if "/" in s:
        raise ValueError(f"Slash fraction forbidden in MathTypst: {s!r}")
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

# ---------- audio ----------
def _audio_key(text):
    payload = json.dumps({"text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC, "pitch": PITCH}, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]

def probe_duration(path: Path) -> float:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)], text=True).strip()
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
                "import asyncio\nimport edge_tts\n"
                f"text={text!r}\nout={str(out)!r}\nvoice={GIONG_DOC!r}\nrate={TOC_DO_DOC!r}\npitch={PITCH!r}\n"
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
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[m]", "-ar", "48000", "-ac", "2", "-t", f"{video_duration:.3f}", str(out_wav)], check=True)

def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)

# ---------- cube geometry ----------
SIDE = 2.8
H = SIDE / 2.0
RAW = {
    "A": np.array([-H, -H, -H]), "B": np.array([ H, -H, -H]),
    "C": np.array([ H,  H, -H]), "D": np.array([-H,  H, -H]),
    "A1": np.array([-H, -H, H]), "B1": np.array([ H, -H, H]),
    "C1": np.array([ H,  H, H]), "D1": np.array([-H,  H, H]),
}
FACES = {
    "front": ["A", "B", "B1", "A1"],
    "right": ["B", "C", "C1", "B1"],
    "back": ["D", "D1", "C1", "C"],
    "left": ["A", "A1", "D1", "D"],
    "bottom": ["A", "D", "C", "B"],
    "top": ["A1", "B1", "C1", "D1"],
}

WORLD_SCALE = 0.78
WORLD_SHIFT = np.array([-3.20, -0.18, 0.0])

def W(p):
    return WORLD_SCALE * np.array(p, dtype=float) + WORLD_SHIFT

def rotate_point_axis(p, axis_a, axis_b, angle):
    p = np.array(p, dtype=float); a = np.array(axis_a, dtype=float); b = np.array(axis_b, dtype=float)
    k = b - a
    nk = np.linalg.norm(k)
    if nk < 1e-12:
        raise ValueError("Zero-length rotation axis")
    k = k / nk
    x = p - a
    return a + x * math.cos(angle) + np.cross(k, x) * math.sin(angle) + k * np.dot(k, x) * (1.0 - math.cos(angle))

def shared_edge(f1, f2):
    common = [v for v in FACES[f1] if v in FACES[f2]]
    if len(common) != 2:
        raise ValueError(f"Faces {f1} and {f2} are not adjacent")
    return common

def face_normal(coords):
    q = np.array(coords)
    n = np.cross(q[1] - q[0], q[2] - q[1])
    n = n / np.linalg.norm(n)
    return n

def pairwise_distances(points):
    vals = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            vals.append(np.linalg.norm(np.array(points[i]) - np.array(points[j])))
    return np.array(vals)

def unfold_chain_numeric(chain):
    fc = {f: {v: RAW[v].copy() for v in FACES[f]} for f in chain}
    base = chain[0]
    base_coords = [fc[base][v] for v in FACES[base]]
    n0 = face_normal(base_coords)
    plane_p = base_coords[0].copy()
    steps = []
    for i in range(1, len(chain)):
        prev, cur = chain[i - 1], chain[i]
        edge = shared_edge(prev, cur)
        a = fc[cur][edge[0]].copy(); b = fc[cur][edge[1]].copy()
        prev_cent = np.mean([fc[prev][v] for v in FACES[prev]], axis=0)
        trials = []
        for sign in (1, -1):
            ang = sign * PI / 2
            test = {v: rotate_point_axis(fc[cur][v], a, b, ang) for v in FACES[cur]}
            dist = max(abs(np.dot(q - plane_p, n0)) for q in test.values())
            hv = b - a
            prev_side = np.dot(np.cross(hv, prev_cent - a), n0)
            cur_cent = np.mean(list(test.values()), axis=0)
            cur_side = np.dot(np.cross(hv, cur_cent - a), n0)
            overlap_penalty = 1 if prev_side * cur_side >= 0 else 0
            trials.append((round(dist, 12), overlap_penalty, sign))
        trials.sort(key=lambda z: (z[0] > 1e-8, z[1], z[0]))
        sign = trials[0][2]
        ang = sign * PI / 2
        for j in range(i, len(chain)):
            f = chain[j]
            for v in FACES[f]:
                fc[f][v] = rotate_point_axis(fc[f][v], a, b, ang)
        steps.append({"index": i, "edge": edge, "a": a, "b": b, "angle": ang})
    return fc, steps, n0, plane_p

def plane_basis(chain, fc, n0):
    f = chain[0]
    p0 = fc[f][FACES[f][0]].copy()
    e1 = fc[f][FACES[f][1]] - p0
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(n0, e1)
    e2 = e2 / np.linalg.norm(e2)
    return p0, e1, e2

def proj2(x, basis):
    p0, e1, e2 = basis
    d = np.array(x) - p0
    return np.array([np.dot(d, e1), np.dot(d, e2)])

def uv_point(face_coords, face, u, v):
    names = FACES[face]
    p0 = face_coords[face][names[0]]
    p1 = face_coords[face][names[1]]
    p3 = face_coords[face][names[3]]
    return p0 + u * (p1 - p0) + v * (p3 - p0)

def raw_uv(face, u, v):
    names = FACES[face]
    p0 = RAW[names[0]]; p1 = RAW[names[1]]; p3 = RAW[names[3]]
    return p0 + u * (p1 - p0) + v * (p3 - p0)

def point_from_spec(face_coords, spec):
    kind = spec[0]
    if kind == "vertex":
        return face_coords[spec[1]][spec[2]].copy()
    if kind == "uv":
        _, face, u, v = spec
        return uv_point(face_coords, face, u, v)
    raise ValueError(spec)

def raw_point_from_spec(spec):
    kind = spec[0]
    if kind == "vertex":
        return RAW[spec[2]].copy()
    if kind == "uv":
        _, face, u, v = spec
        return raw_uv(face, u, v)
    raise ValueError(spec)

def seg_inter(P, Q, A, B, tol=1e-9):
    P = np.array(P); Q = np.array(Q); A = np.array(A); B = np.array(B)
    v = Q - P; w = B - A
    M = np.array([[v[0], -w[0]], [v[1], -w[1]]], dtype=float)
    if abs(np.linalg.det(M)) < 1e-10:
        return None
    t, u = np.linalg.solve(M, A - P)
    if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
        return float(t), float(u), P + t * v
    return None

def path_data(chain, start_spec, end_spec):
    fc, steps, n0, plane_p = unfold_chain_numeric(chain)
    basis = plane_basis(chain, fc, n0)
    P3 = point_from_spec(fc, start_spec)
    Q3 = point_from_spec(fc, end_spec)
    P = proj2(P3, basis); Q = proj2(Q3, basis)
    hits = []
    for i in range(len(chain) - 1):
        edge = shared_edge(chain[i], chain[i + 1])
        A2 = proj2(fc[chain[i]][edge[0]], basis)
        B2 = proj2(fc[chain[i]][edge[1]], basis)
        h = seg_inter(P, Q, A2, B2)
        if h is None:
            raise AssertionError(f"Straight line misses hinge {edge}")
        t, u, X2 = h
        if not (1e-8 < t < 1 - 1e-8 and -1e-8 <= u <= 1 + 1e-8):
            raise AssertionError(f"Invalid hinge crossing t={t}, u={u}")
        raw_a = RAW[edge[0]]; raw_b = RAW[edge[1]]
        raw_x = raw_a + u * (raw_b - raw_a)
        hits.append({"faces": (chain[i], chain[i+1]), "edge": edge, "t": t, "u": u, "p2": X2, "raw": raw_x})
    if any(hits[i]["t"] >= hits[i+1]["t"] - 1e-9 for i in range(len(hits) - 1)):
        raise AssertionError("Hinge crossings are not in chain order")
    return {
        "fc": fc, "steps": steps, "basis": basis,
        "P2": P, "Q2": Q, "Praw": raw_point_from_spec(start_spec), "Qraw": raw_point_from_spec(end_spec),
        "hits": hits, "length": float(np.linalg.norm(Q - P)),
    }

def rigid_preflight_chain(chain):
    fc0 = {f: {v: RAW[v].copy() for v in FACES[f]} for f in chain}
    fc, steps, n0, plane_p = unfold_chain_numeric(chain)
    for f in chain:
        before = [fc0[f][v] for v in FACES[f]]
        after = [fc[f][v] for v in FACES[f]]
        if not np.allclose(pairwise_distances(before), pairwise_distances(after), atol=1e-9, rtol=0):
            raise AssertionError(f"Face {f} was distorted")
        if max(abs(np.dot(q - plane_p, n0)) for q in after) > 1e-8:
            raise AssertionError(f"Face {f} did not land on base plane")
    return True

# ---------- drawing ----------
def solid(a, b, color=EDGE, width=4.0, opacity=0.96):
    return Line(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=width, stroke_opacity=opacity)

def hidden_edge(a, b, color=DIM, width=2.5, opacity=0.62, dash=0.11):
    return DashedLine(np.array(a, dtype=float), np.array(b, dtype=float), color=color, stroke_width=width, stroke_opacity=opacity, dash_length=dash, dashed_ratio=0.56)

def face_poly(points, color=BLUE, opacity=0.12):
    return Polygon(*[np.array(p, dtype=float) for p in points], fill_color=color, fill_opacity=opacity, stroke_width=0)

def cube_shell(opacity=0.065):
    p = {k: W(v) for k, v in RAW.items()}
    faces = VGroup(
        face_poly([p[x] for x in FACES["front"]], PURPLE, opacity),
        face_poly([p[x] for x in FACES["right"]], CYAN, opacity * 1.15),
        face_poly([p[x] for x in FACES["top"]], BLUE, opacity * 1.05),
    )
    visible = [("A","B"),("B","C"),("A","A1"),("B","B1"),("C","C1"),("A1","B1"),("B1","C1"),("C1","D1"),("D1","A1")]
    hidden = [("C","D"),("D","A"),("D","D1")]
    edges = VGroup(*[solid(p[a], p[b], EDGE, 3.7) for a,b in visible])
    hid = VGroup(*[hidden_edge(p[a], p[b]) for a,b in hidden])
    return VGroup(faces, edges, hid)

def strip_face_mob(face_name, color, extra_dot=None):
    pts = [W(RAW[v]) for v in FACES[face_name]]
    poly = face_poly(pts, color, 0.16)
    border = VGroup(*[solid(pts[i], pts[(i+1)%4], color, 3.3) for i in range(4)])
    g = VGroup(poly, border)
    if extra_dot is not None:
        g.add(extra_dot)
    return g

def start_end_dots(start_spec, end_spec):
    P = W(raw_point_from_spec(start_spec)); Q = W(raw_point_from_spec(end_spec))
    return Dot3D(P, radius=0.075, color=GREEN), Dot3D(Q, radius=0.075, color=RED)

def make_strip_mobs(chain, start_spec, end_spec):
    mobs = []
    sd, ed = start_end_dots(start_spec, end_spec)
    for i, f in enumerate(chain):
        extra = None
        if i == 0:
            extra = sd
        if i == len(chain)-1:
            extra = ed if extra is None else VGroup(extra, ed)
        mobs.append(strip_face_mob(f, FACE_COLORS[i % len(FACE_COLORS)], extra))
    return mobs

def unfold_animations(scene, chain, face_mobs, run_each=1.35):
    _, steps, _, _ = unfold_chain_numeric(chain)
    for step in steps:
        i = step["index"]
        downstream = VGroup(*face_mobs[i:])
        a = W(step["a"]); b = W(step["b"])
        scene.play(Rotate(downstream, angle=step["angle"], axis=b-a, about_point=a), run_time=run_each, rate_func=smooth)

def folded_path_segments(chain, start_spec, end_spec, color=GOLD, width=6.8):
    d = path_data(chain, start_spec, end_spec)
    pts = [d["Praw"]] + [h["raw"] for h in d["hits"]] + [d["Qraw"]]
    return VGroup(*[solid(W(pts[i]), W(pts[i+1]), color, width) for i in range(len(pts)-1)]), pts, d

def net_group(chain, start_spec, end_spec, width=6.4, height=4.9, center=np.array([-3.15,-0.15,0.0]), show_path=True):
    d = path_data(chain, start_spec, end_spec)
    fc = d["fc"]; basis = d["basis"]
    face2 = {}
    all2 = []
    for f in chain:
        arr = [proj2(fc[f][v], basis) for v in FACES[f]]
        face2[f] = arr; all2 += arr
    all2 = np.array(all2)
    minx,miny = all2.min(axis=0); maxx,maxy = all2.max(axis=0)
    sx = width / max(maxx-minx, 1e-8); sy = height / max(maxy-miny, 1e-8)
    scale = min(sx,sy)
    mid = np.array([(minx+maxx)/2,(miny+maxy)/2])
    def T(p):
        q = (np.array(p)-mid)*scale
        return np.array([q[0]+center[0], q[1]+center[1], 0.0])
    grp = VGroup()
    for i,f in enumerate(chain):
        pts=[T(q) for q in face2[f]]
        poly=Polygon(*pts, fill_color=FACE_COLORS[i%len(FACE_COLORS)], fill_opacity=0.16, stroke_color=FACE_COLORS[i%len(FACE_COLORS)], stroke_width=2.6)
        grp.add(poly)
    P=T(d["P2"]); Q=T(d["Q2"])
    grp.add(Dot(P, radius=0.075, color=GREEN), Dot(Q, radius=0.075, color=RED))
    if show_path:
        grp.add(Line(P,Q,color=GOLD,stroke_width=6.5))
        for h in d["hits"]:
            grp.add(Dot(T(h["p2"]), radius=0.055, color=GOLD))
    return grp, d, T

# ---------- 2-column layout ----------
def divider():
    return Line(np.array([0.45,-3.50,0]), np.array([0.45,3.18,0]), color=GRID, stroke_width=1.25)

def header_group(kicker, title, subtitle, progress=""):
    k = txt(kicker, 16, GOLD, BOLD).to_corner(UL, buff=0.25)
    t = fit_width(txt(title, 29, INK, BOLD), 9.7).next_to(k, DOWN, aligned_edge=LEFT, buff=0.06)
    s = fit_width(txt(subtitle, 17, MUTED), 9.7).next_to(t, DOWN, aligned_edge=LEFT, buff=0.05)
    items=[k,t,s]
    if progress:
        items.append(txt(progress,16,MUTED,BOLD).to_corner(UR,buff=0.27))
    rule=Line(LEFT*6.7,RIGHT*6.7,color=GRID,stroke_width=1.0).to_edge(UP,buff=1.10)
    items += [rule, divider()]
    return VGroup(*items)

def footer_group():
    a=txt(TEN_THAY,15,MUTED).to_corner(DL,buff=0.22)
    b=txt("SERIES TRẢI PHẲNG · GEODESIC TRÊN ĐA DIỆN",15,MUTED).to_corner(DR,buff=0.22)
    return VGroup(a,b)

def right_panel(title, items, accent=GOLD, y=-0.05):
    bg=RoundedRectangle(width=5.55,height=5.62,corner_radius=0.12,fill_color=PANEL,fill_opacity=0.95,stroke_color=GRID,stroke_width=1.0,stroke_opacity=0.65)
    bg.move_to(np.array([3.62,y,0]))
    bar=Line(bg.get_corner(UL)+RIGHT*0.20+DOWN*0.12,bg.get_corner(DL)+RIGHT*0.20+UP*0.12,color=accent,stroke_width=4.0)
    tt=fit_width(txt(title,23,accent,BOLD),4.65).move_to(bg.get_top()+DOWN*0.36).align_to(bg,LEFT).shift(RIGHT*0.48)
    body=VGroup()
    for it in items:
        if it[0]=="text":
            _,s,size,color=it; m=txt(s,size,color)
        elif it[0]=="math":
            _,s,size,color=it; m=mty(s,size,color)
        elif it[0]=="gap":
            m=VMobject(); m.set_height(0.08)
        else:
            raise ValueError(it)
        body.add(m)
    body.arrange(DOWN,aligned_edge=LEFT,buff=0.18)
    fit_width(body,4.62)
    body.next_to(tt,DOWN,aligned_edge=LEFT,buff=0.25)
    if body.height > 4.55:
        body.scale_to_fit_height(4.55); body.next_to(tt,DOWN,aligned_edge=LEFT,buff=0.20)
    return VGroup(bg,bar,tt,body)

def intro_right(video_no, title_lines, subtitle_lines):
    bg=RoundedRectangle(width=5.55,height=5.35,corner_radius=0.15,fill_color=PANEL,fill_opacity=0.94,stroke_color=GRID,stroke_width=1.1)
    bg.move_to(RIGHT*3.60+DOWN*0.05)
    no=txt(f"TRẢI PHẲNG {video_no:02d}",25,GOLD,BOLD)
    titles=VGroup(*[fit_width(txt(s,32,INK,BOLD),4.65) for s in title_lines]).arrange(DOWN,aligned_edge=LEFT,buff=0.08)
    subs=VGroup(*[fit_width(txt(s,18,CYAN),4.65) for s in subtitle_lines]).arrange(DOWN,aligned_edge=LEFT,buff=0.07)
    allg=VGroup(no,titles,subs).arrange(DOWN,aligned_edge=LEFT,buff=0.25)
    allg.move_to(bg.get_center()).align_to(bg,LEFT).shift(RIGHT*0.46)
    return VGroup(bg,allg)

class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
    def narrate(self,text,min_visual_time=1.0):
        audio=create_audio(text); dur=probe_duration(audio); self.audio_events.append((self.time,audio)); self.wait(max(dur,min_visual_time)); return dur
    def narrate_play(self,text,*anims,min_time=1.0,rate_func=smooth):
        audio=create_audio(text); dur=probe_duration(audio); self.audio_events.append((self.time,audio)); self.play(*anims,run_time=max(dur,min_time),rate_func=rate_func); return dur
    def add_hud(self,kicker,title,subtitle,progress):
        h=header_group(kicker,title,subtitle,progress); f=footer_group(); self.add_fixed_in_frame_mobjects(h,f); return VGroup(h,f)
    def clear_all(self,run_time=0.28):
        mobs=list(self.mobjects)
        if mobs: self.play(*[FadeOut(m) for m in mobs],run_time=run_time)
        self.clear()

# ==========================================================
# VIDEO 02 REBUILT — CUBE II: 4, 5, 6 FACES
# ==========================================================
CHAIN4=["front","right","back","left"]
S4=("uv","front",0.5,0.5)
E4=("uv","left",0.5,0.5)

CHAIN5=["front","top","right","back","bottom"]
S5=("uv","front",0.25,0.75)
E5=("uv","bottom",0.75,0.25)

CHAIN6=["front","right","back","bottom","left","top"]
S6=("uv","front",0.5,0.5)
E6=("uv","top",0.5,0.5)

def geometry_preflight(verbose=True):
    cases=[(CHAIN4,S4,E4,3.0),(CHAIN5,S5,E5,2.0*math.sqrt(2)),(CHAIN6,S6,E6,math.sqrt(17))]
    for chain,S,E,coef in cases:
        rigid_preflight_chain(chain); d=path_data(chain,S,E)
        if abs(d["length"]-coef*SIDE)>1e-8: raise AssertionError((chain,d["length"],coef*SIDE))
        if len(d["hits"]) != len(chain)-1: raise AssertionError("Wrong hinge count")
        if any(not (1e-7<h["t"]<1-1e-7 and 1e-7<h["u"]<1-1e-7) for h in d["hits"]): raise AssertionError("A hinge is only touched at an endpoint")
    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  4 faces: L = 3a")
        print("  5 faces: L = 2a*sqrt(2)")
        print("  6 faces: L = a*sqrt(17)")
        print("  all required hinges crossed strictly inside and in order")
    return True

class TraiPhang02Rebuilt(BaseLesson):
    def intro(self):
        self.clear_all(); self.set_camera_orientation(phi=66*DEGREES,theta=-48*DEGREES,zoom=0.92)
        self.add(cube_shell(0.08))
        panel=intro_right(2,["LẬP PHƯƠNG II","KIẾN ĐI QUA 4 · 5 · 6 MẶT"],["Bài toán có ràng buộc tuyến mặt.","Mở cả dải mặt như một tấm giấy."])
        self.add_fixed_in_frame_mobjects(panel,divider(),footer_group()); self.play(FadeIn(panel),run_time=0.7)
        self.narrate("Video hai tiếp tục đúng một mô hình là lập phương, nhưng nâng độ khó lên đường đi qua bốn, năm và sáu mặt. Có một lưu ý toán học phải nói rõ ngay: nếu kiến được đi tự do giữa hai điểm trên lập phương, nó thường không tự nguyện vòng qua quá nhiều mặt. Vì vậy các bài trong video này cho thêm ràng buộc: kiến phải đi qua một dải mặt hoặc các cổng theo thứ tự đã chỉ định.",2.0)
        self.narrate("Khi thứ tự mặt đã cố định, bài toán vẫn có một cấu trúc rất đẹp. Ta cắt các cạnh không cần thiết, mở cả dải mặt bằng các phép quay cứng nối tiếp, rồi tìm đoạn thẳng ngắn nhất trong bản trải. Điều khó nhất không phải căn thức, mà là kiểm tra đoạn thẳng đó có cắt đủ mọi cạnh bản lề theo đúng thứ tự hay không.",1.9)

    def honesty(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Ràng buộc tuyến mặt là gì?","Không được gọi một đường vòng 6 mặt là tối ưu nếu đề không bắt buộc","01 / 17")
        self.add(cube_shell())
        panel=right_panel("QUY ƯỚC BÀI TOÁN",[("text","Đề cho thứ tự các mặt phải đi qua.",20,INK),("text","Hoặc cho các cổng bắt buộc trên cạnh.",20,INK),("text","Ta tìm đường ngắn nhất trong đúng lớp đường đó.",19,CYAN),("gap",),("text","Không đánh tráo với cực tiểu toàn cục không ràng buộc.",18,RED)],RED)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Đây là điểm mình muốn làm thật chuẩn. Nếu P và Q nằm trên hai mặt kề nhau mà ta cố cho kiến vòng bốn hay sáu mặt rồi gọi đó là đường ngắn nhất, kết luận sẽ sai. Vì thế từ đây, mỗi bài đều ghi rõ tuyến mặt bắt buộc. Ta đang tối ưu trong lớp đường đi thỏa ràng buộc ấy.",1.8)

    def method(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Thuật toán dải mặt","Mỗi lần mở: quay toàn bộ phần dải phía sau quanh cạnh bản lề","02 / 17")
        self.add(cube_shell())
        panel=right_panel("ENGINE HÌNH HỌC",[("text","1. Chuỗi mặt F₁ → F₂ → ... → Fₖ",20,INK),("text","2. Tìm cạnh chung liên tiếp.",20,INK),("text","3. Quay cả phần dải phía sau 90°.",20,INK),("text","4. Lặp đến khi toàn dải đồng phẳng.",20,INK),("text","5. Nối P,Q và kiểm tra từng bản lề.",20,CYAN)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Engine mới không mở từng mặt độc lập. Sau khi mặt thứ hai đã được mở, muốn mở mặt thứ ba thì phải quay mặt thứ ba cùng toàn bộ phần dải còn treo phía sau quanh cạnh chung hiện tại. Nhờ vậy mọi khớp nối được bảo toàn như một dải giấy thật. Cách này quan trọng khi chuỗi có bốn, năm hoặc sáu mặt.",1.9)

    def case4_3d(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 02","Bài 1 · Đi qua 4 mặt","Mặt trước → phải → sau → trái","03 / 17")
        self.add(cube_shell())
        path,pts,d=folded_path_segments(CHAIN4,S4,E4,ORANGE,5.8); self.add(path)
        self.add(Dot3D(W(pts[0]),radius=0.08,color=GREEN),Dot3D(W(pts[-1]),radius=0.08,color=RED))
        panel=right_panel("RÀNG BUỘC",[("text","P: tâm mặt trước.",20,GREEN),("text","Q: tâm mặt trái.",20,RED),("text","Phải lần lượt qua 4 mặt bên.",20,INK),("gap",),("text","Tức phải cắt 3 cạnh bản lề.",19,MUTED)],ORANGE)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Bài bốn mặt: P là tâm mặt trước, Q là tâm mặt trái, nhưng kiến bị yêu cầu đi quanh dải bốn mặt bên theo thứ tự trước, phải, sau, trái. Như vậy đường phải cắt ba cạnh đứng B B phẩy, C C phẩy và D D phẩy theo đúng thứ tự.",1.7)

    def unfold_case(self,chain,S,E,title,subtitle,progress,panel_items,after_text):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.94)
        self.add_hud("TRẢI PHẲNG · 02",title,subtitle,progress)
        mobs=make_strip_mobs(chain,S,E); self.add(*mobs)
        panel=right_panel("MỞ DẢI MẶT",panel_items,CYAN); self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Ta tách đúng dải mặt cần dùng. Mặt đầu giữ cố định. Ở mỗi bước, cạnh chung hiện tại là trục quay; toàn bộ phần dải còn lại quay cùng nhau. Đây là khác biệt giữa một phép trải hình học thật và việc biến hình từng mặt về một vị trí 2D bằng mắt.",1.6)
        unfold_animations(self,chain,mobs,run_each=1.1)
        self.narrate(after_text,1.4)

    def case4_net(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Bản trải 4 mặt","Bốn hình vuông thành một dải thẳng","05 / 17")
        net,d,T=net_group(CHAIN4,S4,E4); self.add_fixed_in_frame_mobjects(net)
        panel=right_panel("ĐỘ DÀI",[("text","P,Q là tâm ô đầu và ô cuối.",20,INK),("text","Độ lệch theo dải: 3a.",20,INK),("math","L_4 = 3 a",42,GOLD),("gap",),("text","Đường thẳng cắt cả 3 bản lề tại trung điểm.",18,CYAN)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Bản trải là bốn hình vuông nối thành một dải. P và Q là tâm ô đầu và ô cuối, nằm trên cùng một đường ngang. Khoảng cách giữa hai tâm là ba a. Đường thẳng đi qua trung điểm của cả ba cạnh bản lề, nên khi gấp lại nó thực sự sử dụng đủ bốn mặt.",1.8)

    def case5_setup(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 02","Bài 2 · Đi qua 5 mặt","Trước → trên → phải → sau → đáy","07 / 17")
        self.add(cube_shell())
        path,pts,d=folded_path_segments(CHAIN5,S5,E5,ORANGE,5.8); self.add(path)
        panel=right_panel("ĐIỂM P, Q",[("text","P ở mặt trước: 1/4 theo ngang, 3/4 theo cao.",18,GREEN),("text","Q ở đáy: 3/4 theo sâu, 1/4 theo ngang.",18,RED),("gap",),("text","Tuyến mặt được chỉ định trước.",19,CYAN)],ORANGE)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Bài năm mặt cần hai điểm không đối xứng để bản trải không biến thành một ví dụ quá đơn giản. P nằm trong mặt trước tại vị trí một phần tư theo chiều ngang và ba phần tư theo chiều cao. Q nằm trong đáy tại vị trí tương ứng ba phần tư theo chiều sâu và một phần tư theo chiều ngang. Kiến phải đi theo chuỗi trước, trên, phải, sau, đáy.",1.9)

    def case5_net(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Bản trải 5 mặt","Đường thẳng phải cắt đủ 4 bản lề","09 / 17")
        net,d,T=net_group(CHAIN5,S5,E5); self.add_fixed_in_frame_mobjects(net)
        panel=right_panel("TỌA ĐỘ TRÊN BẢN TRẢI",[("text","Sau khi chuẩn hóa theo cạnh a:",19,MUTED),("math","Delta x = 2 a",30,CYAN),("math","Delta y = 2 a",30,CYAN),("math","L_5 = 2 a sqrt(2)",39,GOLD),("gap",),("text","4 giao điểm đều nằm trong cạnh bản lề.",18,GREEN)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Sau bốn phép mở liên tiếp, năm mặt tạo thành một polyomino phẳng. Hai ảnh P và Q có độ lệch ngang hai a và độ lệch dọc hai a. Vì vậy đường thẳng giữa chúng dài hai a căn hai.",1.5)
        self.narrate("Điều quan trọng hơn công thức là bài kiểm tra hợp lệ: đoạn P Q phải cắt đủ bốn cạnh chung, theo đúng thứ tự, và mỗi giao điểm phải nằm bên trong đoạn cạnh chứ không rơi ra phần kéo dài. Geometry preflight kiểm tra trực tiếp bốn điều này.",1.8)

    def case6_setup(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.96)
        self.add_hud("TRẢI PHẲNG · 02","Bài 3 · Đi qua cả 6 mặt","Trước → phải → sau → đáy → trái → trên","11 / 17")
        self.add(cube_shell())
        path,pts,d=folded_path_segments(CHAIN6,S6,E6,ORANGE,5.4); self.add(path)
        panel=right_panel("HAMILTON TRÊN ĐỒ THỊ MẶT",[("text","Mỗi mặt xuất hiện đúng một lần.",20,INK),("text","5 cạnh bản lề liên tiếp.",20,INK),("text","P: tâm mặt trước.",20,GREEN),("text","Q: tâm mặt trên.",20,RED),("gap",),("text","Tuyến mặt bắt buộc, không phải cực tiểu tự do.",18,MUTED)],PURPLE)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Bài sáu mặt là bài tổng hợp: chuỗi trước, phải, sau, đáy, trái, trên đi qua toàn bộ sáu mặt, mỗi mặt đúng một lần. Trong ngôn ngữ đồ thị, đây là một đường Hamilton trên đồ thị các mặt của lập phương. P là tâm mặt trước, Q là tâm mặt trên, và tuyến mặt này là ràng buộc bắt buộc.",1.9)

    def case6_unfold(self):
        self.unfold_case(CHAIN6,S6,E6,"Mở dải 6 mặt","Năm phép quay cứng nối tiếp","12 / 17",[("text","5 cạnh bản lề.",20,GOLD),("text","Ở bước i, quay toàn bộ các mặt i...6.",19,INK),("text","Không mặt nào bị co giãn.",19,MUTED)],"Sau năm lần mở, cả sáu hình vuông nằm phẳng nhưng không nhất thiết tạo thành một dải thẳng. Hình dạng bản trải xuất hiện hoàn toàn từ cấu trúc bản lề, không phải do ta sắp xếp thủ công.")

    def case6_net(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Bản trải 6 mặt","Đoạn thẳng xuyên qua đủ 5 cạnh chung","13 / 17")
        net,d,T=net_group(CHAIN6,S6,E6); self.add_fixed_in_frame_mobjects(net)
        panel=right_panel("KẾT QUẢ 6 MẶT",[("math","Delta x = 4 a",30,CYAN),("math","Delta y = a",30,CYAN),("math","L_6 = a sqrt(17)",40,GOLD),("gap",),("text","5 giao điểm xuất hiện đúng thứ tự.",18,GREEN)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Trong hệ trục của bản trải, hai tâm P và Q lệch nhau bốn a theo một phương và a theo phương vuông góc. Bởi Pythagore, L sáu bằng a căn mười bảy. Đoạn thẳng cắt năm cạnh bản lề theo đúng thứ tự, nên nó tương ứng với một đường liên tục đi qua toàn bộ sáu mặt đã quy định.",1.9)

    def walk_case(self, chain, S, E, title, subtitle, progress, result_math):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.96)
        self.add_hud("TRẢI PHẲNG · 02",title,subtitle,progress)
        self.add(cube_shell())
        path,pts,d=folded_path_segments(chain,S,E,GOLD,6.0); self.add(path)
        ant=Dot3D(W(pts[0]),radius=0.09,color=GREEN); self.add(ant)
        panel=right_panel("KIỂM CHỨNG SAU KHI GẤP",[("text",f"Số đoạn trên mặt: {len(pts)-1}",20,INK),("text",f"Số cạnh bản lề: {len(pts)-2}",20,INK),("math",result_math,36,GOLD),("gap",),("text","Mỗi đoạn nằm trên đúng một mặt của tuyến.",18,GREEN)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        for i in range(len(pts)-1):
            face_name=chain[i]
            self.narrate_play(f"Đoạn {i+1} nằm trên mặt {face_name}. Kiến đi tới {'đích Q' if i==len(pts)-2 else 'cạnh bản lề tiếp theo'}.",MoveAlongPath(ant,Line(W(pts[i]),W(pts[i+1]))),min_time=1.35,rate_func=linear)
        self.narrate("Sau khi kiến chạy hết tuyến, ta đã kiểm chứng trực tiếp rằng đoạn thẳng trên bản trải không hề nhảy mặt, không xuyên qua khối và không bỏ qua bản lề bắt buộc. Đây là bước mình sẽ giữ cho mọi ví dụ nhiều mặt trong series.",1.6)

    def compare(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Không so sánh 3a, 2a√2, a√17 như ba đối thủ","Mỗi giá trị thuộc một bài có ràng buộc khác nhau","15 / 17")
        panel=right_panel("ĐỪNG ĐÁNH TRÁO BÀI TOÁN",[("math","L_4 = 3 a",34,ORANGE),("math","L_5 = 2 a sqrt(2)",34,CYAN),("math","L_6 = a sqrt(17)",34,GOLD),("gap",),("text","Ba tuyến mặt khác nhau → ba miền khả thi khác nhau.",18,RED)],RED)
        self.add_fixed_in_frame_mobjects(panel)
        table=VGroup(
            VGroup(txt("4 mặt",22,ORANGE,BOLD),txt("3 bản lề",20,INK),txt("dải thẳng",20,MUTED)).arrange(RIGHT,buff=0.4),
            VGroup(txt("5 mặt",22,CYAN,BOLD),txt("4 bản lề",20,INK),txt("polyomino",20,MUTED)).arrange(RIGHT,buff=0.4),
            VGroup(txt("6 mặt",22,GOLD,BOLD),txt("5 bản lề",20,INK),txt("toàn bộ khối",20,MUTED)).arrange(RIGHT,buff=0.4),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.48).move_to(LEFT*3.0+UP*0.25)
        self.add_fixed_in_frame_mobjects(table)
        self.narrate("Ba con số không được đem so như ba phương án của cùng một bài. Mỗi bài có điểm đầu, điểm cuối và tuyến mặt bắt buộc khác nhau. Mục tiêu của video là học cách xử lý một dải mặt dài, không phải chứng minh rằng đi nhiều mặt hơn luôn dài hơn hay ngắn hơn.",1.8)

    def validity(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Bộ kiểm tra một ứng viên","Đoạn thẳng đẹp trên bản trải vẫn có thể vô hiệu","16 / 17")
        checks=VGroup(
            txt("1 · Các mặt liên tiếp có thật sự kề nhau?",21,INK),
            txt("2 · Phép mở có giữ nguyên mọi cạnh và góc?",21,INK),
            txt("3 · Đoạn thẳng có cắt từng cạnh bản lề?",21,INK),
            txt("4 · Các giao điểm có nằm trong đoạn cạnh?",21,INK),
            txt("5 · Thứ tự giao điểm có đúng tuyến mặt?",21,INK),
            txt("6 · Gấp lại: mỗi đoạn có nằm trên đúng mặt?",21,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.32).move_to(LEFT*2.9+DOWN*0.05)
        self.add_fixed_in_frame_mobjects(checks)
        panel=right_panel("GEOMETRY PREFLIGHT",[("text","Sai 1 kiểm tra → workflow fail.",20,RED),("text","Không render 1080p khi hình học chưa qua.",20,INK),("gap",),("text","Đây là lớp bảo vệ quan trọng nhất của series.",19,GREEN)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Một đoạn nối P Q có thể nhìn rất đẹp trên bản trải nhưng vẫn không đại diện cho tuyến mặt đã chọn, chẳng hạn nó bỏ qua một cạnh bản lề hoặc cắt phần kéo dài của cạnh thay vì chính đoạn cạnh. Vì vậy engine kiểm tra sáu điều trước khi render. Sai bất kỳ điều nào, GitHub Actions dừng ngay.",1.9)

    def summary(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 02","Tổng kết Lập phương I–II","Từ 2 mặt đến 6 mặt bằng cùng một ngôn ngữ","17 / 17")
        left=VGroup(
            txt("2 mặt · một bản lề",21,CYAN,BOLD),
            txt("3 mặt · hai bản lề",21,CYAN,BOLD),
            txt("4 mặt · ba bản lề",21,CYAN,BOLD),
            txt("5 mặt · bốn bản lề",21,CYAN,BOLD),
            txt("6 mặt · năm bản lề",21,CYAN,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34).move_to(LEFT*3.05+UP*0.20)
        self.add_fixed_in_frame_mobjects(left)
        panel=right_panel("MỘT NGUYÊN LÝ",[("text","Chọn chuỗi mặt.",20,INK),("text","Mở cứng quanh cạnh chung.",20,INK),("text","Nối thẳng hai ảnh.",20,INK),("text","Kiểm tra toàn bộ bản lề.",20,INK),("text","Gấp lại để xác nhận.",20,GREEN)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Hai video đầu bây giờ tạo thành một khối kiến thức hoàn chỉnh. Video một xử lý đường tự nhiên qua hai và ba mặt. Video hai xử lý dải mặt dài từ bốn tới sáu mặt với ràng buộc tuyến. Cùng một engine hình học dùng cho tất cả: chuỗi mặt, cạnh bản lề, phép quay cứng, đoạn thẳng trên bản trải và kiểm tra gấp lại.",1.8)
        self.narrate("Từ video ba, ta chuyển sang hộp chữ nhật và các điểm không còn ở vị trí đối xứng. Khi đó không chỉ phải chọn chuỗi mặt, mà còn phải biến đổi chính xác tọa độ của điểm nằm trên cạnh hoặc trong mặt, rồi so sánh nhiều ứng viên thật sự cạnh tranh với nhau.",1.6)
        badge=txt("VIDEO 03 · HỘP CHỮ NHẬT — HAI ĐIỂM TRÊN CẠNH",18,CYAN,BOLD).to_edge(DOWN,buff=0.58)
        self.add_fixed_in_frame_mobjects(badge); self.play(FadeIn(badge),run_time=0.45)

    def construct(self):
        self.intro(); self.honesty(); self.method(); self.case4_3d();
        self.unfold_case(CHAIN4,S4,E4,"Mở dải 4 mặt","Ba phép quay nối tiếp","04 / 17",[("text","3 bản lề đứng.",20,GOLD),("text","Mở cả phần dải phía sau mỗi lần.",19,INK)],"Bốn mặt bên trở thành một dải bốn hình vuông thẳng hàng.")
        self.case4_net(); self.walk_case(CHAIN4,S4,E4,"Gấp lại tuyến 4 mặt","P → 3 bản lề → Q","06 / 17","L_4 = 3 a"); self.case5_setup();
        self.unfold_case(CHAIN5,S5,E5,"Mở dải 5 mặt","Bốn phép quay, hình net không còn là dải thẳng","08 / 17",[("text","4 cạnh bản lề khác hướng nhau.",19,GOLD),("text","Phải dùng phép biến đổi tích lũy.",19,INK)],"Sau bốn bước, năm mặt cùng nằm trong một mặt phẳng. Vị trí của P và Q cũng được biến đổi bằng đúng các phép quay của mặt chứa chúng.")
        self.case5_net(); self.walk_case(CHAIN5,S5,E5,"Gấp lại tuyến 5 mặt","P → 4 bản lề → Q","10 / 17","L_5 = 2 a sqrt(2)"); self.case6_setup(); self.case6_unfold(); self.case6_net(); self.walk_case(CHAIN6,S6,E6,"Gấp lại tuyến 6 mặt","Đi qua toàn bộ sáu mặt đúng một lần","14 / 17","L_6 = a sqrt(17)"); self.compare(); self.validity(); self.summary()

class Smoke02(ThreeDScene):
    def construct(self):
        geometry_preflight(False); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.92)
        for chain,S,E in [(CHAIN4,S4,E4),(CHAIN5,S5,E5),(CHAIN6,S6,E6)]:
            self.clear(); mobs=make_strip_mobs(chain,S,E); self.add(*mobs); unfold_animations(self,chain,mobs,run_each=0.28); self.wait(0.08)

def render_smoke():
    geometry_preflight(True); config.pixel_width=854; config.pixel_height=480; config.frame_rate=15; config.media_dir=str(SMOKE_MEDIA_DIR); config.output_file="trai_phang_02_rebuilt_smoke"; config.disable_caching=True
    scene=Smoke02(); scene.render(); path=Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists(): raise RuntimeError(path)
    return path

def render_full():
    geometry_preflight(True); config.pixel_width=FINAL_WIDTH; config.pixel_height=FINAL_HEIGHT; config.frame_rate=FINAL_FPS; config.media_dir=str(MEDIA_DIR); config.output_file="trai_phang_02_lap_phuong_4_5_6_mat_REBUILT_1080p"; config.disable_caching=False
    scene=TraiPhang02Rebuilt(); scene.render(); video=Path(scene.renderer.file_writer.movie_file_path)
    if not video.exists(): raise RuntimeError(video)
    master=ROOT/"master_narration_trai_phang_02_rebuilt.wav"; build_master_audio(scene.audio_events,probe_duration(video),master)
    final=video.with_name(video.stem+"_WITH_AUDIO.mp4"); mux_audio(video,master,final); validate_audio(master); print("FINAL:",final); return final

if __name__=="__main__":
    if "--geometry-preflight" in sys.argv: geometry_preflight(True); raise SystemExit(0)
    if "--smoke-render" in sys.argv: render_smoke(); raise SystemExit(0)
    render_full()
