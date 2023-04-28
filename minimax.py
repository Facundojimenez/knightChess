from knightschess import KnightsChess
import numpy as np

center = np.array([
    [  0,  0,  0,  0,  0,  0,  0, 0 ],
    [  0,  1 , 2 , 2,  2,  1,  1, 0 ],
    [  0,  1,  4,  6,  6,  4,  1, 0 ],
    [  0,  1,  4,  8,  8,  4,  1, 0 ],
    [  0,  1,  4,  8,  8,  4,  1, 0 ],
    [  0,  1,  4,  6,  6,  4,  1, 0 ],
    [  0,  1 , 2 , 2,  2,  1,  1, 0 ],
    [  0,  0,  0,  0,  0,  0,  0, 0 ]
    ])

#The score is measured by checking the position of all of the white or black pieces. I made a matrix so that the piece can
#meet each other in the top-left corner of the board
def score(state: KnightsChess):

    res = state.game_over()
    if res != 0:
        print(state)
        return res

    value = 0
    if state.turn == state.BLACK:
        for kn in state.black_knights:
            r, c = kn
            value -= center[r][c]
        # value -= len(state.black_knights)*1
        value *= len(state.black_knights)*2 + 1
        value //= len(state.white_knights)*4 + 1
    else:
        for kn in state.white_knights:
            r, c = kn
            value += center[r][c]
        # value += len(state.white_knights) * 1
        value *= len(state.white_knights) * 2 + 1
        value //= len(state.black_knights) * 4 + 1
    # print(value)
    return value

#For evaluation moves, I first check if it's a Best Move, a Killer Move or a capture. If not I will just take the assigned value from the board
#depending on the position of the piece
def evaluate_move(state, m, bestm):
    global dbg_cnt, dbg_cnt2, dbg_cnt3
    if m == bestm:
        dbg_cnt +=1
        return 10000

    if state.is_capture(m):
        dbg_cnt3 += 1
        return 9000

    if m in killer_moves[0] or m in killer_moves[1]:
        dbg_cnt2 += 1
        return 8000


    return center[m[1][0]][m[1][1]]
def sorted_moves(state: KnightsChess, hbestm):
    def orderer(move):
        return evaluate_move(state, move, hbestm)

    moves = state.legal_moves()
    in_order = sorted(moves, key=orderer, reverse=True)
    return list(in_order)


#I'm only using two killer moves
def insert_killerMove(move, depth):
    global killer_moves
    if killer_moves[0][depth] != move and killer_moves[0][depth] != move:
        killer_moves[1][depth] = killer_moves[0][depth]
        killer_moves[0][depth] = move


def minimax(state: KnightsChess, alpha: int, beta: int, depth: int):
    global node_cnt, hit_cnt, killer_moves
    node_cnt += 1

    res = state.game_over()
    if res != 0:
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
    #
    # if depth == 0:
    #     return score(state)

    # Disabled quiescense search
    if depth == 0:
        res = quiescence(state, alpha, beta, 10)
        return res

    if state.turn == state.WHITE:
        bestm = None
        for m in sorted_moves(state, hbestm):
            state.move(m)
            val = minimax(state, alpha, beta, depth-1)
            state.undo(m)
            if val == state.WIN or val == state.LOSE:
                return val
            if val > alpha:
                alpha = val
                bestm = m
            if alpha >= beta:
                if not state.is_capture(m):
                    insert_killerMove(m, depth)
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
            if val == state.WIN or val == state.LOSE:
                return val
            if val < beta:
                beta = val
                bestm = m
            if alpha >= beta:
                if not state.is_capture(m):
                    insert_killerMove(m, depth)
                htable[hash(state)] = (beta, depth, bestm, "beta")
                return beta
        htable[hash(state)] = (beta, depth, bestm, "exact")
        return beta

#TODO fix quiescence
def quiescence(state: KnightsChess, alpha: int, beta: int,depth):
    scr = score(state)
    if depth <= 0 or state.game_over() != 0:
        return scr


    hbestm = None
    bestm = None
    if state.turn == state.WHITE:
        if scr >= beta:
            return scr
        for m in sorted_moves(state, hbestm):
            if state.is_capture(m):
                state.move(m)
                val = quiescence(state, alpha, beta, depth - 1)
                state.undo(m)
                if val == state.WIN or val == state.LOSE:
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
        if alpha < scr:
            alpha = scr
        for m in sorted_moves(state, hbestm):
            if state.is_capture(m):
                state.move(m)
                val = quiescence(state, alpha, beta, depth - 1)
                state.undo(m)
                if val == state.WIN or val == state.LOSE:
                    return val
                if val < beta:
                    beta = val
                    bestm = m
                if alpha >= beta:
                    htable[hash(state)] = (beta, depth, bestm, "beta")
                    return beta
        htable[hash(state)] = (beta, depth, bestm, "exact")
        return beta

###Debug variables
dbg_cnt = 0
dbg_cnt2 = 0
dbg_cnt3 = 0
###




knights = KnightsChess()
MAX_DEPTH = 20
INITIAL_ALPHA = -100000000
INITIAL_BETA = 100000000
htable = {} # hkey -> (value, depth, bestm, flag)

#Iterative deepening for alpha-beta pruning algorithm
for d in range(2, MAX_DEPTH):
    node_cnt = 0
    hit_cnt = 0
    dbg_cnt = 0

    killer_moves = [[(0, 0) for _ in range(MAX_DEPTH)] for _ in range(2)]

    print(d, minimax(knights,  INITIAL_ALPHA, INITIAL_BETA, d), node_cnt,
          hit_cnt, dbg_cnt, dbg_cnt2, dbg_cnt3)

















