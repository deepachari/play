# simple tic-tac-toe game
import random


class Player(object):

    def __init__(self):

        self.tictac = ['a1', 'a2', 'a3',
                       'b1', 'b2', 'b3',
                       'c1', 'c2', 'c3']

        self.winning_combos = [{0, 1, 2},
                               {3, 4, 5},
                               {6, 7, 8},
                               {0, 4, 8},
                               {2, 4, 6},
                               {0, 3, 6},
                               {1, 4, 7},
                               {2, 5, 8}]

    @property
    def player_moves(self):
        return set([index for index, place in enumerate(self.tictac) if place == 'x '])

    @property
    def my_moves(self):
        return set([index for index, place in enumerate(self.tictac) if place == 'o '])

    @property
    def choices(self):
        return [index for index, place in enumerate(self.tictac) if place not in ('x ', 'o ')]

    def pretty_print(self):

        s = ''
        for i, x in enumerate(self.tictac):
            s += ' {} '.format(self.tictac[i])
            if i not in (2, 5, 8):
                s += '|'
            if i in (2, 5):
                s += '\n----|----|----\n'
        print s
        print '\n'

    # takes a set of moves
    def won(self, m):

        for combo in self.winning_combos:
            if combo.issubset(m):
                return True
        return False

    def winning_move(self, m):
        for combo in self.winning_combos:
            if len(combo.intersection(m)) == 2:
                blocker = combo.difference(m).pop()
                if blocker in self.choices:
                    return blocker
        return None

    def make_my_move(self):
        my_move = self.winning_move(self.my_moves)
        if my_move is None:
            my_move = self.winning_move(self.player_moves)
        if my_move is None:
            my_move = random.choice(self.choices)

        return my_move

    def play(self):
        while self.choices and not self.won(self.player_moves) and not self.won(self.my_moves):
            self.pretty_print()

            player_move = self.get_player_move()
            self.tictac[player_move] = 'x '

            if self.choices:
                my_move = self.make_my_move()
                self.tictac[my_move] = 'o '

        self.print_result()

    def get_player_move(self):
        return random.choice(self.choices)

    def print_result(self):
        self.pretty_print()
        if self.won(self.player_moves):
            print 'You won!!!'
        elif self.won(self.my_moves):
            print 'YEEEAH I WON SUCKA'
        elif not self.choices:
            print 'It\'s a draw, pardner'
        else:
            print 'Game still ongoing'


class InteractivePlayer(Player):

    def play(self):
        super(InteractivePlayer, self).play()



    def get_player_move(self):
        move = raw_input('Make a move! (a1, b2, etc)')
        i = None

        while i is None:
            try:
                i = self.tictac.index(move)
            except ValueError:
                i = None

            if i not in self.choices:
                i = None

            if i is None:
                move = raw_input('That option isn\'t on the board... :( try again')

        return i


class RandomPlayer(Player):
    def make_my_move(self):
        return random.choice(self.choices)


class Person:
    def __init__(self):
        self.name = ''


InteractivePlayer().play()