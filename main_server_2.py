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

WINDOW_WIDTH = 1380
WINDOW_HEIGHT = 710
STARTING_BEAR_POINT_X = 1000
STARTING_BEAR_POINT_Y = 300
BOX_POINT_X = 200
BOX_POINT_Y = 500
CLICK_FOR_SENDING_MESSAGE_POINT_X = 690
CLICK_FOR_SENDING_MESSAGE_POINT_Y = 690
PORT_EIX_EIGUL = 8000
SQL_DATABASE_NAME = "db_member_2.db"


def send_client_board_game(current_socket):
    current_socket.send(str(WINDOW_WIDTH).encode())
    current_socket.send(str(WINDOW_HEIGHT).encode())
    place = str(STARTING_BEAR_POINT_X) + " " + str(STARTING_BEAR_POINT_Y)
    current_socket.send(place.encode())


def change_status_to_connected(mate_server_socket, name_player):
    print("change_status_to_connected name_player=" + str(name_player) + " statusPlayerInGame=connected")

    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE `member` SET `statusPlayerInGame` = ? WHERE `username` = ?",
                   (str("connected"), str(name_player)))
    conn.commit()
    conn.close()
    get_and_send_row_to_mate_server(mate_server_socket, name_player)


def init_database():
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT, statusEixEigulGame TEXT, portEixEigul INTEGER, numberOfWinsEixEigul INTEGER, statusPlayerInGame TEXT, socket TEXT)")
    conn.commit()
    conn.close()


def clear_database():
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `member`")
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
        print("Exit command=" + command + " user_name=" + list_client[1])
        current_socket.close()
        name_player = list_client[1]
        print("Exit command=" + command + " name_player=" + name_player)
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ?, `statusPlayerInGame` = ?, `socket` = ? WHERE `username` = ?",
            ("not playing", 0, "not connected", 0, name_player))
        conn.commit()
        get_and_send_row_to_mate_server(mate_server_socket, name_player)
        conn.close()
        return True

    return False


def check_info_about_the_game(list_client, current_socket):
    command = list_client[0]

    if command == 'controlBoard':
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(numberOfWinsEixEigul) FROM `member`")
        number_of_wins = cursor.fetchone()[0]

        string_of_the_names = ''

        if number_of_wins == 0:
            string_of_the_names = "No one won yet!"
        else:
            cursor.execute("SELECT username FROM `member` WHERE `numberOfWinsEixEigul` = ?", (number_of_wins,))
            list_tuple_of_the_names = cursor.fetchall()

            for i in range(len(list_tuple_of_the_names)):

                if i == 0:
                    string_of_the_names = list_tuple_of_the_names[i][0]
                else:
                    string_of_the_names = string_of_the_names + ", " + list_tuple_of_the_names[i][0]

        cursor.execute("SELECT COUNT(statusEixEigulGame) FROM `member` WHERE statusEixEigulGame = 'playing'")
        number_of_eix_eigul_players = cursor.fetchone()[0]

        message_control_board = pickle.dumps(
            ["control board", string_of_the_names, number_of_wins, number_of_eix_eigul_players])

        current_socket.send(message_control_board)
        conn.close()
        return True

    return False


