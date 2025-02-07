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
from pathlib import Path

import pygame

from breakout import screen_size
from breakout.ball import Ball
from breakout.bricks import Brick
from breakout.paddle import Paddle
from breakout.score import LivesDisplay, NameInput, Scoreboard, ScoreDisplay
from breakout.screens import ArrowButton, Button, LaunchMessage, ScreenManager, Screens

# pylint: disable=no-member


class Game:
    """Class to handle and run the game"""

    def __init__(self):
        self.window = pygame.display.set_mode(astuple(screen_size), pygame.RESIZABLE)
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()

        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = Path(sys._MEIPASS)
        except Exception:
            base_path = Path(__file__).joinpath("..")
        start_bg = pygame.image.load(
            base_path.joinpath("textures", "StartScreen.jpg")
        ).convert()
        game_bg = pygame.image.load(
            base_path.joinpath("textures", "GameScreen.jpg")
        ).convert()
        end_bg = pygame.image.load(
            base_path.joinpath("textures", "EndScreen.jpg")
        ).convert()
        # Assign the background image to the start screen.
        Screens.START.background_image = start_bg
        Screens.GAME.background_image = game_bg
        Screens.END.background_image = end_bg

        self.left_arrow = ArrowButton("left")
        self.right_arrow = ArrowButton("right")
        self.up_arrow = ArrowButton("up")
        self.scoreboard = Scoreboard()
        self.name_imput = NameInput()

        self.setup_screens()
        self.state = GameState()

    def setup_screens(self):
        """Add static button elements to START and END screens"""
        # Start Screen

        Screens.START.add_element(
            Button("START GAME", lambda: self.switch_screen(Screens.GAME), "middle")
        )
        Screens.START.add_element(Button("QUIT", self.quit_game, "bottom"))

        # End Screen
        Screens.END.add_element(
            Button("START GAME", lambda: self.switch_screen(Screens.GAME), "middle")
        )
        Screens.END.add_element(Button("QUIT", self.quit_game, "bottom"))
        Screens.END.add_element(self.scoreboard)
        Screens.END.add_element(self.name_imput)
        Screens.END.add_element(Button("SUBMIT", self.save_score, "top"))

    def switch_screen(self, screen: Screens):
        """
        Switch from current screen
        If the new screen is the game screen, start a new game
        """
        self.state.current_screen = screen
        if screen == Screens.GAME:
            self.start_new_game()

    def start_new_game(self):
        """
        Start a new game
        Create the paddle, ball and brick elements
        """
        self.state = GameState(Screens.GAME)  # fresh game state
        self.up_arrow = ArrowButton("up")  # fresh up arrow
        Screens.GAME.elements.clear()

        # Buttons
        Screens.GAME.add_element(Button("PAUSE GAME", self.pause_game, "middle"))
        Screens.GAME.add_element(
            Button("END GAME", lambda: self.switch_screen(Screens.END), "bottom")
        )
        Screens.GAME.add_element(self.left_arrow)
        Screens.GAME.add_element(self.right_arrow)
        Screens.GAME.add_element(self.up_arrow)

        # Game state objects
        Screens.GAME.add_element(self.state.score_display)
        Screens.GAME.add_element(self.state.ball_group)
        Screens.GAME.add_element(self.state.paddle_group)
        Screens.GAME.add_element(self.state.bricks)
        Screens.GAME.add_element(self.state.lives_display)
        Screens.GAME.add_element(self.state.launch_message)

    def pause_game(self):
        """Pause the game"""
        if self.state.paused:
            return

        self.state.pause_game()

        # Change from pause to resume button
        for idx, element in enumerate(Screens.GAME.elements):
            if isinstance(element, Button) and "pause" in element.text.lower():
                Screens.GAME.elements[idx].update_button(
                    "RESUME GAME", self.resume_game
                )
                break

    def resume_game(self):
        """Resume the game"""
        if not self.state.paused:
            return

        self.state.resume_game()

        # Find and remove the Resume button
        for idx, element in enumerate(Screens.GAME.elements):
            if isinstance(element, Button) and "resume" in element.text.lower():
                Screens.GAME.elements[idx].update_button("PAUSE GAME", self.pause_game)
                break

    def quit_game(self):
        """Quit the game"""
        pygame.quit()
        sys.exit()

    def save_score(self):
        """Saves the current score to the leaderboard and resets it."""
        if not self.name_imput.name:
            return
        self.scoreboard.top_scores[self.state.score] = (
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
                    self.up_arrow in self.state.current_screen.elements
                    and event.key == pygame.K_UP
                ):
                    self.state.launch_ball()
                    self.state.current_screen.elements.remove(self.up_arrow)

            self.state.current_screen.handle_event(event)

    def update_game(self):
        """Handle the gameplay"""
        if self.state.paused or self.state.game_over:
            return

        keys = pygame.key.get_pressed()

        # Check for GUI arrow press for launching the ball.
        if self.up_arrow.pressed:
            self.state.launch_ball()
            if self.up_arrow in self.state.current_screen.elements:
                self.state.current_screen.elements.remove(self.up_arrow)

        # Allow paddle and ball movement only if the ball has been launched.
        if self.state.launched:
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or self.left_arrow.pressed:
                self.state.paddle.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.right_arrow.pressed:
                self.state.paddle.move_right()

            self.state = self.state.ball.move(screen_size, self.state)

        # if the ball is waiting for launch, ensure the up arrow is on screen.
        if (
            not self.state.launched
            and self.state.current_screen == Screens.GAME
            and self.up_arrow not in self.state.current_screen.elements
        ):
            self.up_arrow = ArrowButton("up")
            self.state.current_screen.add_element(self.up_arrow)

    def run(self):
        """Run the main game loop"""
        while True:
            self.handle_events()
            self.update_game()
            self.state.update()

            self.state.current_screen.draw(self.window)
            pygame.display.update()
            self.clock.tick(50)


