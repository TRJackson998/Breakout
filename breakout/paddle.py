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

from breakout.sprite import BreakoutSprite


class Paddle(BreakoutSprite):
    """Carries all of the characteristics of the paddle"""

    WIDTH = 100
    HEIGHT = 20

    def __init__(
        self,
        *groups,
        color=pygame.Color(255, 255, 255),
        x_position=200,
        y_position=400,
        speed=5
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
            speed=speed
        )

        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.x_position, self.y_position))
