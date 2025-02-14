"""
Test Ball and Paddle
====================
Test ball object and its movements/actions.
Test paddle object and its interactions with the screen and ball.

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

from pygame import Color, sprite

from breakout import screen_size
from breakout.__main__ import GameState
from breakout.ball import Ball
from breakout.bricks import Brick
from breakout.paddle import Paddle


def test_ball_initialization():
    """Test ball initializes with correct attributes."""
    ball = Ball()
    assert ball.x_position == 250
    assert ball.y_position == 380
    assert ball.speed_x in [-2.5, 2.5]
    assert ball.speed_y == -2.5
    assert ball.color == Color("white")


def test_ball_wall_collision():
    """Test ball bounces off of the walls correctly."""
    ball = Ball()

    # Simulate hitting the left wall
    ball.x_position = 0  # Place ball at the left wall
    ball.speed_x = -2.5  # Ball moving left
    ball.handle_wall_collisions()
    assert (
        ball.speed_x > 0
    ), f"Expected ball to bounce right, but we got speed_x={ball.speed_x}"

    # Simulate hitting the right wall
    ball.x_position = (
        screen_size.width - ball.rect.width
    )  # Place ball at the right wall
    ball.speed_x = 2.5  # Ball moving right
    ball.handle_wall_collisions()
    assert (
        ball.speed_x < 0
    ), f"Expected ball to bounce left, but we got speed_x={ball.speed_x}"


def test_ball_ceiling_collision():
    """Test ball bounces off the ceiling correctly."""
    ball = Ball()

    # Simulate hitting the ceiling
    ball.y_position = 0  # Place ball at the ceiling
    ball.speed_y = -2.5  # Ball moving upward
    ball.handle_wall_collisions()

    assert (
        ball.speed_y > 0
    ), f"Expected ball to bounce downward, but got speed_y={ball.speed_y}"


def test_ball_paddle_collision():
    """Test ball bounces correctly when hitting the paddle."""
    paddle = Paddle()
    ball = Ball()

    # Don't collide with paddle
    ball.speed_y = -2.5  # traveling up
    assert ball.can_collide_with_paddle
    ball.handle_paddle_collision(paddle)
    assert ball.can_collide_with_paddle

    # Collide with paddle
    ball.rect.center = paddle.rect.center  # Place ball on the paddle
    ball.speed_y = 2.5  # traveling down
    ball.handle_paddle_collision(paddle)
    assert (
        ball.speed_y < 0
    ), f"Expected ball to bounce upward, but got speed_y={ball.speed_y}"
    assert not ball.can_collide_with_paddle


def test_ball_brick_collision():
    """Test ball interaction with bricks."""
    brick_group = sprite.Group()
    # Stage a red brick at specified location
    brick1 = Brick(brick_group, color=Color("red"), x_position=100, y_position=100)
    brick2 = Brick(brick_group, color=Color("yellow"), x_position=50, y_position=50)
    ball = Ball()

    # Position the ball to collide with the red brick w/horizontal overlap
    ball.rect.bottom = 105
    ball.rect.right = 101
    points = ball.handle_brick_collisions(brick_group)
    assert points == 3, f"Expected 3 points, got {points}"  # Red brick gives 3 points

    # Position the ball to collide with the yellow brick w/vertical overlap
    ball.rect.bottom = 51
    ball.rect.right = 55
    points = ball.handle_brick_collisions(brick_group)
    assert (
        points == 2
    ), f"Expected 2 points, got {points}"  # Yellow brick gives 2 points

    assert (
        len(brick_group) == 0
    ), f"Expected brick to be removed, but {len(brick_group)} bricks remain"


def test_ball_life_lost():
    """Test that the player loses a life when the ball falls below the screen."""
    state = GameState()
    ball = state.ball

    assert state.lives == 3, f"Expected initial lives to be 3, but got {state.lives}"

    # Simulate ball falling below the screen (Lose 1 life)
    ball.y_position = screen_size.height + 10
    state = ball.move(state)
    assert state.lives == 2, f"Expected lives to decrease to 2, but got {state.lives}"

    # Simulate another life lost
    ball.y_position = screen_size.height + 10
    state = ball.move(state)
    assert state.lives == 1, f"Expected lives to decrease to 1, but got {state.lives}"

    # Lose final life
    ball.y_position = screen_size.height + 10
    state = ball.move(state)

    assert state.lives == 0, f"Expected lives to be 0, but got {state.lives}"
    assert state.game_is_over, "Expected game_is_over to be True when lives reach 0"


def test_paddle_initialization():
    """Verify that a Paddle is initialized with the correct default settings."""
    paddle = Paddle()
    # Check that the paddle's starting position is recorded correctly.
    assert paddle.x_position == Paddle.initial_x
    assert paddle.y_position == Paddle.initial_y
    assert paddle.rect.topleft == (paddle.x_position, paddle.y_position)
    assert paddle.image.get_size() == (Paddle.width, Paddle.height)  # verify dimensions
    pixel_color = paddle.image.get_at((0, 0))  # check that it is the correct color.
    assert pixel_color == paddle.color


def test_paddle_reset_position():
    """Test that reset_position returns the paddle to its original location."""
    paddle = Paddle()
    # Move the paddle to a new position.
    paddle.move_left()
    # Reset the paddle's position.
    paddle.reset_position()
    # Confirm that the position and the rect's position are reset.
    assert paddle.x_position == Paddle.initial_x
    assert paddle.y_position == Paddle.initial_y
    assert paddle.rect.topleft[0] == Paddle.initial_x, f"{paddle.rect.topleft}"
    assert paddle.rect.topleft[1] == Paddle.initial_y


def test_paddle_move_left_normal():
    """Test that move_left decreases the paddle's x_position by its speed."""
    paddle = Paddle(x_position=200, speed=10)
    original_x = paddle.x_position
    paddle.move_left()
    expected_x = original_x - 10
    if expected_x < 0:
        expected_x = 0
    assert paddle.x_position == expected_x
    assert paddle.rect.x == expected_x


def test_paddle_move_left_boundary():
    """Ensure that move_left does not move the paddle beyond the left screen edge."""
    paddle = Paddle(x_position=5, speed=10)
    paddle.move_left()
    # The paddle should not move left past 0.
    assert paddle.x_position == 0
    assert paddle.rect.x == 0


def test_paddle_move_right_normal():
    """Test that move_right increases the paddle's x_position by its speed."""
    paddle = Paddle(x_position=100, speed=10)
    original_x = paddle.x_position
    paddle.move_right()
    expected_x = original_x + 10
    # Ensure the new position does not exceed the right boundary.
    max_x = screen_size.width - paddle.rect.width
    if expected_x > max_x:
        expected_x = max_x
    assert paddle.x_position == expected_x
    assert paddle.rect.x == expected_x


def test_paddle_move_right_boundary():
    """Ensure that move_right does not move the paddle beyond the right screen edge."""
    # Start with an x_position near the right boundary.
    paddle = Paddle(x_position=screen_size.width - 5, speed=10)
    paddle.move_right()
    # The paddle should not exceed the maximum allowed x position.
    max_x = screen_size.width - paddle.rect.width
    assert paddle.x_position == max_x
    assert paddle.rect.x == max_x
