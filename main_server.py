import pygame
from tkinter import Tk
import chat
import time
import os
import subprocess
import sys
import socket
import select
import pickle
import sqlite3
import threading
import  pyautogui

WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768
STARTING_BEAR_POINT_X = 1000
STARTING_BEAR_POINT_Y = 300
BOX_POINT_X = 200
BOX_POINT_Y = 500
CLICK_FOR_SENDING_MESSAGE_POINT_X = 690
CLICK_FOR_SENDING_MESSAGE_POINT_Y = 690

SERVER_ID                          = 1
MATE_SERVER_ID                     = 2
PORT_EIX_EIGUL_MAX_RANGE           = 5000
PORT_EIX_EIGUL_START_PORT_SERVER_1 = 10000
PORT_EIX_EIGUL_START_PORT_SERVER_2 = 20000
PORT_EIX_EIGUL                     = PORT_EIX_EIGUL_START_PORT_SERVER_1

#SQL_DATABASE_NAME = "db_member.db"
global SQL_DATABASE_NAME


def send_client_board_game(current_socket):
    current_socket.send(str(WINDOW_WIDTH).encode())
    current_socket.send(str(WINDOW_HEIGHT).encode())
    place = str(STARTING_BEAR_POINT_X) + " " + str(STARTING_BEAR_POINT_Y)
    current_socket.send(place.encode())


def change_status_to_connected(mate_server_socket, name_player):
    global  SERVER_ID

    print("change_status_to_connected SERVER_ID="+str(SERVER_ID) + " name_player=" + str(name_player) + " statusPlayerInGame=connected")

    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE `member` SET `serverId` = ?, `statusPlayerInGame` = ? WHERE `userName` = ?",
                   (int(SERVER_ID),str("connected"), str(name_player)))
    conn.commit()
    conn.close()
    get_and_send_row_to_mate_server(mate_server_socket, name_player)


def init_database():
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, serverId INTEGER, userName TEXT, password TEXT, firstName TEXT, lastName TEXT, statusEixEigulGame TEXT, portEixEigul INTEGER, numberOfWinsEixEigul INTEGER, statusBrikeBreakerGame TEXT, numberOfWinsBrikeBreakerGame INTEGER, statusSnakeGame TEXT, scoreOfSnakeGame INTEGER, statusColorGame TEXT, scoreOfColorGame INTEGER, statusPlayerInGame TEXT, socket TEXT)")
    conn.commit()
    conn.close()


def clear_database():
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `member`")
    conn.commit()
    conn.close()


def clear_mate_palayer_status_in_databased():
    global  MATE_SERVER_ID

    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM `member` WHERE `serverId` = ?", (int(MATE_SERVER_ID),))

    list_user = cursor.fetchall()

    for row in list_user:
        userName = row[2]
        print("Clear Mate players status userName=" + userName)
        cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ?, `statusBrikeBreakerGame` = ?, `statusSnakeGame` = ?, `statusColorGame` = ?, `statusPlayerInGame` = ?, `socket` = ? WHERE `userName` = ?",
            ("not playing", 0, "not playing", "not playing", "not playing", "not connected", 0, userName))

    conn.commit()
    conn.close()

def clear_palayer_status_in_databased():
    global  MATE_SERVER_ID

    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM `member`")

    list_user = cursor.fetchall()

    for row in list_user:
        userName = row[2]
        print("Clear Mate players status userName=" + userName)
        cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ?, `statusBrikeBreakerGame` = ?, `statusSnakeGame` = ?, `statusColorGame` = ?, `statusPlayerInGame` = ?, `socket` = ? WHERE `userName` = ?",
            ("not playing", 0, "not playing", "not playing", "not playing", "not connected", 0, userName))

    conn.commit()
    conn.close()

def server_connect(list_client):
    command = list_client[0]

    if command == 'ServerConnect':
        return True

    return False


def Exit(list_client, current_socket, mate_server_socket):
    command = list_client[0]
    if command == 'Exit':
        current_socket.close()
        name_player = list_client[1]
        print("Exit command=" + command + " name_player=" + name_player)
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ?, `statusBrikeBreakerGame` = ?, `statusSnakeGame` = ?, `statusColorGame` = ?, `statusPlayerInGame` = ?, `socket` = ? WHERE `userName` = ?",
            ("not playing", 0, "not playing", "not playing", "not playing", "not connected", 0, name_player))
        conn.commit()
        conn.close()
        get_and_send_row_to_mate_server(mate_server_socket, name_player)
        return True

    return False


