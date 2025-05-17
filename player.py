import pygame as pg

import random


class player(pg.sprite.Sprite):
    def __init__(self, width, height, start_x=0, start_y=0, *groups):
        super().__init__(*groups)
        self.width = width
        self.height = height
        self.x = start_x
        self.y = start_y

        self.scaled_img = pg.transform.scale(pg.image.load(
            "image.png"), (self.width, self.height))

        self.y_vel = 0
        self.x_vel = 0

        self.gravity = 500  # units / f^2

        self.ground_state = 1  # 1: on ground
        self.jumps_left = 1

    def draw(self, wn, scroll: tuple = (0, 0)):
        pg.draw.rect(wn, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (self.x -
                     scroll[0], self.y-scroll[1], self.width, self.height))

        wn.blit(self.scaled_img, (self.x -
                                  scroll[0], self.y-scroll[1], self.width, self.height))

    def update(self, keys, prev_keys, dt: float):
        # key input
        k_left_mono = keys[pg.K_LEFT] and not prev_keys[pg.K_LEFT]
        k_right_mono = keys[pg.K_RIGHT] and not prev_keys[pg.K_RIGHT]
        k_left = keys[pg.K_LEFT]
        k_right = keys[pg.K_RIGHT]
        k_up_mono = keys[pg.K_UP] and not prev_keys[pg.K_UP]
        k_up = keys[pg.K_UP]
        k_down = keys[pg.K_DOWN] and not prev_keys[pg.K_DOWN]

        self.collision()
        if k_up_mono and self.jumps > 0:
            self.y_vel = -600
            self.ground_state = 0
            self.jumps -= 1

        # x movements
        self.x += (1000*(k_right-k_left))*dt

        # velocity updates
        self.y_vel += (500-150*k_up*(self.y<0))*dt

        # position updates
        self.y += self.y_vel * dt

    def collision(self):
        if self.y > 720-self.height:
            self.y = 720-self.height
            self.y_vel = 0
            self.ground_state = 1
            self.jumps = 2
        elif self.y < 0:
            self.y = 0
            self.y_vel = 0
            self.ground_state = 0
        else:
            self.ground_state = 0
