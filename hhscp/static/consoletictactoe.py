#! /usr/bin/python
#
# Tic Tac Toe engine (to be used in a pygame application
#

__author__ = 'ericdennison'

import random

class TTTPosition(object):
    """
    Representation of a tic tac toe board play position (where pieces are and
    whose turn it is)

    Internally, the board is represented as a tuple of 9 integers that represent
    positions on the grid, thus:

    ( 0, 0, 0,
      0, 0, 0,
      0, 0, 0)

    X is represented by +1
    O is represented by -1
    In addition to the board position, the object also knows which player is to
    move NEXT (-1 or +1)
    """

    # Coordinates for three in a row. Each tuple represents the indexes of three
    # positions on the board that represent a win if they all hold the same
    # non-zero value (i.e. all +1 or all -1). We will use this to "automate" the
    # process of checking for a winning position.

    threes = [  (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (0,4,8),
        (2,4,6)]

    # how many moves should we try to look ahead
    searchdepth = 20

    def __init__(self, statelist = [0,0,0,0,0,0,0,0,0], nextplayer = 1):
        """
        Initialization - you can set up the initial board to have any arrangement
        of pieces, with any player needing to make the next move.
        """
        self.board = tuple(statelist)
        self.nextplayer = nextplayer
        self.score = None
        self.nextmoves = []

    def __repr__(self):
        """
        This "hidden" python method is used to customize the string
        REPResentation of an object, so that when we print it on the console,
        it looks sensible.

        A typical print display for a TTTPosition object looks like this;

        nextplayer: X, score: ~
        X~O
        ~X~
        ~~O

        The score parameter represents which player is favored by the current
        position.

        Defining this method will make it possible to write code like:

        print(position1)

        and have it print something sensible.
        """
        # piecefromval is a "mini" function that returns X or O, depending
        # on whether the player is a 1 or -1
        piecefromval = lambda x: 'X' if x == 1 else 'O' if x == -1 else '~'

        retval = 'nextplayer: {0}, score: {1}\n'.format(
            piecefromval(self.nextplayer), piecefromval(self.score))
        for i in range(3):
            for j in range(3):
                retval += '{0}'.format(piecefromval(self.board[i*3+j]))
            retval += '\n'
        return retval


    def __eq__(self, other):
        """
        Check for "equalness" with other board positions. Equalness requires that the
        board and nextplayer members match. Defining this method will allow us to do
        simple things like:

        if position1 == position2:

        """
        if not other:
            return False
        else:
            return self.board == other.board and self.nextplayer == other.nextplayer

    def _ifromxy(self, coords):
        """
        Utility function returns index into the 9 position board list, given an
        x,y coordinate pair.Parameter coords specifies an x,y pair relative to
        the upper left corner of the playing board. coord (0,0) specifies UL
        corner. (2,0) the UR corner, (2,2) the LR corner and (0,2) the LL corner.
        This method returns an index.
        """
        return coords[0]+coords[1]*3

    def _possiblemoves(self):
        """
        Return a list of new TTTPosition objects representing all possible next
        moves. The method walks through every spot on the grid, looking for empty
        ones. Each empty spot is used to define a new TTTPosition object with
        that spot filled. The list of new TTTPosition objects is returned.

        Note: the method sets a property: nextmoves with the result of this call.
        If it is called a second time in the future, it just returns the
        previously computed version.
        """
        if not len(self.nextmoves):
            for i in range(9):
                if not self.board[i]:
                    newboard = list(self.board[:])
                    newboard[i] = self.nextplayer
                    self.nextmoves.append(self._newinstance(newboard, self.nextplayer * -1))
        return self.nextmoves

    def _newinstance(self, statelist, nextplayer):
        """
        Generate new instance of this class
        """
        return type(self)(statelist, nextplayer)

    def setmove(self, coords):
        """
        Play a position on the board. Parameter specifies an x,y pair relative
        to the upper left corner of the playing board. coord (0,0) specifies UL
        corner. (2,0) the UR corner, (2,2) the LR corner and (0,2) the LL corner.
        The piece played will be equal to the nextplayer attribute of the
        current position. This method returns a NEW TTTPosition object with the
        desired state and an updated nextplayer attribute (-1 if it was +1, or
        +1 if it was -1)
        """
        boardlist = list(self.board)
        boardlist[self._ifromxy(coords)] = self.nextplayer
        # return a new instance of this class
        return self._newinstance(boardlist, self.nextplayer * -1)

    def checkwin(self):
        """
        Check the current position to see if it is a winning configuration for
        either player.
        If player +1 wins with this position, return +1
        If player -1 wins with this position, return -1
        Otherwise, return 0.
        """
        match = 0
        for r in self.threes:   # check each possible set of winning indexes
            # next line builds a list of pieces in the row, then checks to see
            # if they all match
            #
            # The reduce function takes two arguments. First is a function
            # reference and second is a list. The function takes two arguments,
            # the first of which is accumulated from item to item. The second
            # argument is pulled from each successive item in the list. See
            # documentation for reduce for details.
            #
            # The lamba function here returns one of the arguments if both
            # input arguments match and 0 if they do not match.
            #
            # The list argument to reduce is a list of board indexes to
            # check for a winning row.
            match = reduce(lambda x,y: x if x == y else 0, [self.board[x] for x in r])
            # if there is a match that is +1 or -1, stop looking
            if match:
                break
        return match

    def getscore(self, searchdepth):
        """
        Evaluate the current position, returning a list of possible next positions
        and a score for this position. Score is +1, 0, or -1, depending on which
        player is favored. +1 or -1 means that player can win from the position.
        The method returns two values: a list of possible next moves (each with
        its own score) and a score for THIS position.

        The method must RECURSIVELY call the getscore method at each oevel
        of the tree below this position. If any set of positions contains
        a winning score for that player, then it is assumed that player would
        pick that option.

        Searchdepth argument determines how far to go in recursion. Since the
        the game tree grows RAPIDLY with depth, it may be worth limiting
        the search.

        The method checks for a WINNING position first, returning +1 or -1
        as the score in that case.
        """
        win = self.checkwin()
        if win:
            # this is a winning position - the score is known
            self.score = win
            return [], self.score
        elif searchdepth:
            nextmoves = self._possiblemoves()
            if len(nextmoves):
                # there are multiple next moves to consider: get their scores
                scores = [move.getscore(searchdepth-1)[1] for move in nextmoves]
                # return the best score that favors the next player, assuming
                # that's the move the player will make
                if self.nextplayer > 0:
                    retval = max(scores)    # most positive for player +1
                else:
                    retval = min(scores)    # most negative for player -1
                self.score = retval
                return nextmoves, retval   #
            else:
                # there are no more moves to make - no one wins
                self.score = 0
                return [], 0
        else:   # recursion depth limit exceed, return ambiguous
            return [], 0

    def inputnextmove(self):
        """
        Solicit next move from the user. Loop until the entered move is one
        of the possible next moves known for the current position.
        """
        possibles = self._possiblemoves()
        next = None
        if len(possibles):
            while not next in possibles:  # ensure valid moves are taken by the human
                print ("Current board position is: ")
                print (self)
                move = input("Your move - enter tuple: e.g. (0,2): ")
                next = self.setmove(move)
            return next
        else:
            return None # no more moves possible

    def autonextmove(self):
        """
        Automatically decide from all possible next moves, which is best for
        the next player. First, attempts to build a list of next moves whose
        scores match our own player (+1 if we are player +1, or -1 if we are
        -1). Otherwise, choose from the neutral options, otherwise, the losing
        ones.

        Method returns a TTTPosition object chosen at random from the
        best list.
        """
        nextmoves, score = self.getscore(self.searchdepth)
        # look for nextmoves that are best for us (nextplayer)
        bestnextmoves = filter( lambda move, np = self.nextplayer:
                                move.score == np,
                                nextmoves)
        if not len(bestnextmoves):
            # otherwise, just take neutral ones
            bestnextmoves = filter(lambda move: move.score == 0, nextmoves)
            if not len(bestnextmoves):
                # only options favor the enemy: probably should give up
                bestnextmoves = filter( lambda move, np = -1 * self.nextplayer:
                                        move.score == np,
                                        nextmoves)
        # choose randomly from the available
        return random.choice(bestnextmoves) if len(bestnextmoves) else None

    def playconsole(self):
        """
        Play a basic console game.

        g is set equal to self, which is the initial position of the board.
        As player and computer make new moves, new TTTPosition objects are
        created and assigned to g, so g is used to keep track of the current
        position at all times. Play switches back and forth between the
        computer (nextplayer = -1) and the human (nextplayer = +1) until
        a winning board position is detected.
        """
        g = self
        lastg = g
        # continue until a draw or a winner
        while g and not g.checkwin():
            lastg = g
            # human is +1 (X)
            if g.nextplayer > 0:
                g = g.inputnextmove()
            else:
                g = g.autonextmove()

        # print the outcome
        if not g:
            print "Draw"
            g = lastg
        else:
            if g.checkwin() > 0:
                print "You win!"
            else:
                print "You lose!"
        print "Final board:"
        print g


# Set an initial, blank position, next player is X
if __name__ == '__main__':
    g = TTTPosition([0,0,0,0,0,0,0,0,0],1)
    g.playconsole()