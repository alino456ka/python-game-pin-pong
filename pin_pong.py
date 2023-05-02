import pygame as pg
import random as rd
import pygame.freetype

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

def move_player_ai():
    if ball.centerx > WIDTH/2 and ball_x > 0:
        if player_ai.bottom < ball.top:
            player_ai.y += ai_speed
        elif player_ai.top > ball.bottom:
            player_ai.y -= ai_speed

def move_ball(x, y):
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        y = -y
    if ball.colliderect(player) and x < 0:
        pong_sound.play()
        if abs(ball.left - player.right) < 10:
            x = -x
        elif abs(ball.top - player.bottom) < 10 and y < 0:
            y = -y
        elif abs(player.top - ball.bottom) < 10 and y > 0:
            y = - y
    if ball.colliderect(player_ai) and x > 0:
        pong_sound.play()
        if abs(ball.right - player_ai.left) < 10:
            x = -x
        elif abs(ball.top - player_ai.bottom) < 10 and y < 0:
            y = -y
        elif abs(player_ai.top - ball.bottom) < 10 and y > 0:
            y = - y
    now = pg.time.get_ticks()
    if now - time > pause_len and not game_over:
        ball.x += x
        ball.y += y
    return x, y

def respawn_ball(x, y):
    ball.center = WIDTH/2, HEIGHT/2
    x = rd.choice((rd.randint(-max_ball_speed, -min_ball_speed), rd.randint(min_ball_speed, max_ball_speed)))
    y = rd.choice((rd.randint(-max_ball_speed, -min_ball_speed), rd.randint(min_ball_speed, max_ball_speed)))
    return x, y        

def sounds():
    if point_player == finish_point:
        win_sound.play()
    elif point_ai == finish_point:
        lose_sound.play()
    else:
        score_sound.play()

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('ПИНГ ПОНГ')

player = pg.Rect(10, HEIGHT/2, 10, 100)
player_ai = pg.Rect(WIDTH-20, HEIGHT/2, 10, 100)
ball = pg.Rect(WIDTH/2, HEIGHT/2, 20, 20)
font = pygame.freetype.Font(None, 30)
player_speed = 0
ball_x, ball_y = -7, 7
time = 0
pause_len = 1000
ai_speed = 10
max_ball_speed = 15
min_ball_speed = 3
point_player = 0
point_ai = 0
game_over = False
finish_point = 15
menu_text = "Нажмите R, чтобы игра продолжилась."
finish_text = ""
win_sound = pg.mixer.Sound("win.wav")
lose_sound = pg.mixer.Sound("lose.wav")
score_sound = pg.mixer.Sound("score.wav")
pong_sound = pg.mixer.Sound("pong.wav")

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r and game_over:
                game_over = False
                point_ai = 0
                point_player = 0
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
    move_player_ai()
    ball_x, ball_y = move_ball(ball_x, ball_y)
    if ball.right <= 0:
        point_ai += 1
        if point_ai == finish_point:
            game_over = True
            finish_text = "Вы проиграли"
    if ball.left >= WIDTH:
        point_player += 1
        if point_player == finish_point:
            game_over = True
            finish_text = "Вы победили"
    if ball.right <= 0 or ball.left >= WIDTH:
        sounds()
        ball_x, ball_y = respawn_ball(ball_x, ball_y)
        time = pg.time.get_ticks()
    
    screen.fill(WHITE)
    pg.draw.rect(screen, ORANGE, player)
    pg.draw.rect(screen, ORANGE, player_ai)
    pg.draw.ellipse(screen, YELLOW, ball)
    font.render_to(screen, (WIDTH//8, HEIGHT//6), str(point_player))
    font.render_to(screen, (WIDTH - 130, HEIGHT//6), str(point_ai))
    if game_over:
        font.render_to(screen, (WIDTH/3, HEIGHT/3), finish_text)
        font.render_to(screen, (WIDTH/5, HEIGHT - 250), menu_text)

    clock.tick(60)
    pg.display.flip()

