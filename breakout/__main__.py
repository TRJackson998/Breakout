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
from breakout.bricks import Brick
from breakout.paddle import Paddle


def main():
    """The main function initializes the game, sets up the winbdow, and runs the game loop"""
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    # Create the paddle
    paddle_group = pygame.sprite.Group()
    paddle = Paddle(paddle_group)

    # Create the brick layout using the Brick class
    brick_group = Brick.create_brick_layout(rows=9, cols=9)

    running = True
    while running:
        window.fill((0, 0, 0))  # Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left()
        if keys[pygame.K_RIGHT]:
            paddle.move_right(screen_width=500)

        # Draw paddle and bricks
        paddle_group.draw(window)
        brick_group.draw(window)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
