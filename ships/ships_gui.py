#!/usr/bin/env python

#importy
#----------------------------------------------
import Tkinter as tk
from PIL import ImageTk, Image
import tkMessageBox
#----------------------------------------------

class Gui():
    
    rows = 10
    columns = 10
    color = "blue"
    dim_background = 40
    filename_0 = "./ship_png/ship0.png"
    filename_1 = "./ship_png/ship1.png"
    filename_2 = "./ship_png/ship2.png"
    filename_3 = "./ship_png/ship3.png"
    ship = ''
    
    def __init__(self, parent):
        self.parent = parent
        self.canvas = tk.Canvas(self.parent, width = 820, height = 800)
        self.canvas.pack(padx = 10, pady = 10) #obszar roboczy - padding
        self.draw_board()
        
    def draw_board(self):
        """Rysowanie planszy"""
        color = self.color
        self.canvas.create_rectangle(0 , 0, 400, 60, fill = 'red', tags = "area")
        self.canvas.create_rectangle(420 , 0, 820, 60, fill = 'red', tags = "area")
        self.canvas.create_text(200,30, text = "Twoje", fill = 'yellow', font = ('', 22))
        self.canvas.create_text(610,30, text = "Przeciwnika", fill = 'yellow', font = ('', 22))
        self.canvas.create_line(400 , 80, 400, 480, fill = 'black')
        self.canvas.create_line(420 , 80, 420, 480, fill = 'black')
        for r in range(self.rows):
            for c in range(self.columns):
                x1 = (c * self.dim_background) 
                y1 = ((9-r) * self.dim_background) + 80
                x2 = x1 + self.dim_background
                y2 = y1 + self.dim_background
                self.canvas.create_rectangle(x1 , y1, x2, y2, fill = color, tags = "area")
        for r in range(self.rows):
            for c in range(self.columns):
                x1 = (c * self.dim_background) + 420
                y1 = ((9-r) * self.dim_background) + 80
                x2 = x1 + self.dim_background
                y2 = y1 + self.dim_background
                self.canvas.create_rectangle(x1 , y1, x2, y2, fill = color, tags = "area")
        self.add_image()
        self.canvas.create_line(0 , 500, 820, 500, fill = 'black')
                
        
    def add_image(self):
        """ladowanie obrazkow"""
#         filename = "./ships/ship_png/ship.png"
#         image_2 = Image.open(filename_2)
#         image_2 = image_2.resize((80, 40), Image.ANTIALIAS)
#         image_2.save("ship3.png", "png")
        photo_0 = ImageTk.PhotoImage(file = self.filename_0)
        photo_1 = ImageTk.PhotoImage(file = self.filename_1)
        photo_2 = ImageTk.PhotoImage(file = self.filename_2)
        photo_3 = ImageTk.PhotoImage(file = self.filename_3)
        self.parent.photo_0 = photo_0
        self.parent.photo_1 = photo_1
        self.parent.photo_2 = photo_2
        self.parent.photo_3 = photo_3
        print self.parent.photo_3
        print self.parent.photo_2
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
        #----------------------------------------------------------
        self.canvas.create_line(800 , 0, 800, 800, fill = 'black')
        self.canvas.create_line(0 , 780, 820, 780, fill = 'black')
        
    
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
        print z
        if x < 10 and y < 10 and y > -1 and int(z) in range(0, 4):
            x1 = (x * self.dim_background) 
            y1 = (y * self.dim_background) + 80
            x2 = x1 + self.dim_background
            y2 = y1 + self.dim_background
#             self.canvas.create_rectangle(x1 , y1, x2, y2, fill = 'green', tags = "area")
            photo = ImageTk.PhotoImage(file = self.ship)
            if z == '0':
                if x in range(2, 8):
                    self.parent.photo_10 = photo
                    self.canvas.create_image(x2 - 20, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
            if z == '1':
                if x in range(1, 9):
                    self.parent.photo_11 = photo
                    self.canvas.create_image(x2 - 20, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
            if z == '2':
                if x in range(1, 10):
                    self.parent.photo_12 = photo
                    self.canvas.create_image(x2 - 40, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
            if z == '3':
                if x in range(0, 10):
                    self.parent.photo_13 = photo
                    self.canvas.create_image(x2 - 20, y2 - 20, image = photo, anchor="c")
                else:
                    tkMessageBox.showerror("Error", "Out of the area")
        else:
            tkMessageBox.showerror("Error", "Out of the area")
            
        
        
    
    def close(self):
        self.parent.destroy()

        
        
def display():
    root = tk.Tk()
    root.title("Battle ship")
    gui = Gui(root)
    root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()
    
    
if __name__ == "__main__":
    display()


