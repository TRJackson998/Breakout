"""
Score
========
Tracks and displays the player's score, manages the leaderboard, and 
handles name input for high scores. Updates the screen with real-time scoring information.

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

import pygame
from pygame.font import SysFont

from breakout import screen_size

# pylint: disable=no-member


class Scoreboard:
    """Handles the leaderboard display."""

    _font = SysFont("courier", max(screen_size.width // 20, 12))

    def __init__(self):
        self.text_color = pygame.Color("white")
        self.top_scores = {}

    def draw(self, screen: pygame.Surface):
        """Draws the scoreboard on the screen."""
        # Display top scores
        title_str = "Leaderboard"
        title_text = Scoreboard._font.render(title_str, True, self.text_color)
        screen.blit(title_text, (screen_size.width // 3, 80))

        for i, (score, name) in enumerate(self.top_scores.items()):
            formatted_score = f"{score:,}"  # Format score with commas
            entry_text = f"{formatted_score}{'.' * (20 - len(name) - len(formatted_score))}{name}"
            score_text = Scoreboard._font.render(entry_text, True, self.text_color)
            screen.blit(score_text, (screen_size.width // 5, 110 + i * 30))


class NameInput:
    """Handles user input for entering a name."""

    def __init__(self):
        self.font_size = max(screen_size.width // 20, 12)
        self.font = SysFont("courier", self.font_size)
        self.active_color = pygame.Color("green")
        self.passive_color = pygame.Color("#0ffffd")
        self.active = False
        self.name = ""
        self.width = max(screen_size.width // 20, self.font_size * 3)
        self.height = max(screen_size.width // 20, self.font_size)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.passive_color)
        self.x_position = screen_size.width // 2 + self.width // 2
        self.y_position = self.height // 2
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))

    def handle_event(self, event: pygame.event.Event):
        """
        Processes mouse and keyboard events to update the name input field.
        Activates the input field on mouse click and updates the name with keyboard input.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pygame.KEYDOWN:
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                self.name = self.name[:-1]
            elif event.key in range(pygame.K_a, pygame.K_z + 1):
                self.name += (
                    event.unicode
                )  # Unicode standard is used for string formation
                self.name = str.upper(self.name)

    def draw(self, screen: pygame.Surface):
        """Draw the name input field."""
        self.name = self.name[:3]
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.rect)
            name_surface = self.font.render(self.name, True, pygame.Color("black"))
        else:
            pygame.draw.rect(screen, self.passive_color, self.rect)
            name_surface = self.font.render(self.name, True, pygame.Color("black"))
        name_rect = name_surface.get_rect(center=self.rect.center)
        screen.blit(name_surface, name_rect)

        name_label = self.font.render("Name: ", True, pygame.Color("white"))
        label_rect = name_label.get_rect(
            center=(self.rect.x - 50, self.rect.y + (self.rect.height // 2))
        )
        screen.blit(name_label, label_rect)


class ScoreDisplay:
    """Tracks and displays the current score in real-time."""

    _font = SysFont("courier", 14, bold=True)

    def __init__(self, score: int = 0):
        self.current_score = score

    def update(self, score: int):
        """Update the score display value"""
        self.current_score = score

    def draw(self, screen: pygame.Surface):
        """Draw the current score on the screen."""
        current_score_text = ScoreDisplay._font.render(
            f"Current Score: {self.current_score}", True, pygame.Color("black")
        )
        screen.blit(
            current_score_text, (0, screen_size.height - screen_size.height // 15)
        )


class LivesDisplay:
    """Displays the player's remaining lives on the screen."""

    _font = SysFont("courier", 14, bold=True)

    def __init__(self, lives=2):
        self.lives = lives

    def update(self, lives: int):
        """Update the number of lives displayed."""
        self.lives = lives

    def draw(self, screen: pygame.Surface):
        """Draw the lives display on the screen."""
        # Draw the lives text above the current score
        lives_text = LivesDisplay._font.render(
            f"Lives: {self.lives}", True, pygame.Color("black")
        )
        screen.blit(lives_text, (0, screen_size.height - screen_size.height // 15 - 30))
