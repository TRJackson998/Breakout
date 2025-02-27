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
from dataclasses import astuple, dataclass

import pygame
from pygame.sprite import Sprite

from breakout import Position, Speed, screen_size
from breakout.bricks import Brick
from breakout.paddle import Paddle
from breakout.sound import SoundManager

# pylint: disable=no-member


@dataclass
class BallConfig:
    """Configuration for Ball constants."""

    radius = 10
    default_speed = 4.0
    max_speed = 5.0
    initial_position = Position(250, 475)
    color = pygame.Color("white")


class Ball(Sprite):
    """Ball class - Characteristics and behavior of the ball."""

    def __init__(
        self,
        *groups,
        position: Position = BallConfig.initial_position,
        radius=BallConfig.radius,
        color: pygame.Color = BallConfig.color,
        speed: Speed = None
    ):
        """
        Initialize the ball.

        Args:
            groups: One or more pygame.sprite.Group instances to add the ball to.
            position: Starting Position of the ball.
            radius: Radius of the ball.
            color: The ball's color.
            speed: A Speed object for the ball's velocity.
            If None, a default random direction is used.
        """
        super().__init__(*groups)
        self.position = position
        self.radius = radius
        self.color = color

        # Create the surface for the ball and draw a circle
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, self.color, (self.radius, self.radius), self.radius
        )

        # Configure ball properties
        self.speed = (
            speed
            if speed
            else Speed(
                0,
                -BallConfig.default_speed,
            )
        )
        self.rect = self.image.get_rect(center=astuple(self.position))

    def increase_speed(self, speed=None):
        """Increase the ball's current speed by a factor without exceeding max_speed."""
        if not speed:
            factor = 1.5
            BallConfig.default_speed = min(
                BallConfig.default_speed * factor, BallConfig.max_speed
            )

            if self.speed.y == 0:
                self.speed.y = min(
                    -BallConfig.default_speed * factor, BallConfig.max_speed
                )
            else:
                self.speed.y = min(self.speed.y * factor, BallConfig.max_speed)
        else:
            self.speed.y = speed
            BallConfig.default_speed = speed
        self.speed.x = 0

    def move(self, screen_state):
        """
        Handles movement and collision with walls, paddle, and bricks.

        Args:
            screen_state: The current game state (including score, lives, etc.).

        Returns the updated screen_state after handling collisions and possible life loss.
        """
        # Update position
        self.update_position()

        # Handle collisions
        self.handle_wall_collisions()

        # only interact with the last paddle, in case of powerup paddle
        paddle = screen_state.paddle_group.sprites()[-1]
        self.handle_paddle_collision(paddle)

        points = self.handle_brick_collisions(screen_state.bricks)
        screen_state.score += points

        # Handle bottom screen collision (losing a life or ending the game)
        if self.position.y >= screen_size.height:
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
        self.position += self.speed
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def handle_wall_collisions(self):
        """Handle collisions with the walls and ceiling."""
        if (
            self.position.x <= 0
            or self.position.x >= screen_size.width - self.rect.width
        ):
            self.bounce_x()
            SoundManager.play_wall()
        if self.position.y <= 0:
            self.bounce_y()  # Reverse vertical movement
            SoundManager.play_wall()

    def handle_paddle_collision(self, paddle: Paddle):
        """Handle collisions with the paddle"""
        if self.speed.y > 0 and self.rect.clipline(
            paddle.rect.topleft, paddle.rect.topright
        ):
            self.bounce_y()
            SoundManager.play_paddle()
            self.position.y = paddle.rect.top - self.rect.height

            # Adjust horizontal speed based on where the ball hits the paddle
            paddle_center = paddle.rect.centerx
            ball_center = self.rect.centerx
            offset = ball_center - paddle_center
            max_offset = paddle.rect.width / 2
            self.speed.x = max(
                -BallConfig.max_speed,
                min(
                    BallConfig.default_speed * (offset / max_offset),
                    BallConfig.max_speed,
                ),
            )
        elif self.speed.y > 0 and (
            self.rect.clipline(paddle.rect.topleft, paddle.rect.bottomleft)
            or self.rect.clipline(paddle.rect.topright, paddle.rect.bottomright)
        ):
            self.bounce_x()
            SoundManager.play_paddle()

    def handle_brick_collisions(self, bricks: pygame.sprite.Group) -> int:
        """Handle collisions with bricks and return points scored."""
        points = 0
        hit_bricks = pygame.sprite.spritecollide(self, bricks, False)
        reversed_x = False
        reversed_y = False

        for brick in hit_bricks:
            brick: Brick
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
            SoundManager.play_brick()
        return points

    def bounce_x(self):
        """Reverse the horizontal direction of the ball."""
        if self.speed.x == 0:
            self.speed.x = random.choice([-self.speed.x, self.speed.x])
        else:
            self.speed.x *= -1
        self.update_position()

    def bounce_y(self):
        """Reverse the vertical direction of the ball."""
        self.speed.y *= -1
        self.update_position()

    def reset_position(self):
        """Resets ball to starting position and waits for launch."""
        self.speed = Speed(0, -self.speed.y)
        self.position = BallConfig.initial_position
        self.rect.center = astuple(self.position)
