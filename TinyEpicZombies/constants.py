import pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH = info.current_w
HEIGHT = info.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

CENTRE_ROOM = (4,2)
COLOURS = ["PURPLE", "ORANGE", "GREEN", "PURPLE", "NONE", "BLUE", "GREEN", "BLUE", "ORANGE"]
peNames = ["echoRidgeSecurity.jpg", "hursJewelers.jpg", "craftsAndColours.jpg", "gamelynWorld.jpg", "centralStore.jpg", "echoRidgeFoodCourt.jpg", "1stPlaceSporting.jpg", "department.jpg", "ampsElectronics.jpg"]
rotations = [0, -90, 0, 90, 0, -90, 180, 90, 180]

CW = (0.23) # Card width
CH = (0.25) # Card Height

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