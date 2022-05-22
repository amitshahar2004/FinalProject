import socket
import select

import sys
import pygame
import time


class EixEigul:
  def __init__(self):
    self.turn = 0
    self.board= [['','',''],['','',''],['','','']]

  def main_call_func(self,row,column):

      (finish,message)= self.draw_player(row,column)
      return finish,message

  def draw_player(self,row,column):
      if self.board[row][column] == '':
          if self.turn == 0:
              self.board[row][column]= 'x'
              self.turn= 1
              shape_player= 'x'
          else:
              self.board[row][column]= 'o'
              self.turn= 0
              shape_player= 'o'

          winner= self.check_winner(shape_player)
          if winner == 'Player x is the winner!' or winner == 'Player o is the winner!' or winner == 'There is no winner!':
              return True,winner
          else:
              return False,"It worked!"
      else:
          return False,"It has caught, try another place!"



  def check_winner(self,shape_player):

        for row in range(len(self.board)):
            if self.board[row][0] == shape_player and self.board[row][1] == shape_player and self.board[row][2] == shape_player:
                return 'Player '+shape_player+' is the winner!'
        for column in range(len(self.board[0])):
            if self.board[0][column] == shape_player and self.board[1][column] == shape_player and self.board[2][column] == shape_player:
                return 'Player '+shape_player+' is the winner!'
        if self.board[0][0] == shape_player and self.board[1][1] == shape_player and self.board[2][2] == shape_player:
            return 'Player '+shape_player+' is the winner!'
        if self.board[0][2] == shape_player and self.board[1][1] == shape_player and self.board[2][0] == shape_player:
            return 'Player '+shape_player+' is the winner!'

        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if self.board[row][column] == '':
                    return 'no winner yet'

        return 'There is no winner!'


def socket_has_been_closed(current_socket, rlist, open_client_sockets):

    for current_socket in rlist:
        try:
            bytes_client = current_socket.recv(1024)
            print("select.select current_socket=" + current_socket)
        except:
            open_client_sockets.remove(current_socket)


def main():

    print("Arguments argv[0]: " + sys.argv[0])
    print("Arguments argv[1]: " + sys.argv[1])
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code

    print("server begin")
    server_socket = socket.socket()

    port = int(sys.argv[1])
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)

    open_client_sockets=[]

    board_game = EixEigul()


    finish= False
    message = ''
    row = 0
    column = 0
    mate_socket = 0
    cur_socket = 1
    game_over= True
    try:
        while game_over:
            rlist, wlist, xlist = select.select([server_socket]+open_client_sockets, [], [])
            for current_socket in rlist:
                if current_socket is server_socket:
                    (new_socket,address) = server_socket.accept()
                    print('socket created '+ str(address))
                    open_client_sockets.append(new_socket)

                else:

                    if open_client_sockets[0] == current_socket:
                        cur_socket = 0
                        mate_socket = 1
                    else:
                        cur_socket = 1
                        mate_socket = 0

                    place = open_client_sockets[cur_socket].recv(4).decode()

                    if len(open_client_sockets) == 1:

                        if place == 'Exit':
                            open_client_sockets[cur_socket].close()
                            server_socket.close()
                            game_over = False

                    if len(open_client_sockets) == 2:

                        if place == 'Exit':
                            open_client_sockets[mate_socket].send("Exit".encode())
                            open_client_sockets[mate_socket].send("Exit".encode())
                            time.sleep(0.2)
                            open_client_sockets[cur_socket].close()
                            open_client_sockets[mate_socket].close()
                            server_socket.close()
                            game_over = False
                        else:
                            row = int(place[0])
                            column = int(place[1])
                            print('Receive Msg from: '+str(cur_socket) +' row: ' + str(row)+' column: '+str(column))

                            (finish, message) = board_game.main_call_func(row, column)
                            open_client_sockets[cur_socket].send(message.encode())
                            print('sending Msg: ' + message + 'to' + str(cur_socket))

                            if message == 'It worked!':
                                open_client_sockets[mate_socket].send((str(row)+str(column)).encode())
                                open_client_sockets[mate_socket].send('the info was send!'.encode())
                                print('sending other player to ' + str(mate_socket) +' row: ' + str(row) + ' column: ' + str(column))

                            if message == 'Player x is the winner!' or message == 'Player o is the winner!' or message == 'There is no winner!':
                                open_client_sockets[mate_socket].send((str(row) + str(column)).encode())
                                open_client_sockets[mate_socket].send(message.encode())
                                print('sending other player to ' + str(mate_socket) + ' row: ' + str(row) + ' column: ' + str(column))
                                time.sleep(1)
                                open_client_sockets[cur_socket].close()
                                open_client_sockets[mate_socket].close()
                                server_socket.close()
                                game_over= False
    except:
        socket_has_been_closed(current_socket, rlist, open_client_sockets)
if __name__ == '__main__':
    main()
