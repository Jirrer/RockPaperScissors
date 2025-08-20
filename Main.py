import pygame, sys, math, random

class Game:
    board = {}

    def startGame(self):
        pygame.init()

        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.cameraX, self.cameraY = 0, 0
        self.dragging = False
        self.mousePosition = (0, 0)

    def createBoard(self):
        startingX, startingY = 100, 300
        rowLength = 20
        
        for row in range(rowLength):
            x, y = startingX, startingY

            for i in range(rowLength):
                self.board[x, y] = False

                x += 75
                y += math.sqrt(3) - (1.732 * 50) / 2

            x, y = startingX, startingY
            x += 75
            y += math.sqrt(3) + (1.732 * 50) / 2

            for i in range(rowLength- 1):
                self.board[x, y] = False

                x += 75
                y += math.sqrt(3) + (1.732 * 50) / 2
            
            startingX += 150
            rowLength -= 1

            print(len(self.board))



    def updateBoard(self):
        for tile in self.board:
            screen_pos = (tile[0] - self.cameraX, tile[1] - self.cameraY)
            pygame.draw.polygon(self.screen, (255, 0, 0), self.hexagon(screen_pos))
            pygame.draw.polygon(self.screen, (255, 255, 255), self.hexagon(screen_pos), 3)

    def removeRandomTile(self):
        boardArray = list(self.board)

        tileToRemove = boardArray[random.randint(0, len(boardArray) - 1)]

        del self.board[tileToRemove]

    def hexagon(self, center):
        cx, cy = center

        points = []

        for i in range(6):
            angle = i * (360 / 6)
            rad = angle * 3.14159 / 180
            x = cx + 50 * math.cos(rad)
            y = cy + 50 * math.sin(rad)
            points.append((x,y))

        return points


    def main(self):
        self.createBoard()
        self.startGame()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or len(self.board) == 0:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.dragging = True
                        self.mousePosition = event.pos 

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.dragging = False
                    elif event.button == 1:
                        self.removeRandomTile()

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        mx, my = event.pos
                        dx_move = mx - self.mousePosition[0]
                        dy_move = my - self.mousePosition[1]
                        self.cameraX -= dx_move 
                        self.cameraY -= dy_move
                        self.mousePosition = event.pos
            

            self.screen.fill((0, 0, 0))

            self.updateBoard()

            pygame.display.flip()

            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.main()