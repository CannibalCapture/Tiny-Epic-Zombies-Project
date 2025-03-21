import pygame, pygame_gui, bcrypt, sqlite3, os
from pygame.locals import *
import pygame_gui.elements.ui_image, pygame_gui.elements.ui_text_box
from TinyEpicZombies.constants import WIDTH, HEIGHT, DISPLAY
from TinyEpicZombies.gamerenderer import GameRenderer
from TinyEpicZombies.gamemanager import GameManager

def createNewUser(username, password):
    flag = True
    salt = bcrypt.gensalt()
    password = hash(password, salt)
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "INSERT INTO Users(Username, Password, Salt, Wins, Losses) VALUES(?,?,?,?,?)"
    try:
        cursor.execute(SQL, (username, password, salt, 0, 0))
        connection.commit()
    except:
        flag = False

    connection.close()
    return flag

def hash(data, salt):
    bytes = data.encode('utf-8')
    hashedData = bcrypt.hashpw(bytes, salt)
    return hashedData

def fetchStatistics(userID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "SELECT Wins, Losses FROM Users WHERE ID = ?"
    stats = cursor.execute(SQL, (userID,)).fetchone()
    connection.close()
    return(stats)

def loginUser(username, password):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "SELECT Salt FROM Users WHERE username = ?"
    try:
        salt = cursor.execute(SQL, (username,)).fetchone() # fetches the salt associated with the username
        password = hash(password, salt[0]) # using the salt, hashes the given password and stores it back in the password variable
        SQL = "SELECT ID FROM Users WHERE username = ? and password = ?" # performs a comparison between the stored username / hashed password and the given username / hashed password.
        result = cursor.execute(SQL, (username, password)).fetchone() # executes the above
    except:
        result = None
    connection.close()
    if result: # if there is a value in result, it will be the user ID of the user associated with the entered username (and password). 
        return result[0]
    else: # if there is NOT a value in result, the password must have been incorrect.
        return -1

pygame.init()

clock = pygame.time.Clock()

# logged out screen elements:
loggedOut = pygame_gui.UIManager((WIDTH, HEIGHT))
loBgImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "loBgImg.jpg"))
loBgImg = pygame.transform.scale(loBgImg, (WIDTH, HEIGHT))
loggedOutBg = pygame_gui.elements.UIImage(pygame.Rect((0,0), (WIDTH, HEIGHT)), loBgImg, manager=loggedOut)
startLoginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2 - 120, HEIGHT/2 - 20), (100, 25)), text="Login", manager=loggedOut)
startSignupButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2 + 20, HEIGHT/2 - 20), (100, 25)), text="Signup", manager=loggedOut)
titleLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2-65, 0), (200, 60)), text="Tiny Epic Zombies", manager=loggedOut)

# login screen elements
login_page = pygame_gui.UIManager((WIDTH, HEIGHT))
loginUsernameInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 50), (100, 30)), manager=login_page)
loginPasswordInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 100), (100, 30)), manager=login_page)
loginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 25)), text="Login", manager=login_page)
returnToLoggedOutButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=login_page)
loginPasswordInput.set_text_hidden(True)
loginPasswordInput.hidden_text_char="*"

# signup page elements
signup_page = pygame_gui.UIManager((WIDTH, HEIGHT))
signupUsernameInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 50), (100, 30)), manager = signup_page)
signupPasswordInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 100), (100, 30)), manager = signup_page)
signupButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 25)), text="Signup", manager=signup_page)
returnToLoggedOutButton1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=signup_page)

# main menu elements
mainMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
mmBgImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "mmBgImg.png"))
mmBgImg = pygame.transform.scale(mmBgImg, (WIDTH, HEIGHT))
mmBg = pygame_gui.elements.UIImage(pygame.Rect((0,0), (WIDTH, HEIGHT)), mmBgImg, manager=mainMenu)
welcomeLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2, 50), (200, 100)),text="Welcome", manager=mainMenu)
logoutButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Logout", manager=mainMenu)
startGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2, HEIGHT/2-100), (100, 25)), text="Start Game", manager=mainMenu)
statsButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-165, HEIGHT-250), (280, 85)), text="Stats", manager=mainMenu)
newGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-300, HEIGHT-335), (280, 85)), text="New Game", manager=mainMenu)
loadGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-15, HEIGHT-335), (280, 85)), text="Load Game", manager=mainMenu)

