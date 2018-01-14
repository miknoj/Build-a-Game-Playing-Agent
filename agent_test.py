"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally. The test
cases used by the project assistant are not public.
"""
import random
import timeit
import unittest

import isolation
import game_agent
import sample_players

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.time_millis = lambda: 1000 * timeit.default_timer()
        self.player1 = "Player1" # Will be changed in test cases.
        self.player2 = "Player2"

    def reset_board(self, player1, dimensions):
        self.game = isolation.Board(player1, self.player2,
                    width=dimensions[0], height=dimensions[1])
    
    def timed_execution(self, time_limit, closure):
        move_start = self.time_millis()
        time_left = lambda : time_limit - (self.time_millis() - move_start)
        # This assignment is done strictly to mirror the assignment code.
        self.player1.time_left = time_left
        result = closure()
        move_end = time_left()
        return move_end, result

    def dumb_score(self, game, player):
        result = game.utility(player)
        return result

    # def test_minimax(self):
    #     print("\n\n\nTest Minimax\n\n\n")
    #     # Test 1
    #     print("\n\n======================= Test 1 =============================\n")

    #     self.player1 = game_agent.MinimaxPlayer(score_fn=self.dumb_score)
        
    #     self.reset_board(self.player1, (3, 3))
    #     self.game.apply_move((2, 0))
    #     self.game.apply_move((0, 0))
    #     self.game.apply_move((0, 1))
    #     self.game.apply_move((1, 2))
    #     time_limit = isolation.isolation.TIME_LIMIT_MILLIS
    #     move_end, coords = self.timed_execution(time_limit, lambda: self.player1.minimax(self.game, 3))

    #     self.game.apply_move(coords)
        
    #     # Run assertions.
    #     self.assertTrue(self.game.is_winner(self.player1))
    #     self.assertEqual(coords,(2, 2))
    #     self.assertTrue(move_end < time_limit)

    #     # Test 2
    #     print("\n\n======================= Test 2 =============================\n")

    #     self.reset_board(self.player1, (3, 3))
    #     self.game.apply_move((0, 1))
    #     self.game.apply_move((1, 1))
    #     time_limit = time_limit = isolation.isolation.TIME_LIMIT_MILLIS
    #     move_end, coords = self.timed_execution(time_limit, lambda: self.player1.minimax(self.game, 3))
    #     self.game.apply_move(coords)
        
    #     # Run assertions.
    #     self.assertTrue(self.game.is_winner(self.player1))
    #     self.assertTrue(move_end < time_limit)

    #     # Test 3
    #     print("\n\n======================= Test 3 =============================\n")

    #     self.reset_board(self.player1, (5, 5))
    #     self.game.apply_move((0, 0))
    #     self.game.apply_move((2, 2))
    #     self.game.apply_move((2, 1))
    #     self.game.apply_move((1, 0))
    #     self.game.apply_move((3, 3))
    #     self.game.apply_move((3, 1))
    #     time_limit = 1000 * 2
    #     move_end, coords = self.timed_execution(time_limit, lambda: self.player1.minimax(self.game, 10))

    #     print(coords)
    #     # Run assertions.
    #     self.assertTrue(move_end < time_limit)

    # def test_alphabeta(self):
    #     print("\n\n\nTest Alpha Beta\n\n\n")

    #     # Test 1
    #     print("\n\n======================= Test 1 =============================\n")

    #     self.player1 = game_agent.AlphaBetaPlayer(score_fn=self.dumb_score)
        
    #     self.reset_board(self.player1, (3, 3))
    #     self.game.apply_move((2, 0))
    #     self.game.apply_move((0, 0))
    #     self.game.apply_move((0, 1))
    #     self.game.apply_move((1, 2))
    #     time_limit = isolation.isolation.TIME_LIMIT_MILLIS
    #     move_end, coords = self.timed_execution(time_limit, lambda: self.player1.alphabeta(self.game, 3))

    #     self.game.apply_move(coords)
        
    #     # Run assertions.
    #     self.assertTrue(self.game.is_winner(self.player1))
    #     self.assertEqual(coords,(2, 2))
    #     self.assertTrue(move_end < time_limit)

    #     # Test 2
    #     print("\n\n======================= Test 2 =============================\n")

    #     self.reset_board(self.player1, (3, 3))
    #     self.game.apply_move((0, 1))
    #     self.game.apply_move((1, 1))
    #     time_limit = time_limit = isolation.isolation.TIME_LIMIT_MILLIS
    #     move_end, coords = self.timed_execution(time_limit, lambda: self.player1.alphabeta(self.game, 3))
    #     self.game.apply_move(coords)
        
    #     # Run assertions.
    #     self.assertTrue(self.game.is_winner(self.player1))
    #     self.assertTrue(move_end < time_limit)

    #     # Test 3
    #     print("\n\n======================= Test 3 =============================\n")

    #     self.reset_board(self.player1, (5, 5))
    #     self.game.apply_move((0, 0))
    #     self.game.apply_move((2, 2))
    #     self.game.apply_move((2, 1))
    #     self.game.apply_move((1, 0))
    #     self.game.apply_move((3, 3))
    #     self.game.apply_move((3, 1))
    #     time_limit = 200
    #     move_end, coords = self.timed_execution(time_limit, lambda: self.player1.alphabeta(self.game, 10))

    #     print(coords)
    #     # Run assertions.
    #     self.assertTrue(move_end < time_limit)
    
    # def test_rounds(self):
    #     self.player1 = game_agent.AlphaBetaPlayer(score_fn=game_agent.custom_score)
    #     self.player2 = game_agent.AlphaBetaPlayer(score_fn=sample_players.improved_score)
    #     self.reset_board(self.player1, (7, 7))

    #     # players take turns moving on the board, so player1 should be next to move
    #     assert(self.player1 == self.game.active_player)
        
    #     for _ in range(2):
    #         move = random.choice(self.game.get_legal_moves())
    #         self.game.apply_move(move)
        
    #     winner, history, outcome = self.game.play()
        
    #     winner_str = "Player 1" if winner == self.player1 else "Player 2"
    #     print("\nWinner: {}\nOutcome: {}".format(winner_str, outcome))
    #     print(self.game.to_string())
    #     print("Percentage of blanks spaces left:", len(self.game.get_blank_spaces())/(self.game.width*self.game.height))
    #     print("Move history:\n{!s}".format(history))

    def test_performance(self):
        # control_group = {"Null Score" : sample_players.null_score, 
        #                 "Open Move Score" : sample_players.open_move_score,
        #                 "Improved Score" : sample_players.improved_score}
        control_group = {"Improved Score" : sample_players.improved_score}
        # test_group = {"custom_score": game_agent.custom_score,
        #             "custom_score_2": game_agent.custom_score_2,
        #             "custom_score_3": game_agent.custom_score_3}
        test_group = {"Custom Score": game_agent.custom_score}
        total = 10
        for j in range(1):
            scores = dict(zip(test_group,[[0]*len(control_group) for n in range(len(test_group))]))
            for round in range(total):
                for k in test_group:
                    for i, c in enumerate(control_group):
                        player1 = game_agent.AlphaBetaPlayer(score_fn=test_group[k])
                        player2 = game_agent.AlphaBetaPlayer(score_fn=control_group[c])
                        game = isolation.Board(player1, player2, 7, 7)
                        for _ in range(2):
                            move = random.choice(game.get_legal_moves())
                            game.apply_move(move)
                        winner, history, outcome = game.play()
                        winner_str = "Player 1" if winner == player1 else "Player 2"
                        print("Player 1:",k,"| Player 2:",c)
                        print("Winner: {}\nOutcome: {}".format(winner_str, outcome))
                        print("Percentage of blanks spaces left:", len(game.get_blank_spaces())/(game.width*game.height))
                        print("Move history:\n{!s}\n".format(history))
                        if winner == player1:
                            scores[k][i] += 1
            print(list(control_group))
            for k in scores:
                print("{0} | {1}".format(k, [x/total for x in scores[k]]))

if __name__ == '__main__':
    unittest.main()
