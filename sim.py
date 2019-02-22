# Planet simulator, by Max Behling.
# Make sure to change the following variables to your screen resolution. 

width = 1900
height = 1000

###################################################################

import pygame
import pygame.mixer
import math  
import pygame.font
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.font.init()

truescreen = pygame.display.set_mode((width,height))
win = truescreen.copy()
clock = pygame.time.Clock()
displayfont = pygame.font.SysFont("Arial", 20)

def distance(A,B):  
    dist = math.sqrt((B.x - A.x)**2 + (B.y - A.y)**2)  
    return dist 

def resetpos():
    for orbiter in orbiterlist:
        orbiter.x = orbiter.ix
        orbiter.y = orbiter.iy
        orbiter.vx = orbiter.ivx
        orbiter.vy = orbiter.ivy
        orbiter.ax = 0
        orbiter.ay = 0
        orbiter.xforce = 0
        orbiter.yforce = 0

class orbiter:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.vx = 0
        self.vy = 0
        self.ix = 200
        self.iy = 200
        self.ivx = 0
        self.ivy = 0
        self.ax = 0
        self.ay = 0
        self.mass = random.uniform(70,90)
        self.xforce = 0
        self.yforce = 0
        self.xtracer = []
        self.ytracer = []
        self.color = red
        self.tracercolor = blue

def tracerUpdate(orbiter, xtracer, ytracer):
    xtracer.insert(0, int(round(orbiter.x)))
    ytracer.insert(0, int(round(orbiter.y)))
    xtracer.pop()
    ytracer.pop()   

# This controls the run speed
ClockSpeed = 100

# Color codes
white = (255, 255, 255)
black = (0, 0, 0)
red =(255, 0 ,0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255,165,0)
purple = (138,43,226)

# Initialize orbiters here

orbiterlist = []

orbiter1 = orbiter()
orbiter1.color = blue
orbiter1.tracercolor = purple
orbiterlist.append(orbiter1)
orbiter1.ix = random.uniform(0,width)
orbiter1.iy = random.uniform(0,height)
orbiter1.ivx = 1
orbiter1.ivy = 1

orbiter2 = orbiter()
orbiter2.color = red
orbiter2.tracercolor = orange
orbiterlist.append(orbiter2)
orbiter2.ix = random.uniform(0,width)
orbiter2.iy = random.uniform(0,height)
orbiter2.ivx = 5
orbiter2.ivy = -1

orbiter3 = orbiter()
orbiter3.color = green
orbiter3.tracercolor = yellow
orbiterlist.append(orbiter3)
orbiter3.ix = random.uniform(0,width)
orbiter3.iy = random.uniform(0,height)
orbiter3.ivx = 3
orbiter3.ivy = -2

resetpos()

# This controls the strength of gravity. Adding more orbiters requires weaker gravity.
G = 0.1/len(orbiterlist)

# Path tracers are initialized with 100 zeroes due to how I wrote the tracer update function
def cleartracers():
    for i in orbiterlist:
        i.xtracer = []
        i.ytracer = []
        for x in range(100):
            i.xtracer.append(0)
            i.ytracer.append(0)

cleartracers()

run = True
while run: 
    
    clock.tick(ClockSpeed)
    for event in pygame.event.get():
        if event.type == "pygame.QUIT":
            run = False

    win.fill((0,0,0)) 
    keys = pygame.key.get_pressed()

    for i in orbiterlist:
        tracerUpdate(i, i.xtracer, i.ytracer)


    # Calculate force on each orbiter
    for orbiter in orbiterlist:
        copylist = orbiterlist.copy()
        copylist.remove(orbiter)
        orbiter.xforce = 0
        orbiter.yforce = 0
        for other in copylist:
            dist = distance(orbiter, other)
            angle = math.atan2((other.y - orbiter.y), (other.x - orbiter.x))
            # The force is ignored if the orbiters are closer than 100 units apart, since it gets too big when they are close together.
            if dist > 100:
                orbiter.xforce += (math.cos(angle) * G * orbiter.mass * other.mass)/(dist**2)
                orbiter.yforce += (math.sin(angle) * G * orbiter.mass * other.mass)/(dist**2)

    # Update positions
    for orbiter in orbiterlist:
        orbiter.ax = orbiter.xforce * orbiter.mass
        orbiter.ay = orbiter.yforce * orbiter.mass
        orbiter.vx += orbiter.ax
        orbiter.vy += orbiter.ay
        # This logic makes the orbiters bounce off the sides of the screen.
        if orbiter.x + orbiter.vx > width-3:
            orbiter.x = width-4
            orbiter.vx *= -1
        elif orbiter.x + orbiter.vx < 3:
            orbiter.x = 4
            orbiter.vx *= -1
        else:
            orbiter.x += orbiter.vx
        if orbiter.y + orbiter.vy > height-3:
            orbiter.y = height-4
            orbiter.vy *= -1
        elif orbiter.y + orbiter.vy < 3:
            orbiter.y = 4
            orbiter.vy *= -1
        else:
            orbiter.y += orbiter.vy



    if keys[pygame.K_r]:
        resetpos()
        cleartracers()
        G += random.uniform(0.005,0.006) - random.uniform(0.005,0.006)
        for orbiter in orbiterlist:
            orbiter.x = random.uniform(0,width)
            orbiter.y = random.uniform(0,height)

    if keys[pygame.K_q]:
        run = False

    if keys[pygame.K_UP]:
        orbiter1.vy -= 0.3

    if keys[pygame.K_DOWN]:
        orbiter1.vy += 0.3
        
    if keys[pygame.K_RIGHT]:
        orbiter1.vx += 0.3

    if keys[pygame.K_LEFT]:
        orbiter1.vx -= 0.3


    for orbiter in orbiterlist:
        for p in range(100):
            pygame.draw.circle(win, orbiter.tracercolor, (int(round(orbiter.xtracer[p])), int(round(orbiter.ytracer[p]))), 1, 0)

    for orbiter in orbiterlist: 
        pygame.draw.circle(win, orbiter.color, (int(round(orbiter.x)), int(round(orbiter.y))), 6, 0)

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
