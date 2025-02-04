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
        self.top_scores = {-1: "AAA"}

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
            screen.blit(score_text, (screen_size.width // 4, 120 + i * 30))

        for i in range(10 - len(self.top_scores)):
            score = -1
            name = "AAA"
            formatted_score = f"{score:,}"  # Format score with commas
            entry_text = f"{formatted_score}{'.' * (20 - len(name) - len(formatted_score))}{name}"
            score_text = Scoreboard._font.render(entry_text, True, self.text_color)
            screen.blit(
                score_text,
                (screen_size.width // 4, 120 + (i + len(self.top_scores)) * 30),
            )


class NameInput:
    """Handles user input for entering a name."""

    def __init__(self):
        self.font_size = max(screen_size.width // 20, 12)
        self.font = SysFont("courier", self.font_size)
        self.active_color = pygame.Color("blue")
        self.passive_color = pygame.Color("grey")
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
        """If this button is clicked, run the function associated with it"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pygame.KEYDOWN:
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                self.name = self.name[:-1]

            # Unicode standard is used for string
            # formation
            else:
                self.name += event.unicode

    def draw(self, screen: pygame.Surface):
        """Draw the name input field."""
        self.name = self.name[:3]
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.rect)
            name_surface = self.font.render(self.name, True, self.passive_color)
        else:
            pygame.draw.rect(screen, self.passive_color, self.rect)
            name_surface = self.font.render(self.name, True, self.active_color)
        name_rect = name_surface.get_rect(center=self.rect.center)
        screen.blit(name_surface, name_rect)

        name_label = self.font.render("Name: ", True, pygame.Color("white"))
        label_rect = name_label.get_rect(
            center=(self.rect.x - 50, self.rect.y + (self.rect.height // 2))
        )
        screen.blit(name_label, label_rect)


class CurrentScore:
    """Tracks and displays the current score."""

    _font = SysFont("courier", max(screen_size.width // 30, 12))

    def __init__(self):
        self.current_score = 0

    def increase_score(self, score: int):
        """Increase the current score by the given value."""
        self.current_score += score

    def draw(self, screen: pygame.Surface):
        """Draw the current score on the screen."""
        current_score_text = CurrentScore._font.render(
            f"Current Score: {self.current_score}", True, pygame.Color("white")
        )
        screen.blit(
            current_score_text, (0, screen_size.height - screen_size.height // 15)
        )


class LivesDisplay:
    """Displays the player's remaining lives."""

    _font = SysFont("courier", max(screen_size.width // 30, 12))

    def __init__(self, lives=2):
        self.lives = lives

    def update(self, lives):
        """Update the number of lives displayed."""
        self.lives = lives

    def draw(self, screen: pygame.Surface):
        """Draw the lives display on the screen."""
        # Draw the lives text above the current score
        lives_text = LivesDisplay._font.render(
            f"Lives: {self.lives}", True, pygame.Color("white")
        )
        screen.blit(lives_text, (0, screen_size.height - screen_size.height // 15 - 30))


class LaunchMessage:
    """Displays a launch message with blinking effect."""

    _font = SysFont("courier", max(screen_size.width // 20, 14))

    def __init__(
        self,
        text="Press ↑ to Launch!",
        pos=None,
        text_color=pygame.Color("white"),
        background_color=pygame.Color("blue"),
        blink_interval=1000,
        padding=10,
    ):
        self.text = text
        self.text_color = text_color
        self.background_color = background_color
        self.padding = padding
        if pos is None:
            self.pos = (screen_size.width // 2, screen_size.height // 2)
        else:
            self.pos = pos
        self.blink_interval = blink_interval
        self.last_toggle = pygame.time.get_ticks()
        self.visible = True

    def draw(self, screen: pygame.Surface):
        """Draw the launch message on the screen."""
        # Toggle visibility based on time elapsed for blinking effect.
        now = pygame.time.get_ticks()
        if now - self.last_toggle > self.blink_interval:
            self.visible = not self.visible
            self.last_toggle = now

        if self.visible:
            # Render the text.
            rendered_text = LaunchMessage._font.render(self.text, True, self.text_color)
            text_rect = rendered_text.get_rect(center=self.pos)

            bg_rect = text_rect.inflate(self.padding * 2, self.padding * 2)

            # Draw the background rectangle.
            pygame.draw.rect(screen, self.background_color, bg_rect)

            # Blit the text on top of the rectangle.
            screen.blit(rendered_text, text_rect)
