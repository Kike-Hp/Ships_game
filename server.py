#!/usr/bin/env python
import socket 
import thread
import cPickle as pickle
import time

class Server_ship():
    def __init__(self):
        #AF_INET - domena adresowa gniazda (socket),  SOCK_STREAM - typ gniazda
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #SOL_SOCKET - warstwa gniazda socket.SO_REUSEADDR - powiazanie z gniazdem, 1 - ilosc prob
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        IP_address = str('127.0.0.1')               # podaje adres Ip
        Port = int(10000)                           # podaje nr portu 
        self.server.bind((IP_address, Port))        # oczekiwanie na polaczenie
        self.server.listen(2)                       #slucha 2 aktywnych polaczen  
        self.list_of_clients = []                   #lista clients
        self.data_of_clients = {}                   #slownik z poczatkowym ustawwieniem
      
    def clientthread(self, conn, addr): 
    
      
        while True: 
            try: 
                message = conn.recv(4096)
                if message:
                    message_to_send = pickle.loads(message)
                    if message_to_send == "CLOSE":
                        time.sleep(0.5)
                        self.Close("CLOSE")
                    else:
                        if len(self.data_of_clients.keys()) < 2:
                            self.data_of_clients[message_to_send[0]] = message_to_send[1]
                            if len(self.data_of_clients.keys()) == 2:
                                self.ship(message_to_send[0])
                        if len(self.data_of_clients.keys()) == 2:
                            self.your_headshot = 0
                            if len(message_to_send[1]) == 2:
                                win = 1
                                for k, v in self.data_of_clients.items():
                                    if k != message_to_send[0]:
                                        if v[message_to_send[1][1], message_to_send[1][0]] in (1, 2, 3, 4):
                                            win = 0
                                            for i in range(1, 5):
                                                if v[message_to_send[1][1], message_to_send[1][0]] == i:
                                                    immersion = 0
                                                    headshot = pickle.dumps(('headshot', [message_to_send[1][1], message_to_send[1][0]]), -1)
                                                    v[message_to_send[1][1], message_to_send[1][0]] = 9
                                                    for row in v:
                                                        for col in row:
                                                            if col == i:
                                                                immersion = 1
                                                    self.headshot(headshot, conn)
                                                    self.your_headshot = 1
                                                    if immersion == 0:
                                                        time.sleep(0.1)
                                                        self.position_ship(message_to_send[0], i, conn)
                                        for row in v:
                                            for col in row:
                                                if col in (1, 2, 3, 4):
                                                    win = 1
                                        v[message_to_send[1][1], message_to_send[1][0]] = 9
                                        time.sleep(0.1)
                                        self.broadcast(message, conn)
                                        if win == 0:
                                            time.sleep(0.2)
                                            self.broadcast('LOSER', conn)
                            if self.your_headshot == 0:
                                time.sleep(0.5)
                                self.broadcast("start", conn)
                else: 
                    self.remove(conn) 
            except: 
                continue
            
    def position_ship(self, user, number, conn):
        for k, v in self.user.items():
            if k != user:
                message = pickle.dumps([number, v[number - 1]])
                self.headshot(message, conn)
        
    def ship(self, name):
        user = {}
        for k, v in self.data_of_clients.items():
            ships = []
            for number in range(1,5):
                row = 0
                col = 0
                count_c = 0
                for index, i in enumerate(v):
                    for column, c in enumerate(i):
                        if c == number:
                            row = row + index
                            col = col + column
                            count_c += 1
                ships.append([row/count_c, col/count_c])
            user[k] = ships
        self.user = user
        
    #wyslanie do wszystkich poza osoba wysylajaca"
    def Close(self, message):
        for clients in self.list_of_clients:
            try:
                self.data_of_clients = {}
                self.list_of_clients.remove(clients)
                clients.send(message)
                clients.close()
            except:
                continue
    def headshot(self, message, connection):
        for clients in self.list_of_clients:
            if clients == connection: 
                try: 
                    clients.send(message) 
                except: 
                    clients.close()
                
    def broadcast(self, message, connection):
        for clients in self.list_of_clients:
            if clients != connection: 
                try: 
                    clients.send(message) 
                except: 
                    clients.close() 
                    # if the link is broken, we remove the client 
                    self.remove(clients) 
                    
            if message == 'LOSER':
                if clients == connection:
                    try:
                        clients.send('WIN')
                    except:
                        clients.close()
                        self.remove(clients)
      
    #usuniecie klientow z listy
    def remove(self, connection): 
        if connection in self.list_of_clients: 
            self.list_of_clients.remove(connection) 
    
    def DUP(self):  
        while True:
      
        #akceptuje polaczenie i przechowuje adres oraz typ gniazda
            conn, addr = self.server.accept() 
        # dodaje do listy klientow
            self.list_of_clients.append(conn)
      
        # wypisuje klientow ktorzy sie polaczyli 
            print addr[0] + " connected"
        #tworzy osobny watek dla kazdego klienta
            thread.start_new_thread(self.clientthread,(conn, addr)) 
        
      
if __name__ == "__main__":
    Server_ship().DUP()
    
    
# server.close() 