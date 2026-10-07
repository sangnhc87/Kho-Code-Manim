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
# VIDEO 01 REBUILT — CUBE I: 2 FACES AND 3 FACES
# ==========================================================
CHAIN2=["bottom","right"]
S2=("vertex","bottom","A")
E2=("vertex","right","C1")
CHAIN3=["front","right","back"]
S3=("uv","front",0.5,0.5)
E3=("uv","back",0.5,0.5)

def geometry_preflight(verbose=True):
    rigid_preflight_chain(CHAIN2); rigid_preflight_chain(CHAIN3)
    d2=path_data(CHAIN2,S2,E2)
    d3=path_data(CHAIN3,S3,E3)
    a=SIDE
    if abs(d2["length"]-a*math.sqrt(5))>1e-8: raise AssertionError("2-face length wrong")
    if len(d2["hits"])!=1 or abs(d2["hits"][0]["u"]-0.5)>1e-8: raise AssertionError("2-face hinge midpoint wrong")
    if abs(d3["length"]-2*a)>1e-8: raise AssertionError("3-face length wrong")
    if len(d3["hits"])!=2 or any(abs(h["u"]-0.5)>1e-8 for h in d3["hits"]): raise AssertionError("3-face hinge crossings wrong")
    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  2 faces: L = a*sqrt(5), hinge midpoint verified")
        print("  3 faces: opposite-face centers, L = 2a")
        print("  rigid unfolding + coplanarity + ordered hinge crossings verified")
    return True

