"""Offline mock API preflight; NEVER claim this is a real Manim or Typst render."""
from __future__ import annotations
import importlib,sys,types,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
class Shape:
    width=1.;height=1.
    def __init__(self,*a,**kw):pass
    def move_to(self,*a,**kw):return self
    def scale_to_fit_width(self,*a,**kw):return self
    def scale_to_fit_height(self,*a,**kw):return self
    def add(self,*a,**kw):return self
    def __getitem__(self,i):return self
class Tracker(Shape):
    def __init__(self,v):self.value=v
    def get_value(self):return self.value
class Config:pass
m=types.ModuleType('manim')
for name in ('Scene','VGroup','Rectangle','RoundedRectangle','Line','Dot','Text','Circle',
             'SVGMobject','FadeIn','FadeOut','Indicate'):
    setattr(m,name,type(name,(Shape,),{}))
m.ValueTracker=Tracker;m.config=Config();m.always_redraw=lambda fn:fn();m.smooth=lambda x:x
sys.modules['manim']=m
scene=importlib.import_module('stat18.scene')
from stat18.lesson import BEATS
obj=scene.STAT18();assert obj.frame() is not None
count=0;animated=0
for b in BEATS:
    g,tr=scene.VISUALS[b.chapter-1](b.step)
    assert g is not None
    if tr is not None:
        assert (b.chapter,b.step)==(7,2)
        animated+=1
    count+=1
with tempfile.TemporaryDirectory() as scratch:
    saved=scene.ROOT;scene.ROOT=Path(scratch)
    folder=scene.ROOT/'assets/stat18_formulas';folder.mkdir(parents=True)
    for key in scene.FORM_KEYS:(folder/(key+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
    for beat in BEATS:assert obj.notes(beat) is not None
    scene.ROOT=saved
assert (count,animated)==(32,1)
print('STAT18_MOCK_STATES_PASS 32 visuals, 32 explanations, 1 tracked animation; NOT real render')
