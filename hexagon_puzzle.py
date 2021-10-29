import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from typing import NamedTuple

import libhex

# Hex_Grid class. Contains hex position, and grid value. 
# Grid value:
#   0 - not occupied
#   1 - occupied
class Hex_Grid(NamedTuple):
    hex: libhex.Hex
    value: int

# Generate hex map
N = 4
Hex_Map = []
for x in range(-N, N+1):
    for y in range(max(-N, -x-N), min(+N, -x+N)+1):
        z = -x-y
        this_grid = Hex_Grid(libhex.Hex(x, y, z), 0)
        Hex_Map.append(this_grid)
#print(Hex_Map)

# Plot the map
fig, ax = plt.subplots(1)
ax.set_aspect('equal')

for grid in Hex_Map:
    hex = grid.hex
    x = hex.q
    y = 2. * np.sin(np.radians(60)) * (hex.r - hex.s) /3.
    hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                         orientation=np.radians(30), 
                         facecolor='orange', alpha=0.2, edgecolor='k')
    ax.add_patch(hex)

ax.autoscale_view()
plt.axis('off')
plt.show()