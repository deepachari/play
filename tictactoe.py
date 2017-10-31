# simple tic-tac-toe game
import player


class GameBoard(object):
    def __init__(self):
        self.WIN_COMBOS = [{0, 1, 2},
                           {3, 4, 5},
                           {6, 7, 8},
                           {0, 4, 8},
                           {2, 4, 6},
                           {0, 3, 6},
                           {1, 4, 7},
                           {2, 5, 8}]
        self.board = range(9)

    def clear(self):
        self.board = range(9)

    @property
    def choices(self):
        return [x for x in self.board if x in range(9)]

    def __str__(self):

        b = self.board

        s = '\n'

        s += '  {}  |  {}  |  {}  '.format(b[0], b[1], b[2])
        s += '\n-----|-----|-----\n'
        s += '  {}  |  {}  |  {}  '.format(b[3], b[4], b[5])
        s += '\n-----|-----|-----\n'
        s += '  {}  |  {}  |  {}  '.format(b[6], b[7], b[8])

        s += '\n'

        return s


class Game(object):

    def __init__(self, player1, player2, pretty=False):

        self.board = GameBoard()

        self.player1 = player1
        self.player2 = player2
        self.pretty = pretty

        if (isinstance(player1, player.HumanPlayer) or isinstance(player2, player.HumanPlayer)) \
                and not pretty:
            raise Exception("ERROR: Invalid setup - one or more of the players is interactive, but we can't see the " \
                            "board!")

        if player1.gamepiece == player2.gamepiece:
            raise Exception("ERROR: Two players with the same gamepiece can't play.")

    def play(self):

        self.board.clear()

        if self.pretty:
            print 'Starting a new game! In one corner: {}. In the other: {}. BEGIN!'.format(self.player1.name,
                                                                                            self.player2.name)
            print str(self.board)

        # take turns making a move
        current_player = other_player = None
        while self.board.choices and not self.player1.has_won(self.board) and not self.player2.has_won(self.board):

            # switch the current player
            if not current_player or not other_player:
                current_player = self.player1
                other_player = self.player2
            else:
                temp = current_player
                current_player = other_player
                other_player = temp

            move = current_player.next_move(board=self.board)
            self.board.board[move] = current_player.gamepiece

            if self.pretty:
                print str(self.board)
                print "{} played {}".format(current_player.name, move)

        # find out who won
        if self.player1.has_won(self.board):
            winner = self.player1.name
        elif self.player2.has_won(self.board):
            winner = self.player2.name
        elif not self.board.choices:
            winner = None
        else:
            raise Exception("ERROR: Can't retrieve the winner")

        if self.pretty:
            if winner:
                print "\n{} won!!!".format(winner)
            else:
                print "\nIt's a draw, pardner"

        return winner


class Simulator(object):

    def __init__(self, game, num_iterations):

        self.game = game
        self.num_iterations = num_iterations
        self.num_player1_wins = None
        self.num_player2_wins = None
        self.draws = None

        if isinstance(game.player1, player.HumanPlayer) or isinstance(game.player2, player.HumanPlayer):
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
player1 = player.SmartAutoPlayer(gamepiece='A', name='Smart')
player2 = player.RandomAutoPlayer(gamepiece='B', name='Dumb')
#
# Game(player1=player1, player2=player2, pretty=True).play()
mygame = Game(player1=player1, player2=player2)

sim = Simulator(mygame, 10000)
sim.simulate()
sim.print_result()
