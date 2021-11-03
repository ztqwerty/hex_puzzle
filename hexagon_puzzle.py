import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Polygon
import numpy as np
from typing import NamedTuple
import time
import math

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


def Hex_reachable(Map, hex_start, movement):
    t0 = time.time()
    # add start to visited
    fringes = [] # array of arrays of hexes
    Hex_find_and_set_grid_conditional(Map, hex_start.q, hex_start.r, hex_start.s, 1)
    fringes.append([hex_start])
    cavity_num = 1 # hex start is the first cavity

    for k in range(1, movement):
        fringes.append([])
        for hex in fringes[k-1]:
            for dir in range(6):
                hex_neighbor = libhex.hex_neighbor(hex, dir)
                found_match, val_set_success = Hex_find_and_set_grid_conditional(Map, hex_neighbor.q, hex_neighbor.r, hex_neighbor.s, 1)
                if found_match and val_set_success:
                # if neighbor not in visited and not blocked:
                    #add neighbor to visited
                    fringes[k].append(hex_neighbor)
                    cavity_num = cavity_num + 1

    # print("Time elapsed - Hex_reachable:", time.time()-t0)
    return fringes, cavity_num


def Hex_check_if_all_remaining_hex_good(Map):
    t0 = time.time()
    Map_copy = Map.copy()
    for grid in Map_copy:
        if grid.val == 0:
            fringes, cavity_num = Hex_reachable(Map_copy, grid.hex, 30)
            # print(fringes, cavity_num)
            if cavity_num % 5 != 0:
                return False
    # print("Time elapsed - Hex_check_if_all_remaininng_hex_good:", time.time()-t0)

    return True


_hex_global_ctr = 0
def Hex_verify_candi_with_level(Map_copy, Puzzle_pieces, Candi):
    if Candi:
        level = len(Candi)
    else:
        level = 0
    # check if next level has a solution (recursively)
    for j in range(3):
        for grid in Map_copy:
            # skip grids that are occupied
            if (grid.val == 1):
                continue
            q_offset = grid.hex.q
            r_offset = grid.hex.r
            s_offset = grid.hex.s
            Candi_next = [level, j, q_offset, r_offset, s_offset]
            result, Map_out, Candi_out = Hex_verify_candi_with_next_level(Map_copy, Puzzle_pieces, Candi, Candi_next)
            if result:
                if len(Candi_out) != hex_pieces.NUM_OF_PIECES:
                    # if the current solution is bad with impossible vacant grids to fill, skip and continue
                    if not Hex_check_if_all_remaining_hex_good(Map_out):
                        continue
                    global _hex_global_ctr
                    _hex_global_ctr = _hex_global_ctr + 1
                    if _hex_global_ctr % 20 == 0:
                        # print(_hex_global_ctr)
                        Hex_plot_current_candi(Hex_Map_Original_Copy, pin_hex, Candi_out)
                    Hex_verify_candi_with_level(Map_out, Puzzle_pieces, Candi_out)
                else:
                    # Found a solution! Return it
                    print("Found a solution:", Candi_out)
                    Hex_plot_current_candi(Hex_Map_Original_Copy, pin_hex, Candi_out)
                    return Candi_out


# Verify whether a new piece (defined by Candi_next) can fit in a map status
# Return success/fail with updated map and candi
def Hex_verify_candi_with_next_level(Map_copy, Puzzle_pieces, Candi_old, Candi_next):
    t0 = time.time()
    Map_test = Map_copy.copy()
    this_piece = Puzzle_pieces[Candi_next[0]]
    this_piece_form = this_piece.form(Candi_next[1])
    q_offset = Candi_next[2]
    r_offset = Candi_next[3]
    s_offset = Candi_next[4]
    for k in range(5):
        this_hex = this_piece_form[k]
        q_in = this_hex.q + q_offset
        r_in = this_hex.r + r_offset
        s_in = this_hex.s + s_offset
        found_match, success = Hex_find_and_set_grid_conditional(Map_test, q_in, r_in, s_in, 1)
        # print(found_match, success)
        if not found_match or not success:
            return False, Map_copy, Candi_old
    # if there is a fit
    if Candi_old:
        Candi_new = Candi_old.copy()
        Candi_new.append(Candi_next)
    else:
        Candi_new = [Candi_next]

    # print("Time elapsed - Hex_verify_candi_with_next_level:", time.time()-t0)
    return True, Map_test, Candi_new