# select save slot menu
saveSlotMenuNew = pygame_gui.UIManager((WIDTH, HEIGHT))
returnToMainMenu1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=saveSlotMenuNew)
saveSlot1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 250), (280, 85)), text="Save Slot 1", manager=saveSlotMenuNew)
saveSlot2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 360), (280, 85)), text="Save Slot 2", manager=saveSlotMenuNew)

# gameName = pygame_gui.elements.UITextEntryLine(pygame.Rect((150, 100), (100, 30)), manager=mainMenu)
# gameNameLabel = pygame_gui.elements.UILabel(pygame.Rect((0, 70), (200, 100)),text="Game Name", manager=mainMenu)
# playersNumber = pygame_gui.elements.UITextEntryLine(pygame.Rect((150, 150), (20, 30)), manager=mainMenu)
# playersNumberLabel = pygame_gui.elements.UILabel(pygame.Rect((20, 115), (200, 100)),text="Players", manager=mainMenu)



# stats gui
statsPage = pygame_gui.UIManager((WIDTH, HEIGHT))
statsLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2 - 200, 50), (200, 100)),text="Statistics", manager=statsPage)
returnToMainMenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=statsPage)
playerWins = pygame_gui.elements.UITextBox("test str", pygame.Rect((200, 200),(100, 40)), manager=statsPage)
playerLosses = pygame_gui.elements.UITextBox("test str", pygame.Rect((200, 260),(100, 40)), manager=statsPage)

# in game gui
gameboard = pygame_gui.UIManager((WIDTH, HEIGHT))
exitGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Exit game", manager=gameboard)

manager = loggedOut
renderer = GameRenderer()
gm = GameManager()

run = True
while run:
    time_delta = clock.tick(30)/1000
    DISPLAY.fill((0, 0, 0))
    DISPLAY.blit(loBgImg)

    if manager == gameboard:
        if not gm.getRunGame():
            manager = mainMenu
        gm.renderGameScreen()

    for event in pygame.event.get():

        if event.type == QUIT:
            run = False

        elif event.type == pygame.KEYUP:
            gm.onKeyPress(event.key)

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            gm.onClick(pos)

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == loginButton: # calls the login process
                username, passw = (loginUsernameInput.text, loginPasswordInput.text)
                loginPasswordInput.clear()
                id = loginUser(username, passw)
                if id > -1:
                    manager = mainMenu
                else:
                    print("Incorrect username or password")
            if event.ui_element == signupButton: # calls the add new user process
                username, passw = (signupUsernameInput.text, signupPasswordInput.text)
                if len(passw) < 8 or passw.isalnum():
                    print("Error - Password must be 8 or more characters and include a special character")
                elif len(username) <= 0:
                    print("Error - Username required")
                else:
                    createNewUser(username, passw)
                    manager = login_page
                signupPasswordInput.clear()
                signupUsernameInput.clear()

            elif event.ui_element == logoutButton: # returns to login screen
                manager = loggedOut
            elif event.ui_element == returnToLoggedOutButton or event.ui_element == returnToLoggedOutButton1:
                manager = loggedOut
            elif event.ui_element == startGameButton: # proceed to game board screen
                manager = gameboard
            elif event.ui_element == exitGameButton or event.ui_element == returnToMainMenu or event.ui_element == returnToMainMenu1: # exit game to main menu
                manager = mainMenu
            elif event.ui_element == startLoginButton: # proceed to login page
                manager = login_page
            elif event.ui_element == startSignupButton: # proceed to signup page
                manager = signup_page
            elif event.ui_element == newGameButton:
                manager = saveSlotMenuNew
            elif event.ui_element == statsButton:
                stats = fetchStatistics(id)
                wins = stats[0]
                losses = stats[1]
                playerWins.set_text(f"Wins: {wins}")
                playerLosses.set_text(f"Losses: {losses}")
                manager = statsPage

        manager.process_events(event)
    
    manager.update(time_delta)
    

    manager.draw_ui(DISPLAY)

    pygame.display.update()

pygame.quit()