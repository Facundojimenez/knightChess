from knightschess import KnightsChess


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
center = [
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 1, 1, 1, 1, 1, 1, 0 ],
    [ 0, 1, 4, 4, 4, 4, 1, 0 ],
    [ 0, 1, 4, 6, 6, 4, 1, 0 ],
    [ 0, 1, 4, 6, 6, 4, 1, 0 ],
    [ 0, 1, 4, 4, 4, 4, 1, 0 ],
    [ 0, 1, 1, 1, 1, 1, 1, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0 ],
    ]

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
#     [ 40, 40, 40, 40, 40, 40,  0, 0 ],
#     [ 35, 35, 35, 35, 35, 35,  0, 0 ],
#     [ 30, 30, 30, 30, 30, 30,  0, 0 ],
#     [ 25, 25, 25, 25, 25, 25,  0, 0 ],
#     [ 20, 20, 20, 20, 20, 20,  0, 0 ],
#     [ 15, 15, 15, 15, 15, 15,  0, 0 ],
#     [ 10, 10, 10, 10, 10, 5, 0, 0 ],
#     [ 0,  0,  0,  0,  0,  0,  0, 0 ]
#     ]

dbg_move = None
def score(state: KnightsChess):
    global dbg_move
    res = state.game_over()

    if res != 0:
        print(res)
        print(state)
        if state.turn == state.WHITE:
            return 1000
        else:
            return -1000

    # if len(state.black_knights) == 0:
    #     print("negro !!!!!!!!!!!")
    #     print(state)
    # if len(state.white_knights) == 0:
    #     print("blanco ??????????")
    #     print(state)

    # if res != 0:
    #     print("pnga")
    #     return res


    # print("MOVIMIENTO: " + state.turn + "----->" + str(dbg_move[0]) + "-"  + str(dbg_move[1]))
    # print("MOVIMIENTO: " + state.turn + "----->" + state.move2notation(dbg_move))
    # print(state)
    # print("BLACK: " + str(len(state.black_knights)))
    # print("WHITE: " + str(len(state.white_knights)))
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

    rez = state.game_over()

    if rez != 0:
        # print(rez)
        return score(state)

    # if depth == 0:
    #     puntuacion = quiescence(state, 3, alpha, beta)
    #     return puntuacion

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
        return score(state)


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


dbg_cnt = 0
dbg_cnt2 = 0
dbg_cnt3 = 0


knights = KnightsChess()
MAX_DEPTH = 50
INITIAL_ALPHA = -100000000
INITIAL_BETA = 100000000
htable = {} # hkey -> (value, depth, bestm, flag)
hit_cnt = 0


for d in range(2, 20):
    node_cnt = 0
    hit_cnt = 0
    dbg_cnt = 0

    killer_moves = [[(0, 0) for _ in range(50)] for _ in range(2)]

    print(d, minimax(knights,  INITIAL_ALPHA, INITIAL_BETA, d), node_cnt,
          hit_cnt, dbg_cnt, dbg_cnt2, dbg_cnt3)

















