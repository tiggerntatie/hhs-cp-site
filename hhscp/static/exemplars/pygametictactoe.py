#! /usr/bin/python
#
# Graphical Tic Tac Toe
#

__author__ = 'ericdennison'

import pygame
from pygame.locals import *
from pygame import font
from consoletictactoe import TTTPosition
from pygameapp import PygameApp

class SuperTTTPosition(TTTPosition):
    """
    Class is an enhanced version of TTTPosition, which can report the
    the difference between two different positions.
    """
    def __init__(self, statelist = [0,0,0,0,0,0,0,0,0], nextplayer = 1):
        """
        Calls base class initializer with default parameters.
        """
        super(SuperTTTPosition, self).__init__(statelist, nextplayer)

    def possiblemoves(self):
        """
        Alias for _possiblemoves
        """
        return self._possiblemoves()

    def __sub__(self, other):
        """
        Subtract one position from another, resulting in a position representing
        only the differences
        """
        # step through board member of self and other, returning a position
        # value only when they are different, otherwise a zero.
        board = list(map(lambda x,y: x+y if x != y else 0, self.board, other.board))
        return SuperTTTPosition(board)

    def positionlist(self):
        """
        Return a list of coordinates for the occupied positions of the board
        """
        pairs = []
        for x in range(3):
            for y in range(3):
                if self.board[x + y * 3]:
                    pairs.append((x,y))
        return pairs


class TTTXO(pygame.sprite.DirtySprite):
    """
    Sprite class representing an X or O in a Tic Tac Toe game.

    Modified from PyGame's DirtySprite class. Each new instance will load
    the appropriate image from disk. No need to worry about performance on
    doing this because it only happens when someone makes a move in the game.
    """
    def __init__(self, XO, coordinates, *groups):
        """
        Class initializer takes the image type as string: "X" or "O" and
        loads the appropriate image. Also must accept a center position for
        the image in pixel coordinates and a list of groups that the
        sprite should belong to. Image file name is X.png or O.png.
        """
        super(TTTXO, self).__init__(groups)
        XOtype = str(XO).upper()
        XOimagepath = './tictactoe/{0}.png'.format(XOtype)
        # every sprite must have an image attribute
        self.image = pygame.image.load(XOimagepath)
        # every sprite must have a rect attribute
        self.rect = self.image.get_rect()   # image as a rectangle
        self.rect.center = coordinates      # move it to the desired location
        self.dirty = 1                      # make sure it gets drawn!


class TTTMessage(pygame.sprite.DirtySprite):
    """
    Sprite class to represent "game over" text message at the bottom
    of the screen
    """
    def __init__(self, message, coordinates, *groups):
        """
        Class initializer takes a text message to display and center
        coordinates
        """
        super(TTTMessage, self).__init__(groups)
        self.font = font.SysFont('arial',30, True)  # BOLD
        # render the message, antialiased, with WHITE color
        self.image = self.font.render(message, True, Color('white'))
        # get the rect attribute going
        self.rect = self.image.get_rect()   # image as a rectangle
        self.rect.center = coordinates      # move it to the desired location
        self.dirty = 1                      # make sure it gets drawn!



