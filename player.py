# All the player-specific logic
import random
from collections import defaultdict

# this file references GameBoard throughout because players need game info to make decisions
# bit messy but couldn't think of a better way


# base class for players; should not be instantiated
class Player(object):

    def __init__(self, gamepiece=None, name=None):
        """
        :param gamepiece: single-character string; this player's board marker (e.g. 'x', 'o')
        :param name: string
        """
        self.gamepiece = gamepiece
        self.name = name

    def my_moves(self, board):
        """:returns: list of ints - this player's past moves on this board"""
        return set([index for index, place in enumerate(board.board) if place == self.gamepiece])

    def their_moves(self, board):
        """:returns: list of ints - this player's opponent's past moves on this board"""
        return set([index for index, place in enumerate(board.board) if place != self.gamepiece and place != index])
    
    def has_won(self, board):
        """:returns: Bool; true if this player has marked three in a row"""
        for combo in board.WIN_COMBOS:
            if combo.issubset(self.my_moves(board)):
                return True
        return False

    @staticmethod
    def next_winning_move(moves, board):
        """given a set of moves, if there are two in a row waiting for a third, returns the third
        :param moves: list of ints; either my_moves or their_moves
        :param board: GameBoard"""
        for combo in board.WIN_COMBOS:
            if len(combo.intersection(moves)) == 2:
                blocker = combo.difference(moves).pop()
                if blocker in board.choices:
                    return blocker
        return None

    @staticmethod
    def ranked_potential_wins(board):
        """
        :param board: GameBoard
        :returns: sorted list of tuples ranking the open spaces on the board by their desirability
            key: int representing one of the open cells on the board.
            value: number of winning combos that cell is part of, which could still potentially be won by either opponent
        """

        ranking = defaultdict(int)

        for p_win in board.potential_wins:
            for cell in p_win:
                if cell in board.choices:
                    ranking[cell] += 1

        return sorted(ranking, key=ranking.get, reverse=True)


# Interactive player class; prompts user for input
class HumanPlayer(Player):
    def __init__(self, name=None, gamepiece=None):

        super(HumanPlayer, self).__init__(name=name, gamepiece=gamepiece)

        if not self.name:
            self.name = raw_input('Enter your name: ')
        print 'Hi {}!'.format(self.name)
        while not self.gamepiece or len(self.gamepiece) > 1 or isinstance(self.gamepiece, int):
            self.gamepiece = raw_input('Enter your gamepiece (**one character only**): ')

    def next_move(self, board):
        """based on the current state of the gameboard, return an int representing the next move
                comes from user input"""
        move = raw_input('\n{}, make a move (0, 1, etc) '.format(self.name))

        while True:
            try:
                x = int(move)
            except ValueError:
                x = None

            if x is not None and board.board[x] == x:
                return x
            else:
                move = raw_input('That option isn\'t on the board... :( try again')


# base class for automatic (non-interactive) players, just so we can override Player.__init__()
# should not be instantiated
class AutoPlayer(Player):
    def __init__(self, gamepiece, name=None):
        super(AutoPlayer, self).__init__(gamepiece=gamepiece, name=name)

        # randomly generate a name if it isn't provided
        if not self.name:
            self.name = 'Player' + str(random.randint(100, 1000))

        if len(self.gamepiece) > 1:
            raise Exception("ERROR: Invalid gamepiece (one character only)")


# dumbest player
class RandomPlayer(Player):

    def next_move(self, board):
        """based on the current state of the gameboard, return an int representing the next move
                randomly plays any available position on the board"""
        return random.choice(board.choices)


# medium-smart
class SmartPlayer(Player):

    def next_move(self, board):
        """based on the current state of the gameboard, return an int representing the next move
                will choose the third in a line of three if the win is waiting
                and will block the opponent if they are about to win"""
        my_moves = self.my_moves(board)
        their_moves = self.their_moves(board)

        # prioritize making my own winning move
        next_move = Player.next_winning_move(my_moves, board)
        if next_move is None:
            # if the other player is about to win, block them
            next_move = Player.next_winning_move(their_moves, board)
        if next_move is None:
            # default to random
            next_move = random.choice(board.choices)

        return next_move


# still not perfect, but cleverer than SmartPlayer
class CleverPlayer(Player):
    def next_move(self, board):
        """based on the current state of the gameboard, return an int representing the next move
                same logic as SmartPlayer except instead of resorting to random choice at the end, pick the cell in
                line for the most potential wins (either yours or your opponent's)"""

        my_moves = self.my_moves(board)
        their_moves = self.their_moves(board)

        next_move = Player.next_winning_move(my_moves, board)
        if next_move:
            return next_move
        next_move = Player.next_winning_move(their_moves, board)
        if next_move:
            return next_move

        return Player.ranked_potential_wins(board)[0]
