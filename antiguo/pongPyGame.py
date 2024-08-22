import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pong')

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Configuración de las paletas
paddle_width, paddle_height = 10, 100
paddle_speed = 5

# Paleta del jugador 1
paddle1 = pygame.Rect(50, (height - paddle_height) // 2, paddle_width, paddle_height)

# Paleta del jugador 2
paddle2 = pygame.Rect(width - 50 - paddle_width, (height - paddle_height) // 2, paddle_width, paddle_height)

# Configuración de la pelota
ball_size = 20
ball_speed_x, ball_speed_y = 4, 4
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)

# Bucle principal del juego
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Movimiento de las paletas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.move_ip(0, -paddle_speed)
    if keys[pygame.K_s] and paddle1.bottom < height:
        paddle1.move_ip(0, paddle_speed)
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.move_ip(0, -paddle_speed)
    if keys[pygame.K_DOWN] and paddle2.bottom < height:
        paddle2.move_ip(0, paddle_speed)
    
    # Movimiento de la pelota
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Colisión con la parte superior e inferior de la pantalla
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y = -ball_speed_y

    # Colisión con las paletas
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x = -ball_speed_x

    # Puntuación y reinicio de la pelota
    if ball.left <= 0 or ball.right >= width:
        ball.center = (width // 2, height // 2)
        ball_speed_x = -ball_speed_x

    # Dibujar todo en la pantalla
    screen.fill(black)
    pygame.draw.rect(screen, white, paddle1)
    pygame.draw.rect(screen, white, paddle2)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (width // 2, 0), (width // 2, height))

    pygame.display.flip()
    clock.tick(60)
