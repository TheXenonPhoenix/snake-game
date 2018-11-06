# Snake Game! 

# Using some steps from this walkthrough
# https://pythonprogramming.net/pygame-python-3-part-1-intro/

# Game Imports
import pygame, sys, random, time
from os import path

#region pygame check
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors))
    sys.exit(-1)    
else:
    print("(+) Pygame successfully initialized!")
#endregion

# Loads the current scores from a file
def loadScore():
    with open("C:\Users\kp56156\Documents\SnakeGame\source-code\highScores.txt",'r') as scores:
        try:
            highscore = int(scores.read())
        except:
            highscore = 0
    return highscore

# Saves the current score to a file
def saveScore():
    with open("C:\Users\kp56156\Documents\SnakeGame\source-code\highScores.txt",'w') as scores:
        scores.write(str(int(score)) + "\n")

#region Variables
# Player Surface
width = 720
height = 460
playSurface = pygame.display.set_mode( (width, height))

# Changing the window title
pygame.display.set_caption("Snake Game!")

# Colors
red   = pygame.Color(200, 0, 0)         # Game over
green = pygame.Color(0, 200, 0)         # Snake & Start
black = pygame.Color(0, 0, 0)           # Score & Quit
white = pygame.Color(255, 255, 255)     # Background
grey = pygame.Color(150, 150, 150)      # Pause
brown = pygame.Color(165, 42, 42)       # Food
brightGreen = pygame.Color(0,255,0)     # Select Start
brightRed = pygame.Color(255,0,0)       # Select Quit
lightGrey = pygame.Color(200, 200, 200) # Pause

# Snake
tempColor = green #pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))

# FPS(Frames Per Second) Controller
fpsController = pygame.time.Clock()

# Important Variables
snakePosition = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]

# First Random spawn of food
foodPosition = [random.randrange(1, width/10)*10, random.randrange(4, height/10)*10]
foodSpawn = True

# If True, then snake will no die when hit the edge of the map
# Else, it will
wrap = True

# Starting direction
direction = "RIGHT"
changeto = direction

# Initial Score
score = 0
highscore = loadScore()

# Turns pause screen on/off
paused = False
#endregion

# Method to create buttons
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(playSurface, ac,(x,y,w,h))
        if click[0] == 1 and action != None: #if clicked on the button
            buttonActionHandler(action)
    else:
        pygame.draw.rect(playSurface, ic,(x,y,w,h))

    myFont = pygame.font.SysFont('monaco', width/25)
    text = myFont.render(msg, True, black)
    rect = text.get_rect()
    rect.center = ( (x+(w/2)), (y+(h/2)) )
    playSurface.blit(text, rect)

# Initalizes inital variables for resets
def initVariables(snakePosition, snakeBody, score, direction, changeto):
    snakePosition = [100, 50]
    snakeBody = [[100, 50], [90, 50], [80, 50]]
    score = 0
    direction = "RIGHT"
    changeto = direction
    return snakePosition, snakeBody, score, direction, changeto 

# Changes the current screen based on the action of the button
def buttonActionHandler(action):
    global snakePosition
    global snakeBody
    global score
    global paused
    global wrap
    global direction
    global changeto
    
    if action == "Play":
        snakePosition, snakeBody, score, direction, changeto = initVariables(snakePosition, snakeBody, score, direction, changeto) 
        wrap = True
        playGame()
    elif action == "Pause":
        pauseScreen()
    elif action == "Reset":
        # Resets variables to original
        snakePosition, snakeBody, score, direction, changeto = initVariables(snakePosition, snakeBody, score, direction, changeto) 
    elif action == "Wrap":    
        snakePosition, snakeBody, score, direction, changeto = initVariables(snakePosition, snakeBody, score, direction, changeto) 
        wrap = False
        playGame()
    elif action == "Home":
        gameIntro()
    elif action == "Resume":
        paused = False
        playGame()
    elif action == "Scores":
        scoresScreen()
    elif action == "Quit":
        pygame.quit()
        quit()

# Screen maker
def screenInfo(playSurface, pygame, text, textColor):
    playSurface.fill(white)
    myFont = pygame.font.SysFont('monaco', width/10)
    gameOverSurface = myFont.render(text, True, textColor) # Three args: ('text', anti-aliasing, color)
    gameOverRect = gameOverSurface.get_rect() # Give a position to gameOverSurface
    gameOverRect.midtop = (width/2, 15)
    playSurface.blit(gameOverSurface, gameOverRect)

# Intro Screen of game
def gameIntro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screenInfo(playSurface, pygame, 'Welcome to Snake!', black)

        # Play button
        button('Play: Wrap Off', width/4, height/2, 200, 50, green, brightGreen, "Wrap")
        # Wrap On button
        button('Play: Wrap On', width/4, height/2 + 100, 200, 50, green, brightGreen, "Play")
        # Quit button
        button('Quit', width*2/3, height/2, 100, 50, red, brightRed, "Quit")
        # Scores Button
        button('Scores', width*2/3, height/2 + 100, 100, 50, red, brightRed, "Scores")

        pygame.display.update()
        fpsController.tick(15)

# Main Logic of the Game
def playGame():
    global changeto
    global direction
    global snakePosition
    global foodPosition
    global score
    global foodSpawn

    while True:
        for event in pygame.event.get():
            changeto = eventLogic(event, changeto)

        direction = validateDirection(changeto, direction)
        snakePosition = changeDirection(direction, snakePosition)
        score, foodSpawn = snakeBodyMechanism(snakeBody, snakePosition, foodPosition, score, foodSpawn)
        foodSpawn, foodPosition = updateFood(foodSpawn, foodPosition)

        draw()

        pygame.display.update()
        fpsController.tick(23) # Frame Rate Control

