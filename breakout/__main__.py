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

import random
import sys
from dataclasses import astuple
from pathlib import Path

import pygame

from breakout import color_choices, screen_size, sound
from breakout.ball import Ball, BallConfig
from breakout.bricks import Brick
from breakout.paddle import Paddle
from breakout.powerups import PowerDown, PowerUp
from breakout.score import LivesDisplay, NameInput, Scoreboard, ScoreDisplay
from breakout.screens import (
    ArrowButton,
    BlinkingMessage,
    Button,
    ScreenManager,
    Screens,
)

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
            base_path = Path(__file__).parent
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

        sound.SoundManager.play_background_music()

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
        elif screen == Screens.END:
            self.state.game_over()

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
        Screens.GAME.add_element(self.state.powerup_group)
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
            if (
                event.type == pygame.KEYDOWN
                and self.up_arrow in self.state.current_screen.elements
                and event.key == pygame.K_UP
            ):
                self.state.launch_ball()
                self.state.current_screen.elements.remove(self.up_arrow)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.state.paused:
                    self.resume_game()
                else:
                    self.pause_game()

            self.state.current_screen.handle_event(event)

    def update_game(self):
        """Handle the gameplay"""
        if (
            self.state.paused
            or self.state.game_is_over
            or self.state.current_screen != Screens.GAME
        ):
            return

        # Check for GUI arrow press for launching the ball.
        if self.up_arrow.pressed:
            self.state.launch_ball()
            if self.up_arrow in self.state.current_screen.elements:
                self.state.current_screen.elements.remove(self.up_arrow)

        # if the ball is waiting for launch, ensure the up arrow is on screen.
        if not self.state.launched:
            if self.up_arrow not in self.state.current_screen.elements:
                self.up_arrow = ArrowButton("up")
                self.state.current_screen.add_element(self.up_arrow)
            return

        # Ball has been launched, allow movement.
        self.move_game_pieces()

    def move_game_pieces(self):
        """Move the paddles, balls, and powerups on the screen"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or self.left_arrow.pressed:
            for paddle in self.state.paddle_group.sprites():
                paddle.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.right_arrow.pressed:
            for paddle in self.state.paddle_group.sprites():
                paddle.move_right()

        for ball in self.state.ball_group.sprites():
            self.state = ball.move(screen_size, self.state)

        for powerup in self.state.powerup_group.sprites():
            powerup.move(self.state)

    def run(self):
        """Run the main game loop"""
        while True:
            self.handle_events()
            self.update_game()
            self.state.update()

            self.state.current_screen.draw(self.window)
            pygame.display.update()
            time = self.clock.tick(50)
            if not self.state.paused and self.state.launched:
                self.state.time += time


class GameState:
    """Manages the game's current state and flags for transitions."""

    def __init__(self, screen: ScreenManager = Screens.START):
        """Reset the game state for a new game."""
        self.level = 1
        self.score = 0  # Default starting score
        self.lives = 3  # Default starting lives
        self.time = 0
        self.bricks = Brick.create_brick_layout(rows=6, cols=8, level=self.level)
        self.ball_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.paddle_group = pygame.sprite.Group()
        self.ball = Ball(self.ball_group)
        self.paddle = Paddle(self.paddle_group)
        self.score_display = ScoreDisplay(self.score)
        self.lives_display = LivesDisplay(self.lives)
        self.launch_message = BlinkingMessage("Press ↑ to Launch!")
        self.pause_message = BlinkingMessage("Paused!", blink_interval=500)
        self.current_screen: ScreenManager = screen

        # Power-up spawn timing
        self.min_wait_time = 15 * 1000  # 15 seconds in milliseconds
        self.max_wait_time = 30 * 1000  # 30 seconds in milliseconds
        self.next_powerup_time = self.time + random.randint(
            self.min_wait_time, self.max_wait_time
        )

        # State flags
        self.launched = False
        self.paused = False
        self.game_is_over = False

        self.powerup_choices = [
            lambda: PowerUp(
                self.powerup_group, power=self.add_paddle, shape="rectangle"
            ),
            lambda: PowerUp(
                self.powerup_group,
                power=self.add_ball,
            ),
            lambda: PowerDown(self.powerup_group, power=self.lose_life),
        ]

    def update(self):
        """Update the game based on the current state"""
        if self.game_is_over:
            self.current_screen = Screens.END
        if self.current_screen != Screens.GAME or self.paused:
            # game state only changes if we're still in the game
            return

        # broke all bricks, go again
        remaining_breakable = [
            brick for brick in self.bricks.sprites() if brick.breakable
        ]
        if len(remaining_breakable) == 0:
            for ball in self.ball_group.sprites():
                ball.increase_speed()  # Increase speed for each ball
                ball.reset_position()
            self.launch_ball()
            self.bricks = Brick.create_brick_layout(rows=6, cols=8, level=self.level)
            Screens.GAME.add_element(self.bricks)

        if not self.launched:
            if self.launch_message not in self.current_screen.elements:
                self.current_screen.add_element(self.launch_message)
            # game state can only change if we're launched
            return

        if (
            self.time >= self.next_powerup_time
            and len(self.powerup_group.sprites()) == 0
        ):
            self.add_powerup()

        for paddle in self.paddle_group.sprites():
            if paddle.timeout:
                # temp paddle, update it
                paddle.check_timeout(self.time)

        self.score_display.update(self.score)
        self.lives_display.update(self.lives)

    def add_powerup(self):
        """
        Choose a random powerup and add it to the screen
        Only allow one paddle powerup at a time to avoid confusion
        """
        if len(self.paddle_group.sprites()) > 1:
            random_powerup = random.choice(self.powerup_choices[1:])
        else:
            random_powerup = random.choice(self.powerup_choices)
        random_powerup()

        self.next_powerup_time = self.time + random.randint(
            self.min_wait_time, self.max_wait_time
        )

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
        if self.pause_message not in self.current_screen.elements:
            self.current_screen.add_element(self.pause_message)

    def resume_game(self):
        """Resume the game."""
        self.paused = False
        if self.pause_message in self.current_screen.elements:
            self.current_screen.elements.remove(self.pause_message)

    def game_over(self):
        """Mark game as over."""
        self.game_is_over = True
        sound.SoundManager.play_game_over()
        sound.SoundManager.stop_other_sounds()

    def add_ball(self):
        """Add a ball to the game"""
        try:
            power_up = self.powerup_group.sprites()[0]
        except IndexError:
            # pull from where the paddle is if you can't find the powerup
            power_up = self.paddle_group.sprites()[0]
        power_up_position: pygame.Rect = power_up.rect

        # Get the current speed from an existing ball if available; otherwise, use the default
        if self.ball_group.sprites():
            current_speed = self.ball_group.sprites()[0].current_speed
        else:
            current_speed = BallConfig.DEFAULT_SPEED

        # Create the new ball with the current speed (using a negative value for upward motion)
        new_ball = Ball(
            self.ball_group,
            x_position=power_up_position.center[0],
            color=random.choice(color_choices),
            speed_y=-current_speed,
        )
        # Ensure the new ball's speed is set properly
        new_ball.current_speed = current_speed

    def add_paddle(self):
        """
        Add a new paddle to the screen as a powerup

        This paddle is twice as big and appears centered on the original
        """
        Paddle(
            self.paddle_group,
            x_position=self.paddle.x_position
            - (Paddle.width // 2),  # in the center of the current paddle
            width=Paddle.width * 2,  # twice as big
            color=random.choice(color_choices),
            timeout=self.time
            + random.randint(
                self.min_wait_time, self.max_wait_time
            ),  # when it should disappear
        )

    def lose_life(self):
        """Lose a life"""
        self.lives -= 1

        if self.lives < 1:
            self.game_over()
            return

        sound.SoundManager.play_life_lost()
        for ball in self.ball_group.sprites():
            ball.reset_position()
        for paddle in self.paddle_group.sprites():
            paddle.reset_position()

        self.launched = False


if __name__ == "__main__":
    Game().run()
