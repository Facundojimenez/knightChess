
from knightschess import KnightsChess
from math import inf

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

# def alphabeta(game, d, alpha, beta):
#     global node_count
#
#     if game.game_over() != 0:
#         node_count += 1
#         return game.game_over()
#     if d == 0:
#         node_count += 1
#         return 0
#     if game.turn == game.WHITE:
#         for m in knights.legal_moves():
#             game.move(m)
#             v = alphabeta(game, d-1, alpha, beta)
#             game.undo(m)
#             if alpha < v:
#                 alpha = v
#             if alpha >= beta:
#                 break
#         return alpha
#     else:
#         for m in knights.legal_moves():
#             game.move(m)
#             v = alphabeta(game, d-1, alpha, beta)
#             game.undo(m)
#             if beta > v:
#                 beta = v
#             if alpha >= beta:
#                 break
#         return beta

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

knights = KnightsChess()

'''
node_count = 0
value = alphabeta(knights, 14, -inf, inf)
print(node_count, value)

'''
node_count = 0
print(minimax(knights, 7))
print(node_count)

node_count = 0
print(alphabeta3(knights, 7, -inf, inf))
print(node_count)

# print(htable)

# value = alphabeta3(knights, 14, -inf, inf)
# print(node_count, hit_count, len(htable), value)
#print(htable)











