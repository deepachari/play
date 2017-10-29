# simple tic-tac-toe game
import random


class UserPlayer(object):
    def __init__(self, name=None, gamepiece=None):

        self.gamepiece = gamepiece
        self.name = name

        if not name:
            self.name = raw_input('Enter your name: ')
        print 'Hi {}!'.format(self.name)
        while not self.gamepiece or len(self.gamepiece) > 1:
            self.gamepiece = raw_input('Enter your gamepiece (**one character only**): ')

        self.gamepiece += ' '  # for board alignment


class AutoPlayer(object):
    def __init__(self, gamepiece, is_smart, name=None):

        if len(gamepiece) > 1:
            raise Exception("ERROR: Invalid gamepiece (one character only)")

        self.gamepiece = gamepiece + ' '  # for board alignment
        self.name = name
        self.is_smart = is_smart

        if not name:
            self.name = 'Player' + str(random.randint(100, 1000))


class Game(object):

    def __init__(self, player1, player2, pretty):

        self.clear_board()

        self.winning_combos = [{0, 1, 2},
                               {3, 4, 5},
                               {6, 7, 8},
                               {0, 4, 8},
                               {2, 4, 6},
                               {0, 3, 6},
                               {1, 4, 7},
                               {2, 5, 8}]

        self.player1 = player1
        self.player2 = player2
        self.pretty = pretty

        if (isinstance(player1, UserPlayer) or isinstance(player2, UserPlayer)) and not pretty:
            raise Exception("ERROR: Invalid setup - one or more of the players is interactive, but we can't see the " \
                            "board!")

        if player1.gamepiece == player2.gamepiece:
            raise Exception("ERROR: Two players with the same gamepiece can't play.")

    # region Game Board

    @property
    def choices(self):
        return [index for index, place in enumerate(self.board) if place not in (self.player1.gamepiece,
                                                                                 self.player2.gamepiece)]

    def clear_board(self):
        self.board = ['a1', 'a2', 'a3',
                      'b1', 'b2', 'b3',
                      'c1', 'c2', 'c3']

    # endregion

    # region Player-Specific Info

    def past_moves(self, player):
        return set([index for index, place in enumerate(self.board) if place == player.gamepiece])

    def next_move(self, current_player, other_player):

        if isinstance(current_player, UserPlayer):
            return self.get_user_input(current_player.name)

        if not current_player.is_smart:
            return random.choice(self.choices)

        # prioritize making my own winning move
        next_move = self.next_winning_move(current_player)
        if next_move is None:
            # if the other player is about to win, block them
            next_move = self.next_winning_move(other_player)
        if next_move is None:
            # default to random
            next_move = random.choice(self.choices)

        return next_move

    def next_winning_move(self, player):  # helper to get_next_move
        moves = self.past_moves(player)
        for combo in self.winning_combos:
            if len(combo.intersection(moves)) == 2:
                blocker = combo.difference(moves).pop()
                if blocker in self.choices:
                    return blocker
        return None

    def get_user_input(self, name):
        move = raw_input('\n{}, make a move (a1, b2, etc) '.format(name))
        i = None

        while i is None:
            try:
                i = self.board.index(move)
            except ValueError:
                i = None

            if i not in self.choices:
                i = None

            if i is None:
                move = raw_input('That option isn\'t on the board... :( try again')

        return i

    def has_won(self, player):

        for combo in self.winning_combos:
            if combo.issubset(self.past_moves(player)):
                return True
        return False

    # endregion

    # region Play Mechanics

    def play(self):

        self.clear_board()

        if self.pretty:
            print 'Starting a new game! In one corner: {}. In the other: {}. BEGIN!'.format(self.player1.name,
                                                                                            self.player2.name)
            print self.pretty_board()

        current_player = other_player = None
        while self.choices and not self.has_won(self.player1) and not self.has_won(self.player2):

            if not current_player or not other_player:
                current_player = self.player1
                other_player = self.player2
            else:
                temp = current_player
                current_player = other_player
                other_player = temp

            move = self.next_move(current_player=current_player, other_player=other_player)
            position = self.board[move]
            self.board[move] = current_player.gamepiece

            if self.pretty:
                print self.pretty_board()
                print "{} played {}".format(current_player.name, position)

        # find out who won
        if self.has_won(self.player1):
            winner = self.player1.name
        elif self.has_won(self.player2):
            winner = self.player2.name
        elif not self.choices:
            winner = None
        else:
            raise Exception("ERROR: Can't retrieve the winner")

        if self.pretty:
            if winner:
                print "\n{} won!!!".format(winner)
            else:
                print "\nIt's a draw, pardner"

        return winner

    def pretty_board(self):

        s = '\n'
        for i, x in enumerate(self.board):
            s += ' {} '.format(self.board[i])
            if i not in (2, 5, 8):
                s += '|'
            if i in (2, 5):
                s += '\n----|----|----\n'
        s += '\n'

        return s

    # endregion

    pass  # so region above will fold


class Simulator(object):

    def __init__(self, game, num_iterations):

        self.game = game
        self.num_iterations = num_iterations
        self.num_player1_wins = None
        self.num_player2_wins = None
        self.draws = None

        if not isinstance(game.player1, AutoPlayer) or not isinstance(game.player2, AutoPlayer):
            raise Exception("ERROR: Can't simulate with a non-automatic player!")

    # returns array: [num player1 wins, num player2 wins, num draws]
    def simulate(self):

        self.num_player1_wins = self.num_player2_wins = self.draws = 0
        printed = []

        for i in range(self.num_iterations):
            winner = self.game.play()

            if not winner:
                self.draws += 1
            elif winner == self.game.player1.name:
                self.num_player1_wins += 1
            elif winner == self.game.player2.name:
                self.num_player2_wins += 1
            else:
                raise Exception("ERROR: Unexpected winner received from Game.play()")

            # counter
            percent_done = int(i * 100.0 / self.num_iterations)
            if percent_done % 5 == 0 and percent_done not in printed:
                print '...{}%'.format(percent_done)
            printed.append(percent_done)

        return

    def print_result(self):

        player1_percent = self.num_player1_wins * 100.0 / self.num_iterations
        player2_percent = self.num_player2_wins * 100.0 / self.num_iterations
        draw_percent = self.draws * 100.0 / self.num_iterations

        print "{} won {} games ({} percent). \n" \
              "{} won {} games ({} percent). \n" \
              "Players drew {} games ({} percent)."\
            .format(self.game.player1.name, self.num_player1_wins, player1_percent,
                    self.game.player2.name, self.num_player2_wins, player2_percent,
                    self.draws, draw_percent)


# player1 = UserPlayer(gamepiece='x', name='Steve')
player1 = AutoPlayer(gamepiece='x', is_smart=True, name='Smart1')
player2 = AutoPlayer(gamepiece='o', is_smart=True, name='Smart2')

# Game(player1=player1, player2=player2, pretty=True).play()
mygame = Game(player1=player1, player2=player2, pretty=False)

sim = Simulator(mygame, 50000)
sim.simulate()
sim.print_result()