def Hex_plot_cube_edges(x, y):
    plt.plot(x + 0.75*np.array([0, 0]), y + 0.75*np.array([0, -1]), 'k', alpha=0.3)
    plt.plot(x + 0.75*np.array([0, math.sqrt(3)/2]), y + 0.75*np.array([0, 0.5]), 'k', alpha=0.3)
    plt.plot(x + 0.75*np.array([0, -math.sqrt(3)/2]), y + 0.75*np.array([0, 0.5]), 'k', alpha=0.3)


def Hex_plot_current_candi(Hex_Map, pin_hex, Sol_candi):
    t0 = time.time()
    if not Sol_candi:
        return

    flag_show_number = False

    plt.close()
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')

    cube_array = 0.75 * np.array([[-math.sqrt(3)/2, 0], [-math.sqrt(3)/2, 0.5], [-math.sqrt(3)/4, 0.75], [0, 0.5], 
                                [math.sqrt(3)/4, 0.75], [math.sqrt(3)/2, 0.5], [math.sqrt(3)/2, 0], [math.sqrt(3)/4, -0.25], 
                                [math.sqrt(3)/4, -0.75], [0, -1], [-math.sqrt(3)/4, -0.75], [-math.sqrt(3)/4, -0.25]])

    for grid in Hex_Map:
        hex = grid.hex
        x = hex.q
        y = 2. * np.sin(np.radians(60)) * (hex.r - hex.s) /3.
        cube = Polygon([x, y] + cube_array, closed=True, 
                    facecolor='orange', alpha=0.2, edgecolor='None')
        ax.add_patch(cube)

    # Plot pin hex
    x = pin_hex.q
    y = 2. * np.sin(np.radians(60)) * (pin_hex.r - pin_hex.s) /3.
    cube = Polygon([x, y] + cube_array, closed=True, 
                    facecolor='red', alpha=0.3, edgecolor='k')
    ax.add_patch(cube)
    if not flag_show_number:
        Hex_plot_cube_edges(x, y)
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
            cube = Polygon([x, y] + cube_array, closed=True, 
                            facecolor=piece.color, alpha=0.3, edgecolor='k')
            ax.add_patch(cube)
            if not flag_show_number:
                Hex_plot_cube_edges(x, y)
            else:
                # Also add a text label
                ax.text(x, y, str(Sol_candi[i][0]), ha='center', va='center', size=7)

    ax.autoscale_view()
    plt.axis('off')
    plt.ion()
    plt.show(block = False)
    plt.pause(0.001)

    # print("Time elapsed - Hex_plot_current_candi:", time.time()-t0)


########### MAIN STEPS ###########
## Set problem
Hex_Map = Hex_generate_map(SIZE_MAP)

# Place problem definition grid (single cell with pin)
# pin_hex = libhex.Hex(0, 0, 0)
# pin_hex = libhex.Hex(-1, 4, -3)
# pin_hex = libhex.Hex(1, 3, -4)
# pin_hex = libhex.Hex(2, 1, -3)
# pin_hex = libhex.Hex(2, 0, -2)
# pin_hex = libhex.Hex(-1, 0, 1) # Cannot find a solution ?!
# pin_hex = libhex.Hex(0, -3, 3)
# pin_hex = libhex.Hex(-3, 1, 2)
pin_hex = libhex.Hex(3, -3, 0)

