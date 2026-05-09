import sys, pygame
from scipy.optimize import fsolve
import random
import os
import math
import numpy as np
import time
def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
def df(x):
    return 1/(2*math.sqrt(x))
def intersection_left(d, fov):
    k = df(d)
    sin_f = np.sin(fov)
    cos_f = np.cos(fov)
    def F(x):
        y = -x / k + d / k
        inside_sqrt = x * cos_f + y * sin_f
        if inside_sqrt < 0:
            return 1e6
        return (-x * sin_f +
                y * cos_f -
                np.sqrt(inside_sqrt))
    x0 = d / 2
    x_sol = fsolve(F, x0)[0]
    y_sol = -x_sol / k + d / k
    return x_sol, y_sol
def intersection_right(d, fov):
    k = df(d)
    sin_f = np.sin(-fov)
    cos_f = np.cos(-fov)
    def F(x):
        y = -x / k + d / k
        inside_sqrt = x * cos_f + y * sin_f
        if inside_sqrt < 0:
            return 1e6
        return (-x * sin_f +
                y * cos_f -
                np.sqrt(inside_sqrt))
    x0 = d / 2
    x_sol = fsolve(F, x0)[0]
    y_sol = -x_sol / k + d / k
    return x_sol, y_sol
def project_x(z,x):
    a = 4 * z * z
    b = -8 * x
    c = 4
    d = - x * x
    roots = np.roots([a, b, c, d])
    d = np.real(roots[0])
    sqrt_d = np.sqrt(d)
    a = 2 * sqrt_d
    b = 1
    c = -2 * d * sqrt_d
    u_roots = np.roots([a, b, c])
    valid_u = u_roots[u_roots >= 0]
    x_solution = valid_u ** 2
    x_solution = x_solution[0]
    mid_parallel = (x_solution, math.sqrt(x_solution))
    left_intersect = intersection_left(d, 0.6)
    # make this use dist function
    dist_mid_left = math.sqrt((mid_parallel[0] - left_intersect[0]) ** 2 + (mid_parallel[1] - left_intersect[1]) ** 2)
    a = 4
    b = -8 * x
    c = 4 * x * x
    d = - z * z
    roots = np.roots([a, b, c, d])
    d = np.real(roots[0])
    sqrt_d = np.sqrt(d)
    a = 2 * sqrt_d
    b = 1
    c = -2 * d * sqrt_d
    u_roots = np.roots([a, b, c])
    valid_u = u_roots[u_roots >= 0]
    x_solution = valid_u ** 2
    x_solution = x_solution[0]
    mid_parallel = (x_solution, math.sqrt(x_solution))
    right_intersect = intersection_right(d, 0.6)
    dist_mid_right = math.sqrt((mid_parallel[0] - right_intersect[0]) ** 2 + (mid_parallel[1] - right_intersect[1]) ** 2)
    point_to_left = dist([x, z], left_intersect)
    point_to_right = dist([x,z], right_intersect)
    dist_mid_point = math.sqrt((mid_parallel[0] - x) ** 2 + (mid_parallel[1] - z) ** 2)
    # if the point is closer to the right then use the right projection
    # else: use the left projection
    print(point_to_right,point_to_left)
    if point_to_right > point_to_left:
        screen_pct_x = dist_mid_point / dist_mid_left
        chosen_side = "left"
    else:
        screen_pct_x = dist_mid_point / dist_mid_right
        chosen_side = "right"

    return screen_pct_x, chosen_side
def project_y(z,y):
    a = 4
    b = -8 * y
    c = 4 * y * y
    d = - z * z
    roots = np.roots([a, b, c, d])
    d = np.real(roots[0])
    sqrt_d = np.sqrt(d)
    a = 2 * sqrt_d
    b = 1
    c = -2 * d * sqrt_d
    u_roots = np.roots([a, b, c])
    valid_u = u_roots[u_roots >= 0]
    print(valid_u)
    y_solution = valid_u ** 2
    y_solution = y_solution[0]
    mid_parallel = (y_solution, math.sqrt(y_solution))
    left_intersect = intersection_left(d, 0.6)
    # make this use dist function
    dist_mid_left = math.sqrt((mid_parallel[0] - left_intersect[0]) ** 2 + (mid_parallel[1] - left_intersect[1]) ** 2)
    dist_mid_point = math.sqrt((mid_parallel[0] - y) ** 2 + (mid_parallel[1] - z) ** 2)
    screen_pct_y = dist_mid_point / dist_mid_left
    return screen_pct_y
def project_point(x, y, z):
    screen_pct_x, chosen_side_x = project_x(x,z)
    screen_pct_y = project_y(y,z)
    print(chosen_side_x)
    if chosen_side_x == "left":

        return [-screen_pct_x * 120 + 240, screen_pct_y * 90 + 180]
    return [screen_pct_x * 120 + 240, screen_pct_y * 90 + 180]

vertices = []
vertice_path = "C:/Users/colin/Downloads/all_vertices.txt"
with open(vertice_path, 'r') as file:
    for line in file:
        spl = line.split(",")
        vertices.insert(0,[float(spl[0]),float(spl[1]),float(spl[2])])
points = [[2,3,5],[7,0.1,10],[2,3.8,5]]
os.environ['SDL_AUDIODRIVER'] = 'dsp'

pygame.init()
size = width, height = 480, 360
speed = [1, 1]
screen = pygame.display.set_mode(size)
pygame.font.init()
cam = [0,0,0]
cam_r = 0
while 1:
    clock = pygame.time.Clock()
    # Limit to 60 frames per second
    clock.tick(60)
    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cam_r += 0.01
    if keys[pygame.K_RIGHT]:
        cam_r -= 0.01
    if keys[pygame.K_a]:
        cam[0] -= 0.1
    if keys[pygame.K_d]:
        cam[0] += 0.1
    if keys[pygame.K_e]:
        cam[1] -= 0.1
    if keys[pygame.K_q]:
        cam[1] += 0.1
    if keys[pygame.K_w]:
        cam[2] -= 0.1
    if keys[pygame.K_s]:
        cam[2] += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    for vertice in vertices:
        try:
            proj = project_point(vertice[0]-cam[0],vertice[1]-cam[1],vertice[2]-cam[2])
            pygame.draw.circle(screen, (255,255,255), (proj[0],proj[1]), 5)
        except:
            continue

    pygame.display.flip()