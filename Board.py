# File: Board.py
# Versions: Python 2.7.13
# Name: Ezra Robinson
# Date: 3/31/17
# Desc: Connect-four game with very basic AI
# Usage: create a board object, then player objects for the number of AI
#       players you want, then call playGame on the board passing in 'human'
#       or the AI Player objects as players

import random


class Board:
    """ a datatype representing a C4 board
        with an arbitrary number of rows and cols
    """

    def __init__( self, width, height ):
        """ the constructor for objects of type Board """

        self.width = width
        self.height = height

        W = self.width
        H = self.height

        self.data = [ [' ']*W for row in range(H) ]

    def __repr__(self):
        """ this method returns a string representation
            for an object of type Board
        """
        W = self.width
        H = self.height

        s = ''   # the string to return
        for row in range(0,H):
            s += '|'
            for col in range(0,W):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*W+1) * '-'    # bottom of the board
        s += '\n'

        x = -1
        for i in range(W):
            if x == 9:
                x = 0
                s += " " +str(x)
            else:
                x+= 1
                s += " " + str(x)

        return s       # the board is complete, return it

    def addMove(self, col, ox):
        row = -1

        for i in range(self.height):
            if self.data[i][col] == ' ':
                row += 1

        self.data[row][col] = ox

    def clear(self):
        W = self.width
        H = self.height

        self.data = [[' ']*W for row in range(H)]

    def setBoard(self, moveString):
        """ takes in a string of columns and places
            alternating checkers in those columns,
            starting with 'X'

            For example, call b.setBoard('012345')
            to see 'X's and 'O's alternate on the
            bottom row, or b.setBoard('000000') to
            see them alternate in the left column.

            moveString must be a string of integers
        """
        nextCh = 'X'   # start by playing 'X'
        for colString in moveString:
            col = int(colString)
            if 0 <= col <= self.width:
                self.addMove(col, nextCh)
            if nextCh == 'X': nextCh = 'O'
            else: nextCh = 'X'

    def allowsMove(self, c):
        if c >= self.width or c < 0:
            return False
        elif self.data[0][c] != ' ':
            return False
        else:
            return True

    def isFull(self):
        full = True

        for i in range(self.width):
            for j in range(self.height):
                if self.data[j][i] == ' ':
                    full = False

        return full

    def delMove(self, col):
        row = 0

        for i in range(self.height):
            if self.data[i][col] == ' ':
                row += 1

        self.data[row][col] = ' '

    def winsFor(self, ox):
        H = self.height
        W = self.width
        D = self.data
        wins = False

        # check for horizontal wins
        for row in range(0,H):
            for col in range(0,W-3):
                if D[row][col] == ox and \
                   D[row][col+1] == ox and \
                   D[row][col+2] == ox and \
                   D[row][col+3] == ox:
                    wins = True

        # check for vertical wins
        for col in range(0,W):
            for row in range(0,H-3):
                if D[row][col] == ox and \
                   D[row+1][col] == ox and \
                   D[row+2][col] == ox and \
                   D[row+3][col] == ox:
                    wins = True

        # check for down diagonals
        for row in range(0,H-3):
            for col in range(0,W-3):
                if D[row][col] == ox and \
                   D[row+1][col+1] == ox and \
                   D[row+2][col+2] == ox and \
                   D[row+3][col+3] == ox:
                    wins = True

        # check for up diagonals
        for row in range(3,H):
            for col in range(0,W-3):
                if D[row][col] == ox and \
                   D[row-1][col+1] == ox and \
                   D[row-2][col+2] == ox and \
                   D[row-3][col+3] == ox:
                    wins = True

        return wins

    def hostGame(self):
        done = False
        won = False
        self.clear()

        print "Welcome to Gonnegt Fore!"

        while not done:

            players = ['X', 'O']

            for activePlayer in players:
                print self.__repr__()

                print activePlayer + "\'s Turn:"

                col = int(raw_input("What column would you like to play in?"))
                while not self.allowsMove(col):
                    col = int(raw_input("You cannot play in column " + str(col) + ".\nWhat column would you like to play in?"))

                self.addMove(col, activePlayer)

                if self.winsFor(activePlayer):
                    print activePlayer + "s win!"
                    done = True
                    won = True
                    print self.__repr__()

                if self.isFull() and not won:
                    print "The board is full and nobody has won."
                    done = True

    def playGame(self, px, po):
        done = False
        won = False
        self.clear()

        print "Welcome to Gonnegt Fore!"

        while not done:

            players = [px, po]

            for activePlayer in players:

                if not won:

                    print self.__repr__()

                    if activePlayer == px:
                        playerLetter = 'X'
                    elif activePlayer == po:
                        playerLetter = 'O'

                    print '\n'

                    if activePlayer == 'human':
                        print playerLetter + "\'s Turn:"

                        col = int(raw_input("What column would you like to play in?"))
                        while not self.allowsMove(col):
                            col = int(raw_input("You cannot play in column " + str(col) + ".\nWhat column would you like to play in?"))

                        self.addMove(col, playerLetter)
                    else:
                        col = activePlayer.nextMove(self)
                        print "The AI played in column " + str(col)
                        self.addMove(col, playerLetter)

                    if self.winsFor(playerLetter):
                        print self.__repr__()
                        print playerLetter + "s win!"
                        done = True
                        won = True

                    if self.isFull() and not won:
                        print "The board is full and nobody has won."
                        done = True

class Player:

    def __init__(self, ox, tbt, ply):
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        if self.ox == 'X':
            return 'O'
        else:
            return 'X'

    def scoreBoard(self, b):
        if b.winsFor(self.ox):
            return 100.0
        elif b.winsFor(self.oppCh()):
            return 0.0
        else:
            return 50.0

    def tiebreakMove(self, scores):

        maxIndices = []
        for i in range(len(scores)):
            if scores[i] == max(scores):
                maxIndices.append(i)

        if len(maxIndices) > 1:
            if self.tbt == 'LEFT':
                return maxIndices[0]
            elif self.tbt == 'RIGHT':
                return maxIndices[len(maxIndices)-1]
            else:
                return maxIndices[random.randrange(len(maxIndices))]
        else:
            return maxIndices[0]

    def scoresFor(self, b):
        scores = []

        for col in range(b.width):
            b.addMove(col, self.ox)
            if b.allowsMove(col):
                if self.scoreBoard(b) == 100.0:
                    scores.append(self.scoreBoard(b))
                else:
                    b.addMove(col, self.oppCh())
                    scores.append(self.scoreBoard(b))
                    b.delMove(col)
            else:
                scores.append(-1)
            b.delMove(col)

        for col in range(b.width):
            b.addMove(col, self.oppCh())
            if scores[col] != 100.0:
                # scores[col] = self.scoreBoard(b)
                if b.winsFor(self.oppCh()):
                    scores[col] = 75.0
            b.delMove(col)

        return scores

    def nextMove(self, b):
        return self.tiebreakMove(self.scoresFor(b))

def test():
    b = Board(7,6)
    p = Player('X', 'RANDOM', 4)
    b.playGame(p,'human')
    print b
