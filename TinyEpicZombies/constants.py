import pygame, os
from .helperfunctions.roomrects import genRoomRects

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

roomrects = genRoomRects()

OFFSETS = {
    (-0.03, 0):[(0,0), (0,1), (0,2), 
               (1,0), (1,1), (1,2), 
               (2,0), (2,1), 
               (3,0), (3,1), (3,2), 
               (4,1), (4,2), (4,4), 
               (5,0), (5,1), (5,2), 
               (6,1), (6,2), 
               (7,1), (7,2), 
               (8,0)],

    (0, -0.03):[(2,2), 
               (4,0), (4,3), 
               (6,0), 
               (7,0), 
               (8,1), (8,2)]
}