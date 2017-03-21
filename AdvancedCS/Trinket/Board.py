# python 2
#
# Problem Set 2, Problem 1
# Name: EZ-Rob
#

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
        else:
            row = -1

            for i in range(self.height):
                if self.data[i][c] == ' ':
                    row += 1

            if row >= self.height:
                return False
            else:
                return True

    def isFull(self):
        full = True

        for i in range(self.width):
            for j in range(self.height):
                if self.data[i][j] == ' ':
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
                   D[row][col+1] == ox and \
                   D[row][col+2] == ox and \
                   D[row][col+3] == ox:
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
