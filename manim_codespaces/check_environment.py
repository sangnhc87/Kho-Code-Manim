"""Kiểm tra nhanh môi trường; --smoke dựng đoạn thử ngắn sau lần cài đầu."""
import importlib.metadata as meta
import shutil,subprocess,sys,tempfile
from pathlib import Path

def check():
    missing=[n for n in ['ffmpeg','ffprobe','latex','dvisvgm','kpsewhich','fc-match'] if not shutil.which(n)]
    if missing:raise RuntimeError('Thiếu công cụ: '+', '.join(missing))
    for name in ['manim','edge-tts','nest_asyncio','ipywidgets']:meta.version(name)
    if meta.version('manim')!='0.19.0':raise RuntimeError('Cần manim==0.19.0')
    import manim,edge_tts,nest_asyncio
    for name in ['standalone.cls','amsmath.sty','amssymb.sty','bm.sty']:
        r=subprocess.run(['kpsewhich',name],capture_output=True,text=True)
        if r.returncode or not r.stdout.strip():raise RuntimeError('Thiếu TeX: '+name)
    font=subprocess.run(['fc-match','DejaVu Sans','--format=%{family}'],capture_output=True,text=True,check=True).stdout
    if 'DejaVu Sans' not in font:raise RuntimeError('Thiếu phông DejaVu Sans')

def smoke():
    with tempfile.TemporaryDirectory(prefix='manim-smoke-') as directory:
        root=Path(directory);source=root/'smoke.py'
        source.write_text('''from manim import *
class Smoke(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65*DEGREES,theta=-48*DEGREES)
        self.add(Dot3D(point=ORIGIN,color=BLUE,resolution=(6,8)))
        self.add_fixed_in_frame_mobjects(Text("Nước dâng – Tâm tỉ cự",font="DejaVu Sans",font_size=25).to_edge(UP))
        self.add_fixed_in_frame_mobjects(MathTex(r"A(h)h'(t)=Q").to_edge(DOWN))
        self.wait(0.3)
''',encoding='utf-8')
        subprocess.run([sys.executable,'-m','manim','--renderer','cairo','-ql','--disable_caching',
            '--progress_bar','none','--verbosity','ERROR','--media_dir',str(root/'media'),str(source),'Smoke'],check=True)
        videos=[p for p in (root/'media').rglob('Smoke.mp4') if 'partial_movie_files' not in str(p)]
        if not videos:raise RuntimeError('Không tìm thấy MP4 kiểm tra')
        subprocess.run(['ffprobe','-v','error',str(videos[0])],check=True)

if __name__=='__main__':
    try:
        check()
        if '--smoke' in sys.argv:smoke()
        print('Môi trường Manim 0.19.0, tiếng Việt, LaTeX và FFmpeg: đạt.')
    except Exception as e:
        print('Môi trường chưa sẵn sàng: '+str(e),file=sys.stderr);sys.exit(1)
