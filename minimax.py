
from knightschess import KnightsChess
from math import inf
import numpy as np

def count(game, d):
    if game.game_over() != 0:
        return 1
    if d == 0:
        return 1
    cnt = 0
    for m in knights.legal_moves():
        game.move(m)
        cnt += count(game, d-1)
        game.undo(m)
    return cnt

def minimax(game, depth):
    global node_count

    if game.game_over() != 0:
        node_count += 1
        return game.game_over()
    if depth == 0:
        node_count += 1
        return 0

    if game.turn == game.WHITE:
        maxv = -inf
        for move in game.legal_moves():
            game.move(move)
            value = minimax(game, depth - 1)
            game.undo(move)
            if value > maxv:
                maxv = value
        return maxv
    else:
        minv = inf
        for move in game.legal_moves():
            game.move(move)
            value = minimax(game, depth - 1)
            game.undo(move)
            if value < minv:
                minv = value
            return minv

def alphabeta(game, depth, alpha, beta):

    global node_count

    if game.game_over() != 0:
        node_count += 1
        return game.game_over()

    if depth == 0:
        node_count += 1
        return 0

    if game.turn == game.WHITE:
        maxv = -inf
        for move in game.legal_moves():
            game.move(move)
            value = alphabeta(game, depth - 1, alpha, beta)
            game.undo(move)
            if value > maxv:
                maxv = value
                alpha = value
            if alpha >= beta:
                break
        return alpha
    else:
        minv = inf
        for move in game.legal_moves():
            game.move(move)
            value = alphabeta(game, depth - 1, alpha, beta)
            game.undo(move)

            if value < minv:
                minv = value
                beta = value
            if alpha >= beta:
                break
        return beta

heat_map = [
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    ]

def printBoard(board):
    s = ""
    for r in reversed(range(8)):
        s += str(r + 1) + "   "
        for c in range(8):
                s += str(board[r][c]) + " "
        s += "\n"
    s += "    a b c d e f g h\n"
    print(s)

def sorted_moves2(game):
    # heat_map = np.array([
    # [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    # [ 0, 1, 2, 2, 2, 2, 1, 0 ],
    # [ 0, 1, 2, 3, 3, 2, 1, 0],
    # [ 0, 1, 2, 5, 5, 2, 1, 0 ],
    # [ 0, 1, 2, 5, 5, 2, 1, 0 ],
    # [ 0, 1, 2, 3, 3, 2, 1, 0 ],
    # [ 0, 1, 2, 2, 2, 2, 1, 0 ],
    # [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    # ])

    # heat_map = np.array([
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    # ])

    # heat_map = np.array([
    #     [7, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [7, 4, 3, 2, 1, 0, 0, 0],
    # ])

    # heat_map = np.array([
    #     [7, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [5, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [6, 4, 3, 2, 1, 0, 0, 0],
    #     [7, 4, 3, 2, 1, 0, 0, 0],
    # ])

    heat_map = np.array([
        [6, 4, 3, 2, 0, 0, 0, 0],
        [6, 4, 3, 2, 0, 0, 0, 0],
        [6, 4, 3, 2, 0, 0, 0, 0],
        [0, 3, 3, 2, 0, 0, 0, 0],
        [0, 3, 3, 2, 0, 0, 0, 0],
        [6, 4, 3, 2, 0, 0, 0, 0],
        [6, 4, 3, 2, 0, 0, 0, 0],
        [7, 4, 3, 2, 0, 0, 0, 0],
    ])

    if game.turn == game.WHITE:
        oknights = game.black_knights
    else:
        oknights = game.white_knights
    moves = knights.legal_moves()
    vmoves = []

    for enemy in oknights:
        r, c = enemy
        for i in range(0, 3):
            if(r - 1 >= 0 and c - 1 + i >= 0 and c - 1 + i < 8):
                heat_map[r - 1][c - 1 + i] += 50
            if(r - 0 >= 0 and c - 1 + i >= 0 and c - 1 + i < 8):
                heat_map[r - 0][c - 1 + i] += 50
            if(r + 1 < 8 and c - 1 + i >= 0 and c - 1 + i < 8):
                heat_map[r + 1][c - 1 + i] += 50
        heat_map[r][c] = 999

    # printBoard(heat_map)
    for m in moves:
        kfrom, kto = m
        v = heat_map[kto[0]][kto[1]]
        # print(v)
        vmoves.append((m, v))
        # print(vmoves)
    vmoves = sorted(vmoves, key=lambda x: -x[1])
    # print(vmoves)
    return [m for m, v in vmoves]

