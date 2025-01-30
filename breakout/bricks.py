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

from breakout import screen_size
from breakout.sprite import BreakoutSprite


class Brick(BreakoutSprite):
    """Brick class - Characteristics for a single brick in the game."""

    WIDTH = 51
    HEIGHT = 25

    def __init__(
        self,
        *groups,
        color=pygame.Color(255, 0, 0),
        x_position=0,
        y_position=0,
        border_radius=5
    ):

        # Create the surface/rect for the brick
        image = pygame.Surface(
            (self.WIDTH, self.HEIGHT), pygame.SRCALPHA
        )  # Create the image surface
        pygame.draw.rect(
            image,  # Surface to draw on
            color,  # Color of the rectangle
            (0, 0, self.WIDTH, self.HEIGHT),  # Rectangle dimensions
            border_radius=border_radius,  # Rounded corners
        )

        # Pass all required arguments to the superclass
        super().__init__(
            *groups,
            x_position=x_position,
            y_position=y_position,
            color=color,
            image=image,
        )

        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.x_position, self.y_position))

    def hit(self):
        """Actions when bricks are hit by the ball"""
        self.disappear()  # remove the brick from the game

    @classmethod
    def create_brick_layout(cls, rows, cols):
        """Orders and centers the brick grid layout with dynamic colors."""
        brick_group = pygame.sprite.Group()

        screen_width = screen_size.width
        screen_height = screen_size.height

        # Spacing and margins
        x_offset = 10  # Horizontal spacing between bricks
        y_offset = 10  # Vertical spacing between bricks
        top_margin = 2  # Number of empty rows at the top

        # Calculate the total brick area width and starting X position for centering
        brick_area_width = cols * (cls.WIDTH + x_offset) - x_offset
        start_x = (screen_width - brick_area_width) // 2  # Center bricks horizontally

        # Calculate starting Y position to account for the top margin
        start_y = cls.HEIGHT * top_margin

        # Determine the number of rows for each color
        red_rows = max(1, rows // 4)  # Red occupies the first quarter
        yellow_rows = max(1, rows // 3)  # Yellow occupies the next third
        green_rows = rows - (red_rows + yellow_rows)  # Remaining rows are green

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (cls.WIDTH + x_offset)  # Adjusted x position
                y = start_y + row * (cls.HEIGHT + y_offset)  # Adjusted y position

                # Assign colors based on row
                if row < red_rows:
                    color = pygame.Color(255, 0, 0)  # Red
                elif row < red_rows + yellow_rows:
                    color = pygame.Color(255, 255, 0)  # Yellow
                else:
                    color = pygame.Color(0, 255, 0)  # Green

                brick = cls(brick_group, color=color, x_position=x, y_position=y)
                brick_group.add(brick)

        return brick_group
