import pygame as pg
import math
import chess
import time as impt
import datetime as impdt
import sys
# UI Class
class view_board():
    # Initial calling
    def __init__(self, board ="", side=chess.WHITE):
        self.color1 = "tan"
        self.color2 = "sienna"
        self.bcolor = "black"
        self.size = 80
        self.gameDisplay = pg.display.set_mode((self.size * 10, self.size * 10))
        self.board = board
        self.squares = []
        self.time = {chess.WHITE: 1, chess.BLACK: 1}
        self.board = self.board.replace(" ", "")
        self.board = self.board.replace("\n", "")
        pg.font.init()

        #"chessalpha2"
        self.font = pg.font.SysFont("chessalpha2", 80)
        self.font2 = pg.font.SysFont("times new roman", 30)
        self.font3 = pg.font.SysFont("times new roman", 200)
        pg.init()
        pg.display.set_caption("Gecko")

        #self.drawBoard()
    # Setup board
    def setBoard(self, board):
        self.board = board
        self.board = self.board.replace(" ", "")
        self.board = self.board.replace("\n", "")
    # Draws main menu and awaits user interaction
    def drawMainMenu(self):
        STgecko = self.font3.render("Gecko", True, "darkslategrey")
        STchess = self.font3.render("Chess", True, "darkslategrey")
        STplay = self.font2.render("Play", True, "whitesmoke")
        STplus = self.font2.render("+", True, "whitesmoke")
        STminus = self.font2.render("-", True, "whitesmoke")
        STstarting = self.font2.render("Starting time", True, "whitesmoke")

        STincrement = self.font2.render("Increment", True, "whitesmoke")
        STwhitegecko = self.font2.render("Gecko", True, "black")
        STwhitehuman = self.font2.render("Human", True, "black")
        STblackgecko = self.font2.render("Gecko", True, "white")
        STblackhuman = self.font2.render("Human", True, "white")

        white = "human"
        black = "gecko"
        #STanalysis = self.font2.render("Analysis", True, "whitesmoke")
        self.gameDisplay.fill(self.bcolor)
        self.gameDisplay.blit(STgecko, (self.size*1.7, self.size * 0))
        self.gameDisplay.blit(STchess, (self.size*1.7, self.size * 2.2))

        buttons = []
        buttons.append(pg.draw.rect(self.gameDisplay, "darkslategrey",
                                    [self.size * 2.5, self.size * 5.7, self.size, self.size]))
        buttons.append(
            pg.draw.rect(self.gameDisplay, "darkslategrey", [self.size * 2.5, self.size * 8.7, self.size, self.size]))
        buttons.append(pg.draw.rect(self.gameDisplay, "darkslategrey",
                                    [self.size * 6.5, self.size * 5.7, self.size, self.size]))
        buttons.append(
            pg.draw.rect(self.gameDisplay, "darkslategrey", [self.size * 6.5, self.size * 8.7, self.size, self.size]))
        buttons.append(
            pg.draw.rect(self.gameDisplay, "darkslategrey",
                         [self.size * 4, self.size * 6.7, self.size * 2, self.size * 2]))
        buttons.append(
            pg.draw.rect(self.gameDisplay, "white",
                         [self.size * 0.25, self.size * 7.2, self.size * 1.25, self.size * 1]))
        buttons.append(
            pg.draw.rect(self.gameDisplay, "white",
                         [self.size * 8.5, self.size * 7.2, self.size * 1.25, self.size * 1]))
        pg.draw.rect(self.gameDisplay, "black",
                     [self.size * 8.53, self.size * 7.23, self.size * 1.21, self.size * 0.96])

        self.gameDisplay.blit(STwhitehuman, (self.size * 0.3, self.size * 7.5))
        self.gameDisplay.blit(STblackgecko, (self.size * 8.65, self.size * 7.5))

        self.gameDisplay.blit(STplus, (self.size * 2.9, self.size * 6))
        self.gameDisplay.blit(STminus, (self.size * 2.9, self.size * 9))
        self.gameDisplay.blit(STplus, (self.size * 6.9, self.size * 6))
        self.gameDisplay.blit(STminus, (self.size * 6.9, self.size * 9))
        self.gameDisplay.blit(STplay, (self.size * 4.7, self.size * 7.4))

        self.gameDisplay.blit(STstarting, (self.size * 2.15, self.size * 5.1))

        self.gameDisplay.blit(STincrement, (self.size * 6.2, self.size * 5.1))

        #self.gameDisplay.blit(STanalysis, (self.size * 4.35, self.size * 7.3))

        mins = 3
        inc = 2
        STmins = self.font2.render(str(mins), True, "whitesmoke")
        STinc = self.font2.render(str(inc), True, "whitesmoke")
        self.gameDisplay.blit(STmins, (self.size * 2.9, self.size * 7.5))
        self.gameDisplay.blit(STinc, (self.size * 6.9, self.size * 7.5))
        pg.display.update()
        while(True):
            ev = pg.event.get()
            # proceed events
            for event in ev:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # handle MOUSE BUTTON UP
                if event.type == pg.MOUSEBUTTONUP:
                    pg.draw.rect(self.gameDisplay, self.bcolor,
                                 [self.size * 2.5, self.size * 6.7, self.size, self.size*2])
                    pg.draw.rect(self.gameDisplay, self.bcolor,
                                 [self.size * 6.5, self.size * 6.7, self.size, self.size*2])
                    pos = pg.mouse.get_pos()
                    clicked_buttons = [s for s in range(len(buttons)) if buttons[s].collidepoint(pos)]
                    try:
                        n = clicked_buttons[0]

                    except:
                        continue
                    if n == 0:
                        mins+=1
                    elif n ==1:
                        if mins>=2:
                            mins-=1
                    elif n == 2:
                        inc += 1
                    elif n == 3:
                        if inc>=1:
                            inc-=1
                    elif n == 4:
                        return [white, black, mins, inc]
                    elif n == 5:
                        if white == "human":
                            white = "gecko"
                            pg.draw.rect(self.gameDisplay, "white",
                                         [self.size * 0.25, self.size * 7.2, self.size * 1.25, self.size * 1])
                            self.gameDisplay.blit(STwhitegecko, (self.size * 0.35, self.size * 7.5))
                        else:
                            white = "human"
                            pg.draw.rect(self.gameDisplay, "white",
                                         [self.size * 0.25, self.size * 7.2, self.size * 1.25, self.size * 1])
                            self.gameDisplay.blit(STwhitehuman, (self.size * 0.3, self.size * 7.5))
                    elif n == 6:
                        if black == "human":
                            black = "gecko"
                            pg.draw.rect(self.gameDisplay, "white",
                                         [self.size * 8.5, self.size * 7.2, self.size * 1.25, self.size * 1])
                            pg.draw.rect(self.gameDisplay, "black",
                            [self.size * 8.53, self.size * 7.23, self.size * 1.21, self.size * 0.96])
                            self.gameDisplay.blit(STblackgecko, (self.size * 8.65, self.size * 7.5))
                        else:
                            black = "human"
                            pg.draw.rect(self.gameDisplay, "white",
                                         [self.size * 8.5, self.size * 7.2, self.size * 1.25, self.size * 1])
                            pg.draw.rect(self.gameDisplay, "black",
                            [self.size * 8.53, self.size * 7.23, self.size * 1.21, self.size * 0.96])
                            self.gameDisplay.blit(STblackhuman, (self.size * 8.6, self.size * 7.5))
                    STmins = self.font2.render(str(mins), True, "whitesmoke")
                    STinc = self.font2.render(str(inc), True, "whitesmoke")
                    self.gameDisplay.blit(STmins, (self.size * 2.9, self.size * 7.5))
                    self.gameDisplay.blit(STinc, (self.size * 6.9, self.size * 7.5))
                    pg.display.update()
    # Draws board
    def drawBoard(self, side=chess.WHITE, update = True):


        self.gameDisplay.fill(self.bcolor)

        color = self.color1
        self.squares = []
        for i in range(8):
            if color == self.color1:
                color = self.color2
            else:
                color = self.color1
            for j in range(8):
                if color == self.color1:
                    color = self.color2
                else:
                    color = self.color1

                self.drawPiece(i, j, color, side)
        pg.draw.rect(self.gameDisplay, "black", [self.size, self.size, 8 * self.size, 8 * self.size], 1)
        self.displayTime(side)
        if update:
            pg.display.update()
    # Draws gaem over and awaits user interaction
    def displayGameOver(self, sideWhoWon, side):
        STwhitewins = self.font2.render("White Wins!", True, "white")
        STblackwins = self.font2.render("Black Wins!", True, "grey")
        STdraw = self.font2.render("Draw!", True, "white")
        STplayagain = self.font2.render("Play again?", True, "white")
        if sideWhoWon is not None:
            if side:
                if sideWhoWon == chess.WHITE:
                    self.gameDisplay.blit(STwhitewins, (self.size * 9-STwhitewins.get_rect().width, self.size * 9.2))
                elif sideWhoWon == chess.BLACK:
                    self.gameDisplay.blit(STblackwins, (self.size * 9-STblackwins.get_rect().width, self.size * 0.5))
            else:
                if sideWhoWon == chess.BLACK:
                    self.gameDisplay.blit(STblackwins, (self.size * 9-STwhitewins.get_rect().width, self.size * 9.2))
                elif sideWhoWon == chess.WHITE:
                    self.gameDisplay.blit(STwhitewins, (self.size * 9-STblackwins.get_rect().width, self.size * 0.5))
        else:
            self.gameDisplay.blit(STdraw, (self.size * 9 - STdraw.get_rect().width, self.size * 9.2))
            self.gameDisplay.blit(STdraw, (self.size * 9 - STdraw.get_rect().width, self.size * 0.5))
        buttons = []
        buttons.append(
            pg.draw.rect(self.gameDisplay, "darkslategrey",
                         [self.size * 4, self.size * 9.2, self.size * 2, self.size * 0.5]))
        self.gameDisplay.blit(STplayagain, (self.size * 5-STplayagain.get_rect().width/2, self.size * 9.2))
        pg.display.update()
        while (True):
            ev = pg.event.get()
            # proceed events
            for event in ev:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # handle MOUSE BUTTON UP
                if event.type == pg.MOUSEBUTTONUP:

                    pos = pg.mouse.get_pos()
                    clicked_buttons = [s for s in range(len(buttons)) if buttons[s].collidepoint(pos)]
                    try:
                        n = clicked_buttons[0]

                    except:
                        continue
                    if n == 0:
                        return True
    # Converts piece character to chessalpha2
    def convertCharacter(self, character):
        c = character.lower()
        rc = c
        if c == '.':
            return ' '
        elif c == 'r':
            rc = "L"
        elif c == 'n':
            rc = "K"
        elif c == 'b':
            rc = "J"
        elif c == 'q':
            rc = "M"
        elif c == 'k':
            rc = "N"
        elif c == 'p':
            rc = "I"
        return rc
    # Draws an individual piece
    def drawPiece(self, i, j, color, side):
        if side == chess.BLACK:
            di, dj = 7 - i, 7 - j
        else:
            di, dj = i, j
        self.squares.append(
            pg.draw.rect(self.gameDisplay, color, [self.size * (dj + 1), self.size * (di + 1), self.size, self.size]))
        ch = self.board[i * 8 + j]
        horizontal_multiplier = (1 / 7)
        if ch.lower() == 'p' or ch.lower() == 'r':
            horizontal_multiplier = 1 / 4
        elif ch.lower() == 'b' or ch.lower() == 'n':
            horizontal_multiplier = 2 / 11
        if ch.islower():
            piece_color = "black"
        else:
            piece_color = "white"
        ch = self.convertCharacter(ch)
        img = self.font.render(ch, True, piece_color)
        self.gameDisplay.blit(img, (
        self.size * (dj + 1) + self.size * horizontal_multiplier, self.size * (di + 1) + self.size * (1 / 15)))
    # Displays how much time each side has
    def displayTime(self, side):
        img = self.font2.render( str(math.floor(self.time[chess.WHITE] / 60)) + ":" + str(math.floor(self.time[chess.WHITE] % 60)), True, "white")

        img2 = self.font2.render(
        str(math.floor(self.time[chess.BLACK] / 60)) + ":" + str(math.floor(self.time[chess.BLACK] % 60)), True,
            "grey")
        pg.draw.rect(self.gameDisplay, "black",
                     [self.size, self.size * 9.15, self.size * 2, self.size * 0.5])
        pg.draw.rect(self.gameDisplay, "black",
                     [self.size, self.size * 0.45, self.size * 2, self.size * 0.5])
        if side:
            self.gameDisplay.blit(img, (self.size, self.size * 9.2))
            self.gameDisplay.blit(img2, (self.size, self.size * 0.5))
        else:
            self.gameDisplay.blit(img, (self.size, self.size * 0.5))
            self.gameDisplay.blit(img2, (self.size, self.size * 9.2))
    # Changes time variable
    def setTime(self, time):
        self.time = time
    # Awaits user interaction and returns move
    def getMove(self, chessboard, time):
        STresign = self.font2.render("Resign", True, "white")
        buttons = []
        buttons.append(
            pg.draw.rect(self.gameDisplay, "darkslategrey",
                         [self.size * 4, self.size * 9.2, self.size * 2, self.size * 0.5]))
        self.gameDisplay.blit(STresign, (self.size * 5-STresign.get_rect().width/2, self.size * 9.2))
        pg.display.update()
        held_square = ""
        held_piece = "q"
        t1 = impdt.datetime.now()
        update_time = t1
        while True:
            if (impdt.datetime.now()-update_time).total_seconds() > 1:
                update_time = impdt.datetime.now()
                if chessboard.turn == chess.WHITE:
                    self.setTime({chess.WHITE: max(0, time-(impdt.datetime.now()-t1).total_seconds()), chess.BLACK: self.time[chess.BLACK]})
                else:
                    self.setTime({chess.BLACK: max(0, time - (impdt.datetime.now() - t1).total_seconds()),
                                  chess.WHITE: self.time[chess.WHITE]})
                if self.time[chessboard.turn] <= 0:
                    return "time", 0
                self.displayTime(chessboard.turn)

                pg.display.update()

            ev = pg.event.get()

            for event in ev:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                #handle keyboard promote options
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_n or event.key == pg.K_k:
                        held_piece = "n"
                    elif event.key == pg.K_r:
                        held_piece = "r"
                    elif event.key == pg.K_b:
                        held_piece = "b"
                    elif event.key == pg.K_q:
                        held_piece = "q"
                # handle MOUSE BUTTON UP
                if event.type == pg.MOUSEBUTTONUP:
                    self.drawBoard(chessboard.turn, update=False)
                    pos = pg.mouse.get_pos()
                    pg.draw.rect(self.gameDisplay, "darkslategrey",
                                 [self.size * 4, self.size * 9.2, self.size * 2, self.size * 0.5])
                    self.gameDisplay.blit(STresign, (self.size * 5 - STresign.get_rect().width / 2, self.size * 9.2))
                    pg.display.update()


                    if pos[0]<self.size or pos[0] >self.size*9 or pos[1] < self.size or pos[1] >self.size*9:
                        clicked_buttons = [s for s in range(len(buttons)) if buttons[s].collidepoint(pos)]
                        try:
                            n = clicked_buttons[0]
                            if n == 0:
                                return "resign", time - (impdt.datetime.now() - t1).total_seconds()
                        except:
                            continue
                        continue
                    clicked_squares = [s for s in range(len(self.squares)) if self.squares[s].collidepoint(pos)]
                    n = clicked_squares[0]
                    i = math.floor(n/8)
                    j = n%8
                    #if chessboard.turn == chess.BLACK:
                    #    i, j = 7-i, 7-j
                    if held_square == "":
                        self.drawPiece(i, j, "limegreen", chessboard.turn)
                    pg.display.update()
                    rank = str(8-i)
                    file = chr(j+ord('a'))
                    sq = file+rank
                    if held_square != "":

                        if sq == held_square:
                            held_square=""
                        else:
                            try_move = held_square+sq

                            try:

                                if (rank == "8" or rank == "1") and chessboard.piece_type_at(chess.parse_square(held_square)) == chess.PAWN:

                                    try_move += held_piece
                                move = chessboard.parse_uci(try_move)

                            except:

                                print("Illegal move!")
                                self.drawPiece(i, j, "red", chessboard.turn)
                                pg.display.update()
                                impt.sleep(0.2)
                                held_square = ""
                                held_piece = "q"
                                self.drawBoard(chessboard.turn, update=False)
                                pg.draw.rect(self.gameDisplay, "darkslategrey",
                                             [self.size * 4, self.size * 9.2, self.size * 2, self.size * 0.5])
                                self.gameDisplay.blit(STresign, (self.size * 5-STresign.get_rect().width/2, self.size * 9.2))
                                pg.display.update()
                                continue

                            time_left = time-(impdt.datetime.now()-t1).total_seconds()
                            return chessboard.san(move), time_left
                    else:
                        held_square = sq


