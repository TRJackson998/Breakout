"""
Powerups
========
Implement the Powerups object and related interactions/physics
Subclass of BreakoutSprite

Powers
------
Paddle size bigger
Extra ball
Lose a life

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

import math
import random
from dataclasses import dataclass
from typing import Literal

import pygame
from pygame.font import SysFont
from pygame.sprite import Sprite

from breakout import Position, Speed, color_choices, screen_size, sound
from breakout.paddle import Paddle

# pylint: disable=no-member


@dataclass
class PowerupConfig:
    """Configuration for Powerup constants."""

    size = 10
    default_speed = 2.5
    blink_interval = 100
    font = SysFont("courier", max(screen_size.width // 30, 14))


class PowerUp(Sprite):
    """Handle power up execution"""

    def __init__(
        self,
        *groups,
        power=lambda: None,
        shape: Literal["circle", "rectangle"] = "circle",
        size: int = PowerupConfig.size,
        color: int = random.choice([i for i in range(len(color_choices))])
    ):
        super().__init__(*groups)
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
        self.text_surface = PowerupConfig.font.render("+", True, pygame.Color("black"))
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
            sound.SoundManager.play_powerup()
            self.collect()
            self.kill()

        if self.rect.bottom < paddle.rect.top:
            self.can_collide_with_paddle = True

    def change_color(self):
        """Handles the power up color changes"""
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
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))
        self.text_surface = PowerupConfig.font.render("+", True, pygame.Color("black"))
        text_rect = self.text_surface.get_rect(
            center=(self.size, self.size)
        )  # Center text
        self.image.blit(self.text_surface, text_rect)  # Draw text onto self.image


class PowerDown(Sprite):
    def __init__(self, *groups, power=lambda: None):
        super().__init__(*groups)
        self.x_position = random.randint(
            PowerupConfig.size * 5, screen_size.width - PowerupConfig.size * 5
        )
        self.y_position = 15
        self.speed_x = 0
        self.radius = PowerupConfig.size
        self.speed_y = PowerupConfig.default_speed
        self.collect = power
        self.blink_interval = PowerupConfig.blink_interval
        self.last_toggle = pygame.time.get_ticks()
        self.exploded = False
        self.explode_time = 0

        # Draw bomb body (shaded)
        self.image = pygame.Surface((self.radius * 6, self.radius * 6), pygame.SRCALPHA)

        pygame.draw.circle(
            self.image,
            pygame.Color("dark gray"),
            (self.radius * 3, self.radius * 3),
            self.radius,
        )  # Outline
        pygame.draw.circle(
            self.image,
            pygame.Color("black"),
            (self.radius * 3, self.radius * 3),
            self.radius // 1.25,
        )  # Main body
        pygame.draw.circle(
            self.image,
            pygame.Color("white"),
            (self.radius * 3 - 2.25, self.radius * 3 - 2.25),
            self.radius // 2.25,
        )  # Highlight

        # Draw fuse
        fuse_start = (self.radius * 3, self.radius * 2)
        self.fuse_end = (self.radius * 3.5, self.radius)
        pygame.draw.line(
            self.image, pygame.Color("dark gray"), fuse_start, self.fuse_end, 3
        )

        # Flickering spark at the end of the fuse
        fuse_color = random.choice(
            [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow")]
        )  # Simulates flickering
        pygame.draw.circle(self.image, fuse_color, self.fuse_end, self.radius // 2.5)

        # I want the collide rectangle to be smaller
        self.rect = pygame.Surface(
            (self.radius * 4, self.radius * 4), pygame.SRCALPHA
        ).get_rect(center=(self.x_position, self.y_position))

    def move(self, screen_state):
        """Handles movement and collision with walls, paddle, and bricks."""
        now = pygame.time.get_ticks()
        if self.exploded:
            if (self.explode_time + (self.blink_interval * 4)) < now:
                self.collect()
                self.kill()
        else:
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

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if self.speed_y > 0 and self.rect.colliderect(paddle.rect):
            self.explode()

    def change_color(self):
        """Redraw flickering spark at the end of the fuse"""
        fuse_color = random.choice(
            [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow")]
        )  # Simulates flickering
        pygame.draw.circle(self.image, fuse_color, self.fuse_end, self.radius // 2.5)

    def explode(self):
        self.exploded = True
        self.explode_time = pygame.time.get_ticks()
        self.speed_y = 0
        self.generate_explosion()

    def generate_explosion(self):
        size = self.radius * 4
        outer_explosion = self.generate_explosion_points(size)
        middle_explosion = self.generate_explosion_points(size * 0.7)
        inner_explosion = self.generate_explosion_points(size * 0.4)

        pygame.draw.polygon(self.image, pygame.Color("red"), outer_explosion)
        pygame.draw.polygon(self.image, pygame.Color("orange"), middle_explosion)
        pygame.draw.polygon(self.image, pygame.Color("yellow"), inner_explosion)

    def generate_explosion_points(self, size: int) -> list[int]:
        points = []
        num_spikes = 12
        angle_step = 360 / num_spikes

        for i in range(num_spikes):
            angle = i * angle_step
            radius = size // 2 if i % 2 == 0 else size // 4  # Alternating spike sizes
            x = self.radius * 3 - int(
                radius * random.uniform(0.8, 1.2) * math.cos(math.radians(angle))
            )
            y = self.radius * 3 - int(
                radius * random.uniform(0.8, 1.2) * math.sin(math.radians(angle))
            )
            points.append((x, y))

        return points
