"""
Paddle
========
Implements the player's paddle, allowing movement based on user input. 
Handles collisions with the ball and resets position when needed.

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

"""

import pygame

from breakout import screen_size
from breakout.sprite import BreakoutSprite


class Paddle(BreakoutSprite):
    """Carries all of the characteristics of the paddle"""

    WIDTH = screen_size.width // 5
    HEIGHT = screen_size.height // 25

    def __init__(
        self,
        *groups,
        color=pygame.Color(255, 255, 255),
        x_position=screen_size.width // 2.5,
        y_position=screen_size.height // 1.25,
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

        # Store the initial position for later resets
        self.initial_position = (self.x_position, self.y_position)

    def reset_position(self):
        """Reset the paddle to its initial position."""
        self.x_position, self.y_position = self.initial_position
        self.rect.topleft = self.initial_position

    def move_left(self):
        """Move the paddle to the left"""
        new_x = self.x_position - self.speed
        self.x_position = max(0, min(screen_size.width - self.rect.width, new_x))
        self.rect.x = self.x_position

    def move_right(self):
        """Move the paddle to the right"""
        new_x = self.x_position + self.speed
        self.x_position = max(0, min(screen_size.width - self.rect.width, new_x))
        self.rect.x = self.x_position
