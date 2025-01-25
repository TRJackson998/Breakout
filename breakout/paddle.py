"""
Paddle
========
Implement the Paddle object and related interactions/physics
Subclass of BreakoutSprite

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


class Paddle(BreakoutSprite):
    def __init__(self, *groups, width=0, height=0):
        super().__init__(*groups)
        self.width = width
        self.height = height
