import os
import shutil
from manim import *

class TestTypst(Scene):
    def construct(self):
        text = Typst("Công thức Toán với Typst: $int_0^1 x^2 dx = 1/3$")
        self.play(Write(text))
        self.wait(2)

if __name__ == "__main__":
    # Configure output directory
    output_dir = "/tmp/manim-output"
    os.makedirs(output_dir, exist_ok=True)
    
    config.media_dir = output_dir
    config.video_dir = output_dir
    config.format = "mp4"
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    
    # Render scene
    scene = TestTypst()
    scene.render()
    
    # Locate the output video
    mp4_path = os.path.join(output_dir, "TestTypst.mp4")
    
    # The output might actually be nested inside /tmp/manim-output/TestTypst/1080p60/
    # So we'll find all mp4s in the directory and move the latest one to the root output
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".mp4") and file != "TestTypst.mp4":
                file_path = os.path.join(root, file)
                shutil.copy(file_path, mp4_path)
                break
