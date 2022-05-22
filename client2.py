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




def user_want_send_everyone_message(pos_x, pos_y, player, treat_messages):
        # אם המשתמש לחץ על המלבן הלבן האומר שהוא רוצה לשלוח הודעה
        if (pos_x >= 571 and pos_x <= 808) and (pos_y >= 655 and pos_y <= 694):
            root = Tk()
            gui = chat.GUI(root, player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages)
            root.mainloop()

            return True

        return False

def user_clicked_on_box_to_play(pos_x, pos_y, zira, player):
        # אם המשתמש לחץ על התיבה זה אומר שהוא רוצה לשחק עם מישהו ולכן כל מי שלוחץ על התיבה צריך להיות באותו מקום ממנה
        if (pos_x >= zira.get_BOX_POINT_X() and pos_x <= 306) and (pos_y >= zira.get_BOX_POINT_Y() and pos_y <= 566):

            player.set_clicked_on_box()

            player.move_player(pos_x - 100, pos_y - 100)

            return True

        return False

def user_want_to_see_control_board(pos_x, pos_y, player, zira, my_socket):
        # אם המשתמש לחץ על המלבן הלבן האומר שהוא רוצה לראות את לוח הבקרה של המשחק
        if (pos_x >= 108 and pos_x <= 491) and (pos_y >= 69 and pos_y <= 102):

            if zira.get_clicked_for_showing_control_board() == False:

                message = pickle.dumps(["controlBoard", zira.get_background_picture()])
                my_socket.send(message)

            else:

                player.move_player(pos_x - 100, pos_y - 100)

            return True

        return False

def user_want_close_control_board(pos_x, pos_y, player, zira, my_socket, treat_messages):
        # אם המשתמש לחץ על האיקס של הלוח בקרה האומר שהוא רוצה לסגור את הלוח
        if (pos_x >= 115 and pos_x <= 162) and (pos_y >= 157 and pos_y <= 185):

            if zira.get_clicked_for_showing_control_board() == True:

                zira.set_clicked_for_showing_control_board(False)
                message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
                my_socket.send(message)

            else:

                player.move_player(pos_x - 100, pos_y - 100)

            return True

        return False

def user_want_to_go_to_pool_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):

    # אם המשתמש לחץ על הגבול של התמונה של היער זה אומר שהוא רוצה לעבור למקום הבריכה
    if pos_x >= 1 and pos_x <= WINDOW_WIDTH-1 and pos_y == 0 and zira.get_background_picture() == 'forest':

            player.move_player(pos_x - 100, pos_y - 100)
            zira.set_clicked_for_showing_control_board(False)
            zira.set_background_picture("pool")
            player.set_starting_bear_point_x(100)
            player.set_starting_bear_point_y(WINDOW_HEIGHT - 200)
            message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
            my_socket.send(message)

            return True

    return False


def user_want_to_go_to_forest_from_pool_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):

    # אם המשתמש לחץ על הגבול של התמונה של הבריכה זה אומר שהוא רוצה לעבור למקום היער
    if pos_x >= 1 and pos_x <= WINDOW_WIDTH-1 and pos_y >= WINDOW_HEIGHT-1 and zira.get_background_picture() == 'pool':

        player.move_player(pos_x - 100, pos_y - 100)
        zira.set_clicked_for_showing_control_board(False)
        zira.set_background_picture("forest")
        player.set_starting_bear_point_x(500)
        player.set_starting_bear_point_y(0)
        message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
        my_socket.send(message)

        return True

    return False


def user_want_to_go_to_slides_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):
    # אם המשתמש לחץ על הגבול של התמונה של היער זה אומר שהוא רוצה לעבור למקום המגלשות
    if pos_x == 0 and pos_y >= 1 and pos_y <= WINDOW_HEIGHT-1 and zira.get_background_picture() == 'forest':

        player.move_player(pos_x - 100, pos_y - 100)
        zira.set_clicked_for_showing_control_board(False)
        zira.set_background_picture("slides")
        player.set_starting_bear_point_x(WINDOW_WIDTH - 200)
        player.set_starting_bear_point_y(100)
        message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
        my_socket.send(message)

        return True

    return False

def user_want_to_go_to_forest_from_slides_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):
    # אם המשתמש לחץ על הגבול של התמונה של המגלשות זה אומר שהוא רוצה לעבור למקום היער
    if pos_x >= WINDOW_WIDTH-1 and pos_y >= 1 and pos_y <= WINDOW_HEIGHT-1 and zira.get_background_picture() == 'slides':

        player.move_player(pos_x - 100, pos_y - 100)
        zira.set_clicked_for_showing_control_board(False)
        zira.set_background_picture("forest")
        player.set_starting_bear_point_x(50)
        player.set_starting_bear_point_y(200)
        message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
        my_socket.send(message)

        return True

    return False


