import chess.svg
import chess.pgn
#import chess
import game
import os
from datetime import date

#os.system('ls')
#print( open("./OmegaFifteen/3-4-5piecesSyzygy/3-4-5", "r").readlines() )
#import brain
#from IPython.display import SVG
today = date.today()
d1 = today.strftime("%Y.%m.%d")
g = game.game()
"""bbb = chess.Board(fen="7k/3rn3/8/3p4/2Q5/4N3/8/7K w - - 0 1")
b = brain.brain(bbb)
b.see(b.board, chess.D5, chess.WHITE)"""
result = False
FEN = chess.STARTING_FEN
#FEN = "4kbn1/8/8/8/8/8/8/4K3 w - - 0 1"
g.board = chess.Board(fen=FEN)
g.pgn.setup(g.board)
white_player = "bot"
black_player = "bot"
while not result:
    if g.board.turn == chess.WHITE:
        result = g.move(white_player)
    else:
        result = g.move(black_player)
    if not result:
        result = g.gameOver()
    print(g.board)
    #SVG(chess.svg.board(board=board, size=400))
    display_move = g.board.fullmove_number
    if g.board.turn == chess.WHITE:
        display_move-=1
    print(str(display_move)+": "+g.board.peek().uci())
    print("\n")
    f = open("board.SVG", "w")
    boardsvg = chess.svg.board(board=g.board)
    f.write(boardsvg)
    f.close()
if white_player == "bot":
    white_player = "Gecko"
if black_player == "bot":
    black_player = "Gecko"
g.pgn.headers = chess.pgn.Headers(Event='Training Match',
                                  Site='Local',
                                  Date=d1,
                                  Round='?',
                                  White=white_player.capitalize(),
                                  Black=black_player.capitalize(),
                                  Result=result,
                                  FEN=FEN)
print(result)
print("\n\n")
print(g.pgn)
"""
 boardsvg = chess.svg.board(board=board)
        f = open("board.SVG", "w")
        f.write(boardsvg)
        f.close()
"""