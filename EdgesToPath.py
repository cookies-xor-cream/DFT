#Plot to check

import random
import csv
import pygame
pygame.init()

proximity_threshold = 5
threshold = 200

def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def sort_edges(edges):
#     random.seed(30)
    edgepath = [edges[random.randrange(0,len(edges))]]
    
    while len(edges) > 0:
        xi = 0
        edgetest = 0
        mindist = float("inf")
        
        for i in range(len(edges)):
            distance = dist(edges[i], edgepath[-1])
            if distance < mindist:
                mindist = distance
                next_edge = edges[i]
                edgetest = mindist
                
                xi = i
                
                if distance < proximity_threshold:
                    break
                
        point = edges.pop(xi)
        
        if edgetest < threshold:
            edgepath.append(point)
            
#     edgepath = edgepath[:(19*len(edgepath)//20)]
               
    return edgepath
    
scale = 1
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

pathcompletion = len(coordinates)

# while True:
#     coordinates = sort_edges(coordinates)
#     if 2*pathcompletion//3 < len(coordinates):
#         break
    
coordinates = sort_edges(coordinates)

with open("DFT.csv", mode = "w") as DFTFile:
    DFTFile.truncate()
    DFTLog = csv.writer(DFTFile, lineterminator = "\n", delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for i in range(0, len(coordinates)):
        DFTLog.writerow(coordinates[i])
        
# for i in range(len(coordinates)):
#     x = scale*coordinates[i][0]
#     y = scale*coordinates[i][1]
#     pygame.draw.line(canvas, (255, 255, 255), (x, y),(x, y), 2)
#     pygame.time.delay(3)
#     pygame.display.update()

for i in range(len(coordinates)-1):
    x0 = scale*coordinates[i][0]
    y0 = scale*coordinates[i][1]
    x1 = scale*coordinates[i+1][0]
    y1 = scale*coordinates[i+1][1]
    
    if dist((x0,y0),(x1,y1)) < 10:
        pygame.draw.line(canvas, (255, 255, 255), (x0, y0),(x1, y1), 1)
    pygame.time.delay(3)
    pygame.display.update()