#!/usr/bin/env python

#importy
import numpy
import socket

    
class yoursShips():
    
    yours_ships = numpy.zeros((10,10), int)
    
    def __init__(self, data,):
        self.data = data
        self.error = 0
    
    def check(self):
        for r in self.data.keys():
            if r == 0:
                x = self.data[r][0]
                y = self.data[r][1]
                for i_x in range(x - 2, x + 3):
                    if self.yours_ships[y][i_x] in (0, 1):
                        self.yours_ships[y][i_x] = 1
                    else:
                        self.error = 1
            elif r == 1:
                x = self.data[r][0]
                y = self.data[r][1]
                for i_x in range(x - 1, x + 2):
                    if self.yours_ships[y][i_x] in (0, 2):
                        self.yours_ships[y][i_x] = 2
                    else:
                        self.error = 2
            elif r == 2:
                x = self.data[r][0]
                y = self.data[r][1]
                for i_x in range(x - 1, x + 1):
                    if self.yours_ships[y][i_x] in (0, 3):
                        self.yours_ships[y][i_x] = 3
                    else:
                        self.error = 3
            elif r == 3:
                x = self.data[r][0]
                y = self.data[r][1]
                if self.yours_ships[y][x] in (0, 4):
                    self.yours_ships[y][x] = 4
                else:
                    self.error = 4
        return self
    

