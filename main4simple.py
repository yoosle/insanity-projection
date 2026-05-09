import pygame, sys
from math import *
def rotate_point(x,y,r):
    return (x * cos(r) - y * sin(r), x * sin(r) + y * cos(r))
def func_y(y):
    return abs(sqrt(y)*sin(y))+1
def func_x(x):
    return abs(sqrt(x)*sin(x))+1
def project_y(y,z):
    return y/(func_y(z))
def project_x(x,z):
    return x/(func_x(z))

vertices = []
vertice_path = "C:/Users/colin/Downloads/all_vertices.txt"
with open(vertice_path, 'r') as file:
    for line in file:
        spl = line.split(",")
        vertices.insert(0,[float(spl[0]),float(spl[1]),float(spl[2])])
points = [[2,3,5],[7,0.1,10],[2,3.8,5]]
vertices = []
for x in range(-5,5):
    for y in range(-5,5):
        for z in range(-5,5):
            vertices.insert(0,(x,y,z))
pygame.init()
size = width, height = 800, 600
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
            rel_x = vertice[0]-cam[0]
            rel_y = vertice[1] - cam[1]
            rel_z = vertice[2] - cam[2]
            rot_1 = rotate_point(rel_x,rel_z,cam_r)
            rot_2 = rotate_point(rel_y,rel_z,cam_r)
            proj_x = project_x(rot_1[0],rot_1[1])
            proj_y = project_y(rot_2[0],rot_2[1])
            screen_x = proj_x * 200 + 400
            screen_y = proj_y * 150 + 300
            pygame.draw.circle(screen, (255,255,255), (screen_x,screen_y), 5)
        except:
            continue

    pygame.display.flip()