import socket
import threading
from time import sleep

clients = []
client_names = []

letters_to_numbers = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
                      'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}

player1board = [['· '] * 7 for x in range(7)]
player1health = 12

player2board = [['· '] * 7 for x in range(7)]
player2health = 12

game_start = False

def drawboard(board):
    for i in range(0,7): 
        print()
        if i == 0:
            print('  A  B  C  D  E  F  G ')
        print(i, end= ' ')
        for j in range(0,7):
            print(board[i][j], end='  ')
    print()

def checkboardspot(board, checking, row, column):
        if board[row][column] == checking:
            return 0
        else:
            return 1

def recieve_message(client, addr):
    global player1health, player2health
    print("Started thread ", threading.current_thread())

    client_name = client.recv(1024).decode('utf-8')
    print(client_name)

    if len(clients) < 2:
        client.send("welcome1".encode('utf-8'))
    else:
        client.send("welcome2".encode('utf-8'))

    client_names.append(client_name)

    p1 = clients[0].recv(4096).decode('utf-8')
    print(threading.current_thread(), p1)
    p2 = clients[1].recv(4096).decode('utf-8')
    print(threading.current_thread(), p2)

    n = 0
    for i in range(0, 7):
        for j in range(0, 7):
            player1board[i][j] = p1[n]
            player2board[i][j] = p2[n]
            n += 1

    print('Done setting up', threading.current_thread())

    while True:
        data = client.recv(1024).decode('utf-8')
        print(data)

        if not data:
            break
        if player1health == 0:
            print('Player2 won!')
            clients[0].send('You lost'.encode('utf-8'))
            clients[1].send('You win'.encode('utf-8'))
            break
        elif player2health == 0:
            print('Player1 won!')
            clients[0].send('You win'.encode('utf-8'))
            clients[1].send('You lost'.encode('utf-8'))
            break

        if client == clients[0]:
            clients[1].send("yourturn".encode('utf-8'))
            sleep(0.2)

            column = data[0]
            intcolumn = letters_to_numbers[column]
            row = data[1]
            introw = int(row)
            guess = column + row
            result = checkboardspot(player2board, 'O', introw, intcolumn)
            # P1 hit P2
            if result == 0:
                print('HITP2')
                guess0 = guess + '+guesshit'
                clients[0].send(guess0.encode('utf-8'))
                guess1 = guess + '+ownhit'
                clients[1].send(guess1.encode('utf-8'))
                player2health -= 1
                print(player2health)
            # P1 missed P2
            else:
                print('MISSEDP2')
                guess0 = guess + '+guessmiss'
                clients[0].send(guess0.encode('utf-8'))
                guess1 = guess + '+ownmiss'
                clients[1].send(guess1.encode('utf-8'))

            clients[1].send(data.encode('utf-8'))
            clients[0].send('good'.encode('utf-8'))
        else:
            clients[0].send("yourturn".encode('utf-8'))
            sleep(0.2)

            column = data[0]
            intcolumn = letters_to_numbers[column]
            row = data[1]
            introw = int(row)
            guess = column + row
            result = checkboardspot(player1board, 'O', introw, intcolumn)
            # P2 hit P1
            if result == 0:
                print('HITP1')
                guess0 = guess + '+ownhit'
                clients[0].send(guess0.encode('utf-8'))
                guess1 = guess + '+guesshit'
                clients[1].send(guess1.encode('utf-8'))
                player1health -= 1
                print(player1health)
            # P2 missed P1
            else:
                print('MISSEDP1')
                guess0 = guess + '+ownmiss'
                clients[0].send(guess0.encode('utf-8'))
                guess1 = guess + '+guessmiss'
                clients[1].send(guess1.encode('utf-8'))

            clients[0].send(data.encode('utf-8'))
            clients[1].send('good'.encode('utf-8'))

    idx = getidx(client)
    del client_names[idx]
    del clients[idx]
    client.close()
    print("Ended thread ", threading.current_thread())
    
def start_server():
    serversoc = socket.socket()
    port = 52063
    serversoc.bind(("localhost", port))
    serversoc.listen(5)

    thnum = 1
    while True:
        if len(clients) < 2:
            print("Listening on port: ", port)
            client, addr = serversoc.accept()
            clients.append(client)
            tid = threading.Thread(name="thr_{}".format(thnum), target=recieve_message, args=(client,addr,))
            thnum = thnum + 1
            tid.setDaemon(True)
            tid.start()
        sleep(0.2)

    serversoc.close()

def getidx(client):
    idx = 0
    for conn in clients:
        if conn == client:
            break
        idx = idx + 1
    return idx

if __name__ == "__main__":
    start_server()
