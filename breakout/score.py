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
        self.top_scores = {
            "AAA": 0,
            "BBB": 0,
            "CCC": 0,
            "DDD": 0,
            "EEE": 0,
            "FFF": 0,
            "GGG": 0,
            "HHH": 0,
            "III": 0,
            "JJJ": 0,
        }

    def save_score(self, score: int, name: str):
        """Saves the current score to the leaderboard and resets it."""
        self.top_scores[name] = score  # update this player's top score
        self.top_scores = dict(
            sorted(self.top_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        )  # Sort, only keep only the top 10 scores

    def draw(self, screen: pygame.surface.Surface):
        """Draws the scoreboard on the screen."""
        # Display top scores
        title_str = "Leaderboard"
        title_text = Scoreboard._font.render(title_str, True, Color("white"))
        screen.blit(title_text, (screen_size.width // 3, 80))

        for i, (name, score) in enumerate(self.top_scores.items()):
            formatted_score = f"{score:,}"  # Format score with commas
            entry_text = f"{formatted_score}{'.' * (20 - len(name) - len(formatted_score))}{name}"
            score_text = Scoreboard._font.render(entry_text, True, Color("white"))
            screen.blit(score_text, (screen_size.width // 4, 120 + i * 30))


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
