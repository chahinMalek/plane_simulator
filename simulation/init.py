import json
import random
from time import time
from typing import Tuple

import pygame

from objects.geometric_objects import Point2, Polygon, Sphere
from objects.simulation_objects import Flight
from simulation.line_sweep import get_intersections

with open('../resources/constants.json', 'r') as f:
    CONSTANTS = json.load(f)


def get_color(key: str) -> Tuple:
    return tuple(int(x) for x in CONSTANTS[key].split(','))


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

area = Polygon([Point2.from_tuple(point) for point in CONSTANTS['flight_area']])

min_x = min(area, key=lambda p: p.x).x
max_x = max(area, key=lambda p: p.x).x
min_y = min(area, key=lambda p: p.y).y
max_y = max(area, key=lambda p: p.y).y

# list of flight generators
flights = []

running = True
start = time()

while running:

    screen.fill(BG_COLOR)

    pygame.draw.polygon(
        screen,
        get_color('color_black'),
        [x.to_tuple() for x in area.vertices],
        2
    )

    points = []

    for flight in flights:

        try:
            point = next(flight)

            if Point2.from_point3(point) in area:
                points.append(next(flight))

        except StopIteration:
            flights.remove(flight)
            continue

    intersections = get_intersections([Sphere(point, CONSTANTS['plane_radius']) for point in points])

    if time() - start >= CONSTANTS['fg_period']:

        flights_to_generate = random.randint(CONSTANTS['min_fcount'], CONSTANTS['max_fcount'])

        # todo generate random flight types
        for _ in range(flights_to_generate):

            generated_flight = Flight.get_random_flight(
                min_x, max_x,
                min_y, max_y,
                CONSTANTS['min_height'], CONSTANTS['max_height'],
                random.randint(CONSTANTS['plane_min_velocity'], CONSTANTS['plane_max_velocity']),
                CONSTANTS['plane_radius']
            )

            position = generated_flight.get_plane_position()
            c_sphere = Sphere(next(position), CONSTANTS['plane_radius'])
            valid_flight = True

            for point in points:
                if c_sphere.intersects(Sphere(point, CONSTANTS['plane_radius'])):
                    valid_flight = False
                    break

            if valid_flight:
                flights.append(position)

        start = time()

    for point in points:

        pygame.draw.circle(
            screen,
            get_color('color_black') if point.to_tuple() not in intersections else get_color('color_red'),
            (point.x, point.y),
            CONSTANTS['plane_radius'],
            2
        )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = not running

    pygame.display.update()
    clock.tick(10)

pygame.quit()
