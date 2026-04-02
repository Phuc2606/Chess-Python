import pygame
import chess
import time
from gui import draw_board, draw_pieces, draw_moves, SQ_SIZE
from node import Node
from mcts import mcts

pygame.init()

WIDTH = 640
screen = pygame.display.set_mode((WIDTH, WIDTH))
font = pygame.font.Font(None, 72)

board = chess.Board()

pieces = {}

names = [
    "wp","bp","wr","br","wn","bn",
    "wb","bb","wq","bq","wk","bk"
]

for name in names:
    img = pygame.image.load(f"assets/{name}.svg")
    img = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
    pieces[name] = img

selected = None
legal_targets = []
running = True

message = None
message_color = (255, 255, 255)
message_time = 0

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and message is None:

            x, y = pygame.mouse.get_pos()

            col = x // SQ_SIZE
            row = y // SQ_SIZE

            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)

            if selected is None:
                if piece and piece.color == board.turn:
                    selected = square
                    legal_targets = [
                        move.to_square
                        for move in board.legal_moves
                        if move.from_square == selected
                    ]

            else:
                piece = board.piece_at(selected)

                if piece and piece.piece_type == chess.PAWN:
                    if (piece.color == chess.WHITE and chess.square_rank(square) == 7) or \
                       (piece.color == chess.BLACK and chess.square_rank(square) == 0):

                        move = chess.Move(selected, square, promotion=chess.QUEEN)
                    else:
                        move = chess.Move(selected, square)
                else:
                    move = chess.Move(selected, square)

                if move in board.legal_moves:
                    board.push(move)

                    if board.is_game_over():
                        result = board.result()
                        if result == "1-0":
                            message = "WHITE WIN"
                            message_color = (0, 255, 0)
                        elif result == "0-1":
                            message = "BLACK WIN"
                            message_color = (255, 0, 0)
                        else:
                            message = "DRAW"
                            message_color = (255, 255, 255)
                        message_time = time.time()
                        selected = None
                        legal_targets = []
                        continue

                    root = Node(board.copy(), player=board.turn)
                    best = mcts(root, 300)

                    if best:
                        board.push(best.move)

                        if board.is_game_over():
                            result = board.result()
                            if result == "1-0":
                                message = "WHITE WIN"
                                message_color = (0, 255, 0)
                            elif result == "0-1":
                                message = "BLACK WIN"
                                message_color = (255, 0, 0)
                            else:
                                message = "DRAW"
                                message_color = (255, 255, 255)
                            message_time = time.time()

                selected = None
                legal_targets = []

    draw_board(screen)
    draw_moves(screen, legal_targets)
    draw_pieces(screen, board, pieces)

    if message:
        text = font.render(message, True, message_color)
        rect = text.get_rect(center=(WIDTH // 2, WIDTH // 2))
        screen.blit(text, rect)

        if time.time() - message_time > 3:
            board = chess.Board()
            selected = None
            legal_targets = []
            message = None

    pygame.display.flip()