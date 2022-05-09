# This code is for 2-players locally, I DON'T THINK IT WORKS OVER NETWORK
# But this is all the logic for playing battleship

class battleship(object):

    def __init__(self):
        self.yourships = {'Ship': 'O', 'Hit': 'X', 'noship': '·'}
        self.enemyships = {'Hit': 'H', 'Miss': 'M', 'noattempt': '·'}
        self.letters_to_numbers = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
        self.ship_sizes = [4, 3, 2, 2, 1]
        self.currentturn = 0

        self.p1shipboard = [['· '] * 7 for x in range(7)]
        self.p1guessboard = [['· '] * 7 for x in range(7)]
        self.p1health = 12

        self.p2shipboard = [['· '] * 7 for x in range(7)]
        self.p2guessboard = [['· '] * 7 for x in range(7)]
        self.p2health = 12

    def drawboard(self, board):
        for i in range(0,7): 
            print()
            if i == 0:
                print('  A  B  C  D  E  F  G ')
            print(i, end= ' ')
            for j in range(0,7):
                print(board[i][j], end=' ')
        print()

    # Checks for "checking" in the board ar postion ["row"]["column"]
    def checkboardspot(self, board, checking, row, column):
        if board[row][column] == checking:
            return 0
        else:
            return 1

    # Checks for winner based on health (Return Key: 1: winner, 0: no winner)
    def checkwinner(self, health1, health2):
        if health1 == 0:
            print('Player 2 is the winner!')
            return 1
        elif health2 == 0:
            print('Player 1 is the winner!')
            return 1
        return 0

    # Places size 1 ships; still needs work done for different wrong scenarios
    def placeships(self, board):
        ship = input('Please type the location you want your ship to be: ')
        column = ship[0]
        row = ship[1]
        row = int(row)

        while ship[0] not in 'ABCDEFG' or ship[1] not in '0123456':
            print('Not a valid entry, please try again')
            return
        column = self.letters_to_numbers[column]
        column = int(column)
        board[row][column] = 'O '

    # Places variable size ships
    def placeships2(self, board, size):
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
        if (start_column and end_column) not in ('ABCDEFG' or 'abcdegf') or (start_row and end_row) not in '0123456':
            print('Not a valid entry, please try again')
            return -1
        start_column = self.letters_to_numbers[start_column]
        end_column = self.letters_to_numbers[end_column]
        start_column = int(start_column)
        start_row = int(start_row)
        end_column = int(end_column)
        end_row = int(end_row)

        if start_column == end_column:
            if (abs(start_row - end_row)+1) != size:
                print('Wrong size ship given, please try again')
                return -1
            for x in range(start_row, end_row+1):
                if self.checkboardspot(board, 'O ', x, start_column) == 0:
                    print('There is already a ship in given locations, please try again')
                    return -1
                board[x][start_column] = 'O '
        elif start_row == end_row:
            if (abs(start_column - end_column)+1) != size:
                print('Wrong size ship given, please try again')
                return -1
            for x in range(start_column, end_column+1):
                if self.checkboardspot(board, 'O ', start_row, x) == 0:
                    print('There is already a ship in given locations, please try again')
                    return -1
                board[start_row][x] = 'O '
        else:
            print('Ships cannot go diagonally, please try again')
            return -1
        return 0

    # Shooting at enemy board; (Return Key: -1: error, 0: miss, 1: hit)
    def yourturn(self, guessboard, enemyboard):
        guess = input('Please input the location you would like to guess: ')
        column = guess[0]
        row = guess[1]
        # Check if input is valid
        if column not in ('ABCDEFG' or 'abcdegf') or row not in '0123456':
            print('Not a valid entry, please try again')
            return -1
        column = self.letters_to_numbers[column]
        column = int(column)
        row = int(row)
        
        # No guess made here
        if guessboard[row][column] == '· ':
            # Miss
            if enemyboard[row][column] == '· ':
                guessboard[row][column] = 'M '
                return 0
            # Hit
            elif enemyboard[row][column] == 'O ':
                guessboard[row][column] = 'H '
                enemyboard[row][column] = 'X '
                return 1
        # Guess already made here
        else:
            print('You have already guessed here, please try again')
            return -1
        return -1

    # 10x10 battleship; ship sizes = 5, 4, 3, 3, 2
    def normalbattleship(self):
        print('This modes is still under construction, please come back once its ready!')

    # 7x7 battleship, ship sizes = 4, 3, 2, 2, 1
    def minibattleship(self):
        print('Welcome to Mini-Battleship!')
        print('This board size is 7 x 7 with a size 4 ship, size 3 ship, two size 2 ships, and a size 1 ship')
        self.drawboard(self.p1shipboard)
        i = 0
        print('Player 1 is placing their ships!')
        while i != 5:
            check = self.placeships2(self.p1shipboard, self.ship_sizes[i])
            self.drawboard(self.p1shipboard)
            if check == 0:
                i += 1
        i = 0
        print('Player 2 is placing their ships!')
        while i != 5:
            check = self.placeships2(self.p2shipboard, self.ship_sizes[i])
            self.drawboard(self.p2shipboard)
            if check == 0:
                i += 1
        
        while True:
            if self.currentturn == 0:
                print('Player 1 is guessing!')
                self.drawboard(self.p1shipboard)
                self.drawboard(self.p1guessboard)
                result = self.yourturn(self.p1guessboard, self.p2shipboard)
                if result == 0:
                    print('Miss!')
                elif result == 1:
                    print('Hit!')
                    self.p2health -= 1
                elif result == -1:
                    continue
            elif self.currentturn == 1:
                print('Player 2 is guessing!')
                self.drawboard(self.p2shipboard)
                self.drawboard(self.p2guessboard)
                result = self.yourturn(self.p2guessboard, self.p1shipboard)
                if result == 0:
                    print('Miss!')
                elif result == 1:
                    print('Hit!')
                    self.p1health -= 1
                elif result == -1:
                    continue

            winner = self.checkwinner(self.p1health, self.p2health)
            if winner == 1:
                break
            else:
                if self.currentturn == 0:
                    self.currentturn = 1
                else:
                    self.currentturn = 0

    # 5x5 battleship, five ships all size 1
    def size1battleship(self):
        print('This modes is still under construction, please come back once its ready!')

    def playgame(self):
        while True:
            print('\nWelcome to Battleship!')
            print('The three different modes available are Normal battleship, mini-battleship, and One-Hit Wonders')
            print('0 = Normal Battleship: Standard 10 x 10 battleship with a size 5 ship, size 4 ship, two size 3 ships, and a size 2 ship!')
            print('1 = Mini-Battleship: 7 x 7 board with a size 4 ship, size 3 ship, two size 2 ships, and a size one ship!')
            print('2 = One-Hit Wonders: 5 x 5 board with five ships that are all size 1!')
            print('3 = Exit')
            choice = input('Please type one of the given numbers for one of the modes: ')
            if choice == '0':
                self.normalbattleship()
            elif choice == '1':
                self.minibattleship()
            elif choice == '2':
                self.size1battleship()
            elif choice == '3':
                print('Thank you for playing. Goodbye!\n')
                return
            else:
                print('Invalid input given, please try again\n')
                self.playgame()

    def run(self):
        self.playgame()

if __name__ == '__main__':
    bs = battleship()
    bs.run()