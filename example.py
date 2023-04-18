
from knightschess import KnightsChess

node_cnt = 0

# center = [
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     ]

# center = [
#         [7, 4, 3, 2, 0, 0, 0, 0],
#         [6, 4, 3, 2, 0, 0, 0, 0],
#         [6, 4, 3, 2, 0, 0, 0, 0],
#         [0, 3, 3, 2, 0, 0, 0, 0],
#         [0, 3, 3, 2, 0, 0, 0, 0],
#         [6, 4, 3, 2, 0, 0, 0, 0],
#         [6, 4, 3, 2, 0, 0, 0, 0],
#         [7, 4, 3, 2, 0, 0, 0, 0],
#     ]

#-----------SOLUCION PARA DEPTH = 16
# center = [
#         [7, 4, 3, 0, 0, 0, 0, 0],
#         [6, 4, 3, 0, 0, 0, 0, 0],
#         [6, 4, 3, 2, 0, 0, 0, 0],
#         [0, 3, 3, 2, 0, 0, 0, 0],
#         [0, 3, 3, 2, 0, 0, 0, 0],
#         [6, 4, 3, 2, 0, 0, 0, 0],
#         [6, 4, 3, 0, 0, 0, 0, 0],
#         [7, 4, 3, 0, 0, 0, 0, 0],
#     ]

#
# #-----------SOLUCION PARA DEPTH = 15
# center = [
#         [12, 9, 8, 5, 5, 5, 5, 5],
#         [11, 9, 8, 5, 5, 5, 5, 5],
#         [11, 9, 8, 7, 7, 5, 5, 5],
#         [5,  8, 8, 7, 7, 5, 5, 5],
#         [5,  8, 8, 7, 7, 5, 5, 5],
#         [11, 9, 8, 7, 7, 5, 5, 5],
#         [11, 9, 8, 5, 5, 5, 5, 5],
#         [12, 9, 8, 5, 5, 5, 5, 5],
#     ]

# center = [
#         [12, 9, 8, 5, 5, 8, 9, 12],
#         [11, 9, 8, 5, 5, 8, 9, 11],
#         [11, 9, 8, 7, 7, 8, 9, 11],
#         [5,  8, 8, 7, 7, 8, 8, 5],
#         [5,  8, 8, 7, 7, 8, 8, 5],
#         [11, 9, 8, 7, 7, 8, 9, 11],
#         [11, 9, 8, 5, 5, 8, 9, 11],
#         [12, 9, 8, 5, 5, 8, 9, 12],
#     ]

# center = [
#     [ 5, 5, 5, 5, 5, 5, 5, 5 ],
#     [ 5, 5, 5, 5, 5, 5, 5, 5 ],
#     [ 5, 5, 5, 5, 5, 5, 5, 5 ],
#     [ 5, 5, 5, 5, 5, 5, 5, 5 ],
#     [ 5, 5, 5, 5, 5, 5, 5, 5 ],
#     [ 5, 4, 4, 4, 4, 4, 4, 5 ],
#     [ 5, 3, 3, 3, 3, 3, 3, 5 ],
#     [ 5, 3, 3, 3, 3, 3, 3, 5 ],
#     ]

# ------------ el mejor hasta ahora
# center = [
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, -2, -2, 0, 0, 0 ],
#     [ 0, -1, -1, -1, -1, -1, -1, 0 ],
#     [ 0, -2, -2, -2, -2, -2, -2, 0 ],
#     [ 0, -2, -2, -2, -2, -2, -2, 0 ],
#     ]

center = [
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0, -2, -2,  0,  0, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, -2, -2, -2, -2, -2, -2, 0 ],
    [ 0, -2, -2, -2, -2, -2, -2, 0 ],
    ]

def score(state: KnightsChess):
    value = 0
    for kn in state.black_knights:
        r, c = kn
        value -= center[r][c]
    return value

dbg_cnt = 0
dbg_cnt2 = 0

def sorted_moves(state: KnightsChess, hbestm):
    global dbg_cnt, dbg_cnt2
    moves = state.legal_moves()
    if hbestm not in moves:
        dbg_cnt2 += 1
        return sorted(moves, key=lambda m: -center[m[1][0]][m[1][1]])
    else:
        dbg_cnt += 1
        return sorted(moves, key=lambda m: -center[m[1][0]][m[1][1]] - (1000 if m == hbestm else 0))

htable = {} # hkey -> (value, depth, bestm, flag)
hit_cnt = 0

def minimax(state: KnightsChess, alpha, beta, depth):
    global node_cnt, hit_cnt
    node_cnt += 1
    rez = state.game_over()
    if rez:
        return rez #, []
    
    hbestm = None
    if hash(state) in htable:
        hit_cnt += 1
        hval, hdepth, hbestm, hflag = htable[hash(state)]
        if hdepth >= depth and hflag == "exact":
            return hval
        if hdepth >= depth and hflag == "alpha" and hval >= beta:
            return hval
        if hdepth >= depth and hflag == "beta" and alpha >= hval:
            return hval       
    
    if depth == 0:
        return score(state) ##, []
    
    if state.turn == state.WHITE:
        bestm = None
        for m in sorted_moves(state, hbestm):
            state.move(m)
            val = minimax(state, alpha, beta, depth-1)
            state.undo(m)
            if val > alpha:
                alpha = val
                bestm = m
            if alpha >= beta:
                htable[hash(state)] = (alpha, depth, bestm, "alpha")
                return alpha
        htable[hash(state)] = (alpha, depth, bestm, "exact")
        return alpha# , [ bestm ] + sublist
    else:
        bestm = None
        for m in sorted_moves(state, hbestm):
            state.move(m)
            val = minimax(state, alpha, beta, depth-1)
            state.undo(m)
            if val < beta:
                beta = val
                bestm = m
            if alpha >= beta:
                htable[hash(state)] = (beta, depth, bestm, "beta")
                return beta
        htable[hash(state)] = (beta, depth, bestm, "exact")
        return beta
    
knights = KnightsChess()

for d in range(1, 19): #10 or 11
    node_cnt = 0
    hit_cnt = 0
    dbg_cnt = 0
    # htable = {}
    print(d, minimax(knights, -10000, 10000, d), node_cnt, hit_cnt, dbg_cnt, dbg_cnt2)

















