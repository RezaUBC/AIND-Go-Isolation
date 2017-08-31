
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
        
    If the player has more moves than the opponent get closer, if not run away!
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    ## Calculate sum of distance of all the moves to the center
    Xcen, Ycen = game.width / 2., game.height / 2.
    own_moves = game.get_legal_moves(player)
    len_opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    SumDist = 0.0
    for move in own_moves:
        new_game = game.forecast_move(move)
        Yplayer, Xplayer = new_game.get_player_location(player) ## player's location is (x,y)
        playersDist = float((Yplayer - Ycen)**2 + (Xplayer - Xcen)**2)
        SumDist += playersDist

    return SumDist*float(1.2*len(own_moves) - len_opp_moves)
 


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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    Yplayer, Xplayer = game.get_player_location(player) ## player's location is (x,y)
    Yoppon,  Xoppon  = game.get_player_location(game.get_opponent(player))
    
    playersDist = float((Yplayer - Yoppon)**2 + (Xplayer - Xoppon)**2)

    if own_moves >= opp_moves:
        return playersDist
    else:
        return -1.0/playersDist
    return 0

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    active_player = game.active_player
    inactive_player = game.inactive_player
    movesleftAc = game.get_legal_moves(active_player)
    movesleftInAc= game.get_legal_moves(inactive_player)
    if (player == active_player):
        return float(1.2*len(movesleftAc) - len(movesleftInAc))
    else:
        return float(1.2*len(movesleftInAc) - len(movesleftAc))


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
        self._best_move = None


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def terminal_test(self, gameState):
        """ Return True if the game is over for the active player
        and False otherwise.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        movesleft = gameState.get_legal_moves()
        if len(movesleft)>0:
            return False
        else:
            return True


    def min_value(self,gameState,current_depth,max_depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(gameState):
            return float("inf")

        movesleft = gameState.get_legal_moves()
        if (current_depth >= max_depth):
            return self.score(gameState,self)
        current_depth += 1
        sc = float("inf")
        for child in movesleft:
            sc = min(sc,self.max_value(gameState.forecast_move(child),current_depth,max_depth))
        return sc

    def max_value(self,gameState,current_depth,max_depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(gameState):
            return float("-inf")
        
        movesleft = gameState.get_legal_moves()
        
        if (current_depth >= max_depth):
            return self.score(gameState,self)
        
        current_depth += 1
        sc = float("-inf")
        for child in movesleft:
            sc = max(sc,self.min_value(gameState.forecast_move(child),current_depth, max_depth))
        return sc
    
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
        best_move = (-1,-1)
        lmoves = game.get_legal_moves()
        if not lmoves:
            return best_move
        if game.active_player == self:   
            best_score = float("-inf")
            for m in lmoves:
                v = self.min_value(game.forecast_move(m),1,depth)
                if v > best_score:
                    best_score = v
                    best_move = m
        else:
            best_score = float("inf")
            for m in lmoves:
                v = self.max_value(game.forecast_move(m),1,depth)
                if v < best_score:
                    best_score = v
                    best_move = m
        return best_move

#        return max(game.get_legal_moves(), key=lambda m: min_value(game.forecast_move(m),0,depth))


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    
    def terminal_test(self, gameState):
        """ Return True if the game is over for the active player
        and False otherwise.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        movesleft = gameState.get_legal_moves()
        if len(movesleft)>0:
            return False
        else:
            return True


    def min_value(self,gameState,depth,alpha,beta):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(gameState):
            return float("inf")

        movesleft = gameState.get_legal_moves()
        if (depth==0):
            return self.score(gameState,self)
#        depth -= 1
        
        sc = float("inf")
        for child in movesleft:
            sc = min(sc,self.max_value(gameState.forecast_move(child),depth-1,alpha,beta))
            if sc<=alpha:
                return sc
            beta=min(beta,sc)
            if (beta<=alpha):
                break
        return sc

    def max_value(self,gameState,depth,alpha,beta):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if self.terminal_test(gameState):
            return float("-inf")
        
        movesleft = gameState.get_legal_moves()
        
        if (depth==0):
            return self.score(gameState,self)
#        depth -= 1
        
        sc = float("-inf")
        for child in movesleft:
            sc = max(sc,self.min_value(gameState.forecast_move(child),depth-1,alpha,beta))
            if sc>=beta:
                return sc
            alpha=max(alpha,sc)
            if (beta<=alpha):
                break
        return sc
    
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

        # TODO: finish this function!
        
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1;
            while True:
                best_move = self.alphabeta(game, depth)
                self._best_move = best_move
                depth += 1
            return best_move

        except SearchTimeout:
            return self._best_move  # Handle any actions required after timeout as needed

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
        
        best_move = (-1,-1)
        lmoves = game.get_legal_moves()
        if not lmoves:
            return best_move
        
        if game.active_player == self:   
            best_score = float("-inf")
            for m in lmoves:
                v = self.min_value(game.forecast_move(m),depth-1,alpha,beta)
                if v > best_score:
                    best_score = v
                    best_move = m
                    self._best_move = best_move
                alpha = max(alpha,best_score)
                if (beta<=alpha):
                    break
        else:
            best_score = float("inf")
            for m in lmoves:
                v = self.max_value(game.forecast_move(m),depth-1,alpha,beta)
                if v < best_score:
                    best_score = v
                    best_move = m
                    self._best_move = best_move
                beta = min(beta,best_score)
                if (beta<=alpha):
                    break
        return best_move

#        best_move = (-1,-1)
#        lmoves = game.get_legal_moves()
#        if not lmoves:
#            return best_move
#        if game.active_player == self:   
#            for m in lmoves:
#                best_move = self.max_value(game.forecast_move(m),depth,alpha,beta)
#                self._best_move = best_move
#        else:
#            for m in lmoves:
#                best_move = self.min_value(game.forecast_move(m),depth,alpha,beta)
#                self._best_move = best_move
#        return best_move
