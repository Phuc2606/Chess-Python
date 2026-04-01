import pygame
import chess
from gui import draw_board, draw_pieces, draw_moves, SQ_SIZE
from node import Node
from mcts import mcts

pygame.init()

WIDTH = 640
screen = pygame.display.set_mode((WIDTH,WIDTH))

board = chess.Board()

pieces = {}

names = [
"wp","bp","wr","br","wn","bn",
"wb","bb","wq","bq","wk","bk"
]

for name in names:
    img = pygame.image.load(f"assets/{name}.svg")
    img = pygame.transform.scale(img,(SQ_SIZE,SQ_SIZE))
    pieces[name] = img
selected = None
running = True
legal_targets = []
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x,y = pygame.mouse.get_pos()

            col = x//SQ_SIZE
            row = y//SQ_SIZE

            square = chess.square(col,7-row)

            if selected is None:
                piece = board.piece_at(square)
                if piece and piece.color == board.turn:
                    selected = square
                    legal_targets = []
                    for move in board.legal_moves:
                        if move.from_square == selected:
                            legal_targets.append(move.to_square)

            else:

                move = chess.Move(selected,square)

                if move in board.legal_moves:

                    board.push(move)

                    root = Node(board)
                    best = mcts(root,150)

                    board.push(best.move)

                selected = None

    draw_board(screen)
    draw_moves(screen,legal_targets)
    draw_pieces(screen,board,pieces)

    pygame.display.flip()