def user_want_to_go_to_vacation_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):
    # אם המשתמש לחץ על הגבול של התמונה של היער זה אומר שהוא רוצה לעבור למקום החופשה
    if pos_x >= WINDOW_WIDTH-1 and pos_y >= 1 and pos_y <= WINDOW_HEIGHT-1 and zira.get_background_picture() == 'forest':

        player.move_player(pos_x - 100, pos_y - 100)
        zira.set_clicked_for_showing_control_board(False)
        zira.set_background_picture("vacation")
        player.set_starting_bear_point_x(0)
        player.set_starting_bear_point_y(100)
        message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
        my_socket.send(message)

        return True

    return False

def user_want_to_go_to_forest_from_vacation_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):
    # אם המשתמש לחץ על הגבול של התמונה של החופשה זה אומר שהוא רוצה לעבור למקום היער
    if pos_x == 0 and pos_y >= 1 and pos_y <= WINDOW_HEIGHT-1 and zira.get_background_picture() == 'vacation':

        player.move_player(pos_x - 100, pos_y - 100)
        zira.set_clicked_for_showing_control_board(False)
        zira.set_background_picture("forest")
        player.set_starting_bear_point_x(WINDOW_WIDTH - 200)
        player.set_starting_bear_point_y(100)
        message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
        my_socket.send(message)

        return True

    return False

def user_want_to_go_to_beach_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):
    #  אם המשתמש לחץ על הגבול של התמונה של היער זה אומר שהוא רוצה לעבור למקום החוף ים
    if pos_x >= 1 and pos_x <= WINDOW_WIDTH-1 and pos_y >= WINDOW_HEIGHT-1 and zira.get_background_picture() == 'forest':

        player.move_player(pos_x - 100, pos_y - 100)
        zira.set_clicked_for_showing_control_board(False)
        zira.set_background_picture("beach")
        player.set_starting_bear_point_x(500)
        player.set_starting_bear_point_y(0)
        message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
        my_socket.send(message)

        return True

    return False

def user_want_to_go_to_forest_from_beach_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket):
    # אם המשתמש לחץ על הגבול של התמונה של החוף ים זה אומר שהוא רוצה לעבור למקום היער
    if pos_x >= 1 and pos_x <= WINDOW_WIDTH-1 and pos_y == 0 and zira.get_background_picture() == 'beach':

        player.move_player(pos_x - 100, pos_y - 100)
        zira.set_clicked_for_showing_control_board(False)
        zira.set_background_picture("forest")
        player.set_starting_bear_point_x(100)
        player.set_starting_bear_point_y(WINDOW_HEIGHT - 200)
        message = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), treat_messages.get_last_message(), zira.get_background_picture()])
        my_socket.send(message)

        return True

    return False


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
        self.background_picture = "forest"

    def get_BOX_POINT_X(self):

        return self.BOX_POINT_X

    def get_BOX_POINT_Y(self):

        return self.BOX_POINT_Y

    def get_background_picture(self):

        return self.background_picture

    def get_clicked_for_showing_control_board(self):

        return self.clicked_for_showing_control_board

    def set_clicked_for_showing_control_board(self, boolean):

        self.clicked_for_showing_control_board = boolean

    def set_background_picture(self, pic):

        self.background_picture = pic

    def set_player(self, data_clients):

        print(data_clients)

        for player in data_clients:

            if player[4] == self.background_picture:

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

        if self.background_picture == 'forest':
            img = pygame.image.load("pictures_for_game/forest1.png")
            self.screen.blit(img, (0, 0))

        elif self.background_picture == 'pool':
            img = pygame.image.load("pictures_for_game/pool.png")
            self.screen.blit(img, (0, 0))

        elif self.background_picture == 'vacation':
            img = pygame.image.load("pictures_for_game/vacation.png")
            self.screen.blit(img, (0, 0))

        elif self.background_picture == 'slides':
            img = pygame.image.load("pictures_for_game/slides.png")
            self.screen.blit(img, (0, 0))

        elif self.background_picture == 'beach':
            img = pygame.image.load("pictures_for_game/beach.png")
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

        if self.info_control_board[1] == "eix eigul" or self.info_control_board[1] == "brike breaker":

            text_the_winner_player = font_name.render("The player who has won the most times: " + str(self.info_control_board[2]), True, self.BLACK)
            self.screen.blit(text_the_winner_player, (168, 119))

            text_num_of_times_the_winner_won = font_name.render("The number of times he won: " + str(self.info_control_board[3]), True, self.BLACK)
            self.screen.blit(text_num_of_times_the_winner_won, (168, 169))

            text_num_of_players_are_playing_in_this_game = font_name.render("The number of players are playing in game " + str(self.info_control_board[1])+": " + str(self.info_control_board[4]), True, self.BLACK)
            self.screen.blit(text_num_of_players_are_playing_in_this_game, (168, 219))

            pygame.display.flip()

        else:
            text_the_winner_player = font_name.render("The player who has the highest score: " + str(self.info_control_board[2]), True, self.BLACK)
            self.screen.blit(text_the_winner_player, (168, 119))

            text_num_of_times_the_winner_won = font_name.render("His score: " + str(self.info_control_board[3]), True, self.BLACK)
            self.screen.blit(text_num_of_times_the_winner_won, (168, 169))

            text_num_of_players_are_playing_in_this_game = font_name.render("The number of players are playing in game " + str(self.info_control_board[1]) + ": " + str(self.info_control_board[4]), True, self.BLACK)
            self.screen.blit(text_num_of_players_are_playing_in_this_game, (168, 219))

            pygame.display.flip()


