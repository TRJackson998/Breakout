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

from pygame.color import Color
from pygame.surface import Surface


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
