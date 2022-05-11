import socket
import threading
from time import sleep

from numpy import take

your_turn = False

yourships = {'Ship': 'O', 'Hit': 'X', 'Miss': '/', 'noship': '·'}
enemyships = {'Hit': 'H', 'Miss': 'M', 'noattempt': '·'}
letters_to_numbers = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
                      'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6}
ship_sizes = [4, 3, 2, 2, 1]
playershipboard = [['· '] * 7 for x in range(7)]
playerguessboard = [['· '] * 7 for x in range(7)]
playerhealth = 12

def drawboard(board):
        for i in range(0,7): 
            print()
            if i == 0:
                print('  A  B  C  D  E  F  G ')
            print(i, end= ' ')
            for j in range(0,7):
                print(board[i][j], end=' ')
        print()

def checkboardspot(board, checking, row, column):
        if board[row][column] == checking:
            return 0
        else:
            return 1

def placeship2(board, size):
        print('You will be choosing the location for ship size', size)
        if size == 1:
            ship = input('Please type the location for your ship (Example: G6): ')
            if len(ship) != 2:
                print('Invalid input, please try again')
                return -1
            start_column = ship[0]
            start_row = ship[1]
            end_column = ship[0]
            end_row = ship[1]
        else:
            ship = input('Please type the starting and ending location for your ship, please put a space inbetween (Example: A0 D0): ')
            if len(ship) != 5:
                print('Invalid input, please try again')
                return -1
            arr = ship.partition(' ')
            start_column = arr[0][0]
            start_row = arr[0][1]
            end_column = arr[2][0]
            end_row = arr[2][1]
        
        # Check if input is valid
        if (start_column and end_column) not in ('ABCDEFGabcdefg') or (start_row and end_row) not in '0123456':
            print('Not a valid entry, please try again')
            return -1
        start_column = letters_to_numbers[start_column]
        end_column = letters_to_numbers[end_column]
        start_column = int(start_column)
        start_row = int(start_row)
        end_column = int(end_column)
        end_row = int(end_row)

        if start_column == end_column:
            if (abs(start_row - end_row)+1) != size:
                print('Wrong size ship given, please try again')
                return -1
            for x in range(start_row, end_row+1):
                if checkboardspot(board, 'O ', x, start_column) == 0:
                    print('There is already a ship in given locations, please try again')
                    return -1
                board[x][start_column] = 'O '
        elif start_row == end_row:
            if (abs(start_column - end_column)+1) != size:
                print('Wrong size ship given, please try again')
                return -1
            for x in range(start_column, end_column+1):
                if checkboardspot(board, 'O ', start_row, x) == 0:
                    print('There is already a ship in given locations, please try again')
                    return -1
                board[start_row][x] = 'O '
        else:
            print('Ships cannot go diagonally, please try again')
            return -1
        return 0

def placeships2(board, size, number):
    i = 0
    while i != number:
        check = placeship2(board, size[i])
        drawboard(board)
        if check == 0:
            i += 1

def takeshot(board):
    while True:
        guess = input('Please input a location to shoot at: ')
        column = int(letters_to_numbers[guess[0]])
        row = int(guess[1])
        if board[row][column] != '· ':
            print('You have already guess this, please try again')
            continue
        return guess

def replacechars(board):
    board = board.replace(' ', '')
    board = board.replace('[', '')
    board = board.replace(']', '')
    board = board.replace(',', '')
    board = board.replace("'", '')
    return board

def replacecell(board, character, row, column):
    board[row][column] = character

def connect():
    commsoc = socket.socket()
    commsoc.connect(("localhost", 52063))
    name = input("Enter your player name: ")
    commsoc.send(name.encode('utf-8'))
    
    recieve_message(commsoc)

def recieve_message(commsoc):
    global your_turn, playerguessboard, playershipboard, playerhealth, letters_to_numbers
    placeships2(playershipboard, ship_sizes, len(ship_sizes))

    board = str(playershipboard)
    board = replacechars(board)
    #print(board)
    commsoc.send(board.encode('utf-8'))
    sleep(0.2)
    commsoc.send(board.encode('utf-8'))

    while True:
        print('Recieving message')
        data = commsoc.recv(1024).decode('utf-8')
        print(data)
        if data == 'welcome1':
            your_turn = True

        if data == 'You lost' or playerhealth == 0:
            break
        elif data == 'You win':
            break

        if '+' in data:
            datalist = data.split('+')

            if datalist[1] == 'guesshit':
                replacecell(playerguessboard, 'H ', int(datalist[0][1]), int(letters_to_numbers[datalist[0][0]]))
            if datalist[1] == 'ownhit':
                replacecell(playershipboard, 'X ', int(datalist[0][1]), int(letters_to_numbers[datalist[0][0]]))
                playerhealth -= 1
            if datalist[1] == 'guessmiss':
                replacecell(playerguessboard, 'M ', int(datalist[0][1]), int(letters_to_numbers[datalist[0][0]]))
            if datalist[1] == 'ownmiss':
                replacecell(playershipboard, '/ ', int(datalist[0][1]), int(letters_to_numbers[datalist[0][0]]))

        drawboard(playerguessboard)
        drawboard(playershipboard)

        if your_turn:
            guess = takeshot(playerguessboard)
            #guess = input('Please input a location to shoot at: ')
            commsoc.send(guess.encode('utf-8'))
            your_turn = False

        elif data == 'yourturn':
            your_turn = True
            
if __name__ == "__main__":
    connect()
