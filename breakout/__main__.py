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
from breakout.screens import Screens

CURRENT_SCREEN = None


def main():
    """The main function initializes the game, sets up the winbdow, and runs the game loop"""
    global CURRENT_SCREEN
    window = pygame.display.set_mode(astuple(screen_size))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()
    CURRENT_SCREEN = Screens.START

    # Create the brick layout using the Brick class
    brick_group = Brick.create_brick_layout(rows=9, cols=9)
    Screens.GAME.add_element(brick_group)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check if any of the elements on the screen need to handle an event
            for element in CURRENT_SCREEN.elements:
                try:
                    # Button elements on the screen run functions when clicked
                    element.handle_event(event)
                except AttributeError:
                    # Groups of Sprites like bricks do not handle events
                    pass

        CURRENT_SCREEN.draw(window)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