def change_status_eix_eigul_game(list_client, current_socket, mate_server_socket):
    global PORT_EIX_EIGUL

    command = list_client[0]

    if command == 'StatusEixEigulGame':
        USERNAME = list_client[1]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT statusEixEigulGame FROM `member` WHERE `username` = ?", (str(USERNAME),))
        is_not_playing = cursor.fetchone()[0]

        if is_not_playing == 'not playing':

            cursor.execute("SELECT * FROM `member` WHERE `statusEixEigulGame` = ?", (str("waiting"),))
            if cursor.fetchone() is not None:
                cursor.execute("SELECT username FROM `member` WHERE `statusEixEigulGame` = ?", (str("waiting"),))
                username_of_other_player = cursor.fetchone()[0]
                cursor.execute("SELECT portEixEigul FROM `member` WHERE `username` = ?",
                               (str(username_of_other_player),))
                port_eix_eigul = cursor.fetchone()[0]
                cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ? WHERE `username` = ?",
                               (str("playing"), str(username_of_other_player)))
                cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ? WHERE `username` = ?",
                               (str("playing"), port_eix_eigul, str(USERNAME)))
                conn.commit()
                message_change_status_eix_eigul_game = ["player_o.py", port_eix_eigul]
            else:
                cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ?  WHERE `username` = ?",
                               (str("waiting"), PORT_EIX_EIGUL, str(USERNAME)))
                conn.commit()
                message_change_status_eix_eigul_game = ["player_x.py", PORT_EIX_EIGUL]
                PORT_EIX_EIGUL = PORT_EIX_EIGUL + 1

            message_change_status_eix_eigul_game = pickle.dumps(message_change_status_eix_eigul_game)
            current_socket.send(message_change_status_eix_eigul_game)
            get_and_send_row_to_mate_server(mate_server_socket, USERNAME)
            conn.close()
            return True
        else:
            message_change_status_eix_eigul_game = pickle.dumps(["you are waiting or playing"])
            current_socket.send(message_change_status_eix_eigul_game)
            conn.close()
            return True

    if command == 'WinnerEixEigul':
        USERNAME = list_client[1]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT numberOfWinsEixEigul FROM `member` WHERE `username` = ?", (str(USERNAME),))
        num_of_wins = cursor.fetchone()[0]
        num_of_wins = num_of_wins + 1
        cursor.execute("UPDATE `member` SET `numberOfWinsEixEigul` = ? WHERE `username` = ?",
                       (num_of_wins, str(USERNAME)))
        conn.commit()
        get_and_send_row_to_mate_server(mate_server_socket, USERNAME)
        conn.close()
        return True

    if command == 'FinishEixEigulGame':
        USERNAME = list_client[1]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `statusEixEigulGame` = ?, `portEixEigul` = ? WHERE `username` = ?",
                       (str("not playing"), 0, str(USERNAME)))
        get_and_send_row_to_mate_server(mate_server_socket, USERNAME)
        conn.commit()
        conn.close()
        return True

    return False


def Register(list_client, current_socket, mate_server_socket):
    command = list_client[0]

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
            cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME,))
            if cursor.fetchone() is not None:
                print("Username is already taken " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                message_register = pickle.dumps(["Username is already taken", "red"])
            else:
                print("Username insert " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                cursor.execute("INSERT INTO `member` (username, password, firstname, lastname, statusEixEigulGame, portEixEigul, numberOfWinsEixEigul, statusPlayerInGame, socket) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (str(USERNAME), str(PASSWORD), str(FIRSTNAME), str(LASTNAME), str("not playing"), 0, 0,
                     "not connected", 0))
                conn.commit()
                message_register = pickle.dumps(["Successfully Created!", "black"])

            cursor.close()
            conn.close()

        print("send to client Register reply")
        current_socket.send(message_register)
        print("send to mate server ServerUpdate")
        message_server_register = pickle.dumps(["ServerUpdate", USERNAME, PASSWORD, FIRSTNAME, LASTNAME, "not playing", 0 , 0, "not connected", 0])

        if mate_server_socket:
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
            cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME,))
            if cursor.fetchone() is None:
                print("Username is dosn't exist " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                message_unregister = pickle.dumps(["Username is dosn't exist", "red"])
            else:
                print("Username delete " + command + " USERNAME=" + USERNAME + " PASSWORD=" + PASSWORD)
                cursor.execute("DELETE FROM `member` WHERE `username` = ?", str(USERNAME))
                #cursor.execute("DELETE FROM `member` WHERE `username` = cfff")
                conn.commit()
                message_unregister = pickle.dumps(["Successfully deleted!", "black"])

            cursor.close()
            conn.close()

        print("send to client UnRegister reply")
        current_socket.send(message_unregister)

        if mate_server_socket:
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
        user_name = list_client[1]
        password = list_client[2]
        first_name = list_client[3]
        last_name = list_client[4]

        statusEixEigulGame = list_client[5]
        portEixEigul = list_client[6]
        numberOfWinsEixEigul = list_client[7]
        statusPlayerInGame = list_client[8]
        socket = list_client[9]

        print("receive ServerUpdate user_name="+user_name+" password="+password+" statusEixEigulGame="+statusEixEigulGame+" statusPlayerInGame="+statusPlayerInGame)


        # print("receive " + command + " user_name=" + user_name + " password=" + password + " statusPlayerInGame=" + statusPlayerInGame)
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (user_name,))
        if cursor.fetchone() is not None:
            print(
                "Username update " + command + " user_name=" + user_name + " password=" + password + " statusPlayerInGame=" + statusPlayerInGame + " statusEixEigulGame=" + statusEixEigulGame)

            cursor.execute(
                "UPDATE `member` SET `password` = ?, `firstname` = ?,`lastname` = ? ,`statusEixEigulGame` = ?,`numberOfWinsEixEigul` = ? ,`statusPlayerInGame` = ? WHERE `username` = ?",
                (str(password), str(first_name), str(last_name), str(statusEixEigulGame), int(numberOfWinsEixEigul),
                 str(statusPlayerInGame), str(user_name)))

            conn.commit()
        else:
            print(
                "Username insert " + command + " user_name=" + user_name + " password=" + password + " statusPlayerInGame=" + statusPlayerInGame + " statusEixEigulGame=" + statusEixEigulGame)
            cursor.execute(
                "INSERT INTO `member` (username, password, firstname, lastname, statusEixEigulGame, numberOfWinsEixEigul, statusPlayerInGame, socket) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                (str(user_name), str(password), str(first_name), str(last_name), str(statusEixEigulGame),
                 int(numberOfWinsEixEigul), str(statusPlayerInGame), 0))
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

        print("receive ServerDeleteUpdate user_name="+user_name+" password="+password)

        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (user_name,))
        if cursor.fetchone() is not None:
            print("Username update " + command + " user_name=" + user_name + " password=" + password)
            cursor.execute("DELETE FROM `member` WHERE `username` = ?",str(user_name))
            conn.commit()

        cursor.close()
        conn.close()
        return True
    else:
        # print("receive error for " + command)
        return False


