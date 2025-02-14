"""
Breakout Init
=============
Package init for resources shared accross the whole project

Class
-----
Capstone in Computer Science
UMGC CMSC 495
Professor Munoz

Team Charlie
------------
Daniel Coreas
Aimi Hanson
Terrence Jackson
Thomas Nugent

"""

from dataclasses import dataclass

import pygame


@dataclass
class Size:
    """Dataclass to store sizes for easy access"""

    width: int
    height: int


pygame.init()
screen_size = Size(500, 600)

color_choices = [
    pygame.Color("red"),
    pygame.Color("orange"),
    pygame.Color("yellow"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("purple"),
    pygame.Color("pink"),
]

__all__ = [
    "ball",
    "bricks",
    "paddle",
    "powerups",
    "score",
    "color_choices",
    "screen_size",
]
