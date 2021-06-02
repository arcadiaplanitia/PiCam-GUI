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
screen = pygame.display.set_mode((0, 0)) #Setup screen , pygame.FULLSCREEN
font = pygame.font.Font(None, 24) #Create font

#Create some colors
black = 0,0,0
white = 255,255,255

#Functions
class Button:
    def __init__(self, text,  pos, font, bg, feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg):
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        layer.blit(button1.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg=white)



layer = pygame.Surface([width, height], pygame.SRCALPHA) #Creates transparent surface for GUI
text = 'Hello'
textGraphic = font.render(text, True, white)

camera = picamera.PiCamera() #Setup camera
camera.resolution = (4056, 2434) #Set resolution
camera.start_preview() #Start preview

#Buttons
button1 = Button("Click here", (100, 100), font=30, bg=black, feedback="You clicked me")

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
        button1.click(event)
    
    button1.show()
    pygamesScreenRaw = pygame.image.tostring(layer, 'RGBA')
    if firstLoop:
        o = camera.add_overlay(pygamesScreenRaw, size=(width, height), fullscreen=True)
        o.alpha = 255
        o.layer = 3
        firstLoop = False
    else:
        screen.blit(layer, (0,0))
        pygame.display.update()
        o.update(pygamesScreenRaw)
    

    clock.tick(60)
