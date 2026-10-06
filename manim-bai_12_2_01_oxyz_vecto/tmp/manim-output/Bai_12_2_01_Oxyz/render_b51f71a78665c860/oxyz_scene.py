
from manim import *
import numpy as np
import math,json,textwrap
from pathlib import Path
HERE=Path(__file__).resolve().parent
LESSONS=json.loads((HERE/'lessons.json').read_text(encoding='utf-8'))
SETTINGS=json.loads((HERE/'settings.json').read_text(encoding='utf-8'))
BG='#0B1120';PANEL='#0E1D34';INK='#EDF4FF';MUTED='#7A9ABF'
BLUE='#38BDF8';CYAN='#3ADEC8';GOLD='#FFD700';GREEN='#4ADE80';RED='#FF6B6B'
config.background_color=BG
config.pixel_width=SETTINGS['width'];config.pixel_height=SETTINGS['height'];config.frame_rate=SETTINGS['fps']
TMPL=TexTemplate();TMPL.add_to_preamble(r'\usepackage{amsmath}\usepackage{amssymb}')
def pt(x,y,z=0):return np.array([x,y,z],dtype=float)
def txt(s,size=24,color=INK,bold=False):
    return Text(s,font='DejaVu Sans',font_size=size,color=color,weight='BOLD' if bold else 'NORMAL',disable_ligatures=True)
def mtx(s,size=31,color=INK):return MathTex(s,font_size=size,color=color,tex_template=TMPL)
def fit(m,w,h=None):
    k=min(1,w/max(m.width,1e-9))
    if h is not None:k=min(k,h/max(m.height,1e-9))
    return m.scale(k)
def panel(w,h,center,fill=1):
    return RoundedRectangle(width=w,height=h,corner_radius=.15,fill_color=PANEL,fill_opacity=fill,
        stroke_color=MUTED,stroke_opacity=.23,stroke_width=1.2).move_to(center)