def Login(list_client, current_socket):
    command = list_client[0]

    if command == 'Login':
        USERNAME = list_client[1]
        PASSWORD = list_client[2]
        conn = sqlite3.connect(SQL_DATABASE_NAME)
        cursor = conn.cursor()
        if USERNAME == "" or PASSWORD == "":
            message_login = pickle.dumps(["Please complete the required field!", "orange"])
        else:
            cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME, PASSWORD))
            if cursor.fetchone() is not None:
                cursor.execute("SELECT statusPlayerInGame FROM `member` WHERE `username` = ?", (str(USERNAME),))
                status_player_in_game = cursor.fetchone()[0]
                if status_player_in_game == 'not connected':
                    message_login = pickle.dumps(["You Successfully Login", "blue"])
                    cursor.execute("UPDATE `member` SET `statusPlayerInGame` = ?,`socket` = ? WHERE `username` = ?",
                                   (str("connecting"), str(current_socket), str(USERNAME)))
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
    user_name           = row[1]
    password            = row[2]
    first_name          = row[3]
    last_name           = row[4]
    statusEixEigulGame  = row[5]
    portEixEigul        = row[6]
    numberOfWinsEixEigul = row[7]
    statusPlayerInGame  = row[8]
    socket              = row[9]

    if mate_server_socket:
        data_update = pickle.dumps(["ServerUpdate", user_name, password, first_name, last_name, statusEixEigulGame, portEixEigul,numberOfWinsEixEigul, statusPlayerInGame, socket])
        print("send to mate:" + str(data_update))
        mate_server_socket.send(data_update)


def get_and_send_row_to_mate_server(mate_server_socket, user_name):
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (user_name,))
    list_user = cursor.fetchall()
    print("get_and_send_row_to_mate_server")

    for row in list_user:
        send_row_to_mate_server(mate_server_socket, row)


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
                print("data- " + str(data_clients))
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
            print("thread_mate_server_function except")
            return


def thread_mate_server(mate_server_socket):
    #    time.sleep(5)
    x = threading.Thread(target=thread_mate_server_function, args=(mate_server_socket,))
    x.start()


def thread_server_function(mate_server_socket):
    try:
        sync_db_to_mate_server(mate_server_socket)
    except:
        print("thread_server_function except")


