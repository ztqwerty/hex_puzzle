import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from typing import NamedTuple

import libhex, hex_pieces


## Settings
SIZE_MAP = 4   # Map size

# Hex_Grid class. Contains hex position, and grid value. 
# Grid value:
#   0 - not occupied
#   1 - occupied
class Hex_Grid(NamedTuple):
    hex: libhex.Hex
    value: int

# Generate hex map
def Hex_generate_map(map_size):
    Map = []
    for x in range(-map_size, map_size+1):
        for y in range(max(-map_size, -x-map_size), min(+map_size, -x+map_size)+1):
            z = -x-y
            this_grid = Hex_Grid(libhex.Hex(x, y, z), 0)
            Map.append(this_grid)
    return Map


## Set problem
Hex_Map = Hex_generate_map(SIZE_MAP)

# Place problem definition grid (single cell with pin)
pin_hex = libhex.Hex(0, 0, 0)

# Generate puzzle pieces
Puzzle_pieces = hex_pieces.generate_all_pieces()


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

for piece in Puzzle_pieces:
    piece_form = piece.form_0
    for hex in piece_form:
        x = hex.q
        y = 2. * np.sin(np.radians(60)) * (hex.r - hex.s) /3.
        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                            orientation=np.radians(30), 
                            facecolor=piece.color, alpha=0.3, edgecolor='k')
        ax.add_patch(hex)

ax.autoscale_view()
plt.axis('off')
plt.show()