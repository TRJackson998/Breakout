"""
Ball
====
Defines the ball's movement, physics, and collision interactions with the paddle, bricks, and walls. 
Tracks remaining lives and resets position when necessary.

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

from breakout import sound
from breakout.paddle import Paddle

# pylint: disable=no-member


@dataclass
class BallConfig:
    """Configuration for Ball constants."""

    radius = 10
    default_speed = 2.5
    max_speed = 5.0
    initial_x = 250
    initial_y = 380
    color = pygame.Color("white")


class Ball(Sprite):
    """Ball class - Characteristics and behavior of the ball."""

    def __init__(
        self,
        *groups,
        x_position=BallConfig.initial_x,
        y_position=BallConfig.initial_y,
        speed_y=-BallConfig.default_speed,
        radius=BallConfig.radius,
        color=BallConfig.color,
    ):
        """
        Initialize the ball.
        Args:
            groups: Sprite groups to add the ball to.
            color: The color of the ball.
        """
        super().__init__(*groups)
        self.x_position = x_position
        self.y_position = y_position
        self.radius = radius
        self.color = color

        # Initialize lives and state
        self.can_collide_with_paddle = True

        # Create the surface for the ball and draw a circle
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, self.color, (self.radius, self.radius), self.radius
        )

        # Configure ball properties
        self.speed_x = random.choice(
            [-BallConfig.default_speed, BallConfig.default_speed]
        )
        self.speed_y = speed_y
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def move(self, screen_size, screen_state):
        """Handles movement and collision with walls, paddle, and bricks."""
        # Update position
        self.update_position()

        # Handle collisions
        self.handle_wall_collisions(screen_size)
        for paddle in screen_state.paddle_group.sprites():
            self.handle_paddle_collision(paddle)
        points = self.handle_brick_collisions(screen_state.bricks)
        screen_state.score += points

        # Handle bottom screen collision (losing a life or ending the game)
        if self.y_position >= screen_size.height:
            group = self.groups()[0]
            if len(group.sprites()) > 1:
                # There's more balls, losing this one doesn't lose a life
                self.kill()
            else:
                screen_state.lose_life()
                # this is the only ball on the screen

        return screen_state

    def update_position(self):
        """Update the ball's position based on its speed."""
        self.x_position += self.speed_x
        self.y_position += self.speed_y
        self.rect.x = self.x_position
        self.rect.y = self.y_position

    def handle_wall_collisions(self, screen_size):
        """Handle collisions with the walls and ceiling."""
        if (
            self.x_position <= 0
            or self.x_position >= screen_size.width - self.rect.width
        ):
            self.bounce_x()
            sound.SoundManager.play_wall()
        if self.y_position <= 0:
            self.bounce_y()  # Reverse vertical movement
            sound.SoundManager.play_wall()

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if (
            self.speed_y > 0
            and self.rect.colliderect(paddle.rect)
            and self.can_collide_with_paddle
        ):
            self.bounce_y()
            sound.SoundManager.play_paddle()
            self.y_position = paddle.rect.top - self.rect.height

            # Adjust horizontal speed based on where the ball hits the paddle
            paddle_center = paddle.rect.centerx
            ball_center = self.rect.centerx
            offset = ball_center - paddle_center
            max_offset = paddle.rect.width / 2
            self.speed_x = max(
                -BallConfig.max_speed,
                min(
                    BallConfig.default_speed * (offset / max_offset),
                    BallConfig.max_speed,
                ),
            )

            self.can_collide_with_paddle = False

        if self.rect.bottom < paddle.rect.top:
            self.can_collide_with_paddle = True

    def handle_brick_collisions(self, bricks: pygame.sprite.Group) -> int:
        """Handle collisions with bricks and return points scored."""
        points = 0
        hit_bricks = pygame.sprite.spritecollide(self, bricks, False)
        reversed_x = False
        reversed_y = False

        for brick in hit_bricks:
            vertical_overlap = min(
                abs(self.rect.bottom - brick.rect.top),
                abs(self.rect.top - brick.rect.bottom),
            )
            horizontal_overlap = min(
                abs(self.rect.right - brick.rect.left),
                abs(self.rect.left - brick.rect.right),
            )

            if vertical_overlap < horizontal_overlap and not reversed_y:
                self.bounce_y()
                reversed_y = True
            elif horizontal_overlap < vertical_overlap and not reversed_x:
                self.bounce_x()
                reversed_x = True

            points += brick.hit()

            # Play sound effect for each brick hit
            sound.SoundManager.play_brick()
        return points

    def bounce_x(self):
        """Reverse the horizontal direction of the ball."""
        self.speed_x = -self.speed_x

    def bounce_y(self):
        """Reverse the vertical direction of the ball."""
        self.speed_y = -self.speed_y

    def reset_position(self):
        """Resets ball to starting position and waits for launch."""
        self.speed_x = random.choice(
            [-BallConfig.default_speed, BallConfig.default_speed]
        )
        self.speed_y = -BallConfig.default_speed
        self.x_position = BallConfig.initial_x
        self.y_position = BallConfig.initial_y
        self.rect.x = self.x_position
        self.rect.y = self.y_position
