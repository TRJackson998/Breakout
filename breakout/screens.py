"""
Screens
=======
Defines and manages the different game screens, including the 
start, gameplay, and end screens. Handles button interactions and visual updates.

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

from dataclasses import dataclass
from typing import Literal

import pygame
from pygame.color import Color
from pygame.font import SysFont
from breakout.sound import SoundManager
from breakout import screen_size

# pylint: disable=no-member


class ScreenManager:
    """
    Class to contain various elements of a screen and draw them
    Theoretically should only be instantiated in this script
    """

    def __init__(self, elements: list, background_image: pygame.Surface = None):
        self.elements = elements
        self.background_image = background_image

    def add_element(self, element):
        """Give the Screen another element"""
        self.elements.append(element)

    def draw(self, pygame_window: pygame.Surface):
        """Draw the Screen."""
        if self.background_image:
            bg = pygame.transform.scale(self.background_image, pygame_window.get_size())
            pygame_window.blit(bg, (0, 0))
        else:
            pygame_window.fill(
                pygame.Color("black")
            )  # clear screen if no background image

        for element in self.elements:
            element.draw(pygame_window)

    def handle_event(self, event: pygame.event.Event):
        """Send the event to all elements that might need to respond."""
        for element in self.elements:
            try:
                # Button elements on the screen run functions when clicked
                element.handle_event(event)
            except AttributeError:
                # Groups of Sprites like bricks do not handle events
                pass


class Button:
    """
    A class to create Button objects

    Buttons have text, run an 'on_click' function, and change color when a mouse hovers over them
    Position is used to determine where to place the button. There are 2-3 buttons per screen,
    with fixed positioning - top middle and bottom. Most screens have 'middle' and 'bottom' buttons.
    """

    _font = SysFont("courier", 15, bold=True)

    def __init__(
        self,
        text: str,
        on_click,
        position: Literal["top", "middle", "bottom"],
        color: pygame.Color = pygame.Color("#0ffffd"),
        hover_color: pygame.Color = pygame.Color("green"),
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

        if position == "middle":
            # two button's worth up from the bottom of the screen
            y = screen_size.height - ((height + pad) * 2)
        elif position == "bottom":
            # one button's worth up from the bottom of the screen
            y = screen_size.height - height - pad
        elif position == "top":
            x = screen_size.width // 2
            y = screen_size.width // 40 + height // 2
        else:
            raise ValueError("Not a valid button position")

        # make the rectangle
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen: pygame.Surface):
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

        # Draw white border
        pygame.draw.rect(screen, pygame.Color("white"), self.rect, 3)

        # get the center of the rectangle and blit the text onto the screen there
        text_surface = Button._font.render(self.text, True, pygame.Color("black"))
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

    def update_button(self, text: str, on_click):
        "Change button display and functionality"
        self.text = text
        self.on_click = on_click


class ArrowButton:
    """A special button type in the shape of an arrow"""

    def __init__(self, direction: Literal["left", "right", "up"]):
        self.pressed = False
        self.color: Color = Color("grey")
        self.hover_color: Color = Color("white")
        width = 40
        height = 30

        if direction == "right":
            x, y = (screen_size.width - 100, screen_size.height - 40)
            self.arrow_points = [
                (x, y - height // 4),  # Left base top
                (x + width, y - height // 4),  # Right base top
                (x + width, y - height // 2),  # Bottom corner of arrowhead
                (x + width * 2, y),  # Arrowhead tip
                (x + width, y + height // 2),  # Top corner of arrowhead
                (x + width, y + height // 4),  # Right base bottom
                (x, y + height // 4),  # Left base bottom
            ]
        elif direction == "left":
            x, y = (screen_size.width - 187, screen_size.height - 40)
            self.arrow_points = [
                (x + width * 2, y - height // 4),
                (x + width, y - height // 4),
                (x + width, y - height // 2),
                (x, y),
                (x + width, y + height // 2),
                (x + width, y + height // 4),
                (x + width * 2, y + height // 4),
            ]
        elif direction == "up":
            x, y = (screen_size.width - 104, screen_size.height - 135)
            height = 40
            width = 30
            self.arrow_points = [
                (x - width // 4, y + height * 2),  # Bottom left of base
                (x - width // 4, y + height),  # Top left of base
                (x - width // 2, y + height),  # Left corner of arrowhead
                (x, y),  # Arrowhead tip
                (x + width // 2, y + height),  # Right corner of arrowhead
                (x + width // 4, y + height),  # Top right of base
                (x + width // 4, y + height * 2),  # Bottom right of base
            ]

        center_x = sum(point[0] for point in self.arrow_points) // 7
        center_y = sum(point[1] for point in self.arrow_points) // 7
        top = center_x - width // 1.5
        left = center_y - height // 1.5
        self.rect = pygame.Rect(
            top, left, width * 1.5, height * 1.5
        )  # Rough bounding box

        self.direction = direction

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
            pygame.draw.polygon(screen, self.hover_color, self.arrow_points)
        else:
            # mouse is not hovering, draw button in color, render text in hover color
            pygame.draw.polygon(screen, self.color, self.arrow_points)

    def handle_event(self, event: pygame.event.Event):
        """If this button is clicked, run the function associated with it"""
        if (
            event.type == pygame.MOUSEBUTTONDOWN  # a mouse has been clicked
            and event.button == 1  # the left mouse button has been clicked
            and self.rect.collidepoint(event.pos)  # the event collided with this button
        ):
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False


class BlinkingMessage:
    """Displays a launch message with blinking effect."""

    _font = SysFont("courier", max(screen_size.width // 20, 14))

    def __init__(
        self,
        text: str,
        pos: tuple[int, int] = None,
        text_color: pygame.Color = pygame.Color("white"),
        background_color: pygame.Color = pygame.Color("blue"),
        blink_interval: int = 1000,
        padding: int = 10,
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
            rendered_text = BlinkingMessage._font.render(
                self.text, True, self.text_color
            )
            text_rect = rendered_text.get_rect(center=self.pos)

            bg_rect = text_rect.inflate(self.padding * 2, self.padding * 2)

            # Draw the background rectangle.
            pygame.draw.rect(screen, self.background_color, bg_rect)

            # Blit the text on top of the rectangle.
            screen.blit(rendered_text, text_rect)


class MusicToggle:
    """GUI to allow user to turn off the background music"""

    def __init__(self, x=10, y=10, font=None, initial_state=True):
        self.x = x
        self.y = y
        self.music_on = initial_state
        self.label = "MUSIC: "
        self.text_on = "ON"
        self.text_off = "OFF"
        self.font = font if font else SysFont("courier", 16, bold=True)

        # Colors for label and options.
        self.label_color = pygame.Color("#0ffffd")
        self.highlight_color = pygame.Color("#0ffffd")
        self.normal_color = pygame.Color("gray")

        self.label_surface = self.font.render(self.label, True, self.label_color)
        self.label_rect = self.label_surface.get_rect(topleft=(x, y))

        # Position ON and OFF texts to the right of the label.
        self.on_offset = 5  # space between label and ON
        self.between_offset = 10  # space between ON and OFF

        self.on_surface = self.font.render(
            self.text_on,
            True,
            self.highlight_color if self.music_on else self.normal_color,
        )
        self.off_surface = self.font.render(
            self.text_off,
            True,
            self.normal_color if self.music_on else self.highlight_color,
        )
        self.on_rect = self.on_surface.get_rect(
            topleft=(self.label_rect.right + self.on_offset, y)
        )
        self.off_rect = self.off_surface.get_rect(
            topleft=(self.on_rect.right + self.between_offset, y)
        )

        # Set the music state.
        if self.music_on:
            SoundManager.play_background_music()
        else:
            SoundManager.stop_background_music()

    def draw(self, surface: pygame.Surface):
        # Draw the label.
        surface.blit(self.label_surface, self.label_rect)
        # Re-render ON and OFF texts according to state.
        if self.music_on:
            self.on_surface = self.font.render(self.text_on, True, self.highlight_color)
            self.off_surface = self.font.render(self.text_off, True, self.normal_color)
        else:
            self.on_surface = self.font.render(self.text_on, True, self.normal_color)
            self.off_surface = self.font.render(
                self.text_off, True, self.highlight_color
            )
        surface.blit(self.on_surface, self.on_rect)
        surface.blit(self.off_surface, self.off_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.on_rect.collidepoint(event.pos):
                if not self.music_on:
                    self.music_on = True
                    SoundManager.play_background_music()
            elif self.off_rect.collidepoint(event.pos):
                if self.music_on:
                    self.music_on = False
                    SoundManager.stop_background_music()


@dataclass
class Screens:
    """
    Store all my screen objects here
    Then I can do things like Screens.START.draw()
    Init the screens here, fill in elements later to avoid circular logic
    """

    START = ScreenManager([])
    GAME = ScreenManager([])
    END = ScreenManager([])
