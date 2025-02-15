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

import random
import pygame
from pygame.sprite import Sprite
from breakout import screen_size
from pathlib import Path

# pylint: disable=no-member


class Brick(Sprite):
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
        super().__init__(
            *groups,
        )
        self.x_position = x_position
        self.y_position = y_position
        self.color = color
        self.breakable = True  # Bricks are breakable by default
        self.border_radius = border_radius

        # Create the surface/rect for the brick
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Initialize the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(self.x_position, self.y_position))
        # Fill the rectangle onto the image
        pygame.draw.rect(
            self.image,  # Surface to draw on
            color,  # Color of the rectangle
            (0, 0, self.WIDTH, self.HEIGHT),  # Rectangle dimensions
            border_radius=border_radius,  # Rounded corners
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
        if not self.breakable:
            # Unbreakable bricks do not get destroyed.
            self.breakable = True
            # Clear the texture by redrawing the brick in its base color.
            self.image.fill((0, 0, 0, 0))  # Clear with transparency.
            pygame.draw.rect(
                self.image,
                self.color,
                (0, 0, self.WIDTH, self.HEIGHT),
                border_radius=self.border_radius,
            )
            return 0
        else:
            self.kill()  # remove the brick from the game
            return self.points

    @classmethod
    def create_brick_layout(cls, rows, cols, level):
        """Orders and centers the brick grid layout with dynamic colors."""
        brick_group = pygame.sprite.Group()
        screen_width = screen_size.width

        # Spacing and margins
        x_offset = 10  # Horizontal spacing between bricks
        y_offset = 10  # Vertical spacing between bricks
        top_margin = 2  # Number of empty rows at the top

        # Calculate the total brick area width and starting X position for centering
        brick_area_width = cols * (cls.WIDTH + x_offset) - x_offset
        start_x = (screen_width - brick_area_width) // 2  # Center bricks horizontally
        start_y = cls.HEIGHT * top_margin

        # Determine the number of rows for each color
        red_rows = max(1, rows // 4)  # Red occupies the first quarter
        yellow_rows = max(
            1, rows // 3
        )  # Yellow occupies the next third with the remaining being green

        # Load the brick texture
        if level >= 1 and not hasattr(cls, "unbreakable_texture"):
            try:
                base_path = Path(__file__).parent
                texture_path = base_path.joinpath("textures", "unbreakable_texture.jpg")
                cls.unbreakable_texture = pygame.image.load(
                    str(texture_path)
                ).convert_alpha()
                cls.unbreakable_texture = pygame.transform.scale(
                    cls.unbreakable_texture, (cls.WIDTH, cls.HEIGHT)
                )
                print("Texture loaded successfully from", texture_path)
            except Exception as e:
                print("Error loading texture:", e)
                cls.unbreakable_texture = None

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (cls.WIDTH + x_offset)  # Adjusted x position
                y = start_y + row * (cls.HEIGHT + y_offset)  # Adjusted y position

                # Assign colors based on row
                if row < red_rows:
                    color = pygame.Color("red")
                elif row < red_rows + yellow_rows:
                    color = pygame.Color("yellow")
                else:
                    color = pygame.Color("green")

                brick = cls(brick_group, color=color, x_position=x, y_position=y)

                if level >= 1 and random.random() < 0.2:  # 20% chance
                    brick.breakable = False
                    if hasattr(cls, "unbreakable_texture") and cls.unbreakable_texture:
                        brick.image.blit(cls.unbreakable_texture, (0, 0))
                    else:
                        brick.image.fill((0, 0, 0))
                brick_group.add(brick)

        return brick_group
