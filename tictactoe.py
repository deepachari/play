# simple tic-tac-toe game
import player
from gameboard import GameBoard


# given two players, play a game of tic-tac-toe
class Game(object):

    def __init__(self, player1, player2, pretty=False):
        """
        :param player1: Player object; represents the player who will go first
        :param player2: Player object; represents the player who will go second
        :param pretty: Bool indicating whether to print friendly messages + the board after each turn
        """

        self.board = GameBoard([player1.gamepiece, player2.gamepiece])

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
        """:returns: the name of the player who won, or None in case of a draw"""

        self.board.reset()

        if self.pretty:
            print 'Starting a new game! In one corner: {}. In the other: {}. BEGIN!'.format(self.player1.name,
                                                                                            self.player2.name)
            print str(self.board)

        # take turns making a move
        current_player = other_player = None
        while not self.player1.has_won(self.board) \
                and not self.player2.has_won(self.board) \
                and self.board.potential_wins:

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
        elif not self.board.potential_wins:
            winner = None
        else:
            raise Exception("ERROR: Can't retrieve the winner")

        if self.pretty:
            if winner:
                print "\n{} won!!!".format(winner)
            else:
                print "\nIt's a draw, pardner"

        return winner


# run several games of tic-tac-toe in a row and print statistics
class Simulator(object):

    def __init__(self, game, num_iterations):
        """
        :param game: Game object to simulate; can be given two players of varying intelligence
        :param num_iterations: total number of times to play
        """

        self.game = game
        self.num_iterations = num_iterations
        self.num_player1_wins = None
        self.num_player2_wins = None
        self.draws = None

        if isinstance(game.player1, player.HumanPlayer) or isinstance(game.player2, player.HumanPlayer):
            raise Exception("ERROR: Can't simulate with a non-automatic player!")

    def run(self):
        """:returns: array [num player1 wins, num player2 wins, num draws]"""

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
player1 = player.HumanPlayer(gamepiece='A', name='Player1')
player2 = player.CleverPlayer(gamepiece='B', name='Player2')

Game(player1=player1, player2=player2, pretty=True).play()
# mygame = Game(player1=player1, player2=player2)

# sim = Simulator(mygame, 10000)
# sim.simulate()
# sim.print_result()
