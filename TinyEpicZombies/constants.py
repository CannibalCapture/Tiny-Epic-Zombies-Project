import pygame, os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
WIDTH = info.current_w
HEIGHT = info.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

CENTRE_ROOM = (4,2)
COLOURS = ["PURPLE", "ORANGE", "GREEN", "PURPLE", "NONE", "BLUE", "GREEN", "BLUE", "ORANGE"]
peNames = ["parkingDeckZ.jpg", "galleria.jpg", "craftsAndColours.jpg", "hoardsCollectibles.jpg", "centralStore.jpg", "echoRidgeFoodCourt.jpg", "1stPlaceSporting.jpg", "department.jpg", "ampsElectronics.jpg"]
rotations = [0, -90, 0, 90, 0, -90, 180, 90, 180]

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

# roomCoords will form a polygon which will be the space you can click to select a room. 
# the coords will be relative to the top-left corner of the room.
roomCoords = [
            [
            [()],
            [()],
            [()],
            ],

            [     # Store 1
            [((131, 145), (167, 188))], # (0,0)
            [((69, 107), (107, 152))], # (0,1)
            [((13, 112), (51, 174))], # (0,2)
            ],

            [
            [()],
            [()],
            [()],
            ],

            [
            [()],
            [()],
            [()],
            ],

            [       # Central Store
            [((10, 31), (51, 145))],
            [((57, 2), (232, 23))],
            [((94, 52), (214, 132))],
            [((81, 159), (243, 181))],
            [((251, 31), (291, 153))],
            ],

            [
            [()],
            [()],
            [()],
            ],

            [
            [()],
            [()],
            [()],
            ],

            [
            [()],
            [()],
            [()],
            ],

            [
            [()],
            [()],
            [()],
            ]
        ]