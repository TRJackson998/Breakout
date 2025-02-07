"""Test ball object and its movements/actions."""

from pygame import Color, sprite
from breakout.ball import Ball
from breakout.paddle import Paddle
from breakout.bricks import Brick
from breakout import screen_size


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


def test_ball_paddle_collision():
    """Test ball bounces correctly when hitting the paddle."""
    paddle = Paddle()
    ball = Ball()
    ball.rect.midbottom = paddle.rect.midtop  # Place ball just above the paddle
    ball.speed_y = 2.5
    ball.handle_paddle_collision(paddle)
    assert ball.speed_y > 0


def test_ball_brick_collision():
    """Test ball interaction with bricks."""
    brick_group = sprite.Group()
    # Stage a red brick at specified location
    brick = Brick(brick_group, color=Color("red"), x_position=100, y_position=100)
    ball = Ball()

    # Position the ball to collide with the brick
    ball.rect.topleft = (100, 100)  # Align ball with the brick
    points = ball.handle_brick_collisions(brick_group)

    assert points == 3, f"Expected 3 points, got {points}"  # Red brick gives 3 points
    assert (
        len(brick_group) == 0
    ), f"Expected brick to be removed, but {len(brick_group)} bricks remain"
