import pygame
import project

def test_reset_ball():
    ball = pygame.Rect(100, 100, 20, 20)
    vel_x = 5
    new_vel_x = project.reset_ball(ball, 800, 600, vel_x)
    assert ball.center == (400, 300)
    assert new_vel_x == -5

def test_check_score_player2():
    ball = pygame.Rect(-10, 200, 20, 20)  # Ball went off left
    p1, p2, vel_x = project.check_score(ball, 800, 600, 0, 0, 5)
    assert p2 == 1
    assert p1 == 0
    assert ball.center == (400, 300)

def test_check_score_player1():
    ball = pygame.Rect(810, 200, 20, 20)  # Ball went off right
    p1, p2, vel_x = project.check_score(ball, 800, 600, 0, 0, 5)
    assert p1 == 1
    assert p2 == 0
    assert ball.center == (400, 300)

def test_check_collision_wall():
    ball = pygame.Rect(300, 0, 20, 20)  # At top
    left_paddle = pygame.Rect(50, 250, 15, 100)
    right_paddle = pygame.Rect(735, 250, 15, 100)
    new_vx, new_vy = project.check_collision(ball, left_paddle, right_paddle, 5, -5)
    assert new_vy == 5  # bounced off wall

def test_check_collision_paddle():
    ball = pygame.Rect(65, 300, 20, 20)  # Touching left paddle
    left_paddle = pygame.Rect(50, 250, 15, 100)
    right_paddle = pygame.Rect(735, 250, 15, 100)
    new_vx, new_vy = project.check_collision(ball, left_paddle, right_paddle, -5, 0)
    assert new_vx == -5  # bounced off paddle