class VectorView:
    """True world geometry; one isotropic scale; screen-fixed labels only.
    Arc sampled in the span of its two vectors, never a screen Circle.
    Orthographic camera makes projected parallelism exact and stable.
    """
    def __init__(self,scene,data,pose='base'):
        self.scene=scene;data=data.get('variants',{}).get(pose,data);self.data=data;self.pose=pose
        self.points={k:np.array(v,dtype=float) for k,v in data['points'].items()}
        self.R=scene.camera.get_rotation_matrix()
        values=list(self.points.values())+[np.zeros(3)]
        cloud=np.array(values);lo=cloud.min(axis=0);hi=cloud.max(axis=0)
        self.axislo=np.minimum(lo-.35,-.5);self.axishi=np.maximum(hi+.55,1.7)
        samples=list(values)
        for a in range(3):
            for t in [self.axislo[a],self.axishi[a]]:
                p=np.zeros(3);p[a]=t;samples.append(p)
        projection=(self.R@np.array(samples).T).T[:,:2]
        mid=(projection.min(axis=0)+projection.max(axis=0))/2
        ext=projection.max(axis=0)-projection.min(axis=0)
        self.scale=min(4.55/max(ext[0],1e-8),3.4/max(ext[1],1e-8),1.3)
        self.offset=self.R.T@(pt(-3.78,.42)-pt(*mid)*self.scale)
        self.world=VGroup();self.labels=VGroup();self.used=[]
        self.make_axes()
        self.make_geometry()
    def worldpt(self,p):return self.offset+self.scale*np.array(p,dtype=float)
    def screenpt(self,p):
        q=self.R@self.worldpt(p);q[2]=0;return q
    def label(self,s,p,col=INK,size=22):
        q=self.screenpt(p);mob=mtx(s,size,col)
        best=None;cost=1e9
        for dx,dy in [(0,.24),(.25,.12),(-.25,.12),(.22,-.23),(-.22,-.23),(0,-.30),(.44,0),(-.44,0),(0,.48)]:
            c=q+pt(dx,dy)
            l,r=c[0]-mob.width/2,c[0]+mob.width/2;b,t=c[1]-mob.height/2,c[1]+mob.height/2
            penalty=100*max(0,-6.55-l)+100*max(0,r+1.02)+100*max(0,t-2.35)+100*max(0,-1.62-b)
            for ll,rr,bb,tt in self.used:
                penalty+=1000*max(0,min(r,rr)-max(l,ll)+.08)*max(0,min(t,tt)-max(b,bb)+.08)
            if penalty<cost:best=(c,(l,r,b,t));cost=penalty
        c,box=best;mob.move_to(c);self.used.append(box);self.labels.add(mob)
    def edge(self,a,b,col=MUTED,dash=False,width=2):
        a=self.worldpt(a);b=self.worldpt(b)
        return DashedLine(a,b,color=col,stroke_width=width,dash_length=.085) if dash else Line(a,b,color=col,stroke_width=width)
    def arrow(self,a,b,col):
        a=self.worldpt(a);b=self.worldpt(b);length=np.linalg.norm(b-a)
        return Arrow3D(start=a,end=b,color=col,thickness=.014,height=min(.17,length*.19),base_radius=.045,resolution=12)
    def make_axes(self):
        cols=[BLUE,CYAN,RED]
        for axis in range(3):
            a=np.zeros(3);b=np.zeros(3);a[axis]=self.axislo[axis];b[axis]=self.axishi[axis]
            self.world.add(self.arrow(a,b,cols[axis]).set_opacity(.48))
            self.label(['x','y','z'][axis],b,cols[axis],24)
            unit=np.zeros(3);unit[axis]=1
            d=np.zeros(3);d[(axis+1)%3]=.055
            self.world.add(self.edge(unit-d,unit+d,cols[axis],width=2))
        origin_label=self.data.get('aliases',{}).get(self.pose,{}).get('O','O')
        if 'A' in self.points and np.linalg.norm(self.points['A'])<1e-9:origin_label='A=O'
        self.label(origin_label,np.zeros(3),MUTED,20)
    def make_geometry(self):
        d=self.data;p=self.points
        for face in d['faces']:
            self.world.add(Polygon(*[self.worldpt(p[k]) for k in face],fill_color=BLUE,fill_opacity=.12,stroke_width=0))
        for a,b,kind in d['edges']:
            self.world.add(self.edge(p[a],p[b],MUTED,kind=='dash',2))
        vectors=list(d['vectors'])
        if self.pose=='normal':vectors.append([*d['normal'],'gold'])
        if self.pose=='reverse':vectors.append([*d['reverse'],'gold'])
        if self.pose=='obtuse':vectors.append([*d['alternate'],'gold'])
        if self.pose=='volume' and 'normal' in d:vectors.append([*d['normal'],'gold'])
        for a,b,col in vectors:
            self.world.add(self.arrow(p[a],p[b],{'blue':BLUE,'cyan':CYAN,'gold':GOLD}.get(col,INK)))
        hidden=set()
        for key in ['normal','reverse','alternate']:
            if key in d:hidden.add(d[key][1])
        visible=set(p)-hidden
        visible.update(v[1] for v in vectors)
        if self.pose=='base' and 'projection' in d:visible.discard('H')
        for name in sorted(visible):
            if name=='O' or (name=='A' and np.linalg.norm(p[name])<1e-9):continue
            col=GOLD if name in {'N','R','H','I','G','S'} else INK
            self.world.add(Dot3D(self.worldpt(p[name]),radius=.043,color=col,resolution=(6,12)))
            self.label(d.get('aliases',{}).get(self.pose,{}).get(name,name),p[name],col)
        if self.pose=='components' and 'components' in d:
            q=p[d['components']];path=[np.zeros(3),pt(q[0],0,0),pt(q[0],q[1],0),q]
            for a,b,col in zip(path,path[1:],[BLUE,CYAN,RED]):
                if np.linalg.norm(b-a)>1e-8:self.world.add(self.arrow(a,b,col));self.label(str(round(float(np.linalg.norm(b-a)),3)),(a+b)/2,col,19)
            self.labels.add(fit(mtx(r'\Delta x\quad\Delta y\quad\Delta z',24),4.7).move_to(pt(-3.78,-1.94)))
        if 'angle' in d and self.pose not in ['obtuse','reverse']:
            a,b=d['angle'];origin=p.get('O',p.get('A',np.zeros(3)))
            self.arc(origin,p[a]-origin,p[b]-origin)
        if self.pose=='obtuse':
            a,b=d['angle'];o=p['O'];self.arc(o,p[a]-o,p[d['alternate'][1]]-o)
        if self.pose=='projection':
            u,v=(p[k] for k in d['projection']);h=np.dot(v,u)/np.dot(u,u)*u
            self.world.add(self.edge(v,h,GOLD,True,2.5),self.arrow(np.zeros(3),h,GOLD))
            self.right_angle(h,u,v-h)
            if 'H' not in visible:
                self.world.add(Dot3D(self.worldpt(h),radius=.04,color=GOLD,resolution=(6,12)));self.label('H',h,GOLD)
        if self.pose=='volume':
            a,b=d['height'];self.world.add(self.edge(p[a],p[b],GOLD,True,3))
            self.right_angle(p[b],p[a]-p[b],p['B']-p['A'])
        note='Ba trục cùng đơn vị • Nét đứt: đường phụ'
        if self.pose in ['normal','reverse','volume']:note='Mũi tên pháp tuyến biểu diễn hướng, đã thu ngắn'
        self.labels.add(fit(txt(note,15,MUTED),5.4,.4).move_to(pt(-3.78,-2.56)))
        self.labels.add(fit(txt('Phối cảnh 3D • Không đo góc trên màn hình',14,MUTED),5.4,.4).move_to(pt(-3.78,-2.89)))
    def arc(self,o,u,v):
        if np.linalg.norm(u)<1e-9 or np.linalg.norm(v)<1e-9:return
        e=u/np.linalg.norm(u);f=v/np.linalg.norm(v);c=np.clip(np.dot(e,f),-1,1);theta=math.acos(c)
        if theta<1e-7 or abs(theta-math.pi)<1e-7:return
        w=(f-c*e)/math.sin(theta);radius=min(np.linalg.norm(u),np.linalg.norm(v))*.27
        points=[self.worldpt(o+radius*(e*math.cos(t)+w*math.sin(t))) for t in np.linspace(0,theta,65)]
        arc=VMobject(color=GOLD,stroke_width=2.3);arc.set_points_as_corners(points);self.world.add(arc)
        if abs(c)<1e-8:self.right_angle(o,u,v)
        else:self.label(r'\theta',o+radius*1.35*(e*math.cos(theta/2)+w*math.sin(theta/2)),GOLD,20)
    def right_angle(self,o,u,v):
        if np.linalg.norm(u)<1e-9 or np.linalg.norm(v)<1e-9:return
        e=u/np.linalg.norm(u);f=v/np.linalg.norm(v)
        if abs(np.dot(e,f))>1e-7:raise ValueError('Ký hiệu góc vuông đặt vào góc không vuông')
        r=min(.24,np.linalg.norm(u)*.19,np.linalg.norm(v)*.19)
        points=[self.worldpt(o+r*e),self.worldpt(o+r*(e+f)),self.worldpt(o+r*f)]
        mark=VMobject(color=GOLD,stroke_width=2.4);mark.set_points_as_corners(points);self.world.add(mark)

