"""
Brick
=====
Implement the Brick object and related interactions/physics
Subclass of BreakoutSprite
Should be added to a group of sprites to represent the overall level, use spritecollide

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

import pygame
from breakout.sprite import BreakoutSprite


class Brick(BreakoutSprite):
    """Brick class - Characteristics for a single brick in the game."""

    WIDTH = 51
    HEIGHT = 20

    def __init__(
        self, *groups, color=pygame.Color(255, 0, 0), x_position=0, y_position=0
    ):
        # Create the surface/rect for the brick
        image = pygame.Surface((self.WIDTH, self.HEIGHT))  # Create the image surface
        image.fill(color)  # Fill it with the provided color

        # Pass all required arguments to the superclass
        super().__init__(
            *groups,
            x_position=x_position,
            y_position=y_position,
            color=color,
            image=image
        )

        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.x_position, self.y_position))

    @classmethod
    def create_brick_layout(cls, rows, cols, x_offset=5, y_offset=5):
        """Orders and colors the brick grid layout."""
        brick_group = pygame.sprite.Group()

        # Calculate dynamic division for brick colors
        red_rows = max(1, rows // 4)  # Min of 1 row for red
        yellow_rows = max(1, rows // 3)  # Min of 1 row for yellow

        for row in range(rows):
            # Assign colors based on dynamic boundaries
            if row < red_rows:
                color = pygame.Color(255, 0, 0)  # Red
            elif row < red_rows + yellow_rows:
                color = pygame.Color(255, 255, 0)  # Yellow
            else:
                color = pygame.Color(0, 255, 0)  # Green is all remaining rows

            for col in range(cols):
                x = col * (cls.WIDTH + x_offset)
                y = row * (cls.HEIGHT + y_offset)
                brick = cls(brick_group, color=color, x_position=x, y_position=y)
                brick_group.add(brick)

        return brick_group
