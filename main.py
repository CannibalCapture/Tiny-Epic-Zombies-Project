import pygame, pygame_gui, bcrypt, sqlite3
from pygame.locals import *
import pygame_gui.elements.ui_image

def createNewUser(username, password):
    flag = True
    salt = bcrypt.gensalt()
    password = hash(password, salt)
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "INSERT INTO Users(username, password, salt) VALUES(?,?, ?)"
    try:
        cursor.execute(SQL, (username, password, salt))
        connection.commit()
    except:
        flag = False

    connection.close()
    return flag

def hash(data, salt):
    bytes = data.encode('utf-8')
    hashedData = bcrypt.hashpw(bytes, salt) 
    return hashedData

# createNewUser("Toby", "password123")

def loginUser(username, password):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "SELECT Salt FROM Users WHERE username = ?"
    salt = cursor.execute(SQL, (username,)).fetchone()
    password = hash(password, salt[0])
    SQL = "SELECT ID FROM Users WHERE username = ? and password = ?"
    result = cursor.execute(SQL, (username, password)).fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return -1

pygame.init()

WIDTH = 700
HEIGHT = 600
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

login_page = pygame_gui.UIManager((WIDTH, HEIGHT))
usernameInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 50), (100, 30)), manager = login_page)
passwordInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 100), (100, 30)), manager = login_page)
loginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 25)), text="Login")


mainMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
welcomeLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2, 50), (200, 100)),text="Welcome", manager=mainMenu)
logoutButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 150), (100, 25)), text="Logout", manager=mainMenu)
startGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2, HEIGHT/2), (100, 25)), text="Start Game", manager=mainMenu)

gameboard = pygame_gui.UIManager((WIDTH, HEIGHT))
gameboardSurf = pygame.image.load("C:\\Users\\DELL\\Desktop\\School-Note\\Computing\\Tiny-Epic-Zombies\\TinyEpicZombies-Code\\gameboard.png")
pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect((0, 0), (WIDTH, HEIGHT)), image_surface=gameboardSurf, manager=gameboard)
exitGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Exit game", manager=gameboard)

manager = login_page

run = True
while run:
    time_delta = clock.tick(30)/1000

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == loginButton: # calls the login process
                id = loginUser(usernameInput.text, passwordInput.text)
                if id > -1:
                    manager = mainMenu
            elif event.ui_element == logoutButton: # returns to login screen
                manager = login_page
            elif event.ui_element == startGameButton: # sends to game board screen
                manager = gameboard
            elif event.ui_element == exitGameButton: # exit game to main menu
                manager = mainMenu
            
        manager.process_events(event)
    
    manager.update(time_delta)

    display.fill((0, 0, 0))

#    pygame.draw.rect(display, (255, 0, 0), (100, 100, 100, 100))

    manager.draw_ui(display)


    pygame.display.update()

pygame.quit()
