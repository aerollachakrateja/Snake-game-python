import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

def main_menu():
    while True:
        WINDOW.fill(BLACK)
        title_font = pygame.font.SysFont("Arial", 60)
        option_font = pygame.font.SysFont("Arial", 30)
        title = title_font.render("PONG", True, WHITE)
        option1 = option_font.render("1. Single player (vs AI)", True, WHITE)
        option2 = option_font.render("2. Multiplayer", True, WHITE)
        option3 = option_font.render("Q. Quit", True, WHITE)

        WINDOW.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        WINDOW.blit(option1, (WIDTH // 2 - option1.get_width() // 2, HEIGHT // 2 - 40))
        WINDOW.blit(option2, (WIDTH // 2 - option2.get_width() // 2, HEIGHT // 2))
        WINDOW.blit(option3, (WIDTH // 2 - option3.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main("single")
                elif event.key == pygame.K_2:
                    main("multi")
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_over(winner):
    while True:
        WINDOW.fill(BLACK)
        font_large = pygame.font.SysFont("Arial", 50)
        font_small = pygame.font.SysFont("Arial", 30)

        game_over_text = font_large.render(f"{winner} - Game Over!", True, WHITE)
        replay_text = font_small.render("Press R to Replay or Q to Quit", True, WHITE)
        WINDOW.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
        WINDOW.blit(replay_text, (WIDTH//2 - replay_text.get_width()//2, HEIGHT//2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def reset_ball(ball, width, height, ball_vel_x):
    ball.center = (width // 2, height // 2)
    return -ball_vel_x

def check_score(ball, width, height, player1_score, player2_score, ball_vel_x):
    if ball.left <= 0:
        player2_score += 1
        ball_vel_x = reset_ball(ball, width, height, ball_vel_x)
    elif ball.right >= width:
        player1_score += 1
        ball_vel_x = reset_ball(ball, width, height, ball_vel_x)
    return player1_score, player2_score, ball_vel_x

def check_collision(ball, left_paddle, right_paddle, ball_vel_x, ball_vel_y):
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel_y *= -1
    # Left paddle
    if ball.colliderect(left_paddle) or left_paddle.collidepoint(ball.left, ball.centery):
        if ball_vel_x < 0:
            ball_vel_x *= -1
    # Right paddle
    if ball.colliderect(right_paddle) or right_paddle.collidepoint(ball.right, ball.centery):
        if ball_vel_x > 0:
            ball_vel_x *= -1
    return ball_vel_x, ball_vel_y

def main(mode):
    player1_score = 0
    player2_score = 0
    paddle_w, paddle_h = 15, 100
    ball_size = 20

    left_paddle = pygame.Rect(50, HEIGHT//2 - paddle_h//2, paddle_w, paddle_h)
    right_paddle = pygame.Rect(WIDTH - 50 - paddle_w, HEIGHT//2 - paddle_h//2, paddle_w, paddle_h)
    ball = pygame.Rect(WIDTH//2 - ball_size//2, HEIGHT//2 - ball_size//2, ball_size, ball_size)

    ball_vel_x = 5
    ball_vel_y = 5
    paddle_speed = 7

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        # Player 1
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed
        # Player 2 or AI
        if mode == "multi":
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed
        else:
            if right_paddle.centery < ball.centery and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed
            if right_paddle.centery > ball.centery and right_paddle.top > 0:
                right_paddle.y -= paddle_speed

        ball.x += ball_vel_x
        ball.y += ball_vel_y

        # Use helper functions
        ball_vel_x, ball_vel_y = check_collision(ball, left_paddle, right_paddle, ball_vel_x, ball_vel_y)
        player1_score, player2_score, ball_vel_x = check_score(ball, WIDTH, HEIGHT, player1_score, player2_score, ball_vel_x)

        if player1_score == 10:
            game_over("Player 1 wins")
        elif player2_score == 10:
            game_over("Player 2 wins" if mode=="multi" else "AI wins!")

        WINDOW.fill(BLACK)
        pygame.draw.rect(WINDOW, WHITE, left_paddle)
        pygame.draw.rect(WINDOW, WHITE, right_paddle)
        pygame.draw.ellipse(WINDOW, WHITE, ball)

        score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
        WINDOW.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
