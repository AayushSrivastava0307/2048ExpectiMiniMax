from random import random, choice

#directions 
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)
directions = [LEFT, UP, RIGHT, DOWN]

class Board:
    #board representation  
    def __init__(self, boardSize=4):
        self.boardSize = boardSize
        self.board = [[0] * boardSize for _ in range(boardSize)]
        self.score = 0
        self.moveCount = 0  # track moves
        self.addTile()
        self.addTile()

    def __str__(self):
        return "\n".join("\t".join(map(str, row)) for row in self.board)

    def __getitem__(self, key):
        return self.board[key]

    def getOpenTiles(self):
        #empty tiles list
        return [(i, j) for i in range(self.boardSize) for j in range(self.boardSize) if self.board[i][j] == 0]

    def addTile(self, pos=None, tileToAdd=0):
        #10% of 4 addition to board and 90% of 2 free to change
        if pos is None:
            openTiles = self.getOpenTiles()
            if not openTiles:
                return
            pos = choice(openTiles)

        if tileToAdd == 0:
            tileToAdd = 2 if random() < 0.9 else 4

        self.board[pos[0]][pos[1]] = tileToAdd

    def move(self, direction, addNextTile=True):
        #sliding and merging 
        hadCollision = [[False] * self.boardSize for _ in range(self.boardSize)]
        hadMovement = False
        moveScore = 0

        # determine iteraction based on direction
        if direction[1] > 0:
            xRange = range(self.boardSize - 1, -1, -1)
        else:
            xRange = range(self.boardSize)
        if direction[0] > 0:
            yRange = range(self.boardSize - 1, -1, -1)
        else:
            yRange = range(self.boardSize)

        for y in yRange:
            for x in xRange:
                if self.board[y][x] == 0:
                    continue

                curY, curX = y, x
                # move in the direction ie slide
                while True:
                    nextY = curY + direction[0]
                    nextX = curX + direction[1]
                    if not (0 <= nextY < self.boardSize and 0 <= nextX < self.boardSize):
                        break
                    if self.board[nextY][nextX] != 0:
                        break
                    curY, curX = nextY, nextX

                # merge it 
                nextY = curY + direction[0]
                nextX = curX + direction[1]
                if (0 <= nextY < self.boardSize and 0 <= nextX < self.boardSize and
                        self.board[nextY][nextX] == self.board[y][x] and not hadCollision[nextY][nextX]):
                    hadCollision[nextY][nextX] = True
                    mergeValue = self.board[y][x] * 2
                    self.board[nextY][nextX] = mergeValue
                    moveScore += mergeValue
                    self.board[y][x] = 0
                    hadMovement = True
                # just slide no merge 
                elif (curY, curX) != (y, x) and self.board[curY][curX] == 0:
                    self.board[curY][curX] = self.board[y][x]
                    self.board[y][x] = 0
                    hadMovement = True

        self.score += moveScore
        if hadMovement:
            self.moveCount += 1  # track move count
            if addNextTile:
                self.addTile()
        return moveScore, hadMovement

    def check2048(self):
        #check if 2048 tile is present
        return any(2048 in row for row in self.board)

    def checkLoss(self):
        #ie if no legal moves exist
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if self.board[y][x] == 0:
                    return False
                for direction in directions:
                    newY, newX = y + direction[0], x + direction[1]
                    if (0 <= newY < self.boardSize and 0 <= newX < self.boardSize and
                            self.board[y][x] == self.board[newY][newX]):
                        return False
        return True
