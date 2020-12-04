# Controls how the game functions

import chess
import chess.pgn
import random
import pyximport; pyximport.install()
import datetime
import math
testing = False
# Conditional imports because it takes awhile to import cython classes
if not testing:
    import cython_brain
    import cython_brain_mat_only
else:
    import brain

# Game controller class, must be functional with both UI and lichess API
class game:
    # Class initializer
    def __init__(self, FEN = chess.STARTING_FEN):
       self.board = chess.Board(fen=FEN)


       self.lichessPlay = False
       self.tb = chess.syzygy.open_tablebase("./Gecko_Bot/3-4-5piecesSyzygy/3-4-5")
       f = open("board.SVG", "w")
       boardsvg = chess.svg.board(board=self.board)
       f.write(boardsvg)
       f.close()

       self.pgn = chess.pgn.Game()
       self.node = self.pgn
       time = 180,2#self.getTime()
       self.time = {chess.WHITE: time[0], chess.BLACK: time[0]}
       self.increment = time[1]
       self.t1, self.t2 = datetime.datetime.now(), datetime.datetime.now()

    # Makes a mvoe on the board
    def move(self, mover="human", move=None):
        self.legal_moves = self.movesToList()
        moved = True
        if not self.lichessPlay:
            self.t1 = datetime.datetime.now()
            if self.time[chess.WHITE] < 0 or self.time[chess.BLACK] < 0:
                return self.clockFlag(not self.board.turn)
        print("White Time: " +
              str(math.floor(self.time[chess.WHITE] / 60)) + ":" + str(math.floor(self.time[chess.WHITE] % 60)) +
              "\nBlack Time: " +
              str(math.floor(self.time[chess.BLACK] / 60)) + ":" + str(math.floor(self.time[chess.BLACK] % 60)))
        if move is not None:
            print(move)
            self.board.push(self.board.parse_san(move))
            return False
        while True:


            move_inputted = chess.Move.null()
            if mover == "human":
                    print("What do you want to do?")
                    input_given = input()
                    if input_given.lower() == "back":
                        self.board.pop()
                        self.board.pop()
                        self.node = self.node.parent.parent

                        print(self.board)

                        continue
                    elif input_given.lower() == "resign":
                        if self.board.turn == chess.WHITE:
                            return "0-1"
                        else:
                            return "1-0"
                    try:
                        move_inputted = self.board.parse_san(input_given)
                    except:
                        print("Illegal move!")

                        continue
            elif mover == "random":
                move_inputted = self.legal_moves[random.randint(0, len(self.legal_moves)-1)]

            elif mover == "bot" or mover == "gecko":

                if not testing:
                    b = cython_brain.brain(self.board, self.tb)
                    t = min(1000*max(self.time[self.board.turn]-7, 0.1)/max(15, 40-self.board.fullmove_number+max(0, 15-self.board.fullmove_number)), 100000)
                else:
                    b = brain.brain(self.board, self.tb)
                    t = min(900*max(self.time[self.board.turn]-7, 0.1)/max(15, 40-self.board.fullmove_number+max(0, 15-self.board.fullmove_number)), 100000)

                print("Allocating "+str(t)+" time.")
                move_inputted = b.findMove(time=t)
            elif mover == "mat":

                b = cython_brain_mat_only.brain(self.board, self.tb)
                t = 150000

                move_inputted = b.findMove(time=t)
            self.board.push(move_inputted)

            self.node = self.node.add_main_variation(move_inputted)


            break
        if not self.lichessPlay:

            self.t2 = datetime.datetime.now()
            self.time[not self.board.turn] += (self.t2 - self.t1).total_seconds() * -1 + self.increment
        return False
    # How to handle a game being over
    def gameOver(self):

        if self.board.is_game_over() or self.board.is_repetition(3) or self.board.can_claim_fifty_moves():
            self.tb.close()
            if self.time[chess.WHITE] < 0:

                return self.clockFlag(chess.WHITE)
            elif self.time[chess.BLACK] < 0:

                return self.clockFlag(chess.BLACK)
            return self.board.result(claim_draw=True)
        else:
            return False
    # Converts legalMoveGenerator to list
    def movesToList(self):
        list = []
        for i in self.board.legal_moves:
            list.append(i)
        return list
    # No longer used.  Gets time controls in text app
    def getTime(self):
        try:
            tc = input("What time control would you like to play? e.g. '3+2', '15+10', or 'Unlimited'\n")
            l = tc.split("+")
            secs = int(l[0])*60
            inc = int(l[1])
            return secs,inc
        except:
            return 9999,9999
    # Determines on clock flag whether the game is a win or a draw
    def clockFlag(self, side_who_flagged, remove_last = True):
        if remove_last:
            self.board.pop()
        if self.board.has_insufficient_material(not side_who_flagged):
            return "1/2-1/2"
        else:
            if side_who_flagged == chess.WHITE:
                return "0-1"
            else:
                return "1-0"

