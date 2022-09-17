import pygame
from math import cos, sin, pi
import numpy as np
from time import sleep
from random import randint


WHITE = (255, 255, 255)
WIDTH = 500
HEIGHT = 500

pygame.init()
display = pygame.display
surface = display.set_mode((WIDTH, HEIGHT))
display.set_caption("3D")


done = False
# points = (
#     ( 150,  150,  150),
#     (-150,  150,  150),
#     (-150, -150,  150),
#     ( 150, -150,  150),
#     ( 150,  150, -150),
#     (-150,  150, -150),
#     (-150, -150, -150),
#     ( 150, -150, -150),
# )

points = [[], [], [], [], [], []]

points[0] = []

points = []

for i in range(0, 4):
    for j in range(0, 4):
        points.append([-150+i*100, -150+j*100, 150])

for i in range(0, 4):
    for j in range(0, 4):
        if i == 0 or i == 3 or j == 0 or j == 3:
            points.append([-150+i*100, -150+j*100, 50])

for i in range(0, 4):
    for j in range(0, 4):
        if i == 0 or i == 3 or j == 0 or j == 3:
            points.append([-150+i*100, -150+j*100, -50])

for i in range(0, 4):
    for j in range(0, 4):
        points.append([-150+i*100, -150+j*100, -150])

rotation = [0, 0, 0]


def generate_x(theta):
    return np.matrix([
        [1, 0, 0],
        [0, cos(theta), -sin(theta)],
        [0, sin(theta), cos(theta)]
    ])

def generate_y(theta):
    return np.matrix([
        [cos(theta), 0, -sin(theta)],
        [0, 1, 0],
        [sin(theta), 0, cos(theta)]
    ])

def generate_z(theta):
    return np.matrix([
        [cos(theta), -sin(theta), 0],
        [sin(theta), cos(theta), 0],
        [0, 0, 1]
    ])


while not done:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
            break

    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT))

    render_points = []

    for p in points:
        m = np.matrix(p).T

        for method, angle in zip((generate_x, generate_y, generate_z), rotation):
            m = method(angle) * m

        x, y, z = map(lambda x: int(WIDTH/2 - x), (m[0,0], m[1,0], m[2,0]))
        render_points.append((WIDTH/2 - m)[:2].flatten().tolist()[0])

    for p1 in render_points:
        pygame.draw.polygon(surface, WHITE, (p1))
    

    # for p1 in range(len(render_points) - 1):
    #     for p2 in range(p1 + 1, len(render_points)):
    #         if p1 + 4 == p2 or (p1//4 == p2//4 and ((p1 + 1)%4 == p2%4 or (p1 + 3)%4 == p2%4)):
    #             pygame.draw.line(surface, WHITE, render_points[p1], render_points[p2])

    rotation[0] += pi / randint(100, 200)
    rotation[1] += pi / randint(100, 200)

    display.flip()
    sleep(1/16)
