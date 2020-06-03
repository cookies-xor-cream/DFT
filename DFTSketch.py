import pygame
import random
from math import *
import DFT

pygame.init()


def initialize_canvas():
    global canvas_width
    global canvas_height
    canvas_width = 1000
    canvas_height = 1000
    
    global xStartx
    global xStarty
    global yStartx
    global yStarty
#     xStartx = 2*canvas_width//3
#     xStarty = canvas_height//8
#     yStartx = canvas_width//8
#     yStarty = 2*canvas_height//3

    xStartx = 500
    xStarty = 100
    yStartx = 500
    yStarty = 500

    global canvas
    global width_const
    canvas = pygame.display.set_mode((canvas_width, canvas_height))
    width_const = 1
    
    global fps
    global clock
    fps = 60
    clock = pygame.time.Clock()
    
    global maxlen
    maxlen = 1000000
    
    global startx
    global starty
    global rez
    startx = canvas_width//5
    starty = canvas_height//2
    rez = 200
    
    global stroke
    stroke = 2

def initialize_colours():
    global white
    global black
    white = (255, 255, 255)
    black = (0, 0, 0)
   
   
def initialize_all():
    initialize_colours()
    initialize_canvas()
    

def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
    

def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
    
    
class Epicycle:
    def __init__(self, x, y, amplitude, frequency, theta):
        self.x0 = x
        self.y0 = y
        self.a = amplitude
        self.f = frequency
        self.phase = theta
        
        self.x1 = 0
        self.y1 = 0
        self.update()
        
    def draw(self):
        pygame.draw.circle(canvas, white, (int(self.x0), int(self.y0)), int(abs(self.a)), width_const)
        pygame.draw.line(canvas, white, (int(self.x0), int(self.y0)), (int(self.x1),int(self.y1)))
        
    def update(self):
        self.x1 = self.x0 + self.a*cos(self.f*angle - self.phase)
        self.y1 = self.y0 + self.a*sin(self.f*angle - self.phase)
        
    def tail(self, previous):
        self.x0 = previous.x1
        self.y0 = previous.y1
    
class Projection:
    def __init__(self, offset = 0):
        self.offset = offset
        self.array = []
        
    def addpoint(self, x, y):
        self.array.append([x,y])
        
    def limit(self):
        if len(self.array) > maxlen:
            self.array.pop(0)
        
    def push(self, variable):
        mapping = {"x": 0, "y": 1}
        index = mapping[variable]
        
        for i in self.array:
            i[index] += pushstrength
        
    def draw(self):
        for i in range(len(self.array)-1):
            x0 = self.array[i][0]
            y0 = self.array[i][1]
            x1 = self.array[i+1][0]
            y1 = self.array[i+1][1]
            
            if dist((x0, y0), (x1, y1)) < 5:
                pygame.draw.line(canvas, white, (int(x0), int(y0)), (int(x1), int(y1)),stroke)

            
def c_project(x0, y0, x1, y1):
    pygame.draw.line(canvas, white, (int(x0), int(y0)), (int(x1), int(y1)))
    
    
def main_loop():
    global angle
    thing = 0
    
    running = True
    
    angle = 0
    
    sine = []
    cosine = []
    epix = []
    epiy = []
    curves = []
    
    X, Y = DFT.transform()
    depth = len(X)
    
    epix.append(Epicycle(xStartx, xStarty, X[0][0], X[0][1], X[0][2]))
    
    for i in range(1,depth):
        epix.append(Epicycle(epix[i-1].x1, epix[i-1].y1, X[i][0], X[i][1], X[i][2]))
        
    
    epiy.append(Epicycle(yStartx, yStarty, -1*Y[0][0], Y[0][1], Y[0][2]))
    
    for i in range(1, depth):
        epiy.append(Epicycle(epiy[i-1].x1, epiy[i-1].y1, Y[i][0], -1*Y[i][1], -1*(Y[i][2]+pi/2)))
    
    curves.append(Projection())
    
    clock.tick(fps)
    
    epix = sorted(epix, key = lambda x: -x.a)
    epiy = sorted(epiy, key = lambda x: -x.a)
    
    while running:
        dt = 2*pi/depth
        canvas.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        curves[0].addpoint(epix[-1].x1, epiy[-1].y1)
        curves[0].limit()
                
        pygame.draw.line(canvas,white,(epix[-1].x1,epix[-1].y1),(epix[-1].x1,epiy[-1].y1))
        pygame.draw.line(canvas,white,(epiy[0].x0,epiy[-1].y1),(epix[-1].x1,epiy[-1].y1))
        
        
        for i in curves:
            i.draw()
        
        for epi in [epix, epiy]:
            epi[0].update()
            epi[0].draw()
        
        for i in range(1, depth):
            for epi in [epix, epiy]:
                epi[i].tail(epi[i-1])
                epi[i].update()
                if epi[i].a >= 1:
                    epi[i].draw()

        angle -= dt
        
        pygame.display.update()
        
        
    pygame.time.delay(500)
    
    pygame.quit()
    quit()

    
def sketchDFT():
    initialize_all()
    pygame.time.delay(500)
    main_loop()