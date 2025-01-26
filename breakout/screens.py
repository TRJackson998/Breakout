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


class _Button:
    """
    A class to create Button objects, private to screens.py

    Buttons have text, run an 'on_click' function, and change color when a mouse hovers over them
    Position is used to determine where to place the button. There will be two buttons
    on each screen, so buttons can be in two positions: top or bottom.
    """

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
        width: int = screen_size.width // 5
        height: int = screen_size.height // 15
        pad: int = screen_size.width // 100

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


@dataclass
class Screens:
    """
    Store all my screen objects here
    Then I can do things like Screens.START.draw()
    TBD fill in all the elements belonging to each screen
    This is the class to access outside this script
    """

    START = _Screen([])
    GAME = _Screen([])
    END = _Screen([])
