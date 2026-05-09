import sys, pygame, math
import matplotlib.pyplot as plt
import numpy as np


def rotate_point(x,y,r):
    return x*math.cos(r) - y*math.sin(r), x*math.sin(r) + y*math.cos(r)
def depressed_cubit(a, b, c): # what a name lol
    # After substitution u = sqrt(x), we get bu^3 + au + c = 0
    # np.roots takes coefficients [b, 0, a, c] for bu^3 + 0u^2 + au + c
    pass
def get_d(x,y):
    a=0
    b=0
    c=0
    coeffs = [b, 0, a, c]
    roots_u = np.roots(coeffs)

    solutions = []
    for u in roots_u:
        if np.isreal(u) and u.real >= 0:  # u = sqrt(x) must be real and non-negative
            solutions.append(u.real ** 2)  # x = u^2

    return solutions