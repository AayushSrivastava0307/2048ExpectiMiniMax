import sys
import pygame
import Model
from math import log2
from ExpectiMiniMax import getNextBestMoveExpectiminimax
import multiprocessing as mp

# game settings
ai_enabled = False
depth = 2
boardSize = 4

# ui settings
size = width, height = 480, 500
playRegion = (480, 480)
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_COLOR = (82, 52, 42)
DEFAULT_TILE_COLOR = (232, 232, 232)

def drawBoard(screen, board, tileFont, scoreFont):
    screen.fill(BLACK)
    for i in range(board.boardSize):
        for j in range(board.boardSize):
            color = DEFAULT_TILE_COLOR
            numberText = ''
            
            tileValue = board.board[i][j]
            if tileValue != 0:
                gComponent = 235 - log2(tileValue)*((235 - 52) / (board.boardSize ** 2))
                color = (235, int(gComponent), 52)
                numberText = str(tileValue)
                
            rect = pygame.Rect(j * playRegion[0] / board.boardSize,
                               i * playRegion[1] / board.boardSize,
                               playRegion[0] / board.boardSize,
                               playRegion[1] / board.boardSize)
            
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, FONT_COLOR, rect, 1)
            
            fontImage = tileFont.render(numberText, True, FONT_COLOR)
            if fontImage.get_width() > playRegion[0] / board.boardSize:
                scaledWidth = playRegion[0] / board.boardSize
                scaledHeight = fontImage.get_height() / fontImage.get_width() * scaledWidth
                fontImage = pygame.transform.scale(fontImage, (int(scaledWidth), int(scaledHeight)))
            
            screen.blit(fontImage, (
                j * playRegion[0] / board.boardSize + (playRegion[0] / board.boardSize - fontImage.get_width()) / 2,
                i * playRegion[1] / board.boardSize + (playRegion[1] / board.boardSize - fontImage.get_height()) / 2
            ))
    
    scoreText = f"Score: {board.score:,}  Moves: {board.moveCount}  " + (f" Press Space [__] to enable AI" if (ai_enabled==False) else "")+(f" [AI enabled, depth={depth}]" if ai_enabled else "") 
    fontImage = scoreFont.render(scoreText, True, WHITE)
    screen.blit(fontImage, (1, playRegion[1] + 1))

def handleInput(event, board, pool):
    global ai_enabled

    if event.type == pygame.QUIT:
        pool.close()
        pool.terminate()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            board.move(Model.RIGHT)
        elif event.key == pygame.K_LEFT:
            board.move(Model.LEFT)
        elif event.key == pygame.K_UP:
            board.move(Model.UP)
        elif event.key == pygame.K_DOWN:
            board.move(Model.DOWN)
        elif event.key == pygame.K_r:
            board = Model.Board(boardSize)
        elif event.key == pygame.K_ESCAPE:
            pool.close()
            pool.terminate()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            ai_enabled = not ai_enabled

    return board

def gameLoop(screen, tileFont, scoreFont, pool):
    clock = pygame.time.Clock()
    board = Model.Board(boardSize)

    printed2048 = False #for showing no of moves if 2048 reached
    printedLoss = False #game over gg

    while True:
        for event in pygame.event.get():
            board = handleInput(event, board, pool)

        if ai_enabled and not board.checkLoss():
            nextMove = getNextBestMoveExpectiminimax(board, pool, depth)
            board.move(nextMove)

        if board.check2048() and not printed2048:
            print(f"2048 reached in {board.moveCount} moves.")
            printed2048 = True

        if board.checkLoss() and not printedLoss:
            print(f"No Legal Moves Left, GAME OVER!")
            printedLoss = True

        drawBoard(screen, board, tileFont, scoreFont)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    mp.freeze_support()
    mp.set_start_method('spawn')
    pool = mp.Pool(processes=4)

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("2048")
    tileFont = pygame.font.SysFont("", 72)
    scoreFont = pygame.font.SysFont("", 22)

    gameLoop(screen, tileFont, scoreFont, pool)
