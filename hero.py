import pygame
from settings import *
from utils import image_load


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos=None):
        super().__init__()
        self._sheet = image_load(BASEDIR / "assets" / "images" / "characters.png").convert_alpha()
        self.animation = {}
        self._position = pos or [0, 0]
        self.velocity = [0, 0]
        self.anim_dir = "down"
        self.frame = 0.0
        self.frame_speed = 3.0
        self.speed = 20

        for i, anim in enumerate(["down", "left", "right", "up"]):
            r = pygame.Rect((3 * 16, 16 * i), (16, 16))
            self.animation.setdefault(anim, []).append(self._sheet.subsurface(r))
            r.left += 16
            self.animation.setdefault(anim, []).append(self._sheet.subsurface(r))
            r.left += 16
            self.animation.setdefault(anim, []).append(self._sheet.subsurface(r))

        self.image = self.animation[self.anim_dir][int(self.frame)]
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width + 4, 4)
        self._old_position = self.position

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, dt):
        self._old_position = self._position[:]
        if self.velocity == [0, 0]:
            self.frame = 1.0
            self.frame_speed = 3.0
        else:
            # Make this to ping pong
            self.frame += self.frame_speed * dt
            if self.frame < 0.0:
                self.frame_speed = -self.frame_speed
                self.frame = 0.0
            if self.frame >= 3.0:
                self.frame_speed = -self.frame_speed
                self.frame = 2.99

            self._position[0] += self.velocity[0] * self.speed * dt
            self._position[1] += self.velocity[1] * self.speed * dt

        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        self.image = self.animation[self.anim_dir][int(self.frame)]

    def move_back(self):
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
