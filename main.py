import pygame, pygame_gui, bcrypt, sqlite3, os, json, pprint
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
    return flag

def addWin(userID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "UPDATE Users SET Wins = Wins + 1 WHERE ID = ?"
    cursor.execute(SQL, (userID,))
    connection.commit()
    connection.close()
    return

def addLoss(userID):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "UPDATE Users SET Losses = Losses + 1 WHERE ID = ?"
    cursor.execute(SQL, (userID,))
    connection.commit()
    connection.close()
    return

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
loginPasswordInput.set_text("password123*")
loginUsernameInput.set_text("Toby")

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
logoutButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Logout", manager=mainMenu)
statsButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-165, HEIGHT-250), (280, 85)), text="Stats", manager=mainMenu)
newGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-300, HEIGHT-335), (280, 85)), text="New Game", manager=mainMenu)
loadGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-15, HEIGHT-335), (280, 85)), text="Load Game", manager=mainMenu)
# testButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 50)), text="TEST", manager=mainMenu)

# select save slot menu
saveSlotMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
returnToMainMenu1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=saveSlotMenu)
saveSlot1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 150), (280, 85)), text="Save Slot 1", manager=saveSlotMenu)
saveSlot2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 260), (280, 85)), text="Save Slot 2", manager=saveSlotMenu)
saveSlot3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 370), (280, 85)), text="Save Slot 3", manager=saveSlotMenu)
saveSlot4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 480), (280, 85)), text="Save Slot 4", manager=saveSlotMenu)

# load slot menu
loadSlotMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
returnToMainMenu2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=loadSlotMenu)
loadSlot1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 250), (280, 85)), text="Load Slot 1", manager=loadSlotMenu)
loadSlot2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 360), (280, 85)), text="Load Slot 2", manager=loadSlotMenu)
loadSlot3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 470), (280, 85)), text="Load Slot 3", manager=loadSlotMenu)
loadSlot4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-115, 580), (280, 85)), text="Load Slot 4", manager=loadSlotMenu)

# stats gui
statsPage = pygame_gui.UIManager((WIDTH, HEIGHT))
statsLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2 - 200, 50), (200, 100)),text="Statistics", manager=statsPage)
returnToMainMenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=statsPage)
playerWins = pygame_gui.elements.UITextBox("test str", pygame.Rect((200, 200),(100, 40)), manager=statsPage)
playerLosses = pygame_gui.elements.UITextBox("test str", pygame.Rect((200, 260),(100, 40)), manager=statsPage)

# game variables menu
gameVarMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
returnToSaveSlotMenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=gameVarMenu)
playersNumber = pygame_gui.elements.UIDropDownMenu(["2","3","4"], "2", pygame.Rect((150, 150), (100, 50)), manager=gameVarMenu)
players = 2
playersNumberLabel = pygame_gui.elements.UILabel(pygame.Rect((20, 115), (200, 100)),text="Players", manager=gameVarMenu)
startGameButton1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2, HEIGHT/2-100), (100, 25)), text="Start Game", manager=gameVarMenu)

# character select menu
charSelectMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
returnToGameVariablesMenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=charSelectMenu)
charsRemaining = ["teenager", "doctor", "popstar", "athlete"]
char = "teenager"
selectedChars = []
characters = pygame_gui.elements.UIDropDownMenu(charsRemaining, "teenager", pygame.Rect((150, 150), (100, 50)), manager=charSelectMenu)
scImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "characters", "teenagerCard.jpg"))
charCard = pygame_gui.elements.UIImage(pygame.Rect((WIDTH/2,120), (600, 400)), scImg, manager=charSelectMenu)
startGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-50, HEIGHT-100), (100, 25)), text="Start Game", manager=charSelectMenu)
selectCharButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2-50, HEIGHT-50), (100, 25)), text="Select Character", manager=charSelectMenu)

# in game gui
gameboard = pygame_gui.UIManager((WIDTH, HEIGHT))
exitGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Exit game", manager=gameboard)

def saveGame(slot):
    f = open(f'TinyEpicZombies/jsonfiles/saves/save{slot}.json', 'w')
    saveData = gm.serialize()
    json.dump(saveData, f, indent=4)

def loadGame(slot):
    f = open(f'TinyEpicZombies/jsonfiles/saves/save{slot}.json', 'r')
    saveData = json.load(f)
    global gm
    del gm
    GameManager.deserialize(saveData)
    gm = GameManager.getInstance()

# win screen
winScreen = pygame_gui.UIManager((WIDTH, HEIGHT))
winBgImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "winScreen.jpg"))
winBgImg = pygame.transform.scale(winBgImg, (WIDTH, HEIGHT))
winBg = pygame_gui.elements.UIImage(pygame.Rect((0,0), (WIDTH, HEIGHT)), winBgImg, manager=winScreen)
pwImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "text", "playersWin.png"))
pwImg = pygame.transform.scale(pwImg, (400, 200))
pwText = pygame_gui.elements.UIImage(pygame.Rect((WIDTH/2 - 300, 80), (700, 200)), pwImg, manager=winScreen)
returnToMainMenu4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=winScreen)