class TTTApp(PygameApp):
    """
    Modified from PygameApp AND TTTPosition to use a fixed size background
    image of a Tic Tac Toe grid.
    """
    def __init__(self):
        """
        Initialize the Tic Tac Toe game by initializing the base PygameApp
        class, but with a specific size and title, then override some of
        the default behaviors.
        """
        backgroundsurface = pygame.image.load("./tictactoe/tictactoe.png")
        # call the pygameapp base initializer, using the size of the image
        super(TTTApp, self).__init__(backgroundsurface.get_size(), False, "Tic Tac Toe")
        # initialize the font system
        font.init()
        # now override the background attribute of the application
        self.background = backgroundsurface
        # allow selecting who goes first
        self.gameover = True
        self.endmessage("[H]uman or [C]omputer first?")
        self.awaitingupdate = True

    def _physicaltological(self, physicalcoordinates):
        """
        Convert screen coordinates to logical coordinates
        """
        mapcoordinates = lambda physical, screensize: physical * 3 // screensize
        return list(map(mapcoordinates, physicalcoordinates, self.screensize))

    def _logicaltophysical(self, logicalcoordinates):
        """
        Convert logical coordinates to screen coordinates
        """
        mapcoordinates = lambda logical, screensize: logical*(screensize/3) + screensize/6
        return list(map(mapcoordinates, logicalcoordinates, self.screensize))
        #return [mapcoordinates(logical,size) for (logical,size) in zip(logicalcoordinates, self.screensize)]

    def newgame(self, firstplayer):
        """
        Set up for a new game. Accepts identity of first player as 'X' or 'O'
        """
        # now create a console TicTacToe game object.
        if firstplayer == 'O':
            start = -1
            self.humanmove = False
        else:
            start = 1
            self.humanmove = True
        self.tttposition = SuperTTTPosition([0,0,0,0,0,0,0,0,0], start)
        # keep track of the game state
        self.gameover = False
        # make sure there are no sprites to display
        self.spritegroup.empty()
        # track whether a screen update is pending
        self.awaitingupdate = True


    def drawmove(self, XO, logicalcoordinates):
        """
        Define a move for 'X' or 'O', to coordinates in X,Y space where
        X and Y are in the range 0 to 2
        """
        # Create a sprite and add it to the sprite group
        TTTXO(XO, self._logicaltophysical(logicalcoordinates), self.spritegroup)
        # Something needs to be drawn
        self.awaitingupdate = True

    def endmessage(self, message):
        """
        Generate a message sprite with the desired message
        """
        # Create a sprite and add it to the sprite group
        TTTMessage(message, (self.screensize[0]//2, self.screensize[1]*4//5), self.spritegroup)

    def handle_event(self, event):
        """
        Tic Tac Toe is driven entirely by actions from the user! This method
        will be called repeatedly and will accept user input, if appropriate
        or calculate the computer move, if appropriate.
        """
        # It is ALWAYS time to accept a human move, unless the game is OVER
        if not self.gameover:
            if self.humanmove and event.type == MOUSEBUTTONDOWN and event.button == 1:
                humanmove = self._physicaltological(event.pos)
                possiblemoves = self.tttposition.possiblemoves()
                # get a new Tic Tac Toe position object based on the human move
                desiredposition = self.tttposition.setmove(humanmove)
                if desiredposition in possiblemoves:
                    self.tttposition = desiredposition
                    self.gameover = self.tttposition.checkwin()
                    self.humanmove = False
                    ttt.drawmove('x', humanmove)
                    if self.gameover:
                        self.endmessage('You win! Press H or C.')
        else:   # Game is over.. look for key press for a new game
            if event.type == KEYDOWN:
                if event.unicode.upper() == u'H':
                    self.newgame('X')
                elif event.unicode.upper() == u'C':
                    self.newgame('O')
                elif event.unicode.upper() == u'Q' or event.key == K_ESCAPE: # escape or Q
                    pygame.event.post(pygame.event.Event(QUIT))
        return True
    
    def poll(self):
        """
        Periodic processing is used to generate computer move. This method
        is automatically called by the base PygameApp class.
        """
        # only process the computer move if the human's move isn't waiting to draw
        if not self.awaitingupdate:
            # if the game is on and it's the computer's move...
            if not self.gameover and not self.humanmove:
                # get a new Tic Tac Toe position object from the computer's move
                newposition = self.tttposition.autonextmove()
                if newposition:
                    # get a list of moves that are new or different from the previous
                    computermoves = (newposition - self.tttposition).positionlist()
                    # there should be only one thing in the list: the computer's move coordinates
                    ttt.drawmove('o', computermoves[0])
                    self.gameover = newposition.checkwin()
                    if self.gameover:
                        self.endmessage('I win! Press H or C')
                    elif not newposition.possiblemoves():
                        self.gameover = True
                        self.endmessage('Draw! Press H or C')
                    self.humanmove = True
                else:  # draw game
                    self.gameover = True
                    self.endmessage('Draw! Press H or C')
                # save the current board position
                self.tttposition = newposition
                # clean out the event queue in case the user has been banging the keyboard
                pygame.event.clear()
        else:
            self.awaitingupdate = False

# Run the Tic Tac Toe app
if __name__ == '__main__':
    ttt = TTTApp()
    ttt.run()
