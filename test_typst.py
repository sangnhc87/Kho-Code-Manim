from manim import *

class TestTypst(Scene):
    def construct(self):
        text = Typst("Công thức Toán với Typst: $int_0^1 x^2 dx = 1/3$")
        self.play(Write(text))
        self.wait(2)
