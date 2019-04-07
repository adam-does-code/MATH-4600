# All my movement related functions will be here

import random
import time
import pygame
import sys
from pygame.locals import *

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

    for y in range(0, len(pieceList)):
        individBoard = []
        for x in range(0, 10):
            # print(board[x][pieceList[y]])
            individBoard.append(board[x][pieceList[y]])
        # print(individBoard)
        smolBoard.append(individBoard)
    # print(smolBoard)
    return smolBoard

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
    moves.append(spaceEvent)
    rotation = piece['rotation']
    if (rotation != y):
        moves.append(rotate)
        rotation += 1
    # print("moves: %s" % moves)
    return moves


## Scoring Related Functions
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