def check_info_about_eix_eigul_game(list_client, current_socket):

    command = list_client[0]

    if command == 'controlBoard':
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        background_picture = list_client[1]
        if background_picture == 'forest':
            cursor.execute("SELECT MAX(numberOfWinsEixEigul) FROM `member`")
            number_of_wins = cursor.fetchone()[0]

            string_of_the_names = ''

            if number_of_wins == 0:
                string_of_the_names = "No one won yet!"
            else:
                cursor.execute("SELECT userName FROM `member` WHERE `numberOfWinsEixEigul` = ?", (number_of_wins,))
                list_tuple_of_the_names = cursor.fetchall()

                for i in range(len(list_tuple_of_the_names)):

                    if i == 0:
                        string_of_the_names = list_tuple_of_the_names[i][0]
                    else:
                        string_of_the_names = string_of_the_names + ", " + list_tuple_of_the_names[i][0]


            cursor.execute("SELECT COUNT(statusEixEigulGame) FROM `member` WHERE statusEixEigulGame = 'playing'")
            number_of_eix_eigul_players = cursor.fetchone()[0]

            message_control_board = pickle.dumps(["control board", "eix eigul", string_of_the_names, number_of_wins, number_of_eix_eigul_players])
            current_socket.send(message_control_board)
            conn.close()
            return True

    return False


def check_info_about_brike_breaker_game(list_client, current_socket):

    command = list_client[0]

    if command == 'controlBoard':
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()

        background_picture = list_client[1]
        if background_picture == 'pool':
            cursor.execute("SELECT MAX(numberOfWinsBrikeBreakerGame) FROM `member`")
            number_of_wins = cursor.fetchone()[0]

            string_of_the_names = ''

            if number_of_wins == 0:
                string_of_the_names = "No one won yet!"
            else:
                cursor.execute("SELECT userName FROM `member` WHERE `numberOfWinsBrikeBreakerGame` = ?", (number_of_wins,))
                list_tuple_of_the_names = cursor.fetchall()

                for i in range(len(list_tuple_of_the_names)):

                    if i == 0:
                        string_of_the_names = list_tuple_of_the_names[i][0]
                    else:
                        string_of_the_names = string_of_the_names + ", " + list_tuple_of_the_names[i][0]

            cursor.execute("SELECT COUNT(statusBrikeBreakerGame) FROM `member` WHERE statusBrikeBreakerGame = 'playing'")
            number_of_brike_breaker_players = cursor.fetchone()[0]

            message_control_board = pickle.dumps(["control board", "brike breaker", string_of_the_names, number_of_wins, number_of_brike_breaker_players])
            current_socket.send(message_control_board)
            conn.close()
            return True

    return False


def check_info_about_color_game(list_client, current_socket):

    command = list_client[0]

    if command == 'controlBoard':
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        background_picture = list_client[1]
        if background_picture == 'vacation' or background_picture == 'beach':
            cursor.execute("SELECT MAX(scoreOfColorGame) FROM `member`")
            score = cursor.fetchone()[0]

            string_of_the_names = ''

            if score == 0:
                string_of_the_names = "No one did scores!"
            else:
                cursor.execute("SELECT userName FROM `member` WHERE `scoreOfColorGame` = ?", (score,))
                list_tuple_of_the_names = cursor.fetchall()

                for i in range(len(list_tuple_of_the_names)):

                    if i == 0:
                        string_of_the_names = list_tuple_of_the_names[i][0]
                    else:
                        string_of_the_names = string_of_the_names + ", " + list_tuple_of_the_names[i][0]

            cursor.execute("SELECT COUNT(statusColorGame) FROM `member` WHERE statusColorGame = 'playing'")
            number_of_color_players = cursor.fetchone()[0]

            message_control_board = pickle.dumps(["control board", "color", string_of_the_names, score, number_of_color_players])
            conn.close()
            current_socket.send(message_control_board)
            return True

    return False


def check_info_about_snake_game(list_client, current_socket):

    command = list_client[0]

    if command == 'controlBoard':
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        background_picture = list_client[1]
        if background_picture == 'slides':
            cursor.execute("SELECT MAX(scoreOfSnakeGame) FROM `member`")
            score = cursor.fetchone()[0]

            string_of_the_names = ''

            if score == 0:
                string_of_the_names = "No one did scores!"
            else:
                cursor.execute("SELECT userName FROM `member` WHERE `scoreOfSnakeGame` = ?", (score,))
                list_tuple_of_the_names = cursor.fetchall()

                for i in range(len(list_tuple_of_the_names)):

                    if i == 0:
                        string_of_the_names = list_tuple_of_the_names[i][0]
                    else:
                        string_of_the_names = string_of_the_names + ", " + list_tuple_of_the_names[i][0]

            cursor.execute("SELECT COUNT(statusSnakeGame) FROM `member` WHERE statusSnakeGame = 'playing'")
            number_of_snake_players = cursor.fetchone()[0]

            message_control_board = pickle.dumps(["control board", "snake", string_of_the_names, score, number_of_snake_players])
            conn.close()
            current_socket.send(message_control_board)
            return True

    return False

