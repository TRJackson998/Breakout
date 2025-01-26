"""
Breakout
========
The main driver script for the overall Breakout game
Run game loop
Control window/screen state
3 screens - start, gameplay, game over

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

from dataclasses import astuple

import pygame

from breakout import screen_size
from breakout.bricks import Brick


def main():
    """The main function initializes the game, sets up the winbdow, and runs the game loop"""
    pygame.init()
    window = pygame.display.set_mode(astuple(screen_size))
    clock = pygame.time.Clock()

    # Create the brick layout using the Brick class
    brick_group = Brick.create_brick_layout(rows=9, cols=9)

    running = True
    while running:
        window.fill((0, 0, 0))  # Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw all bricks
        brick_group.draw(window)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