class VectorLesson(ThreeDScene):
    lesson_id='C01'
    def construct(self):
        lesson=next(l for l in LESSONS if l['id']==self.lesson_id);self.events=[]
        self.set_camera_orientation(phi=65*DEGREES,theta=-48*DEGREES,focal_distance=1e9,zoom=1)
        self.camera.reset_rotation_matrix()
        title=fit(txt(lesson['title'],31,INK,True),12.9,.48).move_to(pt(0,3.5))
        subtitle=txt('BÀI 12.2.01 • OXYZ VÀ CÁC PHÉP TOÁN VECTƠ',16,BLUE).move_to(pt(0,3.07))
        left=panel(5.95,6.05,pt(-3.78,-.22),fill=0);right=panel(6.95,6.05,pt(2.92,-.22),fill=.98)
        footer=txt(SETTINGS['teacher'],19,MUTED).move_to(pt(-4.7,-3.74))
        rule=Line(pt(-6.7,-3.44),pt(6.7,-3.44),color=MUTED,stroke_width=1)
        self.add_fixed_in_frame_mobjects(title,subtitle,left,right,footer,rule)
        view=None;pose=None
        for pi,page in enumerate(lesson['pages']):
            if pose!=page['action']:
                new=VectorView(self,lesson['model'],page['action'])
                if view is not None:
                    self.play(FadeOut(view.world),FadeOut(view.labels),run_time=.35)
                    self.remove_fixed_in_frame_mobjects(view.labels);self.remove(view.world)
                self.add_fixed_in_frame_mobjects(new.labels);self.add(new.world)
                self.play(LaggedStart(*[FadeIn(m) for m in new.world],lag_ratio=.045),FadeIn(new.labels),run_time=1.2)
                view=new;pose=page['action']
            heading=fit(txt(page['title'],23,CYAN,True),6.15,.55).move_to(pt(-.19,2.48),aligned_edge=LEFT)
            counter=txt(f"Chương {lesson['order']}/{lesson['total']} • Trang {pi+1}/{len(lesson['pages'])}",14,MUTED).move_to(pt(4.7,-3.74))
            self.add_fixed_in_frame_mobjects(heading,counter);self.play(FadeIn(heading),run_time=.45)
            current=[];previous=None
            for ri,row in enumerate(page['rows']):
                if row['kind']=='math':mob=fit(mtx(row['text'],31,GOLD if row.get('gold') else INK),6.15,.94)
                else:
                    s=textwrap.fill(row['text'],width=41,break_long_words=False,break_on_hyphens=False)
                    mob=fit(txt(s,24),6.15,.92)
                mob.move_to(pt(-.19,1.55-ri*1.10),aligned_edge=LEFT)
                self.camera.add_fixed_in_frame_mobjects(mob)
                start=self.time;self.add_sound(row['audio'])
                if row['kind']=='math' and previous is not None:
                    copy=previous.copy();self.add_fixed_in_frame_mobjects(copy)
                    self.play(TransformMatchingTex(copy,mob),run_time=.9)
                    self.remove_fixed_in_frame_mobjects(copy)
                else:self.play(Write(mob) if row['kind']=='math' else FadeIn(mob,shift=UP*.08),run_time=.9)
                current.append(mob)
                if row['kind']=='math':previous=mob
                self.events.append({'start':start,'end':start+row['duration'],'text':row['voice']})
                self.wait(max(.15,row['duration']-(self.time-start))+.3)
                if row.get('gold'):self.play(Circumscribe(mob,color=GOLD,buff=.07),run_time=.8)
                if row.get('pause'):self.wait(row['pause'])
            self.wait(.9)
            self.play(*[FadeOut(m) for m in current+[heading,counter]],run_time=.45)
            self.remove_fixed_in_frame_mobjects(*current,heading,counter)
        (HERE/'events').mkdir(exist_ok=True)
        (HERE/'events'/(self.lesson_id+'.json')).write_text(json.dumps(self.events,ensure_ascii=False),encoding='utf-8')

