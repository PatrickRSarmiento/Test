"""
	Patrick Sarmiento
	CSC 376 Distributed Systems
	Assignment 3 Chat - Client
	video link: https://youtu.be/p_7CEa3pnw0
"""

import sys
import socket
import select

### list for sockets ###
sockList = []
### dictionary for usernames ###
usernames = {}

### server function  ###
def server():
  if len(sys.argv) < 2:
    port = 6001
  else:
    port = sys.argv[1]

### sockets settings ####
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(('', int(port)))
  server_socket.listen(10)

 ### append server socket to socket list ###  
  sockList.append(server_socket)

  while True:
    prepare_connect, _,_ = select.select(sockList,[],[],0)
    
    for sock in prepare_connect:
      if sock == server_socket: 
        sockfd, addr = server_socket.accept()
        sockList.append(sockfd) 
        usernames[sockfd.getpeername()] = "EMPTY"
      else:
        try:
          data = sock.recv(4096)
          if data:
            if usernames[sock.getpeername()] == "EMPTY":
              usernames[sock.getpeername()] = data.decode().rstrip()
            else:
              send_msg(server_socket, sock, "\r" + usernames[sock.getpeername()] + ': ' + data.decode())  
          else:
            if sock in sockList:
              sockList.remove(sock)

        except Exception as e:
          continue

  server_socket.close()

  ### send function ### 
def send_msg(server_socket, sock, message):
  for socket in sockList:
    if socket != server_socket and socket != sock :
      try :
        socket.send(message.encode())
      except Exception as e:
        socket.close()
        if socket in sockList:
          sockList.remove(socket)
 
sys.exit(server())    