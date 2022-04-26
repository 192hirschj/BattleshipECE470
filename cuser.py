class Cuser(object):

    def __init__(self, u: str, p: str, bal: float):
        self._username = u
        self._password = p
        self._balance = bal

    def getBalance(self):
        return self._balance

    def updateBalance(self, balance):
        self._balance = balance
        
    def __str__(self):
        return '{} {} {}\n'.format(self._username, self._password, self._balance)
        
    def login(self, u: str, p: str) -> bool:
        if ((self._username == u) and (self._password == p)):
            return True
        else:
            return False
