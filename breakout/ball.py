"""
Ball
====
Implement the Ball object and related interactions/physics
Subclass of BreakoutSprite

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

Developer
---------
Terrence

Last Edited
-----------
1.20.25
"""

import random
import pygame
from pygame.sprite import Sprite

# pylint: disable=no-member


class BallConfig:
    """Configuration for Ball constants."""

    RADIUS = 10
    DEFAULT_SPEED = 2.5
    MAX_SPEED = 5.0
    INITIAL_X = 250
    INITIAL_Y = 380


class Ball(Sprite):
    """Ball class - Characteristics and behavior of the ball."""

    def __init__(self, *groups, color=pygame.Color(255, 255, 255)):
        """
        Initialize the ball.
        Args:
            groups: Sprite groups to add the ball to.
            color: The color of the ball.
        """
        # Initialize lives and state
        self.lives = 2
        self.waiting_for_launch = True
        self.can_collide_with_paddle = True

        # Create the surface for the ball and draw a circle
        self.radius = BallConfig.RADIUS
        image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(image, color, (self.radius, self.radius), self.radius)

        super().__init__(
            *groups,
            x_position=BallConfig.INITIAL_X,
            y_position=BallConfig.INITIAL_Y,
            color=color,
            image=image,
            speed=BallConfig.DEFAULT_SPEED,
        )

        # Configure ball properties
        self.configure_ball()

    def configure_ball(
        self,
        x_position=BallConfig.INITIAL_X,
        y_position=BallConfig.INITIAL_Y,
        radius=None,
        speed_x=None,
        speed_y=None,
    ):
        """Configure the initial state of the ball."""
        self.radius = radius or BallConfig.RADIUS
        self.x_position = x_position
        self.y_position = y_position
        self.speed_x = speed_x or random.choice(
            [-BallConfig.DEFAULT_SPEED, BallConfig.DEFAULT_SPEED]
        )
        self.speed_y = speed_y or -BallConfig.DEFAULT_SPEED
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def move(self, screen_size, paddle, brick_group, switch_screen, Screens) -> int:
        """Handles movement and collision with walls, paddle, and bricks."""
        if self.waiting_for_launch:
            return 0

        # Update position
        self.update_position()

        # Handle collisions
        self.handle_wall_collisions(screen_size)
        self.handle_paddle_collision(paddle)
        points = self.handle_brick_collisions(brick_group)

        # Handle bottom screen collision (losing a life or ending the game)
        if self.y_position >= screen_size.height:
            if self.lives > 1:
                self.lives -= 1
                self.reset_position()
                paddle.reset_position()
            else:
                switch_screen(Screens.END)
                return 0

        return points

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
            self.bounce_y()

    def handle_paddle_collision(self, paddle):
        """Handle collision with the paddle."""
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

    def handle_brick_collisions(self, brick_group: pygame.sprite.Group) -> int:
        """Handle collisions with bricks and return points scored."""
        points = 0
        hit_bricks = pygame.sprite.spritecollide(self, brick_group, False)
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

    def reset_position(self, wait=True):
        """Resets ball to starting position and waits for launch."""
        self.configure_ball(
            x_position=BallConfig.INITIAL_X,
            y_position=BallConfig.INITIAL_Y,
            speed_x=random.choice(
                [-BallConfig.DEFAULT_SPEED, BallConfig.DEFAULT_SPEED]
            ),
            speed_y=-BallConfig.DEFAULT_SPEED,
        )
        self.waiting_for_launch = wait
