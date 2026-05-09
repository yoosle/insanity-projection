import sys, pygame
import matplotlib.pyplot as plt
import os
import math
import numpy as np
import time

# solve it...then add the transformation matrix

def dist(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
def d_sqrt(x):
    return 1/(2*math.sqrt(x))

def quad(a,b,c):
    d = (b ** 2) - (4 * a * c)
    if d < 0:
        return [0]
    # Calculate two solutions using the quadratic formula: (-b ± sqrt(d)) / 2a
    sol1 = (-b + math.sqrt(d)) / (2 * a)
    sol2 = (-b - math.sqrt(d)) / (2 * a)
    return [sol1, sol2]

def sqrt_fov(x, cam_r, fov):
    inverse_x = -math.sin(cam_r+fov)
    y = math.sqrt(x)

def solve_left_intersect(d, cam_r,fov, df_func,x0=1.0):
    df = df_func(d,cam_r,fov)
    def h(x):
        term1 = x * np.sin(cam_r+fov) + (1/df) * (d - x) * np.cos(cam_r+fov)
        term2_inner = x * np.cos(cam_r+fov) - (1/df) * (d - x) * np.sin(cam_r+fov)
        return term1**2 - np.maximum(term2_inner, 0)
    x = x0
    for _ in range(100):
        dx = 1e-6
        slope = (h(x + dx) - h(x)) / dx
        if slope == 0: break
        x_new = x - h(x) / slope
        if abs(x_new - x) < 1e-8:
            return x_new
        x = x_new
    return x
def solve_right_intersect(d, cam_r,fov, df_func, x0=1.0):
    df = df_func(d,cam_r,-fov)
    def h(x):
        term1 = x * np.sin(cam_r-fov) + (1/df) * (d - x) * np.cos(cam_r-fov)
        term2_inner = x * np.cos(cam_r-fov) - (1/df) * (d - x) * np.sin(cam_r-fov)
        return term1**2 - np.maximum(term2_inner, 0)
    x = x0
    for _ in range(100):
        dx = 1e-6
        slope = (h(x + dx) - h(x)) / dx
        if slope == 0: break
        x_new = x - h(x) / slope
        if abs(x_new - x) < 1e-8:
            return x_new
        x = x_new
    return x
def get_d(p_x, p_y):
    coeffs = [2, 0, -2 * p_x, -p_y]
    roots_u = np.roots(coeffs)
    real_u = roots_u[np.isreal(roots_u) & (roots_u.real >= 0)].real
    solutions_x = real_u**2
    return solutions_x
def solve_mid_intersect(d,cam_r):
    v = sqrt_fov(d,cam_r,0)
    #    return 1000
    coeffs = [(2*v), 1, (-2*(v**3))]
    roots_u = np.roots(coeffs)
    valid_u = roots_u[roots_u >= 0]
    x_solutions = valid_u**2
    return x_solutions
def project_x(z,x,cam_r,fov):
    d = get_d(x,z)
    if not any(d):
        return 1
    d = d[0]
    print(d)
    left_intersect_x = solve_left_intersect(d,cam_r,fov,sqrt_fov)
    left_intersect = (left_intersect_x, sqrt_fov(left_intersect_x,cam_r,fov))
    '''except:
        left_intersect = (1000,1000)'''
    right_intersect_x = solve_right_intersect(d,cam_r,fov,sqrt_fov)
    right_intersect = (right_intersect_x, sqrt_fov(right_intersect_x,cam_r,-fov))
    mid_intersect_x = solve_mid_intersect(d,cam_r)[0]
    mid_intersect = (mid_intersect_x, sqrt_fov(mid_intersect_x,cam_r,0))
    '''except:
        mid_intersect = (0,0)'''
    '''except:
        mid_intersect = (0,0)'''
    dist_mid_point = dist(mid_intersect,[x,z])
    dist_left_point = dist(left_intersect,[x,z])
    dist_right_point = dist(right_intersect,[x,z])
    dist_mid_left = dist(mid_intersect, left_intersect)
    dist_mid_right = dist(mid_intersect, right_intersect)
    #print(dist_mid_point,dist_left_point,dist_right_point)
    #print(dist_mid_left,dist_mid_right)
    if dist_left_point < dist_right_point:
        # point closer to left than right:
        print("left")
        return dist_mid_point/dist_mid_left
    # else:
    print("right")
    return -dist_mid_point/dist_mid_right
def project_point(x,y,z):
    return
'''fig, ax = plt.subplots(4, 4)
ax[0].plot([1, 2, 3], [4, 5, 6]) # Left plot
ax[0].set_title('First Graph')
ax[1].scatter([1, 2, 3], [6, 5, 4]) # Right plot
ax[1].set_title('Second Graph')
r = 0
c = 0
for row in range(0,64,4):

    plot = ax[c][r]
    plot.set_xlim(-1.1,1.1)
    plot.set_ylim(-1.1,1.1)
    for i in range(0,400,2):
        for dos in range(0,2):
            if dos == 0:
                x1 = i / 400
                y1 = sqrt_fov(x1 - 0.5, row / 11, 0, False)
                plot.plot(x1, y1, 'o')
            else:
                x1 = i / 400
                y1 = sqrt_fov(x1 - 0.5, row / 11, 0, True)
                plot.plot(x1, y1, 'o')
    plot.set_title('graph ' + str(round(row/11,2)))
    r += 1
    if r == 4:
        r = 0
        c += 1'''
#plt.show()

#time.sleep(100)
#project_x(1,2)
vertices = []
vertice_path = "C:/Users/colin/Downloads/all_vertices.txt"
with open(vertice_path, 'r') as file:
    for line in file:
        spl = line.split(",")
        vertices.insert(0,[float(spl[0]),float(spl[1]),float(spl[2])])
#os.environ['SDL_AUDIODRIVER'] = 'dsp'
#vertices = [[1,1,1]]
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
    clock.tick(20)
    screen.fill((50, 50, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cam_r += 0.03
    if keys[pygame.K_RIGHT]:
        cam_r -= 0.03
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
            #proj = project_point(vertice[0]-cam[0],vertice[1]-cam[1],vertice[2]-cam[2])
            #print(vertice[0]-cam[0],vertice[1]-cam[1],vertice[2]-cam[2])
            screen_x = project_x(vertice[0]-cam[0],vertice[2]-cam[2],cam_r,0.6)

            screen_x *= 100
            screen_x += 400
            screen_y = project_x(vertice[1] - cam[1], vertice[2] - cam[2], cam_r, 0.6)
            screen_y *= 75
            screen_y += 300
            '''screen_y = project_y(vertice[1]-cam[1],vertice[2]-cam[2],cam_r,0.6)
            screen_y *= 90
            screen_y += 180'''
            pygame.draw.circle(screen, (255,255,255), (screen_x,screen_y), 5)
        except:
            print('point off screen')
    pygame.draw.rect(screen, color=(100,100,70),rect=(0,height-60,80,60))
    for vertice in vertices:
        #v = (vertice[0] - cam[0], vertice[1]-cam[1],vertice[2],cam[2])
        pygame.draw.circle(screen, (255,100,0), (vertice[0]+40,vertice[2]+150), 2)
    pygame.draw.circle(screen, (0,200,0), (cam[0]+40,cam[2]+150),2)
    pygame.display.flip()