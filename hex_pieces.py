import numpy as np
import libhex

# Number of hex per Hex_Piece
NUM_OF_HEX_PER_PIECE = 5
NUM_OF_PIECES = 12


class Hex_Piece:
    def __init__(self, form_0, index): 
        if (len(form_0) != NUM_OF_HEX_PER_PIECE):
            print('Error: wrong input of hex piece definition (wrong number of hex)')
            return
        if str(type(form_0[0])) != "<class 'libhex.Hex'>":
            print('Error: wrong input of hex piece definition (not formed by hex)')
            return
        self.index = index
        self.form_0 = form_0
        self.form_1 = []
        self.form_2 = []
        self.Calculate_form_1_and_2_from_0()
        self.color = list(np.random.choice(range(256), size=3)/256.0)
          
    def Calculate_form_1_and_2_from_0(self):
        for hex in self.form_0:
            self.form_1.append(libhex.hex_rotate_left(libhex.hex_rotate_left(hex)))
            self.form_2.append(libhex.hex_rotate_right(libhex.hex_rotate_right(hex)))

    def form(self, form_idx):
        return getattr(self, 'form_' + str(form_idx))


def generate_all_pieces():
    Puzzle_pieces = []

    piece_0_form_0 = []
    piece_0_form_0.append(libhex.Hex(0,0,0))
    piece_0_form_0.append(libhex.Hex(1,0,-1))
    piece_0_form_0.append(libhex.Hex(0,1,-1))
    piece_0_form_0.append(libhex.Hex(0,-1,1))
    piece_0_form_0.append(libhex.Hex(-1,-1,2))
    Piece_0 = Hex_Piece(piece_0_form_0, 0)

    piece_1_form_0 = []
    piece_1_form_0.append(libhex.Hex(0,0,0))
    piece_1_form_0.append(libhex.Hex(0,1,-1))
    piece_1_form_0.append(libhex.Hex(1,0,-1))
    piece_1_form_0.append(libhex.Hex(2,0,-2))
    piece_1_form_0.append(libhex.Hex(0,-1,1))
    Piece_1 = Hex_Piece(piece_1_form_0, 1)

    piece_2_form_0 = []
    piece_2_form_0.append(libhex.Hex(0,0,0))
    piece_2_form_0.append(libhex.Hex(-1,0,1))
    piece_2_form_0.append(libhex.Hex(1,-1,0))
    piece_2_form_0.append(libhex.Hex(0,1,-1))
    piece_2_form_0.append(libhex.Hex(0,2,-2))
    Piece_2 = Hex_Piece(piece_2_form_0, 2)

    piece_3_form_0 = []
    piece_3_form_0.append(libhex.Hex(0,0,0))
    piece_3_form_0.append(libhex.Hex(1,0,-1))
    piece_3_form_0.append(libhex.Hex(2,0,-2))
    piece_3_form_0.append(libhex.Hex(0,-1,1))
    piece_3_form_0.append(libhex.Hex(0,-2,2))
    Piece_3 = Hex_Piece(piece_3_form_0, 3)

    piece_4_form_0 = []
    piece_4_form_0.append(libhex.Hex(0,0,0))
    piece_4_form_0.append(libhex.Hex(0,-1,1))
    piece_4_form_0.append(libhex.Hex(1,0,-1))
    piece_4_form_0.append(libhex.Hex(2,0,-2))
    piece_4_form_0.append(libhex.Hex(3,0,-3))
    Piece_4 = Hex_Piece(piece_4_form_0, 4)

    piece_5_form_0 = []
    piece_5_form_0.append(libhex.Hex(0,0,0))
    piece_5_form_0.append(libhex.Hex(-1,0,1))
    piece_5_form_0.append(libhex.Hex(0,-1,1))
    piece_5_form_0.append(libhex.Hex(0,1,-1))
    piece_5_form_0.append(libhex.Hex(0,2,-2))
    Piece_5 = Hex_Piece(piece_5_form_0, 5)

    piece_6_form_0 = []
    piece_6_form_0.append(libhex.Hex(0,0,0))
    piece_6_form_0.append(libhex.Hex(0,1,-1))
    piece_6_form_0.append(libhex.Hex(0,-1,1))
    piece_6_form_0.append(libhex.Hex(-1,0,1))
    piece_6_form_0.append(libhex.Hex(-2,0,2))
    Piece_6 = Hex_Piece(piece_6_form_0, 6)

    piece_7_form_0 = []
    piece_7_form_0.append(libhex.Hex(0,0,0))
    piece_7_form_0.append(libhex.Hex(0,1,-1))
    piece_7_form_0.append(libhex.Hex(1,0,-1))
    piece_7_form_0.append(libhex.Hex(1,-1,0))
    piece_7_form_0.append(libhex.Hex(1,-2,1))
    Piece_7 = Hex_Piece(piece_7_form_0, 7)

    piece_8_form_0 = []
    piece_8_form_0.append(libhex.Hex(0,0,0))
    piece_8_form_0.append(libhex.Hex(0,1,-1))
    piece_8_form_0.append(libhex.Hex(0,2,-2))
    piece_8_form_0.append(libhex.Hex(1,0,-1))
    piece_8_form_0.append(libhex.Hex(1,-1,0))
    Piece_8 = Hex_Piece(piece_8_form_0, 8)

    piece_9_form_0 = []
    piece_9_form_0.append(libhex.Hex(0,0,0))
    piece_9_form_0.append(libhex.Hex(-1,1,0))
    piece_9_form_0.append(libhex.Hex(-1,0,1))
    piece_9_form_0.append(libhex.Hex(1,-1,0))
    piece_9_form_0.append(libhex.Hex(1,-2,1))
    Piece_9 = Hex_Piece(piece_9_form_0, 9)

    piece_10_form_0 = []
    piece_10_form_0.append(libhex.Hex(0,0,0))
    piece_10_form_0.append(libhex.Hex(-1,0,1))
    piece_10_form_0.append(libhex.Hex(0,-1,1))
    piece_10_form_0.append(libhex.Hex(0,1,-1))
    piece_10_form_0.append(libhex.Hex(1,1,-2))
    Piece_10 = Hex_Piece(piece_10_form_0, 10)

    piece_11_form_0 = []
    piece_11_form_0.append(libhex.Hex(0,0,0))
    piece_11_form_0.append(libhex.Hex(0,1,-1))
    piece_11_form_0.append(libhex.Hex(0,2,-2))
    piece_11_form_0.append(libhex.Hex(1,-1,0))
    piece_11_form_0.append(libhex.Hex(1,-2,1))
    Piece_11 = Hex_Piece(piece_11_form_0, 11)

    Puzzle_pieces.append(Piece_0)
    Puzzle_pieces.append(Piece_1)
    Puzzle_pieces.append(Piece_2)
    Puzzle_pieces.append(Piece_3)
    Puzzle_pieces.append(Piece_4)
    Puzzle_pieces.append(Piece_5)
    Puzzle_pieces.append(Piece_6)
    Puzzle_pieces.append(Piece_7)
    Puzzle_pieces.append(Piece_8)
    Puzzle_pieces.append(Piece_9)
    Puzzle_pieces.append(Piece_10)
    Puzzle_pieces.append(Piece_11)

    return Puzzle_pieces