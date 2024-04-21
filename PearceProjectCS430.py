import tkinter as tk
import random
import sys
from functools import partial

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
DEPTH = 6

class ConnectFourGame:
    def columnIsPlayable(self, coins, x):
        if coins[x] == 0:
                return True
        return False

    def simulateMove(self, coins, x, playerNum):
        newPosition = list(coins)
        for j in range(5, -1, -1):
            if newPosition[j*BOARD_WIDTH + x] == 0:
                newPosition[j*BOARD_WIDTH + x] = playerNum
                break
        return newPosition

    def evaluatePosition(self, coins, playerNum, depth):
        winner = self.checkForWin(coins)
        #print(winner)
        if winner != False:
            winner = 1 if (winner == "red") else 2
            score = (DEPTH - depth) if winner == playerNum else (depth - DEPTH)
            return score
        elif depth < DEPTH:

            minScore = (depth + 1) - DEPTH
            enemyMoves = []
            enemyNum = 2 if playerNum == 1 else 1
            #print(minScore)
            #print(maxScore)
            for i in [3,4,2,1,0,5,6]:
                if self.columnIsPlayable(coins, i):
                    tcoins = self.simulateMove(coins, i, enemyNum)
                    thisMoveScore = -self.evaluatePosition(tcoins, enemyNum, depth + 1)
                    if thisMoveScore <= minScore:
                        #print(enemyMoves)
                        #print(thisMoveScore)
                        #print("yellow" if playerNum == 2 else "red")
                        return thisMoveScore
                    else:
                        enemyMoves.append(thisMoveScore)
            #print(enemyMoves)
            if len(enemyMoves) > 0:
                score = min(enemyMoves)
            else:
                score = 0
            return score
        else:
            return 0

    def AIPlay(self):
        moves = []
        move = 0
        playerNum = 1 if self.redTurn else 2
        for x in range(BOARD_WIDTH):
            if self.columnIsPlayable(self.coins, x):
                moves.append(self.evaluatePosition(self.simulateMove(self.coins, x, playerNum), playerNum, 0))
            else:
                moves.append(-999)

        print(moves)
        # If there are multiple 'best' moves pick a random one
        bestCount = moves.count(max(moves))
        moveIndex = random.randint(0, bestCount - 1)
        for mv in moves:
            if mv == max(moves):
                
                if moveIndex == 0:
                    break
                else:
                    moveIndex -= 1
                
            move += 1
        
        #print(move) 
        return move

    def placeCoin(self, x):
        for j in range(5, -1, -1):
            if self.coins[j*7 + x] == 0:
                if self.redTurn:
                    fillColor = "red"
                    coinVal = 1
                    self.redTurn = False
                else:
                    fillColor = "yellow"
                    coinVal = 2
                    self.redTurn = True
                self.coinCanvases[(j)*7 + x].delete("all")
                self.coins[j*7 + x] = coinVal
                self.coinCanvases[(j)*7 + x].create_oval(5, 5, 135, 135, fill=fillColor, outline="white", width=0)
                break
        # Check for and handle a win 
        winner = self.checkForWin(self.coins)
        if winner != False:
            winDialog = tk.Label(self.root, text=str(winner) + " wins", font=("arial", 50))
            winDialog.place(x=450, y=450)
            for b in self.buttons:
                b.destroy()
            return True
        elif self.cpuFirst:
            if self.redTurn == True and self.pve:
                self.placeCoin(self.AIPlay())

        elif self.redTurn == False and self.pve:
                self.placeCoin(self.AIPlay())
        return False

    def checkForWinOnSlot(self, coins, x, y):
        checkRight = True
        checkDown = True
        checkDownRight = True
        checkDownLeft = True
        foundWin = False
        if x < 3:
            checkDownLeft = False
        if x > 3:
            checkDownRight = False
            checkRight = False
        if y > 2:
            checkDown = False
            checkDownLeft = False
            checkDownRight = False
        if checkRight:
            if coins[y*BOARD_WIDTH + x] == coins[y*BOARD_WIDTH + x + 1] == coins[y*BOARD_WIDTH + x + 2] ==coins[y*BOARD_WIDTH + x + 3]:
                foundWin = True
        if checkDown and not foundWin:
             if coins[(y)*BOARD_WIDTH + x] == coins[(y+1)*BOARD_WIDTH + x] == coins[(y+2)*BOARD_WIDTH + x] ==coins[(y+3)*BOARD_WIDTH + x]:
                foundWin = True
        if checkDownRight and not foundWin:
             if coins[(y)*BOARD_WIDTH + x] == coins[(y+1)*BOARD_WIDTH + x + 1] == coins[(y+2)*BOARD_WIDTH + x + 2] ==coins[(y+3)*BOARD_WIDTH + x + 3]:
                foundWin = True
        if checkDownLeft and not foundWin:
             if coins[(y)*BOARD_WIDTH + x] == coins[(y+1)*BOARD_WIDTH + x - 1] == coins[(y+2)*BOARD_WIDTH + x - 2] ==coins[(y+3)*BOARD_WIDTH + x - 3]:
                foundWin = True
        if foundWin:
            if coins[y*BOARD_WIDTH + x] == 1:
                foundWin = "red"
            elif coins[y*BOARD_WIDTH + x] == 2:
                foundWin = "yellow"
        return foundWin
                       
    def checkForWin(self, coins):
        result = False
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if coins[y*BOARD_WIDTH + x] == 0:
                    continue
                else:
                    result = self.checkForWinOnSlot(coins, x, y)
                    if result != False:
                        return result

        return result

    def __init__(self) -> None:
        global DEPTH
        self.pve = True
        self.eve = False
        self.cpuFirst = False
        if len(sys.argv) > 1: 
            if sys.argv[1] == "pvp":
                self.pve = False
            elif sys.argv[1] == "evp":
                self.cpuFirst = True
            elif sys.argv[1] == "eve":
                self.eve = True
            else:
                DEPTH = int(sys.argv[1])

        # Initialize game variables
        self.redTurn = True
        self.coins = []

        # Initialize tkinter GUI variables
        self.root = tk.Tk()
        self.root.geometry("1000x1000")
        self.root.title("Connect-4")
        self.slots = tk.Frame(self.root)
        self.buttons = []
        self.coinCanvases = []
        for j in range(BOARD_HEIGHT + 1):
            self.slots.rowconfigure(j, weight=1)
            for i in range(BOARD_WIDTH):
                self.slots.columnconfigure(i, weight=1)
                if j == 0:
                    self.buttons.append(tk.Button(self.slots, text=str(i), font=("arial", 16), command=partial(self.placeCoin, i)))
                    self.buttons[i].grid(row=j, column=i, sticky="news")
                else:
                    self.coins.append(0)   
                    self.coinCanvases.append(tk.Canvas(self.slots, width=0, height=0, bg="blue"))
                    self.coinCanvases[(j-1)*7 + i].create_oval(5, 3, 135, 133, fill="white", outline="white", width=0)
                    self.coinCanvases[(j-1)*7 + i].grid(row=j, column=i, sticky="news")

        self.slots.pack(fill="both", expand=True)
        if self.cpuFirst:
            self.placeCoin(self.AIPlay())
        if self.eve:
            for b in self.buttons:
                b.destroy()
            self.evePlay()
        self.root.mainloop()
        
    def evePlay(self):
        gameOver = self.placeCoin(self.AIPlay())
        if not gameOver:
            self.root.after(50, self.evePlay)

ConnectFourGame()
