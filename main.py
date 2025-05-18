import pygame as pg
from platform_1 import *
from player import player
from npc import NPC

pg.init()

screen = pg.display.set_mode((1280, 720))

clock = pg.time.Clock()
player1 = player(100, 200, 0, 100)
player1.set_hitbox(25, 0, 50, 200)

platform1 = Platform(1000, 250, 220, 120)
platform2 = SlowPlatform(700, 250, 220, 120)
platform3 = FastPlatform(400, 250, 220, 120)
platform4 = IcePlatform(100, 250, 220, 120)

king = NPC(1000, 500, 100, 200, "images/michael jordan.png")
king.set_text("Heeheeheehaw, nothing interesting\nhappens if you slide on a wall and let go")

dt = 1 / 60

scroll = [-500, 0]

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

    player1.update(
        keys_pressed,
        prev_keys_pressed,
        dt,
        platformlists=[platform1, platform2, platform3, platform4],
    )

    # set scroll to tween to player's position
    scroll[0] += (player1.x - screen.get_width() / 2 - scroll[0]) * (5 * dt)
    scroll[1] = player1.y // screen.get_height() * screen.get_height()
    #print(player1.height // screen.get_height(), player1.height)
    #print(scroll)

    screen.fill("white")  # Fill the display with a solid color

    # Render the graphics here.
    # ...
    # scrolled graphics
    platform1.draw(screen, scroll)
    platform2.draw(screen, scroll)
    platform3.draw(screen, scroll)
    platform4.draw(screen, scroll)

    king.draw(screen,player1, scroll)
    player1.draw(screen, scroll)

    # unscrolled graphics
    player1.draw_health(screen)

    pg.display.flip()  # Refresh on-screen display
    prev_keys_pressed = keys_pressed
    dt = max(clock.tick(60), 1) / 1000  # wait until next frame (at 60 FPS)