class Player:

    def __init__(self, starting_bear_point_x, starting_bear_point_y, name_player):

        self.starting_bear_point_x = starting_bear_point_x
        self.starting_bear_point_y = starting_bear_point_y
        self.name_player = name_player
        self.clicked_on_box = False
        self.treat_messages = ''

    def set_starting_bear_point_x(self, starting_bear_point_x):

        self.starting_bear_point_x = starting_bear_point_x

    def set_starting_bear_point_y(self, starting_bear_point_y):

        self.starting_bear_point_y = starting_bear_point_y

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
            if self.treat_messages.get_zira().get_background_picture() == 'forest':
                self.play_game("eix eigul")
            elif self.treat_messages.get_zira().get_background_picture() == 'pool':
                self.play_game("brike breaker")
            elif self.treat_messages.get_zira().get_background_picture() == 'slides':
                self.play_game("snake")
            else:
                self.play_game("color")


    def play_game(self, game):

        try:
            my_socket = self.treat_messages.get_my_socket()

            if game == "eix eigul":
                message = pickle.dumps(["StatusEixEigulGame", self.name_player])
            elif game == "brike breaker":
                message = pickle.dumps(["StatusBrikeBreakerGame", self.name_player])
            elif game == "snake":
                message = pickle.dumps(["StatusSnakeGame", self.name_player])
            else:
                message = pickle.dumps(["StatusColorGame", self.name_player])

            my_socket.send(message)

            which_player_file = ''
            data_client = []

            while which_player_file != "you are waiting or playing" and which_player_file != "player_x.py" and which_player_file != "player_o.py" and which_player_file != "brike_breaker_game.py" and which_player_file != "color_game.py" and which_player_file != "snake_game.py":
                data_client = self.treat_messages.get_data_clients()
                which_player_file = data_client[0]

            if which_player_file == "you are waiting or playing":
                return

            if game == "eix eigul":
                port_to_game = data_client[1]
                if which_player_file == "player_x.py":
                    pid_server = subprocess.Popen([sys.executable, "server_eix_eigul.py", str(port_to_game)])

                x = threading.Thread(target=self.thread_eix_eigul, args=(which_player_file, my_socket, port_to_game))
                x.start()

            else:
                x = threading.Thread(target=self.thread_game_that_not_eix_eigul, args=(which_player_file, my_socket, game))
                x.start()

        except:
            print("the client close the game!")


    def thread_game_that_not_eix_eigul(self, which_player_file, my_socket, game):

        try:
            pid_game_that_not_eix_eigul = subprocess.Popen([sys.executable, which_player_file], stdout=subprocess.PIPE)

            data_in_game = ''
            won_in_brike_breaker_game = False
            score = 0

            while True:
                if pid_game_that_not_eix_eigul.poll() is not None:
                    break
                data_in_game = pid_game_that_not_eix_eigul.stdout.readline().decode()
                print(data_in_game)
                if 'Sorry Game Over Try Again!' in data_in_game:
                    won_in_brike_breaker_game = True
                if 'score' in data_in_game:
                    data_in_game = data_in_game.split(" ")
                    data_in_game = data_in_game[1]
                    data_in_game = data_in_game.split("\r")
                    score = data_in_game[0]
                    score = int(score)

            #pid_client.communicate()


            if won_in_brike_breaker_game == True:
                message = pickle.dumps(["WinnerBrikeBreaker", self.name_player])
                my_socket.send(message)

            if score != 0:
                if game == "color":
                    message = pickle.dumps(["WinnerColorGame", score, self.name_player])
                else:
                    message = pickle.dumps(["WinnerSnakeGame", score, self.name_player])

                my_socket.send(message)


            message = pickle.dumps(["FinishGame", game, self.name_player])
            my_socket.send(message)

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

            message = pickle.dumps(["FinishGame", "eix eigul", self.name_player])
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

    def get_zira(self):
        return self.zira

    def draw_new_board(self):

        while True:
            try:
                self.data_clients = self.my_socket.recv(1024)
                self.data_clients = pickle.loads(self.data_clients)
                print(self.data_clients)
                if self.data_clients[0] == "you are waiting or playing" or self.data_clients[0] == "player_x.py" or self.data_clients[0] == "player_o.py" or self.data_clients[0] == "brike_breaker_game.py" or self.data_clients[0] == "color_game.py" or self.data_clients[0] == "snake_game.py":
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
            message = pickle.dumps(["PlayerValues", first_place_x, first_place_y, name_player, self.last_message, self.zira.get_background_picture()])
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

    user = connect_user.TreatUser(my_socket)

    name_player = user.get_username()

    pygame.init()

    try:
        WINDOW_WIDTH = int(my_socket.recv(4).decode())
        WINDOW_HEIGHT = int(my_socket.recv(3).decode())
        place = my_socket.recv(1024).decode()
    except:
        my_socket.close()
        sys.exit()

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

    data_clients.append([player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), '', "forest"])

    zira = Zira(screen)

    zira.set_zira(data_clients)

    treat_messages = TreatMessages(my_socket, data_clients, zira)

    player.set_treat_messages(treat_messages)

    send_data_clients = pickle.dumps(["PlayerValues", player.get_starting_bear_point_x(), player.get_starting_bear_point_y(), player.get_name_player(), '', "forest"])
    my_socket.send(send_data_clients)

    x = threading.Thread(target=treat_messages.draw_new_board)
    x.start()

    finish1 = False
    try:
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

                    is_user_want_send_everyone_message = user_want_send_everyone_message(pos_x, pos_y, player, treat_messages)
                    if is_user_want_send_everyone_message == False:
                        is_user_clicked_on_box_to_play = user_clicked_on_box_to_play(pos_x, pos_y, zira, player)
                        if is_user_clicked_on_box_to_play == False:
                            is_user_want_to_see_control_board = user_want_to_see_control_board(pos_x, pos_y, player, zira, my_socket)
                            if is_user_want_to_see_control_board == False:
                                is_user_want_close_control_board = user_want_close_control_board(pos_x, pos_y, player, zira, my_socket, treat_messages)
                                if is_user_want_close_control_board == False:
                                    is_user_want_to_go_to_pool_background = user_want_to_go_to_pool_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket)
                                    if is_user_want_to_go_to_pool_background == False:
                                        is_user_want_to_go_to_forest_from_pool_background = user_want_to_go_to_forest_from_pool_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket)
                                        if is_user_want_to_go_to_forest_from_pool_background == False:
                                            is_user_want_to_go_to_slides_from_forest_background = user_want_to_go_to_slides_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket)
                                            if is_user_want_to_go_to_slides_from_forest_background == False:
                                                is_user_want_to_go_to_forest_from_slides_background = user_want_to_go_to_forest_from_slides_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket)
                                                if is_user_want_to_go_to_forest_from_slides_background == False:
                                                    is_user_want_to_go_to_vacation_from_forest_background = user_want_to_go_to_vacation_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira, treat_messages, my_socket)
                                                    if is_user_want_to_go_to_vacation_from_forest_background == False:
                                                        is_user_want_to_go_to_forest_from_vacation_background = user_want_to_go_to_forest_from_vacation_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira,treat_messages, my_socket)
                                                        if is_user_want_to_go_to_forest_from_vacation_background == False:
                                                            is_user_want_to_go_to_beach_from_forest_background = user_want_to_go_to_beach_from_forest_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira,treat_messages, my_socket)
                                                            if is_user_want_to_go_to_beach_from_forest_background == False:
                                                                is_user_want_to_go_to_forest_from_beach_background = user_want_to_go_to_forest_from_beach_background(pos_x, pos_y, WINDOW_WIDTH, WINDOW_HEIGHT, player, zira,treat_messages, my_socket)
                                                                if is_user_want_to_go_to_forest_from_beach_background == False:
                                                                    player.move_player(pos_x - 100, pos_y - 100)
    except:
        finish1 = True
        message = pickle.dumps(["Exit", player.get_name_player()])
#        my_socket.send(message)
#        time.sleep(0.2)
#        my_socket.close()
        sys.exit()


if __name__ == '__main__':
    main()
