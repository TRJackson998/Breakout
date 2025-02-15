"""
Brick
=====
Represents individual bricks in the game, managing their appearance, structure, 
and removal upon collision with the ball. Assigns point values for scoring.

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

from dataclasses import dataclass

import pygame
from pygame.sprite import Sprite

from breakout import screen_size

# pylint: disable=no-member
@dataclass
class BrickConfig:
    """Configuration for Ball constants."""

    width = 51
    height = 25
    border_radius = 5


class Brick(Sprite):
    """Brick class - Characteristics for a single brick in the game."""

    def __init__(
        self,
        *groups,
        color: pygame.Color,
        x_position: int = 0,
        y_position: int = 0,
        border_radius: int = 5
    ):
        super().__init__(
            *groups,
        )
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.width = BrickConfig.width
        self.height = BrickConfig.height

        # Create the surface/rect for the brick
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.x_position, self.y_position))
        # Fill the rectangle onto the image
        pygame.draw.rect(
            self.image,  # Surface to draw on
            color,  # Color of the rectangle
            (0, 0, self.width, self.height),  # Rectangle dimensions
            border_radius=border_radius,  # Rounded corners
            border_radius=BrickConfig.border_radius,  # Rounded corners
        )

        # Set point value
        if self.color == pygame.Color("red"):
            self.points = 3
        elif self.color == pygame.Color("yellow"):
            self.points = 2
        else:
            self.points = 1

    def hit(self) -> int:
        """Actions when bricks are hit by the ball"""
        self.kill()  # remove the brick from the game
        return self.points

    @classmethod
    def create_brick_layout(cls, rows: int, cols: int):
        """Orders and centers the brick grid layout with dynamic colors."""
        brick_group = pygame.sprite.Group()

        screen_width = screen_size.width

        # Spacing and margins
        x_offset = 10  # Horizontal spacing between bricks
        y_offset = 10  # Vertical spacing between bricks
        top_margin = 2  # Number of empty rows at the top

        # Calculate the total brick area width and starting X position for centering
        brick_area_width = cols * (BrickConfig.width + x_offset) - x_offset
        start_x = (screen_width - brick_area_width) // 2  # Center bricks horizontally

        # Calculate starting Y position to account for the top margin
        start_y = BrickConfig.height * top_margin

        # Determine the number of rows for each color
        red_rows = max(1, rows // 4)  # Red occupies the first quarter
        yellow_rows = max(
            1, rows // 3
        )  # Yellow occupies the next third with the remaining being green

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (
                    BrickConfig.width + x_offset
                )  # Adjusted x position
                y = start_y + row * (
                    BrickConfig.height + y_offset
                )  # Adjusted y position

                # Assign colors based on row
                if row < red_rows:
                    color = pygame.Color("red")  # Red
                elif row < red_rows + yellow_rows:
                    color = pygame.Color("yellow")  # Yellow
                else:
                    color = pygame.Color("green")  # Green

                brick = cls(brick_group, color=color, x_position=x, y_position=y)
                brick_group.add(brick)

        return brick_group
