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

from dataclasses import astuple, dataclass

import pygame
from pygame.sprite import Sprite

from breakout import Position, Size, screen_size


# pylint: disable=no-member
@dataclass
class BrickConfig:
    """Configuration for Ball constants."""

    size = Size(51, 25)
    border_radius = 5


class Brick(Sprite):
    """Brick class - Characteristics for a single brick in the game."""

    def __init__(
        self,
        *groups,
        color: pygame.Color,
        position: Position | tuple = Position(0, 0),
    ):
        super().__init__(
            *groups,
        )
        if isinstance(position, tuple):
            self.position = Position(position[0], position[1])
        else:
            self.position = position
        self.color = color
        self.size = BrickConfig.size

        # Create the surface/rect for the brick
        self.image = pygame.Surface(astuple(self.size), pygame.SRCALPHA)
        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.position.x, self.position.y))
        # Fill the rectangle onto the image
        pygame.draw.rect(
            self.image,  # Surface to draw on
            color,  # Color of the rectangle
            (0, 0, self.size.width, self.size.height),  # Rectangle dimensions
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
        offset = 10  # Margin between bricks

        # Calculate the total brick area width and starting X position for centering bricks horizontally
        brick_area_width = cols * (BrickConfig.size.width + offset) - offset
        start_x = (screen_size.width - brick_area_width) // 2

        # Calculate starting Y position to account for the top margin
        start_y = BrickConfig.size.height * (offset // 5)

        for row in range(rows):
            for col in range(cols):
                # calculate position for this specific brick
                x = start_x + col * (BrickConfig.size.width + offset)
                y = start_y + row * (BrickConfig.size.height + offset)

                # Assign colors based on row
                first_quarter = max(1, rows // 4)
                if row < first_quarter:
                    # Red occupies the first quarter
                    color = pygame.Color("red")
                elif row < first_quarter + max(1, rows // 3):
                    # Yellow occupies the next third
                    color = pygame.Color("yellow")
                else:
                    # Rest are green
                    color = pygame.Color("green")

                brick = cls(brick_group, color=color, position=Position(x, y))
                brick_group.add(brick)

        return brick_group
