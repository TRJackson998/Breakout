"""
Breakout
========
Manages the core game loop, screen transitions, and overall game logic. 
Handles user input, game state changes, and object initialization for gameplay.

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

import sys
from dataclasses import astuple

import pygame

from breakout import screen_size
from breakout.ball import Ball
from breakout.bricks import Brick
from breakout.paddle import Paddle
from breakout.score import (
    CurrentScore,
    LaunchMessage,
    LivesDisplay,
    NameInput,
    Scoreboard,
)
from breakout.screens import ArrowButton, Button, Screens

# pylint: disable=no-member


class Game:
    """Class to handle and run the game"""

    def __init__(self):
        self.current_screen = Screens.START
        self.window = pygame.display.set_mode(astuple(screen_size), pygame.RESIZABLE)
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.ball, self.paddle, self.bricks = None, None, None
        self.paused = False
        self.scoreboard = Scoreboard()
        self.current_score = CurrentScore()
        self.name_imput = NameInput()
        self.setup_screens()
        self.lives_display = None
        self.launch_message = None

    def setup_screens(self):
        """Add static button elements to START and END screens"""
        # Start Screen

        Screens.START.add_element(
            Button("START GAME", lambda: self.switch_screen(Screens.GAME), "top")
        )
        Screens.START.add_element(Button("QUIT", self.quit_game, "bottom"))

        # End Screen
        Screens.END.add_element(
            Button("START GAME", lambda: self.switch_screen(Screens.GAME), "top")
        )
        Screens.END.add_element(Button("QUIT", self.quit_game, "bottom"))
        Screens.END.add_element(self.scoreboard)
        Screens.END.add_element(self.name_imput)
        Screens.END.add_element(Button("SUBMIT", self.save_score, "right"))

    def switch_screen(self, screen: Screens):
        """
        Switch from current screen
        If the new screen is the game screen, start a new game
        """
        self.current_screen = screen
        if screen == Screens.GAME:
            self.start_new_game()

    def start_new_game(self):
        """
        Start a new game
        Create the paddle, ball and brick elements
        """
        self.paused = False
        self.current_score = CurrentScore()
        Screens.GAME.elements.clear()
        Screens.GAME.add_element(Button("PAUSE GAME", self.pause_game, "top"))
        Screens.GAME.add_element(
            Button("END GAME", lambda: self.switch_screen(Screens.END), "bottom")
        )
        Screens.GAME.add_element(self.current_score)

        ball_group = pygame.sprite.Group()
        paddle_group = pygame.sprite.Group()
        brick_group = Brick.create_brick_layout(rows=6, cols=8)

        Screens.GAME.add_element(ball_group)
        Screens.GAME.add_element(paddle_group)
        Screens.GAME.add_element(brick_group)

        self.ball = Ball(ball_group)
        self.paddle = Paddle(paddle_group)
        self.bricks = brick_group

        # Create and add the LivesDisplay & Launch element.
        self.lives_display = LivesDisplay(self.ball.lives)
        Screens.GAME.add_element(self.lives_display)
        self.launch_message = LaunchMessage()
        Screens.GAME.add_element(self.launch_message)

        self.left_arrow = ArrowButton(
            "left", (screen_size.width - 187, screen_size.height - 40)
        )
        Screens.GAME.add_element(self.left_arrow)
        self.right_arrow = ArrowButton(
            "right", (screen_size.width - 100, screen_size.height - 40)
        )
        Screens.GAME.add_element(self.right_arrow)

    def pause_game(self):
        """Pause the game"""
        self.paused = True

        # Find and remove the Pause button
        for element in Screens.GAME.elements:
            if isinstance(element, Button) and "pause" in element.text.lower():
                Screens.GAME.elements.remove(element)

        # Add a resume button
        Screens.GAME.add_element(Button("RESUME GAME", self.resume_game, "top"))

    def resume_game(self):
        """Resume the game"""
        self.paused = False

        # Find and remove the Resume button
        for element in Screens.GAME.elements:
            if isinstance(element, Button) and "resume" in element.text.lower():
                Screens.GAME.elements.remove(element)

        # Add a pause button
        Screens.GAME.add_element(Button("PAUSE GAME", self.pause_game, "top"))

    def quit_game(self):
        """Quit the game"""
        pygame.quit()
        sys.exit()

    def save_score(self):
        """Saves the current score to the leaderboard and resets it."""
        if not self.name_imput.name:
            return
        self.scoreboard.top_scores[self.current_score.current_score] = (
            self.name_imput.name.upper()
        )  # update this player's top score
        self.scoreboard.top_scores = dict(
            sorted(
                self.scoreboard.top_scores.items(), key=lambda x: x[0], reverse=True
            )[:10]
        )  # Sort, only keep only the top 10 scores
        self.name_imput.name = ""

    def handle_events(self):
        """Handle all events in the game loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                # Launch the ball only when the up arrow is pressed
                if (
                    event.key == pygame.K_UP
                    and self.ball is not None
                    and self.ball.waiting_for_launch
                ):
                    self.ball.waiting_for_launch = False
                    if self.launch_message in self.current_screen.elements:
                        self.current_screen.elements.remove(self.launch_message)
            for element in self.current_screen.elements:
                try:
                    # Button elements on the screen run functions when clicked
                    element.handle_event(event)
                except AttributeError:
                    # Groups of Sprites like bricks do not handle events
                    pass

    def update_game(self):
        """Handle the gameplay"""
        keys = pygame.key.get_pressed()
        # Allow paddle movement only if the ball has been launched
        if not self.ball.waiting_for_launch:
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or self.left_arrow.pressed:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.right_arrow.pressed:
                self.paddle.move_right()

        points = self.ball.move(
            screen_size, self.paddle, self.bricks, self.switch_screen, Screens
        )
        self.current_score.increase_score(points)

        # Update the lives display with the current number of lives
        self.lives_display.update(self.ball.lives)

        # Check if all the bricks are gone, and if so, reset the brick layout
        if len(self.bricks.sprites()) == 0:
            self.next_level()

    def next_level(self):
        """Reset the brick layout to continue the game play."""
        self.ball.reset_position(wait=False)
        # Create a new brick layout.
        self.bricks = Brick.create_brick_layout(rows=6, cols=8)
        # Add to screen
        Screens.GAME.add_element(self.bricks)

    def run(self):
        """Run the main game loop"""
        while True:
            self.handle_events()
            if self.current_screen == Screens.GAME and not self.paused:
                self.update_game()
            self.current_screen.draw(self.window)
            pygame.display.update()
            self.clock.tick(50)


if __name__ == "__main__":
    Game().run()
