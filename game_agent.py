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
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    moves = len(game.get_legal_moves())
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(moves - opp_moves + calc_central(game, game.get_player_location(player)))


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
    
    moves = len(game.get_legal_moves())
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(moves - opp_moves)


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
    
    moves = len(game.get_legal_moves())
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    if moves != opp_moves:
        return float(moves - opp_moves)

    else:
        #If the number of moves is equal I use the manhathan disrtance to determine te evaluation function 
        
        center_y_pos, center_x_pos = int(game.height / 2), int(game.width / 2)
        player_y_pos, player_x_pos = game.get_player_location(player)
        opponent_y_pos, opponent_x_pos = game.get_player_location(game.get_opponent(player))
        player_distance = abs(player_y_pos - center_y_pos) + abs(player_x_pos - center_x_pos)
        opponent_distance = abs(opponent_y_pos - center_y_pos) + abs(opponent_x_pos - center_x_pos)
        # Diference between the player and opponente player scale between -1 y 1.
        return float(opponent_distance - player_distance) / 10.

def calc_central(game, move):
    """ Calculate the distance between move and the center of the board
    
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
        The distance value between the position and the center of the board.
    """
    x, y = move
    cx, cy = (math.ceil(game.width / 2), math.ceil(game.height / 2))
    return (game.width - cx) ** 2 + (game.height - cy) ** 2 - (x - cx) ** 2 - (y - cy) ** 2

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
        # Initializing the lis to store the utilities values
        utility=[]
        # First I get the legal moves for the actual state of the board
        legal_moves=game.get_legal_moves()
        print(legal_moves)
        # If there is no legal_moves we have to return (-1,-1)
        if len(legal_moves)==0:
            return (-1,1)
        
        # I made an iteration to get the utility value for each move aplying minmax
        for move in legal_moves:
            #I get a new game apliying the first move
            print(move)
            new_game= game.forecast_move(move)
            utility.append(self.min_value(new_game,depth-1))
        #Taking the maximun value from the utility
        max_utility=max(utility)
        
        return legal_moves[utility.index(max_utility)]
    
        #raise NotImplementedError

    def max_value(self,game, current_depth):
        """ Implement a function to obtain the max value of a tree 
        
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        
        current_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        

        Returns
        -------
        int        
            The utility value for the movement
        """
        utility=[]
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if self.terminal_test(game) or (current_depth==0):
            return self.score(game,self)
        
        legal_moves=game.get_legal_moves()
        
        for move in legal_moves:
            new_game=game.forecast_move(move)
            utility.append(self.min_value(new_game,current_depth-1))
        
        return max(utility)
    
    def min_value(self,game,current_depth):
        """ Implement a function to obtain the min value of a tree 
        
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        current_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        int        
            The utility value for the movement
        """
        utility=[]
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if self.terminal_test(game) or (current_depth==0):
            return self.score(game,self)
        
        legal_moves=game.get_legal_moves()
        
        for move in legal_moves:
            new_game=game.forecast_move(move)
            utility.append(self.max_value(new_game,current_depth-1))
        
        return min(utility)
        
    def terminal_test(self,game):
        """ Determine if the game is at the end for the player
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        
        Returns
        -------
        boolean        
            if the legal_moves=0 then is the end of the game 
        """
            
        moves=game.get_legal_moves()
        
        if len(moves)==0:
            return True
        return False
    
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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = 1
            while True:
                best_move= self.alphabeta(game, depth)
                depth+=1

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
    
        # First I get the legal moves for the actual state of the board
        legal_moves=game.get_legal_moves()
        # If there is no legal_moves we have to return (-1,-1)
        if len(legal_moves)==0:
            return (-1,1)
        
        best_action= None
        
        # I run through all the values in legal moves to obtain the best action
        for move in legal_moves:
            new_game=game.forecast_move(move)
            utility=self.min_value(new_game,depth-1, alpha,beta)
            if utility > alpha:
                alpha=utility
                best_action=move
                
        return best_action
        
    
    def max_value(self,game, current_depth,alpha,beta):
        """ Implement a function to obtain the max value of a tree 
        
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        
        current_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers
        

        Returns
        -------
        int        
            The utility value for the movement
        """
        
        utility=float("-inf")
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if self.terminal_test(game) or (current_depth==0):
            return self.score(game,self)
        
        legal_moves=game.get_legal_moves()
        
        for move in legal_moves:
            new_game=game.forecast_move(move)
            utility=max(utility,self.min_value(new_game,current_depth-1,alpha,beta))
            if utility >= beta:
                return utility
            alpha=max(alpha,utility)
        
        return utility
    
    def min_value(self,game,current_depth,alpha,beta):
        """ Implement a function to obtain the min value of a tree 
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        current_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        int        
            The utility value for the movement
        """
      
        utility=float("inf")
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if self.terminal_test(game) or (current_depth==0):
            return self.score(game,self)
        
        legal_moves=game.get_legal_moves()
        
        for move in legal_moves:
            new_game=game.forecast_move(move)
            utility=min(utility,self.max_value(new_game,current_depth-1,alpha,beta))
            if utility <= alpha:
                return utility
            beta=min(beta,utility)
    
        return utility
        
    def terminal_test(self,game):
        """ Determine if the game is at the end for the player
        
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        
        Returns
        -------
        boolean        
            if the legal_moves=0 then is the end of the game 
        """
            
        moves=game.get_legal_moves()
        
        if len(moves)==0:
            return True
        return False
     
        