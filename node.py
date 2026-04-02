class Node:
    def __init__(self, board, parent=None, move=None, player=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.player = player

        self.children = []
        self.visits = 0
        self.wins = 0

        self.untried_moves = list(board.legal_moves)