# SPOILERS!!!
# Sol for pin_hex(0, 0, 0)
# Sol = [[0, 0, 3, 0, -3], [1, 0, -4, 2, 2], [2, 1, -1, 0, 1], [3, 1, 2, 2, -4], [4, 1, 1, 2, -3], [5, 0, 4, -3, -1], [6, 2, -2, 4, -2], [7, 1, 0, -3, 3], [8, 1, -1, -1, 2], [9, 2, 2, -3, 1], [10, 0, -3, 0, 3], [11, 1, -2, 3, -1]]
# Sol for pin_hex(-1, 4, -3)
# Sol = [[0, 0, 0, 3, -3], [1, 2, 2, -4, 2], [2, 0, -3, 1, 2], [3, 0, -4, 4, 0], [4, 1, 4, -1, -3], [5, 1, -3, -1, 4], [6, 1, 0, -1, 1], [7, 0, 2, -1, -1], [8, 1, 2, 2, -4], [9, 2, -2, 2, 0], [10, 1, -1, -2, 3], [11, 0, 1, -1, 0]]
# Sol for pin_hex(1, 3, -4)
# Sol = [[0, 0, -3, 2, 1], [1, 2, 1, -4, 3], [2, 0, 2, -3, 1], [3, 0, -4, 4, 0], [4, 1, 1, 1, -2], [5, 1, -3, -1, 4], [6, 0, 0, -1, 1], [7, 2, -1, 0, 1], [8, 0, 3, -3, 0], [9, 0, 3, 0, -3], [10, 0, -1, 3, -2], [11, 1, 2, 2, -4]]
# Sol for pin_hex(2, 1, -3)
# Sol = [[0, 0, -3, 2, 1], [1, 1, 3, 1, -4], [2, 0, 0, 1, -1], [3, 0, -4, 4, 0], [4, 2, 0, -4, 4], [5, 0, 4, -3, -1], [6, 0, -2, 0, 2], [7, 0, 0, -1, 1], [8, 0, -1, -2, 3], [9, 2, 2, -3, 1], [10, 0, -1, 3, -2], [11, 0, 1, 1, -2]]
# Sol for pin_hex(2, 0, -2)
# Sol = [[0, 2, -3, 0, 3], [1, 2, 3, -4, 1], [2, 1, 0, 3, -3], [3, 1, 3, 1, -4], [4, 2, 0, -4, 4], [5, 0, 4, -2, -2], [6, 2, 1, -1, 0], [7, 1, 0, -2, 2], [8, 2, 1, 0, -1], [9, 2, -4, 3, 1], [10, 0, -2, 3, -1], [11, 2, -1, 1, 0]]
# Sol for pin_hex(0, -3, 3)
# Sol = [[0, 0, -3, 2, 1], [1, 1, 3, 1, -4], [2, 2, -2, 0, 2], [3, 0, -4, 4, 0], [4, 2, 0, -4, 4], [5, 0, 0, 1, -1], [6, 0, 4, -2, -2], [7, 1, 3, -3, 0], [8, 0, 1, 1, -2], [9, 1, 1, -1, 0], [10, 0, -1, 3, -2], [11, 1, 0, -2, 2]]
# Sol for pin_hex(-3, 1, 2)
# Sol = [[0, 1, 0, -2, 2], [1, 2, 3, -4, 1], [2, 1, 1, -1, 0], [3, 0, -4, 2, 2], [4, 2, 0, -4, 4], [5, 0, 0, 1, -1], [6, 1, -2, -1, 3], [7, 2, -3, 3, 0], [8, 0, 3, -2, -1], [9, 0, 3, 1, -4], [10, 0, -1, 3, -2], [11, 0, 1, 1, -2]]
# Sol for pin_hex(3, -3, 0)
# Sol = [[0, 1, 2, 1, -3], [1, 0, -4, 1, 3], [2, 2, -1, 0, 1], [3, 1, 4, 0, -4], [4, 0, -4, 4, 0], [5, 0, 0, 2, -2], [6, 1, 1, -1, 0], [7, 2, -2, 2, 0], [8, 1, -2, -1, 3], [9, 1, 1, -4, 3], [10, 1, 3, -2, -1], [11, 1, 1, -2, 1]]


# Set pin hex in grid map to be occupied
found_match, val_set_success = Hex_find_and_set_grid_conditional(Hex_Map, pin_hex.q, pin_hex.r, pin_hex.s, 1)
Hex_Map_Original_Copy = Hex_Map.copy()
# print(Hex_Map)

# Generate puzzle pieces
Puzzle_pieces = hex_pieces.generate_all_pieces()

# Solver
# t0 = time.time()
Sol = Hex_verify_candi_with_level(Hex_Map_Original_Copy, Puzzle_pieces, [])

Hex_plot_current_candi(Hex_Map, pin_hex, Sol)
# print("Time elapsed:", time.time() - t0, "s")


## END OF CODE