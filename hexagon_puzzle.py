import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from typing import NamedTuple

import libhex, hex_pieces


## Settings
SIZE_MAP = 4   # Map size

# Hex_Grid class. Contains hex position, and grid status. 
# Grid val:
#   0 - not occupied
#   1 - occupied
class Hex_Grid(NamedTuple):
    hex: libhex.Hex
    val: int


# Generate hex map
def Hex_generate_map(map_size):
    Map = []
    for x in range(-map_size, map_size+1):
        for y in range(max(-map_size, -x-map_size), min(+map_size, -x+map_size)+1):
            z = -x-y
            this_grid = Hex_Grid(libhex.Hex(x, y, z), 0)
            Map.append(this_grid)
    return Map


# Find grid position with value
def Hex_search_grid(Map, q, r, s):
    found_match = False
    current_val = 0
    for i in range(len(Map)):
        grid = Map[i]
        hex = grid.hex
        if hex.q == q and hex.r == r and hex.s == s:
            found_match = True
            current_val = grid.val
            break
    return found_match, current_val


# Toggle grid value if found 
def Hex_find_and_set_grid_conditional(Map, q, r, s, new_val):
    val_set_success = False
    found_match = False
    for i in range(len(Map)):
        grid = Map[i]
        hex = grid.hex
        if hex.q == q and hex.r == r and hex.s == s:
            found_match = True
            if grid.val != new_val:
                val_set_success = True
                Map[i] = grid._replace(val=new_val)
            break
    return found_match, val_set_success


## Set problem
Hex_Map = Hex_generate_map(SIZE_MAP)

# Place problem definition grid (single cell with pin)
pin_hex = libhex.Hex(0, 0, 0)

# Set pin hex in grid map to be occupied
found_match, val_set_success = Hex_find_and_set_grid_conditional(Hex_Map, pin_hex.q, pin_hex.r, pin_hex.s, 1)
# print(Hex_Map)

# Generate puzzle pieces
Puzzle_pieces = hex_pieces.generate_all_pieces()

# Solution candidate
Sol_candi = []

# Solver
for i in range(len(Puzzle_pieces)):
    # print("i = ", i)
    this_piece = Puzzle_pieces[i]
    # try an extra piece to see if there is any fit
    flag_break_j_loop = False
    for j in range(3):
        if flag_break_j_loop:
            break
        # print("j = ", j)
        this_piece_form = this_piece.form(j)
        # print(this_piece_form)
        # print(this_piece_form)
        for grid in Hex_Map:
            q_offset = grid.hex.q
            r_offset = grid.hex.r
            s_offset = grid.hex.s
            Hex_Map_Candi = Hex_Map.copy()
            # print(Hex_Map_Candi)
            # print("offset: ", q_offset, r_offset, s_offset)
            flag_all_hex_in_piece_can_fit = True
            for k in range(5):
                # print("k = ", k)
                this_hex = this_piece_form[k]
                q_in = this_hex.q + q_offset
                r_in = this_hex.r + r_offset
                s_in = this_hex.s + s_offset
                found_match, success = Hex_find_and_set_grid_conditional(Hex_Map_Candi, q_in, r_in, s_in, 1)
                # print(found_match, success)
                if not found_match or not success:
                    flag_all_hex_in_piece_can_fit = False
                    break
            # if there is a fit
            if flag_all_hex_in_piece_can_fit:
                # print("Found a fit")
                # print(Hex_Map_Candi)
                # update grid and candidate solution
                Hex_Map = Hex_Map_Candi.copy()
                Sol_candi.append([i, j, q_offset, r_offset, s_offset])
                flag_break_j_loop = True
                break

print(Sol_candi)


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

# Plot pin hex
x = pin_hex.q
y = 2. * np.sin(np.radians(60)) * (pin_hex.r - pin_hex.s) /3.
hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                        orientation=np.radians(30), 
                        facecolor='red', alpha=0.3, edgecolor='k')
ax.add_patch(hex)
dot = RegularPolygon((x, y), numVertices=20, radius=0.1, 
                        facecolor='black', alpha=1, edgecolor='k')
ax.add_patch(dot)

# Plot all pieces on the map
for i in range(len(Sol_candi)):
    piece = Puzzle_pieces[Sol_candi[i][0]]
    piece_form = piece.form(Sol_candi[i][1])
    q_offset = Sol_candi[i][2]
    r_offset = Sol_candi[i][3]
    s_offset = Sol_candi[i][4]
    for hex in piece_form:
        x = hex.q + q_offset
        y = 2. * np.sin(np.radians(60)) * (hex.r + r_offset - hex.s - s_offset) /3.
        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                            orientation=np.radians(30), 
                            facecolor=piece.color, alpha=0.3, edgecolor='k')
        ax.add_patch(hex)
        # Also add a text label
        ax.text(x, y, str(Sol_candi[i][0]), ha='center', va='center', size=7)

ax.autoscale_view()
plt.axis('off')
plt.show()