def is_playing_game(USERNAME):

    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT statusEixEigulGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
    is_not_playing_eix_eigul = cursor.fetchone()[0]

    cursor.execute("SELECT statusSnakeGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
    is_not_playing_snake = cursor.fetchone()[0]

    cursor.execute("SELECT statusColorGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
    is_not_playing_color = cursor.fetchone()[0]

    cursor.execute("SELECT statusBrikeBreakerGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
    is_not_playing_brike_breaker = cursor.fetchone()[0]

    if is_not_playing_eix_eigul == 'not playing' and is_not_playing_snake == 'not playing' and is_not_playing_color == 'not playing' and is_not_playing_brike_breaker == 'not playing':
        conn.close()
        return False

    conn.close()
    return True

def get_raddr_from_socket(socket):
    socket_list = list(socket.split("raddr=("))
    raddr_list = list(socket_list[1].split(","))
    raddr = str(raddr_list[0])
    return raddr



def change_status_eix_eigul_game(list_client, current_socket, mate_server_socket):
    global PORT_EIX_EIGUL
    global PORT_EIX_EIGUL_MAX_RANGE
    global SERVER_ID

    command = list_client[0]

    if command == 'StatusEixEigulGame':
        USERNAME = list_client[1]

        if is_playing_game(USERNAME) == False:
            conn = sqlite3.connect(SQL_DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM `member` WHERE `serverId` = ? and `statusEixEigulGame` = ?", (int (SERVER_ID), str("waiting")))

            if cursor.fetchone() is not None:
                cursor.execute("SELECT userName FROM `member` WHERE `serverId` = ? and `statusEixEigulGame` = ?", (int (SERVER_ID), str("waiting")))
                username_of_other_player = cursor.fetchone()[0]
                cursor.execute("SELECT portEixEigul FROM `member` WHERE `userName` = ?", (str(username_of_other_player),))
                port_eix_eigul = cursor.fetchone()[0]

                #cursor.execute("SELECT socket FROM `member` WHERE `userName` = ?", (str(username_of_other_player),))
                #client_socket = cursor.fetchone()[0]
                #raddr = ""
                #raddr = get_raddr_from_socket(client_socket)
                #print("remote ip = " + str(raddr))

                cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ? WHERE `userName` = ?", (str("playing"), str(username_of_other_player)))
                cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ? WHERE `userName` = ?", (str("playing"), port_eix_eigul, str(USERNAME)))
                conn.commit()
                conn.close()
                get_and_send_row_to_mate_server(mate_server_socket, USERNAME)
                get_and_send_row_to_mate_server(mate_server_socket, username_of_other_player)
                message_change_status_eix_eigul_game = ["player_o.py", port_eix_eigul]
            else:
                cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ?  WHERE `userName` = ?", (str("waiting"), PORT_EIX_EIGUL, str(USERNAME)))
                conn.commit()
                conn.close()
                get_and_send_row_to_mate_server(mate_server_socket, USERNAME)
                message_change_status_eix_eigul_game = ["player_x.py", PORT_EIX_EIGUL]
                PORT_EIX_EIGUL = PORT_EIX_EIGUL + 1


            message_change_status_eix_eigul_game = pickle.dumps(message_change_status_eix_eigul_game)
            current_socket.send(message_change_status_eix_eigul_game)
            return True
        else:
            message_change_status_eix_eigul_game = pickle.dumps(["you are waiting or playing"])
            current_socket.send(message_change_status_eix_eigul_game)
            return True

    return False

def change_status_brike_breaker_game(list_client, current_socket, mate_server_socket):

    command = list_client[0]

    if command == 'StatusBrikeBreakerGame':
        USERNAME = list_client[1]

        if is_playing_game(USERNAME) == False:
            conn = sqlite3.connect(SQL_DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("UPDATE `member` SET `statusBrikeBreakerGame` = ? WHERE `userName` = ?",(str("playing"), str(USERNAME)))
            conn.commit()

            message_change_status_brike_breaker_game = ["brike_breaker_game.py"]

            message_change_status_brike_breaker_game = pickle.dumps(message_change_status_brike_breaker_game)
            conn.close()
            current_socket.send(message_change_status_brike_breaker_game)
            return True
        else:
            message_change_status_brike_breaker_game = pickle.dumps(["you are waiting or playing"])
            current_socket.send(message_change_status_brike_breaker_game)
            return True

    return False


def change_status_snake_game(list_client, current_socket, mate_server_socket):

    command = list_client[0]

    if command == 'StatusSnakeGame':
        USERNAME = list_client[1]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()

        if is_playing_game(USERNAME) == False:

            cursor.execute("UPDATE `member` SET `statusSnakeGame` = ? WHERE `userName` = ?",(str("playing"), str(USERNAME)))
            conn.commit()

            message_change_status_snake_game = ["snake_game.py"]

            message_change_status_snake_game = pickle.dumps(message_change_status_snake_game)
            conn.close()
            current_socket.send(message_change_status_snake_game)
            return True
        else:
            message_change_status_snake_game = pickle.dumps(["you are waiting or playing"])
            current_socket.send(message_change_status_snake_game)
            return True

    return False


def change_status_color_game(list_client, current_socket, mate_server_socket):
    command = list_client[0]

    if command == 'StatusColorGame':
        USERNAME = list_client[1]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()

        if is_playing_game(USERNAME) == False:

            cursor.execute("UPDATE `member` SET `statusColorGame` = ? WHERE `userName` = ?",(str("playing"), str(USERNAME)))
            conn.commit()

            change_status_color_game = ["color_game.py"]

            change_status_color_game = pickle.dumps(change_status_color_game)
            conn.close()
            current_socket.send(change_status_color_game)
            return True
        else:
            change_status_color_game = pickle.dumps(["you are waiting or playing"])
            current_socket.send(change_status_color_game)
            return True

    return False

def winner_eix_eigul(list_client,mate_server_socket):

    command = list_client[0]

    if command == 'WinnerEixEigul':
        USERNAME = list_client[1]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT numberOfWinsEixEigul FROM `member` WHERE `userName` = ?", (str(USERNAME),))
        num_of_wins = cursor.fetchone()[0]
        num_of_wins = num_of_wins + 1
        cursor.execute("UPDATE `member` SET `numberOfWinsEixEigul` = ? WHERE `userName` = ?",(num_of_wins, str(USERNAME)))
        conn.commit()
        conn.close()
        get_and_send_row_to_mate_server(mate_server_socket, USERNAME)
        return True

    return False

def winner_brike_breaker(list_client,mate_server_socket):

    command = list_client[0]

    if command == 'WinnerBrikeBreaker':
        USERNAME = list_client[1]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT numberOfWinsBrikeBreakerGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
        num_of_wins = cursor.fetchone()[0]
        num_of_wins = num_of_wins + 1
        cursor.execute("UPDATE `member` SET `numberOfWinsBrikeBreakerGame` = ? WHERE `userName` = ?",(num_of_wins, str(USERNAME)))
        conn.commit()
        conn.close()
        get_and_send_row_to_mate_server(mate_server_socket, USERNAME)

        return True

    return False

def winner_color(list_client,mate_server_socket):

    command = list_client[0]

    if command == 'WinnerColorGame':
        score = list_client[1]
        USERNAME = list_client[2]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT scoreOfColorGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
        max_score_color_game = cursor.fetchone()[0]
        if score > max_score_color_game:
            cursor.execute("UPDATE `member` SET `scoreOfColorGame` = ? WHERE `userName` = ?", (score, str(USERNAME)))
            conn.commit()

        conn.close()
        get_and_send_row_to_mate_server(mate_server_socket, USERNAME)

        return True

    return False

def winner_snake(list_client, mate_server_socket):

    command = list_client[0]

    if command == 'WinnerSnakeGame':
        score = list_client[1]
        USERNAME = list_client[2]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT scoreOfSnakeGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
        max_score_snake_game = cursor.fetchone()[0]
        if score > max_score_snake_game:
            cursor.execute("UPDATE `member` SET `scoreOfSnakeGame` = ? WHERE `userName` = ?", (score, str(USERNAME)))
            conn.commit()
        conn.close()
        get_and_send_row_to_mate_server(mate_server_socket, USERNAME)

        return True

    return False

def finish_game(list_client, mate_server_socket):

    command = list_client[0]

    if command == 'FinishGame':
        game = list_client[1]
        USERNAME = list_client[2]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        if game == "eix eigul":
            cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ? WHERE `userName` = ?", (str("not playing"), 0, str(USERNAME)))
            conn.commit()

        elif game == "brike breaker":
            cursor.execute("UPDATE `member` SET `StatusBrikeBreakerGame` = ? WHERE `userName` = ?", (str("not playing"), str(USERNAME)))
            conn.commit()

        elif game == "snake":
            cursor.execute("UPDATE `member` SET `statusSnakeGame` = ? WHERE `userName` = ?", (str("not playing"), str(USERNAME)))
            conn.commit()

        else:
            cursor.execute("UPDATE `member` SET `StatusColorGame` = ? WHERE `userName` = ?", (str("not playing"), str(USERNAME)))
            conn.commit()

        conn.close()
        get_and_send_row_to_mate_server(mate_server_socket, USERNAME)

        return True

    return False


def Register(list_client, current_socket, mate_server_socket):
    command = list_client[0]
    global SERVER_ID

    if command == 'Register':
        USERNAME = list_client[1]
        PASSWORD = list_client[2]
        FIRSTNAME = list_client[3]
        LASTNAME = list_client[4]
        print("receive " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        if USERNAME == "" or PASSWORD == "" or FIRSTNAME == "" or LASTNAME == "":
            message_register = pickle.dumps(["Please complete the required field!", "orange"])
        else:
            cursor.execute("SELECT * FROM `member` WHERE `userName` = ?", (USERNAME,))
            if cursor.fetchone() is not None:
                print("Username is already taken " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                message_register = pickle.dumps(["Username is already taken", "red"])
            else:
                print("Username insert " + command + " SERVER_ID"+ str(SERVER_ID)+" USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                cursor.execute("INSERT INTO `member` (serverId, userName, password, firstName, lastName, statusEixEigulGame, portEixEigul, numberOfWinsEixEigul, StatusBrikeBreakerGame, numberOfWinsBrikeBreakerGame, StatusSnakeGame, scoreOfSnakeGame, StatusColorGame, scoreOfColorGame, statusPlayerInGame, socket) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (int(SERVER_ID),str(USERNAME), str(PASSWORD), str(FIRSTNAME), str(LASTNAME), str("not playing"), 0, 0,
                     "not playing", 0, "not playing", 0, "not playing", 0, "not connected", 0))
                conn.commit()
                message_register = pickle.dumps(["Successfully Created!", "black"])

            cursor.close()
            conn.close()

        print("send to client Register reply")
        current_socket.send(message_register)
        print("send to mate server ServerUpdate")
        message_server_register = pickle.dumps(["ServerUpdate", SERVER_ID, USERNAME, PASSWORD, FIRSTNAME, LASTNAME, "not playing", 0 , 0, "not playing", 0, "not playing", 0, "not playing", 0, "not connected", 0])

        if mate_server_socket and not mate_server_socket.fileno() == -1:
            mate_server_socket.send(message_server_register)

        return True
    else:
        # print("2. getsockname = " + current_socket.getsockname())
        return False

def UnRegister(list_client, current_socket, mate_server_socket):
    command = list_client[0]

    if command == 'UnRegister':
        USERNAME = list_client[1]
        PASSWORD = list_client[2]

        print("receive " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        if USERNAME == "" or PASSWORD == "":
            message_unregister = pickle.dumps(["Please complete the required field!", "orange"])
        else:
            cursor.execute("SELECT * FROM `member` WHERE `userName` = ? and `statusPlayerInGame` = ?", (USERNAME, "not connected"))
            if cursor.fetchone() is None:
                print("Username is dosn't exist " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                message_unregister = pickle.dumps(["Username dosn't exist or already connected", "red"])
            else:
                print("Username delete " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                cursor.execute("DELETE FROM `member` WHERE `userName` = ?", str(USERNAME))
                #cursor.execute("DELETE FROM `member` WHERE `userName` = cfff")
                conn.commit()
                message_unregister = pickle.dumps(["Successfully deleted!", "black"])

            cursor.close()
            conn.close()

        print("send to client UnRegister reply")
        current_socket.send(message_unregister)

        if mate_server_socket and not mate_server_socket.fileno() == -1:
            print("send to mate server ServerDeleteUpdate")
            message_server_unregister = pickle.dumps(["ServerDeleteUpdate", USERNAME, PASSWORD])
            mate_server_socket.send(message_server_unregister)

        return True
    else:
        # print("2. getsockname = " + current_socket.getsockname())
        return False

def server_update(list_client):
    command = list_client[0]

    if command == 'ServerUpdate':
        server_id               = list_client[1]
        user_name               = list_client[2]
        password                = list_client[3]
        first_name              = list_client[4]
        last_name               = list_client[5]
        statusEixEigulGame      = list_client[6]
        portEixEigul            = list_client[7]
        numberOfWinsEixEigul    = list_client[8]

        statusBrikeBreakerGame  = list_client[9]
        numberOfWinsBrikeBreakerGame= list_client[10]
        statusSnakeGame         = list_client[11]
        scoreOfSnakeGame        = list_client[12]
        statusColorGame         = list_client[13]
        scoreOfColorGame        = list_client[14]
        statusPlayerInGame      = list_client[15]

        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `member` WHERE `userName` = ?", (user_name))
        if cursor.fetchone() is not None:
            print("Username update " + command + " server_id=" + str(server_id) + " user_name=" + user_name + " statusPlayerInGame=" + statusPlayerInGame)

#            cursor.execute(
#                "UPDATE `member` SET 'server_id' = ? , `password` = ?, `firstName` = ?,`lastName` = ? ,`statusEixEigulGame` = ?, portEixEigul = ? ,`numberOfWinsEixEigul` = ? ,`statusBrikeBreakerGame` = ?,`numberOfWinsBrikeBreakerGame` = ?,`statusSnakeGame` = ?,`scoreOfSnakeGame` = ?,`statusColorGame` = ?,`scoreOfColorGame`= ? ,`statusPlayerInGame` = ? WHERE `userName` = ?",
#                (int(server_id), str(password), str(first_name), str(last_name), str(statusEixEigulGame), int(portEixEigul),  int(numberOfWinsEixEigul),
#                 str(statusBrikeBreakerGame), int(numberOfWinsBrikeBreakerGame), str(statusSnakeGame), int(scoreOfSnakeGame), str(statusColorGame), int(scoreOfColorGame),
#                 str(statusPlayerInGame), str(user_name)))
            cursor.execute(
                "UPDATE `member` SET `serverId` = ?, `password` = ?, `firstName` = ?,`lastName` = ? ,`statusEixEigulGame` = ?, portEixEigul = ? ,`numberOfWinsEixEigul` = ? ,`statusBrikeBreakerGame` = ?,`numberOfWinsBrikeBreakerGame` = ?,`statusSnakeGame` = ?,`scoreOfSnakeGame` = ?,`statusColorGame` = ?,`scoreOfColorGame`= ? ,`statusPlayerInGame` = ? WHERE `userName` = ?",
                (str(server_id), str(password), str(first_name), str(last_name), str(statusEixEigulGame), int(portEixEigul),  int(numberOfWinsEixEigul),
                 str(statusBrikeBreakerGame), int(numberOfWinsBrikeBreakerGame), str(statusSnakeGame), int(scoreOfSnakeGame), str(statusColorGame), int(scoreOfColorGame),
                 str(statusPlayerInGame), str(user_name)))

            conn.commit()
        else:
            print("Username insert " + command + " user_name=" + user_name + " statusPlayerInGame=" + statusPlayerInGame + " statusEixEigulGame=" + statusEixEigulGame)
            cursor.execute(
                "INSERT INTO `member` (serverid, userName, password, firstName, lastName, statusEixEigulGame, portEixEigul, numberOfWinsEixEigul, statusBrikeBreakerGame ,numberOfWinsBrikeBreakerGame ,statusSnakeGame, scoreOfSnakeGame, statusColorGame , scoreOfColorGame , statusPlayerInGame ,  socket) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (int(server_id), str(user_name), str(password), str(first_name), str(last_name), str(statusEixEigulGame), int(portEixEigul), int(numberOfWinsEixEigul),
                 str(statusBrikeBreakerGame), int(numberOfWinsBrikeBreakerGame), str(statusSnakeGame), int(scoreOfSnakeGame), str(statusColorGame), int(scoreOfColorGame),
                 str(statusPlayerInGame), 0))
            conn.commit()

        cursor.close()
        conn.close()
        return True
    else:
        # print("receive error for " + command)
        return False

def server_delete_update(list_client):
    command = list_client[0]

    if command == 'ServerDeleteUpdate':
        user_name = list_client[1]
        password = list_client[2]

        print("receive ServerDeleteUpdate user_name="+user_name)

        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `member` WHERE `userName` = ? and 'password' = ?", (user_name,password))
        if cursor.fetchone() is not None:
            print("Username update " + command + " user_name=" + user_name)
            cursor.execute("DELETE FROM `member` WHERE `userName` = ?",str(user_name))
            conn.commit()

        cursor.close()
        conn.close()
        return True
    else:
        # print("receive error for " + command)
        return False


def Login(list_client, current_socket):
    global  SERVER_ID

    command = list_client[0]

    if command == 'Login':
        USERNAME = list_client[1]
        PASSWORD = list_client[2]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        if USERNAME == "" or PASSWORD == "":
            message_login = pickle.dumps(["Please complete the required field!", "orange"])
        else:
            cursor.execute("SELECT * FROM `member` WHERE `userName` = ? and `password` = ?", (USERNAME, PASSWORD))
            if cursor.fetchone() is not None:
                cursor.execute("SELECT statusPlayerInGame FROM `member` WHERE `userName` = ?", (str(USERNAME),))
                status_player_in_game = cursor.fetchone()[0]
                if status_player_in_game == 'not connected':
                    message_login = pickle.dumps(["You Successfully Login", "blue"])
                    cursor.execute("UPDATE `member` SET 'serverId' = ?, `statusPlayerInGame` = ?,`socket` = ? WHERE `userName` = ?",
                                   (str(SERVER_ID),str("connecting"), str(current_socket), str(USERNAME)))
                    conn.commit()
                    print("user update user=" + str(USERNAME) + " statusPlayerInGame=connecting")
                else:
                    message_login = pickle.dumps(["The player is already in the game", "red"])

            else:
                message_login = pickle.dumps(["Invalid Username or password", "red"])

        current_socket.send(message_login)

        if pickle.loads(message_login)[0] == "You Successfully Login":
            send_client_board_game(current_socket)

        conn.close()
        return True
    else:
        return False


def send_row_to_mate_server(mate_server_socket: object, row):
    server_id           = row[1]
    user_name           = row[2]
    password            = row[3]
    first_name          = row[4]
    last_name           = row[5]
    statusEixEigulGame  = row[6]
    portEixEigul        = row[7]
    numberOfWinsEixEigul = row[8]
    statusBrikeBreakerGame = row[9]
    numberOfWinsBrikeBreakerGame = row[10]
    statusSnakeGame = row[11]
    scoreOfSnakeGame = row[12]
    statusColorGame = row[13]
    scoreOfColorGame = row[14]
    statusPlayerInGame = row[15]

    if mate_server_socket and not mate_server_socket.fileno() == -1:
        print("send to mate: server_id="+ str(server_id) +" user_name"+user_name + " statusEixEigulGame="+statusEixEigulGame + " portEixEigul"+ str(portEixEigul))
        data_update = pickle.dumps(["ServerUpdate", server_id, user_name, password, first_name, last_name, statusEixEigulGame, portEixEigul,numberOfWinsEixEigul, statusBrikeBreakerGame, numberOfWinsBrikeBreakerGame, statusSnakeGame, scoreOfSnakeGame,statusColorGame,scoreOfColorGame, statusPlayerInGame])
        #print("send to mate:" + str(data_update))
        mate_server_socket.send(data_update)


def get_and_send_row_to_mate_server(mate_server_socket, user_name):

    if not mate_server_socket or mate_server_socket.fileno() == -1:
        return

    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `member` WHERE `userName` = ?", (user_name,))
    list_user = cursor.fetchall()
    print("get_and_send_row_to_mate_server")

    for row in list_user:
        send_row_to_mate_server(mate_server_socket, row)

    conn.close()


def sync_db_to_mate_server(mate_server_socket):
    print ("sync_db_to_mate_server")
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `member`")
    list_user = cursor.fetchall()

    for row in list_user:
        send_row_to_mate_server(mate_server_socket, row)
        time.sleep(0.5)

    conn.close()


def send_all_clients(open_client_sockets, data_clients):
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT socket FROM `member` WHERE `statusPlayerInGame` = ?", ("connected",))
    list_tuple_of_the_sockets = cursor.fetchall()

    #    print("data- " + str(data_clients))
    #    data_dump = pickle.dumps(data_clients)

    for i in range(len(list_tuple_of_the_sockets)):

        for client in open_client_sockets:

            if list_tuple_of_the_sockets[i][0] == str(client):
                #print("data- " + str(data_clients))
                data_dump = pickle.dumps(data_clients)
                client.send(data_dump)
                break
    conn.close()


def thread_mate_server_function(mate_server_socket):
    while True:
        try:
            bytes_client = mate_server_socket.recv(1024)
            list_client = pickle.loads(bytes_client)
            is_register = server_update(list_client)
            is_delete_update = server_delete_update(list_client)
        except:
            server_socket_has_been_closed(mate_server_socket)
            print("thread_mate_server_function except")
            return


def thread_mate_server(mate_server_socket):
    #    time.sleep(5)
    x = threading.Thread(target=thread_mate_server_function, args=(mate_server_socket,))
    x.start()


def thread_server_function(mate_server_socket):
    try:
        clear_mate_palayer_status_in_databased()
        sync_db_to_mate_server(mate_server_socket)
    except:
        print("thread_server_function except")


def thread_server(mate_server_socket):
    x = threading.Thread(target=thread_server_function, args=(mate_server_socket,))
    x.start()


def client_socket_has_been_closed(current_socket, data_clients, mate_server_socket, socket_id_and_user_name):
    list_client = ["Exit", "user_name", "password"]
    user_name = ""
    for i in range(len(socket_id_and_user_name)):
        print("socket_has_been_closed")
        if current_socket == socket_id_and_user_name[i][1]:
            user_name = socket_id_and_user_name[i][0]
            list_client[0] = "Exit"
            list_client[1] = socket_id_and_user_name[i][0]
            Exit(list_client, current_socket, mate_server_socket)
            socket_id_and_user_name.remove(socket_id_and_user_name[i])
            break

    for i in range(len(data_clients)):
        print("socket_has_been_closed")
        if user_name == data_clients[i][2]:
            data_clients.remove(data_clients[i])
            break

def server_socket_has_been_closed(mate_server_socket):
    if mate_server_socket and not mate_server_socket.fileno() == -1:
        mate_server_socket.close()

    clear_mate_palayer_status_in_databased()

def socket_has_been_closed(current_socket, rlist, data_clients, mate_server_socket, open_client_sockets,
                           socket_id_and_user_name):
    list_client = ["Exit", "user_name", "password"]
    user_name = ""
    for current_socket in rlist:
        try:
            bytes_client = current_socket.recv(1024)
            print("select.select current_socket=" + current_socket, list_client)
        except:
            try:
                open_client_sockets.remove(current_socket)
                if current_socket == mate_server_socket:
                    server_socket_has_been_closed(mate_server_socket)
                else:
                    client_socket_has_been_closed(current_socket, data_clients, mate_server_socket, socket_id_and_user_name)
            except:
                print("socket_has_been_closed user not exist")


def main():
    """
    Add Documentation here
    """
    global SQL_DATABASE_NAME
    global PORT_EIX_EIGUL
    global PORT_EIX_EIGUL_START_PORT_SERVER_2
    global PORT_EIX_EIGUL_START_PORT_SERVER_1
    global SERVER_ID
    global MATE_SERVER_ID

    pass  # Replace Pass with Your Code

    print(sys.argv[1])
    my_ip = sys.argv[1]
    my_port = int(sys.argv[2])

    mate_server_ip = sys.argv[3]
    mate_server_port = int(sys.argv[4])
    SQL_DATABASE_NAME = sys.argv[5]

    open_client_sockets = []
    data_clients = []
    socket_id_and_user_name = []
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    print(
        "server begin my_ip=" + mate_server_ip + "/" + str(my_port) + ", mate_server_ip=" + mate_server_ip + "/" + str(
            mate_server_port) + "SQL_DATABASE_NAME=" + SQL_DATABASE_NAME)
    server_socket = socket.socket()
    mate_server_socket = 0
    init_database()

    try:
        mate_server_socket = socket.socket()
        mate_server_socket.connect((mate_server_ip, mate_server_port))
        clear_database()
        SERVER_ID      = 2
        MATE_SERVER_ID = 1
        PORT_EIX_EIGUL = PORT_EIX_EIGUL_START_PORT_SERVER_2
        message_server_connect = pickle.dumps(["ServerConnect"])
        thread_mate_server(mate_server_socket)
        if mate_server_socket and not mate_server_socket.fileno() == -1:
            mate_server_socket.send(message_server_connect)
        print("connected to mate server")
        # sync_db_to_mate_server(mate_server_socket) only the connected send the data !!
    except socket.error:
        mate_server_socket = 0
        clear_palayer_status_in_databased()
        print("no mate server cleat all user status")

    server_socket.bind(('0.0.0.0', my_port))
    server_socket.listen(1)

    game_not_over = True
    while game_not_over:
        try:
            rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, [], [])

            for current_socket in rlist:
                if current_socket is server_socket:
                    (new_socket, address) = server_socket.accept()
                    print('socket created ' + str(address))
                    open_client_sockets.append(new_socket)

                else:
                    try:
                        bytes_client = current_socket.recv(1024)
                        list_client = pickle.loads(bytes_client)
                        print("receive msg" + str(list_client))
                        is_server_connect = server_connect(list_client)
                        if is_server_connect == True:
                            print("receive server connect ")
                            mate_server_socket = current_socket
                            thread_server_function(current_socket)

                        print("receive new msg")
                        is_exit = Exit(list_client, current_socket, mate_server_socket)
                        is_update = server_update(list_client)
                        is_delete_update = server_delete_update(list_client)
                        is_delete_update = server_delete_update(list_client)
                        is_register = Register(list_client, current_socket, mate_server_socket)
                        is_unregister = UnRegister(list_client, current_socket, mate_server_socket)
                        is_login = Login(list_client, current_socket)
                        is_check_info_about_eix_eigul_game = check_info_about_eix_eigul_game(list_client, current_socket)
                        is_check_info_about_brike_breaker_game = check_info_about_brike_breaker_game(list_client,current_socket)
                        is_check_info_about_color_game = check_info_about_color_game(list_client,current_socket)
                        is_check_info_about_snake_game = check_info_about_snake_game(list_client, current_socket)
                        is_status_eix_eigul_game = change_status_eix_eigul_game(list_client, current_socket, mate_server_socket)
                        is_status_brike_breaker_game = change_status_brike_breaker_game(list_client, current_socket, mate_server_socket)
                        is_status_snake_game = change_status_snake_game(list_client, current_socket, mate_server_socket)
                        is_status_color_game = change_status_color_game(list_client, current_socket, mate_server_socket)
                        is_winner_eix_eigul = winner_eix_eigul(list_client,mate_server_socket)
                        is_winner_brike_breaker = winner_brike_breaker(list_client,mate_server_socket)
                        is_winner_color = winner_color(list_client,mate_server_socket)
                        is_winner_snake = winner_snake(list_client,mate_server_socket)
                        is_finish_game = finish_game(list_client, mate_server_socket)

                        if is_update == False and is_delete_update == False and is_server_connect == False and \
                                is_unregister == False and is_register == False and is_login == False and is_exit == False and is_check_info_about_eix_eigul_game == False and \
                                is_check_info_about_brike_breaker_game == False and is_check_info_about_color_game == False and is_check_info_about_snake_game == False \
                                and is_status_eix_eigul_game == False and is_status_brike_breaker_game == False and \
                                is_status_snake_game == False and is_status_color_game == False and is_winner_eix_eigul == False \
                                and is_winner_brike_breaker == False and is_winner_color == False and is_winner_snake == False and is_finish_game == False:

                            found = False
                            for i in range(len(data_clients)):
                                print("receive " + str(data_clients[i][2]) + " " + str(list_client[3]))
                                if data_clients[i][2] == list_client[3]:
                                    data_clients[i][0] = list_client[1]
                                    data_clients[i][1] = list_client[2]
                                    data_clients[i][3] = list_client[4]
                                    data_clients[i][4] = list_client[5]
                                    print("receive server connect " + str(data_clients[i][2]) + " " + str(list_client[3]))
                                    found = True

                            if found == False:
                                socket_id_and_user_name.append([list_client[3], current_socket])
                                data_clients.append([list_client[1], list_client[2], list_client[3], list_client[4], list_client[5]])
                                change_status_to_connected(mate_server_socket, list_client[3])

                            print(str(data_clients))
                            send_all_clients(open_client_sockets, data_clients)

                    except:
                        socket_has_been_closed(current_socket, rlist, data_clients, mate_server_socket, open_client_sockets,
                                               socket_id_and_user_name)
                        print("the client close the game!")
        except:
            socket_has_been_closed(current_socket, rlist, data_clients, mate_server_socket, open_client_sockets,
                                   socket_id_and_user_name)


if __name__ == '__main__':
    main()
