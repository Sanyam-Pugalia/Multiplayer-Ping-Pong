#

import pygame
import random
import multiprocessing
import threading
import time

# Initialize Pygame
pygame.init()

# Constant
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 70
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Define a USEREVENT
countdown_event = pygame.USEREVENT + 1


game_started=False
countdown =4

# Countdown timer
def countdown_thread():
    global countdown, game_started
    while countdown > 0:
        countdown -= 1
        time.sleep(1)
    game_started = True

# Start the countdown thread
countdown_thread = threading.Thread(target=countdown_thread)
countdown_thread.start()



# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Paddles
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [random.choice((BALL_SPEED_X, -BALL_SPEED_X)), random.choice((BALL_SPEED_Y, -BALL_SPEED_Y))]

clock = pygame.time.Clock()

# Score
left_score = 0
right_score = 0

font = pygame.font.Font(None, 36)

# Winner message
winner_font = pygame.font.Font(None, 72)

# Game state
game_paused = False

# Main game loop
running = True
while running:
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == countdown_event:
            if countdown > 0:
                countdown -= 1
            else:
                # Stop the countdown timer
                pygame.time.set_timer(countdown_event, 0)
                game_started = True

    keys = pygame.key.get_pressed()

    # Display countdown
    if countdown > 0:
        countdown_text = font.render(str(countdown), True, WHITE)
        center_x = WIDTH // 2 - countdown_text.get_width() // 2
        win.blit(countdown_text, (center_x, 0)) # Draw at the top center of the screen
    else:
        # Stop countdown timer
              pygame.time.set_timer(countdown_event, 0)
              game_started = True

    # Handle game pause
    if not game_paused and game_started:
        # Left paddle movement
        if keys[pygame.K_w] and left_paddle.y > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.y < HEIGHT - PADDLE_HEIGHT:
            left_paddle.y += PADDLE_SPEED

        # Right paddle movement (for the second player in a multiplayer scenario)
        if keys[pygame.K_UP] and right_paddle.y > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.y < HEIGHT - PADDLE_HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Ball movement
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed[0] = -ball_speed[0]

         # Ball collision with walls
        
        if ball.top <= 0 or ball.bottom >= HEIGHT:
           ball_speed[1] = -ball_speed[1]
        if ball.left <= 0:
           # Right player scores a point
           right_score += 1
           if right_score >= 3:
               winner = "Right Player"
               game_paused = True
           else:
               ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
               ball_speed = [random.choice((BALL_SPEED_X, -BALL_SPEED_X)), random.choice((BALL_SPEED_Y, -BALL_SPEED_Y))]
               # Reset paddles to the center of the screen
               left_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
               right_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
               
        elif ball.right >= WIDTH:
           # Left player scores a point
           left_score += 1
           if left_score >= 3:
               winner = "Left Player"
               game_paused = True
           else:
               ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
               ball_speed = [random.choice((BALL_SPEED_X, -BALL_SPEED_X)), random.choice((BALL_SPEED_Y, -BALL_SPEED_Y))]
               # Reset paddles to the center of the screen
               left_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
               right_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
               

    

    # Draw paddles and ball
    pygame.draw.rect(win, WHITE, left_paddle)
    pygame.draw.rect(win, WHITE, right_paddle)
    pygame.draw.ellipse(win, WHITE, ball)

    # Display the score
    left_score_text = font.render(f"Left Player: {left_score}", True, WHITE)
    right_score_text = font.render(f"Right Player: {right_score}", True, WHITE)
    win.blit(left_score_text, (50, 50))
    win.blit(right_score_text, (WIDTH - 220, 50))

    # Display winner when the game sis paused
    if game_paused and winner:
        winner_text = winner_font.render(f"{winner} wins!", True, WHITE)
        win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))

        # Restart the game when 'SPACE' is pressed
        if keys[pygame.K_SPACE]:
            left_score = 0
            right_score = 0
            game_paused = False
            winner = None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()