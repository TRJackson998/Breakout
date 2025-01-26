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

Developer
---------
Terrence

Last Edited
-----------
1.20.25
"""

from dataclasses import dataclass

import pygame


@dataclass
class Size:
    """Dataclass to store sizes for easy access"""

    width: int
    height: int


pygame.init()
screen_size = Size(500, 500)

__all__ = ["ball", "bricks", "paddle", "powerups", "score", "sprite", "screen_size"]
