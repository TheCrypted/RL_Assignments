import math
import random

import pygame
import numpy as np
pygame.init()

SCREEN_WIDTH = 1028
SCREEN_HEIGHT = 720
color_rgb = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0), "orange": (255, 165, 0), "purple": (128, 0, 128), "pink": (255, 192, 203)}

FPS = 60
run = True
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
track_coords = []
track_coords_drawn = []
final_coords = []
button_hold = False


def l2_dist(point_a, point_b):
    return math.sqrt(np.sum((np.array(point_a) - np.array(point_b)) ** 2))

def sort_b(coords, arranged_arr, track_coords_inp):
    arranged = []
    temp = [0] * len(track_coords_inp)
    closest_point = sorted(coords, key=lambda x: l2_dist(x, (0, 0)), reverse=False)[0]
    arranged.append(closest_point)

    while len(arranged) <= len(coords):
        point_start = arranged[-1]
        arranged_spec = sorted(coords, key=lambda x: l2_dist(x, point_start), reverse=False)[1:]
        if arranged_spec[0] not in arranged:
            arranged.append(arranged_spec[0])
        else:
            arranged.append(arranged_spec[1])

    for coordA, orig in zip(arranged_arr, track_coords_inp):
        temp[arranged.index(coordA)] = orig

    return arranged[:-1], temp



def sort_a(coords, track_coords_inp):
    arranged = sorted(coords, key=lambda x: l2_dist(x, (0, 0)), reverse=True)
    temp = [0]*len(coords)
    for coords, orig in zip(coords, track_coords_inp):
        temp[arranged.index(coords)] = orig

    return arranged, temp


while run:
    screen.fill(color_rgb["black"])
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for cone in track_coords:
        pygame.draw.circle(screen, color_rgb["white"], cone, 7)

    if len(final_coords) == len(track_coords) and len(final_coords) > 0:
        for i in range(len(track_coords_drawn)-1):
            # print(track_coords_drawn[i])
            pygame.draw.line(screen, color_rgb["red"], track_coords_drawn[i], track_coords_drawn[i+1], 7)

    if button_hold:
        dist_to_prev = l2_dist(track_coords[-1], (mouse_x, mouse_y)) if len(track_coords) > 0 else 0
        if dist_to_prev > 60 or len(track_coords) == 0:
            track_coords.append((mouse_x, mouse_y))

    key = pygame.key.get_pressed()
    if key[pygame.K_q]:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button_hold = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_hold = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_t:
                new_center = (track_coords[0][0] - 10, track_coords[0][1])
                final_coords = []
                for coord in track_coords:
                    x, y = coord
                    x_origin, y_origin = new_center
                    final_coords.append((x - x_origin, y - y_origin))
                print(track_coords)
                sorted_arr= random.sample(final_coords, len(final_coords))
                final_coords, track_coords_drawn = sort_b(sorted_arr, final_coords, track_coords)
                print(track_coords_drawn)

    pygame.display.update()
    # pygame.display.flip()
    clock.tick(FPS)