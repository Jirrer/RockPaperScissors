import pygame, sys, math

class Game:
    # board = [(300, 300), (375, 343.30),(375, 256.70)]
    board = []

    def startGame(self):
        pygame.init()

        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def createBoard(self):
        startingX, startingY = 100, 300
        rowLength = 7
        
        for row in range(rowLength):
            x, y = startingX, startingY

            for i in range(rowLength):
                self.board.append([[x, y], False])

                x += 75
                y += math.sqrt(3) - (1.732 * 50) / 2

            x, y = startingX, startingY
            x += 75
            y += math.sqrt(3) + (1.732 * 50) / 2

            for i in range(rowLength- 1):
                self.board.append([[x, y], False])

                x += 75
                y += math.sqrt(3) + (1.732 * 50) / 2
            
            startingX += 150
            rowLength -= 1

            print(len(self.board))



    def updateBoard(self):
        for tile in self.board:
            if tile:
                pygame.draw.polygon(self.screen, (255, 0, 0), self.hexagon((tile[0])))
                pygame.draw.polygon(self.screen, (255, 255, 255), self.hexagon((tile[0])), 3)

     

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
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))

            self.updateBoard()

            pygame.display.flip()

            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.main()