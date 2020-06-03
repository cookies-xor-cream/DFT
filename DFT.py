#DFT program

from math import *
import cv2


def initialize_canvas():
    global canvas_width
    global canvas_height
    canvas_width = 500
    canvas_height = 500

    global canvas
    canvas = pygame.display.set_mode((canvas_width, canvas_height))
    

def variables():
    rowskip = 1

    file = open("DFT.csv", "r")
    fread = file.read()
    file.close()
    fread = fread.split("\n")
    for i in range(len(fread)):
        fread[i] = fread[i].split(",")
    fread = fread[:-1]

    x = []
    y = []
    for i in range(0, len(fread), rowskip):
        x.append(int(fread[i][0]))
        y.append(int(fread[i][1]))

    X = []
    Y = []
    for i,j in zip([x,y],[X,Y]):
        N = len(i)
        for k in range(N):
            re = 0
            im = 0
            for n in range(N):
                theta = 2*pi*k*n/N
                re += i[n]*cos(theta)
                im -= i[n]*sin(theta)
                
            re /= N
            im /= N
            
            amp = (re**2 + im**2)**0.5
            freq = k
            
            if re:
                phase = atan2(im,re)
            else:
                phase = 0
            
            j.append((amp, freq, phase))
        
    return X, Y