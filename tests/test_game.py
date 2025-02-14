"""
Test Game
=========
Test game/GUI events

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
from breakout.__main__ import Game, GameState
from breakout.screens import ArrowButton, BlinkingMessage, ScreenManager, Screens


def test_game_initialization():
    """Test that the game initializes with the correct state and objects."""
    game = Game()
    assert isinstance(game.state, GameState)
    assert len(Screens.START.elements) > 0
    assert len(Screens.END.elements) > 0
    assert game.state.current_screen == Screens.START


def test_switch_screen():
    """Ensure the game switches screens correctly."""
    game = Game()

    game.switch_screen(Screens.GAME)
    assert game.state.current_screen == Screens.GAME

    game.switch_screen(Screens.END)
    assert game.state.current_screen == Screens.END

    game.switch_screen(Screens.START)
    assert game.state.current_screen == Screens.START


def test_start_new_game():
    """Test starting a new game resets the state."""
    game = Game()

    # Start the game
    game.start_new_game()
    assert game.state.score == 0
    assert game.state.lives == 3
    assert len(game.state.bricks.sprites()) > 0
    assert len(game.state.ball_group.sprites()) == 1
    assert len(game.state.paddle_group.sprites()) == 1


def test_pause_and_resume_game():
    """Test pausing and resuming the game."""
    game = Game()
    game.start_new_game()

    # Pause the game
    game.pause_game()
    assert game.state.paused

    # Resume the game
    game.resume_game()
    assert not game.state.paused


def test_update_game():
    """Ensure update_game() properly updates game state."""
    game = Game()
    game.start_new_game()

    game.state.launch_ball()
    initial_x = game.state.paddle_group.sprites()[0].x_position

    game.update_game()
    assert (
        game.state.paddle_group.sprites()[0].x_position == initial_x
    )  # Ensure paddle does not move unexpectedly


def test_save_score():
    """Ensure scores are saved and sorted correctly."""
    game = Game()
    game.state.score = 500
    game.name_imput.name = "XYZ"

    game.save_score()

    assert (500, "XYZ") in game.scoreboard.top_scores.items()


def test_add_ball():
    """Test adding a new ball to the game."""
    game_state = GameState(Screens.GAME)

    initial_ball_count = len(game_state.ball_group.sprites())
    game_state.add_ball()
    assert len(game_state.ball_group.sprites()) == initial_ball_count + 1


def test_handle_key_events():
    """Test launching ball and pausing game."""
    game = Game()
    game.start_new_game()

    # Simulate UP key for launching the ball
    up_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})
    pygame.event.post(up_event)
    game.handle_events()
    assert game.state.launched

    # Simulate SPACE key for pausing the game
    space_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    pygame.event.post(space_event)
    game.handle_events()
    assert game.state.paused


def test_powerup_spawn_timing():
    """Test that power-ups spawn at random intervals."""
    game_state = GameState(Screens.GAME)

    # Simulate game state where power-ups can spawn
    game_state.launch_ball()
    game_state.time += 2000

    # Force the next power-up spawn time to trigger
    game_state.next_powerup_time = game_state.time - 1000  # Set to the past
    game_state.update()

    # Verify a power-up was added to the group
    assert (
        len(game_state.powerup_group.sprites()) > 0
    ), "Expected power-up to spawn, but none were added."


# Helper Classes for Testing


class DummyElement:
    """A dummy element to test ScreenManager methods."""

    def __init__(self):
        self.draw_called = False
        self.event_handled = False

    def draw(self, surface):
        self.draw_called = True

    def handle_event(self, event):
        self.event_handled = True


def test_screen_manager_draw_with_element():
    """Test that ScreenManager.draw calls the element's draw method."""
    surface = pygame.Surface((screen_size.width, screen_size.height))
    dummy = DummyElement()
    manager = ScreenManager([dummy])
    manager.draw(surface)
    assert dummy.draw_called, "Expected DummyElement.draw() to be called"


def test_arrow_button_click():
    """Ensure an ArrowButton registers a press and then resets after release."""
    ab = ArrowButton("left")
    # Build a fake mouse down event at the arrow's location.
    event_down = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"pos": ab.rect.center, "button": 1}
    )
    ab.handle_event(event_down)
    # The button should now be marked as pressed.
    assert ab.pressed, "ArrowButton should be pressed after mouse button down."

    # Release the mouse button
    event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": ab.rect.center})
    ab.handle_event(event_up)
    # The arrow button should no longer be pressed.
    assert not ab.pressed, "ArrowButton should not be pressed after mouse button up."


def test_launch_message_blink_toggle():
    """Check that LaunchMessage toggles its visibility after the blink interval."""
    surface = pygame.Surface((screen_size.width, screen_size.height))
    lm = BlinkingMessage(
        "Test Launch",
        pos=(screen_size.width // 2, screen_size.height // 2),
        blink_interval=1,
    )
    lm.last_toggle = pygame.time.get_ticks() - 2
    original_visibility = lm.visible
    # Call draw; this should toggle the message's visibility.
    lm.draw(surface)
    # Verify that the visibility has changed.
    assert (
        lm.visible != original_visibility
    ), "LaunchMessage did not toggle its visibility as expected."
