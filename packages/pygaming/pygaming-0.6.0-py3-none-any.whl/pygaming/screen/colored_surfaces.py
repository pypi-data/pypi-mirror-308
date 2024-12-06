"""The colored_surface module contains the ColoredSurface class which is a pygame Surface."""

from typing import Union, Sequence
from pygame import Surface, SRCALPHA
from ..color import Color
import pygame

ColorLike = Union[Color, tuple[int, int, int], tuple[int, int, int, int]]

class ColoredRectangle(Surface):
    """A ColoredRectangle is a Surface with only one color."""

    def __init__(
        self,
        color: ColorLike,
        width: int,
        height: int,
        thickness: int = 0,
        border_radius: int = -1,
        border_top_left_radius: int = -1,
        border_top_right_radius: int = -1,
        border_bottom_left_radius: int = -1,
        border_bottom_right_radius: int = -1
    ):
        """Create a rectangle"""
        super().__init__((width, height), SRCALPHA)

        pygame.draw.rect(
            self,
            color,
            (0,0, width, height),
            thickness,
            border_radius,
            border_top_left_radius,
            border_top_right_radius,
            border_bottom_left_radius,
            border_bottom_right_radius
        )
    
class ColoredCircle(Surface):
    """A ColoredCircle is a Surface with a colored circle at the center of it."""

    def __init__(
        self,
        color: ColorLike,
        radius: int,
        thickness: int = 0,
        draw_top_right: bool = False,
        draw_top_left: bool = False,
        draw_bottom_left: bool = False,
        draw_bottom_right: bool = False,):
        super().__init__((radius*2, radius*2), SRCALPHA)
        pygame.draw.circle(self, color, (radius, radius), radius, thickness, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)

class ColoredPolygon(Surface):

    def __init__(
        self,
        color: ColorLike,
        points: Sequence[tuple[int, int]],
        thickness: int = 0
        ):
        min_x = min(p[0] for p in points)
        min_y = min(p[1] for p in points)
        points = [(p[0] - min_x, p[1] - min_y) for p in points]
        max_x = max(p[0] for p in points)
        max_y = max(p[1] for p in points)
        super().__init__((max_x, max_y), SRCALPHA)
        pygame.draw.polygon(self, color, points, thickness)