class VectorAudit(ThreeDScene):
    lesson_id='C01';pose='base'
    def construct(self):
        lesson=next(l for l in LESSONS if l['id']==self.lesson_id)
        self.set_camera_orientation(phi=65*DEGREES,theta=-48*DEGREES,focal_distance=1e9,zoom=1)
        self.camera.reset_rotation_matrix()
        title=fit(txt(lesson['title'],31,INK,True),12.9,.48).move_to(pt(0,3.5))
        subtitle=txt('BÀI 12.2.01 • KIỂM TRA HÌNH TRƯỚC KHI RENDER',16,BLUE).move_to(pt(0,3.07))
        left=panel(5.95,6.05,pt(-3.78,-.22),fill=0);right=panel(6.95,6.05,pt(2.92,-.22),fill=.98)
        self.add_fixed_in_frame_mobjects(title,subtitle,left,right)
        view=VectorView(self,lesson['model'],self.pose);self.add(view.world);self.add_fixed_in_frame_mobjects(view.labels)
        page=next((p for p in lesson['pages'] if p['action']==self.pose),lesson['pages'][0])
        heading=fit(txt(page['title'],23,CYAN,True),6.15,.55).move_to(pt(-.19,2.48),aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(heading)
        for ri,row in enumerate(page['rows']):
            if row['kind']=='math':m=fit(mtx(row['text'],31,GOLD if row.get('gold') else INK),6.15,.94)
            else:m=fit(txt(textwrap.fill(row['text'],41,break_long_words=False),24),6.15,.92)
            m.move_to(pt(-.19,1.55-ri*1.10),aligned_edge=LEFT);self.add_fixed_in_frame_mobjects(m)
        self.wait(.1)
class C_C01(VectorLesson):
    lesson_id='C01'

class C_C02(VectorLesson):
    lesson_id='C02'

class C_C03(VectorLesson):
    lesson_id='C03'

class C_C04(VectorLesson):
    lesson_id='C04'

class C_C05(VectorLesson):
    lesson_id='C05'

class C_C06(VectorLesson):
    lesson_id='C06'

class C_C07(VectorLesson):
    lesson_id='C07'

class C_C08(VectorLesson):
    lesson_id='C08'

class C_C09(VectorLesson):
    lesson_id='C09'

class C_C10(VectorLesson):
    lesson_id='C10'

class C_C11(VectorLesson):
    lesson_id='C11'

class C_C12(VectorLesson):
    lesson_id='C12'

class C_C13(VectorLesson):
    lesson_id='C13'

class C_C14(VectorLesson):
    lesson_id='C14'


