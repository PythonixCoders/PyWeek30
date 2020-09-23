import argparse
import pygame
from game import Game

parser = argparse.ArgumentParser(description="PythonixCoders PyWeek30")
parser.add_argument("--map", dest="map_name", help="Map name to load")
parser.add_argument("--spawn", dest="spawn_name", help="Spawn to start from")

if __name__ == "__main__":
    args = parser.parse_args()
    args_dict = {k: v for k, v in vars(args).items() if v}
    pygame.init()
    game = Game(**args_dict)
    game.run()
