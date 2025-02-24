"""
Powerups
========
Implement the Powerups object and related interactions/physics


Powers
------
Paddle size bigger
Extra ball
Lose a life
Gain a life

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

from breakout import Position, Speed, base_path, color_choices, screen_size, sound
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
    """A generic powerup that moves downward,
    flickers by changing its color, and triggers
    a specified power effect when collected.
    """

    def __init__(
        self,
        *groups,
        power=lambda: None,
        shape: Literal["circle", "rectangle"] = "circle",
        color: int = random.choice(list(range(len(color_choices))))
    ):
        """
        Initialize a generic powerup.

        Args:
            groups: One or more pygame.sprite.Group instances to add the powerup to.
            power: A callable to execute when the powerup is collected.
            shape: The shape of the powerup ('circle' or 'rectangle').
            color: An index into the color_choices list determining the initial color.
        """
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
        """
        Update the powerup's state: blink, update position, handle paddle collision,
        and self-destruction if it falls off-screen.
        """
        now = pygame.time.get_ticks()
        if now - self.last_toggle > PowerupConfig.blink_interval:
            self.last_toggle = now
            self.change_color()

        # Update position
        self.update_position()

        # Only collide with the last paddle in the group
        paddle = list(screen_state.paddle_group.sprites())[-1]
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
        """Handle collisions with the paddle
        If collision is detected while falling,
        trigger the powerup's effect and remove it."""
        if self.speed.y > 0 and self.rect.colliderect(paddle.rect):
            sound.SoundManager.play_powerup()
            self.collect()
            self.kill()

    def change_color(self):
        """Cycle through available colors to create a flickering effect."""
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


class ExtraLifePowerup(Sprite):
    """A powerup that gives the player an extra life.
    This powerup is uses a red_heart.png image.
    """

    def __init__(self, *groups, power=lambda: None):
        super().__init__(*groups)
        # Load the red heart image.
        try:
            heart_path = base_path.joinpath("textures", "red_heart.png")
            self.image = pygame.image.load(str(heart_path)).convert_alpha()
            # Scale to be a 20x20 heart
            self.image = pygame.transform.scale(self.image, (20, 20))
        except Exception as e:
            print("Error loading heart image:", e)
            # Will drop a transparent image
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(
            center=(random.randint(30, screen_size.width - 30), 15)
        )
        self.speed = Speed(0, 4.5)  # Falling speed
        self.collect = power

    def move(self, screen_state):
        """Move the powerup downwards and handle collision with the paddle."""
        self.rect.y += self.speed.y
        # If the powerup falls off screen, kill it
        if self.rect.top > screen_size.height:
            self.kill()
        # Check collision with the paddle.
        for paddle in screen_state.paddle_group.sprites():
            if self.rect.colliderect(paddle.rect):
                sound.SoundManager.play_powerup()
                self.collect()
                self.kill()

    def update_position(self):
        """Update the powerup's position and check if it goes off-screen."""
        self.rect.y += self.speed.y
        if self.rect.top > screen_size.height:
            self.kill()

    def handle_paddle_collision(self, paddle):
        """Call the powerup's effect if it collides with the paddle."""
        if self.rect.colliderect(paddle.rect):
            sound.SoundManager.play_powerup()
            self.collect()
            self.kill()


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
        """Check for collision with the paddle. If collided, trigger explosion."""
        if self.speed.y > 0 and self.rect.colliderect(paddle.rect):
            self.explode()

    def change_color(self):
        """Redraw flickering spark at the end of the fuse."""
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
        self.speed = Speed(0, 0)
        self.generate_explosion()

    def generate_explosion(self):
        """Trigger the explosion: stop movement, display an explosion effect,
        and update state so that after a delay the negative effect is applied."""
        size = PowerupConfig.size * 4
        outer_explosion = self.generate_explosion_points(size)
        middle_explosion = self.generate_explosion_points(size * 0.7)
        inner_explosion = self.generate_explosion_points(size * 0.4)

        pygame.draw.polygon(self.image, pygame.Color("red"), outer_explosion)
        pygame.draw.polygon(self.image, pygame.Color("orange"), middle_explosion)
        pygame.draw.polygon(self.image, pygame.Color("yellow"), inner_explosion)

    def generate_explosion_points(self, size: int) -> list[int]:
        """Generate a list of (x, y) coordinate tuples
        representing the explosion polygon vertices."""
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
