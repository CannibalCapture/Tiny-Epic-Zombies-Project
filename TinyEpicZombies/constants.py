import pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH = info.current_w
HEIGHT = info.current_h

CENTRE_ROOM = (4,2)
COLOURS = ["PURPLE", "ORANGE", "GREEN", "PURPLE", "NONE", "BLUE", "GREEN", "BLUE", "ORANGE"]
# WIDTH = 900
# HEIGHT = 600
CARD_WIDTH = (WIDTH/8.5)*2.5*0.8
CARD_HEIGHT = (HEIGHT/8.5)*2.4*0.8