import pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH = info.current_w
HEIGHT = info.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

CW = 0.23 # Card width
CH = 0.25 # Card Height

COLOURS = {
    "PURPLE":(133,9,181),
    "RED":(255,0,0),
    "BLUE":(0,0,255),
    "GREEN":(0,255,0),
    "BLACK":(0,0,0)
}