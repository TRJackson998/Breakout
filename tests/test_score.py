"""
Test Score
==========
Test file for the scoreboard and name input

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

from breakout import screen_size
from breakout.score import LivesDisplay, NameInput, Scoreboard, ScoreDisplay


def test_scoreboard_initialization():
    """Test that the scoreboard initializes correctly."""
    scoreboard = Scoreboard()
    assert isinstance(scoreboard.top_scores, dict)
    assert not scoreboard.top_scores


def test_scoreboard_draw():
    """Test that the scoreboard's draw method executes without error."""
    scoreboard = Scoreboard()
    screen = pygame.Surface((screen_size.width, screen_size.height))

    scoreboard.draw(screen)


def test_name_input_initialization():
    """Test that the name input initializes correctly."""
    name_input = NameInput()
    assert name_input.name == ""
    assert name_input.active is False


def test_name_input_handle_mouse_event():
    """Test mouse click activation in the NameInput field."""
    name_input = NameInput()

    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": name_input.rect.center})
    name_input.handle_event(event)

    assert name_input.active is True


def test_name_input_handle_keyboard_event():
    """Test keyboard input handling for NameInput."""
    name_input = NameInput()
    name_input.active = True

    # Simulate typing 'A'
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "A"})
    name_input.handle_event(event)

    assert name_input.name == "A"

    # Simulate backspace
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_BACKSPACE})
    name_input.handle_event(event)

    assert name_input.name == ""


def test_name_input_draw():
    """Test that the name input's draw method executes without error."""
    name_input = NameInput()
    screen = pygame.Surface((screen_size.width, screen_size.height))

    name_input.draw(screen)


def test_score_display_initialization():
    """Test that the score display initializes with the correct score."""
    score_display = ScoreDisplay(score=10)
    assert score_display.current_score == 10


def test_score_display_update():
    """Test updating the score display."""
    score_display = ScoreDisplay()
    score_display.update(50)

    assert score_display.current_score == 50


def test_score_display_draw():
    """Test that the score display's draw method executes."""
    score_display = ScoreDisplay(score=25)
    screen = pygame.Surface((screen_size.width, screen_size.height))

    score_display.draw(screen)


def test_lives_display_initialization():
    """Test that the lives display initializes correctly."""
    lives_display = LivesDisplay(lives=5)
    assert lives_display.lives == 5


def test_lives_display_update():
    """Test updating the lives display."""
    lives_display = LivesDisplay()
    lives_display.update(1)

    assert lives_display.lives == 1


def test_lives_display_draw():
    """Test that the lives display's draw method executes"""
    lives_display = LivesDisplay(lives=3)
    screen = pygame.Surface((screen_size.width, screen_size.height))

    lives_display.draw(screen)
