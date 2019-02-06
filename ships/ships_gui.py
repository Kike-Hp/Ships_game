#!/usr/bin/env python

#importy
#----------------------------------------------
import Tkinter as tk
from PIL import ImageTk, Image
import tkMessageBox
import yours_ships
from Tkconstants import DISABLED, NORMAL
import cPickle as pickle
import time
from PIL.ImageTk import PhotoImage
import socket
import select

#----------------------------------------------

class Gui():
    
    rows = 10
    columns = 10
    color = "blue"
    dim_background = 40
    filename_0 = "./ships/ship_png/ship1.png"
    filename_1 = "./ships/ship_png/ship2.png"
    filename_2 = "./ships/ship_png/ship3.png"
    filename_3 = "./ships/ship_png/ship4.png"
    filename_01 = "./ships/ship_png/ship01.png"
    filename_02 = "./ships/ship_png/ship02.png"
    filename_03 = "./ships/ship_png/ship03.png"
    filename_04 = "./ships/ship_png/ship04.png"
    
    ship = ''
    data = {}
    ship_coordinates = []
    i = 0
    enemy = 0
    photo_enemy = []
    photo_x = []
    
    def __init__(self, parent, nick, ip):
        self.nick = nick
        self.ip = ip
        self.parent = parent
        self.port = int(10000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.parent.after(1, self.read_from_server)
        self.canvas = tk.Canvas(self.parent, width = 820, height = 800)
        self.canvas.pack(padx = 10, pady = 10) 
        
    def draw_board(self):
        """Rysowanie planszy"""
        self.canvas.create_rectangle(0 , 0, 400, 60, fill = 'red', tags = "area")
        self.canvas.create_rectangle(420 , 0, 820, 60, fill = 'red', tags = "area")
        self.canvas.create_text(200,30, text = "Twoje", fill = 'yellow', font = ('', 22))
        self.canvas.create_text(610,30, text = "Przeciwnika", fill = 'yellow', font = ('', 22))
        for r in range(self.rows):
            for c in range(self.columns):
                x1 = (c * self.dim_background) 
                y1 = ((9-r) * self.dim_background) + 80
                x2 = x1 + self.dim_background
                y2 = y1 + self.dim_background
                self.canvas.create_rectangle(x1 , y1, x2, y2, fill = self.color, tags = "area")
        for r in range(self.rows):
            for c in range(self.columns):
                x1 = (c * self.dim_background) + 420
                y1 = ((9-r) * self.dim_background) + 80
                x2 = x1 + self.dim_background
                y2 = y1 + self.dim_background
                self.canvas.create_rectangle(x1 , y1, x2, y2, fill = self.color, tags = "area")
        self.add_image()
#         self.canvas.create_line(0 , 500, 820, 500, fill = 'black')
                
        
    def add_image(self):
        """ladowanie obrazkow"""
        photo_0 = ImageTk.PhotoImage(file = self.filename_0)
        photo_1 = ImageTk.PhotoImage(file = self.filename_1)
        photo_2 = ImageTk.PhotoImage(file = self.filename_2)
        photo_3 = ImageTk.PhotoImage(file = self.filename_3)
        self.parent.photo_0 = photo_0
        self.parent.photo_1 = photo_1
        self.parent.photo_2 = photo_2
        self.parent.photo_3 = photo_3
        self.canvas.create_image(100, 550, image = photo_0, anchor="c")
        self.canvas.create_image(100, 620, image = photo_1, anchor="c")
        self.canvas.create_image(100, 690, image = photo_2, anchor="c")
        self.canvas.create_image(100, 760, image = photo_3, anchor="c")
        self.button()
        
        
    def button(self):
        "dodawanie przyciskow"
        self.button_exit = tk.Button(self.canvas, text = "Zamknij", command = self.close)
        self.button_exit.configure(width = 10)
        self.button_exit_window = self.canvas.create_window(743, 765, window = self.button_exit)
        
        self.button_ship_1 = tk.Button(self.canvas, text = "Wybierz", command = lambda: self.set_ship(self.filename_0))
        self.button_ship_1.configure(width = 10)
        self.button_ship_1_window = self.canvas.create_window(300, 550, window = self.button_ship_1)
        
        self.button_ship_2 = tk.Button(self.canvas, text = "Wybierz", command = lambda: self.set_ship(self.filename_1))
        self.button_ship_2.configure(width = 10)
        self.button_ship_2_window = self.canvas.create_window(300, 620, window = self.button_ship_2)
        
        self.button_ship_3 = tk.Button(self.canvas, text = "Wybierz", command = lambda: self.set_ship(self.filename_2))
        self.button_ship_3.configure(width = 10)
        self.button_ship_3_window = self.canvas.create_window(300, 690, window = self.button_ship_3)
        
        self.button_ship_4 = tk.Button(self.canvas, text = "Wybierz", command = lambda: self.set_ship(self.filename_3))
        self.button_ship_4.configure(width = 10)
        self.button_ship_4_window = self.canvas.create_window(300, 760, window = self.button_ship_4)
        
        self.button_save = tk.Button(self.canvas, text = "Save", command = self.save)
        self.button_save.configure(width = 10)
        self.button_save_window = self.canvas.create_window(600, 765, window = self.button_save)
        #----------------------------------------------------------
#         self.canvas.create_line(800 , 0, 800, 800, fill = 'black')
#         self.canvas.create_line(0 , 780, 820, 780, fill = 'black')
        
    
    def square_clicked(self, event, z):
        '''wspolrzedne punktow'''
        x =  event.x/self.dim_background
        y =  event.y / self.dim_background - 2
        self.selected_fields(x, y, z)
        
        
    def set_ship(self, filename):
        '''akcja po kliknieciu'''
        self.ship = filename
        self.canvas.bind ("<Button-1>", lambda event: self.square_clicked(event, filename[-5]))
        
    def selected_fields(self, x, y, z):
        '''dodawanie obrazkow na plansze'''
        if x < 10 and y < 10 and y > -1 and int(z) in range(1, 5):
            self.data[int(z) - 1] = x, y
            x1 = (x * self.dim_background) 
            y1 = (y * self.dim_background) + 80
            x2 = x1 + self.dim_background
            y2 = y1 + self.dim_background
            photo = ImageTk.PhotoImage(file = self.ship)
            if z == '1':
                if x in range(2, 8):
                    self.parent.photo_10 = photo
                    self.canvas.create_image(x2 - 20, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
            if z == '2':
                if x in range(1, 9):
                    self.parent.photo_11 = photo
                    self.canvas.create_image(x2 - 20, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
            if z == '3':
                if x in range(1, 10):
                    self.parent.photo_12 = photo
                    self.canvas.create_image(x2 - 40, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
            if z == '4':
                if x in range(0, 10):
                    self.parent.photo_13 = photo
                    self.canvas.create_image(x2 - 20, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
        else:
            tkMessageBox.showerror("Error", "Out of the area")
            
    def save(self):
        '''zapisywanie i wysylanie ustawienia na server'''
        if self.data != None and self.data != '':
            if len(self.data.keys()) == 4:
                self.your_ships_data = yours_ships.yoursShips(self.data).check()
                if self.your_ships_data.error == 0:
                    self.button_ship_1.config(state = DISABLED)
                    self.button_ship_2.config(state = DISABLED)
                    self.button_ship_3.config(state = DISABLED)
                    self.button_ship_4.config(state = DISABLED)
                    self.button_save.config(state = DISABLED)
                    self.canvas.bind ("<Button-1>", '')
                    self.connect()
                    
                else:
                    tkMessageBox.showerror("Error", "DUPA")
            else:
                tkMessageBox.showinfo("Add ships", "Add all ships to the board ")
    
    def connect(self):
        data_string = pickle.dumps((self.nick, self.your_ships_data.yours_ships), -1)
        self.sock.send(data_string)
    
    def send(self, send_data):
        self.sock.send(send_data)
        
    def read_from_server(self):
        read_sockets, write_socket, error_socket = select.select([self.sock],[],[], 0.1)
        for socks in read_sockets:
            if socks == self.sock:
                message = socks.recv(2048)
                if message == "CLOSE":
                    self.sock.close()
                    self.win()
                elif message == 'start':
                    tkMessageBox.showinfo("","Your turn")
                    self.your_turn()
                elif message == 'WIN':
                    self.win()
                elif message == 'LOSER':
                    self.loser()
                else:
                    message = pickle.loads(message)
                    if message[0] in (1, 2, 3, 4):
                        self.immersion(message)
                    else:
                        if message[0] == 'headshot':
                            tkMessageBox.showinfo("traienie","You've been hit, your move")
                            self.your_turn()
                        else:
                            self.enemy_turn(message)
        self.parent.after(1, self.read_from_server)
        
    def your_turn(self):
        self.canvas.bind ("<Button-1>", self.shot)
    
    def immersion(self, message):
        x = ((message[1][1] + 10) * self.dim_background) + self.dim_background
        y = (message[1][0] * self.dim_background) + 100
        if message[0] == 1:
            file_01 = Image.open(self.filename_01)
            image_01 = ImageTk.PhotoImage(file_01)
            self.parent.photo_01 = image_01
            self.canvas.create_image(x, y, image = image_01)
        elif message[0] == 2:
            file_02 = Image.open(self.filename_02)
            image_02 = ImageTk.PhotoImage(file_02)
            self.parent.photo_02 = image_02
            self.canvas.create_image(x, y, image = image_02)
        elif message[0] == 3:
            file_03 = Image.open(self.filename_03)
            image_03 = ImageTk.PhotoImage(file_03)
            self.parent.photo_03 = image_03
            self.canvas.create_image(x + 20, y, image = image_03)
        elif message[0] == 4:
            file_04 = Image.open(self.filename_04)
            image_04 = ImageTk.PhotoImage(file_04)
            self.parent.photo_04 = image_04
            self.canvas.create_image(x, y, image = image_04)
    
    
    def shot(self, event):
        '''wspolrzedne punktow na planszy przeciwnika'''
        x =  (event.x - 20)/self.dim_background
        y =  event.y / self.dim_background - 2
        if x > 9 and y < 10 and y > -1:
            x1 = (x * self.dim_background) + self.dim_background
            y1 = (y * self.dim_background) + 80
            image = Image.open("./ships/ship_png/x.png")
            self.photo_x.append(ImageTk.PhotoImage(image))
            self.parent.photo= self.photo_x[self.i]
            self.canvas.create_image( x1, y1 + 20,  image = self.photo_x[self.i] )
            send_data = pickle.dumps((self.nick, [x - 10, y]), -1)
            self.send(send_data)
            self.i += self.i
            self.canvas.bind ("<Button-1>", '')
        else:
            tkMessageBox.showerror("Error", "Out of the area")
    
    def enemy_turn(self, message):
        '''zaznaczenie miejsca trafienia przez przeciwnika'''
        x = (message[1][0] * self.dim_background) + self.dim_background 
        y = (message[1][1] * self.dim_background) + 80
        image = Image.open("./ships/ship_png/boom.png")
        self.photo_enemy.append(ImageTk.PhotoImage(image))
        self.parent.photo= self.photo_enemy[self.enemy]
        self.canvas.create_image( x - 20, y + 20,  image = self.photo_enemy[self.enemy] )
        self.enemy += self.enemy
    
    def headshot(self):
        tkMessageBox.showinfo("traienie","Your turn")
    
    def close(self):
        try:
            send_data = pickle.dumps(('CLOSE'), -1)
            self.send(send_data)
        except:
            pass
        self.sock.close()
        self.parent.destroy()

    def win(self):
        tkMessageBox.showinfo("","Wygrales")
    def loser(self):
        tkMessageBox.showinfo("","Przegrany")
        
def display(nick, ip):
    root = tk.Tk()
    root.title("Battle ship")
    root.resizable(False, False)
    gui = Gui(root, nick, ip)
    gui.draw_board()
    root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()

# filename = "./ship_png/boom.png"
# imagenes = Image.open(filename)
# imagenes = imagenes.resize((40, 40), Image.ANTIALIAS)
# imagenes.save("boom.png", "png")    
#      


