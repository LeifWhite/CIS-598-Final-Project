
# Gecko, my chess engine, for my CIS-598 class

import chess.pgn
import chess.engine
import view_board
#import chess
import game

import pyximport; pyximport.install()

from datetime import date

today = date.today()
d1 = today.strftime("%Y.%m.%d")
# Main loop
while True:
    g = game.game()

    result = False
    # Starting position
    FEN = chess.STARTING_FEN
    #FEN = "2r3k1/1p2qpp1/p2rbn2/P1b4p/Rn6/2NBPN1P/1PQ2PP1/2B1K2R w K - 3 19"

    g.board = chess.Board(fen=FEN)
    # UI
    board = view_board.view_board(str(g.board))
    arr = board.drawMainMenu()
    # Time controls
    g.increment = arr[3]
    g.time = {chess.WHITE: arr[2]*60, chess.BLACK: arr[2]*60}
    g.pgn.setup(g.board)
    white_player = arr[0]
    black_player = arr[1]
    perspective = None
    if white_player != black_player:
        if white_player == "human":
            perspective = chess.WHITE
        else:
            perspective = chess.BLACK
    keep_perspective = False
    last_mover = chess.WHITE
    # Game loop
    while not result:
        print(g.board)
        # UI Board
        board.setBoard(str(g.board))
        board.setTime(g.time)
        # Draw board from which side
        if white_player == "human" and black_player == "human":
            board.drawBoard(g.board.turn)
        elif white_player == "gecko" and black_player == "gecko":
            board.drawBoard(chess.WHITE)
        else:
            board.drawBoard(perspective)
        if g.board.turn == chess.WHITE:
            move = None
            if white_player == "human":

                move, g.time[chess.WHITE] = board.getMove(g.board, g.time[chess.WHITE])

                g.time[chess.WHITE] += g.increment
            if move == "resign":
                result = "0-1"
                keep_perspective = True
            elif move == "time":
                result = g.clockFlag(chess.WHITE, remove_last=False)
                keep_perspective = True
            else:
                result = g.move(white_player, move=move)
                last_mover = chess.WHITE

        else:

            move = None
            if black_player == "human":

                move, g.time[chess.BLACK] = board.getMove(g.board, g.time[chess.BLACK])
                g.time[chess.BLACK] += g.increment
            if move == "resign":
                result = "1-0"
                keep_perspective = True
            elif move == "time":
                result = g.clockFlag(chess.WHITE, remove_last=False)
                keep_perspective = True
            else:
                result = g.move(black_player, move=move)
                last_mover = chess.BLACK

        if not result:
            result = g.gameOver()

        display_move = g.board.fullmove_number
        if g.board.turn == chess.WHITE:
            display_move-=1
        if not keep_perspective:
            print(str(display_move)+": "+g.board.peek().uci())
            print("\n")
    # PGN builder
    if white_player == "bot" or white_player == "gecko":
        white_player = "Gecko"
    elif white_player == "mat":
        white_player = "Gecko (Material Only)"
    if black_player == "bot" or black_player == "gecko":
        black_player = "Gecko"
    elif black_player == "mat":
        black_player = "Gecko (Material Only)"
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
    winner = None
    # Display winner and restart if necessary
    if result == "1-0":
        winner = chess.WHITE
    elif result == "0-1":
        winner = chess.BLACK
    else:
        winner = None
    if perspective is None:
        if keep_perspective:
            perspective = not last_mover
        else:
            perspective = last_mover


    board.setBoard(str(g.board))
    board.drawBoard(perspective)
    if not board.displayGameOver(winner, perspective):
        break

