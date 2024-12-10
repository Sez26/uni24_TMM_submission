import math
import numpy as np

# Define the radius of the circle
r = 5  # for example, radius = 5

circle = []
for i in range(16):
    x = r * math.cos(2 * math.pi * i / 16.0)  # Multiply by radius
    y = r * math.sin(2 * math.pi * i / 16.0)  # Multiply by radius
    circle.append([x, y])

circle = np.array(circle)
print(circle)