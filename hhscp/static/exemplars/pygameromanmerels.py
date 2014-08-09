#! /usr/bin/python
#
# Simple Roman Merels engine (to be used in a pygame application)
#

__author__ = 'ericdennison'

import random

from pygametictactoe import TTTPosition

class MerelsPosition(TTTPosition):
    """
    Representation of a Merels board play position (where pieces are and
    whose turn it is)

    Internally, the board is represented as a tuple of 9 integers that represent
    positions on the circular grid, thus:

    ( 0, 0, 0,
      0, 0, 0,
      0, 0, 0)

    Winning positions:

    X ~ ~    ~ ~ X    ~ X ~    ~ ~ ~
    ~ X ~    ~ X ~    ~ X ~    X X X
    ~ ~ X    X ~ ~    ~ X ~    ~ ~ ~

    X is represented by +1
    O is represented by -1
    In addition to the board position, the object also knows which player is to
    move NEXT (-1 or +1)

    See http://gwydir.demon.co.uk/jo/games/romgame/index.htm

    """

    # Coordinates for three in a row. Each tuple represents the indexes of three
    # positions on the board that represent a win if they all hold the same
    # non-zero value (i.e. all +1 or all -1). We will use this to "automate" the
    # process of checking for a winning position.

    threes = [  (3,4,5),    # horizontal
        (1,4,7),            # vertical
        (0,4,8),            # diagonal slope -1
        (2,4,6)]            # diagonal slope +1

    # Coordinates for neighbors of each position on the board. This is used
    # to find candidate positions for sliding
    neighbors = [   (1,3,4), # neighbors from 0
                    (0,2,4), # neighbors from 1
                    (1,4,5), # and so on...
                    (0,4,6),
                    (0,1,2,3,5,6,7,8), # lots of places to go from 4
                    (2,4,8),
                    (3,4,7),
                    (4,6,8),
                    (4,5,7)]

    searchdepth = 7

    def __init__(self, statelist = [0,0,0,0,0,0,0,0,0], nextplayer = 1):
        super(MerelsPosition, self).__init__(statelist, nextplayer)

    
    def _possiblemoves(self):
        """
        Return a list of new MerelsPosition objects representing all possible next
        moves. The method walks through every spot on the grid, looking for empty
        ones. Each empty spot is used to define a new MerelsPosition object with
        that spot filled. The list of new MerelsPosition objects is returned.

        If player hasn't played all his pieces yet, he must play one. If all
        have been played, a piece may be slid one position

        Note: the method sets a property: nextmoves with the result of this call.
        If it is called a second time in the future, it just returns the
        previously computed version.
        """
        # utility function for adding new positions
        appendposition = lambda pos, player=self.nextplayer * -1: self.nextmoves.append(MerelsPosition(pos,player))

        if not len(self.nextmoves):
            if self.mustslide():
                for i in range(9):   # for each spot on the board
                    if self.board[i] == self.nextplayer:   # if our piece is there
                        for n in self.neighbors[i]:        # consider its neighbors
                            if not self.board[n]:          # that are empty
                                newboard = list(self.board[:])
                                newboard[n] = self.nextplayer   # move here
                                newboard[i] = 0                 # from here
                                appendposition(newboard)
            else:
                for i in range(9):
                    if not self.board[i]:
                        newboard = list(self.board[:])
                        newboard[i] = self.nextplayer
                        appendposition(newboard)
                        #self.nextmoves.append(MerelsPosition(newboard, self.nextplayer * -1))
        return self.nextmoves

    def mustslide(self):
        """
        Return True if the nextplayer has played all his positions and must
        begin sliding.
        """
        return self.board.count(self.nextplayer) == 3

    def setslide(self, frcoords, tocoords):
        """
        Play a slide on the board
        """
        boardlist = list(self.board)
        boardlist[self._ifromxy(tocoords)] = self.nextplayer
        boardlist[self._ifromxy(frcoords)] = 0
        return self._newinstance(boardlist, self.nextplayer * -1)


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
                if self.mustslide():
                    frmove, tomove = input("Slide a piece - enter from,to: eg. (0,2),(1,1): ")
                    next = self.setslide(frmove, tomove)
                else:
                    move = input("Your move - enter tuple: e.g. (0,2): ")
                    next = self.setmove(move)
            return next
        else:
            return None # no more moves possible


# Play the game!

# Set an initial, blank position, next player is X
if __name__ == '__main__':
    g = MerelsPosition([0,0,0,0,0,0,0,0,0],1)
    g.playconsole()
