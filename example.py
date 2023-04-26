from knightschess import KnightsChess
import numpy as np

# center = [
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ]
#     ]
#
# center = [
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 1, 1, 1, 1, 1, 1, 0 ],
#     [ 0, 1, 4, 4, 4, 4, 1, 0 ],
#     [ 0, 1, 4, 6, 6, 4, 1, 0 ],
#     [ 0, 1, 4, 6, 6, 4, 1, 0 ],
#     [ 0, 1, 4, 4, 4, 4, 1, 0 ],
#     [ 0, 1, 1, 1, 1, 1, 1, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     ]

# center = [
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 1,  1,  1,  1,  1,  1,  1, 1 ],
#     [ 2,  2,  2,  2,  2,  2,  2, 2 ],
#     [ 4,  4,  4,  4,  4,  4,  4, 4 ],
#     [ 3,  3,  3,  3,  3,  3,  3, 3 ],
#     [ 2,  2,  2,  2,  2,  2,  2, 2 ],
#     [ 1,  1,  1,  1,  1,  1,  1, 1 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ]
#     ]

# center = [
#     [ 80, 50, 40, 40, 40, 40,  0, 0 ],
#     [ 50, 50, 35, 35, 35, 35,  0, 0 ],
#     [ 35, 35, 30, 30, 30, 30,  0, 0 ],
#     [ 25, 25, 25, 25, 25, 25,  0, 0 ],
#     [ 20, 20, 20, 20, 20, 20,  0, 0 ],
#     [ 15, 15, 15, 15, 15, 15,  0, 0 ],
#     [ 10, 10, 10, 10, 10,  5,  0, 0 ],
#     [  0,  0,  0,  0,  0,  0,  0, 0 ]
#     ]

#v2
# center = [
#     [ 80, 50, 40, 40, 40, 35,  0, 0 ],
#     [ 50, 50, 35, 35, 35, 35,  0, 0 ],
#     [ 35, 35, 30, 30, 30, 30,  0, 0 ],
#     [ 25, 25, 25, 25, 25, 25,  0, 0 ],
#     [ 20, 20, 20, 20, 20, 20,  0, 0 ],
#     [ 15, 15, 15, 15, 15, 15,  0, 0 ],
#     [ 10, 10, 10, 10, 10,  5,  0, 0 ],
#     [  0,  0,  0,  0,  0,  0,  0, 0 ]
#     ]

#v3
# center = [
#     [ 80, 50, 40, 40, 40, 35,  0, 0 ],
#     [ 60, 50, 35, 35, 35, 35,  0, 0 ],
#     [ 35, 35, 35, 30, 30, 30,  0, 0 ],
#     [ 25, 25, 25, 25, 25, 25,  0, 0 ],
#     [ 20, 20, 20, 20, 20, 20,  0, 0 ],
#     [ 15, 15, 15, 15, 15, 15,  0, 0 ],
#     [ 10, 10, 10, 10, 10,  5,  0, 0 ],
#     [  0,  0,  0,  0,  0,  0,  0, 0 ]
#     ]

#v4
center = np.array([
    [ 80, 50, 40, 40, 40, 35,  0, 0 ],
    [ 60, 50, 35, 35, 35, 35,  0, 0 ],
    [ 35, 35, 35, 30, 30, 30,  0, 0 ],
    [ 25, 25, 25, 25, 25, 25,  0, 0 ],
    [ 25, 20, 20, 20, 20, 20,  0, 0 ],
    [ 15, 15, 15, 15, 15, 15,  0, 0 ],
    [ 10, 10, 10, 10, 10,  5,  0, 0 ],
    [  0,  0,  0,  0,  0,  0,  0, 0 ]
    ])

dbg_move = None
def score(state: KnightsChess):
    global dbg_move
    res = state.game_over()

    if res != 0:
        # print(res)
        # print(state)
        if state.turn == state.WHITE:
            return -1000
        else:
            return 1000

    value = 0
    if state.turn == state.BLACK:
        for kn in state.black_knights:
            r, c = kn
            value -= center[r][c]
    else:
        for kn in state.white_knights:
            r, c = kn
            value += center[r][c] #TODO CAMBIAR A += A VER SI MEJORA

    return value

