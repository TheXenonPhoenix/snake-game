# Snake Game! 

# Using some steps from this walkthrough
# https://pythonprogramming.net/placing-text-pygame-buttons/

# Game Imports
import pygame, sys, random, time

check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors))
    sys.exit(-1)    
else:
    print("(+) Pygame successfully initialized!")

# Player Surface
width = 720
height = 460
playSurface = pygame.display.set_mode( (width, height))

# Changing the window title
pygame.display.set_caption("Snake Game!")

# Colors
red   = pygame.Color(200, 0, 0)     # Game over
green = pygame.Color(0, 200, 0)     # Snake & Start
black = pygame.Color(0, 0, 0)       # Score & Quit
white = pygame.Color(255, 255, 255) # Background
brown = pygame.Color(165, 42, 42)   # Food
brightGreen = pygame.Color(0,255,0) # Select Start
brightRed = pygame.Color(255,0,0)   # Select Quit

# Snake
tempColor = green #pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))

# FPS(Frames Per Second) Controller
fpsController = pygame.time.Clock()

# Important Variables
snakePosition = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]

foodPosition = [random.randrange(1, width/10)*10, random.randrange(1, height/10)*10]
foodSpawn = True

# If True, then snake will no die when hit the edge of the map
# Else, it will
wrap = True

# Starting direction
direction = "RIGHT"
changeto = direction

score = 0

def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        playSurface.fill(white)
        myFont = pygame.font.SysFont('monaco', width/10)
        gameOverSurface = myFont.render('Welcome to Snake!', True, black) # Three args: ('text', anti-aliasing, color)
        gameOverRect = gameOverSurface.get_rect() # Give a position to gameOverSurface
        gameOverRect.midtop = (width/2, 15)
        playSurface.blit(gameOverSurface, gameOverRect)

        # Play button
        playButton = button('Go!', width/4, height/2, 100, 50, green, brightGreen, "Play")
        # Quit button
        quitButton = button('Quit', width*2/3, height/2, 100, 50, red, brightRed, "Quit")

        pygame.display.update()
        fpsController.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(playSurface, ac,(x,y,w,h))
        if click[0] == 1 and action != None: #if clicked on the button
            if action == "Play":
                print("something")#need to put play game here
            elif action == "Quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(playSurface, ic,(x,y,w,h))

    myFont = pygame.font.SysFont('monaco', width/25)
    text = myFont.render(msg, True, black)
    rect = text.get_rect()
    rect.center = ( (x+(w/2)), (y+(h/2)) )
    playSurface.blit(text, rect)

# Game Over Function
def gameOver():
    myFont = pygame.font.SysFont('monaco', width/10)
    gameOverSurface = myFont.render('Game Over!', True, red) # Three args: ('text', anti-aliasing, color)
    gameOverRect = gameOverSurface.get_rect() # Give a position to gameOverSurface
    gameOverRect.midtop = (width/2, 15)
    playSurface.blit(gameOverSurface, gameOverRect)
    showScore(0)
    pygame.display.update() # Update the Screen
    time.sleep(4)
    pygame.quit() # pygame exit
    sys.exit() # Console exit

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

def updateFood(foodSpawn, foodPosition):
    # Spawns the food on the Background
    if foodSpawn == False:
        foodPosition = [random.randrange(1, width/10)*10, random.randrange(1, height/10)*10]
        foodSpawn = True
    return foodSpawn, foodPosition

# Draws the Graphics of the Game
def draw():
    # Background
    playSurface.fill(white)
    
    # Drawing Snake
    for position in snakeBody:
        pygame.draw.rect(playSurface, tempColor, pygame.Rect(position[0], position[1], 10, 10))
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPosition[0], foodPosition[1], 10, 10))
        
    if(wrap == True):
        wrapOn(snakePosition)
    else:
        wrapOff(snakePosition)

# Ends the game if the snake moves off the board
def wrapOff(snakePosition):
    if snakePosition[0] > width - 10 or snakePosition[0] < 0:
        gameOver()
    if snakePosition[1] > height -10 or snakePosition[1] < 0:
        gameOver()

# Moves the snake to the other side of the board
def wrapOn(snakePosition):
    if snakePosition[0] > width - 10:
        snakePosition[0] = 0
    if snakePosition[0] < 0:
        snakePosition[0] = width - 10
    if snakePosition[1] > height - 10:
        snakePosition[1] = 0      
    if snakePosition[1] < 0:
        snakePosition[1] = height - 10

#gameIntro()
# Main Logic of the Game
#def playGame():
playing = True
while playing:
    for event in pygame.event.get():
        changeto = eventLogic(event, changeto)

    direction = validateDirection(changeto, direction)
    snakePosition = changeDirection(direction, snakePosition)
    score, foodSpawn = snakeBodyMechanism(snakeBody, snakePosition, foodPosition, score, foodSpawn)
    foodSpawn, foodPosition = updateFood(foodSpawn, foodPosition)

    draw()
    
    showScore()
    pygame.display.update()
    fpsController.tick(23) # Frame Rate Control