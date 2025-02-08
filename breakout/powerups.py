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
from typing import Literal

import pygame
from pygame.font import SysFont
from pygame.sprite import Sprite

from breakout import color_choices, screen_size
from breakout.paddle import Paddle

# pylint: disable=no-member


@dataclass
class PowerupConfig:
    """Configuration for Powerup constants."""

    size = 10
    default_speed = 2.5
    blink_interval = 100


class PowerUp(Sprite):
    """Handle power up execution"""

    def __init__(
        self,
        *groups,
        power,
        shape: Literal["circle", "rectangle"] = "circle",
        size=PowerupConfig.size,
        color=random.choice([i for i in range(len(color_choices))])
    ):
        super().__init__(*groups)
        self.font = SysFont("courier", max(screen_size.width // 30, 14))
        self.x_position = random.randint(
            PowerupConfig.size * 5, screen_size.width - PowerupConfig.size * 5
        )
        self.y_position = 15
        self.speed_x = 0
        self.speed_y = PowerupConfig.default_speed
        self.size = size
        self.color = color
        self.collect = power
        self.can_collide_with_paddle = True
        self.shape = shape
        self.blink_interval = PowerupConfig.blink_interval
        self.last_toggle = pygame.time.get_ticks()

        if self.shape == "circle":
            # Create the surface for the ball and draw a circle
            self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                self.image,
                color_choices[self.color],
                (self.size, self.size),
                self.size,
            )
        elif self.shape == "rectangle":
            # Create the surface for the ball and draw a circle
            self.image = pygame.Surface((self.size * 4, self.size * 2))
            self.image.fill(color)
        self.text_surface = self.font.render("+", True, pygame.Color("black"))
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))
        text_rect = self.text_surface.get_rect(
            center=(self.size, self.size)
        )  # Center text
        self.image.blit(self.text_surface, text_rect)  # Draw text onto self.image

    def move(self, screen_state):
        """Handles movement and collision with walls, paddle, and bricks."""
        now = pygame.time.get_ticks()
        if now - self.last_toggle > self.blink_interval:
            self.last_toggle = now
            self.change_color()

        # Update position
        self.update_position()
        for paddle in screen_state.paddle_group.sprites():
            self.handle_paddle_collision(paddle)
        if self.y_position >= screen_size.height:
            self.kill()

    def update_position(self):
        """Update the powerup's position based on its speed."""
        self.y_position += self.speed_y
        self.rect.y = self.y_position

        text_rect = self.text_surface.get_rect(
            center=(self.x_position, self.y_position)
        )  # center text
        self.image.blit(self.text_surface, text_rect)  # Draw text onto self.image

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if (
            self.speed_y > 0
            and self.rect.colliderect(paddle.rect)
            and self.can_collide_with_paddle
        ):
            self.collect()
            self.kill()

        if self.rect.bottom < paddle.rect.top:
            self.can_collide_with_paddle = True

    def change_color(self):
        self.color += 1
        if self.color == len(color_choices):
            self.color = 0
        if self.shape == "circle":
            # Create the surface for the ball and draw a circle
            self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                self.image,
                color_choices[self.color],
                (self.size, self.size),
                self.size,
            )
        elif self.shape == "rectangle":
            # Create the surface for the ball and draw a circle
            self.image = pygame.Surface((self.size * 4, self.size * 2))
            self.image.fill(color_choices[self.color])
        self.text_surface = self.font.render("+", True, pygame.Color("black"))
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))
        text_rect = self.text_surface.get_rect(
            center=(self.size, self.size)
        )  # Center text
        self.image.blit(self.text_surface, text_rect)  # Draw text onto self.image
