import pygame, sys, math, random, Player, NPC

class Game:
    board = {}
    NPCs = []
    player = Player.Player()

    def main(self):
        self.startGame()
        self.createPlayers()
        self.createBoard()
        self.populateBoard()

        self.rockImage = pygame.image.load("graphics/Rock.png").convert_alpha()
        self.rockImage = pygame.transform.scale(self.rockImage, (50, 50)) 

        self.paperImage = pygame.image.load("graphics/Paper.png").convert_alpha()
        self.paperImage = pygame.transform.scale(self.paperImage, (50, 50)) 

        self.scissorsImage = pygame.image.load("graphics/Scissors.png").convert_alpha()
        self.scissorsImage = pygame.transform.scale(self.scissorsImage, (50, 50)) 

        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or len(self.board) == 0:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.dragging = True
                        self.mousePosition = event.pos 

                    elif event.button == 1:
                        self.removeRandomTile()
                        self.populateBoard()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        mx, my = event.pos
                        dx_move = mx - self.mousePosition[0]
                        dy_move = my - self.mousePosition[1]
                        self.cameraX -= dx_move 
                        self.cameraY -= dy_move
                        self.mousePosition = event.pos
            
            self.screen.blit(self.background, (0, 0))

            self.updateBoard()

            pygame.display.flip()

            self.clock.tick(60)

    def startGame(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.cameraX, self.cameraY = 0, 0
        self.dragging = False
        self.mousePosition = (0, 0)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        WIDTH, HEIGHT = self.screen.get_size()
        self.background = pygame.image.load("graphics\\skybackground.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def createPlayers(self):
        for x in range(3):
            newNPC = NPC.NPC("Paper")
            self.NPCs.append(newNPC)

        for x in range(3):
            newNPC = NPC.NPC("Rock")
            self.NPCs.append(newNPC)

        for x in range(3):
            newNPC = NPC.NPC("Scissors")
            self.NPCs.append(newNPC)

    def createBoard(self):
        startingX, startingY = 100, 300
        rowLength = 20
        
        for row in range(rowLength):
            x, y = startingX, startingY

            for i in range(rowLength):
                self.board[x, y] = False

                x += 75
                y += math.sqrt(3) - (1.732 * 50) / 2

            x, y = startingX + 75, startingY + math.sqrt(3) + (1.732 * 50) / 2
    
            for i in range(rowLength- 1):
                self.board[x, y] = False

                x += 75
                y += math.sqrt(3) + (1.732 * 50) / 2
            
            startingX += 150
            rowLength -= 1

    def populateBoard(self):
        boardArray = list(self.board)

        for player in self.NPCs:
            index = random.randint(0, len(boardArray) - 1)

            player.cords = boardArray[index]
            boardArray.remove(boardArray[index])


    def removeRandomTile(self):
        boardArray = list(self.board)

        tileToRemove = boardArray[random.randint(0, len(boardArray) - 1)]

        del self.board[tileToRemove]

    def updateBoard(self):
        for tile in self.board:
            screen_pos = (tile[0] - self.cameraX, tile[1] - self.cameraY)
            pygame.draw.polygon(self.screen, (117, 0, 0), self.hexagon(screen_pos))
            pygame.draw.polygon(self.screen, (255, 255, 255), self.hexagon(screen_pos), 3)

        for player in self.NPCs:
            playerTile = player.cords
            screen_pos = (playerTile[0] - self.cameraX, playerTile[1] - self.cameraY)

            if player.playerType == "Rock": self.screen.blit(self.rockImage, (screen_pos[0] - 25, screen_pos[1] - 25))
            elif player.playerType == "Paper": self.screen.blit(self.paperImage, (screen_pos[0] - 25, screen_pos[1] - 25))
            elif player.playerType == "Scissors": self.screen.blit(self.scissorsImage, (screen_pos[0] - 25, screen_pos[1] - 25))

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

if __name__ == "__main__":
    game = Game()
    game.main()