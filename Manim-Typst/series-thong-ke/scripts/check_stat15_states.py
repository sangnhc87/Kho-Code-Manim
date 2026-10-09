"""Mock static API preflight, NOT a real Manim render.
Actual Manim and SVG smoke rendering is mandatory in GitHub Actions.
"""
from __future__ import annotations
import importlib,sys,types,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
class Shape:
    width=1.0;height=1.0
    def __init__(self,*args,**kw):pass
    def move_to(self,*a,**kw):return self
    def scale_to_fit_width(self,*a,**kw):return self
    def scale_to_fit_height(self,*a,**kw):return self
    def add(self,*a,**kw):return self
    def __getitem__(self,i):return self
class Tracker(Shape):
    def __init__(self,x):self.value=x
    def get_value(self):return self.value
class Config:pass
m=types.ModuleType('manim')
for n in ('Scene','VGroup','Rectangle','RoundedRectangle','Line','Dot','Text','Circle',
          'SVGMobject','FadeIn','FadeOut','Indicate'):
    setattr(m,n,type(n,(Shape,),{}))
m.ValueTracker=Tracker;m.config=Config();m.always_redraw=lambda f:f();m.smooth=lambda x:x
sys.modules['manim']=m
scene=importlib.import_module('stat15.scene')
from stat15.lesson import BEATS
obj=scene.STAT15()
assert obj.frame() is not None
count=0
for b in BEATS:
    visual,tracker=scene.VISUALS[b.chapter-1](b.step)
    assert visual is not None
    if tracker is not None:raise AssertionError('Unexpected visual tracker')
    count+=1
with tempfile.TemporaryDirectory() as scratch:
    saved=scene.ROOT;scene.ROOT=Path(scratch)
    out=scene.ROOT/'assets'/'stat15_formulas';out.mkdir(parents=True)
    for name in scene.FORM_KEYS:(out/(name+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
    for b in BEATS:assert obj.notes(b) is not None
    scene.ROOT=saved
print('STAT15_MOCK_STATES_OK',count,'visuals and notes; NOT real rendering')
