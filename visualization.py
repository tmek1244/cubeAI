from typing import Callable
import pygame
from math import cos, sin, pi
import numpy as np
from time import sleep
from random import randint
import time

from cube import Cube


WIDTH = 500
HEIGHT = 500

pygame.init()
display = pygame.display
surface = display.set_mode((WIDTH, HEIGHT))
display.set_caption("3D")


done = False

def generate_x(theta):
    return np.matrix([
        [1, 0, 0],
        [0, cos(theta), -sin(theta)],
        [0, sin(theta), cos(theta)]
    ])

def generate_y(theta):
    return np.matrix([
        [cos(theta), 0, sin(theta)],
        [0, 1, 0],
        [-sin(theta), 0, cos(theta)]
    ])

def generate_z(theta):
    return np.matrix([
        [cos(theta), -sin(theta), 0],
        [sin(theta), cos(theta), 0],
        [0, 0, 1]
    ])


class Square:
    def __init__(self, gen: Callable, id: int = -1) -> None:
        self.id = id
        # np.matrix(p[i]).T * 100 - 150
        tmp = []
        for i in [(0,0), (0,1), (1,1), (1,0)]:
            tmp.append(np.matrix(gen(i)).T * 100 - 150)
            # self.coords.append(gen(i))
        self.matrix_coords = np.asarray(tmp, dtype=np.float32).reshape(4, -1)
        self.rotated = self.matrix_coords

    def rotate(self, rotation):
        m = self.matrix_coords.T
        for method, angle in zip((generate_x, generate_y, generate_z), rotation):
            m = method(angle) @ m
        m += 250
        m = m.T
        m[:, 2] = 500 - m[:, 2]
        self.rotated = m
        # self.rotated = (WIDTH/2 - m).T
        

points = [[], [], [], [], [], []]

points[0] = [
    Square(lambda x: (i+x[0], j+x[1], 3), (2 - j)*3+i) for i in range(3) for j in range(3)
]
points[1] = [
    Square(lambda x: (i+x[0], 0, j+x[1]), (2-j)*3+i+9) for i in range(3) for j in range(3)
]
points[2] = [
    Square(lambda x: (3, i+x[0], j+x[1]), (2 - j)*3+(i)+18) for i in range(3) for j in range(3)
]
points[3] = [
    Square(lambda x: (i+x[0], 3, j+x[1]), (2-j)*3+i+27) for i in range(3) for j in range(3)
]
points[4] = [
    Square(lambda x: (0, i+x[0], j+x[1]), (2 - j)*3+(2 - i)+36) for i in range(3) for j in range(3)
]
points[5] = [
    Square(lambda x: (i+x[0], j+x[1], 0), j*3+i+45) for i in range(3) for j in range(3)
]
points = np.asarray(points)

def draw_point(x, y, z, rotation):
    m = np.matrix([x, y, z]).T * 100 - 150
        
    for method, angle in zip((generate_x, generate_y, generate_z), rotation):
        m = method(angle) * m
    m = m + 250
    m[2] = 500 - m[2]
    pygame.draw.circle(surface, (128, 128, 128), m[[0, 2]].T.tolist()[0], 10)


if __name__ == '__main__':
    # rotation = np.array([-1.3744469, -2.6507194, 0], dtype=np.float32)
    rotation = np.array([0, 0, 0], dtype=np.float32)

    start_time = time.time()
    x = 5
    counter = 0

    cube = Cube()
    cube.reset()
    # cube.r()

    while not done:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
                break
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_d:
                    cube.d()
                if e.key == pygame.K_u:
                    cube.u()
                if e.key == pygame.K_r:
                    cube.r()
                if e.key == pygame.K_l:
                    cube.l()
                if e.key == pygame.K_LEFT:
                    rotation[0] += pi / 32         
                if e.key == pygame.K_RIGHT:
                    rotation[0] -= pi / 32   
                if e.key == pygame.K_DOWN:
                    rotation[1] += pi / 32 
                if e.key == pygame.K_UP:
                    rotation[1] -= pi / 32 
                if e.key == pygame.K_LCTRL:
                    rotation[2] += pi / 32
                if e.key == pygame.K_LSHIFT:
                    rotation[2] -= pi / 32
                print(rotation)
           
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT))

        for p in points.flat:
            if not p:
                continue
            p.rotate(rotation)

        # render_points = np.array([p.rotate(rotation) for p in points.flat])
        for i, p1 in enumerate(sorted(points.flat, key=lambda x: max(x.rotated[:, 1]), reverse=True)):
            pygame.draw.polygon(surface, cube.get_color(p1.id), p1.rotated[:, [0, 2]].tolist())
        # break
        draw_point(0, 0, 0, rotation)
        # draw_point(0, 0, 3, rotation)
        # draw_point(0, 3, 0, rotation)
        # draw_point(3, 0, 0, rotation)
        # draw_point(0, 0, 3, rotation)
        # rotation += np.array([pi / randint(100, 200), pi / randint(100, 200), 0], dtype=np.float32)

        display.flip()
        counter+=1
        if (time.time() - start_time) > x :
            # print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
        sleep(1/50)
