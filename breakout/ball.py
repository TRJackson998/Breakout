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

import pygame
from pygame.sprite import Sprite

from breakout.paddle import Paddle

# pylint: disable=no-member


class Ball(Sprite):
    """Ball class - Characteristics and behavior of the ball"""

    DEFAULT_RADIUS = 10
    DEFAULT_SPEED = 2.5
    MAX_SPEED = 5.0  # Maximum horizontal speed allowed

    def __init__(
        self,
        *groups,
        color=pygame.Color("white"),
        x_position=250,
        y_position=390,
        radius=None,
        speed_x=None,
        speed_y=None,
    ):
        super().__init__(*groups)
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.speed = self.DEFAULT_SPEED

        # Start with two lives and wait for the launch input
        self.lives = 2
        self.waiting_for_launch = True

        # Flag to prevent multiple paddle collisions in one contact
        self.can_collide_with_paddle = True

        # Define the ball radius/size
        self.radius = radius if radius is not None else self.DEFAULT_RADIUS

        # Create a surface for the ball and fill
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)

        # Initialize movement speed
        self.speed_x = (
            speed_x
            if speed_x is not None
            else random.choice([-self.DEFAULT_SPEED, self.DEFAULT_SPEED])
        )
        self.speed_y = speed_y if speed_y is not None else -self.DEFAULT_SPEED

        # Initialize the collision detection rectangle
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def move(self, screen_size, screen_state) -> int:
        """Handles movement and collision with walls, paddle, and bricks."""
        points = 0

        # Update the ball position
        self.x_position += self.speed_x
        self.y_position += self.speed_y

        # Handle the bounce off the side walls
        if (
            self.x_position <= 0
            or self.x_position >= screen_size.width - self.rect.width
        ):
            self.bounce_x()  # Reverse horizontal movement

        # Handle the bounce off the ceiling
        if self.y_position <= 0:
            self.bounce_y()  # Reverse vertical movement

        # Handle collision with the bottom of the screen (Lose a life or End Game)
        if self.y_position >= screen_size.height:
            if screen_state.lives > 1:
                screen_state.lose_life()  # Decrease lives
                self.reset_position()  # Reset ball position
                screen_state.paddle.reset_position()
            else:
                screen_state.game_over = True  # End Game
                return screen_state  # Stop further movement processing

        paddle: Paddle = screen_state.paddle
        # Handle collisions with the paddle
        if (
            self.speed_y > 0
            and self.rect.colliderect(paddle.rect)
            and self.can_collide_with_paddle
        ):
            self.bounce_y()  # Reverse vertical direction
            # Position the ball right above the paddle to prevent overlapping
            self.y_position = paddle.rect.top - self.rect.height

            # Adjust horizontal speed based on where the ball hits the paddle
            paddle_center = paddle.rect.centerx
            ball_center = self.rect.centerx
            offset = ball_center - paddle_center
            max_offset = paddle.rect.width / 2  # Maximum possible offset from center
            # Calculate new horizontal speed
            new_speed_x = self.DEFAULT_SPEED * (offset / max_offset)
            # Cap the horizontal speed to prevent it from going too fast
            if new_speed_x > self.MAX_SPEED:
                new_speed_x = self.MAX_SPEED
            elif new_speed_x < -self.MAX_SPEED:
                new_speed_x = -self.MAX_SPEED
            self.speed_x = new_speed_x

            # Disable paddle collisions until the ball is away from the paddle
            self.can_collide_with_paddle = False

        # Re-enable paddle collisions once the ball is above the paddle
        if self.rect.bottom < paddle.rect.top:
            self.can_collide_with_paddle = True

        # Handle collisions with bricks
        hit_bricks = pygame.sprite.spritecollide(self, screen_state.bricks, False)
        reversed_x = False
        reversed_y = False

        for brick in hit_bricks:
            # Calculate the collision axis for each brick
            vertical_overlap = min(
                abs(self.rect.bottom - brick.rect.top),
                abs(self.rect.top - brick.rect.bottom),
            )
            horizontal_overlap = min(
                abs(self.rect.right - brick.rect.left),
                abs(self.rect.left - brick.rect.right),
            )

            # Bounce based on the smaller overlap distance
            if vertical_overlap < horizontal_overlap and not reversed_y:
                self.bounce_y()
                reversed_y = True
            elif horizontal_overlap < vertical_overlap and not reversed_x:
                self.bounce_x()
                reversed_x = True

            # Remove the brick
            points += brick.hit()

        # Update rect/collision area position
        self.rect.x = self.x_position
        self.rect.y = self.y_position

        screen_state.score.increase_score(points)
        return screen_state

    def bounce_x(self):
        """Reverse the horizontal direction of the ball."""
        self.speed_x = -self.speed_x

    def bounce_y(self):
        """Reverse the vertical direction of the ball."""
        self.speed_y = -self.speed_y

    def reset_position(self, wait=True):
        """Resets ball to starting position and waits for launch."""
        self.x_position = 250  # Reset to the center of the screen
        self.y_position = 380
        self.speed_x = random.choice([-self.DEFAULT_SPEED, self.DEFAULT_SPEED])
        self.speed_y = -self.DEFAULT_SPEED  # Always start moving upward
        self.waiting_for_launch = wait
        self.rect.topleft = (self.x_position, self.y_position)
