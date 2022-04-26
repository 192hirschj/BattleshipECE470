from cmessage import Cmessage
from cprotocol import Cprotocol
from cuser import Cuser
import random

class Cserverops(object):

    def __init__(self):
        self._users = {}
        self._courses = {}
        self.sproto = Cprotocol()
        self.connected = False
        self._login = False
        self._route = {'LGIN': self._doLogin, 
                       'LOUT': self._doLogout,
                       'SRCH': self._doSearch,
                       'CREA': self._docreateAccount,
                       'BALA': self._doShowBalance}
        self._debug = True
        
    def _debugPrint(self, m: str):
        if self._debug:
            print(m)
        
    def load(self, uname: str):
        with open(uname, 'r') as fp:
            for line in fp:
                line = line.strip()
                values = line.split()
                user = Cuser(values[0],values[1])
                self._users[values[0]] = user
            
    def _doLogin(self, req: Cmessage) -> Cmessage:
        resp = Cmessage()
        u = req.getParam('username')
        p = req.getParam('password')
        if u in self._users:
            if self._users[u].login(u,p):
                resp.setType('GOOD')
                resp.addParam('message', 'Login successful')
                self._login = True
            else:
                resp.setType('ERRO')
                resp.addParam('message', 'Bad login')
                self.connected = False
        else:
            resp.setType('ERRO')
            resp.addParam('message', 'Bad login')
            self.connected = False
        return resp
    
    def _doLogout(self, req: Cmessage) -> Cmessage:
        resp = Cmessage()
        resp.setType('GOOD')
        resp.addParam('message','Logout successful')
        self._login = False
        self.connected = False
        return resp

    def _docreateAccount(self, request: Cmessage) -> Cmessage:
        userName = request.getParam('userName')
        password = request.getParam('password')
        fopen = open('users.txt', 'a')
        if userName not in self._users:
            fopen.write(userName + ' ' + password + '\n')
            fopen.close()
            serverResponse = Cmessage()
            serverResponse.setType('GOOD')
            serverResponse.addParam('message', 'Account Created')
            self.load('users.txt')
            return serverResponse
        else:
            serverResponse = Cmessage()
            serverResponse.setType('ERRO')
            serverResponse.addParam('message', 'User Exists') 
            return serverResponse

    def _doSearch(self, req: Cmessage) -> Cmessage:
        resp = Cmessage()
        cid = req.getParam('cid')
        if cid in self._courses:
            c = self._courses[cid]
            resp.setType('DATA')
            resp.addParam('cid', c.cid)
            resp.addParam('name', c.name)
            resp.addParam('credits', c.credits)
        else:
            resp.setType('ERRO')
            resp.addParam('message', 'course not found')
        return resp

    def _doShowBalance(self, request: Cmessage) -> Cmessage:
        yourUserName = request.getParam('userName')
        if yourUserName in self._users:
            response = Cmessage()
            response.setType('DATA')
            response.addParam('balance', self._users[yourUserName].getBalance())
            return response
        else:
            response = Cmessage()
            response.setType('ERRO')
            response.addParam('message', 'User was not found in the server')
            return response
                        
    def _process(self, req: Cmessage) -> Cmessage:
        m = self._route[req.getType()]
        return m(req)
    
    def shutdown(self):
        self.sproto.close()
        self.connected = False
        self._login = False
        
    def run(self):
        try:
            while (self.connected):
                #get message
                req = self.sproto.getMessage()
                self._debugPrint(req)
                
                # process request
                #resp = self._process(req)
                resp = self._process(req)
                self._debugPrint(resp)
    
                # send response
                self.sproto.putMessage(resp)
        except Exception as e:
            print(e)
        self.shutdown()