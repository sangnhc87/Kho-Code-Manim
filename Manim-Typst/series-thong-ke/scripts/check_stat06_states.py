"""Dependency-free preflight: instantiate 32 Manim states using a strict minimal API mock.
Not a render; actual SVG/Manim rendering is independently enforced by GitHub Actions.
"""
from __future__ import annotations
import importlib,sys,types,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

class Shape:
    width=1.0;height=1.0
    def __init__(self,*args,**kwargs):pass
    def move_to(self,*args,**kwargs):return self
    def scale_to_fit_width(self,*args,**kwargs):return self
    def scale_to_fit_height(self,*args,**kwargs):return self
    def add(self,*args,**kwargs):return self
    def __getitem__(self,i):return self
class Tracker(Shape):
    def __init__(self,x):self.value=x
    def get_value(self):return self.value
class Config:pass
m=types.ModuleType('manim')
for n in ('Scene','VGroup','Rectangle','RoundedRectangle','Line','Dot','Text','Circle','DashedLine',
          'SVGMobject','FadeIn','FadeOut','Indicate'):
    setattr(m,n,type(n,(Shape,),{}))
m.ValueTracker=Tracker
m.config=Config()
m.always_redraw=lambda f:f()
m.smooth=lambda x:x
sys.modules['manim']=m
scene=importlib.import_module('stat06.scene')
from stat06.lesson import BEATS
scene_obj=scene.STAT06()
scene_obj.frame()
for beat in BEATS:
    graphic,tracker=scene.VISUALS[beat.chapter-1](beat.step)
    if graphic is None:raise AssertionError((beat.chapter,beat.step))
    if tracker is not None and not isinstance(tracker,Tracker):raise AssertionError('wrong tracker')
    if beat.chapter==5 and beat.step==3 and tracker is None:raise AssertionError('missing live tracker')
    if beat.chapter==7 and beat.step==1 and tracker is None:raise AssertionError('missing outlier tracker')
with tempfile.TemporaryDirectory() as scratch:
    original_root=scene.ROOT
    scene.ROOT=Path(scratch)
    folder=scene.ROOT/'assets'/'stat06_formulas'
    folder.mkdir(parents=True)
    for k in scene.FORM_KEYS:
        (folder/(k+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
    for beat in BEATS:
        if scene_obj.notes(beat) is None:raise AssertionError('missing note')
    scene.ROOT=original_root
print('STAT06_STATE_PREFLIGHT_OK',len(BEATS),'visuals and notes')
