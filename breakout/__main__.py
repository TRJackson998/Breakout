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

import pygame


def main():
    """Driver function"""
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


if __name__ == """__main__""":
    main()
