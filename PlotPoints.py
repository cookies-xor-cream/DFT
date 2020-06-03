#Plot to check

import pygame
pygame.init()

scale = 2
canvas_width = 700
canvas_height = 700
canvas = pygame.display.set_mode((canvas_width, canvas_height))


class Point:
    def __init__(self, x, y, tone):
        self.x = x
        self.y = y
        self.tone = tone
        

file = open("edges_white_backdrop.csv", "r")
fread = file.read()
file.close()
fread = fread.replace("\n", ",")
fread = fread.split(",")

coordinates = []
for i in range(0, len(fread)-1, 3):
    x = int(fread[i])
    y = int(fread[i+1])
    coordinates.append((x,y))

for i in range(len(coordinates)):
    x = scale*coordinates[i][0]
    y = scale*coordinates[i][1]
    pygame.draw.line(canvas, (255, 255, 255), (x, y),(x, y), 2)

pygame.display.update()