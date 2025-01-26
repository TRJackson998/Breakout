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

import pygame

from breakout import screen_size
from breakout.sprite import BreakoutSprite


class Paddle(BreakoutSprite):
    """Carries all of the characteristics of the paddle"""

    WIDTH = 100
    HEIGHT = 20
    SPEED = 5

    def __init__(
        self, *groups, color=pygame.Color(255, 255, 255), x_position=200, y_position=400
    ):

        # Create the paddle surface
        image = pygame.Surface((self.WIDTH, self.HEIGHT))
        image.fill(color)

        super().__init__(
            *groups,
            x_position=x_position,
            y_position=y_position,
            color=color,
            image=image,
            speed=self.SPEED
        )

        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.x_position, self.y_position))

    def move_left(self):
        """Move the paddle to the left"""
        self.move_horizontal(direction=-1, screen_width=screen_size[0])

    def move_right(self):
        """Move the paddle to the right"""
        self.move_horizontal(direction=1, screen_width=screen_size[0])
