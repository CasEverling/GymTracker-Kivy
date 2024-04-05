from dataclasses import dataclass
from typing import List, Tuple

from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget

@dataclass
class Shadow:
    size: float
    color: List[float]
    radius: float
    internal_size: List[float]
    iterations: int = 100
    
    def draw_shadow(self, widget: Widget) -> None:
        color: List[float, float, float] = self.color + [1/self.iterations]
        shadow_size: float = None

        for i in range(self.iterations):
            shadow_size = (self.iterations-i)*self.size/self.iterations

            size = (
                self.internal_size[0] + 2*shadow_size,
                self.internal_size[1] + 2*shadow_size,
            )
            pos = (
                widget.pos[0] - shadow_size,
                widget.pos[1] - shadow_size,
            )
            
            with widget.canvas.before:
                Color(rgba = color)
                RoundedRectangle(
                    size = size,
                    pos = pos,
                    radius = self.radius,
                )


