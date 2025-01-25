"""
Brick
=====
Implement the Brick object and related interactions/physics
Subclass of BreakoutSprite
Should be added to a group of sprites to represent the overall level, use spritecollide

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

from breakout.sprite import BreakoutSprite


class Brick(BreakoutSprite):
    def __init__(self, *groups, width=0, height=0):
        super().__init__(*groups)
        self.width = width
        self.height = height
