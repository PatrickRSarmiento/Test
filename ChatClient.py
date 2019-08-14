"""
	Patrick Sarmiento
	CSC 376 Distributed Systems
	Assignment 3 Chat - Client
"""

import sys
import socket
import select

### chat client ###
def client():
  if len(sys.argv) < 2:
    port = 6001
  else:
    port = sys.argv[1]

 ### set client socket ###   
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
### try to connect client to server via port number  
  try:
    client_socket.connect(("", int(port)))
  except:
    sys.exit() ### fail to connect -> exit
   
  print('') ### print new line

 ### while client is active and true #### 
  while True:
    sockList = [sys.stdin, client_socket]
     
    prepare_connect,_,_ = select.select(sockList , [], [])
     
    for sock in prepare_connect:       
      if sock == client_socket:
        data = sock.recv(4096)
        if not data:
          sys.exit()
        else:
          print(data.decode())
          print('')  
      else:
        msg = sys.stdin.readline()
        if not msg:
          sys.exit()
        client_socket.send(msg.encode())
        print('')

### System Exit chat client ###
sys.exit(client()) 