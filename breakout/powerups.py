"""
Powerups
========
Implement the Powerups object and related interactions/physics
Subclass of BreakoutSprite

Powers
------
Paddle size bigger
Ball size bigger
Paddle speed faster
Ball speed slower
Extra paddle
Extra ball
Extra life

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

from pygame.sprite import Sprite


class PowerUp(Sprite):
    """Handle power up execution"""

    def __init__(self, *groups, radius=0):
        super().__init__(
            *groups,
        )
        self.radius = radius
