import math
import random
from node import Node

def uct(node, C=1.4):

    if node.visits == 0:
        return float("inf")

    return (node.wins/node.visits) + C * math.sqrt(
        math.log(node.parent.visits) / node.visits
    )

def expand(node):

    move = node.untried_moves.pop()

    new_board = node.board.copy()
    new_board.push(move)

    child = Node(new_board, node, move)

    node.children.append(child)

    return child

def simulate(board):

    board = board.copy()

    while not board.is_game_over():

        moves = list(board.legal_moves)
        move = random.choice(moves)

        board.push(move)

    result = board.result()

    if result == "1-0":
        return 1
    elif result == "0-1":
        return -1
    else:
        return 0

def backpropagate(node, result):

    while node:
        node.visits += 1
        node.wins += result
        node = node.parent

def mcts(root, simulations=500):

    for _ in range(simulations):

        node = root

        while node.children and not node.untried_moves:
            node = max(node.children, key=uct)

        if node.untried_moves:
            node = expand(node)

        result = simulate(node.board)

        backpropagate(node, result)

    return max(root.children, key=lambda c: c.visits)