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

from breakout.paddle import Paddle

# pylint: disable=no-member


@dataclass
class BallConfig:
    """Configuration for Ball constants."""

    radius = 10
    DEFAULT_SPEED = 2.5
    MAX_SPEED = 5.0
    INITIAL_X = 250
    INITIAL_Y = 380
    COLOR = pygame.Color("white")


class Ball(Sprite):
    """Ball class - Characteristics and behavior of the ball."""

    def __init__(
        self,
        *groups,
        x_position=BallConfig.INITIAL_X,
        y_position=BallConfig.INITIAL_Y,
        radius=BallConfig.radius,
        color=BallConfig.COLOR,
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
            [-BallConfig.DEFAULT_SPEED, BallConfig.DEFAULT_SPEED]
        )
        self.speed_y = -BallConfig.DEFAULT_SPEED
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def move(self, screen_size, screen_state):
        """Handles movement and collision with walls, paddle, and bricks."""
        # Update position
        self.update_position()

        # Handle collisions
        self.handle_wall_collisions(screen_size)
        self.handle_paddle_collision(screen_state.paddle)
        points = self.handle_brick_collisions(screen_state.bricks)
        screen_state.score += points

        # Handle bottom screen collision (losing a life or ending the game)
        if self.y_position >= screen_size.height:
            group = self.groups()[0]
            if len(group.sprites()) > 1:
                # There's more balls, losing this one doesn't lose a life
                self.kill()
            else:
                # this is the only ball on the screen
                if screen_state.lives > 1:
                    screen_state.lives -= 1
                    self.reset_position()
                    screen_state.launched = False
                    screen_state.paddle.reset_position()
                else:
                    screen_state.lives -= 1
                    screen_state.game_over = True  # End Game

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
        if self.y_position <= 0:
            self.bounce_y()  # Reverse vertical movement

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if (
            self.speed_y > 0
            and self.rect.colliderect(paddle.rect)
            and self.can_collide_with_paddle
        ):
            self.bounce_y()
            self.y_position = paddle.rect.top - self.rect.height

            # Adjust horizontal speed based on where the ball hits the paddle
            paddle_center = paddle.rect.centerx
            ball_center = self.rect.centerx
            offset = ball_center - paddle_center
            max_offset = paddle.rect.width / 2
            self.speed_x = max(
                -BallConfig.MAX_SPEED,
                min(
                    BallConfig.DEFAULT_SPEED * (offset / max_offset),
                    BallConfig.MAX_SPEED,
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
            [-BallConfig.DEFAULT_SPEED, BallConfig.DEFAULT_SPEED]
        )
        self.speed_y = -BallConfig.DEFAULT_SPEED
        self.x_position = BallConfig.INITIAL_X
        self.y_position = BallConfig.INITIAL_Y
        self.rect.x = self.x_position
        self.rect.y = self.y_position
