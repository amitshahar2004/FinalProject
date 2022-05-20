import pygame
from tkinter import *
import chat
import time
import os
import subprocess
import sys
import socket
import pickle
import threading
import connect_user


class Zira:

    def __init__(self, screen):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BOX_POINT_X = 200
        self.BOX_POINT_Y = 500
        self.CLICK_FOR_SENDING_MESSAGE_POINT_X = 690
        self.CLICK_FOR_SENDING_MESSAGE_POINT_Y = 690
        self.CLICK_FOR_SHOWING_CONTROL_BOARD_POINT_X = 300
        self.CLICK_FOR_SHOWING_CONTROL_BOARD_POINT_Y = 100
        self.screen = screen
        self.clicked_for_showing_control_board = False
        self.info_control_board = []

    def get_BOX_POINT_X(self):

        return self.BOX_POINT_X

    def get_BOX_POINT_Y(self):

        return self.BOX_POINT_Y

    def get_clicked_for_showing_control_board(self):

        return self.clicked_for_showing_control_board

    def set_clicked_for_showing_control_board(self, boolean):

        self.clicked_for_showing_control_board = boolean

    def set_player(self, data_clients):

        print(data_clients)

        for player in data_clients:
            player_image = pygame.image.load("pictures_for_game/panda_walking1.png")
            player_image.set_colorkey(self.BLACK)
            self.screen.blit(player_image, (player[0], player[1]))

            font_name = pygame.font.SysFont('arial', 20)
            text_name = font_name.render(player[2], True, self.BLACK)
            self.screen.blit(text_name, (player[0] + 100, player[1] + 150))

            pygame.display.flip()

            if player[3] != '':
                self.draw_rectangle_with_message(player[3], (player[0] + 100, player[1] + 15), 18)

    def draw_rectangle_with_message(self, text, pos, size):
        font = pygame.font.SysFont('arial', size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(midbottom=pos)

        # Background
        background_rect = text_rect.copy()
        background_rect.inflate_ip(30, 5)

        # Frame
        frame_rect = background_rect.copy()
        frame_rect.inflate_ip(4, 4)

        pygame.draw.rect(self.screen, self.BLACK, frame_rect)
        pygame.draw.rect(self.screen, self.WHITE, background_rect)
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def set_zira(self, data_clients):

        img = pygame.image.load("pictures_for_game/forest1.png")
        self.screen.blit(img, (0, 0))
        pygame.display.flip()

        self.draw_rectangle_with_message("CLICK FOR SENDING MESSAGE", (self.CLICK_FOR_SENDING_MESSAGE_POINT_X, self.CLICK_FOR_SENDING_MESSAGE_POINT_Y), 25)
        pygame.display.flip()

        box_image = pygame.image.load("pictures_for_game/box1.png")
        self.screen.blit(box_image, (self.BOX_POINT_X, self.BOX_POINT_Y))
        pygame.display.flip()

        if self.clicked_for_showing_control_board == False:
            self.draw_rectangle_with_message("CLICK FOR SHOWING CONTROL BOARD", (self.CLICK_FOR_SHOWING_CONTROL_BOARD_POINT_X, self.CLICK_FOR_SHOWING_CONTROL_BOARD_POINT_Y), 22)
            pygame.display.flip()
        else:
            self.display_control_board()

        self.set_player(data_clients)


    def set_info_control_board(self, info_control_board):
        self.info_control_board = info_control_board


    def display_control_board(self):

        img = pygame.image.load("pictures_for_game/tablet_control_board.png")
        self.screen.blit(img, (108, 69))
        pygame.display.flip()

        font_name = pygame.font.SysFont('arial', 16)

        text_the_winner_player = font_name.render("The player who has won the most times: " + str(self.info_control_board[1]), True, self.BLACK)
        self.screen.blit(text_the_winner_player, (168, 119))

        text_num_of_times_the_winner_won = font_name.render("The number of times he won: " + str(self.info_control_board[2]), True, self.BLACK)
        self.screen.blit(text_num_of_times_the_winner_won, (168, 169))

        text_num_of_players_are_playing_eix_eigul = font_name.render("The number of players are playing Eix Eigul: " + str(self.info_control_board[3]), True, self.BLACK)
        self.screen.blit(text_num_of_players_are_playing_eix_eigul, (168, 219))

        pygame.display.flip()


class Player:

    def __init__(self, starting_bear_point_x, starting_bear_point_y, name_player):

        self.starting_bear_point_x = starting_bear_point_x
        self.starting_bear_point_y = starting_bear_point_y
        self.name_player = name_player
        self.clicked_on_box = False
        self.treat_messages = ''

    def get_starting_bear_point_x(self):

        return self.starting_bear_point_x

    def get_starting_bear_point_y(self):

        return self.starting_bear_point_y

    def get_name_player(self):

        return self.name_player

    def set_clicked_on_box(self):

        self.clicked_on_box = True

    def set_treat_messages(self, treat_messages):

        self.treat_messages = treat_messages

    def move_player(self, pos_x, pos_y):

        jump_in_x = (self.starting_bear_point_x - pos_x) / 20
        jump_in_y = (self.starting_bear_point_y - pos_y) / 20

        print("jump_in_x= " + str(jump_in_x) + " jump_in_y= " + str(jump_in_y))

        first_place_x = self.starting_bear_point_x
        first_place_y = self.starting_bear_point_y

        for i in range(20):
            first_place_x = first_place_x - jump_in_x
            first_place_y = first_place_y - jump_in_y
            print("x= " + str(first_place_x) + " y= " + str(first_place_y))
            self.treat_messages.send_message(first_place_x, first_place_y, self.name_player, '')
            time.sleep(0.1)

        self.starting_bear_point_x = pos_x
        self.starting_bear_point_y = pos_y

        if self.clicked_on_box == True:
            self.clicked_on_box = False
            self.play_eix_eigul()

    def play_eix_eigul(self):

        try:
            my_socket = self.treat_messages.get_my_socket()
            message = pickle.dumps(["StatusEixEigulGame", self.name_player])
            my_socket.send(message)

            which_player_file = ''
            data_client = []

            while which_player_file != "you are waiting or playing" and which_player_file != "player_x.py" and which_player_file != "player_o.py":
                data_client = self.treat_messages.get_data_clients()
                which_player_file = data_client[0]

            if which_player_file == "you are waiting or playing":
                return

            port_eix_eigul = data_client[1]
            if which_player_file == "player_x.py":
                pid_server = subprocess.Popen([sys.executable, "server_eix_eigul.py", str(port_eix_eigul)])

            x = threading.Thread(target=self.thread_eix_eigul, args=(which_player_file, my_socket, port_eix_eigul))
            x.start()

        except:
            print("the client close the game!")


    def thread_eix_eigul(self, which_player_file, my_socket, port_eix_eigul):

        try:
            pid_client = subprocess.Popen([sys.executable, which_player_file, str(port_eix_eigul)], stdout=subprocess.PIPE)

            data_in_eix_eigul = ''
            is_player_x_winner = False
            is_player_o_winner = False

            while True:
                if pid_client.poll() is not None:
                    break
                data_in_eix_eigul = pid_client.stdout.readline().decode()
                print(data_in_eix_eigul)
                if 'Player x is the winner!' in data_in_eix_eigul:
                    is_player_x_winner = True
                if 'Player o is the winner!' in data_in_eix_eigul:
                    is_player_o_winner = True

            pid_client.communicate()

            if is_player_x_winner == True and which_player_file == "player_x.py":
                message = pickle.dumps(["WinnerEixEigul", self.name_player])
                my_socket.send(message)

            if is_player_o_winner == True and which_player_file == "player_o.py":
                message = pickle.dumps(["WinnerEixEigul", self.name_player])
                my_socket.send(message)

            message = pickle.dumps(["FinishEixEigulGame", self.name_player])
            my_socket.send(message)

        except:
            print("the client close the game!")




class TreatMessages:

    def __init__(self, my_socket, data_clients, zira):

        self.my_socket = my_socket
        self.data_clients = data_clients
        self.zira = zira
        self.last_message = ''
        self.num_of_threads = 0

    def get_my_socket(self):
        return self.my_socket

    def get_data_clients(self):
        return self.data_clients

    def get_last_message(self):
        return self.last_message

    def draw_new_board(self):

        while True:
            try:
                self.data_clients = self.my_socket.recv(1024)
                self.data_clients = pickle.loads(self.data_clients)
                print(self.data_clients)
                if self.data_clients[0] == "you are waiting or playing" or self.data_clients[0] == "player_x.py" or self.data_clients[0] == "player_o.py":
                    time.sleep(0.2)
                else:
                    if self.data_clients[0] == "control board":
                        self.zira.set_info_control_board(self.data_clients)
                        self.zira.set_clicked_for_showing_control_board(True)
                        self.zira.display_control_board()
                    else:
                        self.zira.set_zira(self.data_clients)

            except:
                print("the client close the game!")
                return

    def send_message(self, first_place_x, first_place_y, name_player, last_message):

        try:
            if last_message != '':
                self.last_message = last_message
                x = threading.Thread(target=self.delete_message, args=(name_player,))
                x.start()
            message = pickle.dumps(["PlayerValues", first_place_x, first_place_y, name_player, self.last_message])
            self.my_socket.send(message)

        except:
            print("the client close the game!")

    def delete_message(self, name_player):

        self.num_of_threads = self.num_of_threads + 1
        time.sleep(4)
        if self.num_of_threads == 1:
            self.last_message = ''

        self.num_of_threads = self.num_of_threads - 1



def main():
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code

    my_socket = socket.socket()
    #ip = "127.0.0.1"
    #port = 8822
    #my_socket.connect((ip, port))

    # try:
    #     ip = input("Please enter the server ip: ")
    #     port = 8822
    #     my_socket.connect((ip, port))
    # except:
    #     print("you type the wrong ip")
    #     return

    user = connect_user.TreatUser(my_socket)

    name_player = user.get_username()

    pygame.init()

    WINDOW_WIDTH = int(my_socket.recv(4).decode())
    WINDOW_HEIGHT = int(my_socket.recv(3).decode())
    place = my_socket.recv(1024).decode()

    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.display.set_caption("Game")
    place = place.split(" ")
    starting_bear_point_x = int(place[0])
    starting_bear_point_y = int(place[1])

    player = Player(starting_bear_point_x, starting_bear_point_y, name_player)

    data_clients = []

    data_clients.append([player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), ''])

    zira = Zira(screen)

    zira.set_zira(data_clients)

    treat_messages = TreatMessages(my_socket, data_clients, zira)

    player.set_treat_messages(treat_messages)

    send_data_clients = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(),player.get_name_player(), ''])
    my_socket.send(send_data_clients)

    x = threading.Thread(target=treat_messages.draw_new_board)
    x.start()

    finish1 = False
    while not finish1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish1 = True
                message = pickle.dumps(["Exit", player.get_name_player()])
                my_socket.send(message)
                time.sleep(0.2)
                my_socket.close()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos_x = pos[0]
                pos_y = pos[1]
                print("pos_x= " + str(pos_x) + " pos_y= " + str(pos_y))
                # אם המשתמש לחץ על המלבן הלבן האומר שהוא רוצה לשלוח הודעה
                if (pos_x >= 571 and pos_x <= 808) and (pos_y >= 655 and pos_y <= 694):
                    root = Tk()
                    gui = chat.GUI(root, player.get_starting_bear_point_x(), player.get_starting_bear_point_y(),player.get_name_player(), treat_messages)
                    root.mainloop()

                else:
                    # אם המשתמש לחץ על התיבה זה אומר שהוא רוצה לשחק עם מישהו ולכן כל מי שלוחץ על התיבה צריך להיות באותו מקום ממנה
                    if (pos_x >= zira.get_BOX_POINT_X() and pos_x <= 306) and (pos_y >= zira.get_BOX_POINT_Y() and pos_y <= 566):
                        player.set_clicked_on_box()

                        player.move_player(pos_x - 100, pos_y - 100)

                    else:
                        #אם המשתמש לחץ על המלבן הלבן האומר שהוא רוצה לראות את לוח הבקרה של המשחק
                        if(pos_x >= 108 and pos_x <= 491) and (pos_y >= 69 and pos_y <= 102):

                            if zira.get_clicked_for_showing_control_board() == False:

                                message = pickle.dumps(["controlBoard"])
                                my_socket.send(message)

                            else:

                                player.move_player(pos_x - 100, pos_y - 100)

                        else:

                            # אם המשתמש לחץ על האיקס של הלוח בקרה האומר שהוא רוצה לסגור את הלוח
                            if (pos_x >= 115 and pos_x <= 162) and (pos_y >= 157 and pos_y <= 185):

                                if zira.get_clicked_for_showing_control_board() == True:

                                    zira.set_clicked_for_showing_control_board(False)
                                    message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message()])
                                    my_socket.send(message)

                                else:

                                    player.move_player(pos_x - 100, pos_y - 100)
                            else:

                                player.move_player(pos_x - 100, pos_y - 100)




if __name__ == '__main__':
    main()
