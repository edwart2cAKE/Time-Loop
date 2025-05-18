import pygame as pg
from platform_1 import *
from player import player
from npc import NPC


class Scene:
    def __init__(self, screen: pg.surface.Surface, init_callback):
        self.screen = screen
        init_callback(self)

    def update(self):
        # Update the scene here
        pass

    def draw(self):
        # Draw the scene here
        pass


class MainScene(Scene):
    def __init__(self, screen: pg.surface.Surface, init_callback):
        super().__init__(screen, init_callback)
        self.player = player(100, 200, 0, 300)
        self.player.set_hitbox(25, 0, 50, 200)

        # world building
        self.platforms = [
            Platform(-100, 510, 370, 30),   # Floor at start
            Platform(-100, 210, 30, 300),   # Left wall at start
            IcePlatform(-100, 210, 370, 30),  # Ceiling at start (icy)

            # to the bald guy
            Platform(440, 410, 300, 30),
            Platform(970, 610, 300, 30),
            IcePlatform(1540, 910, 600, 30),

            # platforms to the end
            IcePlatform(1070, 200, 300, 30),
            FastPlatform(1740, 100, 200, 30),
            IcePlatform(2040, 200, 200, 30),
            FastPlatform(2540, 100, 200, 30),
            IcePlatform(2940, 400, 200, 30),
            FastPlatform(3340, 200, 200, 30),

            # ladder platforms
            Platform(1740, -310, 300, 30),
            Platform(1740, -1610, 30, 1000),
            Platform(2340, -1610, 30, 1000),

            # ladder rungs
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 1
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 2
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 3
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 4
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 5
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 6
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 7
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 8
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 9
            SlowPlatform(1740, -1610, 30, 100),  # Ladder 10
        ]

        # New: platforms2 from the level image, scaled to the player (player is 100w x 200h)
        self.platforms2 = [
            # Starting box platforms
            Platform(-100, 510, 300, 30),   # Floor at start
            Platform(-100, 150, 30, 360),   # Left wall at start
            IcePlatform(-100, 150, 300, 30),  # Ceiling at start (icy)

            # First jump platforms
            Platform(200, 400, 300, 30),    # First small platform
            Platform(600, 300, 300, 30),    # Second small platform

            # Cyan (fast) platforms
            FastPlatform(1000, 250, 300, 30),
            FastPlatform(1400, 250, 300, 30),
            FastPlatform(1800, 250, 300, 30),

            # Middle platforms
            Platform(1200, 150, 300, 30),   # Center left
            Platform(1600, 150, 300, 30),   # Center
            Platform(2000, 150, 300, 30),   # Center right

            # Ice (blue) platforms
            IcePlatform(1400, 50, 300, 30),
            IcePlatform(1800, 50, 300, 30),

            # Ladder platforms (orange, vertical stack)
            SlowPlatform(2200, 100, 30, 100),  # Ladder 1
            SlowPlatform(2200, 200, 30, 100),  # Ladder 2
            SlowPlatform(2200, 300, 30, 100),  # Ladder 3
            SlowPlatform(2200, 400, 30, 100),  # Ladder 4
            SlowPlatform(2200, 500, 30, 100),  # Ladder 5

            # Top left platform (key area)
            Platform(2400, 20, 300, 30),

            # King platform
            Platform(2600, 500, 300, 30),

            # End platform
            Platform(2900, 510, 300, 30),
        ]

        self.bald_guy = NPC(1900, 710, 100, 200, "images/michael jordan.png")
        self.bald_guy.set_text(
            "Heeheeheehaw, nothing interesting happens if you slide on a wall and let go")

        self.king = NPC(2600, 410, 100, 200, "images/king.png")
        self.king.set_text(
            "Oh no, My scientists have realized that there is a loose time machine, and it resets back every 45 seconds!")

        self.time_machine_img = pg.image.load("images/mchine.png")
        self.time_machine_img = pg.transform.scale(
            self.time_machine_img, (100, 100))

        self.time_x = 3000
        self.time_y = 300

        # self.dt = 1 / 60
        self.scroll = [-500.0, 0]
        self.prev_keys_pressed = pg.key.get_pressed()

    def update(self, dt: float = 1 / 60):

        # Do logical updates here.
        # ...
        keys_pressed = pg.key.get_pressed()

        self.player.update(
            keys_pressed,
            self.prev_keys_pressed,
            dt,
            platformlists=self.platforms,
        )

        # set scroll to tween to player's position
        self.scroll[0] += (self.player.x + 50 - self.screen.get_width() /
                           2 - self.scroll[0]) * min(5 * dt, 1)
        self.scroll[1] += (self.player.y + 100 - self.screen.get_height() /
                           2 - self.scroll[1]) * min(5 * dt, 1)

        # set prev_keys_pressed to current keys pressed
        self.prev_keys_pressed = keys_pressed

        self.prev_keys_pressed = keys_pressed

    def draw(self):
        # Render the graphics here.
        # scrolled graphics
        self.screen.blit(
            pg.transform.scale(pg.image.load("images/images.jpg"),
                               (self.screen.get_width(), self.screen.get_height())),
            (0, 0, self.screen.get_width(), self.screen.get_height()))

        for platform in self.platforms:
            platform.draw(self.screen, self.scroll)
        self.bald_guy.draw(self.screen, self.player, self.scroll)
        self.king.draw(self.screen, self.player, self.scroll)
        self.player.draw(self.screen, self.scroll)
        
        # draw the time machine
        self.screen.blit(self.time_machine_img, (self.time_x - self.scroll[0],
                                                 self.time_y - self.scroll[1], 100, 100))

        # unscrolled graphics
        self.player.draw_health(self.screen)

    def touching_time_machine(self):
        # Check if the player is touching the time machine
        time_machine_rect = self.time_machine_img.get_rect(
            topleft=(self.time_x, self.time_y))

        return self.player.rect.colliderect(time_machine_rect)


class TryAgainScene(Scene):
    def __init__(self, screen: pg.surface.Surface, init_callback):
        super().__init__(screen, init_callback)
        self.redo_button = pg.image.load("images/redo.png")
        self.redo_button = pg.transform.scale(
            self.redo_button, (self.redo_button.get_width() / 2, self.redo_button.get_height() / 2))

    def update(self):
        # Update the scene here
        buttons_pressed = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        if buttons_pressed[0]:
            if self.redo_button.get_rect(topleft=(self.screen.get_width() / 2 - self.redo_button.get_width() / 2,
                                                  self.screen.get_height() / 2 - self.redo_button.get_height() / 2)).collidepoint(mouse_pos):
                # Restart the game
                time_passed = 0

    def if_clicked(self):
        # Check if the redo button is clicked
        buttons_pressed = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        if buttons_pressed[0]:
            if self.redo_button.get_rect(topleft=(self.screen.get_width() / 2 - self.redo_button.get_width() / 2,
                                                  self.screen.get_height() / 2 - self.redo_button.get_height() / 2)).collidepoint(mouse_pos):
                return True
        return False

    def draw(self):
        # Draw the scene here
        self.screen.fill((255, 255, 255))
        self.screen.blit(
            self.redo_button,
            (self.screen.get_width() / 2 - self.redo_button.get_width() / 2,
             self.screen.get_height() / 2 - self.redo_button.get_height() / 2),
        )


class GameWonScene(Scene):
    def __init__(self, screen: pg.surface.Surface, init_callback):
        super().__init__(screen, init_callback)
        self.won_img = pg.image.load("images/End screen 2.png")
        self.won_img = pg.transform.scale(
            self.won_img, (self.screen.get_width(), self.screen.get_height()))

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.won_img, (0, 0))
