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

from breakout.sprite import BreakoutSprite


class Ball(BreakoutSprite):
    """Ball class - Characteristics and behavior of the ball"""

    DEFAULT_RADIUS = 10
    DEFAULT_SPEED = 2

    def __init__(
        self,
        *groups,
        color=pygame.Color(255, 255, 255),
        x_position=250,
        y_position=250,
        radius=None,
        speed_x=None,
        speed_y=None,
    ):
        self.can_collide_with_paddle = True

        # Define the ball radius/size
        self.radius = radius if radius is not None else self.DEFAULT_RADIUS

        # Create a surface for the ball and fill
        image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(image, color, (self.radius, self.radius), self.radius)

        super().__init__(
            *groups,
            x_position=x_position,
            y_position=y_position,
            color=color,
            image=image,
            speed=self.DEFAULT_SPEED,
        )

        # Initialize movement speed
        self.speed_x = (
            speed_x
            if speed_x is not None
            else random.choice([-self.DEFAULT_SPEED, self.DEFAULT_SPEED])
        )
        self.speed_y = speed_y if speed_y is not None else -self.DEFAULT_SPEED

        # initialize area for collision detection
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def move(self, screen_size, paddle, brick_group):
        """Handles movement and collision with walls, paddle, and bricks."""
        # Update the position
        self.x_position += self.speed_x
        self.y_position += self.speed_y

        # Handle collisions with the side walls
        if (
            self.x_position <= 0
            or self.x_position >= screen_size.width - self.rect.width
        ):
            self.bounce_x()  # Reverse horizontal movement

        # Handle collision with the ceiling
        if self.y_position <= 0:
            self.bounce_y()  # Reverse vertical movement

        # Handle collisions with the paddle
        if (
            paddle.rect.y < self.y_position + self.rect.height
            and paddle.rect.x < self.x_position + self.rect.width
            and self.x_position > paddle.rect.x - self.rect.width
        ):
            self.bounce_y()  # Reverse vertical direction
            self.y_position = (
                paddle.rect.top - self.rect.height
            )  # Adjust position to avoid sticking

            # Adjust horizontal speed based on where the ball hits the paddle
            paddle_center = paddle.rect.centerx
            ball_center = self.rect.centerx
            offset = ball_center - paddle_center

            # Normalize the offset to adjust speed
            self.speed_x += offset // 10

        # Handle collisions with bricks
        hit_bricks = pygame.sprite.spritecollide(self, brick_group, False)
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

            # Reverse direction based on the smallest overlap
            if vertical_overlap < horizontal_overlap and not reversed_y:
                self.bounce_y()
                reversed_y = True
            elif horizontal_overlap < vertical_overlap and not reversed_x:
                self.bounce_x()
                reversed_x = True

            # Remove the brick
            brick.hit()

        # Reset paddle collision flag
        if self.y_position > paddle.rect.bottom:
            self.can_collide_with_paddle = True

        # Update the rect/collision area position
        self.rect.x = self.x_position
        self.rect.y = self.y_position

    def bounce_x(self):
        """Reverse the horizontal direction of the ball"""
        self.speed_x = -self.speed_x

    def bounce_y(self):
        """Reverse the vertical direction of the ball"""
        self.speed_y = -self.speed_y
