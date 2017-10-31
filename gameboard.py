# defines a three-by-three tic-tac-toe board as a one-dimensional array
class GameBoard(object):
    def __init__(self, gamepieces):
        """
        self.WIN_COMBOS: gives the horizontal, vertical, and diagonal three-in-a-rows that will win the game
        self.board: starts as an array of ints 0 through 8 and gets filled with gamepieces ('x', 'o') over the game
        self.gamepieces: array len 2 - first player's gamepiece, then second player's
        """

        self.WIN_COMBOS = [{0, 1, 2},
                           {3, 4, 5},
                           {6, 7, 8},
                           {0, 4, 8},
                           {2, 4, 6},
                           {0, 3, 6},
                           {1, 4, 7},
                           {2, 5, 8}]
        self.board = range(9)
        self.gamepieces = gamepieces

    def reset(self):
        """clear out the board at the start of a new game"""
        self.board = range(9)

    @property
    def choices(self):
        """list of remaining free spaces on the board"""
        return [x for x in self.board if x in range(9)]

    @property
    def potential_wins(self):
        """list of the sets from self.WIN_COMBOS that could still potentially be won by either opponent
        (i.e. one or both of the players has yet to occupy a space in that combo)"""
        result = []
        for combo in self.WIN_COMBOS:
            b = [self.board[i] for i in combo]
            if self.gamepieces[0] not in b or self.gamepieces[1] not in b:
                result.append(combo)

        return result

    def __str__(self):
        """pretty-print the board"""

        b = self.board

        s = '\n  {}  |  {}  |  {}  '.format(b[0], b[1], b[2])
        s += '\n-----|-----|-----\n'
        s += '  {}  |  {}  |  {}  '.format(b[3], b[4], b[5])
        s += '\n-----|-----|-----\n'
        s += '  {}  |  {}  |  {}  \n'.format(b[6], b[7], b[8])

        return s