
class KnightsChess:
    
    ROWS = 8
    COLUMNS = 8 
    EMPTY = '-'
    WHITE = 'N'
    BLACK = 'n'
    COL_NAMES = { "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7 }
    ROW_NAMES = { "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7 }
    
    def __init__(self, knights=("a1,c1,e1","e8")):
        self.stack = []
        self._setup(knights)
        self.turn = self.WHITE
    
    def notation2square(self, note):
        c, r = note
        return self.ROW_NAMES[r], self.COL_NAMES[c]        
    
    def move2notation(self, m):
        (rf, cf), (rt, ct) = m
        return chr(ord("a") + cf) + str(rf+1) + '-' + chr(ord("a") + ct) + str(rt+1)
    
    def _setup(self, knights):
        self.white_knights = set(self.notation2square(note) for note in knights[0].split(','))
        self.black_knights = set(self.notation2square(note) for note in knights[1].split(','))
    
    def __str__(self):
        s = ""
        for r in reversed(range(self.ROWS)):
            s += str(r+1) + " "
            for c in range(self.COLUMNS):
                if (r,c) in self.white_knights:
                    s += "N "
                elif (r,c) in self.black_knights:
                    s += "n "
                else:
                    s += "- "
            s += "\n"
        s += "  a b c d e f g h\n"
        s += "moves: " + ', '.join(self.move2notation(m) for m in self.legal_moves())
        return s
    
    def __hash__(self):
        state = [ r * self.ROWS + c for r, c in self.white_knights | self.black_knights ]
        state = sorted(state) + [ self.turn ]
        return hash(tuple(state))
    
    def _knight_moves(self, square):
        r, c = square
        moves = [ (r+2, c+1), (r-2, c+1), (r+2, c-1), (r-2, c-1), (r+1, c+2), (r-1, c+2), (r+1, c-2), (r-1, c-2) ]
        return [ (r, c) for r, c in moves if 0 <= r and r < self.ROWS and 0 <= c and c < self.COLUMNS ]
    
    def legal_moves(self):
        moves = []
        knights = self.white_knights if self.turn == self.WHITE else self.black_knights
        for knight in knights:            
            kmoves = [ (knight, kto) for kto in self._knight_moves(knight) if kto not in knights ]
            moves += kmoves
        return moves
    
    def game_over(self):
        if len(self.white_knights) == 0:
            return -1000
        elif len(self.black_knights) == 0:
            return 1000
        return 0
    
    def move(self, m):
        kfrom, kto = m
        if self.turn == self.WHITE:
            self.white_knights.remove(kfrom)
            self.white_knights.add(kto)
            if kto in self.black_knights:
                self.black_knights.remove(kto)
                self.stack.append(True)                
            else:
                self.stack.append(False)
        else:
            self.black_knights.remove(kfrom)
            self.black_knights.add(kto)
            if kto in self.white_knights:
                self.white_knights.remove(kto)
                self.stack.append(True)                
            else:
                self.stack.append(False)
        self.turn = self.WHITE if self.turn == self.BLACK else self.BLACK
    
    def undo(self, m):
        kfrom, kto = m
        self.turn = self.WHITE if self.turn == self.BLACK else self.BLACK
        if self.turn == self.WHITE:
            self.white_knights.remove(kto)
            self.white_knights.add(kfrom)
            if self.stack.pop():
                self.black_knights.add(kto)
        else:
            self.black_knights.remove(kto)
            self.black_knights.add(kfrom)
            if self.stack.pop():
                self.white_knights.add(kto)

if __name__ == '__main__':
    from random import choice
    
    knights = KnightsChess()
    maxmoves = 10
    while not knights.game_over() and maxmoves > 0:
        maxmoves -= 1
        print(knights)
        lm = knights.legal_moves()
        m = choice(lm)
        print(knights.turn, "plays", knights.move2notation(m))
        knights.move(m)            
    print("Game over, winner is", knights.game_over())
    print(knights)
