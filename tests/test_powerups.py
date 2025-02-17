"""
Test Powerups
=============
Test file for powerup actions

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

from unittest.mock import Mock

import pygame

from breakout import screen_size
from breakout.__main__ import GameState
from breakout.paddle import Paddle
from breakout.powerups import PowerDown, PowerUp, PowerupConfig
from breakout.screens import Screens


def test_powerup_initialization():
    """Test power-up initializes with correct attributes."""
    powerup = PowerUp(power=lambda: None, shape="rectangle")  # Test rectangle power-up

    assert powerup.position.x >= PowerupConfig.size * 5
    assert powerup.position.x <= screen_size.width - PowerupConfig.size * 5
    assert powerup.position.y == 15  # Power-up starts near the top
    assert powerup.speed == PowerupConfig.default_speed
    assert powerup.shape == "rectangle"  # Ensures rectangle initialization
    assert isinstance(powerup.color, int)


def test_powerup_movement():
    """Test power-up moves downward."""
    powerup = PowerUp(power=lambda: None)
    initial_y = powerup.position.y
    powerup.update_position()

    assert (
        powerup.position.y > initial_y
    ), f"Expected power-up to move down, but got {powerup.position.y}"


def test_powerup_paddle_collision():
    """Test power-up is collected when hitting the paddle."""
    mock_power_effect = Mock()
    paddle = Paddle()
    powerup = PowerUp(power=mock_power_effect)

    powerup.rect.bottom = paddle.rect.top + 1  # Ensure overlap with the paddle
    powerup.rect.centerx = paddle.rect.centerx
    powerup.speed.y = 2.5

    # Simulate collision
    powerup.handle_paddle_collision(paddle)

    # Assert that the power-up effect was executed.
    mock_power_effect.assert_called_once()

    # Assertions
    assert not powerup.alive(), "Expected power-up to be removed after being collected."


def test_powerup_falls_off_screen():
    """Test power-up disappears when falling off the screen."""
    state = GameState()  # Create game state
    powerup = PowerUp(power=lambda: None)

    # Move power-up below the screen
    powerup.position.y = screen_size.height + 10
    powerup.move(state)  # Pass the correct game state

    assert (
        powerup.alive() is False
    ), "Expected power-up to be removed after falling off-screen."


def test_powerup_color_cycling():
    """Test circle-shaped power-up cycles through colors correctly."""
    powerup = PowerUp(power=lambda: None)

    initial_color = powerup.color
    powerup.last_toggle = pygame.time.get_ticks() - (
        PowerupConfig.blink_interval + 1
    )  # Force a time update

    # Passed in a dummy state for required arugment
    dummy_state = GameState(Screens.GAME)
    powerup.move(dummy_state)

    assert (
        powerup.color != initial_color
    ), f"Expected power-up to change color, but it is still : {powerup.color}"


def test_powerup_rectangle_color_change():
    """Test rectangle-shaped power-up changes color correctly."""
    powerup = PowerUp(power=lambda: None, shape="rectangle")

    initial_color = powerup.color
    powerup.last_toggle = pygame.time.get_ticks() - (
        PowerupConfig.blink_interval + 1
    )  # Force time update
    # Passed in a dummy state for required arugment
    dummy_state = GameState(Screens.GAME)
    powerup.move(dummy_state)

    assert (
        powerup.color != initial_color
    ), f"Expected color to change, but it stayed {powerup.color}"


def test_powerup_text_position_update():
    """Test that the power-up text updates position correctly."""
    powerup = PowerUp(power=lambda: None)

    powerup.update_position()

    # Verify the text surface exists.
    assert powerup.text_surface is not None, "Expected text surface to exist."

    text_rect = powerup.text_surface.get_rect(center=powerup.rect.center)

    assert text_rect.center == powerup.rect.center, (
        f"Expected text surface center {text_rect.center} "
        + "to match power-up center {powerup.rect.center}."
    )


def test_powerdown_initialization():
    """Test power-down initializes with correct attributes."""
    powerdown = PowerDown(power=lambda: None)

    assert powerdown.position.x >= PowerupConfig.size * 5
    assert powerdown.position.x <= screen_size.width - PowerupConfig.size * 5
    assert powerdown.position.y == PowerupConfig.initial_y
    assert powerdown.speed == PowerupConfig.default_speed
    assert not powerdown.exploded


def test_powerdown_movement():
    """Test power-down moves downward."""
    powerdown = PowerDown(power=lambda: None)
    initial_y = powerdown.position.y
    powerdown.update_position()

    assert (
        powerdown.position.y > initial_y
    ), f"Expected power-down to move down, but got {powerdown.position.y}"


def test_powerdown_paddle_collision():
    """Test power-down is collected when hitting the paddle."""
    mock_power_effect = Mock()
    paddle = Paddle()
    powerdown = PowerDown(power=mock_power_effect)

    powerdown.rect.bottom = paddle.rect.top + 1  # Ensure overlap with the paddle
    powerdown.rect.centerx = paddle.rect.centerx
    powerdown.speed.y = 2.5

    # Simulate collision
    powerdown.handle_paddle_collision(paddle)

    # Assertions
    assert powerdown.exploded
    assert powerdown.speed.y == 0  # stopped moving


def test_powerdown_falls_off_screen():
    """Test power-down disappears when falling off the screen."""
    state = GameState()  # Create game state
    powerdown = PowerDown(power=lambda: None)

    # Move power-down below the screen
    powerdown.position.y = screen_size.height + 10
    powerdown.move(state)  # Pass the correct game state

    assert (
        powerdown.alive() is False
    ), "Expected power-down to be removed after falling off-screen."
