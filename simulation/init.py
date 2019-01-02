import json
from typing import Tuple

import pygame

from objects.geometric_objects import Point2, Polygon

with open('../resources/constants.json', 'r') as f:
    CONSTANTS = json.load(f)


def get_color(key):
    return tuple(int(x) for x in CONSTANTS[key].split(','))


def flip_height(position: Tuple[int, int]):
    return position[0], info.current_h - position[1]


pygame.init()

clock = pygame.time.Clock()
info = pygame.display.Info()

BG_COLOR = get_color('color_white')
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT),
                                 pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

pygame.display.set_caption(CONSTANTS['title'])
screen.fill(BG_COLOR)

pygame.display.flip()

polygon = []

running = True

while running:

    screen.fill(BG_COLOR)

    try:
        pygame.draw.lines(
            screen,
            get_color('color_black'),
            True,
            [flip_height(x.to_tuple()) for x in Polygon.simplify_poly(polygon)],
            2
        )
    except ValueError:
        pass

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = not running

        elif event.type == pygame.MOUSEBUTTONDOWN:
            polygon.append(Point2.from_tuple(flip_height(pygame.mouse.get_pos())))

    pygame.display.update()
    clock.tick(1)

pygame.quit()
