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

from dataclasses import astuple, dataclass

import pygame
from pygame.sprite import Sprite

from breakout import Position, Size, Speed, screen_size


@dataclass
class PaddleConfig:
    """Configuration for Paddle constants."""

    size = Size(100, 25)
    initial_position = Position(200, 485)
    speed = Speed(5, 0)
    blink_interval = 600  # in milliseconds
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
        """
        Initialize the paddle.

        Args:
            groups: One or more pygame.sprite.Group instances to add the paddle to.
            color: The paddle's color. Defaults to white.
            x_position: Optional x-coordinate for the paddle.
                If None, uses PaddleConfig's initial position.
            width: Optional width for the paddle. If None, uses PaddleConfig's default width.
            timeout: If set, the paddle disappears after 'timeout' milliseconds (used for powerups).
        """
        super().__init__(
            *groups,
        )
        self.size = Size(
            width if width else PaddleConfig.size.width, PaddleConfig.size.height
        )
        self.position = Position(
            x_position if x_position else PaddleConfig.initial_position.x,
            PaddleConfig.initial_position.y,
        )
        self.color = color
        self.speed = PaddleConfig.speed
        self.timeout = timeout
        self.last_toggle = pygame.time.get_ticks()

        # Create the paddle surface
        self.image = pygame.Surface(astuple(self.size))
        self.image.fill(self.color)

        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=astuple(self.position))

    def reset_position(self):
        """Reset the paddle to its initial position."""
        self.image = pygame.Surface(astuple(self.size))
        self.position.x = PaddleConfig.initial_position.x
        self.image.fill(self.color)
        self.rect = self.image.get_rect(
            topleft=(PaddleConfig.initial_position.x, PaddleConfig.initial_position.y)
        )

    def move_left(self):
        """Move the paddle to the left"""
        self.position -= self.speed
        self.position.x = max(
            0, min(screen_size.width - self.rect.width, self.position.x)
        )
        self.rect.x = self.position.x

    def move_right(self):
        """Move the paddle to the right"""
        self.position += self.speed
        self.position.x = max(
            0, min(screen_size.width - self.rect.width, self.position.x)
        )
        self.rect.x = self.position.x

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
