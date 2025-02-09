"""
Paddle
========
Implements the player's paddle, allowing movement based on user input. 
Handles collisions with the ball and resets position when needed.

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
from pygame.sprite import Sprite

from breakout import screen_size


class Paddle(Sprite):
    """Carries all of the characteristics of the paddle"""

    width = screen_size.width // 5
    height = screen_size.height // 25

    def __init__(
        self,
        *groups,
        color=pygame.Color("white"),
        x_position=screen_size.width // 2.5,
        y_position=screen_size.height // 1.25,
        speed=5,
        width=None,
        timeout=None
    ):
        super().__init__(
            *groups,
        )
        self.width = width if width else Paddle.width
        self.height = Paddle.height
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.flicker_color = pygame.Color("black")
        self.speed = speed
        self.timeout = timeout
        self.last_toggle = pygame.time.get_ticks()
        self.blink_interval = 600

        # Create the paddle surface
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)

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

    def change_color(self):
        now = pygame.time.get_ticks()
        if now - self.last_toggle > self.blink_interval:
            current_color = self.image.get_at((0, 0))
            if current_color == self.color:
                self.image.fill(self.flicker_color)
            else:
                self.image.fill(self.color)
            self.last_toggle = now
            self.blink_interval /= 1.25
