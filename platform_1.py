import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, *groups) -> None:
        super().__init__(*groups)  # type: ignore
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.transform.scale(pg.image.load(
            "images/platform.png"), (self.width, self.height))
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.prev_being_touched = False
        self.being_touched = False

    def draw(self, wn, scroll: tuple = (0, 0)):
        pg.draw.rect(wn, (0, 0, 255), (self.x - scroll[0], self.y -
                                       scroll[1], self.width, self.height))
        # wn.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

    def collide(self, player):
        prev_being_touched = self.being_touched

        if player.x + player.hitbox_x_offset + player.hitbox_width > self.x and player.x + player.hitbox_x_offset < self.x + self.width:
            if player.y+player.hitbox_y_offset + player.hitbox_height > self.y and player.y+player.hitbox_y_offset < self.y + self.height:

                # collision from above+player.hitbox_y_offset
                if self.y + self.height/10 > player.y+player.hitbox_y_offset + player.hitbox_height > self.y:
                    # print("collision from above")
                    player.y = self.y - player.hitbox_height - player.hitbox_y_offset
                    player.y_vel = 0
                    player.ground_state = 1
                    player.jumps = 2
                    self.being_touched = True
                    if not prev_being_touched:
                        self.enter_platform(player)
                    return 1
                # collision from below
                elif self.y + self.height*9/10 < player.y+player.hitbox_y_offset < self.y + self.height:
                    player.y = self.y + self.height - player.hitbox_y_offset
                    player.y_vel = 0
                    player.ground_state = 0
                    return 2

                # collision from the left
                elif self.x + self.width/10 > player.x + player.hitbox_x_offset + player.hitbox_width > self.x:
                    player.x = self.x - player.hitbox_width - player.hitbox_x_offset
                    player.x_vel = 0

                    return 3
                # collision from the right
                elif self.x + self.width*9/10 < player.x + player.hitbox_x_offset < self.x+self.width:
                    player.x = self.x + self.width - player.hitbox_x_offset
                    player.x_vel = 0

                    return 4

        self.being_touched = False
        if prev_being_touched and not self.being_touched:
            self.leave_platform(player)

    def enter_platform(self, player):
        pass

    def leave_platform(self, player):
        pass


class SlowPlatform(Platform):
    def __init__(self, x, y, width, height, *groups) -> None:
        super().__init__(x, y, width, height, *groups)
        self.image = pg.transform.scale(pg.image.load(
            "images/slow_platform.png"), (self.width, self.height))

    def draw(self, wn, scroll: tuple = (0, 0)):
        pg.draw.rect(wn, (150, 75, 0), (self.x - scroll[0], self.y -
                                        scroll[1], self.width, self.height))
        wn.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

    def enter_platform(self, player):
        print("entering slow platform")
        player.max_speed = 100

    def leave_platform(self, player):
        print("leaving slow platform")
        player.max_speed = 1000


class FastPlatform(Platform):
    def __init__(self, x, y, width, height, *groups) -> None:
        super().__init__(x, y, width, height, *groups)
        self.image = pg.transform.scale(pg.image.load(
            "images/fast_platform.png"), (self.width, self.height))

    def draw(self, wn, scroll: tuple = (0, 0)):
        pg.draw.rect(wn, (255, 0, 0), (self.x - scroll[0], self.y -
                                       scroll[1], self.width, self.height))
        wn.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

    def enter_platform(self, player):
        # print("entering slow platform")
        player.max_speed = 2000
        player.accel = 4000

    def leave_platform(self, player):
        # print("leaving slow platform")
        player.max_speed = 1000
        player.accel = 2000
