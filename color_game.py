# import the modules
import tkinter
import random

CLOUR_GAME_TIME  = 20
# colour in the game.
game_colours = ['Red','Blue','Green','Pink','Black',
           'Yellow','Orange','White','Purple','Brown']
player_current_score = 0

# game default time 20 second
remaining_time = CLOUR_GAME_TIME

# function that will start the game.
def colour_start_play(event):

    if remaining_time == CLOUR_GAME_TIME:

        # start counting.
        start_count_down()

    # next colour to choose.
    next_colour_to_choose()

# next colour to choose
def next_colour_to_choose():

    # use the globally declared 'player_current_score'
    # and 'play' variables above.
    global player_current_score
    global remaining_time

    # if a game is currently running
    if remaining_time > 0:

        e.focus_set()


        # choose right
        if e.get().lower() == game_colours[1].lower():

            player_current_score += 1

        # clear the written text.
        e.delete(0, tkinter.END)

        random.shuffle(game_colours)

        # random choosing colour value
        label.config(fg = str(game_colours[1]), text = str(game_colours[0]))

        # update the player_current_score.
        scoreLabel.config(text = "Score: " + str(player_current_score))


# start_count_down timer function
def start_count_down():

    global remaining_time

    # if a game is in play
    if remaining_time > 0:

        # decrement the timer.
        remaining_time -= 1
        if remaining_time == 0:
            print("score: " + str(player_current_score))

        # update the time left label
        time_message.config(text = "Time left: "
                               + str(remaining_time))

        # run the function again after 1 second.
        time_message.after(1000, start_count_down)


# Driver Code

# create a GUI window
root = tkinter.Tk()

# set the title
root.title("COLORGAME")

# set the size
root.geometry("475x300")

# add an instructions label
instructions = tkinter.Label(root, text = "Type in the colour that written", font = ('Helvetica', 12))
instructions.pack()

# add a score label
scoreLabel = tkinter.Label(root, text = "Press enter to start",
                                      font = ('Helvetica', 12))
scoreLabel.pack()

# add a time left
time_message = tkinter.Label(root, text = "Remaining Time: " +
              str(remaining_time), font = ('Helvetica', 12))

time_message.pack()


label = tkinter.Label(root, font = ('Helvetica', 60))
label.pack()

e = tkinter.Entry(root)

root.bind('<Return>', colour_start_play)
e.pack()

e.focus_set()

# start the GAME
root.mainloop()