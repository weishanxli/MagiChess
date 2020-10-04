# Weishan Li
# Jack DeGuglielmo
# September 2020
# Description: GameState class for storing the local state of the chess board

from collections import OrderedDict
from chessPiece import ChessPiece

class GameState:
    def __init__(self):
        self.localPlayerColor = ''
        self.board = OrderedDict([('a1', None), ('b1', None), ('c1', None), ('d1', None), ('e1', None), ('f1', None), ('g1', None), ('h1', None), \
                ('a2', None), ('b2', None), ('c2', None), ('d2', None), ('e2', None), ('f2', None), ('g2', None), ('h2', None), \
                ('a3', None), ('b3', None), ('c3', None), ('d3', None), ('e3', None), ('f3', None), ('g3', None), ('h3', None), \
                ('a4', None), ('b4', None), ('c4', None), ('d4', None), ('e4', None), ('f4', None), ('g4', None), ('h4', None), \
                ('a5', None), ('b5', None), ('c5', None), ('d5', None), ('e5', None), ('f5', None), ('g5', None), ('h5', None), \
                ('a6', None), ('b6', None), ('c6', None), ('d6', None), ('e6', None), ('f6', None), ('g6', None), ('h6', None), \
                ('a7', None), ('b7', None), ('c7', None), ('d7', None), ('e7', None), ('f7', None), ('g7', None), ('h7', None), \
                ('a8', None), ('b8', None), ('c8', None), ('d8', None), ('e8', None), ('f8', None), ('g8', None), ('h8', None)])

    def setCell(self, piece, cell):
        self.board[cell] = piece

    def reset(self):


        # K
        self.setCell(ChessPiece('K', 'w'), 'e1')
        self.setCell(ChessPiece('k', 'b'), 'e8')

        # q
        self.setCell(ChessPiece('Q', 'w'), 'd1')
        self.setCell(ChessPiece('q', 'b'), 'd8')

        # b
        bBishopCells = ['c8', 'f8']
        self.setCell(ChessPiece('b', 'b'), bBishopCells[0])
        self.setCell(ChessPiece('b', 'b'), bBishopCells[1])

        wBishopCells = ['c1', 'f1']
        self.setCell(ChessPiece('B', 'w'), wBishopCells[0])
        self.setCell(ChessPiece('B', 'w'), wBishopCells[1])

        # k
        bKnightCells = ['b8', 'g8']
        self.setCell(ChessPiece('h', 'b'), bKnightCells[0])
        self.setCell(ChessPiece('h', 'b'), bKnightCells[1])

        wKnightCells = ['b1', 'g1']
        self.setCell(ChessPiece('H', 'w'), wKnightCells[0])
        self.setCell(ChessPiece('H', 'w'), wKnightCells[1])

        # r
        bRookCells = ['a8', 'h8']
        self.setCell(ChessPiece('r', 'b'), bRookCells[0])
        self.setCell(ChessPiece('r', 'b'), bRookCells[1])

        wRookCells = ['a1', 'h1']
        self.setCell(ChessPiece('R', 'w'), wRookCells[0])
        self.setCell(ChessPiece('R', 'w'), wRookCells[1])

        # p
        bPonsCells = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
        for item in bPonsCells:
            self.setCell(ChessPiece('p', 'b'), item)

        wPonsCells = ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        for item in wPonsCells:
            self.setCell(ChessPiece('P', 'w'), item)

    def __str__(self):
        newlineCounter = 0
        out = ""

        printBoardKeys = self.board.keys()
        if self.localPlayerColor == 'w':
            printBoardKeys = reversed(self.board.keys())
        for item in printBoardKeys:
            if newlineCounter % 8 == 0:
                out += '\n'
            if self.board.get(item) is not None:
                out += (self.board[item].type + '\t')
            else:
                out += (u'\u4e00' + '\t')
            # print(item, '\t', end='')
            newlineCounter += 1
        return out

test = GameState()
test.localPlayerColor = 'b'  # remove this, must be set based on server state
test.reset()
print(test)     # print will call __str()__