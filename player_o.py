# -*- coding: utf-8 -*-

import pygame
import time
import socket
import threading
import sys

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BEGIN_WIDTH_LINE_1 = [0, 200]
END_WIDTH_LINE_1 = [600, 200]
BEGIN_WIDTH_LINE_2 = [0, 400]
END_WIDTH_LINE_2 = [600, 400]
BEGIN_HEIGHT_LINE_1 = [200, 0]
END_HEIGHT_LINE_1 = [200, 600]
BEGIN_HEIGHT_LINE_2 = [400, 0]
END_HEIGHT_LINE_2 = [400, 600]
HEIGHT_CELL = 200
WIDTH_CELL = 200

my_turn = False
data= ''

def thread_function(my_socket, screen):
    global my_turn
    global last_click_row
    global last_click_column
    global data

    print("thread created" + str(my_socket))

    while True:
        if my_turn == True:
            try:
                data = my_socket.recv(1024).decode()
                if data == 'Exit':
                    exit = my_socket.recv(1024).decode()
                    my_socket.close()
                    wrote_winner(screen, "player X out of the game!")
                if data == 'It worked!' or data == 'Player o is the winner!' or data == 'There is no winner!':
                    draw_player_o(last_click_row, last_click_column, screen)
                    my_turn = False
                else:
                    print("Need to click again -> " + data)
            except:
                sys.exit()
        else:
            try:
                data1 = my_socket.recv(1024).decode()
                data = my_socket.recv(1024).decode()
                if data1 == 'Exit' and data == 'Exit':
                    my_socket.close()
                    wrote_winner(screen, "player X out of the game!")
                else:
                    row_x = int(data1[0])
                    column_x = int(data1[1])
                    print("row x: " + str(row_x) + " column x: " + str(column_x))
                    draw_player_x(row_x, column_x, screen)
                    my_turn = True
            except:
                sys.exit()

        try:
            if data == 'Player x is the winner!' or data == 'Player o is the winner!' or data == 'There is no winner!':
                my_socket.close()
                wrote_winner(screen, data)

        except:
            sys.exit()




def from_click_to_cell_in_array(pos_x, pos_y, screen, my_socket):
    global my_turn
    global last_click_row
    global last_click_column
    global data

    if data == 'Player x is the winner!' or data == 'Player o is the winner!' or data == 'There is no winner!' or data == 'Exit':
        return True

    last_click_row = pos_y // HEIGHT_CELL
    last_click_column = pos_x // WIDTH_CELL

    if my_turn == False:
        print('waiting ....')
        return False

    print('sending row o: ' + str(last_click_row) + ' column o: ' + str(last_click_column))

    try:
        my_socket.send((str(last_click_row) + str(last_click_column)).encode())
    except:
        return True


    return False





def draw_player_x(row, column, screen):

    print("yeah")
    print("row: "+str(row)+" column: "+str(column))
    pygame.draw.line(screen, 'blue', [column * 200 + 50, row * 200 + 50], [column * 200 + 150, row * 200 + 150], 4)
    pygame.display.flip()
    pygame.draw.line(screen, 'blue', [column * 200 + 150, row * 200 + 50], [column * 200 + 50, row * 200 + 150], 4)
    pygame.display.flip()


def draw_player_o(row, column, screen):
    pygame.draw.circle(screen, 'blue', [column * 200 + 100, row * 200 + 100], 50)
    pygame.display.flip()

def wrote_winner(screen, data):

        print(data)

        time.sleep(1)
        WHITE = (255, 255, 255)
        screen.fill(WHITE)
        pygame.display.flip()

        font = pygame.font.SysFont("comicsansms", 50)
        text = font.render(data, True, 'blue')
        screen.blit(text, (0, 200))
        pygame.display.flip()

        if data == 'Player o is the winner!':
            SOUND_FILE = "champions.mp3"
            pygame.mixer.init()
            pygame.mixer.music.load(SOUND_FILE)
            pygame.mixer.music.play()


def main():
    print("Arguments argv[0]: " + sys.argv[0])
    print("Arguments argv[1]: " + sys.argv[1])
    print("Arguments argv[2]: " + sys.argv[2])
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code
    print("client begin")
    my_socket = socket.socket()
    ip = str(sys.argv[2])
    port = int(sys.argv[1])
    my_socket.connect((ip, port))

    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    WHITE = (255, 255, 255)
    screen.fill(WHITE)
    pygame.display.flip()
    pygame.display.set_caption("player O")
    pygame.draw.line(screen, 'blue', BEGIN_WIDTH_LINE_1, END_WIDTH_LINE_1, 4)
    pygame.display.flip()
    pygame.draw.line(screen, 'blue', BEGIN_WIDTH_LINE_2, END_WIDTH_LINE_2, 4)
    pygame.display.flip()
    pygame.draw.line(screen, 'blue', BEGIN_HEIGHT_LINE_1, END_HEIGHT_LINE_1, 4)
    pygame.display.flip()
    pygame.draw.line(screen, 'blue', BEGIN_HEIGHT_LINE_2, END_HEIGHT_LINE_2, 4)
    pygame.display.flip()

    print("thread creating ->" + str(my_socket))
    x = threading.Thread(target=thread_function, args=(my_socket,screen))
    x.start()
    print("thread created")

    finish1 = False
    finish2 = False
    while not finish1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish1 = True
                if data != "Exit" and data != 'Player x is the winner!' and data != 'Player o is the winner!' and data != 'There is no winner!':
                    my_socket.send("Exit".encode())
                    # time.sleep(0.1)
                my_socket.close()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and finish2 == False:
                pos = pygame.mouse.get_pos()
                pos_x = pos[0]
                pos_y = pos[1]
                finish2 = from_click_to_cell_in_array(pos_x, pos_y, screen, my_socket)


if __name__ == '__main__':
    main()