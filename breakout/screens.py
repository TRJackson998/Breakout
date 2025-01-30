"""
Screens
=======
Classes related to building the various screens of our game

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
1.25.25
"""

from dataclasses import dataclass
from typing import Literal

import pygame
from pygame.color import Color
from pygame.font import Font, SysFont
from pygame.surface import Surface

from breakout import screen_size


class _Screen:
    """
    Class to contain various elements of a screen and draw them
    Theoretically should only be instantiated in this script
    """

    def __init__(self, elements: list):
        self.elements = elements

    def add_element(self, element):
        """Give the Screen another element"""
        self.elements.append(element)

    def draw(self, pygame_window: Surface):
        """Draw the Screen"""
        pygame_window.fill(Color("black"))  # clear screen
        for element in self.elements:
            element.draw(pygame_window)


class Button:
    """
    A class to create Button objects

    Buttons have text, run an 'on_click' function, and change color when a mouse hovers over them
    Position is used to determine where to place the button. There will be two buttons
    on each screen, so buttons can be in two positions: top or bottom.
    """

    # dynamically determine with screen size, never below 12pt font
    _font = Font(None, max(screen_size.width // 20, 12))

    def __init__(
        self,
        text: str,
        on_click,
        position: Literal["top", "bottom"],
        color: Color = Color("blue"),
        hover_color: Color = Color("gray"),
    ):
        self.text = text
        self.on_click = on_click
        self.color = color
        self.hover_color = hover_color

        # dynamically determine button size based on screen size
        # max() to never make them so small they can't be seen
        width: int = max(screen_size.width // 5, 50)
        pad: int = screen_size.width // 100
        height: int = max(screen_size.height // 15, 12 + pad)

        # dynamically place in middle of the screen
        x = (screen_size.width // 2) - (width // 2)

        # if it's the top or bottom button
        if position == "top":
            # two button's worth up from the bottom of the screen
            y = screen_size.height - ((height + pad) * 2)
        else:
            # one button's worth up from the bottom of the screen
            y = screen_size.height - height - pad

        # make the rectangle
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen: pygame.surface.Surface):
        """
        Screen elements need to be able to draw themselves
        Write the button text using the font
        Blit the rectangle on the screen
        """
        # Determine if mouse is hovering over this button
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # mouse is hovering, draw button in hover color, text in color
            pygame.draw.rect(screen, self.hover_color, self.rect)
            text_surface = Button._font.render(self.text, True, self.color)
        else:
            # mouse is not hovering, draw button in color, render text in hover color
            pygame.draw.rect(screen, self.color, self.rect)
            text_surface = Button._font.render(self.text, True, self.hover_color)

        # get the center of the rectangle and blit the text onto the screen there
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event):
        """If this button is clicked, run the function associated with it"""
        if (
            event.type == pygame.MOUSEBUTTONDOWN  # a mouse has been clicked
            and event.button == 1  # the left mouse button has been clicked
            and self.rect.collidepoint(event.pos)  # the event collided with this button
        ):
            # run the function associated with this button
            self.on_click()


@dataclass
class Screens:
    """
    Store all my screen objects here
    Then I can do things like Screens.START.draw()
    Init the screens here, fill in elements later to avoid circular logic
    """

    START = _Screen([])
    GAME = _Screen([])
    END = _Screen([])


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
