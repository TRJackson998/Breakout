"""
Sprite
======
Abstract Base Class implementing the pygame Sprite class
to include basic movement and collision functions
for subclasses ball, paddle, etc

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

from abc import ABC

from pygame import Color
from pygame.sprite import Sprite


class BreakoutSprite(Sprite, ABC):
    """Implementation of the pygame Sprite object with movement functionality"""

    def __init__(
        self,
        *groups,
        speed: int = 0,
        x_position: int = 0,
        y_position: int = 0,
        color: Color = Color(0, 0, 0),
        image
    ):
        super().__init__(*groups)
        self.speed = speed
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.image = image

    def move_up(self):
        """Move the sprite up"""
        pass

    def move_down(self):
        """Move the sprite down"""
        pass

    def move_left(self):
        """Move the sprite left"""
        pass

    def move_right(self):
        """Move the sprite right"""
        pass

    def appear(self):
        """Make the sprite appear on the screen"""
        if self.image is not None:
            self.image.fill(self.color)

    def disappear(self):
        """Make the sprite disappear from the screen"""
        self.kill()
