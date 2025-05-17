import pygame as pg
from pygame.sprite import _Group

class platform(pg.sprite.Sprite):
  def __init__(self, *groups) -> None:
    super().__init__(*groups) # type: ignore