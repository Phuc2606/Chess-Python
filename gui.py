import pygame
import chess

WIDTH = 640
SQ_SIZE = WIDTH // 8

def draw_board(screen):

    colors = [(240,217,181),(181,136,99)]

    for r in range(8):
        for c in range(8):

            color = colors[(r+c)%2]

            pygame.draw.rect(
                screen,
                color,
                (c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE)
            )

def draw_pieces(screen,board,pieces):

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece:

            row = 7 - square//8
            col = square%8

            name = piece.symbol()

            key = ("w" if name.isupper() else "b") + name.lower()

            img = pieces[key]

            x = col * SQ_SIZE
            y = row * SQ_SIZE

            screen.blit(img,(x,y))

def draw_moves(screen,targets):
    SQ_SIZE = 80
    for sq in targets:

        col = sq % 8
        row = 7 - sq//8
        s = pygame.Surface((SQ_SIZE,SQ_SIZE),pygame.SRCALPHA)
        s.fill((0,255,0,80))
        screen.blit(s,(col*SQ_SIZE,row*SQ_SIZE))