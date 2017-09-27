"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))
    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parajmeters
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
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)
    p_moves = game.get_legal_moves()

    if not opp_moves:
        return float("inf")

    if not p_moves:
        return float("-inf")

    return float(len(p_moves) - len(opp_moves)) 


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
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)
    p_moves = game.get_legal_moves()
    common_moves = opp_moves and p_moves

    if not opp_moves:
        return float("inf")

    if not p_moves:
        return float("-inf")

    factor = 1 / (game.move_count + 1)
    ifactor = 1 / factor

    return float(len(common_moves) * factor + ifactor * len(game.get_legal_moves()))


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


        if game.move_count == 0:

            return(int(game.height/2), int(game.width/2))

        else:
        
            best_move = (-1, -1)

            try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            #best_move= self.minimax(game, self.search_depth)
                best_move, _ = self.minimax(game, self.search_depth)

           # Return the best move from the last completed search iteration 
                return best_move   

            except SearchTimeout:

            #pass

                raise SearchTimeout() # Handle any actions required after timeout as needed


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

        #self.time_left = time_left


        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout


        # Are there any legal moves left for us to play? If not, then we lost!
        # The maximizing (minimizing) player returns the lowest (highest) possible score.
        legal_moves = game.get_legal_moves()

        lowest_score_so_far, highest_score_so_far, best_move_so_far = float("inf"), float("-inf"), (-1, -1)

        
        if not legal_moves:

            if game.active_player:
                return (-1, -1), float("-inf")
            else:
                return (-1, -1), float("inf")

        # So, there are still some legal moves.
        # Have we reached the target search depth? If so, return the best possible move at this level.
        # For the maximizing (minimizing) player, that would be the move with the highest (lowest) score.

        if depth == 1:
            if game.active_player:
                for move in legal_moves:
                    # Evaluate this move.
                    score = self.score(game.forecast_move(move), self)
                    # If this is a winning move, no need to search further. Otherwise, remember the best move.
                    if score == float("inf"):
                        return move, score
                    if max(score, highest_score_so_far) == score:
                        highest_score_so_far, best_move_so_far = score, move
                return best_move_so_far, highest_score_so_far
            else:
                for move in legal_moves:
                    # Evaluate this move.
                    score = self.score(game.forecast_move(move), self)
                    # If this is a winning move, no need to search further. Otherwise, remember the best move.
                    if score == float("-inf"):
                        return move, score
                    if min(score, lowest_score_so_far) == score:
                        lowest_score_so_far, best_move_so_far = score, move
                return best_move_so_far, lowest_score_so_far

        # There are still some legal moves and we are not at target search depth.
        # Go down search branches one after the other, and return the best possible branch at this level.
        # For the maximizing (minimizing) player, that would be the branch with the highest (lowest) score.
        if game.active_player:
            for move in legal_moves:
                # Evaluate this move in depth.
                _, score = self.minimax(game.forecast_move(move), depth-1)
                # If this branch yields a sure win, no need to search further. Otherwise, remember the best move.
                if score == float("inf"):
                    return move, score
                if max(score, highest_score_so_far) == score:
                    highest_score_so_far, best_move_so_far = score, move
            return best_move_so_far, highest_score_so_far
        else:
            for move in legal_moves:
                # Evaluate this move in depth.
                _, score = self.minimax(game.forecast_move(move), depth-1)
                # If this branch yields a sure win, no need to search further. Otherwise, remember the best move.
                if score == float("-inf"):
                    return move, score
                if min(score, lowest_score_so_far) == score:
                    lowest_score_so_far, best_move_so_far = score, move
            return best_move_so_far, lowest_score_so_far



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
    

        # TODO: finish this function!

        
        self.time_left = time_left

        best_move = (-1, -1)


        if game.move_count == 0:

            best_move = (int(game.height/2), int(game.width/2))

            return best_move
        
        
        for i in range(1, 10000):

            try:
                best_move, _ = self.alphabeta(game, i)

                return best_move

            except SearchTimeout:
                break
        #print(move)
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


        # TODO: finish this function!
    

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        
        legal_moves = game.get_legal_moves()

        lowest_score_so_far, highest_score_so_far, best_move_so_far = float("inf"), float("-inf"), (-1, -1)


        if not legal_moves:

            if game.active_player:
                return (-1, -1), float("-inf")
            else:
                return (-1, -1), float("inf")

        if depth == 1:

            if game.active_player:

                for move in legal_moves:

                    game_child = game.forecast_move(move)

                    score = self.score(game_child, self)

                    if score >= beta:

                        return move, score

                    if max(score, highest_score_so_far) == score:
                        highest_score_so_far, best_move_so_far = score, move


                return best_move_so_far, highest_score_so_far

            else:

                for move in legal_moves:

                    game_child = game.forecast_move(move)

                    score = self.score(game_child, self)

                    if score <= alpha:

                        return move, score

                    if min(score, lowest_score_so_far) == score:
                        lowest_score_so_far, best_move_so_far = score, move


                return best_move_so_far, lowest_score_so_far



        
        if game.active_player:

            for move in legal_moves:

                game_child = game.forecast_move(move)

                _, score = self. alphabeta(game_child, depth-1, alpha, beta)

                if score >= beta:
                    return move, score

                if max(score, highest_score_so_far) == score:
                        highest_score_so_far, best_move_so_far = score, move

                alpha = max(alpha, highest_score_so_far)

            return best_move_so_far, highest_score_so_far

        else:

            for move in legal_moves:

                game_child = game.forecast_move(move)

                _, score = self.alphabeta(game_child, depth-1, alpha, beta)

                if score <= alpha:

                    return move, score

                if min(score, lowest_score_so_far) == score:
                        lowest_score_so_far, best_move_so_far = score, move


                beta = min(beta, lowest_score_so_far)

            return best_move_so_far, lowest_score_so_far





if __name__ == "__main__":
    from isolation import Board
    #from sample_players import RandomPlayer

    # create an isolation board (by default 7x7)
    
    player2 = MinimaxPlayer()
    #player1 = RandomPlayer()
    player1 = AlphaBetaPlayer()
    game = Board(player1, player2)

    # place player 1 on the board at row 2, column 3, then place player 2 on
    # the board at row 0, column 5; display the resulting board state.  Note
    # that the .apply_move() method changes the calling object in-place.
    
    #game.apply_move((6, 3))
    #game.apply_move((2, 3))
    #game.apply_move((0, 5))
    #print(game.to_string())

    # players take turns moving on the board, so player1 should be next to move
    #assert(player1 == game.active_player)

    # get a list of the legal moves available to the active player
    #print(game.get_legal_moves())

    # get a successor of the current state by making a copy of the board and
    # applying a move. Notice that this does NOT change the calling object
    # (unlike .apply_move()).
    
    #new_game = game.forecast_move((1, 1))



    #assert(new_game.to_string() != game.to_string())
    #print("\nOld state:\n{}".format(game.to_string()))
    #print("\nNew state:\n{}".format(new_game.to_string()))

    # play the remainder of the game automatically -- outcome can be "illegal
    # move", "timeout", or "forfeit"
    winner, history, outcome = game.play()
    print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    print(game.to_string())
    print("Move history:\n{!s}".format(history))


