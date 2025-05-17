import pygame as pg
from platform_1 import *
from player import player

pg.init()

screen = pg.display.set_mode((1280, 720))

clock = pg.time.Clock()
player1 = player(100, 200, 0, 100)
player1.set_hitbox(25, 0, 50, 200)

platform1 = Platform(1000, 250, 220, 120)
platform2 = SlowPlatform(700, 250, 220, 120)
platform3 = FastPlatform(400, 250, 220, 120)

dt = 1/60

prev_keys_pressed = pg.key.get_pressed()

while True:
    # Process player inputs.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    # Do logical updates here.
    # ...
    keys_pressed = pg.key.get_pressed()

    player1.update(keys_pressed, prev_keys_pressed, dt,
                   platformlists=[platform1, platform2, platform3])

    screen.fill("white")  # Fill the display with a solid color

    # Render the graphics here.
    # ...
    player1.draw(screen)
    platform1.draw(screen)
    platform2.draw(screen)
    platform3.draw(screen)

    pg.display.flip()                 # Refresh on-screen display
    prev_keys_pressed = keys_pressed
    dt = max(clock.tick(60), 1)/1000  # wait until next frame (at 60 FPS)
