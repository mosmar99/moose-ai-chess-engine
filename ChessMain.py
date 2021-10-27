"""
This is our main driver fail. It will be responsible for handling user input and displaying the current 
GameState information.
"""

import pygame as p
import ChessEngine # https://csatlas.com/python-import-file-module/

WIDTH = HEIGHT = 512
DIMENSION = 8 # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly once in the main.
"""
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bR', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wp']'

"""
The main driver for our code. This will handle user input and updating graphics
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made, false until valid move is made

    loadImages() # only do this once, before the while loop
    running = True
    sqSelected = () # n,o squares are selected initially, keep rack of the last click of the user (tuple, (r,c))
    playerClicks = [] # keep track of player clicks (two tuples: [(6,4),(4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): # the user clicked the same square twice
                    sqSelected = () # deselect
                    playerClicks = [] # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # we append for both 1st and 2nd clicks
                if len(playerClicks) == 2: # after 2nd click  
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () # reset user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            # key handlers
            elif e.type ==  p.KEYDOWN:
                if e.key == p.K_LEFT: # undo when 'left-arrow' is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Responsible for all graphics within a current game state.
"""
def drawGameState(screen, gs):
    drawBoard(screen) # draws squares on board
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw pieces on top of those squares

"""
Draw the squares on the board. The top left square is always light.
"""
def drawBoard(screen):
    colors = [p.Color(232, 235, 239), p.Color(125, 135, 150)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draws from top left

"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece],  p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()