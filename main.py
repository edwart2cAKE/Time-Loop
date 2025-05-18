from scene import *

pg.init()

screen = pg.display.set_mode((1280, 720))

clock = pg.time.Clock()

dt = 1 / 60

gameplay = MainScene(screen, lambda scene: None)

game_over_scene = TryAgainScene(screen, lambda scene: None)

won_scene = GameWonScene(screen, lambda scene: None)

time_passed = 0
game_state = 0  # 0: playing, 1: game over, 2: game won

while True:
    # Process system inputs.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

    # Do logical updates here.
    # ...

    # Update the scene here
    if game_state == 0:
        gameplay.update(dt)
        if gameplay.touching_time_machine():
            game_state = 2
            time_passed = 0
    elif game_state == 1:
        game_over_scene.update()
        if game_over_scene.if_clicked():
            gameplay = MainScene(screen, lambda scene: None)
            game_over = False
            time_passed = 0
    elif game_state == 2:
        won_scene.update()


    screen.fill("white")  # Fill the display with a solid color

    # Render the graphics here.
    # ...
    if game_state == 0:
        gameplay.draw()
    elif game_state == 1:
        game_over_scene.draw()
    elif game_state == 2:
        won_scene.draw()

    pg.display.flip()  # Refresh on-screen display
    # prev_keys_pressed = keys_pressed
    dt = max(clock.tick_busy_loop(60), 1) / 1000  # wait until next frame (at 60 FPS)
    time_passed += dt
    if time_passed > 45:
        game_over = True
    
