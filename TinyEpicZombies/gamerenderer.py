import pygame, pygame_gui
import os
from .constants import WIDTH, HEIGHT

gameboard = pygame_gui.UIManager((WIDTH, HEIGHT))

class GameRenderer:
    def __init__(self): # maybe use a dictionary to return buttons and images to main. {"button":pygame_gui.elements.UIButton...}
        gameboardSurf = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg"))
        pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect((0, 0), (WIDTH, HEIGHT)), image_surface=gameboardSurf, manager=gameboard)
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Exit game", manager=gameboard)

