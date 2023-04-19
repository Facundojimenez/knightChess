from knightschess import KnightsChess
# ------------ el mejor hasta ahora
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, 0, 0, 0, 0, 0 ],
#     [ 0, 0, 0, -2, -2, 0, 0, 0 ],
#     [ 0, -1, -1, -1, -1, -1, -1, 0 ],
#     [ 0, -2, -2, -2, -2, -2, -2, 0 ],
#     [ 0, -2, -2, -2, -2, -2, -2, 0 ],
#     ]

# center = [
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ],
#     [ 0,  0,  0, -2, -2,  0,  0, 0 ],
#     [ 0, -1, -1, -1, -1, -1, -1, 0 ],
#     [ 0, -2, -2, -2, -2, -2, -2, 0 ],
#     [ 0, -2, -2, -2, -2, -2, -2, 0 ],
#     ]
#
center = [
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ],
    [ 0,  0,  0,  0,  0,  0,  0, 0 ]
    ]

# center = [
#     [ 2,  1,  0,  0,  0,  0,  0, 0 ],
#     [ 1,  1,  0,  0,  0,  0,  0, 0 ],
#     [ 1,  1,  0,  0,  0,  0,  0, 0 ],
#     [ 1,  1,  0,  0,  0,  0,  0, 0 ],
#     [ 1,  1,  0,  0,  0,  0,  0, 0 ],
#     [ 1,  1,  0,  0,  0,  0,  0, 0 ],
#     [ 1,  1,  0,  0,  0,  0,  0, 0 ],
#     [ 2,  1,  0,  0,  0,  0,  0, 0 ]
#     ]

def score(state: KnightsChess):
    value = 0
    for kn in state.black_knights:
        r, c = kn
        value -= center[r][c]
    return value

dbg_cnt = 0
dbg_cnt2 = 0

# def sorted_moves(state: KnightsChess, hbestm):
#     global dbg_cnt, dbg_cnt2
#     moves = state.legal_moves()
#
#     if hbestm not in moves:
#         dbg_cnt2 += 1
#         return sorted(moves, key=lambda m: -center[m[1][0]][m[1][1]])
#     else:
#         dbg_cnt += 1
#         return sorted(moves, key=lambda m: -center[m[1][0]][m[1][1]] - (1000 if m == hbestm else 0))


def evaluate_move(state, m, hbest):
    if m == hbest:
        # print("hhh")
        return 10000
    if m == killer_moves:
        print("kkk")
        return 9000
    if state.is_capture(m):
        print("ccc")
        return 8000

    # print("xxx")
    return 0
def sorted_moves(state: KnightsChess, hbestm):
    def orderer(move):
        return evaluate_move(state, move, hbestm)

    moves = state.legal_moves()
    in_order = sorted(moves, key=orderer, reverse=True)
    return list(in_order)

htable = {} # hkey -> (value, depth, bestm, flag)
hit_cnt = 0


def insert_killerMove(move, depth):
    global killer_moves
    if killer_moves[0][depth] != move:
        killer_moves[1][depth] = killer_moves[0][depth]
        killer_moves[0][depth] = move

def minimax(state: KnightsChess, alpha: int, beta: int, depth: int):
    global node_cnt, hit_cnt, killer_moves
    node_cnt += 1

    res = state.game_over()
    if res:
        return res

    # if depth == 0:
    #     puntuacion = quiescence(state, 1, alpha, beta)
    #     return puntuacion

    if depth == 0:
        return score(state)

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
                    if not state.is_capture(m):
                        insert_killerMove(bestm, depth)
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
            if val < beta:
                beta = val
                bestm = m
            if alpha >= beta:
                if not state.is_capture(m):
                    insert_killerMove(bestm, depth)
                htable[hash(state)] = (beta, depth, bestm, "beta")
                return beta
        htable[hash(state)] = (beta, depth, bestm, "exact")
        return beta


def quiescence(state: KnightsChess, depth, alpha: int, beta: int):
    puntuacion = score(state)

    if depth == 0:
        return puntuacion

    if puntuacion >= beta:
        return beta
    if alpha < puntuacion:
        alpha = puntuacion

    hbestm = None
    if state.turn == state.WHITE:
        bestm = None
        for m in sorted_moves(state, hbestm):
            if state.is_capture(m):
                state.move(m)
                val = minimax(state, alpha, beta, depth - 1)
                state.undo(m)
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
                val = minimax(state, alpha, beta, depth - 1)
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
MAX_DEPTH = 50
INITIAL_ALPHA = -10000
INITIAL_BETA = 10000

for d in range(2, 19): #10 or 11
    node_cnt = 0
    hit_cnt = 0
    dbg_cnt = 0

    killer_moves = [[(0, 0) for _ in range(50)] for _ in range(2)]

    print(d, minimax(knights,  INITIAL_ALPHA, INITIAL_BETA, d), node_cnt, hit_cnt, dbg_cnt, dbg_cnt2)

















