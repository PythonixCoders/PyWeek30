import random
import sys
import pygame
from pytmx.util_pygame import load_pygame
import pyscroll
from settings import *

from hero import Hero
from utils import Position, object_to_rect


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


class Game:
    def __init__(self):
        pygame.init()

        self.FPS = 60
        self.BG_COLOR = pygame.Color("black")
        self.GAME_AREA_POS = Position(96, 32)
        self.GAME_AREA_SIZE = (15, 15)
        self.GAME_AREA_SIZE_PIXELS = (self.GAME_AREA_SIZE[0] * 16, self.GAME_AREA_SIZE[1] * 16)
        self.screen = pygame.display.set_mode((self.GAME_AREA_SIZE_PIXELS[0] + self.GAME_AREA_POS.x, self.GAME_AREA_SIZE_PIXELS[1] + self.GAME_AREA_POS.y), pygame.SCALED)
        self.clock = pygame.time.Clock()

        self.hero = Hero()

        self.wait = False  # Wait for something to end, stop character updates
        self.actions = []

        # Map data
        self.map_surface = pygame.Surface(self.GAME_AREA_SIZE_PIXELS)
        self.tmx_data = None
        self.map_data = None
        self.map_layer = None
        self.map_sprite_group = None
        self.spawns = None
        self.impassables = None
        self.doors = None

        self.load_map("level1", "spawn1")

    def load_map(self, map_name, spawn_point):
        self.tmx_data = load_pygame(BASEDIR / "assets" / "maps" / f"{map_name}.tmx")
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(self.map_data, self.GAME_AREA_SIZE_PIXELS)
        self.map_sprite_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)

        # Find first spawn point
        spawns_layer = self.tmx_data.get_layer_by_name("spawns")
        self.spawns = {spawn.name: [spawn.x, spawn.y] for spawn in spawns_layer}
        self.hero.position = self.spawns[spawn_point]
        self.map_sprite_group.add(self.hero)

        # Build impassable rect list
        impassables_layer = self.tmx_data.get_layer_by_name("impassables")
        self.impassables = [object_to_rect(o) for o in impassables_layer]

        doors_layer = self.tmx_data.get_layer_by_name("doors")
        self.doors = [(object_to_rect(o), o) for o in doors_layer]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if self.wait:
            self.hero.velocity = [0, 0]
            return

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            self.hero.anim_dir = "left"
            self.hero.velocity[0] = -1
        elif pressed[pygame.K_RIGHT]:
            self.hero.anim_dir = "right"
            self.hero.velocity[0] = 1
        else:
            self.hero.velocity[0] = 0
        if pressed[pygame.K_UP]:
            self.hero.anim_dir = "up"
            self.hero.velocity[1] = -1
        elif pressed[pygame.K_DOWN]:
            self.hero.anim_dir = "down"
            self.hero.velocity[1] = 1
        else:
            self.hero.velocity[1] = 0
            
    def update(self, dt):
        if self.wait:
            return

        self.map_sprite_group.update(dt)
        self.map_sprite_group.center(self.hero.rect.center)
        if self.hero.feet.collidelist(self.impassables) != -1:
            self.hero.move_back()

        # Check doors:
        for rect, door in self.doors:
            if self.hero.feet.colliderect(rect):
                to_map = door.properties["to_map"]
                to_spawn = door.properties["to_spawn"]
                self.wait = True
                self.actions.append(MapTransitionIn(self, lambda: self.next_map(to_map, to_spawn)))

    def next_map(self, map_name, spawn_name):
        self.load_map(map_name, spawn_name)
        self.map_sprite_group.update(0)
        self.map_sprite_group.center(self.hero.rect.center)
        self.actions = [MapTransitionOut(self, lambda: self.start_map())]

    def start_map(self):
        self.wait = False
        self.actions = []

    def render(self, surface):
        self.map_sprite_group.draw(self.map_surface)
        surface.blit(self.map_surface, self.GAME_AREA_POS.int_xy)

        # UI
        pygame.draw.rect(surface, pygame.Color("yellow"), pygame.Rect(0, 0, self.GAME_AREA_SIZE_PIXELS[0] + 96, 32))
        pygame.draw.rect(surface, pygame.Color("brown"), pygame.Rect(0, 32, 96, self.GAME_AREA_SIZE_PIXELS[1]))

        for action in self.actions[:]:
            action()

    def run(self):
        while True:
            self.handle_events()
            dt = self.clock.tick(self.FPS) / 1000.0
            self.screen.fill(self.BG_COLOR)
            self.update(dt)
            self.render(self.screen)

            pygame.display.flip()
