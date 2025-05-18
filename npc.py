import pygame as pg
from player import player


class NPC(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, img_filename, *groups):
        super().__init__(*groups)
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.text = "asdkljh"
        self.font = pg.font.Font("fonts/Minecrafter.Reg.ttf", 20)

        self.scaled_img = pg.transform.scale(
            pg.image.load(img_filename), (self.width, self.height)
        )

    def set_text(self, text):
        self.text = text

    def draw(self, wn: pg.surface.Surface, p: player, scroll: list[int] = [0, 0]):
        wn.blit(
            self.scaled_img,
            (self.x - scroll[0], self.y - scroll[1], self.width, self.height),
        )

        # show text on top if colliding
        #print(type(self.rect), type(p))
        if self.rect.colliderect(p.rect):
            text_surface: pg.surface.Surface = self.font.render(self.text, True, (0,0,0))
            wn.blit(
                text_surface,
                (
                    self.rect.midtop[0] - text_surface.get_width() / 2 - scroll[0],
                    self.rect.midtop[1] - text_surface.get_height() - 10 - scroll[1],
                ),
            )
