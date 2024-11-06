import sqlite3
import pygame, pygame_gui
from pygame.locals import *

def createNewUser(username, password):
    flag = True
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "INSERT INTO Users(username, password) VALUES(?,?)"
    try:
        cursor.execute(SQL, (username, password))
        connection.commit()
    except:
        flag = False

    connection.close()
    return flag

def loginUser(username, password):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "SELECT ID FROM Users WHERE username = ? and password = ?"
    result = cursor.execute(SQL, (username, password)).fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return -1
    
pygame.init()

WIDTH = 1100
HEIGHT = 500
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

login_page = pygame_gui.UIManager((WIDTH, HEIGHT))
usernameInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 50), (100, 30)), manager = login_page)
passwordInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 100), (100, 30)), manager = login_page)
loginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 25)), text="Login")


mainMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
welcomeLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2, HEIGHT/2), (200, 100)),text="Welcome", manager=mainMenu)

manager = login_page

run = True
while run:
    time_delta = clock.tick(30)/1000

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == loginButton:
                id = loginUser(usernameInput.text, passwordInput.text)
                print(id)
                if id > -1:
                    manager = mainMenu
        manager.process_events(event)
    
    manager.update(time_delta)

    display.fill((0, 0, 0))

#    pygame.draw.rect(display, (255, 0, 0), (100, 100, 100, 100))

    manager.draw_ui(display)


    pygame.display.update()

pygame.quit()


# createNewUser("Toby", "password123")