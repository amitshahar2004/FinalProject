
from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import pickle
import time
import tkinter as tk
import hashlib

server_is_selected = False
server_is_connected = False

# width = 640
# height = 480
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# x = (screen_width/2) - (width/2)
# y = (screen_height/2) - (height/2)
# root.geometry("%dx%d+%d+%d" % (width, height, x, y))
# root.resizable(0, 0)

class TreatUser:

    def __init__(self, my_socket):

        self.my_socket = my_socket

        self.root = Tk()
        self.root.title("Connect user")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print(screen_width)
        print(screen_height)
        self.root.geometry("%dx%d" % (screen_width, screen_height))
        self.root.resizable(0, 0)

        self.USERNAME = StringVar()
        self.PASSWORD = StringVar()
        self.FIRSTNAME = StringVar()
        self.LASTNAME = StringVar()

        self.SERVER_ID   = 0
        self.SERVER_NAME_1 = StringVar()
        self.SERVER_NAME_2 = StringVar()
        self.SERVER_IP_1   = StringVar()
        self.SERVER_IP_2   = StringVar()
        self.SERVER_PORT_1 = 0
        self.SERVER_PORT_2 = 0
        self.read_file_data()
        self.LoginForm()

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.Exit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        self.root.mainloop()


    # def Database(self):
    #     self.conn = sqlite3.connect("db_member.db")
    #     self.cursor = self.conn.cursor()
    #     self.cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")


    def Exit(self):
        result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
        if result == 'yes':
            self.root.destroy()
            self.my_socket.close()
            exit()

    def LoginForm(self):
        global LoginFrame, lbl_result1 , liste, password , btn_login , username, lbl_register, lbl_unregister
        LoginFrame = Frame(self.root)
        LoginFrame.pack(side=TOP, pady=80)
        lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
        lbl_username.grid(row=3)

        lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
        lbl_password.grid(row=4)
        lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
        lbl_result1.grid(row=6, columnspan=2)

        username = Entry(LoginFrame, font=('arial', 20), textvariable=self.USERNAME, width=15)
        username.grid(row=3, column=1)
        username['state'] = 'disabled'

        password = Entry(LoginFrame, font=('arial', 20), textvariable=self.PASSWORD, width=15, show="*")
        password.grid(row=4, column=1)
        password['state'] = 'disabled'

        btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=self.Login)
        btn_login.grid(row=5, columnspan=2, pady=20)
        btn_login['state'] = 'disabled'

        lbl_server = Label(LoginFrame, text="Choose Server to Connect", fg="Black", font=('arial', 12))
        lbl_server.grid(row=2, sticky=W)
        #scrollbar = Scrollbar(LoginFrame, orient = tk.HORIZONTAL, width=4, command=self.server2)
        liste = Listbox(LoginFrame, font=('arial', 12), width=20,height=3)
        liste.grid(row=2, column=1, sticky='ns')

        server_1_str = str(self.SERVER_NAME_1) + " " + str(self.SERVER_IP_1) + ":" + str(self.SERVER_PORT_1)
        server_2_str = str(self.SERVER_NAME_2) + " " + str(self.SERVER_IP_2) + ":" + str(self.SERVER_PORT_2)

        liste.insert(0, server_1_str)
        liste.insert(1, server_2_str)
