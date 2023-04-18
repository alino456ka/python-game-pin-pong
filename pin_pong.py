import pygame as pg

WIDTH = 900
HEIGHT = 600
WHITE = (255, 255, 255)

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('ПИНГ ПОНГ')

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screen.fill(WHITE)
    
    clock.tick(60)
    pg.display.flip()
