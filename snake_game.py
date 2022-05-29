import pygame
import time
import random
import tkinter as tk

pygame.init()

yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
banana_color = (227,207,87)
display_width = 600
display_height = 400

display_game = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game')

snake_timer = pygame.time.Clock()

block_size = 10
game_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def score_disply(score):
    value = score_font.render("Your Score: " + str(score), True, blue)
    display_game.blit(value, [0, 0])


def snake_image(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(display_game, black, [x[0], x[1], block_size, block_size])


def snake_print_message(msg, color):
    mesg = font_style.render(msg, True, color)
    display_game.blit(mesg, [display_width / 6, display_height / 3])


def snake_main_loop():
    game_over = False
    game_close = False

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    food_block_x = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
    food_block_y = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            display_game.fill(banana_color)
            snake_print_message("You Lost! Press C to CONTINUE Q to Quit", red)
            score_disply(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                        print("score: " + str(Length_of_snake - 1))
                    if event.key == pygame.K_c:
                        snake_main_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        display_game.fill(banana_color)
        pygame.draw.rect(display_game, green, [food_block_x, food_block_y, block_size, block_size])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        snake_image(block_size, snake_List)
        score_disply(Length_of_snake - 1)

        pygame.display.update()

        if x1 == food_block_x and y1 == food_block_y:
            food_block_x = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
            food_block_y = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0
            Length_of_snake += 1

        snake_timer.tick(game_speed)

    pygame.quit()
    quit()


snake_main_loop()