#        liste.bind("<1>", self.validate_server)
        liste.bind("<Double-1>", self.validate_server)

        lbl_register = Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
        lbl_register.grid(row=0, sticky=W)
        lbl_register.bind('<Button-1>', self.ToggleToRegister)
        lbl_register['state'] = 'disabled'

        lbl_unregister = Label(LoginFrame, text="UnRegister", fg="Blue", font=('arial', 12))
        lbl_unregister.grid(row=1, sticky=W)
        lbl_unregister.bind('<Button-1>', self.ToggleToUnRegister)
        lbl_unregister['state'] = 'disabled'

    def enable_login_frame(self):
        username['state'] = 'normal'
        password['state'] = 'normal'
        btn_login['state'] = 'normal'
        lbl_register['state'] = 'normal'
        lbl_unregister['state'] = 'normal'
        liste['state'] = 'disable'

    def disable_register_frame(self):
        username['state']  = 'disabled'
        password['state']  = 'disabled'
        firstname['state'] = 'disabled'
        lastname['state']  = 'disabled'
        btn_register['state'] = 'disabled'


    def disable_unregister_frame(self):
        unreg_username['state']  = 'disabled'
        unreg_password['state']  = 'disabled'
        btn_unregister['state'] = 'disabled'

    def RegisterForm(self):
        global RegisterFrame, lbl_result2,username,password,firstname,lastname,btn_register

        RegisterFrame = Frame(self.root)
        RegisterFrame.pack(side=TOP, pady=40)
        lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 18), bd=18)
        lbl_username.grid(row=1)
        lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
        lbl_password.grid(row=2)
        lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('arial', 18), bd=18)
        lbl_firstname.grid(row=3)
        lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('arial', 18), bd=18)
        lbl_lastname.grid(row=4)
        lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
        lbl_result2.grid(row=5, columnspan=2)
        username = Entry(RegisterFrame, font=('arial', 20), textvariable=self.USERNAME, width=15)
        username.grid(row=1, column=1)
        password = Entry(RegisterFrame, font=('arial', 20), textvariable=self.PASSWORD, width=15, show="*")
        password.grid(row=2, column=1)
        firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=self.FIRSTNAME, width=15)
        firstname.grid(row=3, column=1)
        lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=self.LASTNAME, width=15)
        lastname.grid(row=4, column=1)
        btn_register = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=self.Register)
        btn_register.grid(row=6, columnspan=2, pady=20)
        lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12))
        lbl_login.grid(row=0, sticky=W)
        lbl_login.bind('<Button-1>', self.RegisterToggleToLogin)

    def UnRegisterForm(self):
        global UnRegisterFrame, unreg_lbl_result,unreg_username,unreg_password,btn_unregister

        UnRegisterFrame = Frame(self.root)
        UnRegisterFrame.pack(side=TOP, pady=40)
        lbl_username = Label(UnRegisterFrame, text="Username:", font=('arial', 18), bd=18)
        lbl_username.grid(row=1)
        lbl_password = Label(UnRegisterFrame, text="Password:", font=('arial', 18), bd=18)
        lbl_password.grid(row=2)
        unreg_lbl_result = Label(UnRegisterFrame, text="", font=('arial', 18))
        unreg_lbl_result.grid(row=5, columnspan=2)
        unreg_username = Entry(UnRegisterFrame, font=('arial', 20), textvariable=self.USERNAME, width=15)
        unreg_username.grid(row=1, column=1)
        unreg_password = Entry(UnRegisterFrame, font=('arial', 20), textvariable=self.PASSWORD, width=15, show="*")
        unreg_password.grid(row=2, column=1)
        btn_unregister = Button(UnRegisterFrame, text="Un-Register", font=('arial', 18), width=35, command=self.UnRegister)
        btn_unregister.grid(row=6, columnspan=2, pady=20)
        lbl_login = Label(UnRegisterFrame, text="Login", fg="Blue", font=('arial', 12))
        lbl_login.grid(row=0, sticky=W)
        lbl_login.bind('<Button-1>', self.UnRegisterToggleToLogin)

    def RegisterToggleToLogin(self, event=None):
        RegisterFrame.destroy()

        self.LoginForm()
        if server_is_connected == True:
            self.enable_login_frame()

    def UnRegisterToggleToLogin(self, event=None):
        UnRegisterFrame.destroy()

        self.LoginForm()
        if server_is_connected == True:
            self.enable_login_frame()


    def ToggleToRegister(self, event=None):
        LoginFrame.destroy()
        self.RegisterForm()

    def ToggleToUnRegister(self, event=None):
        LoginFrame.destroy()
        self.UnRegisterForm()

    def validate_server(self, event):
        self.server_selected(lbl_result1)

    def Register(self):
        hexdigest_password_result = ""

        if not self.USERNAME.get() or not self.PASSWORD.get() or not self.FIRSTNAME.get() or not self.LASTNAME.get():
            text = "one of the field is empty"
            lbl_result2.config(text=text)
            print("user and password can't be empty")
            return

        self.server_selected(lbl_result2)
        if server_is_connected == False:
            print("no server is not connected")
            return

        encoded = self.PASSWORD.get().encode("utf8")
        result = hashlib.md5(encoded)
        hexdigest_password_result = result.hexdigest()

        print ("hexdigest_password_result" + hexdigest_password_result + " self.PASSWORD.get()="+self.PASSWORD.get())
        #data_register = pickle.dumps(["Register", self.USERNAME.get(), self.PASSWORD.get(), self.FIRSTNAME.get(), self.LASTNAME.get()])
        data_register = pickle.dumps(["Register", self.USERNAME.get(), hexdigest_password_result, self.FIRSTNAME.get(), self.LASTNAME.get()])

        self.my_socket.send(data_register)

        bytes_message_register = self.my_socket.recv(1024)
        message_register = pickle.loads(bytes_message_register)

        text = message_register[0]
        color = message_register[1]
        lbl_result2.config(text=text, fg=color)

        if text == "Successfully Created!":
            self.USERNAME.set("")
            self.PASSWORD.set("")
            self.FIRSTNAME.set("")
            self.LASTNAME.set("")
            self.disable_register_frame()

    def UnRegister(self):
        hexdigest_password_result = ""

        if not self.USERNAME.get() or not self.PASSWORD.get() :
            text = "one of the field is empty"
            lbl_result2.config(text=text)
            print("user and password can't be empty")
            return

        self.server_selected(unreg_lbl_result)
        if server_is_connected == False:
            print("no server is not connected")
            return

        encoded = self.PASSWORD.get().encode("utf8")
        result = hashlib.md5(encoded)
        hexdigest_password_result = result.hexdigest()

        print ("hexdigest_password_result" + hexdigest_password_result + " self.PASSWORD.get()="+self.PASSWORD.get())
        data_register = pickle.dumps(["UnRegister", self.USERNAME.get(), hexdigest_password_result])

        self.my_socket.send(data_register)

        bytes_message_register = self.my_socket.recv(1024)
        message_register = pickle.loads(bytes_message_register)

        text = message_register[0]
        color = message_register[1]
        unreg_lbl_result.config(text=text, fg=color)

        if text == "Successfully Deleted!":
            self.USERNAME.set("")
            self.PASSWORD.set("")
            self.disable_unregister_frame()

    def server_selected(self, lbl_result):
        global server_is_selected
        global server_is_connected

        if server_is_connected == True:
            return

        try:
            for select_server in liste.curselection():
                print("select_server=" + str(select_server))
                if select_server == 0:
                    server_is_selected = True;
                    self.server1()
                else:
                    server_is_selected = True;
                    self.server2()
        except:
            text = "unable to connect server (choose different server)"
            print("unable to connect server (choose different server)")
            self.SERVER_ID = 0
            lbl_result.config(text=text)
            return

        if server_is_selected == False:
            text = "no server is selected"
            print("no server is selected")
            lbl_result.config(text=text)
            return

        server_is_connected = True
        self.enable_login_frame()
        text = "connection to server succeed"
        print("connection to server succeed")
        lbl_result.config(text=text)

    def Login(self):
        global server_is_selected
        global server_is_connected
        hexdigest_password_result = ""

        if not self.USERNAME.get() or not self.PASSWORD.get():
            text = "user and password can't be empty"
            lbl_result1.config(text=text)
            print("user and password can't be empty")
            return

        self.server_selected(lbl_result1)
        if server_is_connected == False:
            print("no server is not connected")
            return

        liste['state'] = 'disabled'

        encoded = self.PASSWORD.get().encode("utf8")
        result = hashlib.md5(encoded)
        hexdigest_password_result = result.hexdigest()

        data_login = pickle.dumps(["Login", self.USERNAME.get(), hexdigest_password_result])
        self.my_socket.send(data_login)

        bytes_message_login = self.my_socket.recv(1024)
        message_login = pickle.loads(bytes_message_login)

        text = message_login[0]
        color = message_login[1]
        lbl_result1.config(text=text, fg=color)

        if text == "You Successfully Login":
            self.root.destroy()

    def server1(self):
        if self.SERVER_ID == 1:
            print("server-1 didn't changed")
            return

        if self.SERVER_ID == 2:
            print("server-1 chosen first close close server-2")
            self.my_socket.close()

        self.SERVER_ID = 1

        print("server-1 chosen" + " SERVER_IP=" + self.SERVER_IP_1 + " SERVER_PORT=" + str(self.SERVER_PORT_1))
        self.my_socket.connect((self.SERVER_IP_1, self.SERVER_PORT_1))

    def server2(self):
        if self.SERVER_ID == 2:
            print("server-2 didn't changed")
            return

        if self.SERVER_ID == 1:
            print("server-2 chosen first close close server-1")
            self.my_socket.close()

        self.SERVER_ID = 2

        print("server-2 chosen" + " SERVER_IP=" + self.SERVER_IP_2 + " SERVER_PORT=" + str(self.SERVER_PORT_2))
        self.my_socket.connect((self.SERVER_IP_2, self.SERVER_PORT_2))

    def read_file_data(self):
        file = open("server_cfg.txt", "r")

        server_data = file.readline()
        self.SERVER_NAME_1 = server_data.strip()

        server_data = file.readline()
        self.SERVER_IP_1 = server_data.strip()

        server_data = file.readline()
        server_data = server_data.strip()
        self.SERVER_PORT_1 = int(server_data)

        server_data = file.readline()
        self.SERVER_NAME_2 = server_data.strip()

        server_data = file.readline()
        self.SERVER_IP_2 = server_data.strip()

        server_data = file.readline()
        server_data = server_data.strip()
        self.SERVER_PORT_2 = int(server_data)

        file.close()

    def get_username(self):
        return self.USERNAME.get()

    def get_server_ip(self):
        return self.SERVER_IP.get()

    def get_server_port(self):
        return self.SERVER_PORT.get()

    # def Register(self):
    #     self.Database()
    #     if self.USERNAME.get == "" or self.PASSWORD.get() == "" or self.FIRSTNAME.get() == "" or self.LASTNAME.get == "":
    #         lbl_result2.config(text="Please complete the required field!", fg="orange")
    #     else:
    #         self.cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (self.USERNAME.get(),))
    #         if self.cursor.fetchone() is not None:
    #             lbl_result2.config(text="Username is already taken", fg="red")
    #         else:
    #             self.cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)",(str(self.USERNAME.get()), str(self.PASSWORD.get()), str(self.FIRSTNAME.get()), str(self.LASTNAME.get())))
    #             self.conn.commit()
    #             self.USERNAME.set("")
    #             self.PASSWORD.set("")
    #             self.FIRSTNAME.set("")
    #             self.LASTNAME.set("")
    #             lbl_result2.config(text="Successfully Created!", fg="black")
    #         self.cursor.close()
    #         self.conn.close()


    # def Login(self):
    #     self.Database()
    #     if self.USERNAME.get == "" or self.PASSWORD.get() == "":
    #         lbl_result1.config(text="Please complete the required field!", fg="orange")
    #     else:
    #         self.cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?",(self.USERNAME.get(), self.PASSWORD.get()))
    #         if self.cursor.fetchone() is not None:
    #             lbl_result1.config(text="You Successfully Login", fg="blue")
    #         else:
    #             lbl_result1.config(text="Invalid Username or password", fg="red")


def main():
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code

    root = Tk()
    root.title("Connect user")

    read_file_data()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print(screen_width)
    print(screen_height)
    root.geometry("%dx%d" % (screen_width, screen_height))
    root.resizable(0, 0)

    LoginForm()

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=Exit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    root.mainloop()


if __name__ == '__main__':
    main()

