"""
Score
========
Implement the leaderboard
Implement score tracking display during gameplay

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
from pygame.color import Color
from pygame.font import Font, SysFont
from pygame.surface import Surface

from breakout import screen_size


class Scoreboard:
    _font = SysFont("courier", max(screen_size.width // 20, 12))

    def __init__(self):
        self.text_color = Color("white")
        self.top_scores = {-1: "AAA"}

    def draw(self, screen: pygame.surface.Surface):
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
    def __init__(self):
        self.font_size = max(screen_size.width // 20, 12)
        self.font = SysFont("courier", self.font_size)
        self.active_color = Color("blue")
        self.passive_color = Color("grey")
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

    def draw(self, screen: pygame.surface.Surface):
        self.name = self.name[:3]
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.rect)
            name_surface = self.font.render(self.name, True, self.passive_color)
        else:
            pygame.draw.rect(screen, self.passive_color, self.rect)
            name_surface = self.font.render(self.name, True, self.active_color)
        name_rect = name_surface.get_rect(center=self.rect.center)
        screen.blit(name_surface, name_rect)

        name_label = self.font.render("Name: ", True, Color("white"))
        label_rect = name_label.get_rect(
            center=(self.rect.x - 50, self.rect.y + (self.rect.height // 2))
        )
        screen.blit(name_label, label_rect)


class CurrentScore:
    _font = Font(None, max(screen_size.width // 20, 12))

    def __init__(self):
        self.current_score = 0

    def increase_score(self, score: int):
        self.current_score += score  # Increase current score

    def draw(self, screen: pygame.surface.Surface):
        # Display current score
        current_score_text = CurrentScore._font.render(
            f"Current Score: {self.current_score}", True, Color("white")
        )
        screen.blit(
            current_score_text, (0, screen_size.height - screen_size.height // 15)
        )
