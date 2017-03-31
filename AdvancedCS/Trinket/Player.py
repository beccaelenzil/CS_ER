from Board import Board
import random

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
            if scores[col] == 50.0:
                scores[col] = self.scoreBoard(b)
            b.delMove(col)

        return scores

    def nextMove(self, b):
        return self.tiebreakMove(self.scoresFor(b))
