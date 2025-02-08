import pygame
from breakout.__main__ import Game, GameState
from breakout.screens import Screens


def test_game_initialization():
    """Test that the game initializes with the correct state and objects."""
    game = Game()
    assert isinstance(game.state, GameState)
    assert len(Screens.START.elements) > 0
    assert len(Screens.END.elements) > 0
    assert game.state.current_screen == Screens.START


def test_setup_screens():
    """Test that setup_screens correctly initializes the start and end screens."""
    game = Game()
    assert len(Screens.START.elements) > 0
    assert len(Screens.END.elements) > 0


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
    assert game.state.paused is True

    # Resume the game
    game.resume_game()
    assert game.state.paused is False


def test_update_game():
    """Ensure update_game() properly updates game state."""
    game = Game()
    game.start_new_game()

    game.state.launched = True
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
    assert game.state.launched is True

    # Simulate SPACE key for pausing the game
    space_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    pygame.event.post(space_event)
    game.handle_events()
    assert game.state.paused is True


def test_powerup_spawn_timing():
    """Test that power-ups spawn at random intervals."""
    game_state = GameState(Screens.GAME)

    # Simulate game state where power-ups can spawn
    game_state.launched = True
    game_state.current_screen = Screens.GAME
    current_time = pygame.time.get_ticks()

    # Force the next power-up spawn time to trigger
    game_state.next_powerup_time = current_time - 1000  # Set to the past
    game_state.update()

    # Verify a power-up was added to the group
    assert (
        len(game_state.powerup_group.sprites()) > 0
    ), "Expected power-up to spawn, but none were added."
