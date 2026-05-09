import sys, pygame, math
import matplotlib.pyplot as plt
import numpy as np


def rotated_curve(f, theta_deg, t_range=(-5, 5), n=10000):
    theta = np.radians(theta_deg)
    t = np.linspace(*t_range, n)

    # Original curve points
    x0 = t
    y0 = f(t)

    # Apply rotation matrix
    x_rot = x0 * np.cos(theta) - y0 * np.sin(theta)
    y_rot = x0 * np.sin(theta) + y0 * np.cos(theta)

    return x_rot, y_rot


# Example: rotate y = sin(x) by 30 degrees
x, y = rotated_curve(np.sqrt, 60)
plt.plot(x, y)
plt.show()