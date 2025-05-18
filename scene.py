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
        self.player = player(100, 200, 0, 100)
        self.player.set_hitbox(25, 0, 50, 200)

        self.platform1 = Platform(1000, 250, 220, 120)
        self.platform2 = SlowPlatform(700, 250, 220, 120)
        self.platform3 = FastPlatform(400, 250, 220, 120)
        self.platform4 = IcePlatform(100, 250, 220, 120)

        self.king = NPC(1000, 500, 100, 200, "images/michael jordan.png")
        self.king.set_text(
            "Heeheeheehaw,\nnothing interesting happens if you slide on a wall and let go")

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
            platformlists=[self.platform1, self.platform2,
                           self.platform3, self.platform4],
        )

        # set scroll to tween to player's position
        self.scroll[0] += (self.player.x - self.screen.get_width() /
                           2 - self.scroll[0]) * max(5 * dt, 1)
        self.scroll[1] = self.player.y // self.screen.get_height() * \
            self.screen.get_height()

        # set prev_keys_pressed to current keys pressed
        self.prev_keys_pressed = keys_pressed

        self.prev_keys_pressed = keys_pressed

    def draw(self):
        # Render the graphics here.
        # scrolled graphics
        self.platform1.draw(self.screen, self.scroll)
        self.platform2.draw(self.screen, self.scroll)
        self.platform3.draw(self.screen, self.scroll)
        self.platform4.draw(self.screen, self.scroll)
        self.king.draw(self.screen, self.player, self.scroll)
        self.player.draw(self.screen, self.scroll)
        
        # unscrolled graphics
        self.player.draw_health(self.screen)
