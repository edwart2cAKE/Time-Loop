import pygame as pg
from platform_1 import Platform

import random
import math


class player(pg.sprite.Sprite):
    def __init__(self, width, height, start_x=0, start_y=0, *groups):
        super().__init__(*groups)
        self.width = width
        self.height = height
        self.x = start_x
        self.y = start_y

        self.hitbox_width = width
        self.hitbox_height = height
        self.hitbox_x_offset = 0
        self.hitbox_y_offset = 0

        self.scaled_img = pg.transform.scale(
            pg.image.load("images/main_character.png"), (self.width, self.height)
        )
        self.right_scaled_run1 = pg.transform.scale(
            pg.image.load("images/run 1.png"), (int(self.width * 1.2), self.height)
        )
        self.right_scaled_run2 = pg.transform.scale(
            pg.image.load("images/run 2.png"), (int(self.width * 1), self.height)
        )
        self.left_scaled_run1 = pg.transform.flip(self.right_scaled_run1, True, 0)
        self.left_scaled_run2 = pg.transform.flip(self.right_scaled_run2, True, 0)
        self.dist = 0

        self.max_speed = 1000
        self.accel = 2000
        self.slipperiness = 0.01

        self.health = 2
        self.heart_size = 40
        self.alive_heart_img = pg.transform.scale(
            pg.image.load("images/heartalive.png"), (self.heart_size, self.heart_size)
        )
        self.dead_heart_img = pg.transform.scale(
            pg.image.load("images/heartdead.png"), (self.heart_size, self.heart_size)
        )

        self.y_vel = 0
        self.x_vel = 0
        self.px_vel = 0

        self.gravity = 500  # units / f^2

        self.ground_state = 1  # 1: on ground
        self.jumps_left = 1

    def set_hitbox(self, x_offset, y_offset, width, height):
        self.hitbox_width = width
        self.hitbox_height = height
        self.hitbox_x_offset = x_offset
        self.hitbox_y_offset = y_offset

    def draw(self, wn, scroll: tuple = (0, 0)):
        # draw hitbox
        # pg.draw.rect(wn, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (self.x + self.hitbox_x_offset -
        #             scroll[0], self.y-scroll[1] + self.hitbox_y_offset, self.hitbox_width, self.hitbox_height))

        walk_dist_per_frame = 50

        reset_dist = (self.px_vel > 0) ^ (self.x_vel > 0)
        if reset_dist:
            self.dist = 0
        else:
            self.dist += abs(self.x_vel * 1 / 60)

        facing_right = self.x_vel > 0
        anim_frame = (
            (
                self.right_scaled_run1
                if (self.dist // walk_dist_per_frame) % 2
                else self.right_scaled_run2
            )
            if facing_right
            else (
                self.left_scaled_run1
                if (self.dist // walk_dist_per_frame) % 2
                else self.left_scaled_run2
            )
        )

        wn.blit(
            anim_frame,
            (self.x - scroll[0]-15*(anim_frame==self.left_scaled_run1), self.y - scroll[1], self.width, self.height),
        )
        self.px_vel = self.x_vel

    def draw_health(self, wn: pg.Surface):
        health_bar_pos = (20, 20)
        heart_spacing = 20

        if self.health == 3:
            health_list = [1, 1, 1]
        elif self.health == 2:
            health_list = [1, 1, 0]
        elif self.health == 1:
            health_list = [1, 0, 0]
        else:
            health_list = [0, 0, 0]

        for i, heart in enumerate(health_list):
            wn.blit(
                self.alive_heart_img if heart else self.dead_heart_img,
                (
                    health_bar_pos[0] + i * (heart_spacing + self.heart_size),
                    health_bar_pos[1],
                    self.heart_size,
                    self.heart_size,
                ),
            )

    def update(self, keys, prev_keys, dt: float, platformlists: list[Platform] = []):

        # key input
        k_left_mono = keys[pg.K_LEFT] and not prev_keys[pg.K_LEFT]
        k_right_mono = keys[pg.K_RIGHT] and not prev_keys[pg.K_RIGHT]
        k_up_mono = keys[pg.K_UP] and not prev_keys[pg.K_UP]
        k_down = keys[pg.K_DOWN] and not prev_keys[pg.K_DOWN]
        k_e_mono = keys[pg.K_e] and not prev_keys[pg.K_e]

        k_left = keys[pg.K_LEFT]
        k_right = keys[pg.K_RIGHT]
        k_up = keys[pg.K_UP]

        self.collision(platformlists)

        # jump
        if k_up_mono and self.jumps > 0:
            self.y_vel = -600
            self.ground_state = 0
            self.jumps -= 1

        # dash with e
        if k_e_mono:
            self.x_vel = (2 * (self.x_vel > 0) - 1) * self.max_speed

        # x movements
        self.x_vel += (self.accel * (k_right - k_left)) * dt
        self.x_vel = pg.math.clamp(self.x_vel, -self.max_speed, self.max_speed) * (
            self.slipperiness**dt
        )
        self.x += self.x_vel * dt

        # velocity updates
        self.y_vel += (500 - 150 * k_up * (self.y < 0)) * dt

        # position updates
        self.y += self.y_vel * dt

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def collision(self, platforms: list[Platform] = []):

        # collision with the ground and ceiling
        if self.y + self.hitbox_y_offset > 720 - self.hitbox_height:
            self.y = 720 - self.hitbox_height - self.hitbox_y_offset
            self.y_vel = 0
            self.ground_state = 1
            self.jumps = 2
        else:
            self.ground_state = 0

        # collision with platforms
        for platform in platforms:
            platform.collide(self)
