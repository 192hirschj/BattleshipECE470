import socket
from cprotocol import Cprotocol
from cmessage import Cmessage

class Cclientops(object):

    def __init__(self):
        self._cproto = Cprotocol()
        self._login = False
        self._done = False
        self._debug = True
        self._curruser = ''
        self._menucheck = False
        
    def _debugPrint(self, m: str):
        if self._debug:
            print(m)
            
    def _connect(self):
        commsoc = socket.socket()
        commsoc.connect(("localhost", 56437))
        self._cproto = Cprotocol(commsoc)
            
    def _doLogin(self):
        username = input('username: ')
        password = input('password: ')
        self._connect()
        req = Cmessage()
        req.setType('LGIN')
        req.addParam('username', username)
        req.addParam('password', password)
        self._cproto.putMessage(req)
        resp = self._cproto.getMessage()
        if resp:
            print(resp.getParam('message'))
            print()
            if resp.getType() == 'GOOD':
                self._login = True
                self._curruser = username
            else:
                self._cproto.close()
        
    def _doLogout(self):
        req = Cmessage()
        req.setType('LOUT')
        self._cproto.putMessage(req)
        resp = self._cproto.getMessage()
        if resp:
            print(resp.getParam('message'))
        self._curruser = ' '
        self._login = False

    def _docreateAccount(self):
        print('Create Account')
        username = input('Type your username: ')
        password = input('Type your password: ')
        request = Cmessage()
        self._connect()
        request.setType('CREA')
        request.addParam('userName', username)
        request.addParam('password', password)
        self._cproto.putMessage(request)
        response = self._cproto.getMessage()
        if response.getType() == 'GOOD':
            loginRequest = Cmessage()
            loginRequest.setType('LGIN')
            loginRequest.addParam('username', username)
            loginRequest.addParam('password', password)
            self._cproto.putMessage(loginRequest)
            response = self._cproto.getMessage()
            if response:
                print(response.getParam('message'))
                if response.getType() == 'GOOD':
                    self._login = True
                    self._curruser = username
                else:
                    self._cproto.close()

    def _doSearch(self):
        recipient = input('Search for a user to find: ')
        if recipient == self._curruser:
            print('You must search for a different user.')
            return ' '
        req = Cmessage()
        req.setType('SRCH')
        req.addParam('user', recipient)
        self._cproto.putMessage(req)
        resp = self._cproto.getMessage()
        print(resp.getParam('message'))
        print()
        if resp.getType() == 'GOOD':
            return recipient
        else:
            return ' '

    def _doShowBalance(self):
        request = Cmessage()
        request.setType('BALA')
        request.addParam('userName', self._curruser)
        self._cproto.putMessage(request)
        response = self._cproto.getMessage()
        if response:
            if response.getType() == 'DATA':
                print('Your current balance is {}\n'.format(response.getParam('balance')))
            else:
                print(response.getParam('message'))
    
    def _shutdown(self):
        if self._login:
            self._doLogout()
            self._cproto.close()
        self._login = False
        self._done = True

    def _doMainMenuhelp(self):
        print('\nCreate Game -- Create a game lobby and receive a game code')
        print('Join Game -- Join a game lobby by typing in a game code')
        print('Search for Player -- Search by username for another player')
        print('View Personal Stats -- Displays current stats for games played')
        print('View Leaderboard -- Views top five players by wins')
        print('Back -- Will bring you back to the previous menu, here it will log you out')
        print('Exit -- Completly exits the application\n')

    def _doLoginMenu(self):
        menu = ['1. Login', '2. Create Account', '3. Exit']
        choices = {'1': self._doLogin,'2':self._docreateAccount, '3': self._shutdown}
        print('\n'.join(menu))
        choice = input('> ')
        if choice in choices:
            m = choices[choice]
            m()

    def _doMainMenu(self):
        menu = ['1. Create Game', '2. Join Game', '3. Search for Player', '4. View Balance', '5. View Personal Stats', '6. View Leaderboard', 
                '97. Help', '98. Logout', '99. Exit']
        choices = {'3': self._doSearch, '4': self._doShowBalance, '97': self._doMainMenuhelp, '98': self._doLogout, '99': self._shutdown}
        print('\n'.join(menu))
        choice = input('> ')
        if choice in choices:
            m = choices[choice]
            m()
    
    def run(self):
        while (self._done == False):
            if (self._login == False):
                self._doLoginMenu()
            else:
                self._doMainMenu()
        self._shutdown()
        