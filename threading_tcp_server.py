import socket
import threading
from cserverops import Cserverops
from cprotocol import Cprotocol

def thr_run(sops: Cserverops):
    print("Started thread ", threading.current_thread())
    sops.run()
    print("Ended thread ", threading.current_thread())

if __name__ == '__main__':
    # create the server socket
    #  defaults family=AF_INET, type=SOCK_STREAM, proto=0, filno=None
    serversoc = socket.socket()
    
    # bind to local host:50000
    port = 56437
    serversoc.bind(("localhost", port))
                   
    # make passive with backlog=5
    serversoc.listen(5)
    thnum = 1
    
    # wait for incoming connections
    while True:
        print("Listening on ", port)
        
        # accept the connection
        commsoc, raddr = serversoc.accept()
        
        # run the serverops
        sops = Cserverops()
        sops.load("users.txt")
        sops.sproto = Cprotocol(commsoc)
        sops.connected = True
        tid = threading.Thread(name="thr_{}".format(thnum), target=thr_run, args=(sops,))
        thnum = thnum + 1
        tid.setDaemon(True)
        tid.start()
        #sops.run()
        
    
    # close the server socket
    serversoc.close()