def thread_server(mate_server_socket):
    x = threading.Thread(target=thread_server_function, args=(mate_server_socket,))
    x.start()


def socket_has_been_closed(current_socket, rlist, data_clients, mate_server_socket, open_client_sockets,
                           socket_id_and_user_name):
    list_client = ["Exit", "user_name", "password"]
    user_name = ""
    for current_socket in rlist:
        try:
            bytes_client = current_socket.recv(1024)
            print("select.select current_socket=" + current_socket, list_client)
        except:
            open_client_sockets.remove(current_socket)

            for i in range(len(socket_id_and_user_name)):
                print("socket_has_been_closed")
                if current_socket == socket_id_and_user_name[i][1]:
                    user_name = socket_id_and_user_name[i][0]
                    list_client[0] = "Exit"
                    list_client[1] = socket_id_and_user_name[i][0]
                    Exit(list_client, current_socket, mate_server_socket)
                    socket_id_and_user_name.remove(socket_id_and_user_name[i])

            for i in range(len(data_clients)):
                print("socket_has_been_closed")
                if user_name == data_clients[i][2]:
                    data_clients.remove(data_clients[i])


def main():
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code
    print(sys.argv[1])
    my_ip = sys.argv[1]
    my_port = int(sys.argv[2])

    mate_server_ip = sys.argv[3]
    mate_server_port = int(sys.argv[4])
    #SQL_DATABASE_NAME = sys.argv[5]

    open_client_sockets = []
    data_clients = []
    socket_id_and_user_name = []
    conn = sqlite3.connect(SQL_DATABASE_NAME)
    cursor = conn.cursor()
    print(
        "server begin my_ip=" + mate_server_ip + "/" + str(my_port) + ", mate_server_ip=" + mate_server_ip + "/" + str(
            mate_server_port) + "SQL_DATABASE_NAME=" + SQL_DATABASE_NAME)
    server_socket = socket.socket()
    mate_server_socket = 0;
    init_database()

    try:
        mate_server_socket = socket.socket()
        mate_server_socket.connect((mate_server_ip, mate_server_port))
        clear_database()
        message_server_connect = pickle.dumps(["ServerConnect"])
        thread_mate_server(mate_server_socket)
        if mate_server_socket:
            mate_server_socket.send(message_server_connect)
        print("connected to mate server")
        # sync_db_to_mate_server(mate_server_socket) only the connected send the data !!
    except socket.error:
        mate_server_socket = 0;
        print("no mate server")

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
                        is_register = Register(list_client, current_socket, mate_server_socket)
                        is_unregister = UnRegister(list_client, current_socket, mate_server_socket)
                        is_login = Login(list_client, current_socket)
                        is_control_board = check_info_about_the_game(list_client, current_socket)
                        is_status_eix_eigul_Game = change_status_eix_eigul_game(list_client, current_socket,
                                                                                mate_server_socket)

                        if is_update == False and is_delete_update == False and is_server_connect == False and is_register == False and is_unregister == False and is_login == False and is_control_board == False and is_status_eix_eigul_Game == False and is_exit == False:
                            found = False
                            for i in range(len(data_clients)):
                                print("receive " + str(data_clients[i][2]) + " " + str(list_client[3]))
                                if data_clients[i][2] == list_client[3]:
                                    data_clients[i][0] = list_client[1]
                                    data_clients[i][1] = list_client[2]
                                    data_clients[i][3] = list_client[4]
                                    print(
                                        "receive server connect " + str(data_clients[i][2]) + " " + str(list_client[3]))
                                    found = True

                            if found == False:
                                socket_id_and_user_name.append([list_client[3], current_socket]);
                                data_clients.append([list_client[1], list_client[2], list_client[3], list_client[4]])
                                change_status_to_connected(mate_server_socket, list_client[3])

                            print(str(data_clients))
                            send_all_clients(open_client_sockets, data_clients)

                    except:
                        open_client_sockets.remove(current_socket)
                        print("the client close the game!")
        except:
            socket_has_been_closed(current_socket, rlist, data_clients, mate_server_socket, open_client_sockets,
                                   socket_id_and_user_name)


if __name__ == '__main__':
    main()
