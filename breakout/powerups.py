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
from dataclasses import astuple, dataclass
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
    default_speed = Speed(0, 2.5)
    initial_y = 15
    blink_interval = 100
    font = SysFont("courier", max(screen_size.width // 30, 14))


class PowerUp(Sprite):
    """Handle power up execution"""

    def __init__(
        self,
        *groups,
        power=lambda: None,
        shape: Literal["circle", "rectangle"] = "circle",
        color: int = random.choice(list(range(len(color_choices))))
    ):
        super().__init__(*groups)
        self.position = Position(
            random.randint(
                PowerupConfig.size * 5, screen_size.width - PowerupConfig.size * 5
            ),
            PowerupConfig.initial_y,
        )
        self.speed = PowerupConfig.default_speed
        self.color = color
        self.collect = power
        self.shape = shape
        self.last_toggle = pygame.time.get_ticks()

        if self.shape == "circle":
            # Create the surface for the ball and draw a circle
            self.image = pygame.Surface(
                (PowerupConfig.size * 2, PowerupConfig.size * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                self.image,
                color_choices[self.color],
                (PowerupConfig.size, PowerupConfig.size),
                PowerupConfig.size,
            )
        elif self.shape == "rectangle":
            # Create the surface for the ball and draw a circle
            self.image = pygame.Surface(
                (PowerupConfig.size * 4, PowerupConfig.size * 2)
            )
            self.image.fill(color)
        self.text_surface = PowerupConfig.font.render("+", True, pygame.Color("black"))
        self.rect = self.image.get_rect(center=astuple(self.position))
        text_rect = self.text_surface.get_rect(
            center=(PowerupConfig.size, PowerupConfig.size)
        )  # Center text
        self.image.blit(self.text_surface, text_rect)  # Draw text onto self.image

    def move(self, screen_state):
        """Handles movement and collision with walls, paddle, and bricks."""
        now = pygame.time.get_ticks()
        if now - self.last_toggle > PowerupConfig.blink_interval:
            self.last_toggle = now
            self.change_color()

        # Update position
        self.update_position()
        for paddle in screen_state.paddle_group.sprites():
            self.handle_paddle_collision(paddle)
        if self.position.y >= screen_size.height:
            self.kill()

    def update_position(self):
        """Update the powerup's position based on its speed."""
        self.position += self.speed
        self.rect.y = self.position.y

        text_rect = self.text_surface.get_rect(
            center=astuple(self.position)
        )  # center text
        self.image.blit(self.text_surface, text_rect)  # Draw text onto self.image

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if self.speed.y > 0 and self.rect.colliderect(paddle.rect):
            sound.SoundManager.play_powerup()
            self.collect()
            self.kill()

    def change_color(self):
        """Handles the power up color changes"""
        self.color += 1
        if self.color == len(color_choices):
            self.color = 0
        if self.shape == "circle":
            # Redraw the circle in the new color
            pygame.draw.circle(
                self.image,
                color_choices[self.color],
                (PowerupConfig.size, PowerupConfig.size),
                PowerupConfig.size,
            )
        elif self.shape == "rectangle":
            # Redraw the rectangle in the new color
            self.image.fill(color_choices[self.color])
        self.text_surface = PowerupConfig.font.render("+", True, pygame.Color("black"))
        self.rect = self.image.get_rect(center=astuple(self.position))
        text_rect = self.text_surface.get_rect(
            center=(PowerupConfig.size, PowerupConfig.size)
        )  # Center text
        self.image.blit(self.text_surface, text_rect)  # Draw text onto self.image


class PowerDown(Sprite):
    """An obstacle that causes the player to lose a life"""

    def __init__(self, *groups, power=lambda: None):
        super().__init__(*groups)
        self.position = Position(
            random.randint(
                PowerupConfig.size * 5, screen_size.width - PowerupConfig.size * 5
            ),
            PowerupConfig.initial_y,
        )
        self.speed = PowerupConfig.default_speed
        self.collect = power
        self.last_toggle = pygame.time.get_ticks()
        self.exploded = False
        self.explode_time = 0

        # Draw bomb body (shaded)
        self.image = pygame.Surface(
            (PowerupConfig.size * 6, PowerupConfig.size * 6), pygame.SRCALPHA
        )

        pygame.draw.circle(
            self.image,
            pygame.Color("dark gray"),
            (PowerupConfig.size * 3, PowerupConfig.size * 3),
            PowerupConfig.size,
        )  # Outline
        pygame.draw.circle(
            self.image,
            pygame.Color("black"),
            (PowerupConfig.size * 3, PowerupConfig.size * 3),
            PowerupConfig.size // 1.25,
        )  # Main body
        pygame.draw.circle(
            self.image,
            pygame.Color("white"),
            (PowerupConfig.size * 3 - 2.25, PowerupConfig.size * 3 - 2.25),
            PowerupConfig.size // 2.25,
        )  # Highlight

        # Draw fuse
        fuse_start = (PowerupConfig.size * 3, PowerupConfig.size * 2)
        self.fuse_end = (PowerupConfig.size * 3.5, PowerupConfig.size)
        pygame.draw.line(
            self.image, pygame.Color("dark gray"), fuse_start, self.fuse_end, 3
        )

        # Flickering spark at the end of the fuse
        fuse_color = random.choice(
            [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow")]
        )  # Simulates flickering
        pygame.draw.circle(
            self.image, fuse_color, self.fuse_end, PowerupConfig.size // 2.5
        )

        # I want the collide rectangle to be smaller
        self.rect = pygame.Surface(
            (PowerupConfig.size * 4, PowerupConfig.size * 4), pygame.SRCALPHA
        ).get_rect(center=astuple(self.position))

    def move(self, screen_state):
        """Handles movement and collision with walls, paddle, and bricks."""
        now = pygame.time.get_ticks()
        if self.exploded:
            if (self.explode_time + (PowerupConfig.blink_interval * 4)) < now:
                self.collect()
                self.kill()
        else:
            if now - self.last_toggle > PowerupConfig.blink_interval:
                self.last_toggle = now
                self.change_color()

        # Update position
        self.update_position()
        for paddle in screen_state.paddle_group.sprites():
            self.handle_paddle_collision(paddle)
        if self.position.y >= screen_size.height:
            self.kill()

    def update_position(self):
        """Update the powerup's position based on its speed."""
        self.position += self.speed
        self.rect.y = self.position.y

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if self.speed.y > 0 and self.rect.colliderect(paddle.rect):
            self.explode()

    def change_color(self):
        """Redraw flickering spark at the end of the fuse"""
        fuse_color = random.choice(
            [pygame.Color("red"), pygame.Color("orange"), pygame.Color("yellow")]
        )  # Simulates flickering
        pygame.draw.circle(
            self.image, fuse_color, self.fuse_end, PowerupConfig.size // 2.5
        )

    def explode(self):
        """Update the powerdown because the player hit it"""
        self.exploded = True
        self.explode_time = pygame.time.get_ticks()
        self.speed.y = 0
        self.generate_explosion()

    def generate_explosion(self):
        """Create the graphics for the explosion"""
        size = PowerupConfig.size * 4
        outer_explosion = self.generate_explosion_points(size)
        middle_explosion = self.generate_explosion_points(size * 0.7)
        inner_explosion = self.generate_explosion_points(size * 0.4)

        pygame.draw.polygon(self.image, pygame.Color("red"), outer_explosion)
        pygame.draw.polygon(self.image, pygame.Color("orange"), middle_explosion)
        pygame.draw.polygon(self.image, pygame.Color("yellow"), inner_explosion)

    def generate_explosion_points(self, size: int) -> list[int]:
        """Do the math to generate the points on the screen for each explosion layer"""
        points = []
        num_spikes = 12
        angle_step = 360 / num_spikes

        for i in range(num_spikes):
            angle = i * angle_step
            radius = size // 2 if i % 2 == 0 else size // 4  # Alternating spike sizes
            x = PowerupConfig.size * 3 - int(
                radius * random.uniform(0.8, 1.2) * math.cos(math.radians(angle))
            )
            y = PowerupConfig.size * 3 - int(
                radius * random.uniform(0.8, 1.2) * math.sin(math.radians(angle))
            )
            points.append((x, y))

        return points
