# simple tic-tac-toe game
import random

class Person(object):
    def __init__(self, is_smart):
        self.is_smart = is_smart



class Player(object):

    def __init__(self, smart_computer, smart_player):

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

        self.smart_computer = smart_computer
        self.smart_player = smart_player

    # region Properties

    @property
    def player_moves(self):
        return set([index for index, place in enumerate(self.tictac) if place == 'x '])

    @property
    def my_moves(self):
        return set([index for index, place in enumerate(self.tictac) if place == 'o '])

    @property
    def choices(self):
        return [index for index, place in enumerate(self.tictac) if place not in ('x ', 'o ')]

    # endregion

    # region Player Mechanics

    # takes a set of moves
    def get_move(self, is_smart):
        if not is_smart:
            return random.choice(self.choices)

        my_move = self.winning_move(self.my_moves)
        if my_move is None:
            my_move = self.winning_move(self.player_moves)
        if my_move is None:
            my_move = random.choice(self.choices)

        return my_move

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

    def get_player_move(self):
        return self.get_move(self.smart_player)

    def play(self):
        while self.choices and not self.won(self.player_moves) and not self.won(self.my_moves):
            self.pretty_print()

            player_move = self.get_player_move()
            self.tictac[player_move] = 'x '

            if self.choices:
                my_move = self.get_move(self.smart_computer)
                self.tictac[my_move] = 'o '

        self.pretty_print()
        return self.get_result()

    def get_result(self):
        if self.won(self.player_moves):
            return 'player'
        elif self.won(self.my_moves):
            return 'computer'
        elif not self.choices:
            return 'draw'
        else:
            raise Exception

    # endregion

    def pretty_print(self):
        pass


class InteractivePlayer(Player):

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

    def play(self):
        result = super(InteractivePlayer, self).play()
        if result == 'player':
            print "You won!!"
        elif result == 'computer':
            print "YOINKS! I WON!"
        else:
            print "It's a draw!"

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


def simulate(n):
    p = Player(smart_computer=False, smart_player=False)
    num_plays = 0
    computer_wins = 0
    player_wins = 0
    draws = 0
    for i in range(n):
        result = p.play()
        if result == 'computer':
            computer_wins += 1
        elif result == 'player':
            player_wins += 1
        elif result == 'draw':
            draws += 1
        else:
            raise Exception
        num_plays += 1
    print '{} games played. ' \
          '{} computer wins ({} percent). ' \
          '{} player wins ({} percent). '\
          '{} draws ({} percent).'\
        .format(num_plays,
                computer_wins, computer_wins * 100.0 / num_plays,
                player_wins, player_wins * 100.0 / num_plays,
                draws, draws * 100.0 / num_plays)


InteractivePlayer(smart_computer=True, smart_player=False).play()