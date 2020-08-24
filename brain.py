# Controls how the program thinks and plays

import chess
import chess.polyglot
import copy
import random
import math
import chess.syzygy
#import chess.gaviota
# Many ideas for how to improve algorithm efficiency and position evaluation taken from:
# https://www.chessprogramming.org/ and Alan Turing's "Turbochamp" program
# I realize the latter is slightly outdated, but I am a big Alan Turing fan and wanted to use some of his ideas
class brain:
    # Initializes constant variables for brain class to assess positional strength
    def __init__(self, board):
        self.time = 0
        self.board = copy.deepcopy(board)
        self.test = True
        self.game_phase = "opening"
        self.out_of_book = False
        self.in_tablebase = False
        self.current_depth = 0
        self.tb = chess.syzygy.open_tablebase("./OmegaFifteen/3-4-5piecesSyzygy/3-4-5")
        # Search Parameters
        self.MIN_DEPTH_SEARCH = 2
        self.MAX_DEPTH_SEARCH = 6
        self.MAX_INITIAL_SEARCH = 4
        self.ATTACKS_HIGHER_PIECE_PLIES = 2
        self.CHECK_PLIES = 3
        # Evaluation Factors
        self.PIECE_VALUE_MULTIPLIER = 5
        self.TEMPO_BONUS = 0.35

        self.SQUARES_BY_KING_OPPOSITE_CONTROLS_BONUS = 0.7
        self.KING_EXPOSURE_NEGATIVE_VALUE = 0.15
        self.CHECK_BONUS = 0.1
        self.KING_PROXIMITY_BONUS = 0.3
        self.OPPONENT_QUEEN_KING_SAFETY_NEGATIVE_MULTIPLIER = 1.7
        self.CAN_CASTLE_BONUS = 0.1
        self.KING_ATTACK_PAWNS_BONUS = 0.1
        self.KING_DEFEND_PAWNS_BONUS = 0.05
        self.THREATEN_CHECKMATE_BONUS = 0.4

        self.PAWN_ADVANCEMENT_BONUS = 2.5
        self.PAWN_PROTECTED_BY_NON_PAWN_BONUS = 0.7
        self.PAWN_PROTECTED_BY_PAWN_BONUS = 0.5
        self.PAWN_BLOCKED_NEGATIVE_BONUS = 0.1
        self.CDE_PAWN_BLOCKED_NEGATIVE_BONUS = 0.25
        self.ISOLATED_PAWN_NEGATIVE_BONUS = 0.3
        self.DOUBLED_PAWN_NEGATIVE_BONUS = 0.4
        self.DOUBLED_ISOLATED_PAWN_NEGATIVE_BONUS = 0.8
        self.PASSED_PAWN_BONUS = 0.6
        self.FIRST_CHECK_BONUS = 1

        self.PIECE_MOBILITY_BONUS = 0.5
        self.PIECE_CAN_CAPTURE_BONUS = 0.8
        self.PIECE_DEFENDED_BONUS = 0.5
        self.PIECE_DEFENDED_AGAIN_BONUS = 0.25

        self.ROOK_OPPOSE_KQ = 0.175
        self.CONNECTED_ROOKS_BONUS = 0.35

        # Rough estimates of how each piece is valued.  Seen a lot of opinions on this.
        # I chose to use my personal weighting of each piece's value
        self.PIECE_VALUES = {
            chess.KING: 100,

            chess.QUEEN: 9,
            chess.ROOK: 5,
            chess.BISHOP: 3.2,
            chess.KNIGHT: 3.05,
            chess.PAWN: 1,

        }
        self.i = []
        self.qvaluations = 0
        # Tables assess approximate value of each piece on each square.
        # Taken from https://www.chessprogramming.org/Simplified_Evaluation_Function
        self.PAWN_TABLE = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.KNIGHT_TABLE = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

        self.BISHOP_TABLE = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        self.ROOK_TABLE = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.QUEEN_TABLE = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]
        # Modified to incentivize castling more
        self.KING_TABLE = [
            20, 35, 10, 0, 0, 10, 35, 20,
            20, 20, -15, -10, -10, -15, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]
        self.KING_TABLE_END_GAME =  [
            -50,-40,-30,-20,-20,-30,-40,-50,
            -30,-20,-10,  0,  0,-10,-20,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-30,  0,  0,  0,  0,-30,-30,
            -50,-30,-30,-30,-30,-30,-30,-50]

        self.table_reference = {
            chess.KING: self.KING_TABLE,

            chess.QUEEN: self.QUEEN_TABLE,
            chess.ROOK: self.ROOK_TABLE,
            chess.BISHOP: self.BISHOP_TABLE,
            chess.KNIGHT: self.KNIGHT_TABLE,
            chess.PAWN: self.PAWN_TABLE,

        }
     # Only method interacted with by game class.  Returns best move.
    def findMove(self, time):
        self.positionEvaluation(self.board)
        # bbb = self.board.piece_map()
        """try:
            move = chess.polyglot.MemoryMappedReader("bookfish.bin").weighted_choice(self.board).move

            return move
        except:"""
        self.time = time
        ans = self.selectMove()
        best = ans[1]
        val = ans[0]
        m = 1
        if self.board.turn == chess.BLACK:
            m = -1
        print(m*val)
        print(best)
        print("ITERATIONS: " + str(self.qvaluations))
        print("\n")
        self.tb.close()
        return best
    # TODO: Establish a percentage of search complete of move
    # First level of search
    def selectMove(self):
        # Tries checking tablebase and book first
        try:
            #raise ValueError()
            piece_count = chess.popcount(self.board.occupied_co[0]) + chess.popcount(self.board.occupied_co[1])
            if piece_count <= 5:
                return self.endgameTablebase()

            choice = chess.polyglot.MemoryMappedReader(
                "./OmegaFifteen/ProDeo292/books/elo2500.bin"
                ).weighted_choice(
                self.board)
            weight = choice.weight
            move = choice.move
            return weight, move
        # If nothing in book or tablebase, proceed normally
        except:
            # Sets default values for alpha, beta, move, and evaluation
            self.out_of_book = True
            best_value = -99999
            best_move = chess.Move.null()
            alpha = -100000
            beta = 100000
            # estimates how long it will take to make this move
            depth_can_go_guess = self.estimateTime()
            max_go_to = min(depth_can_go_guess+2, self.MAX_DEPTH_SEARCH)
            # used to calculate how long it thinks on each ply
            self.i.append(0)
            up_cool_down = 0
            l_move_count = self.board.legal_moves.count()
            copy_board = self.board.copy()
            can_increase_depth = True
            # iterates through all legal moves
            for i in self.board.legal_moves:
                # can't increase ply count twice in a row
                if up_cool_down > 0:
                    up_cool_down -= 1
                # makes the move
                self.board.push(i)

                try:
                    self.current_depth += 1
                    # uses minimax algorithm using negamax implementation
                    value = -self.minimax(max(depth_can_go_guess, self.MIN_DEPTH_SEARCH), alpha=-beta, beta=-alpha,
                                          depth=1)
                    self.current_depth -= 1
                # If it is thinking too long, reset the board and calculate with minimum search
                except MemoryError:
                    print("ERROR")
                    self.qvaluations = 0
                    self.board = copy_board
                    self.board.push(i)
                    d = self.MIN_DEPTH_SEARCH
                    can_increase_depth = False
                    if depth_can_go_guess <= self.MIN_DEPTH_SEARCH:
                        print(
                            "MIN DEPTH TOO MUCH TO HANDLE.\nIF YOU ARE READING THIS, THIS IS REALLY BAD\nREDUCING BY 1")
                        d -= 1
                    depth_can_go_guess = self.MIN_DEPTH_SEARCH
                    self.current_depth = 1
                    value = -self.minimax(d, alpha=-beta, beta=-alpha, depth=1)
                    self.current_depth -= 1
                self.board.pop()
                #print("This move: "+i.uci()+" is worth: "+str(value))

                self.i[0] += 1
                # Based on how many positions it has evaluated so far
                reval_estimate = (self.qvaluations / self.i[0]) * l_move_count
                # Increases or decreases search depth as time permits
                if reval_estimate > self.time * 3 and depth_can_go_guess >= self.MIN_DEPTH_SEARCH + 1:
                    depth_can_go_guess -= 1
                    print("Down to " + str(depth_can_go_guess) + " ply search!")
                elif reval_estimate < self.time / 10 \
                        and up_cool_down == 0 \
                        and depth_can_go_guess < max_go_to \
                        and can_increase_depth:
                    depth_can_go_guess += 1
                    up_cool_down = 2
                    print("Up to " + str(depth_can_go_guess) + " ply search!")
                # Determines best move and score
                if value > best_value or best_move == chess.Move.null():
                    best_value = value
                    best_move = i
                # Alpha beta pruning
                if value > alpha:
                    alpha = value

            return best_value, best_move
    # Minimax algorithm with alpha-beta pruning and negamax implementation
    # Second level of search
    def minimax(self, max_depth, alpha, beta, depth=0):

        piece_count = chess.popcount(self.board.occupied_co[0]) + chess.popcount(self.board.occupied_co[1])
        if piece_count <= 5:
            score = self.staticEvaluation(self.board)
            self.in_tablebase = False
            return score
        best_score = -9999
        # If max depth exceeded, keep looking, but only at checks and captures
        if depth >= max_depth-1:
            return self.checkSearch(alpha, beta)
        if len(self.i) == depth:
            self.i.append(0)
        has_moves = False
        # This is important to check if the game could be over here,
        # so that it doesn't just return the game ends founds in the quiesce function
        if self.checkDrawClaimable(self.board) or self.board.is_game_over():
            return self.staticEvaluation(self.board)
        # Iterates through legal moves
        for i in self.board.legal_moves:

            self.i[depth] += 1

            if not has_moves:
                has_moves = True
            # Same thing as before, pushes move, recursively scans, uses negamax
            # Negamax implementation pretty much uses alpha-beta operating under the principle that what is good
            # for me is bad for my opponent and vise versa
            self.board.push(i)
            self.current_depth += 1
            score = -self.minimax(max_depth, alpha=-beta, beta=-alpha, depth=depth + 1)
            self.current_depth -= 1
            self.board.pop()

            # Alpha-beta pruning
            if score >= beta:
                return beta
            if score > best_score:
                best_score = score
                if score > alpha:
                    alpha = score
        # I don't think this is necessary... just too scared to remove it.
        if not has_moves:
            return self.staticEvaluation(self.board)
        return alpha

    def checkSearch(self, alpha, beta, qdepth=0):
        piece_count = chess.popcount(self.board.occupied_co[0]) + chess.popcount(self.board.occupied_co[1])
        if piece_count <= 5:
            score = self.staticEvaluation(self.board)
            self.in_tablebase = False
            return score
        best_score = -9999
        # If max depth exceeded, keep looking, but only at checks and captures
        if qdepth >= self.CHECK_PLIES:
            return self.quiesce(alpha, beta)
        has_moves = False
        # This is important to check if the game could be over here,
        # so that it doesn't just return the game ends founds in the quiesce function
        if self.checkDrawClaimable(self.board) or self.board.is_game_over():
            return self.staticEvaluation(self.board)
        is_check = self.board.is_check()
        # Iterates through legal moves
        for i in self.board.legal_moves:

            if not has_moves:
                has_moves = True
            # Same thing as before, pushes move, recursively scans, uses negamax
            # Negamax implementation pretty much uses alpha-beta operating under the principle that what is good
            # for me is bad for my opponent and vise versa
            self.current_depth += 1
            if not is_check and not self.board.gives_check(i):
                self.board.push(i)
                score = -self.quiesce(alpha=-beta, beta=-alpha, qdepth=qdepth + 1)
            else:
                self.board.push(i)
                score = -self.checkSearch(alpha=-beta, beta=-alpha, qdepth=qdepth + 1)
            self.board.pop()
            self.current_depth -= 1
            # Alpha-beta pruning
            if score >= beta:
                return beta
            if score > best_score:
                best_score = score
                if score > alpha:
                    alpha = score
        # I don't think this is necessary... just too scared to remove it.
        if not has_moves:
            return self.staticEvaluation(self.board)
        return alpha
    # Third level of search, evaluates captures and some checks
    # TODO Fix captures
    def quiesce(self, alpha, beta, qdepth=0, checked=False):
        #if self.checkDrawClaimable(self.board) or self.board.is_game_over():
        #  return self.staticEvaluation(self.board)
        #is_check = self.board.is_check()
        #if not is_check and not checked:
        # Works under the assumption that a position is not Zugzwang and it can do a normal move whenever
        stand_pat = self.staticEvaluation(self.board)
        if self.in_tablebase:
            self.in_tablebase = False
            return stand_pat
        # Increases the amount of positions evaluated
        self.qvaluations += 1
        # If too many positions are evaluated, something is wrong.  You gotta restart
        if self.qvaluations > 15 * self.time:
            print("Move officially wasted.")
            raise MemoryError("Maximum positions evaluated.  Must redo search at lowest value.")
        # Alpha-beta pruning, no point in evaluating if what you already have is better than what you possibly can get
        if stand_pat >= beta:  # and not self.board.is_check():
            return beta

        # Delta Pruning: Won't consider moves that put it too far down in material
        delta = self.PIECE_VALUES[chess.QUEEN] * self.PIECE_VALUE_MULTIPLIER + 1
        if stand_pat + delta < alpha:
            return alpha

        if alpha < stand_pat:
            alpha = stand_pat
        # Looks at all legal moves
        for i in self.board.legal_moves:
            capture = self.board.is_capture(i)
            #gives_check = self.board.gives_check(i)
            # JK, just captures and some checks.  Not too many checks though
            if capture or i.promotion is not None:

                # Only looks at move with a positive static exchange evaluation
                if capture:
                    if self.see(self.board, i.to_square, self.board.turn) < 0:
                        continue

                # We need to go deeper! (Using negamax, still)
                self.board.push(i)
                self.current_depth += 1
                score = - self.quiesce(-beta, -alpha, qdepth + 1)
                self.current_depth -= 1
                self.board.pop()
                # Alpha-beta pruning
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha
    # Static exchange evaluation
    def see(self, node, square, side):

        value = 0
        # Pretty much always takes back with smallest valued attacker.
        # If at the end it wasn't worth it, then no point in evaluating that move
        piece = self.getSmallestAttacker(node, square, side)
        if piece is not None:
            try_move = chess.Move(piece, square)
            if not node.is_en_passant(try_move):
                piece_just_captured = self.PIECE_VALUES[node.piece_type_at(square)]
            else:
                piece_just_captured = self.PIECE_VALUES[chess.PAWN]

            node.push(try_move)
            value = piece_just_captured - self.see(node, square, not side)
            node.pop()

        return value
    # Determines the smallest attacker on a given square
    def getSmallestAttacker(self, node, square, side):
        min_a = 100
        min_i = None
        for i in node.attackers(side, square):
            p = node.piece_type_at(i)
            val = self.PIECE_VALUES[p]
            if val < min_a:
                min_a = val
                min_i = i

        return min_i
    # Estimates how long the computer thinks a move will take to accurately allocate plies
    # TODO factor checks into estimation
    def estimateTime(self):
        # Pseudo legal required for estimate so that checks don't skew results
        i1 = self.board.pseudo_legal_moves.count()
        self.board.turn = not self.board.turn
        i2 = self.board.pseudo_legal_moves.count()
        self.board.turn = not self.board.turn
        # Gets total material
        pm = self.board.piece_map()
        pieces = {
            chess.WHITE: {
                chess.KING: self.board.pieces(chess.KING, chess.WHITE),
                chess.QUEEN: self.board.pieces(chess.QUEEN, chess.WHITE),
                chess.ROOK: self.board.pieces(chess.ROOK, chess.WHITE),
                chess.BISHOP: self.board.pieces(chess.BISHOP, chess.WHITE),
                chess.KNIGHT: self.board.pieces(chess.KNIGHT, chess.WHITE),
                chess.PAWN: self.board.pieces(chess.PAWN, chess.WHITE)
            },
            chess.BLACK: {
                chess.KING: self.board.pieces(chess.KING, chess.BLACK),
                chess.QUEEN: self.board.pieces(chess.QUEEN, chess.BLACK),
                chess.ROOK: self.board.pieces(chess.ROOK, chess.BLACK),
                chess.BISHOP: self.board.pieces(chess.BISHOP, chess.BLACK),
                chess.KNIGHT: self.board.pieces(chess.KNIGHT, chess.BLACK),
                chess.PAWN: self.board.pieces(chess.PAWN, chess.BLACK)
            }
        }
        m1, m2 = self.getTotalMaterial(pieces)
        # Determines about how much time it will take based on the principle that more material usually means more moves
        counter, sum_used = self.counterEvaluate(i1, i2, m1, m2)

        recount = False
        pawn_map = self.generatePawnMap(pm)
        # Pawns that could become queens within this span of time must be counted as more material
        for i in pawn_map:
            square = chess.square(i[0], i[1])
            d_f_q = self.distFromQueening(square)

            if d_f_q < counter / 2:
                sub = 4
                if self.isPassed(pawn_map, square):
                    sub = 8
                recount = True
                if i[2] == chess.WHITE:
                    m1 += max(sub - d_f_q, 0)
                else:
                    m2 += max(sub - d_f_q, 0)
        # If there is a theoretical future queen in the near future, you have to do the eval again
        # This isn't that big of a deal, because this function is only run once per move
        if recount:
            counter, sum_used = self.counterEvaluate(i1, i2, m1, m2)
        return_val = min(counter, self.MAX_INITIAL_SEARCH)
        return_val = max(return_val, self.MIN_DEPTH_SEARCH)
        print("Counter estimates " + str(sum_used) + " in " + str(counter)
              + " iterations.  Will conduct " + str(return_val) + " ply search.")
        return return_val
    # Sums up move possibilities to produce estimate
    def counterEvaluate(self, i1, i2, m1, m2):
        sum_used = 0
        counter = 0
        sum_total = 1
        if self.board.turn == chess.BLACK:
            m2, m1 = m1, m2
        # Add each sides material on their turn to guess how many moves they can make
        # Once the estimate sum gets higher than the timer, you stop
        while sum_total < self.time:
            sum_used = sum_total
            if counter % 2 == 0:
                sum_total *= i1 * (math.sqrt(m1) / 4)
            else:
                sum_total *= i2 * (math.sqrt(m2) / 4)
            counter += 1
        counter -= 1
        return counter, sum_used
    # Determines if move attacks a piece of higher value.  CURRENTLY UNUSED
    def attacksHigherPiece(self, move):
        self.board.push(move)
        for i in self.board.attacks(move.to_square):
            test_piece = self.board.piece_at(i)
            if test_piece is not None:
                if test_piece.color == self.board.turn:
                    if self.PIECE_VALUES[test_piece.piece_type] > self.PIECE_VALUES[
                        self.board.piece_type_at(move.to_square)]:
                        self.board.pop()
                        return True
        self.board.pop()
        return False
    # TODO: threatening checkmate good, instill it with the box (less material equals higher pawn advancement benefit)
    #  Unstoppable passed pawn
    # Evaluation function, assesses positional strength based on one position without calculating any further
    def positionEvaluation(self, t_board):
        # Checkmate is the best.
        if t_board.is_checkmate():
            # Faster checkmates are better
            if t_board.turn == chess.WHITE:
                return -9999+self.current_depth
            else:
                return 9999-self.current_depth
        # Draws are neutral
        if t_board.can_claim_fifty_moves() \
                or t_board.is_repetition(3) \
                or t_board.is_stalemate() \
                or t_board.is_insufficient_material():
            return 0

        evaluation = 0
        piece_map = t_board.piece_map()
        pieces = {
            chess.WHITE: {
                chess.KING: t_board.pieces(chess.KING, chess.WHITE),
                chess.QUEEN: t_board.pieces(chess.QUEEN, chess.WHITE),
                chess.ROOK: t_board.pieces(chess.ROOK, chess.WHITE),
                chess.BISHOP: t_board.pieces(chess.BISHOP, chess.WHITE),
                chess.KNIGHT: t_board.pieces(chess.KNIGHT, chess.WHITE),
                chess.PAWN: t_board.pieces(chess.PAWN, chess.WHITE)
            },
            chess.BLACK: {
                chess.KING: t_board.pieces(chess.KING, chess.BLACK),
                chess.QUEEN: t_board.pieces(chess.QUEEN, chess.BLACK),
                chess.ROOK: t_board.pieces(chess.ROOK, chess.BLACK),
                chess.BISHOP: t_board.pieces(chess.BISHOP, chess.BLACK),
                chess.KNIGHT: t_board.pieces(chess.KNIGHT, chess.BLACK),
                chess.PAWN: t_board.pieces(chess.PAWN, chess.BLACK)
            }
        }
        pw = pieces[chess.WHITE]
        pb = pieces[chess.BLACK]
        unions = {
            chess.WHITE: pw[chess.KING].union(pw[chess.QUEEN].union(
                pw[chess.ROOK].union(pw[chess.BISHOP].union(pw[chess.KNIGHT].union(pw[chess.PAWN]))))),
            chess.BLACK: pb[chess.KING].union(pb[chess.QUEEN].union(
                pb[chess.ROOK].union(pb[chess.BISHOP].union(pb[chess.KNIGHT].union(pb[chess.PAWN])))))
        }
        k_positions = {
            chess.Piece.from_symbol('K'): chess.lsb(pieces[chess.WHITE][chess.KING].mask),
            chess.Piece.from_symbol('k'): chess.lsb(pieces[chess.BLACK][chess.KING].mask)
        }
        w_count, b_count = self.getTotalMaterial(pieces)

        m_count = w_count+b_count
        # Total material is approximately 83 (including 2.5 for each king)
        if (len(t_board.pieces(chess.QUEEN, chess.WHITE)) == 0
                and len(t_board.pieces(chess.QUEEN, chess.BLACK)) == 0
                and m_count < 45) or m_count < 30:
            self.table_reference[chess.KING] = self.KING_TABLE_END_GAME
            self.game_phase = "endgame"
        elif self.table_reference[chess.KING] == self.KING_TABLE_END_GAME:
            self.table_reference[chess.KING] = self.KING_TABLE
            self.game_phase = "opening"
        # Legal moves if you can move into check
        pseudo_m_legal_moves = t_board.pseudo_legal_moves
        if self.game_phase != "endgame" and (pseudo_m_legal_moves.count() >= 40 or m_count <= 76 or self.out_of_book):
            self.game_phase = "middlegame"

        # Dictionaries to define the mobility of each piece and what they can capture and if those captures are tempos
        moving_map = {}
        capture_count = {}
        attacking_map = {}
        tempo_count = 0

        squares_by_black_king_white_controls = 0
        squares_by_white_king_black_controls = 0
        # "Patzer sees a check, gives a check" - Bobby Fischer
        if t_board.is_check():
            if t_board.turn == chess.WHITE:
                evaluation -= self.CHECK_BONUS
                tempo_count += 1
            else:
                evaluation += self.CHECK_BONUS
                tempo_count -= 1
        checkmates_threatened = 0
        # Determines which pieces defend what.  The more defended pieces the better.
        defense_map = {}
        # Connected rook bonus
        wcr_bonus = False
        bcr_bonus = False
        # Used to evaluate pawn structure.  Doubled pawns bad.  Isolated pawns bad.  Doubled isolated pawns really bad.
        w_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
        b_pawns = [0, 0, 0, 0, 0, 0, 0, 0]
        # Strictly material advantage
        mat_eval = 0
        # Used for calculations that require both the rank and file of each pawn.  In format [file, rank, color]
        pawn_map = []
        # Where the kings are

        # To tell if the queen/king share a file with the opponent's rooks
        w_q_file = None
        b_q_file = None
        w_rook_files = []
        b_rook_files = []

        # Iterates through all of the pieces
        for key, value in piece_map.items():
            # m value used to either add for white or subtract for black
            m = 1
            # Looks on tables to see where good squares are
            if value.color == chess.BLACK:
                m = -1
                evaluation -= self.table_reference[value.piece_type][chess.square_mirror(key)] / 100
            else:
                evaluation += self.table_reference[value.piece_type][key] / 100
            # Which pieces can attack what
            attacking_map[key] = t_board.attacks(key)
            # How many captures each piece has
            capture_count[key] = attacking_map[key].intersection(unions[not value.color]).__len__()
            # Locations of pieces with a higher values than this piece
            running_higher_pieces = chess.SquareSet()
            for k, v in pieces[not value.color].items():
                if self.PIECE_VALUES[k] > self.PIECE_VALUES[value.piece_type]+0.5:
                    running_higher_pieces = running_higher_pieces.union(v.intersection(attacking_map[key]))
            tempo_count += m * running_higher_pieces.__len__()
            # Generates moving map for non-pawns
            can_move = False
            if value.piece_type != chess.PAWN:
                moving_map[key] = attacking_map[key] - attacking_map[key].intersection(unions[value.color])
                can_move = True
            if value.piece_type != chess.KING:
                p_a = t_board.attackers(value.color, key)
                defense_map[key] = p_a
            else:
                p_a = chess.SquareSet()
            # Non pawn evaluation operations
            if value.piece_type != chess.PAWN:
                # Good to put rooks in front of queens
                if value.piece_type == chess.QUEEN:
                    if m == 1 and w_q_file is None:
                        w_q_file = chess.square_file(key)
                    elif m == 1:
                        w_q_file = -1
                    elif b_q_file is None:
                        b_q_file = chess.square_file(key)
                    else:
                        b_q_file = -1
                elif value.piece_type == chess.ROOK:
                    if m == 1:
                        w_rook_files.append(chess.square_file(key))
                    else:
                        b_rook_files.append(chess.square_file(key))
                if can_move:
                    # Adds mobility and capturability bonus
                    if value.piece_type != chess.QUEEN or self.game_phase != "opening":
                        evaluation += m * math.sqrt(len(moving_map[key])
                                                    * self.PIECE_MOBILITY_BONUS + capture_count[key]
                                                    * self.PIECE_CAN_CAPTURE_BONUS)

                # Adds bonus if pieces are defended
                if p_a.__len__() >= 1:
                    # NBR piece operations
                    if value.piece_type == chess.ROOK \
                            or value.piece_type == chess.KNIGHT \
                            or value.piece_type == chess.BISHOP:
                        evaluation += m * self.PIECE_DEFENDED_BONUS
                        # Adds slightly smaller bonus if pieces are defended multiple times
                        if len(defense_map[key]) >= 2:
                            evaluation += m * self.PIECE_DEFENDED_AGAIN_BONUS
                        if value.piece_type == chess.ROOK:
                            # Adds connected rook bonus
                            if (not wcr_bonus and m == 1) or (not bcr_bonus and m == -1):
                                for i in defense_map[key]:
                                    if piece_map[i].piece_type == chess.ROOK:
                                        evaluation += self.CONNECTED_ROOKS_BONUS
                                        if m == 1:
                                            wcr_bonus = True
                                        else:
                                            bcr_bonus = True
                # Determines tempos off of smaller pieces
                else:
                    lower_pieces = unions[not value.color] - running_higher_pieces
                    lower_attackers = t_board.attackers(not value.color, key).intersection(lower_pieces)
                    attacks = t_board.attacks(key)
                    intersection = lower_attackers.intersection(attacks)
                    tempo_count -= m * (len(list(lower_attackers)) - len(list(intersection)))

            # Pawn bonuses
            else:
                # How far the pawn is pushed
                if value.color == chess.WHITE:
                    p_adv = chess.square_rank(key)
                else:
                    p_adv = (8-chess.square_rank(key))
                # If it is the endgame, it is advantageous to have your king near you opponents pawns
                # It is also advantageous to have your king near your own pawns in defense, but not as much
                if self.game_phase == "endgame":
                    if value.color == chess.WHITE:
                        evaluation += math.pow((chess.square_distance(k_positions[chess.Piece.from_symbol('k')], key)),
                                               2)*self.KING_ATTACK_PAWNS_BONUS
                        evaluation -= math.pow((chess.square_distance(k_positions[chess.Piece.from_symbol('K')], key)),
                                               2) * self.KING_DEFEND_PAWNS_BONUS
                    else:
                        evaluation += math.pow((chess.square_distance(k_positions[chess.Piece.from_symbol('k')], key)),
                                               2) * self.KING_DEFEND_PAWNS_BONUS
                        evaluation -= math.pow((chess.square_distance(k_positions[chess.Piece.from_symbol('K')], key)),
                                               2) * self.KING_ATTACK_PAWNS_BONUS
                # Creates pawn map to determine which pawns are passed
                pawn_map.append([chess.square_file(key), chess.square_rank(key), value.color])
                # Negative bonus for blocked pawns
                if self.isBlocked(key):
                    f = chess.square_file(key)
                    if (f == 2 or f == 3 or f == 4) or self.game_phase == "endgame":
                        evaluation -= m*self.CDE_PAWN_BLOCKED_NEGATIVE_BONUS*math.sqrt(p_adv)
                    else:
                        evaluation -= m*self.PAWN_BLOCKED_NEGATIVE_BONUS*math.sqrt(p_adv)

                # It is good if pawns are advanced.  Especially with less material on board.
                if value.color == chess.WHITE:
                    w_pawns[chess.square_file(key)] += 1
                    evaluation += self.PAWN_ADVANCEMENT_BONUS * p_adv/math.pow(b_count, 0.75)

                else:
                    b_pawns[chess.square_file(key)] += 1
                    evaluation -= self.PAWN_ADVANCEMENT_BONUS * p_adv/math.pow(w_count, 0.75)
                # It is good if pawns are defended by either a pawn or a non-pawn.  But non-pawn defense is better.
                if key in defense_map.keys():
                    non_pawn = False
                    for i in defense_map[key]:
                        if piece_map[i].piece_type != chess.PAWN:
                            non_pawn = True

                    if non_pawn:
                        evaluation += m*self.PAWN_PROTECTED_BY_NON_PAWN_BONUS/math.pow(m_count, 0.3)
                    else:
                        evaluation += m*self.PAWN_PROTECTED_BY_PAWN_BONUS/math.pow(m_count, 0.3)
        # Adds tempo bonus
        mult = 1
        if tempo_count < 0:
            mult = -1
        t_bonus = mult * math.pow(tempo_count, 2) * self.TEMPO_BONUS

        evaluation += t_bonus
        # Threaten checkmate good

        evaluation += checkmates_threatened*self.THREATEN_CHECKMATE_BONUS
        # It is good to still be able to castle.  Don't want to reward this too much though, as otherwise it could
        # deincentivize castling
        if t_board.has_castling_rights(chess.WHITE):
            evaluation += self.CAN_CASTLE_BONUS
        if t_board.has_castling_rights(chess.BLACK):
            evaluation -= self.CAN_CASTLE_BONUS
        # Rook in front of king/queen good
        if self.game_phase != "endgame":
            if w_q_file is not None and w_q_file != -1 and w_q_file in b_rook_files:
                evaluation -= self.ROOK_OPPOSE_KQ
            if b_q_file is not None and b_q_file != -1 and b_q_file in w_rook_files:
                evaluation += self.ROOK_OPPOSE_KQ
            if chess.square_file(k_positions[chess.Piece.from_symbol('K')]) in b_rook_files:
                evaluation -= self.ROOK_OPPOSE_KQ
            if chess.square_file(k_positions[chess.Piece.from_symbol('k')]) in w_rook_files:
                evaluation += self.ROOK_OPPOSE_KQ

        # Determines who has more pieces than their opponent
        w_minus_pawns = w_count - pieces[chess.WHITE][chess.PAWN].__len__() * self.PIECE_VALUES[chess.PAWN]
        b_minus_pawns = b_count - pieces[chess.BLACK][chess.PAWN].__len__() * self.PIECE_VALUES[chess.PAWN]
        pawn_eval = (pieces[chess.WHITE][chess.PAWN].__len__() * math.sqrt(w_count / b_count)
                     - pieces[chess.BLACK][chess.PAWN].__len__() * math.sqrt(b_count / w_count)) \
                     * self.PIECE_VALUES[chess.PAWN]
        piece_eval = (w_minus_pawns-b_minus_pawns) * self.PIECE_VALUE_MULTIPLIER

        # Material evaluation is modified based on who has more stuff.  If you're up material, trade pieces, keep pawns.
        # If you're down material, keep pieces trade pawns.
        piece_eval *= math.sqrt(max(w_minus_pawns, b_minus_pawns) / min(w_minus_pawns, b_minus_pawns))
        pawn_eval *= self.PIECE_VALUE_MULTIPLIER
        evaluation += piece_eval+pawn_eval
        o_pawns = w_pawns

        m = 1
        # Performs more pawn operations.  Goes through list twice.  Once for each side
        for c in range(2):
            # Switches sides
            if c == 1:
                o_pawns = b_pawns
                m = -1
            # Isolated, or doubled disadvantages
            for i in range(len(o_pawns)):
                if self.isIsolated(o_pawns, i):
                    if o_pawns[i] > 1:
                        evaluation -= m * (o_pawns[i]-1) * self.DOUBLED_ISOLATED_PAWN_NEGATIVE_BONUS
                    else:
                        evaluation -= m * self.ISOLATED_PAWN_NEGATIVE_BONUS
                elif w_pawns[i] > 1:
                    evaluation -= m * (o_pawns[i] - 1) * self.DOUBLED_PAWN_NEGATIVE_BONUS
       # The following numbers are used to determine unstoppable passed pawns by rule of the square
        min_unstop_black = 999
        min_unstop_white = 999
        for i in pawn_map:
            if i[2] == chess.WHITE:
                o_pawns = b_pawns
                m = 1
                advancement = i[1]
            else:
                o_pawns = w_pawns
                m = -1
                advancement = 8-i[1]
            pawn_square = chess.square(i[0], i[1])
            if self.isPassed(pawn_map, pawn_square, o_pawns):
                # Passed pawn bonus
                evaluation += m * self.PASSED_PAWN_BONUS*math.pow(advancement, 1.5)/math.pow(m_count, 0.3)
                # This program *incorrectly* assumes that unstoppable passed pawns can only occur in the endgame
                # However, as the way it is checking if a pawn is unstoppable by rule of the square, it doesn't matter
                if self.game_phase == "endgame":
                    # Takes the pawn map of the side of the evaluated pawn
                    if m == 1:
                        po = pb

                        # To account for moving up two
                        if i[1] == 1:

                            pawn_square = chess.square(i[0], i[1]+1)

                    else:
                        po = pw
                        # To account for moving up two
                        if i[1] == 6:
                            pawn_square = chess.square(i[0], i[1] - 1)
                    # If there is no material
                    if len(po[chess.QUEEN]) == 0 and len(po[chess.ROOK]) == 0 and len(po[chess.BISHOP]) == 0 and len(po[chess.KNIGHT]) == 0:
                        if i[2] == chess.WHITE:
                            qr = 7
                        else:
                            qr = 0
                        # The square you are aiming for, 8th rank for white, 1st for black
                        queening_square = chess.square(i[0], qr)
                        # Penalty of 1 if it is not your turn
                        o_turn_penalty = 0
                        if t_board.turn != i[2]:
                            o_turn_penalty = 1
                        # Penalty of 1 if your king is in the way
                        king_in_way_penalty = 0
                        if ((chess.square_rank(t_board.king(i[2])) > chess.square_rank(pawn_square) and i[2] == chess.WHITE)\
                            or (chess.square_rank(t_board.king(i[2])) < chess.square_rank(pawn_square) and i[2] == chess.BLACK))\
                            and chess.square_file(t_board.king(i[2])) == i[0]:
                            king_in_way_penalty = 2
                        pawn_dist = chess.square_distance(pawn_square, queening_square)\
                                    + o_turn_penalty\
                                    + king_in_way_penalty

                        # Checks to see which is closer to the queening square, the pawn or the king
                        # This currently doesn't account for two stoppable passers which can't both be stopped
                        if pawn_dist < chess.square_distance(t_board.king(not i[2]), queening_square):
                            # Sets minimum unstoppable distance for that side
                            if m == 1:
                                if pawn_dist < min_unstop_white:
                                    min_unstop_white = pawn_dist
                            else:
                                if pawn_dist < min_unstop_black:
                                    min_unstop_black = pawn_dist

        # A generality, but normally whoever is closer to making a queen is much better.  Adds queen value for side
        # which is closer.  So, four unstoppable pawns on the first rank is worse than 1 unstoppable pawn on the fourth
        diff = abs(min_unstop_black - min_unstop_white)
        if diff > 0:
            m = 1
            if min_unstop_white > min_unstop_black:
                m = -1
            evaluation += m*(self.PIECE_VALUES[chess.QUEEN]-self.PIECE_VALUES[chess.PAWN]-1)*self.PIECE_VALUE_MULTIPLIER

        # Determines how exposed the king is.  King should be safe.
        k_e = self.generateKingExposure(t_board.copy(), k_positions, unions)

        # The more pieces leave the board, the less king exposure matters
        w_mult = 1
        b_mult = 1
        if chess.Piece.from_symbol('q') in piece_map.values():
            w_mult = self.OPPONENT_QUEEN_KING_SAFETY_NEGATIVE_MULTIPLIER
        if chess.Piece.from_symbol('Q') in piece_map.values():
            b_mult = self.OPPONENT_QUEEN_KING_SAFETY_NEGATIVE_MULTIPLIER
        w_n_bonus = w_mult*math.sqrt(k_e[0] * self.KING_EXPOSURE_NEGATIVE_VALUE)/math.sqrt(max(1, 45-b_count))
        b_n_bonus = b_mult*math.sqrt(k_e[1] * self.KING_EXPOSURE_NEGATIVE_VALUE)/math.sqrt(max(1, 45-w_count))
        evaluation -= w_n_bonus
        evaluation += b_n_bonus

        # It is good to control squares around your opponent's king
        evaluation -= math.sqrt(squares_by_white_king_black_controls * self.SQUARES_BY_KING_OPPOSITE_CONTROLS_BONUS)
        evaluation += math.sqrt(squares_by_black_king_white_controls * self.SQUARES_BY_KING_OPPOSITE_CONTROLS_BONUS)
        # Having kings which are close to each other favors the side with more material
        proximity_multiplier = math.sqrt(abs(max(w_count, b_count)/min(w_count, b_count)))
        if b_count > w_count:
            proximity_multiplier *= -1
        evaluation -= (chess.square_distance(k_positions[chess.Piece.from_symbol('K')], k_positions[chess.Piece.from_symbol('k')])*self.KING_PROXIMITY_BONUS * proximity_multiplier)/math.sqrt(m_count)

        return evaluation
    # Determines if the position is a draw
    def checkDrawClaimable(self, t_board):
        if t_board.can_claim_fifty_moves() or t_board.is_repetition(3):
            return True
    # Converts the position evaluation to be an evaluation for one side
    def staticEvaluation(self, t_board):
        piece_count = chess.popcount(self.board.occupied_co[0])+chess.popcount(self.board.occupied_co[1])

        m = 1
        if t_board.turn == chess.BLACK:
            m = -1
        if piece_count <= 5:
            self.in_tablebase = True
            WDL = self.getSingleEndgameTablebaseEvaluation()
            if 1 >= WDL >= -1:
                evaluation = 0
            else:
                evaluation = WDL * (4000-self.current_depth)

            if m*evaluation*-1 < 0:

                evaluation = m * self.positionEvaluation(t_board)
        else:
            evaluation = m*self.positionEvaluation(t_board)
        return evaluation
    # Generates the files, ranks, and color of each pawn
    def generatePawnMap(self, piece_map):
        pawn_map = []
        for key, value in piece_map.items():
            if value.piece_type == chess.PAWN:
                pawn_map.append([chess.square_file(key), chess.square_rank(key), value.color])
        return pawn_map
    # Determines if a pawn is isolated
    def isIsolated(self, p_array, index):
         if p_array[index]>0:
             if index == 0:
                 if p_array[1] == 0:
                     return True
             elif index == 7:
                 if p_array[6] == 0:
                     return True
             else:
                 if p_array[index+1] == 0 and p_array[index-1] == 0:
                     return True
         return False
    # Determines if a pawn is passed
    def isPassed(self, pawn_map, pawn_square, p_array=None):
        if p_array is None:
            p_array = [1, 1, 1, 1, 1, 1, 1, 1]
        pf = chess.square_file(pawn_square)
        pr = chess.square_rank(pawn_square)
        pc = self.board.color_at(pawn_square)
        if p_array[max(0, pf - 1)] == 0 and p_array[pf] == 0 and p_array[min(7, pf + 1)] == 0:
            return True
        else:
            for i in pawn_map:
                if i[2] != pc:
                    if pf - 1 <= i[0] <= pf + 1:
                        if (pc == chess.WHITE and i[1] > pr) or (pc == chess.BLACK and i[1] < pr):
                            return False
        return True
    # Determines if a pawn is blocked or not, assumes inputted key is a pawn
    def isBlocked(self, key):
        if self.board.color_at(key) == chess.WHITE:
            rank_to = chess.square_rank(key) + 1
        else:
            rank_to = chess.square_rank(key) - 1
        if self.board.piece_at(chess.square(chess.square_file(key), rank_to)) is not None:
            return True
        return False
    # How far a given pawn is away from queening
    def distFromQueening(self, square):
        if self.board.color_at(square) == chess.WHITE:
            return 8 - chess.square_rank(square)
        else:
            return chess.square_rank(square) - 1
    # Determines how much material is on board
    def getTotalMaterial(self, pieces):
        w_count = 0
        b_count = 0
        for key, value in pieces.items():
            #print(key)
            #print(value)
            for k, v in value.items():
                if k != chess.KING:
                    if key == chess.WHITE:
                        w_count += self.PIECE_VALUES[k]*v.__len__()
                    else:
                        b_count += self.PIECE_VALUES[k]*v.__len__()
                else:
                    if key == chess.WHITE:
                        w_count += 2.5
                    else:
                        b_count += 2.5
        return w_count, b_count
    # Determines king exposure by using the method Alan Turing recommended in his program "Turbochamp".
    # Places a same color queen on the king's square and calculates that piece's mobility
    # Reduces that side's evaluation by the square root of how many squares that queen can go
    def generateKingExposure(self, t_board, k_positions, unions):
        w_king_exposure = 0
        b_king_exposure = 0
        # Iterates through king locations
        for value, key in k_positions.items():
            # Switches out the king for a same color queen
            q_value = chess.Piece.from_symbol('q')
            q_value.color = value.color

            t_board.set_piece_at(key, q_value)
            t_board.turn = value.color
            exposure = (t_board.attacks(key) - unions[chess.WHITE] - unions[chess.BLACK]).__len__()
            if t_board.turn == chess.WHITE:
                w_king_exposure += exposure
            else:
                b_king_exposure += exposure
            t_board.set_piece_at(key, value)
        return w_king_exposure, b_king_exposure
    # References an endgame tablebase
    # WDL means win/draw/loss.
    # WDL = 2 means that the endgame is a win for the moving side within the 50 move rule.
    # WDL = 1 means that the endgame is a win for the moving side, but it is prevented by the 50 move rule.
    # WDL = 0 means the endgame is drawn
    # WDL = -1 means that the endgame is a loss for the moving side, but it is prevented by the 50 move rule.
    # WDL = -2 means that the endgame is a loss for the moving side within the 50 move rule.
    # DTZ means "Distance to Zeroing" is a term determining the fewest moves before a checkmate, capture, or pawn move
    # TODO: Make the program strive to win better, but drawn positions
    def endgameTablebase(self):

        dtz = None
        wdl = None
        best_move = chess.Move.null()
        # Should remain the same with optimal play
        start_wdl = self.tb.probe_wdl(self.board)
        if start_wdl < 0:
            defending_side = self.board.turn
        else:
            defending_side = not self.board.turn
        # This took me longer than I am willing to admit.
        # Finding the way to minimax this tablebase optimally is more difficult than it looks.
        for i in self.board.legal_moves:
            # Captures and pawn moves zero the move
            is_zero = False
            # For ensuring that all dtz values are positive
            defending = not (defending_side == self.board.turn)
            if self.board.is_zeroing(i):
                is_zero = True
            self.board.push(i)
            # If it is not zeroing, determine distance until zeroing
            if not is_zero:
                move_dtz = self.tb.probe_dtz(self.board)
                # To Ensure all DTZ positive
                if move_dtz < 0:
                    move_dtz *= -1




            else:
                move_dtz = 0
            # Is the genereated position a W/D/L?
            """if defending_side == chess.BLACK:
                m = -1
            else:
                m = 1"""
            move_wdl = self.tb.probe_wdl(self.board)*-1
            # So that it knows checkmate is good
            if self.board.is_checkmate():
                self.board.pop()
                return move_wdl, i
            # Threefold repetition is a draw
            if self.board.can_claim_threefold_repetition():
                move_dtz = 0
                move_wdl = 0

            # dadwashere
            # Hi Dad!
            self.board.pop()
            # No point in looking over moves which worsen our position!
            if move_wdl < start_wdl:
                continue
            # Sets DTZ if there is none
            if dtz is None:
                dtz = move_dtz
                wdl = move_wdl
                best_move = i
            # Winning side finds the fastest possible victory, losing side finds the slowest possible defeat
            elif (move_dtz < dtz and defending) or (move_dtz > dtz and not defending):

                dtz = move_dtz
                wdl = move_wdl
                best_move = i
        print("DTZ: " + str(dtz))
        print("WDL: " + str(wdl))
        return wdl*-1, best_move
    # Tablebase Evaluation of a specific position
    def getSingleEndgameTablebaseEvaluation(self):

        start_wdl = self.tb.probe_wdl(self.board)

        return start_wdl

