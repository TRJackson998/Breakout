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

import pygame
from pygame.sprite import Sprite

from breakout import Position, Size, base_path, screen_size


# pylint: disable=no-member
@dataclass
class BrickConfig:
    """Configuration for Brick constants."""

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
        """
        Initialize a Brick.

        Args:
            groups: Sprite groups to add the brick to.
            color: The color of the brick.
            position: The position where the brick is placed.
            texture: If True, marks the brick as unbreakable and applies a texture.
        """
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
        self.image.fill((0, 0, 0, 0))
        self.kill()  # remove the brick from the game
        return self.points

    @classmethod
    def load_texture(cls):
        """Load the unbreakable texture (Multi-hit bricks will be wearing this texture)"""
        try:
            texture_path = base_path.joinpath("textures", "unbreakable_texture.jpg")
            Brick.unbreakable_texture = pygame.image.load(
                str(texture_path)
            ).convert_alpha()
            Brick.unbreakable_texture = pygame.transform.scale(
                Brick.unbreakable_texture, astuple(BrickConfig.size)
            )
            print("Texture loaded successfully from", texture_path)
        except (FileNotFoundError, pygame.error) as e:
            print("Error loading texture:", e)
            Brick.unbreakable_texture = None

    @classmethod
    def create_brick_layout(cls, rows: int, cols: int, level: int):
        """
        Order and center the brick grid layout with dynamic colors.
        A fixed percentage per level (10% per level, capped at 100%)
        are randomly marked as multi-hit.

        Args:
            rows: Number of rows in the brick layout.
            cols: Number of columns in the brick layout.
            level: The current game level, used to determine the percentage of unbreakable bricks.
        """
        brick_group = pygame.sprite.Group()
        offset = 10  # Margin between bricks

        total = rows * cols  # For 6 rows x 8 cols, total is 48.
        chance = min(level * 0.1, 1.0)
        extra_count = round(total * chance)

        # Create a list of indices and randomly shuffle it.
        indices = list(range(total))
        random.shuffle(indices)
        # Select exactly extra_count indices that will be 'unbreakable'.
        selected = set(indices[:extra_count])

        # Calculate the total brick area width
        brick_area_width = cols * (BrickConfig.size.width + offset) - offset

        # Center bricks horizontally, account for top margin
        start_position = Position(
            (screen_size.width - brick_area_width) // 2,
            BrickConfig.size.height * (offset // 5),
        )

        # Load the brick texture if needed.
        if not hasattr(cls, "unbreakable_texture"):
            cls.load_texture()

        index = 0  # Running index for each brick.
        design = [(x, y) for x in range(rows) for y in range(cols)]
        if level != 1:
            design = random.choice([design, generate_random_design(rows, cols)])

        for row, col in design:
            position = Position(
                start_position.x + col * (BrickConfig.size.width + offset),
                start_position.y + row * (BrickConfig.size.height + offset),
            )
            color = assign_color(rows, row)
            # Mark this brick as extra durable if its index is in the selected set.
            texture = index in selected
            brick_group.add(
                cls(
                    brick_group,
                    color=color,
                    position=position,
                    texture=texture,
                )
            )
            index += 1

        return brick_group


def assign_color(rows: int, row: int):
    """
    Determine the brick's color based on its row position.

    Args:
        rows: Total number of rows.
        row: The row index for the current brick.
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


def generate_random_design(rows: int, cols: int):
    """
    Generate a list of row-col indices forming a random shape within a given grid.
    The shape can be a triangle, circle, or diagonal pattern.
    """
    random.seed()
    shape_type = random.choice(["triangle", "circle", "diagonal"])
    selected_indices = set()

    if shape_type == "triangle":
        for r in range(rows):
            for c in range(r + 1):  # Creates a right triangle shape
                selected_indices.add((r, c))

    elif shape_type == "circle":
        center = (rows // 2, cols // 2)
        radius = min(rows, cols) // 3
        for r in range(rows):
            for c in range(cols):
                if (r - center[0]) ** 2 + (c - center[1]) ** 2 <= radius**2:
                    selected_indices.add((r, c))

    elif shape_type == "diagonal":
        thickness = random.randint(1, cols // 2)
        for r in range(rows):
            for c in range(cols):
                if abs(r - c) < thickness:  # Randomized diagonal thickness
                    selected_indices.add((r, c))

    return list(selected_indices)
