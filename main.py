from scene import *

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
king.set_text(
    "Heeheeheehaw, nothing interesting\nhappens if you slide on a wall and let go")

dt = 1 / 60

scroll = [-500.0, 0, 0]

prev_keys_pressed = pg.key.get_pressed()

gameplay = MainScene(screen, lambda scene: None)

while True:
    # Process system inputs.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    # Do logical updates here.
    # ...

    # Update the scene here
    gameplay.update(dt)


    screen.fill("white")  # Fill the display with a solid color

    # Render the graphics here.
    # ...
    gameplay.draw()

    pg.display.flip()  # Refresh on-screen display
    # prev_keys_pressed = keys_pressed
    dt = max(clock.tick(60), 1) / 1000  # wait until next frame (at 60 FPS)
