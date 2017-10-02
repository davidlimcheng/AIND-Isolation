"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


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
    # TODO: finish this function!
    # Similar to the improved_score method in sample_players.py, but goes one step deeper and gets
    # the total number of moves for child nodes as well.
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    my_moves_total = len(my_moves)
    opponent_moves_total = len(opponent_moves)
    for move in my_moves:
        child_board = game.forecast_move(move)
        child_board_moves = child_board.get_legal_moves(player)
        my_moves_total += len(child_board_moves)
    for move in opponent_moves:
        child_board = game.forecast_move(move)
        child_board_moves = child_board.get_legal_moves(game.get_opponent(player))
        opponent_moves_total += len(child_board_moves)
    return float(my_moves_total - opponent_moves_total)


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
    # TODO: finish this function!
    # Splits the board into 9 3x3 "units", and evaluates how many remaining spaces
    # are on the units the player is currently on.
    # Occupation of multiple units are more heavily weighted via a multiplier.

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    units = [
        [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
        [(2, 0), (3, 0), (4, 0), (2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2)],
        [(4, 0), (5, 0), (6, 0), (4, 1), (5, 1), (6, 1), (4, 2), (5, 2), (6, 2)],
        [(0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4)],
        [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (4, 3), (2, 4), (3, 4), (4, 4)],
        [(4, 2), (5, 2), (6, 2), (4, 3), (5, 3), (6, 3), (4, 4), (5, 4), (6, 4)],
        [(0, 4), (1, 4), (2, 4), (0, 5), (1, 5), (2, 5), (0, 6), (1, 6), (2, 6)],
        [(2, 4), (3, 4), (4, 4), (2, 5), (3, 5), (4, 5), (2, 6), (3, 6), (4, 6)],
        [(4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)]
    ]
    units_occupied = 0
    blank_spaces_in_units = []
    pos = game.get_player_location(player)
    blank_spaces = game.get_blank_spaces()
    for unit in units:
        if pos in unit:
            units_occupied += 1
            for space in blank_spaces:
                if space in unit:
                    blank_spaces_in_units.append(space)
    unique_blank_spaces = len(set(blank_spaces_in_units))
    return float(units_occupied * unique_blank_spaces)


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
    # TODO: finish this function!
    # A mix of both improved_score and center_score, but gives more weight to improved_score since it seems to be
    # doing a bit better in the tournament.
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    improved_score_util = float(own_moves - opp_moves)

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    center_score_util = float((h - y)**2 + (w - x)**2)

    return (0.75 * improved_score_util) + (0.25 * center_score_util)


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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


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
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        def min_value(board, depth, current_depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            utility = board.utility(self)
            current_depth += 1
            if utility != 0 or current_depth >= depth:
                return self.score(board, self)
            value = float("inf")
            legal_moves = board.get_legal_moves()
            for move in legal_moves:
                child_board = board.forecast_move(move)
                value = min(value, max_value(child_board, depth, current_depth))
            return value

        def max_value(board, depth, current_depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            utility = board.utility(self)
            current_depth += 1
            if utility != 0 or current_depth >= depth:
                return self.score(board, self)
            value = float("-inf")
            legal_moves = board.get_legal_moves()
            for move in legal_moves:
                child_board = board.forecast_move(move)
                value = max(value, min_value(child_board, depth, current_depth))
            return value

        current_depth = 0
        moves = game.get_legal_moves()
        if not len(moves):
            return -1, -1
        scores = []
        for move in moves:
            child_board = game.forecast_move(move)
            value = min_value(child_board, depth, current_depth)
            scores.append(value)
        best_score_index = scores.index(max(scores))
        return moves[best_score_index]


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
        self.time_left = time_left
        self.search_depth = 1

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                best_move = self.alphabeta(game, self.search_depth)
                self.search_depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        def max_value(board, depth, current_depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            utility = board.utility(self)
            if utility != 0 or current_depth >= depth:
                # Since this is a terminal state, returns (-1, -1) as there are no moves available
                return self.score(board, self), (-1, -1)
            current_depth += 1
            scores, moves = [], []
            legal_moves = board.get_legal_moves()
            for move in legal_moves:
                child_board = board.forecast_move(move)
                # Assume that the child is a terminal node, so we only care about the utility it brings back
                child_util, _ = min_value(child_board, depth, current_depth, alpha, beta)
                if child_util >= beta:
                    return child_util, move
                alpha = max(alpha, child_util)
                scores.append(child_util)
                moves.append(move)
            best_score_index = scores.index(max(scores))
            return scores[best_score_index], moves[best_score_index]

        def min_value(board, depth, current_depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            utility = board.utility(self)
            if utility != 0 or current_depth >= depth:
                return self.score(board, self), (-1, -1)
            current_depth += 1
            scores, moves = [], []
            legal_moves = board.get_legal_moves()
            for move in legal_moves:
                child_board = board.forecast_move(move)
                child_util, _ = max_value(child_board, depth, current_depth, alpha, beta)
                if child_util <= alpha:
                    return child_util, move
                beta = min(beta, child_util)
                scores.append(child_util)
                moves.append(move)
            best_score_index = scores.index(min(scores))
            return scores[best_score_index], moves[best_score_index]

        current_depth = 0
        # We don't care about the bound at this point, just the move we need to make
        _, move = max_value(game, depth, current_depth, alpha, beta)
        return move
