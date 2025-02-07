"""Test ball object and its movements/actions."""

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
    ball.handle_wall_collisions(screen_size)
    assert (
        ball.speed_x > 0
    ), f"Expected ball to bounce right, but we got speed_x={ball.speed_x}"

    # Simulate hitting the right wall
    ball.x_position = (
        screen_size.width - ball.rect.width
    )  # Place ball at the right wall
    ball.speed_x = 2.5  # Ball moving right
    ball.handle_wall_collisions(screen_size)
    assert (
        ball.speed_x < 0
    ), f"Expected ball to bounce left, but we got speed_x={ball.speed_x}"


def test_ball_ceiling_collision():
    """Test ball bounces off the ceiling correctly."""
    ball = Ball()

    # Simulate hitting the ceiling
    ball.y_position = 0  # Place ball at the ceiling
    ball.speed_y = -2.5  # Ball moving upward
    ball.handle_wall_collisions(screen_size)

    assert (
        ball.speed_y > 0
    ), f"Expected ball to bounce downward, but got speed_y={ball.speed_y}"


def test_ball_paddle_collision():
    """Test ball bounces correctly when hitting the paddle."""
    paddle = Paddle()
    ball = Ball()

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
    brick = Brick(brick_group, color=Color("red"), x_position=100, y_position=100)
    ball = Ball()

    # Position the ball to collide with the red brick w/horizontal overlap
    ball.rect.bottom = 105
    ball.rect.right = 101
    points = ball.handle_brick_collisions(brick_group)

    assert points == 3, f"Expected 3 points, got {points}"  # Red brick gives 3 points
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
    state = ball.move(screen_size, state)
    assert state.lives == 2, f"Expected lives to decrease to 2, but got {state.lives}"

    # Simulate another life lost
    ball.y_position = screen_size.height + 10
    state = ball.move(screen_size, state)
    assert state.lives == 1, f"Expected lives to decrease to 1, but got {state.lives}"

    # Lose final life
    ball.y_position = screen_size.height + 10
    state = ball.move(screen_size, state)

    assert state.lives == 0, f"Expected lives to be 0, but got {state.lives}"
    assert state.game_over is True, "Expected game_over to be True when lives reach 0"
