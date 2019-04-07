# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random
import time
import pygame
import sys
from pygame.locals import *

# SCORE STUFF 
#  maybe lets put these into a JSON obj so we can make them into an array n shit?
HEIGHT = -0.5
HOLE = -5.0
TOUCHPIECE = 0.1
TOUCHWALL = 0.1
TOUCHFLOOR = 0.5
CLEARLINE = 1.2

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0,   0,   0)
RED = (155,   0,   0)
LIGHTRED = (175,  20,  20)
GREEN = (0, 155,   0)
LIGHTGREEN = (20, 175,  20)
BLUE = (0,   0, 155)
LIGHTBLUE = (20,  20, 175)
YELLOW = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)  # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetromino')
    print("START")
    while True:  # game loop
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        # pygame.mixer.music.play(-1, 0.0)
        # runGame()
        runAI()
        # pygame.mixer.music.stop()
        showTextScreen('Game Over')


def runAI():

    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False  # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    totalScore = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    num = 0

    while True:  # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()  # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return  # can't fit a new piece on the board, so game over

        checkForQuit()
        # print(board)
        surfaceLevel = getSurface(board)
        print(surfaceLevel)
        bestMovement = calculateBestMove(surfaceLevel, fallingPiece, board)
        print("BEST MOVE", bestMovement)
        print("Actualy rotation", fallingPiece['rotation'])
        pyGameEvents = calculateMoves(fallingPiece, bestMovement['index'], bestMovement['rotation'])
        print(pyGameEvents)
        for event in pyGameEvents:  # event handling loop
            # print(event)
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')  # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                    # if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                    #     fallingPiece['x'] -= 1
                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()
                    # if movingRight and isValidPosition(board, fallingPiece, adjX=1):
                    #     fallingPiece['x'] += 1
                    

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (
                        fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (
                            fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q):  # rotate the other direction
                    fallingPiece['rotation'] = (
                        fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (
                            fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                #UNCOMMENT ME
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1
            pyGameEvents.pop(0)

        # handle moving the piece because of user input
        # if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
        #     if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
        #         fallingPiece['x'] -= 1
        #     elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
        #         fallingPiece['x'] += 1
            # lastMoveSidewaysTime = time.time()
        # if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
        #     fallingPiece['y'] += 1
        #     lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)

                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def calculateMoves(piece, x, y):
    # x y would be the right most bottom cornor of where the piece is
    current = piece['x'] + 1
    moves = []
    leftEvent = pygame.event.Event(2, {'scancode': 123, 'key': K_LEFT, 'unicode': u'\uf702', 'mod': 0})
    rightEvent = pygame.event.Event(pygame.KEYDOWN, {'key':pygame.K_RIGHT})
    spaceEvent = pygame.event.Event(2, {'scancode': 35, 'key': K_DOWN, 'unicode': u'p', 'mod': 0})
    rotate = pygame.event.Event(2, {'key': K_UP})
    # print("x: %s to go: %s\n" % (piece['x'], x))

    if (piece['x'] > x):
        numLefts = piece['x'] - x
        # numLefts = numLefts - 2
        for x in range(0, numLefts):
            # print("LEFT?")
            moves.append(leftEvent)
    elif (piece['x'] < x):
        # numRights = 2
        numRights =  x - piece['x']
        # print("num rights", numRights)
        for x in range(0, numRights):
            # print("RIGHT:")
            moves.append(rightEvent)

    rotation = piece['rotation']
    numRotate = y - rotation
    if (numRotate < 0): 
        numRotate = -numRotate
    if (rotation != y):
        for x in range(0, numRotate - 1):
            moves.append(rotate)

    moves.append(spaceEvent)

    return moves


def getSurface(board):
    surfaceLevel = [19, 19, 19, 19, 19, 19, 19, 19, 19, 19]
    i = -1
    for row in board:
        i += 1
        for index in row:
            if index is not '.':
                surfaceLevel[i] = row.index(index)
                break
    return surfaceLevel


def calculateBestMove(surface, piece, board):
    # print(piece["shape"])
    if piece['shape'] is 'I':
        options = []
        for idx, val in enumerate(surface):
            if (idx <= 6 and val == surface[idx + 1] == surface[idx + 2] == surface[idx + 3]):
                shapeList = [ (val, idx), (val, idx + 1), (val, idx + 2), (val, idx + 3)]
                indexTo = idx - 2
                option = { 'shapeList': shapeList,
                        'index': indexTo,
                        'rotation': 1,
                        'score': 0 }
                options.append(option)
            shapeList = [ (val, idx), (val - 1, idx), (val - 2, idx), (val - 3, idx)]
            indexTo = idx - 2
            option = { 'shapeList': shapeList,
                        'index': indexTo,
                        'rotation': 0,
                        'score': 0 }
            options.append(option)
        return getMaxScore(options, board)
    elif piece['shape'] is 'O':
        options = []
        for idx, val in enumerate(surface):
            if (val == surface[idx - 1]):
                shapeList = [ (val, idx - 1), (val, idx), (val - 1, idx - 1), (val - 1, idx)]
                indexTo = idx - 2
                option = { 'shapeList': shapeList,
                            'index': indexTo,
                            'rotation': piece['rotation'],
                            'score': 0 }
                options.append(option)
        return getMaxScore(options, board)
    elif piece['shape'] == 'S':
        options = []
        for idx, val in enumerate(surface):
            if (idx <= 7):
                sol = (val, idx - 2)
                shapeList = [(val, idx), (val, idx + 1), (val - 1, idx + 1), (val - 1, idx + 2)]
                indexTo = idx - 2
                option = { 'shapeList': shapeList,
                            'index': indexTo,
                            'rotation': 0,
                            'score': 0 }
                options.append(option)
            if (idx <= 8 and val != 19):
                sol = (val, idx - 2)
                shapeList = [(val, idx), (val - 1, idx), (val, idx + 1), (val + 1, idx + 1)]  
                indexTo = idx - 2   
                option = { 'shapeList': shapeList,
                            'index': indexTo,
                            'rotation': 1,
                            'score': 0 }
                options.append(option)
        print("options", options)
        return getMaxScore(options, board)
    elif piece['shape'] == 'T':
        options = []
        for idx, val in enumerate(surface):
            if (idx <= 7 and val == surface[idx + 1] == surface[idx + 2]):
                shapeList = [ (val, idx), (val, idx + 1), (val - 1, idx + 1), (val, idx + 2)]
                option = { 'shapeList': shapeList,
                            'index': idx - 1,
                            'rotation': 0,
                            'score': 0 }
                options.append(option)
            if (idx <= 8 and val == surface[idx + 1] + 1):
                shapeList = [ (val, idx), (val - 1, idx), (val - 2, idx), (val - 1, idx + 1)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 1,
                            'score': 0 }
                options.append(option)
            if (idx <= 7 and (val == surface[idx + 1] - 1 or val == surface[idx + 1] + 1)):
                shapeList = [ (val - 1, idx), (val - 1, idx + 1), (val - 1, idx + 2), (val, idx + 1)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 2,
                            'score': 0 }
                options.append(option)
            if (idx <= 8 and val == surface[idx + 1] - 1):
                option = { 'shapeList': [(val, idx), (val - 1, idx), (val - 2, idx), (val - 1, idx - 1)],
                            'index': idx - 2,
                            'rotation': 3,
                            'score': 0 }
                options.append(option)
        return getMaxScore(options, board)
    elif piece['shape'] == 'Z':
        options = []
        for idx, val in enumerate(surface):
            print("idx val: %s %s" % (idx, val))
            if (idx <= 7):
                shapeList = [(val, idx - 1), (val - 1, idx - 1), (val - 1, idx), (val - 2, idx)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 1,
                            'score': 0 }
                options.append(option)
            if (idx <= 8): 
                shapeList = [(val - 1, idx - 1), (val - 1, idx), (val, idx), (val, idx + 1)]
                option = { 'shapeList': shapeList,
                            'index': idx - 1,
                            'rotation': 0,
                            'score': 0 }
                options.append(option)
        return getMaxScore(options, board)
    elif piece['shape'] == 'J':
        options = []
        for idx, val in enumerate(surface):
            print("idx val: %s %s" % (idx, val))
            if (idx <= 7):
                shapeList = [(val, idx), (val - 1, idx), (val, idx + 1), (val, idx + 2)]
                option = { 'shapeList': shapeList,
                            'index': idx - 1,
                            'rotation': 0,
                            'score': 0 }
                options.append(option)
            if (idx <= 8):
                shapeList = [(val, idx), (val - 1, idx), (val - 2, idx), (val - 2, idx + 1)] 
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 1,
                            'score': 0 }
                options.append(option)
            if (idx <= 7): 
                shapeList = [(val - 1, idx - 2), (val - 1, idx - 1), (val - 1, idx), (val, idx)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 2,
                            'score': 0 }
                options.append(option)
            if (idx <= 8): 
                shapeList = [(val, idx - 1), (val, idx), (val - 1, idx), (val - 2, idx)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 3,
                            'score': 0 }
                options.append(option)
        return getMaxScore(options, board)     
    elif piece['shape'] == 'L':
        options = []
        for idx, val in enumerate(surface):
            if (idx <= 8):
                shapeList = [ (val, idx - 2), (val, idx - 1), (val, idx), (val, idx - 1)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 0,
                            'score': 0 }
                options.append(option)
                
                shapeList = [ (val - 1, idx - 2), (val - 1, idx - 1), (val - 1, idx), (val, idx - 2)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 2,
                            'score': 0 }
                options.append(option)
            if (idx <= 7):
                shapeList = [ (val - 2, idx), (val - 1, idx), (val, idx), (val, idx + 2) ]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 1,
                            'score': 0 }
                options.append(option)
                
                shapeList = [ (val - 2, idx -1), (val -2, idx), (val - 1, idx), (val, idx)]
                option = { 'shapeList': shapeList,
                            'index': idx - 2,
                            'rotation': 3,
                            'score': 0 }
                options.append(option)
        return getMaxScore(options, board)     

def heightPeanlizer(piece):
  pieceIndex = []
  for x in piece:
    pieceIndex.append(x[0])
  
  return len(pieceIndex)

def doesCreateHole(piece, board):
  pieceIndex = []
  # print(board[0])
  for x in piece:
    pieceIndex.append(x[1])

  print("piece", pieceIndex)
  print("board", board)
  indexFits = 0
  for row in board:
    for index in row:
      # print(index)
      for piece in pieceIndex:
        if (row[piece] == "."):
          indexFits = board.index(row)
        else:
          indexFits = 0 

  print("index", indexFits)

  print("board", board[indexFits])
  for index in board[indexFits]:
    for piece in pieceIndex:
      if board[indexFits][piece] == ".":
        board[indexFits][piece] = "T"
  
  for row in range(0, 1):
    for index in range(0, 10):
      if board[row][index] is "." and board[row + 1][index] is "T":
        return True

  return False

def doesClearLine(piece, board):
    pieceIndex = []
    for x in piece:
        pieceIndex.append(x[1])
    for row in board:
        for index in row:
            for piece in pieceIndex:
                if (board[0][piece] == "."):
                    board[0][piece] = "T"
    for row in board:
        for index in row:
            if index is ".":
                return False
    return True 

def touchWall(shapeList):
    for shape in shapeList:
        if shape[1] is 0 or shape[1] is 9:
            return True
    return False

def touchFloor(shapeList):
  for shape in shapeList:
    if shape[0] is 19:
      return True
  return False  

def getMaxScore(options, board):
    for option in options:
        score = 0
        reducedBoard = getReducedboard(board, option['shapeList'])
        if touchWall(option['shapeList']) is True:
            score += TOUCHWALL
        if touchFloor(option['shapeList']) is True:
            score += TOUCHFLOOR
        if doesClearLine(option['shapeList'], reducedBoard) is True: 
            score += LINECLEAR
        score += HOLE * doesCreateHole(option['shapeList'], getReducedboard(board, option['shapeList']))
        score += HEIGHT * heightPeanlizer(option['shapeList'])
        option['score'] = score
    
    biggestOption = options[0]
    for option in options:
        if biggestOption['score'] <= option['score']:
            biggestOption = option
    return biggestOption


# Function that takes the board and where the piece is going to go
# and returns the the board but only for the rows where the piece will be!
def getReducedboard(board, piece):
    pieceList = []
    smolBoard = []
    for x, idx in piece:
        if x not in pieceList:
            pieceList.append(x)

    # print("piecelist", pieceList)
    pieceList.append(pieceList[-1] - 1)
    for y in range(0, len(pieceList)):
        individBoard = []
        for x in range(0, 10):
            # print(board[x][pieceList[y]])
            individBoard.append(board[x][pieceList[y]])
        # print(individBoard)
        smolBoard.append(individBoard)
    # print("smol", smolBoard)
    return smolBoard

def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False  # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    while True:  # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()  # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return  # can't fit a new piece on the board, so game over
        # print(fallingPiece['shape'], fallingPiece['x'], fallingPiece['y'])
        # print(board)

        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')  # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (
                        fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (
                            fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q):  # rotate the other direction
                    fallingPiece['rotation'] = (
                        fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (
                            fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1
        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs(
        'Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq


def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    # shape = "L"
    # print("SHAPE %s" % shape)
    # random.randint(0, len(PIECES[shape]) - 1)
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2,  # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True


def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1  # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1  # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(
        DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(
        DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7,
                                                (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN,
                                            BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx +
                        (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
    main()
