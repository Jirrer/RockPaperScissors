import pygame, sys, math, random, Player, NPC

class Game:
    board = []
    NPCs = []
    player = Player.Player("Rock")
    tilesToKeep = []
    playerAllowedMoves = set()

    def main(self):
        self.startGame()
        self.createPlayers()
        self.createBoard()
        self.populateBoard()
        self.player.cords = self.board[0]

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
                        self.userMove(event.pos)
                        self.removeRandomTile()
                        self.npcMove()
                        self.checkOutcome()

                        if self.checkGameStatus(): pygame.quit(); sys.exit()

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
        for x in range(7):
            newNPC = NPC.NPC("Paper")
            self.NPCs.append(newNPC)

        for x in range(7):
            newNPC = NPC.NPC("Rock")
            self.NPCs.append(newNPC)

        for x in range(7):
            newNPC = NPC.NPC("Scissors")
            self.NPCs.append(newNPC)

    def createBoard(self):
        startingX, startingY = 100, 300
        rowLength = 20
        
        for row in range(rowLength):
            x, y = startingX, startingY

            for i in range(rowLength):
                self.board.append((x, y))

                x += 75
                y += math.sqrt(3) - (1.732 * 50) / 2

            x, y = startingX + 75, startingY + math.sqrt(3) + (1.732 * 50) / 2
    
            for i in range(rowLength- 1):
                self.board.append((x, y))

                x += 75
                y += math.sqrt(3) + (1.732 * 50) / 2
            
            startingX += 150
            rowLength -= 1

    def populateBoard(self):
        self.tilesToKeep = []

        boardArray = self.board.copy()

        for player in self.NPCs:
            index = random.randint(0, len(boardArray) - 1)

            player.cords = boardArray[index]
            boardArray.remove(boardArray[index])
            
            self.tilesToKeep.append(player.cords)

    def userMove(self, userCords):
        self.playerAllowedMoves = set(self.findNeighbors(userCords))
        self.player.cords = userCords

    def removeRandomTile(self):
        boardArray = self.board.copy()

        for tile in self.tilesToKeep:
            boardArray.remove(tile)

        tileToRemove = boardArray[random.randint(0, len(boardArray) - 1)]

        self.board.remove(tileToRemove)

    def npcMove(self):
        for player in self.NPCs:
            allowedMoves = self.findNeighbors(player.cords)

            player.cords = allowedMoves[random.randint(0, len(allowedMoves) - 1)]

    def findNeighbors(self, tile, max_neighbors=6):
        x, y = tile
        distances = []
        for bx, by in self.board:
            if (bx, by) != (x, y):
                d = math.dist((x, y), (bx, by))
                distances.append(((bx, by), d))
        # Sort by distance and pick closest 6
        distances.sort(key=lambda t: t[1])
        return [pos for pos, _ in distances[:max_neighbors]]
    
    def checkOutcome(self):
        to_remove = set()
        seenTiles = {}

        for player in self.NPCs:
            if player.cords not in seenTiles:
                seenTiles[player.cords] = [player]
            else:
                seenTiles[player.cords].append(player)

        for tile, players in seenTiles.items():
            if len(players) > 1:
                for i in range(len(players)):
                    for j in range(i + 1, len(players)):
                        p1, p2 = players[i], players[j]
                        if p1.playerType == p2.playerType:
                            continue
                        if (p1.playerType == "Rock" and p2.playerType == "Scissors") or \
                        (p1.playerType == "Scissors" and p2.playerType == "Paper") or \
                        (p1.playerType == "Paper" and p2.playerType == "Rock"):
                            to_remove.add(p2)
                        else:
                            to_remove.add(p1)

        self.NPCs = [npc for npc in self.NPCs if npc not in to_remove]

    def checkGameStatus(self):
        teamsAlive = set()

        for player in self.NPCs:
            if player.playerType not in teamsAlive: teamsAlive.add(player.playerType)

        if len(teamsAlive) == 1: return True
        else: return False

    def updateBoard(self):
        for tile in self.board:
            if tile in self.playerAllowedMoves:
                screen_pos = (tile[0] - self.cameraX, tile[1] - self.cameraY)
                pygame.draw.polygon(self.screen, (0, 102, 255), self.hexagon(screen_pos))
                pygame.draw.polygon(self.screen, (255, 255, 255), self.hexagon(screen_pos), 3)
            else:
                screen_pos = (tile[0] - self.cameraX, tile[1] - self.cameraY)
                pygame.draw.polygon(self.screen, (117, 0, 0), self.hexagon(screen_pos))
                pygame.draw.polygon(self.screen, (255, 255, 255), self.hexagon(screen_pos), 3)

        for player in self.NPCs:
            playerTile = player.cords
            screen_pos = (playerTile[0] - self.cameraX, playerTile[1] - self.cameraY)

            if player.playerType == "Rock": self.screen.blit(self.rockImage, (screen_pos[0] - 25, screen_pos[1] - 25))
            elif player.playerType == "Paper": self.screen.blit(self.paperImage, (screen_pos[0] - 25, screen_pos[1] - 25))
            elif player.playerType == "Scissors": self.screen.blit(self.scissorsImage, (screen_pos[0] - 25, screen_pos[1] - 25))

        playerTile = self.player.cords
        screen_pos = (playerTile[0] - self.cameraX, playerTile[1] - self.cameraY)

        if self.player.playerType == "Rock": self.screen.blit(self.rockImage, (screen_pos[0] - 25, screen_pos[1] - 25))
        elif self.player.playerType == "Paper": self.screen.blit(self.paperImage, (screen_pos[0] - 25, screen_pos[1] - 25))
        elif self.player.playerType == "Scissors": self.screen.blit(self.scissorsImage, (screen_pos[0] - 25, screen_pos[1] - 25))

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