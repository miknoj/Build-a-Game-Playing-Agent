"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import math
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def get_Lmoves(game, position):
    # Taken straight from isolation. This is why source access is great :)
    y, x = position
    l_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                      (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(y + dy, x + dx) for dy, dx in l_moves
                    if game.move_is_legal((y + dy, x + dx))]
    return valid_moves

def get_tree2(pos, blanks, game):
    curr = []
    moves = get_Lmoves(game, pos)
    for mv in moves:
        if mv in blanks:
            curr = [pos] + get_tree2(mv, [x for x in blanks if x != mv], game)
    return curr

def get_tree(game, player):
    tree = []
    blanks = game.get_blank_spaces()
    for y, x in game.get_legal_moves(player):
        tree += get_tree2((y, x), blanks, game)
    return tree

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float('-inf')

    if game.is_winner(player):
        return float('inf')

    blanks = game.get_blank_spaces()
    blanks_n = len(blanks)
    max_blanks = game.width * game.height

    # Beginning game & Middle game.
    if blanks_n > max_blanks*0.1:
        return custom_score_2(game, player)
    # End game.
    else:
        my_tree = get_tree(game, player)
        opp_tree = get_tree(game, game.get_opponent(player))
        return float(len(my_tree) - len(opp_tree))

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float('-inf')

    if game.is_winner(player):
        return float('inf')
    
    my_score, opp_score = 0, 0
    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # Look one more ply ahead and count all the possible moves there.
    for move in my_moves:
        my_score += len(get_Lmoves(game, move))
    
    for move in opp_moves:
        opp_score += len(get_Lmoves(game, move))

    return float(my_score - opp_score)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float('-inf')

    if game.is_winner(player):
        return float('inf')

    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    my_moves_n = len(my_moves)
    opp_moves_n = len(opp_moves)

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    # While considering available moves, try to stay towards the middle.
    return float(my_moves_n - opp_moves_n) - float(math.sqrt((h - y)**2 + (w - x)**2))*0.25


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=20.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def time_remaining(self):            
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def terminal_test(self, game):
        if game.get_legal_moves():
            return False
        return True

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        moves = game.get_legal_moves()
        if not moves:
            return -1,-1

        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = random.choice(moves)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def __max_value(self, game, depth):
        super().time_remaining()

        if self.terminal_test(game) or depth <= 0:
            return self.score(game, self)
        v = float('-inf')
        for move in game.get_legal_moves():
            v = max(v, self.__min_value(game.forecast_move(move), depth-1))
        return v

    def __min_value(self, game, depth):
        super().time_remaining()

        if self.terminal_test(game) or depth <= 0:
            return self.score(game, self)
        v = float('inf')
        for move in game.get_legal_moves():
            v = min(v, self.__max_value(game.forecast_move(move), depth-1))
        return v

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if not game:
            raise Exception("Expected a game object but got None.")
        if depth <= 0 and self.search_depth:
            depth = self.search_depth
        
        # Minimax.
        best = max(game.get_legal_moves(),
            key=lambda move: self.__min_value(game.forecast_move(move), depth-1))

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return best

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        moves = game.get_legal_moves()
        if not moves:
            return -1,-1
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = random.choice(moves)
        depth = 1
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                move = self.alphabeta(game, depth)
                # Only make it a best move if it's not the null case.
                if move != (-1,-1):
                    best_move = move
                depth += 1
                # Cutoff: You've gone too deep...
                if move == (-1,-1):
                    break
            
        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        return best_move
    
    def __alphabeta_max(self, game, alpha, beta, depth):
        super().time_remaining()
        if self.terminal_test(game) or depth <= 0:
            return self.score(game, self), None
        v, best = float('-inf'), (-1, -1)
        for move in game.get_legal_moves():
            child_v, _ = self.__alphabeta_min(game.forecast_move(move), alpha, beta, depth-1)
            if child_v > v:
                v = child_v
                best = move
            if v >= beta: break
            alpha = max(alpha, v)
        return v, best

    def __alphabeta_min(self, game, alpha, beta, depth):
        super().time_remaining()
        if self.terminal_test(game) or depth <= 0:
            return self.score(game, self), None
        v, best = float('inf'), (-1, -1)
        for move in game.get_legal_moves():
            child_v, _ = self.__alphabeta_max(game.forecast_move(move), alpha, beta, depth-1)
            if child_v < v:
                v = child_v
                best = move
            beta = min(beta, v)
            if v <= alpha: break
        return v, best

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if not game:
            raise Exception("Expected a game object but got None.")
        if depth <= 0 and self.search_depth:
            depth = self.search_depth

        # Alpha Beta Search
        best_value, best_move = self.__alphabeta_max(game, alpha, beta, depth)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return best_move
