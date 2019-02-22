# Planet simulator, by max behling.
# Make sure to change the following variables to your screen resolution. 

width = 2560
height = 1440

###################################################################3

import pygame
import pygame.mixer
import math  
import pygame.font

pygame.init()
pygame.mixer.init()
pygame.font.init()

win = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()


def distance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist 

def resetpos():
    earth.vx = 0
    earth.vy = 0.1 
    earth.x = width/2 - width/3 
    earth.y = height/2
    sun.x = width/2
    sun.y = height/2
    sun.vx = 0
    sun.vy = -0.1
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


# This controls the number of position updates per frame
ClockSpeed = 200

# Color codes
white = (255, 255, 255)
black = (0, 0, 0)
red =(255, 0 ,0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# You can change initial velocities and starting positions here
earth = orbiter()
earth.vx = 0
earth.vy = 5
earth.x = width/2 - width/3 
earth.y = height/2
earth.mass = 1

sun = orbiter()
sun.x = width/2
sun.y = height/2
sun.mass = 200

# This controls the strength of gravity
G = 500

run = True
while run: 
    
    clock.tick(ClockSpeed)
    for event in pygame.event.get():
        if event.type == "pygame.QUIT":
            run = False

    win.fill((0,0,0)) 
    keys = pygame.key.get_pressed()

    
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

    if keys[pygame.K_q]:
        run = False

    if keys[pygame.K_UP]:
        earth.vy -= 0.1

    if keys[pygame.K_DOWN]:
        earth.vy += 0.1
        
    if keys[pygame.K_RIGHT]:
        earth.vx += 0.1

    if keys[pygame.K_LEFT]:
        earth.vx -= 0.1

    if dist < 12:
        resetpos()


    displayfont = pygame.font.SysFont("Arial", 20)
    text1 = displayfont.render("controls:",0,white)
    text2 = displayfont.render("arrow keys: control earth's motion",0,white)
    text3 = displayfont.render("r: reset simulation",0,white)
    text4 = displayfont.render("q: quit",0,white)
    win.blit(text1,(5,height-125))
    win.blit(text2,(5,height-100))
    win.blit(text3,(5,height-75))
    win.blit(text4,(5,height-50))
    pygame.draw.circle(win, blue, ((int(round(earth.x))), int(round(earth.y))), 3,0)
    pygame.draw.circle(win, yellow, (int(round(sun.x)),int(round(sun.y))), 12, 0)


    pygame.display.update()



pygame.quit()
