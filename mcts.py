import math
import random
import chess
from node import Node

def uct(node, C=1.4):
    if node.visits == 0:
        return float("inf")

    return (node.wins / node.visits) + C * math.sqrt(
        math.log(node.parent.visits + 1) / node.visits
    )

def expand(node):
    move = node.untried_moves.pop()

    new_board = node.board.copy()
    new_board.push(move)

    child = Node(new_board, node, move, not node.player)
    node.children.append(child)

    return child

def simulate(board, player):
    board = board.copy()

    for _ in range(50):
        if board.is_game_over():
            break

        moves = list(board.legal_moves)
        capture_moves = [m for m in moves if board.is_capture(m)]

        move = random.choice(capture_moves if capture_moves else moves)
        board.push(move)

    if not board.is_game_over():
        return 0

    result = board.result()

    if result == "1-0":
        return 1 if player == chess.WHITE else -1
    elif result == "0-1":
        return 1 if player == chess.BLACK else -1
    else:
        return 0

def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        result = -result
        node = node.parent

def mcts(root, simulations=300):

    for _ in range(simulations):

        node = root

        while node.children and not node.untried_moves:
            node = max(node.children, key=uct)

        if node.untried_moves:
            node = expand(node)

        result = simulate(node.board, root.player)
        backpropagate(node, result)

    if not root.children:
        return None

    return max(root.children, key=lambda c: c.visits)