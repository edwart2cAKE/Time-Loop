import pygame as pg
from player import player

pg.init()

screen = pg.display.set_mode((1280, 720))

clock = pg.time.Clock()

player1 = player(200, 200, 0, 100)

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

    player1.update(keys_pressed, prev_keys_pressed, dt)

    screen.fill("white")  # Fill the display with a solid color

    # Render the graphics here.
    # ...
    player1.draw(screen)

    pg.display.flip()                 # Refresh on-screen display
    prev_keys_pressed = keys_pressed
    dt = max(clock.tick(60), 1)/1000  # wait until next frame (at 60 FPS)
