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

Created
-------
1.20.25
"""

import sys
from dataclasses import astuple

import pygame

from breakout import screen_size
from breakout.ball import Ball
from breakout.bricks import Brick
from breakout.paddle import Paddle
from breakout.screens import Button, Screens

CURRENT_SCREEN = None
NEW_GAME = False


def switch_screen(screen: Screens):
    """Update the current screen global variable with the new screen passed in"""
    global CURRENT_SCREEN, NEW_GAME
    CURRENT_SCREEN = screen

    if screen == Screens.GAME:
        NEW_GAME = True


def new_game() -> tuple[Ball, Paddle, pygame.sprite.Group]:
    """Init all gameplay objects"""
    Screens.GAME.elements.clear()

    Screens.GAME.add_element(Button("PAUSE GAME", pause_game, "top"))
    Screens.GAME.add_element(
        Button("END GAME", lambda: switch_screen(Screens.END), "bottom")
    )
    # Create the ball
    ball_group = pygame.sprite.Group()
    Screens.GAME.add_element(ball_group)

    # Create the paddle
    paddle_group = pygame.sprite.Group()
    Screens.GAME.add_element(paddle_group)

    # Create the brick layout using the Brick class
    brick_group = Brick.create_brick_layout(rows=6, cols=7)
    Screens.GAME.add_element(brick_group)

    return (Ball(ball_group), Paddle(paddle_group), brick_group)


def pause_game():
    """Placeholder for pause functionality"""
    print("Pause")


def quit_game():
    """Placeholder for quit functionality"""
    pygame.quit()
    sys.exit()


Screens.START.add_element(
    Button("START GAME", lambda: switch_screen(Screens.GAME), "top")
)
Screens.START.add_element(Button("QUIT", quit_game, "bottom"))

Screens.END.add_element(
    Button("START GAME", lambda: switch_screen(Screens.GAME), "top")
)
Screens.END.add_element(Button("QUIT", quit_game, "bottom"))


def main():
    """The main function initializes the game, sets up the winbdow, and runs the game loop"""
    global CURRENT_SCREEN, NEW_GAME
    ball, paddle, bricks = None, None, None
    window = pygame.display.set_mode(astuple(screen_size), pygame.RESIZABLE)
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()
    CURRENT_SCREEN = Screens.START

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
        if NEW_GAME:
            NEW_GAME = False
            ball, paddle, bricks = new_game()

        if CURRENT_SCREEN == Screens.GAME:
            # Handle paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                paddle.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                paddle.move_right()

            # Move the ball
            ball.move(screen_size, paddle, bricks)

        CURRENT_SCREEN.draw(window)

        pygame.display.update()
        clock.tick(50)


if __name__ == "__main__":
    main()
