import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

import libhex

# Generate hex map
N = 4
results = []
for x in range(-N, N+1):
    for y in range(max(-N, -x-N), min(+N, -x+N)+1):
        z = -x-y
        results.append(libhex.Hex(x, y, z))
#print(results)

# Plot the map
fig, ax = plt.subplots(1)
ax.set_aspect('equal')

for hex in results:
    x = hex.q
    y = 2. * np.sin(np.radians(60)) * (hex.r - hex.s) /3.
    hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                         orientation=np.radians(30), 
                         facecolor='orange', alpha=0.2, edgecolor='k')
    ax.add_patch(hex)

ax.autoscale_view()
plt.axis('off')
plt.show()