# Screen to pause when playing
def pauseScreen():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screenInfo(playSurface, pygame, 'Paused', black)

        # Resume button
        button('Resume', width/4, height/2, 200, 50, green, brightGreen, "Resume")
        # Quit button
        button('Quit', width*2/3, height/2, 100, 50, red, brightRed, "Quit")

        pygame.display.update()
        fpsController.tick(15)

# Screen to display high scores
def scoresScreen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screenInfo(playSurface, pygame, 'High Score', black)

        # Home Button
        button('Home', width - 150, height - 80, 100, 50, green, brightGreen, "Home")

        myFont = pygame.font.SysFont('monaco', width/10)
        gameOverSurface = myFont.render(str(highscore), True, black) # Three args: ('text', anti-aliasing, color)
        gameOverRect = gameOverSurface.get_rect() # Give a position to gameOverSurface
        gameOverRect.midtop = (width/2, height/2)
        playSurface.blit(gameOverSurface, gameOverRect)

        pygame.display.update()
        fpsController.tick(15)

# Game Over Function
def gameOver():
    gameOver = True
    gameSaved = False
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screenInfo(playSurface, pygame, 'Game Over!', red)

        # Play button
        button('Home', width/4, height/2, 200, 50, green, brightGreen, "Home")
        # Quit button
        button('Quit', width*2/3, height/2, 100, 50, red, brightRed, "Quit")

        showScore(0)
        # Saves the score once
        if not gameSaved and score > highscore:
            saveScore()
            gameSaved = True

        pygame.display.update()
        fpsController.tick(15)

# Displays current score at top left of game screen
def showScore(choice = 1):
    scoreFont = pygame.font.SysFont('monaco', 24)
    scoreSurface = scoreFont.render('Score : {0}'.format(score), True, black)
    scoreRect = scoreSurface.get_rect()
    if choice == 1:
        scoreRect.midtop = (80, 10)
    else:
        scoreRect.midtop = (width/2, 120)
    playSurface.blit(scoreSurface, scoreRect)

# Checks the events of the game while its running
# Will either end the game or move the snake's direction
def eventLogic(event, changeto):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            changeto = 'RIGHT'
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            changeto = 'LEFT'
        if event.key == pygame.K_UP or event.key == ord('w'):
            changeto = 'UP'
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            changeto = 'DOWN'
        if event.key == pygame.K_ESCAPE:
            # post() is used to create an event
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    return changeto

# Validation of direction
def validateDirection(changeto, direction):
    if changeto == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeto == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeto == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeto == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
    return direction

# Changing values of x and y co-ordinate
def changeDirection(direction, snakePosition):
    if direction == 'RIGHT':
        snakePosition[0] += 10
    if direction == 'LEFT':
        snakePosition[0] -= 10
    if direction == 'UP':
        snakePosition[1] -= 10
    if direction == 'DOWN':
        snakePosition[1] += 10
    return snakePosition

# Handles the addition of new pieces of the snak
def snakeBodyMechanism(snakeBody, snakePosition, foodPosition, score, foodSpawn):
    snakeBody.insert(0, list(snakePosition))
    if snakePosition[0] == foodPosition[0] and snakePosition[1] == foodPosition[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    for block in snakeBody[1:]:
        if snakePosition[0] == block[0] and snakePosition[1] == block[1]:
            gameOver()
    return score, foodSpawn

# Spawns the food on the Background
def updateFood(foodSpawn, foodPosition):
    if foodSpawn == False:
        foodPosition = [random.randrange(1, width/10)*10, random.randrange(4, height/10)*10]
        foodSpawn = True
    return foodSpawn, foodPosition

# Draws the Graphics of the Game
def draw():
    playSurface.fill(white) # Background
    pygame.draw.rect(playSurface, green, (0, 0, width, 40), 1)
    
    for position in snakeBody: # Drawing Snake
        pygame.draw.rect(playSurface, tempColor, pygame.Rect(position[0], position[1], 10, 10))
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPosition[0], foodPosition[1], 10, 10))
        
    if(wrap == True):
        wrapOn(snakePosition)
    else:
        wrapOff(snakePosition)

    showScore()
    # Home Button
    button('Home', width - 300, 10, 80, 20, grey, lightGrey, "Home")
    # Reset Button
    button('Reset', width - 200, 10, 80, 20, grey, lightGrey, "Reset")
    # Pause Button
    button('Pause', width - 100, 10, 80, 20, grey, lightGrey, "Pause")

# Ends the game if the snake moves off the board
def wrapOff(snakePosition):
    if snakePosition[0] > width - 10 or snakePosition[0] < 0:
        gameOver()
    if snakePosition[1] > height -10 or snakePosition[1] < 40:
        gameOver()

# Moves the snake to the other side of the board
def wrapOn(snakePosition):
    # Controls movements right and left
    if snakePosition[0] > width - 10:
        snakePosition[0] = 0
    elif snakePosition[0] < 0:
        snakePosition[0] = width - 10
    # Contorls movements down and up
    if snakePosition[1] > height - 10:
        snakePosition[1] = 30
    elif snakePosition[1] < 40:
        snakePosition[1] = height - 10

# Run the game
gameIntro()

