import pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH = info.current_w
HEIGHT = info.current_h

CENTRE_ROOM = (4,2)
COLOURS = ["PURPLE", "ORANGE", "GREEN", "PURPLE", "NONE", "BLUE", "GREEN", "BLUE", "ORANGE"]

CW = (WIDTH/8.5)*2.5*0.8 # Card width
CH = (HEIGHT/8.5)*2.4*0.9 # Card Height

tlCoords = [((WIDTH - CH)/2 - CW, (HEIGHT - CW)/2 - CH),
            ((WIDTH - CH)/2,(HEIGHT - CH)/2 - CW),
            ((WIDTH + CH)/2, (HEIGHT - CW)/2 - CH),
            ((WIDTH - CW)/2 - CH, (HEIGHT - CW)/2),
            ((WIDTH - CW)/2, (HEIGHT - CH)/2),
            ((WIDTH + CW)/2, (HEIGHT - CW)/2),
            ((WIDTH - CH)/2 - CW,(HEIGHT + CW)/2),
            ((WIDTH - CH)/2, (HEIGHT+CH)/2),
            ((WIDTH + CH)/2, (HEIGHT + CW)/2)
            ]