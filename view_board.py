import pygame
pygame.init()
class view_board:
    # Size of squares
    def __init__(self):
        size = 20

        # board length, must be even
        boardLength = 8
        gameDisplay.fill(white)

        cnt = 0
        for i in range(1, boardLength + 1):
            for z in range(1, boardLength + 1):
                # check if current loop value is even
                if cnt % 2 == 0:
                    pygame.draw.rect(gameDisplay, white, [size * z, size * i, size, size])
                else:
                    pygame.draw.rect(gameDisplay, black, [size * z, size * i, size, size])
                cnt += 1
            # since theres an even number of squares go back one value
            cnt -= 1
        # Add a nice boarder
        pygame.draw.rect(gameDisplay, black, [size, size, boardLength * size, boardLength * size], 1)

    def display(self):
        pygame.display.update()