class GameState:
    """Manages the game's current state and flags for transitions."""

    def __init__(self, screen: ScreenManager = Screens.START):
        """Reset the game state for a new game."""
        self.score = 0  # Default starting score
        self.lives = 3  # Default starting lives
        self.bricks = Brick.create_brick_layout(rows=6, cols=8)
        self.ball_group = pygame.sprite.Group()
        self.paddle_group = pygame.sprite.Group()
        self.ball = Ball(self.ball_group)
        self.paddle = Paddle(self.paddle_group)
        self.score_display = ScoreDisplay(self.score)
        self.lives_display = LivesDisplay(self.lives)
        self.launch_message = LaunchMessage()
        self.current_screen: ScreenManager = screen

        # State flags
        self.launched = False
        self.paused = False
        self.game_over = False

    def update(self):
        """Update the game based on the current state"""
        if (
            not self.launched
            and self.launch_message not in self.current_screen.elements
            and self.current_screen == Screens.GAME
        ):
            self.current_screen.add_element(self.launch_message)

        if self.game_over:
            self.current_screen = Screens.END

        if len(self.bricks.sprites()) == 0:
            self.ball.reset_position()
            self.launch_ball()
            self.bricks = Brick.create_brick_layout(rows=6, cols=8)
            Screens.GAME.add_element(self.bricks)

        self.score_display.update(self.score)
        self.lives_display.update(self.lives)

    def launch_ball(self):
        """Trigger ball launch."""
        if self.launched:
            return

        self.launched = True
        if self.launch_message in self.current_screen.elements:
            self.current_screen.elements.remove(self.launch_message)

    def pause_game(self):
        """Pause the game."""
        self.paused = True

    def resume_game(self):
        """Resume the game."""
        self.paused = False

    def game_over_state(self):
        """Mark game as over."""
        self.game_over = True


if __name__ == "__main__":
    Game().run()
