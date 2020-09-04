# Controls how the game functions

import chess
import chess.pgn
import random
import pyximport; pyximport.install()
import cython_brain

class game:

    def __init__(self, FEN = chess.STARTING_FEN):
       self.board = chess.Board(fen=FEN)

       f = open("board.SVG", "w")
       boardsvg = chess.svg.board(board=self.board)
       f.write(boardsvg)
       f.close()

       self.pgn = chess.pgn.Game()
       self.node = self.pgn
    def move(self, mover="human"):
        self.legal_moves = self.movesToList()
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

            elif mover == "bot":

                b = cython_brain.brain(self.board)
                t = 15000

                move_inputted = b.findMove(time=t)
            self.board.push(move_inputted)
            self.node = self.node.add_main_variation(move_inputted)


            break
        return False
    def gameOver(self):
        if self.board.is_game_over() or self.board.is_repetition(3) or self.board.can_claim_fifty_moves():

            return self.board.result(claim_draw=True)
        else:
            return False
    def movesToList(self):
        list = []
        for i in self.board.legal_moves:
            list.append(i)
        return list