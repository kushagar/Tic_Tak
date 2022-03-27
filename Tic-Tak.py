from ast import Continue
import time
import socket
import threading
class Board:
    def __init__(self) -> None:
        self.board = []
        for j in range(3):
            temp = ["e"]*3
            self.board.append(temp)

    def update_board(self, pos, val):
        if(self.board[pos[0]][pos[1]] == "e"):
            self.board[pos[0]][pos[1]] = val
            return True
        else:
            return False

    def checkwinner(self):
        winnersymbol = ""
        winnerFound = True
        # for symbol x
        for i in range(3):
            if(self.board[i][0] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][1] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][2] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[0][i] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[1][i] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[2][i] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][i] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][2-i] != "x"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "x"
            return winnerFound, winnersymbol
        # for symbol o
        for i in range(3):
            if(self.board[i][0] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][1] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][2] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[0][i] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[1][i] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[2][i] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][i] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        winnerFound = True
        for i in range(3):
            if(self.board[i][2-i] != "o"):
                winnerFound = False
        if(winnerFound):
            winnersymbol = "o"
            return winnerFound, winnersymbol
        return winnerFound, winnersymbol

    def give_board_state(self):
        string = ""
        for i in range(3):
            for j in range(3):
                if(j <= 1):
                    string += str(self.board[i][j])+" "
                else:
                    string += str(self.board[i][j])+"\n"
        return string


class player:
    def __init__(self, name, symbol) -> None:
        self.name = name
        self.symbol = symbol


addr = ("127.0.0.1", 5050)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
server.listen()
max_connections = 2
connections = 0
players = []
symbols = ["x", "o"]
i = 0
won, won_symbol = False, ""
turn = True
def playerThread(plr, client, board):
    global won, won_symbol, turn, connections
    while(connections != 2):
        Continue
    while(not won):
        while(not turn):
            continue
        if(won):
            client.send(board.give_board_state().encode())
            client.send("You Loose".encode())
            time.sleep(5)
            break
        turn = False
        client.send(board.give_board_state().encode()) 
        client.send("Enter row and column:".encode())   
        pos = client.recv(4096).decode().strip(" ")
        pos = pos.split(",")
        pos = [int(i) for i in pos]
        board.update_board(pos, plr.symbol)
        won, won_symbol = board.checkwinner()
        if(won):
            client.send(board.give_board_state().encode())
            client.send("You win".encode())
            time.sleep(5)
        turn = True
        time.sleep(1)
    connections -= 1
    print("closing thread",connections)
    client.close()
board = Board()
def main_thread():
    global connections, max_connections, board, i,players
    while True:
        if(connections < max_connections):
            while(i==2 and connections==1):
                continue
            if(i == 2 and connections==0):
                 break
            client, caddr = server.accept()
            client.send("Enter your name:".encode())
            name = client.recv(4096).decode().strip(" ")
            players.append([player(name, symbols[i]), client])
            i += 1
            connections += 1
            t = threading.Thread(target=playerThread, args=(
                players[i-1][0], players[i-1][1], board,))
            t.start()
main_thread()
server.close()
