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

from dataclasses import dataclass

import pygame
from pygame.sprite import Sprite

from breakout import screen_size


@dataclass
class PaddleConfig:
    """Configuration for Ball constants."""

    width = screen_size.width // 5
    height = screen_size.height // 25
    initial_x = screen_size.width // 2.5
    initial_y = screen_size.height // 1.25
    speed = 5
    blink_interval = 600
    flicker_color = pygame.Color("black")


class Paddle(Sprite):
    """Carries all of the characteristics of the paddle"""

    def __init__(
        self,
        *groups,
        color: pygame.Color = pygame.Color("white"),
        x_position: int = None,
        width: int = None,
        timeout: int = None
    ):
        super().__init__(
            *groups,
        )
        self.width = width if width else PaddleConfig.width
        self.height = PaddleConfig.height
        self.x_position = x_position if x_position else PaddleConfig.initial_x
        self.y_position = PaddleConfig.initial_y
        self.color = color
        self.speed = PaddleConfig.speed
        self.timeout = timeout
        self.last_toggle = pygame.time.get_ticks()

        # Create the paddle surface
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)

        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.x_position, self.y_position))

    def reset_position(self):
        """Reset the paddle to its initial position."""
        self.image = pygame.Surface((self.width, self.height))
        self.x_position = PaddleConfig.initial_x
        self.image.fill(self.color)
        self.rect = self.image.get_rect(
            topleft=(PaddleConfig.initial_x, PaddleConfig.initial_y)
        )

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
        """Paddle powerups are temporary and should flicker out"""
        now = pygame.time.get_ticks()
        if now - self.last_toggle > PaddleConfig.blink_interval:
            # if it's time to toggle
            current_color = self.image.get_at((0, 0))  # check what color we are
            # switch to the other color
            if current_color == self.color:
                self.image.fill(PaddleConfig.flicker_color)
            else:
                self.image.fill(self.color)

            # we just toggled
            self.last_toggle = now
            PaddleConfig.blink_interval /= 1.25  # speed up the flickering

    def check_timeout(self, time: int):
        """Check if it's time for a temp paddle to die or change color"""
        if time >= self.timeout:
            self.kill()
        elif time >= self.timeout - (3 * 1000):
            # in the last 3 seconds of its life, flicker out
            self.change_color()