# lose screen
loseScreen = pygame_gui.UIManager((WIDTH, HEIGHT))
loseBgImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "loseScreen.jpg"))
loseBgImg = pygame.transform.scale(loseBgImg, (WIDTH, HEIGHT))
loseBg = pygame_gui.elements.UIImage(pygame.Rect((0,0), (WIDTH, HEIGHT)), loseBgImg, manager=loseScreen)
plImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "text", "zombiesWin.png"))
plImg = pygame.transform.scale(plImg, (400, 200))
plText = pygame_gui.elements.UIImage(pygame.Rect((WIDTH/2 - 300, 80), (700, 200)), plImg, manager=loseScreen)
returnToMainMenu3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Back", manager=loseScreen)

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
            if gm.getWin() == True:
                addWin(id)
                manager = winScreen
            elif gm.getWin() == False:
                addLoss(id)
                manager = loseScreen
        else:
            gm.renderGameScreen()

    for event in pygame.event.get():

        if event.type == QUIT:
            saveGame(1)
            print("Game Saved")
            run = False

        elif event.type == pygame.KEYUP:
            gm.onKeyPress(event.key)

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if manager == gameboard:
                gm.onClick(pos)

        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == playersNumber:
                    players = int(event.text)
                elif event.ui_element == characters :
                    char = event.text
                    charCard.kill()
                    scImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "characters", f"{char}Card.jpg"))
                    charCard = pygame_gui.elements.UIImage(pygame.Rect((WIDTH/2,120), (600, 400)), scImg, manager=charSelectMenu)

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

            # elif event.ui_element == testButton:
            #     print(id)
            #     addLoss(id)
            elif event.ui_element == logoutButton: # returns to login screen
                manager = loggedOut
            elif event.ui_element == returnToLoggedOutButton or event.ui_element == returnToLoggedOutButton1:
                manager = loggedOut
            elif event.ui_element == startGameButton:# or event.ui_element == startGameButton2: # proceed to game board screen
                gm.initGame(selectedChars)
                manager = gameboard
            elif event.ui_element == exitGameButton or event.ui_element == returnToMainMenu or event.ui_element == returnToMainMenu1 or event.ui_element == returnToMainMenu2 or event.ui_element == returnToMainMenu3 or event.ui_element == returnToMainMenu4: # exit game to main menu
                manager = mainMenu
            elif event.ui_element == startLoginButton: # proceed to login page
                manager = login_page
            elif event.ui_element == startSignupButton: # proceed to signup page
                manager = signup_page
            elif event.ui_element == newGameButton or event.ui_element == returnToSaveSlotMenu:
                manager = saveSlotMenu
            elif event.ui_element == loadGameButton:
                manager = loadSlotMenu
            elif event.ui_element == saveSlot1 or event.ui_element == returnToGameVariablesMenu:
                manager = gameVarMenu
                slot = 1
            elif event.ui_element == saveSlot2:
                manager = gameVarMenu
                slot = 2
            elif event.ui_element == saveSlot3:
                manager = gameVarMenu
                slot = 3
            elif event.ui_element == saveSlot4:
                manager = gameVarMenu
                slot = 4
            elif event.ui_element == loadSlot1:
                loadGame(1)
                manager = gameboard
            elif event.ui_element == loadSlot2:
                loadGame(2)
                manager = gameboard
            elif event.ui_element == loadSlot3:
                loadGame(3)
                manager = gameboard
            elif event.ui_element == loadSlot4:
                loadGame(4)
                manager = gameboard
            elif event.ui_element == startGameButton1:
                manager = charSelectMenu
            elif event.ui_element == statsButton:
                stats = fetchStatistics(id)
                wins = stats[0]
                losses = stats[1]
                playerWins.set_text(f"Wins: {wins}")
                playerLosses.set_text(f"Losses: {losses}")
                manager = statsPage
            elif event.ui_element == selectCharButton:
                charsRemaining.remove(char)
                selectedChars.append(char)
                characters.kill()
                charCard.kill()
                if len(charsRemaining) == 4-players:
                    selectCharButton.disable()
                else:
                    characters = pygame_gui.elements.UIDropDownMenu(charsRemaining, charsRemaining[0], pygame.Rect((150, 150), (100, 50)), manager=charSelectMenu)
                    char = charsRemaining[0]
                    scImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "characters", f"{charsRemaining[0]}Card.jpg"))
                    charCard = pygame_gui.elements.UIImage(pygame.Rect((WIDTH/2,120), (600, 400)), scImg, manager=charSelectMenu)

        manager.process_events(event)
    
    manager.update(time_delta)
    

    manager.draw_ui(DISPLAY)

    pygame.display.update()

pygame.quit()