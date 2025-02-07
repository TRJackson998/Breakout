"""
Powerups
========
Implement the Powerups object and related interactions/physics
Subclass of BreakoutSprite

Powers
------
Paddle size bigger
Ball size bigger
Paddle speed faster
Ball speed slower
Extra paddle
Extra ball
Extra life

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

import random
from dataclasses import dataclass

import pygame
from pygame.sprite import Sprite

from breakout import screen_size
from breakout.paddle import Paddle

# pylint: disable=no-member


@dataclass
class PowerupConfig:
    """Configuration for Powerup constants."""

    radius = 10
    default_speed = 2.5
    max_speed = 5.0
    color = pygame.Color("red")


class PowerUp(Sprite):
    """Handle power up execution"""

    def __init__(
        self, *groups, power, radius=PowerupConfig.radius, color=PowerupConfig.color
    ):
        super().__init__(*groups)
        self.x_position = random.randint(0, screen_size.width)
        self.y_position = 15
        self.speed_x = 0
        self.speed_y = PowerupConfig.default_speed
        self.radius = radius
        self.color = color
        self.collect = power
        self.can_collide_with_paddle = True

        # Create the surface for the ball and draw a circle
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, self.color, (self.radius, self.radius), self.radius
        )
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def move(self, screen_state):
        """Handles movement and collision with walls, paddle, and bricks."""
        # Update position
        self.update_position()
        self.handle_paddle_collision(screen_state.paddle)
        if self.y_position >= screen_size.height:
            self.kill()

    def update_position(self):
        """Update the powerup's position based on its speed."""
        self.y_position += self.speed_y
        self.rect.y = self.y_position

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if (
            self.speed_y > 0
            and self.rect.colliderect(paddle.rect)
            and self.can_collide_with_paddle
        ):
            self.kill()
            self.collect()

        if self.rect.bottom < paddle.rect.top:
            self.can_collide_with_paddle = True
