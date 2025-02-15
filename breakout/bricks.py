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
from dataclasses import astuple, dataclass
from pathlib import Path

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
        texture: bool = False
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
        self.breakable = True  # Bricks are breakable by default

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

        if texture:
            self.breakable = False
            if hasattr(Brick, "unbreakable_texture") and Brick.unbreakable_texture:
                self.image.blit(Brick.unbreakable_texture, (0, 0))
            else:
                self.image.fill((0, 0, 0))

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
                (0, 0, self.size.width, self.size.height),
                border_radius=BrickConfig.border_radius,
            )
            return 0
        # self.image.fill((0, 0, 0, 0))  # Clear the bricks image entirely TODO is this needed?
        self.kill()  # remove the brick from the game
        return self.points

    @classmethod
    def load_texture(cls):
        """Load the unbreakable texture"""
        try:
            base_path = Path(__file__).parent
            texture_path = base_path.joinpath("textures", "unbreakable_texture.jpg")
            Brick.unbreakable_texture = pygame.image.load(
                str(texture_path)
            ).convert_alpha()
            Brick.unbreakable_texture = pygame.transform.scale(
                Brick.unbreakable_texture, astuple(BrickConfig.size)
            )
            print("Texture loaded successfully from", texture_path)
        except Exception as e:
            print("Error loading texture:", e)
            Brick.unbreakable_texture = None

    @classmethod
    def create_brick_layout(cls, rows: int, cols: int, level: int):
        """Orders and centers the brick grid layout with dynamic colors."""
        brick_group = pygame.sprite.Group()
        offset = 10  # Margin between bricks

        # Calculate the total brick area width
        brick_area_width = cols * (BrickConfig.size.width + offset) - offset

        # Center bricks horizontally, account for top margin
        start_position = Position(
            (screen_size.width - brick_area_width) // 2,
            BrickConfig.size.height * (offset // 5),
        )

        # Load the brick texture
        if level >= 1 and not hasattr(cls, "unbreakable_texture"):
            cls.load_texture()

        chance = min(level * 0.1, 1.0)

        for row in range(rows):
            for col in range(cols):
                # calculate position for this specific brick
                position = Position(
                    start_position.x + col * (BrickConfig.size.width + offset),
                    start_position.y + row * (BrickConfig.size.height + offset),
                )
                # Assign colors based on row
                color = assign_color(rows, row)
                texture = False
                if level >= 1 and random.random() < chance:
                    texture = True
                brick_group.add(
                    cls(
                        brick_group,
                        color=color,
                        position=position,
                        texture=texture,
                    )
                )

        return brick_group


def assign_color(rows: int, row: int):
    """
    Pick what color the brick will be based on which row
    it is in out of the total rows
    """
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
    return color
