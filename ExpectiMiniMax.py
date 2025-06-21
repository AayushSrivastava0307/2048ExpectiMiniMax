import Model
import copy

INF = 2**64
SnakeHeuristicWeights = [
    [2,    2**2, 2**3, 2**4],
    [2**8, 2**7, 2**6, 2**5],
    [2**9, 2**10,2**11,2**12],
    [2**16,2**15,2**14,2**13]
]

def snakeHeuristic(board):
    #evaluate the boards state and give it a heuristic value
    return sum(
        board[i][j] * SnakeHeuristicWeights[i][j]
        for i in range(board.boardSize)
        for j in range(board.boardSize)
    )

def getNextBestMoveExpectiminimax(board, pool, depth=2): #default to 2 depth
    # give best move by the heuristic
    bestScore = -INF
    bestNextMove = Model.directions[0]
    tasks = []
    
    for direction in Model.directions:
        simBoard = copy.deepcopy(board)
        _, moved = simBoard.move(direction, False)
        if not moved:
            continue
        tasks.append(pool.apply_async(expectiminimax, (simBoard, depth, direction)))
    
    for task in tasks:
        score_val, chosenDirection = task.get()
        if score_val >= bestScore:
            bestScore = score_val
            bestNextMove = chosenDirection

    return bestNextMove

def expectiminimax(board, depth, direction=None):
  
    # base cases
    if board.checkLoss():
        return -INF, direction
    if depth < 0:
        return snakeHeuristic(board), direction

    intDepth = int(depth)
    if depth != intDepth:
        # Maxs turn fractional depths 
        bestValue = -INF
        bestDirection = direction
        for move in Model.directions:
            simBoard = copy.deepcopy(board)
            score, moved = simBoard.move(move, False)
            if moved:
                value, _ = expectiminimax(simBoard, depth - 0.5, move)
                if value > bestValue:
                    bestValue = value
                    bestDirection = move
        return bestValue, bestDirection
    else:
        # Mins turn , avg over all tile placements
        openTiles = board.getOpenTiles()
        if not openTiles:
            return snakeHeuristic(board), direction

        averageValue = 0.0
        chance = 1.0 / len(openTiles)
        # place 2 in each posn 
        for pos in openTiles:
            board.addTile(pos, 2)
            value, _ = expectiminimax(board, depth - 0.5, direction)
            averageValue += chance * 0.9 * value
            board.addTile(pos, 0)  #backtrack

        # same for case of placing 4
        for pos in openTiles:
            board.addTile(pos, 4)
            value, _ = expectiminimax(board, depth - 0.5, direction)
            averageValue += chance * 0.1 * value
            board.addTile(pos, 0)   
            
        return averageValue, direction