# Import the pygame module
import pygame
from pygame.locals import *
import time
from os import path, mkdir
import picamera


width = 800
height = 480
alive = True
firstLoop = True


if not path.exists('photos'): #Create photo directory if not present
    mkdir('photos')

pygame.init() # Initialize pygame
clock = pygame.time.Clock() #Setup clock for 60 fps
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #Setup screen
font = pygame.font.Font(None, 24) #Create font


#Create some colors
black = 0,0,0
white = 255,255,255

layer = pygame.Surface([width, height], pygame.SRCALPHA) #Creates transparent surface for GUI
text = 'Hello'
textGraphic = font.render(text, True, white)

camera = picamera.PiCamera() #Setup camera
camera.resolution = (4056, 2434) #Set resolution
camera.start_preview() #Start preview

# Main loop
while alive:
    screen.fill((0, 0, 0))
    layer.fill((0, 0, 0, 0))
    layer.blit(textGraphic, (100,100))

    for event in pygame.event.get(): #Detects key press (temp until GUI)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                alive = False
                pygame.quit()
                camera.stop_preview()
                raise SystemExit

    pygamesScreenRaw = pygame.image.tostring(layer, 'RGBA')
    if firstLoop:
        o = camera.add_overlay(pygamesScreenRaw, size=(
            width, height), fullscreen=True)
        o.alpha = 255
        o.layer = 3
        firstLoop = False
    else:
        o.update(pygamesScreenRaw)
    

    clock.tick(60)