def is_capture(game, move):
    if game.turn == game.WHITE:
        oknights = game.black_knights
    else:
        oknights = game.white_knights

    if move in oknights:
        return True
    else:
        return False


def sorted_moves(game):
    if game.turn == game.WHITE:
        oknights = game.black_knights
    else:
        oknights = game.white_knights
    moves = knights.legal_moves()
    vmoves = []
    for m in moves:
        kfrom, kto = m
        if kto in oknights:
            v = 10
        else:
            v = 0
        vmoves.append((m,v))
    vmoves = sorted(vmoves, key=lambda x: -x[1])
    print(vmoves)
    return [ m for m, v in vmoves ]

def score(game):
    return len(game.white_knights) - len(game.black_knights)

def alphabeta2(game, d, alpha, beta):    
    global node_count
    
    if game.game_over() != 0:
        node_count += 1
        return game.game_over()
    if d == 0:
        node_count += 1
        return score(game)
    if game.turn == game.WHITE:
        for m in sorted_moves(game):
            game.move(m)
            v = alphabeta2(game, d-1, alpha, beta)
            game.undo(m)
            if alpha < v:
                alpha = v
            if alpha >= beta:
                break
        return alpha
    else:
        for m in sorted_moves(game):
            game.move(m)
            v = alphabeta2(game, d-1, alpha, beta)
            game.undo(m)
            if beta > v:
                beta = v
            if alpha >= beta:
                break
        return beta    

htable = {} # hc -> (value, depth)
hit_count = 0

def alphabeta3(game, d, alpha, beta):    
    global node_count, hit_count

    # la idea de hashear el status de la partida es que si en algun momento se repite, ya se de antemano el valor de ese movimiento y no tengo que calcularlo de nuevo.
    if hash(game) in htable:
        hit_count += 1
        hval, hdepth = htable[hash(game)]
        if hdepth >= d:
            return hval
    
    if game.game_over() != 0:
        node_count += 1
        return game.game_over()
    if d == 0:
        node_count += 1
        return score(game)
    if game.turn == game.WHITE:
        for m in sorted_moves(game):
            game.move(m)
            v = alphabeta3(game, d-1, alpha, beta)
            game.undo(m)
            if alpha < v:
                alpha = v
            if alpha >= beta:
                return alpha
        htable[hash(game)] = (alpha, d)
        return alpha
    else:
        for m in sorted_moves(game):
            game.move(m)
            v = alphabeta3(game, d-1, alpha, beta)
            game.undo(m)
            if beta > v:
                beta = v
            if alpha >= beta:
                return beta
        htable[hash(game)] = (beta, d)
        return beta


def alphabeta4(game, d, alpha, beta):
    global node_count, hit_count

    # la idea de hashear el status de la partida es que si en algun momento se repite, ya se de antemano el valor de ese movimiento y no tengo que calcularlo de nuevo.
    if hash(game) in htable:
        hit_count += 1
        hval, hdepth = htable[hash(game)]
        if hdepth >= d:
            return hval

    if game.game_over() != 0:
        node_count += 1
        return game.game_over()
    if d == 0:
        node_count += 1
        return score(game)
    if game.turn == game.WHITE:
        for m in sorted_moves2(game):
            game.move(m)
            v = alphabeta4(game, d - 1, alpha, beta)
            game.undo(m)
            if alpha < v:
                alpha = v
            if alpha >= beta:
                return alpha
        htable[hash(game)] = (alpha, d)
        return alpha
    else:
        for m in sorted_moves2(game):
            game.move(m)
            v = alphabeta4(game, d - 1, alpha, beta)
            game.undo(m)
            if beta > v:
                beta = v
            if alpha >= beta:
                return beta
        htable[hash(game)] = (beta, d)
        return beta



'''
node_count = 0
value = alphabeta(knights, 14, -inf, inf)
print(node_count, value)

'''
# node_count = 0
# print(minimax(knights, 8))
# print(node_count)
#
#
# print(alphabeta3(knights, 2, -inf, inf))
# print(node_count)
knights = KnightsChess()
# node_count = 0
# printBoard(heat_map)
# value = alphabeta3(knights, 6, -inf, inf)
# print(node_count, hit_count, len(htable), value)

node_count = 0
value = alphabeta4(knights, 9, -inf, inf)
print(node_count, hit_count, len(htable), value)
#print(htable)









