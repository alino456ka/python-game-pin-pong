import pygame as pg
import random as rd

WIDTH = 900
HEIGHT = 600
WHITE = (255, 255, 255)
ORANGE = (200, 132, 25)
YELLOW = (247, 211, 10)

def move_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT

def move_ball(x, y):
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        y = -y
    if ball.colliderect(player) or ball.colliderect(player_ai):
        x = -x
    now = pg.time.get_ticks()
    if now - time > pause_len:
        ball.x += x
        ball.y += y
    return x, y

def respawn_ball(x, y):
    ball.center = WIDTH/2, HEIGHT/2
    x = rd.choice((rd.randint(-15, -3), rd.randint(3, 15)))
    y = rd.choice((rd.randint(-15, -3), rd.randint(3, 15)))
    return x, y

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('ПИНГ ПОНГ')

player = pg.Rect(10, HEIGHT/2, 10, 100)
player_ai = pg.Rect(WIDTH-20, HEIGHT/2, 10, 100)
ball = pg.Rect(WIDTH/2, HEIGHT/2, 20, 20)
player_speed = 0
ball_x, ball_y = -7, 7
time = 0
pause_len = 1000

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player_speed -= 10
            if event.key == pg.K_s:
                player_speed += 10
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                player_speed += 10
            if event.key == pg.K_s:
                player_speed -= 10

    move_player()
    ball_x, ball_y = move_ball(ball_x, ball_y)
    if ball.right <= 0 or ball.left >= WIDTH:
        ball_x, ball_y = respawn_ball(ball_x, ball_y)
        time = pg.time.get_ticks()

    screen.fill(WHITE)
    pg.draw.rect(screen, ORANGE, player)
    pg.draw.rect(screen, ORANGE, player_ai)
    pg.draw.ellipse(screen, YELLOW, ball)
    
    clock.tick(60)
    pg.display.flip()

