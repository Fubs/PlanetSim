# Planet simulator, by max behling.
# Make sure to change the following variables to your screen resolution. 

width = 2560
height = 1440

###################################################################

import pygame
import pygame.mixer
import math  
import pygame.font
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

truescreen = pygame.display.set_mode((width,height))
win = truescreen.copy()
clock = pygame.time.Clock()
displayfont = pygame.font.SysFont("Arial", 20)

def distance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist 


# These values control the default position
def resetpos():
    earth.vx = 0
    earth.vy = 5 
    earth.x = width/2 - width/6 
    earth.y = height/2
    sun.x = width/2 + width/6
    sun.y = height/2
    sun.vx = 0
    sun.vy = -5
    return

class orbiter:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.mass = 1

def tracerUpdate(orbiter, xtracer, ytracer):
    xtracer.insert(0, int(round(orbiter.x)))
    ytracer.insert(0, int(round(orbiter.y)))
    xtracer.pop()
    ytracer.pop()   

# This controls the number of position updates per frame
ClockSpeed = 200

# Color codes
white = (255, 255, 255)
black = (0, 0, 0)
red =(255, 0 ,0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

earth = orbiter()
earth.mass = 100

sun = orbiter()
sun.mass = 100

resetpos()

# This controls the strength of gravity
G = 500

# Path tracers are initialized with 100 zeroes due to how I wrote the tracer update function
earthTracerX = []
earthTracerY = []
sunTracerX = []
sunTracerY = []
def cleartracers():
    for x in range(100):
        earthTracerX.append(0)
        earthTracerY.append(0)
        sunTracerX.append(0)
        sunTracerY.append(0)

cleartracers()

run = True
while run: 
    
    clock.tick(ClockSpeed*5)
    for event in pygame.event.get():
        if event.type == "pygame.QUIT":
            run = False

    win.fill((0,0,0)) 
    keys = pygame.key.get_pressed()

    tracerUpdate(earth, earthTracerX, earthTracerY)
    tracerUpdate(sun, sunTracerX, sunTracerY)
    
    dist = distance(earth.x, earth.y, sun.x, sun.y)
    f = (G*sun.mass*earth.mass)/(dist**2)

    theta = math.atan2((sun.y-earth.y),(sun.x-earth.x))
    phi = math.atan2((earth.y-sun.y),(earth.x-sun.x))

    earth.ax = math.cos(theta)*f/earth.mass
    earth.ay = math.sin(theta)*f/earth.mass
    sun.ax = math.cos(phi)*f/sun.mass
    sun.ay = math.sin(phi)*f/sun.mass

    earth.vx += earth.ax
    earth.vy += earth.ay
    sun.vx += sun.ax
    sun.vy += sun.ay

    earth.x += earth.vx
    earth.y += earth.vy
    sun.x += sun.vx
    sun.y += sun.vy

    if keys[pygame.K_r]:
        resetpos()
        earthTracerX = []
        earthTracerY = []
        sunTracerX = []
        sunTracerY = []
        cleartracers()

    if keys[pygame.K_q]:
        run = False

    if keys[pygame.K_UP]:
        earth.vy -= 0.2

    if keys[pygame.K_DOWN]:
        earth.vy += 0.2
        
    if keys[pygame.K_RIGHT]:
        earth.vx += 0.2

    if keys[pygame.K_LEFT]:
        earth.vx -= 0.2

    if dist < 30:
        earth.vx *= 0.5
        sun.vx *= 0.5
        earth.vy *= 0.5
        sun.vy *= 0.5

    for p in range(100):
        pygame.draw.circle(win, green, (int(round(earthTracerX[p])), int(round(earthTracerY[p]))), 1, 0)
        pygame.draw.circle(win, red, (int(round(sunTracerX[p])), int(round(sunTracerY[p]))), 1, 0)

        
    pygame.draw.circle(win, blue, (int(round(earth.x)), int(round(earth.y))), 5,0)
    pygame.draw.circle(win, yellow, (int(round(sun.x)),int(round(sun.y))), 5, 0)

    Xcenter = (earth.x + sun.x)/2  
    Ycenter = (earth.y + sun.y)/2
    


    truescreen.blit(win, (0,0))


    text1 = displayfont.render("controls:",0,white)
    text2 = displayfont.render("arrow keys - control blue dot's motion",0,white)
    text3 = displayfont.render("r - reset",0,white)
    text4 = displayfont.render("q - quit",0,white)
    truescreen.blit(text1,(5,height - int(0.087 * height)))
    truescreen.blit(text2,(5,height - int(0.0694 * height)))
    truescreen.blit(text3,(5,height - int(0.0521 * height)))
    truescreen.blit(text4,(5,height - int(0.0347 * height)))


    pygame.display.update()



pygame.quit()