class TraiPhang01Rebuilt(BaseLesson):
    def intro(self):
        self.clear_all(); self.set_camera_orientation(phi=66*DEGREES,theta=-48*DEGREES,zoom=0.92)
        self.add(cube_shell(0.08))
        P=Dot3D(W(RAW["A"]),radius=0.08,color=GREEN); Q=Dot3D(W(RAW["C1"]),radius=0.08,color=RED); self.add(P,Q)
        panel=intro_right(1,["LẬP PHƯƠNG I","KIẾN ĐI QUA 2 · 3 MẶT"],["Mỗi phép trải là một phép quay cứng.","Hình bên trái · lập luận bên phải."])
        self.add_fixed_in_frame_mobjects(panel,divider(),footer_group())
        self.play(FadeIn(panel),run_time=0.7)
        self.narrate("Mình làm lại series từ đầu với một nguyên tắc thị giác mới. Hình học luôn nằm ở cột trái; đề bài, lập luận và công thức nằm ở cột phải, không còn chữ đè lên mô hình. Video đầu tiên chỉ dùng một mô hình là lập phương, nhưng đi thật kỹ hai tình huống nền tảng: đường kiến qua đúng hai mặt và đường kiến qua đúng ba mặt.",2.0)
        self.narrate("Mọi thao tác mở mặt trong video đều là phép quay cứng quanh đúng cạnh bản lề. Điểm nằm trên mặt phải đi cùng mặt, cạnh bản lề phải đứng yên, và sau khi gấp lại đường vàng phải trở thành đúng đường đi trên bề mặt. Nếu một trong các điều đó sai, workflow sẽ dừng trước khi render dài.",1.8)

    def principle(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Nguyên lý cốt lõi","Đường gấp trên đa diện ↔ đoạn thẳng trên bản trải","01 / 12")
        self.add(cube_shell())
        panel=right_panel("BA BƯỚC",[("text","1. Chọn chuỗi mặt hợp lệ.",21,INK),("text","2. Mở từng mặt quanh cạnh chung.",21,INK),("text","3. Nối thẳng hai ảnh và kiểm tra gấp lại.",21,INK),("gap",),("math","L_s = L_n",34,GOLD)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Một đường đi trên đa diện thường là nhiều đoạn thẳng nằm trên nhiều mặt khác nhau. Khi các mặt được mở đúng, những đoạn ấy có thể nằm trên cùng một đường thẳng. Đây là lý do trải phẳng mạnh: bài toán ba chiều được đưa về khoảng cách phẳng mà không làm thay đổi độ dài.",1.7)
        self.narrate("Nhưng chỉ có thể dùng kết quả nếu đoạn thẳng trên bản trải thực sự cắt các cạnh bản lề theo đúng thứ tự và tại các điểm nằm trên chính những cạnh đó. Vì vậy từ series này trở đi, mỗi ví dụ đều có geometry preflight kiểm tra điều kiện hợp lệ chứ không chỉ kiểm tra công thức cuối.",1.7)

    def case2_setup(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Bài 1 · Kiến đi qua 2 mặt","Từ A tới C' qua đáy và mặt phải","02 / 12")
        self.add(cube_shell())
        path,pts,d=folded_path_segments(CHAIN2,S2,E2,ORANGE,5.8); self.add(path)
        panel=right_panel("MÔ HÌNH 2 MẶT",[("text","Mặt 1: đáy ABCD",20,BLUE),("text","Mặt 2: BCC'B'",20,CYAN),("text","Bản lề: BC",20,GOLD),("gap",),("text","Không được đi xuyên qua khối.",19,MUTED),("math","L_* = ?",38,GOLD)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Bài đầu: lập phương cạnh a. Kiến ở A, đích ở C phẩy. Ta xét đường đi qua đúng hai mặt: mặt đáy A B C D và mặt phải B C C phẩy B phẩy. Hai mặt chung cạnh B C, nên B C là bản lề. Đường thẳng A C phẩy trong không gian đi xuyên qua khối và không được phép.",1.8)

    def case2_unfold(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=1.00)
        self.add_hud("TRẢI PHẲNG · 01","Mở đúng quanh BC","C' chuyển động cùng mặt phải; B và C đứng yên","03 / 12")
        mobs=make_strip_mobs(CHAIN2,S2,E2); self.add(*mobs)
        panel=right_panel("PHÉP QUAY CỨNG",[("text","Giữ mặt đáy cố định.",20,INK),("text","Quay toàn bộ mặt phải 90°.",20,INK),("text","B, C thuộc trục quay nên bất động.",20,MUTED),("gap",),("math","B C = B C",28,CYAN)],CYAN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Ta cô lập đúng hai mặt cần dùng. Mặt đáy đứng yên. Toàn bộ mặt phải, bao gồm cả điểm C phẩy, quay chín mươi độ quanh đường thẳng B C. Không có điểm nào bị kéo bằng tay; đây là một chuyển động cứng của cả mặt.",1.4)
        _,steps,_,_=unfold_chain_numeric(CHAIN2); st=steps[0]; a=W(st["a"]); b=W(st["b"])
        self.narrate_play("Trong lúc quay, cạnh B C đứng yên tuyệt đối. Bốn cạnh của hình vuông vẫn giữ nguyên độ dài. Khi mặt phải chạm mặt phẳng đáy, ta đã có một bản trải đẳng cự.",Rotate(VGroup(*mobs[1:]),angle=st["angle"],axis=b-a,about_point=a),min_time=3.2)

    def case2_net(self):
        self.clear_all(); self.set_camera_orientation(phi=0,theta=-90*DEGREES,zoom=1.0)
        self.add_hud("TRẢI PHẲNG · 01","Bản trải 2 mặt","Đường ngắn nhất trở thành đường chéo của hình chữ nhật","04 / 12")
        net,d,T=net_group(CHAIN2,S2,E2); self.add_fixed_in_frame_mobjects(net)
        panel=right_panel("TÍNH ĐỘ DÀI",[("math","A C_1 = sqrt((2a)^2+a^2)",29,INK),("math","A C_1 = a sqrt(5)",38,GOLD),("gap",),("text","Đoạn thẳng cắt BC tại M.",19,MUTED),("math","B M = M C = frac(a,2)",28,CYAN)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Sau khi trải, hai hình vuông ghép thành một hình chữ nhật kích thước hai a nhân a. Ảnh của C phẩy gọi là C một. Đường ngắn nhất từ A tới C một là đường chéo của hình chữ nhật, nên độ dài bằng căn của bốn a bình phương cộng a bình phương, tức a căn năm.",1.8)
        self.narrate("Đường chéo này cắt cạnh bản lề B C đúng tại trung điểm M. Khi gấp trở lại, nửa đầu trở thành A M trên đáy, nửa sau trở thành M C phẩy trên mặt phải. Hai đoạn cộng lại vẫn bằng a căn năm.",1.6)

    def case2_variable(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 01","Vì sao M là tối ưu?","Cho điểm chuyển mặt X chạy trên BC","05 / 12")
        net,d,T=net_group(CHAIN2,S2,E2,show_path=False); self.add_fixed_in_frame_mobjects(net)
        # derive screen endpoints and hinge endpoints
        P=T(d["P2"]); Q=T(d["Q2"]); h=d["hits"][0]
        fc=d["fc"]; basis=d["basis"]; edge=h["edge"]
        E0=T(proj2(fc[CHAIN2[0]][edge[0]],basis)); E1=T(proj2(fc[CHAIN2[0]][edge[1]],basis))
        t=ValueTracker(0.12)
        xdot=always_redraw(lambda: Dot(E0+t.get_value()*(E1-E0),radius=0.06,color=ORANGE))
        path=always_redraw(lambda: VGroup(Line(P,E0+t.get_value()*(E1-E0),color=ORANGE,stroke_width=5.4),Line(E0+t.get_value()*(E1-E0),Q,color=ORANGE,stroke_width=5.4)))
        self.add_fixed_in_frame_mobjects(path,xdot)
        panel=right_panel("ĐIỂM X BẤT KỲ",[("math","B X = t a",28,ORANGE),("math","A X = a sqrt(1+t^2)",26,INK),("math","X C_1 = a sqrt(1+(1-t)^2)",24,INK),("gap",),("text","Nhỏ nhất khi A, X, C₁ thẳng hàng.",19,GREEN)],ORANGE)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate_play("Nếu điểm chuyển mặt là X bất kỳ trên B C, đường đi trên bản trải là đường gấp A X rồi X C một. Cho X chạy dọc cạnh, tổng độ dài thay đổi. Nhưng bất đẳng thức tam giác cho thấy tổng ấy nhỏ nhất đúng khi hai đoạn nhập thành một đường thẳng.",t.animate.set_value(0.84),min_time=3.5,rate_func=linear)
        self.narrate_play("Điều kiện thẳng hàng xảy ra tại trung điểm của B C. Vì vậy M không phải điểm đoán bằng mắt; nó là hệ quả bắt buộc của đường thẳng trong bản trải.",t.animate.set_value(0.50),min_time=2.6)

    def case2_fold(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Gấp lại và cho kiến chạy","Đường vàng phải nằm trên đúng hai mặt","06 / 12")
        self.add(cube_shell())
        path,pts,d=folded_path_segments(CHAIN2,S2,E2,GOLD,6.5); self.add(path)
        ant=Dot3D(W(pts[0]),radius=0.09,color=GREEN); self.add(ant)
        panel=right_panel("KẾT QUẢ BÀI 1",[("math","L_* = a sqrt(5)",40,GOLD),("math","B M = M C = frac(a,2)",27,CYAN),("gap",),("text","2 mặt · 1 cạnh bản lề",19,MUTED)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate_play("Gấp khối lại, kiến đi từ A tới M trên đáy.",MoveAlongPath(ant,Line(W(pts[0]),W(pts[1]))),min_time=1.9,rate_func=linear)
        self.narrate_play("Tại M, kiến đổi sang mặt phải và tiếp tục tới C phẩy. Đây là cùng một đường thẳng của bản trải sau khi được gấp qua cạnh B C.",MoveAlongPath(ant,Line(W(pts[1]),W(pts[2]))),min_time=2.2,rate_func=linear)

    def symmetry2(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Có bao nhiêu đường 2 mặt tương đương?","Đối xứng của lập phương tạo nhiều bản trải cùng độ dài","07 / 12")
        self.add(cube_shell())
        panel=right_panel("ĐỐI XỨNG",[("text","A nằm trên 3 mặt.",20,INK),("text","C' nằm trên 3 mặt đối diện.",20,INK),("text","Có 6 cặp mặt kề hợp lệ.",20,CYAN),("gap",),("math","L = a sqrt(5)",38,GOLD)],PURPLE)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("A thuộc ba mặt của lập phương, còn C phẩy thuộc ba mặt đối diện. Có sáu cách chọn một mặt chứa A và một mặt chứa C phẩy sao cho hai mặt ấy kề nhau. Do đối xứng, cả sáu bản trải đều cho cùng độ dài a căn năm. Vì vậy lời giải không phụ thuộc vào việc ta chọn đáy cộng mặt phải hay một cặp tương đương khác.",1.8)

    def case3_setup(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Bài 2 · Kiến đi qua 3 mặt","Từ tâm mặt trước P tới tâm mặt sau Q","08 / 12")
        self.add(cube_shell())
        P=raw_uv("front",0.5,0.5); Q=raw_uv("back",0.5,0.5)
        self.add(Dot3D(W(P),radius=0.085,color=GREEN),Dot3D(W(Q),radius=0.085,color=RED))
        panel=right_panel("VÌ SAO CẦN 3 MẶT?",[("text","Mặt trước và mặt sau đối nhau.",20,INK),("text","Chúng không có cạnh chung.",20,INK),("text","Phải qua ít nhất 1 mặt trung gian.",20,CYAN),("gap",),("math","P Q_s = ?",35,GOLD)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Bài thứ hai thay đổi bản chất. P là tâm mặt trước và Q là tâm mặt sau. Hai mặt này đối nhau, không chung cạnh. Vì thế không tồn tại đường đi qua đúng hai mặt từ một điểm trong mặt trước sang một điểm trong mặt sau. Mọi đường trên bề mặt phải đi qua ít nhất một mặt trung gian, tức ít nhất ba mặt.",1.8)

    def case3_unfold_net(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Mở dải 3 mặt","Mặt trước → mặt phải → mặt sau","09 / 12")
        mobs=make_strip_mobs(CHAIN3,S3,E3); self.add(*mobs)
        panel=right_panel("HAI BẢN LỀ",[("text","BB' giữa mặt trước và phải.",19,GOLD),("text","CC' giữa mặt phải và sau.",19,GOLD),("text","Mở lần lượt, không bóp méo mặt.",19,MUTED),("gap",),("math","L_* = 2 a",38,CYAN)],CYAN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Ta chọn mặt phải làm mặt trung gian. Dải ba mặt là mặt trước, mặt phải, rồi mặt sau. Có hai cạnh bản lề: B B phẩy và C C phẩy. Khi mở, ta không quay từng mặt về một vị trí vẽ sẵn; ta quay cả phần dải còn lại quanh bản lề hiện tại, đúng như mở một dải giấy thật.",1.7)
        unfold_animations(self,CHAIN3,mobs,run_each=1.55)
        self.narrate("Sau hai phép quay chín mươi độ, ba hình vuông nằm trên cùng một mặt phẳng thành một dải ba ô. P và Q vẫn là tâm của ô đầu và ô cuối.",1.1)
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 01","Đường thẳng qua dải 3 mặt","Hai tâm cách nhau đúng 2a trên bản trải","09 / 12")
        net,d,T=net_group(CHAIN3,S3,E3); self.add_fixed_in_frame_mobjects(net)
        panel=right_panel("KẾT QUẢ BÀI 2",[("text","P và Q nằm trên hai mặt đối.",20,INK),("text","Đường thẳng cắt cả 2 bản lề.",20,INK),("math","L_* = 2 a",42,GOLD),("gap",),("text","4 lựa chọn mặt trung gian đều tương đương.",18,MUTED)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Trên bản trải, đoạn nối hai tâm là một đoạn thẳng chạy xuyên dải. Khoảng cách giữa hai tâm bằng hai lần cạnh lập phương, nên L sao bằng hai a. Đường thẳng cắt cả hai cạnh bản lề tại trung điểm, vì vậy khi gấp lại nó thực sự đi qua đủ ba mặt.",1.7)
        self.narrate("Có bốn lựa chọn mặt trung gian: trái, phải, trên hoặc dưới. Do tính đối xứng, cả bốn đều cho hai a. Đây là ví dụ quan trọng để phân biệt hai ý: đường đi ngắn nhất trong một chuỗi mặt, và việc chọn chuỗi mặt nào là tối ưu toàn cục.",1.8)

    def case3_fold(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Gấp lại đường 3 mặt","P → X₁ → X₂ → Q trên ba mặt liên tiếp","10 / 12")
        self.add(cube_shell())
        path,pts,d=folded_path_segments(CHAIN3,S3,E3,GOLD,6.2); self.add(path)
        ant=Dot3D(W(pts[0]),radius=0.09,color=GREEN); self.add(ant)
        panel=right_panel("ĐƯỜNG GẤP 3 ĐOẠN",[("text","X₁ nằm trên BB'.",20,INK),("text","X₂ nằm trên CC'.",20,INK),("text","Cả hai là trung điểm cạnh.",20,CYAN),("gap",),("math","P Q_s = 2 a",36,GOLD)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate_play("Gấp dải trở lại khối, đoạn thẳng trên bản trải tách thành ba đoạn. Kiến đi từ P trên mặt trước tới X một, là trung điểm của B B phẩy.",MoveAlongPath(ant,Line(W(pts[0]),W(pts[1]))),min_time=2.0,rate_func=linear)
        self.narrate_play("Từ X một, kiến đi trên mặt phải tới X hai, trung điểm của C C phẩy.",MoveAlongPath(ant,Line(W(pts[1]),W(pts[2]))),min_time=1.8,rate_func=linear)
        self.narrate_play("Đoạn cuối nằm trên mặt sau và kết thúc tại Q. Ba đoạn nhìn gấp khúc trong không gian nhưng trở thành một đoạn thẳng duy nhất khi dải mặt được mở.",MoveAlongPath(ant,Line(W(pts[2]),W(pts[3]))),min_time=2.1,rate_func=linear)

    def reflection_rule(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 01","Luật phản xạ tại cạnh bản lề","Dấu hiệu nhận biết một geodesic trên đa diện","11 / 12")
        net,d,T=net_group(CHAIN2,S2,E2); self.add_fixed_in_frame_mobjects(net)
        panel=right_panel("SAU KHI TRẢI",[("text","Hai đoạn phải thẳng hàng.",20,INK),("text","Tương đương góc tới = góc ra khi nhìn trong hai mặt đã mở.",19,INK),("gap",),("math","alpha = beta",38,GOLD),("text","Nếu còn gãy ở bản lề → chưa tối ưu.",19,RED)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Có một cách nhìn rất hữu ích cho những bài sau. Ở cạnh bản lề, một đường geodesic ngắn nhất phải trở thành đường thẳng sau khi mở hai mặt. Vì thế góc mà đường đi tiến tới cạnh và góc nó rời cạnh, sau khi đặt hai mặt trong cùng một mặt phẳng, phải bằng nhau. Đây là phiên bản đa diện của nguyên lý phản xạ.",1.9)
        self.narrate("Nếu mở đúng hai mặt mà đường vẫn tạo một góc gãy tại bản lề, ta có thể rút ngắn nó bằng cách thay hai đoạn bằng đoạn thẳng nối hai đầu. Vì vậy điều kiện thẳng hàng không chỉ là mẹo giải; nó là điều kiện tối ưu hình học.",1.7)

    def summary(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 01","Tổng kết Video 01","Hai mức cơ bản: 2 mặt và 3 mặt","12 / 12")
        left=VGroup(
            VGroup(txt("2 MẶT",22,GOLD,BOLD),txt("1 bản lề · A → C' · a√5",21,INK)).arrange(RIGHT,buff=0.35),
            VGroup(txt("3 MẶT",22,CYAN,BOLD),txt("2 bản lề · tâm đối diện · 2a",21,INK)).arrange(RIGHT,buff=0.35),
            VGroup(txt("KIỂM TRA",22,GREEN,BOLD),txt("cắt đúng cạnh · đúng thứ tự · gấp lại đúng mặt",19,MUTED)).arrange(RIGHT,buff=0.35),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.48).move_to(LEFT*3.0+UP*0.25)
        self.add_fixed_in_frame_mobjects(left)
        panel=right_panel("MẪU TƯ DUY",[("text","Mặt kề → thử 2 mặt.",20,INK),("text","Mặt đối → cần ít nhất 3 mặt.",20,INK),("text","Mở cứng → nối thẳng → gấp lại.",20,CYAN),("gap",),("text","Video 02: dải 4–6 mặt có ràng buộc tuyến.",18,GREEN)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Video một bây giờ hoàn chỉnh từ nguyên lý đến kiểm chứng. Với hai mặt, ta có một bản lề và kết quả a căn năm. Với hai mặt đối nhau, đường phải đi qua ít nhất ba mặt và ví dụ tâm hai mặt đối cho độ dài hai a. Cả hai bài đều được kiểm chứng bằng cách gấp trở lại và cho kiến chạy trên đúng các mặt.",1.9)
        self.narrate("Điểm cần nhớ là không bắt đầu bằng công thức. Hãy hỏi hai điểm nằm trên những mặt nào, các mặt đó kề hay đối nhau, chuỗi mặt tối thiểu dài bao nhiêu, rồi mới trải. Sang video hai, chuỗi sẽ dài đến sáu mặt và việc kiểm tra từng cạnh bản lề sẽ trở thành phần quan trọng nhất.",1.8)

    def construct(self):
        self.intro(); self.principle(); self.case2_setup(); self.case2_unfold(); self.case2_net(); self.case2_variable(); self.case2_fold(); self.symmetry2(); self.case3_setup(); self.case3_unfold_net(); self.case3_fold(); self.reflection_rule(); self.summary()

class Smoke01(ThreeDScene):
    def case3_fold(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.98)
        self.add_hud("TRẢI PHẲNG · 01","Gấp lại đường 3 mặt","P → X₁ → X₂ → Q trên ba mặt liên tiếp","10 / 12")
        self.add(cube_shell())
        path,pts,d=folded_path_segments(CHAIN3,S3,E3,GOLD,6.2); self.add(path)
        ant=Dot3D(W(pts[0]),radius=0.09,color=GREEN); self.add(ant)
        panel=right_panel("ĐƯỜNG GẤP 3 ĐOẠN",[("text","X₁ nằm trên BB'.",20,INK),("text","X₂ nằm trên CC'.",20,INK),("text","Cả hai là trung điểm cạnh.",20,CYAN),("gap",),("math","P Q_s = 2 a",36,GOLD)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate_play("Gấp dải trở lại khối, đoạn thẳng trên bản trải tách thành ba đoạn. Kiến đi từ P trên mặt trước tới X một, là trung điểm của B B phẩy.",MoveAlongPath(ant,Line(W(pts[0]),W(pts[1]))),min_time=2.0,rate_func=linear)
        self.narrate_play("Từ X một, kiến đi trên mặt phải tới X hai, trung điểm của C C phẩy.",MoveAlongPath(ant,Line(W(pts[1]),W(pts[2]))),min_time=1.8,rate_func=linear)
        self.narrate_play("Đoạn cuối nằm trên mặt sau và kết thúc tại Q. Ba đoạn nhìn gấp khúc trong không gian nhưng trở thành một đoạn thẳng duy nhất khi dải mặt được mở.",MoveAlongPath(ant,Line(W(pts[2]),W(pts[3]))),min_time=2.1,rate_func=linear)

    def reflection_rule(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 01","Luật phản xạ tại cạnh bản lề","Dấu hiệu nhận biết một geodesic trên đa diện","11 / 12")
        net,d,T=net_group(CHAIN2,S2,E2); self.add_fixed_in_frame_mobjects(net)
        panel=right_panel("SAU KHI TRẢI",[("text","Hai đoạn phải thẳng hàng.",20,INK),("text","Tương đương góc tới = góc ra khi nhìn trong hai mặt đã mở.",19,INK),("gap",),("math","alpha = beta",38,GOLD),("text","Nếu còn gãy ở bản lề → chưa tối ưu.",19,RED)],GOLD)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Có một cách nhìn rất hữu ích cho những bài sau. Ở cạnh bản lề, một đường geodesic ngắn nhất phải trở thành đường thẳng sau khi mở hai mặt. Vì thế góc mà đường đi tiến tới cạnh và góc nó rời cạnh, sau khi đặt hai mặt trong cùng một mặt phẳng, phải bằng nhau. Đây là phiên bản đa diện của nguyên lý phản xạ.",1.9)
        self.narrate("Nếu mở đúng hai mặt mà đường vẫn tạo một góc gãy tại bản lề, ta có thể rút ngắn nó bằng cách thay hai đoạn bằng đoạn thẳng nối hai đầu. Vì vậy điều kiện thẳng hàng không chỉ là mẹo giải; nó là điều kiện tối ưu hình học.",1.7)

    def summary(self):
        self.clear_all(); self.add_hud("TRẢI PHẲNG · 01","Tổng kết Video 01","Hai mức cơ bản: 2 mặt và 3 mặt","12 / 12")
        left=VGroup(
            VGroup(txt("2 MẶT",22,GOLD,BOLD),txt("1 bản lề · A → C' · a√5",21,INK)).arrange(RIGHT,buff=0.35),
            VGroup(txt("3 MẶT",22,CYAN,BOLD),txt("2 bản lề · tâm đối diện · 2a",21,INK)).arrange(RIGHT,buff=0.35),
            VGroup(txt("KIỂM TRA",22,GREEN,BOLD),txt("cắt đúng cạnh · đúng thứ tự · gấp lại đúng mặt",19,MUTED)).arrange(RIGHT,buff=0.35),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.48).move_to(LEFT*3.0+UP*0.25)
        self.add_fixed_in_frame_mobjects(left)
        panel=right_panel("MẪU TƯ DUY",[("text","Mặt kề → thử 2 mặt.",20,INK),("text","Mặt đối → cần ít nhất 3 mặt.",20,INK),("text","Mở cứng → nối thẳng → gấp lại.",20,CYAN),("gap",),("text","Video 02: dải 4–6 mặt có ràng buộc tuyến.",18,GREEN)],GREEN)
        self.add_fixed_in_frame_mobjects(panel)
        self.narrate("Video một bây giờ hoàn chỉnh từ nguyên lý đến kiểm chứng. Với hai mặt, ta có một bản lề và kết quả a căn năm. Với hai mặt đối nhau, đường phải đi qua ít nhất ba mặt và ví dụ tâm hai mặt đối cho độ dài hai a. Cả hai bài đều được kiểm chứng bằng cách gấp trở lại và cho kiến chạy trên đúng các mặt.",1.9)
        self.narrate("Điểm cần nhớ là không bắt đầu bằng công thức. Hãy hỏi hai điểm nằm trên những mặt nào, các mặt đó kề hay đối nhau, chuỗi mặt tối thiểu dài bao nhiêu, rồi mới trải. Sang video hai, chuỗi sẽ dài đến sáu mặt và việc kiểm tra từng cạnh bản lề sẽ trở thành phần quan trọng nhất.",1.8)

    def construct(self):
        geometry_preflight(False); self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=1.0)
        for chain,S,E in [(CHAIN2,S2,E2),(CHAIN3,S3,E3)]:
            self.clear(); mobs=make_strip_mobs(chain,S,E); self.add(*mobs); unfold_animations(self,chain,mobs,run_each=0.45); self.wait(0.1)

def render_smoke():
    geometry_preflight(True); config.pixel_width=854; config.pixel_height=480; config.frame_rate=15; config.media_dir=str(SMOKE_MEDIA_DIR); config.output_file="trai_phang_01_rebuilt_smoke"; config.disable_caching=True
    scene=Smoke01(); scene.render(); path=Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists(): raise RuntimeError(path)
    return path

def render_full():
    geometry_preflight(True); config.pixel_width=FINAL_WIDTH; config.pixel_height=FINAL_HEIGHT; config.frame_rate=FINAL_FPS; config.media_dir=str(MEDIA_DIR); config.output_file="trai_phang_01_lap_phuong_2_3_mat_REBUILT_1080p"; config.disable_caching=False
    scene=TraiPhang01Rebuilt(); scene.render(); video=Path(scene.renderer.file_writer.movie_file_path)
    if not video.exists(): raise RuntimeError(video)
    master=ROOT/"master_narration_trai_phang_01_rebuilt.wav"; build_master_audio(scene.audio_events,probe_duration(video),master)
    final=video.with_name(video.stem+"_WITH_AUDIO.mp4"); mux_audio(video,master,final); validate_audio(master); print("FINAL:",final); return final

if __name__=="__main__":
    if "--geometry-preflight" in sys.argv: geometry_preflight(True); raise SystemExit(0)
    if "--smoke-render" in sys.argv: render_smoke(); raise SystemExit(0)
    render_full()
