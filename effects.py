import random

import pygame


class MapTransitionIn:
    def __init__(self, game, done):
        self.BLOCK_SIZE = 10
        self.screen = game.screen
        self.size = game.GAME_AREA_SIZE_PIXELS
        self.surface = pygame.Surface(game.GAME_AREA_SIZE_PIXELS, pygame.SRCALPHA)
        self.pos = game.GAME_AREA_POS.int_xy
        self.done = done
        self.rects = []
        for x in range(0, self.size[0], self.BLOCK_SIZE):
            for y in range(0, self.size[1], self.BLOCK_SIZE):
                self.rects.append(pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))
        random.shuffle(self.rects)

    def __call__(self):
        for _ in range(10):
            if not self.rects:
                self.done()
                return
            r = self.rects.pop()
            self.surface.fill(pygame.Color("black"), r)
            self.screen.blit(self.surface, self.pos)


class MapTransitionOut:
    def __init__(self, game, done):
        self.BLOCK_SIZE = 10
        self.screen = game.screen
        self.size = game.GAME_AREA_SIZE_PIXELS
        self.surface = pygame.Surface(game.GAME_AREA_SIZE_PIXELS, pygame.SRCALPHA)
        self.surface.fill(pygame.Color("black"))
        self.pos = game.GAME_AREA_POS.int_xy
        self.done = done
        self.rects = []
        for x in range(0, self.size[0], self.BLOCK_SIZE):
            for y in range(0, self.size[1], self.BLOCK_SIZE):
                self.rects.append(pygame.Rect(x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))
        random.shuffle(self.rects)

    def __call__(self):
        for _ in range(10):
            if not self.rects:
                self.done()
                return
            r = self.rects.pop()
            self.surface.fill((0, 0, 0, 0), r)
            self.screen.blit(self.surface, self.pos)