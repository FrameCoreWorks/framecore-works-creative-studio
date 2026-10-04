"""Original ManimCE geometry example; no LaTeX, remote assets or provider calls.

Copy into the existing authorized Manim project's scene directory. In a workspace
with a registered Manim wrapper, use that wrapper and its request contract.
This portable example does not install or configure a Manim runtime.
"""
from manim import Scene, Square, Text, Create, FadeIn, Rotate, PI, UP, DOWN


class AreaPreserved(Scene):
    """A square rotates while its side lengths and area remain unchanged."""

    def construct(self):
        self.camera.background_color = "#f3eee2"
        title = Text("ROTATION PRESERVES AREA", color="#182023", font_size=32).to_edge(UP)
        square = Square(side_length=2.0, color="#b83a24", fill_opacity=0.18)
        caption = Text("Same side lengths. Same area.", color="#182023", font_size=24).to_edge(DOWN)
        self.play(FadeIn(title), Create(square), FadeIn(caption), run_time=1)
        self.wait(0.5)
        self.play(Rotate(square, angle=PI / 4), run_time=3)
        self.wait(1.5)
