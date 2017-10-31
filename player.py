# All the player-specific logic
from abc import abstractmethod, ABCMeta
import random


class Player(object):
    def __init__(self, name=None, gamepiece=None):
        self.gamepiece = gamepiece
        self.name = name

    def past_moves(self, board):
        return set([index for index, place in enumerate(board.board) if place == self.gamepiece])

    def other_player_moves(self, board):
        return set([index for index, place in enumerate(board.board) if place != self.gamepiece and place != index])
    
    def has_won(self, board):

        for combo in board.WIN_COMBOS:
            if combo.issubset(self.past_moves(board)):
                return True
        return False


class HumanPlayer(Player):
    def __init__(self, name=None, gamepiece=None):

        super(HumanPlayer, self).__init__(name=name, gamepiece=gamepiece)

        if not self.name:
            self.name = raw_input('Enter your name: ')
        print 'Hi {}!'.format(self.name)
        while not self.gamepiece or len(self.gamepiece) > 1 or not isinstance(self.gamepiece, int):
            self.gamepiece = raw_input('Enter your gamepiece (**one character only**): ')

    def next_move(self, board):
        move = raw_input('\n{}, make a move (0, 1, etc) '.format(self.name))

        while True:
            try:
                x = int(move)
            except ValueError:
                x = None

            if x and board.board[x] == x:
                return x
            else:
                move = raw_input('That option isn\'t on the board... :( try again')


class RandomAutoPlayer(Player):
    def __init__(self, gamepiece, name=None):

        super(RandomAutoPlayer, self).__init__(name=name, gamepiece=gamepiece)

        if not self.name:
            self.name = 'Player' + str(random.randint(100, 1000))

        if len(self.gamepiece) > 1:
            raise Exception("ERROR: Invalid gamepiece (one character only)")

    def next_move(self, board):
        return random.choice(board.choices)


class SmartAutoPlayer(Player):

    def __init__(self, gamepiece, name=None):

        super(SmartAutoPlayer, self).__init__(name=name, gamepiece=gamepiece)

        if not self.name:
            self.name = 'Player' + str(random.randint(100, 1000))

        if len(self.gamepiece) > 1:
            raise Exception("ERROR: Invalid gamepiece (one character only)")

    def next_move(self, board):
        my_moves = self.past_moves(board)
        their_moves = self.other_player_moves(board)

        # prioritize making my own winning move
        next_move = self.next_winning_move(my_moves, board)
        if next_move is None:
            # if the other player is about to win, block them
            next_move = self.next_winning_move(their_moves, board)
        if next_move is None:
            # default to random
            next_move = random.choice(board.choices)

        return next_move
    
    def next_winning_move(self, moves, board):  # helper to get_next_move
        for combo in board.WIN_COMBOS:
            if len(combo.intersection(moves)) == 2:
                blocker = combo.difference(moves).pop()
                if blocker in board.choices:
                    return blocker
        return None


class PerfectAutoPlayer(Player):
    pass