def evaluate_move(state, m, bestm):
    global dbg_cnt, dbg_cnt2, dbg_cnt3
    if m == bestm:
        dbg_cnt +=1
        return 10000

    if m in killer_moves[0] or m in killer_moves[1]:
        dbg_cnt2 += 1
        return 9000

    if state.is_capture(m):
        dbg_cnt3 += 1
        return 8000

    return center[m[1][0]][m[1][1]]
def sorted_moves(state: KnightsChess, hbestm):
    def orderer(move):
        return evaluate_move(state, move, hbestm)

    moves = state.legal_moves()
    in_order = sorted(moves, key=orderer, reverse=True)
    return list(in_order)

def insert_killerMove(move, depth):
    global killer_moves
    if killer_moves[0][depth] != move:
        killer_moves[1][depth] = killer_moves[0][depth]
        killer_moves[0][depth] = move


def minimax(state: KnightsChess, alpha: int, beta: int, depth: int):
    global node_cnt, hit_cnt, killer_moves, dbg_move
    node_cnt += 1


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

    if state.game_over():
        return score(state)

    if depth == 0:
        res = quiescence(state, alpha, beta, 0)
        return res

    if state.turn == state.WHITE:
        bestm = None
        for m in sorted_moves(state, hbestm):
            state.move(m)
            dbg_move = m
            val = minimax(state, alpha, beta, depth-1)
            state.undo(m)
            if val == 1000 or val == -1000:
                return val
            if val > alpha:
                alpha = val
                bestm = m
            if alpha >= beta:
                if not state.is_capture(m):
                    insert_killerMove(m, depth)
                # insert_killerMove(m, depth)
                htable[hash(state)] = (alpha, depth, bestm, "alpha")
                return alpha
        htable[hash(state)] = (alpha, depth, bestm, "exact")
        return alpha
    else:
        bestm = None
        for m in sorted_moves(state, hbestm):
            state.move(m)
            val = minimax(state, alpha, beta, depth-1)
            state.undo(m)
            if val == 1000 or val == -1000:
                return val
            if val < beta:
                beta = val
                bestm = m
            if alpha >= beta:
                if not state.is_capture(m):
                    insert_killerMove(m, depth)
                # insert_killerMove(m, depth)
                htable[hash(state)] = (beta, depth, bestm, "beta")
                return beta
        htable[hash(state)] = (beta, depth, bestm, "exact")
        return beta


def quiescence(state: KnightsChess, alpha: int, beta: int,depth):
    puntuacion = score(state)

    if depth <= 0 or state.game_over() != 0:
        return puntuacion

    if puntuacion >= beta:
        return puntuacion
    if alpha < puntuacion:
        alpha = puntuacion

    hbestm = None
    if state.turn == state.WHITE:
        bestm = None
        for m in sorted_moves(state, hbestm):
            if state.is_capture(m):
                state.move(m)
                val = quiescence(state, alpha, beta, depth - 1)
                state.undo(m)
                if val == 1000 or val == -1000:
                    return val
                if val > alpha:
                    alpha = val
                    bestm = m
                if alpha >= beta:
                    htable[hash(state)] = (alpha, depth, bestm, "alpha")
                    return alpha
            htable[hash(state)] = (alpha, depth, bestm, "exact")
            return alpha
    else:
        bestm = None
        for m in sorted_moves(state, hbestm):
            if state.is_capture(m):
                state.move(m)
                val = quiescence(state, alpha, beta, depth - 1)
                state.undo(m)
                if val == 1000 or val == -1000:
                    return val
                if val < beta:
                    beta = val
                    bestm = m
                if alpha >= beta:
                    htable[hash(state)] = (beta, depth, bestm, "beta")
                    return beta
            htable[hash(state)] = (beta, depth, bestm, "exact")
            return beta


dbg_cnt = 0
dbg_cnt2 = 0
dbg_cnt3 = 0


knights = KnightsChess()
MAX_DEPTH = 50
INITIAL_ALPHA = -100000000
INITIAL_BETA = 100000000
htable = {} # hkey -> (value, depth, bestm, flag)
hit_cnt = 0


for d in range(2, 16):
    node_cnt = 0
    hit_cnt = 0
    dbg_cnt = 0

    killer_moves = [[(0, 0) for _ in range(16)] for _ in range(2)]

    print(d, minimax(knights,  INITIAL_ALPHA, INITIAL_BETA, d), node_cnt,
          hit_cnt, dbg_cnt, dbg_cnt2, dbg_cnt3)

















