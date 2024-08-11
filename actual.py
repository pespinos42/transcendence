import pygame
import sys
import time
from random import *

#Funcion para prever la coordenada y del impacto de la bola
def next_impact_y(x, y, ball_size, ball_speed_y, height, paddle_width, margin):

    result = -1
    x = x - (ball_size // 2) - paddle_width - margin

    print("---ESTADO ACTUAL---")
    print(f"x = {x} y = {y}")

    while x >= height:
        x = x - height
        y = height - y
        ball_speed_y = -ball_speed_y
        print("---ESTADO ACTUAL 2---")
        print(f"x = {x} y = {y}")

    if ball_speed_y < 0:
        if (y - ball_size // 2) < x:
            print("")
            result = x - (y - ball_size // 2)
        elif (y - ball_size // 2) >= x:
            result = (y - ball_size // 2) - x
    elif ball_speed_y > 0:
        if (height - (y + ball_size // 2)) < x:
            result = height - (x - (y + ball_size // 2))
        elif (height - (y + ball_size // 2)) >= x:
            result = height - ((y + ball_size // 2) - x)
    
    return result


#Inicializamos Pygame
pygame.init()

#Configuramos la pantalla
width = 800
height = 800
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pong')

#Definimos los código RGB de los colores que vamos a usar
white = (255, 255, 255)
black = (0, 0, 0)

#Configuramos las características de las paletas
paddle_width = 10
paddle_height = 100
paddle_speed = 5

#Configuramos la posición inicial de la paleta del jugador 1
'''
Los parámetros de Rect son:
1- Coordenada x de la esquina superior izquierda del rectángulo
2- Coordenada y de la esquina superior izquierda del rectángulo
3- Ancho del rectángulo
4- Alto del rectángulo
'''
margin_x = 50
paddle1 = pygame.Rect(margin_x, (height - paddle_height) // 2, paddle_width, paddle_height)

#Configuramos la posición inicial de la paleta del jugador 2
paddle2 = pygame.Rect(width - paddle_width - margin_x, (height - paddle_height) // 2, paddle_width, paddle_height)

#Configuramos la pelota
ball_size = 20
ball_speed_x = -3.5
ball_speed_y = 3.5
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)

#Establecemos los diferentes niveles de dificultad del juego
difficulties = {
    1 : 4, #2
    2 : 4, #3
    3 : 4, #3.5
    4 : 4
}

#Ponemos el grado de dificultad de forma aleatoria
#este grado de dificultad se vuelve a asignar cada vez que la pelota sale
difficulty = randint(1, 4)

#Establecemos la velocidad de la paleta del jugador 1 (AI) basado en la dificultad elegida
ai_speed = difficulties.get(difficulty, 4)

#Inicializamos la futura posición de la pelota para AI
next_y = 0
ball_center_x, ball_center_y = ball.center
next_y = next_impact_y(ball_center_x, ball_center_y, ball_size, ball_speed_y, height, paddle_width, margin_x)
last_update_time = time.time()
print(f"SIGUIENTE PUNTO DE IMPACTO -> (60, {next_y})")


#Bucle principal del juego

#creamos un reloj para controlar el número de fps más adelante
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Movimiento de las paletas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle2.top > 0:
        #move_ip(desplazamiento_x, desplazamiento_y)
        paddle2.move_ip(0, -paddle_speed)
    if keys[pygame.K_DOWN] and paddle2.bottom < height:
        paddle2.move_ip(0, paddle_speed)
    
    #Movimiento automático de la pala de jugador 1 (AI)
    current_time = time.time()
    if current_time - last_update_time >= 1:
        last_update_time = current_time
        ball_center_x, ball_center_y = ball.center
        next_y = next_impact_y(ball_center_x, ball_center_y, ball_size, ball_speed_y, height, paddle_width, margin_x)
        print(f"SIGUIENTE PUNTO DE IMPACTO -> (60, {next_y})")

    if paddle1.centery < ball.centery and paddle1.bottom < height:
        paddle1.move_ip(0, ai_speed)
    if paddle1.centery > ball.centery and paddle1.top > 0:
        paddle1.move_ip(0, -ai_speed)    

    #Movimiento de la pelota
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #Control de las colisiones superiores e inferiores
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y = -ball_speed_y
    
    #Control de la colisión con las paletas
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x = -ball_speed_x
        if ball.colliderect(paddle1):
            print(f"PUNTO DE COLISION -> {ball.x}, {ball.y}")

    #Reinicio de la pelota
    if ball.left <= 0 or ball.right >= width:
        ball.center = (width // 2, height // 2)
        ball_speed_x = -ball_speed_x
        difficulty = randint(1, 3)
        ai_speed = difficulties.get(difficulty, 5)
    
    #Imprimimos todo en pantalla
    screen.fill(black)
    pygame.draw.rect(screen, white, paddle1)
    pygame.draw.rect(screen, white, paddle2)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (width // 2, 0), (width // 2, height))

    pygame.display.flip()
    clock.tick(60)
