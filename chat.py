
from tkinter import Tk, Frame, Label, END, Entry, Text, Button

class GUI:
    def __init__(self, root, starting_point_x, starting_point_y, name_player, treat_messages):

        self.root = root
        self.last_message = ''
        self.starting_point_x = starting_point_x
        self.starting_point_y = starting_point_y
        self.name_player = name_player
        self.treat_messages = treat_messages

        self.initialize_gui()


    def initialize_gui(self):  # GUI initializer
        self.root.title("Chat")
        self.root.resizable(0, 0)
        self.display_chat_entry_box()

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter message:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=3, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side='top')

    def on_enter_key_pressed(self, event):
        self.send_chat()
        self.clear_text()
        self.on_close_window()

    def clear_text(self):
        self.enter_text_widget.delete(1.0, 'end')
        self.treat_messages.send_message(self.starting_point_x, self.starting_point_y, self.name_player,  self.last_message)


    def send_chat(self):
        data = self.enter_text_widget.get(1.0, 'end').strip()
        self.last_message = data
        # print(data)

    def on_close_window(self):
        print("destroy!")
        self.root.destroy()
        # exit(0)


def main():
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code

if __name__ == '__main__':
    main()
