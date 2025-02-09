"""Test file for powerup actions"""

from unittest.mock import Mock
import pygame
from breakout.__main__ import GameState
from breakout.powerups import PowerUp, PowerupConfig
from breakout import screen_size
from breakout.paddle import Paddle
from breakout.screens import Screens


def test_powerup_initialization():
    """Test power-up initializes with correct attributes."""
    powerup = PowerUp(power=lambda: None, shape="rectangle")  # Test rectangle power-up

    assert powerup.x_position >= PowerupConfig.size * 5
    assert powerup.x_position <= screen_size.width - PowerupConfig.size * 5
    assert powerup.y_position == 15  # Power-up starts near the top
    assert powerup.speed_y == PowerupConfig.default_speed
    assert powerup.can_collide_with_paddle is True
    assert powerup.shape == "rectangle"  # Ensures rectangle initialization
    assert isinstance(powerup.color, int)


def test_powerup_movement():
    """Test power-up moves downward."""
    powerup = PowerUp(power=lambda: None)
    initial_y = powerup.y_position
    powerup.update_position()

    assert (
        powerup.y_position > initial_y
    ), f"Expected power-up to move down, but got {powerup.y_position}"


def test_powerup_paddle_collision():
    """Test power-up is collected when hitting the paddle."""
    mock_power_effect = Mock()
    paddle = Paddle()
    powerup = PowerUp(power=mock_power_effect)

    powerup.rect.bottom = paddle.rect.top + 1  # Ensure overlap with the paddle
    powerup.rect.centerx = paddle.rect.centerx
    powerup.speed_y = 2.5
    powerup.can_collide_with_paddle = True  # Allow collision

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
    powerup.y_position = screen_size.height + 10
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

    assert (
        text_rect.center == powerup.rect.center
    ), f"Expected text surface center {text_rect.center} to match power-up center {powerup.rect.center}."
