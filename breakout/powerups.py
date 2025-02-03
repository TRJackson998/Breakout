"""
Powerups
========
Implement the Powerups object and related interactions/physics
Power Ups are circles that move from the top of the screen down
If the paddle collides with a power up, the player receives that power
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

Developer
---------
Terrence

Last Edited
-----------
1.20.25
"""

from breakout.sprite import BreakoutSprite


class PowerUp(BreakoutSprite):
    """Handle power up execution"""

    def __init__(self, *groups, radius=0):
        super().__init__(
            *groups,
        )
        self.radius = radius
