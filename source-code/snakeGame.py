# Snake Game! 

# Game Imports
import pygame, sys, random, time

check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors))
    sys.exit(-1)    
else:
    print("(+) Pygame successfully initialized!")

# Player Surface
playSurface = pygame.display.set_mode( (720, 460))

# Changing the window title
pygame.display.set_caption("Snake Game!")

# Colors
red   = pygame.Color(255, 0, 0)     # Game over
green = pygame.Color(0, 255, 0)     # Snake
black = pygame.Color(0, 0, 0)       # Score
white = pygame.Color(255, 255, 255) # Background
brown = pygame.Color(165, 42, 42)   # Food

# FPS(Frames Per Second) Controller
fpsController = pygame.time.Clock()

#Important Variables
snakePosition = [100, 50]
snakeBody = [[100, 50], [90, 50], [80, 50]]

foodPosition = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
foodSpawn = True

# If True, then snake will no die when hit the edge of the map
# Else, it will
wrap = False

# Starting direction
direction = "RIGHT"
changeto = direction

score = 0

# Game Over Function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    gameOverSurface = myFont.render('Game Over!', True, red) # Three args: ('text', anti-aliasing, color)
    gameOverRect = gameOverSurface.get_rect() # Give a position to gameOverSurface
    gameOverRect.midtop = (360, 15)
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
        scoreRect.midtop = (360, 120)
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
    return score, foodSpawn


# Ends the game if the snake moves off the board
def wrapOff(snakePosition):
    if snakePosition[0] > 710 or snakePosition[0] < 0:
        gameOver()
    if snakePosition[1] > 450 or snakePosition[1] < 0:
        gameOver()

# Moves the snake to the other side of the board
def wrapOn(snakePosition):
    if snakePosition[0] > 710:
        snakePosition[0] = 10
    if snakePosition[0] < 0:
        snakePosition[0] = 700
    if snakePosition[1] > 450:
        snakePosition[1] = 10      
    if snakePosition[1] < 0:
        snakePosition[1] = 440

# Main Logic of the Game
while True:
    for event in pygame.event.get():
        changeto = eventLogic(event, changeto)

    direction = validateDirection(changeto, direction)
    snakePosition = changeDirection(direction, snakePosition)
    score, foodSpawn = snakeBodyMechanism(snakeBody, snakePosition, foodPosition, score, foodSpawn)
    
    # Spawns the food on the Background
    if foodSpawn == False:
        foodPosition = [random.randrange(1, 72)*10, random.randrange(1, 46)*10]
        foodSpawn = True
    
    # Graphics of the Game
    # Background
    playSurface.fill(white)
    
    # Drawing Snake
    for position in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(position[0], position[1], 10, 10))
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPosition[0], foodPosition[1], 10, 10))
    
    if(wrap == True):
        wrapOn(snakePosition)
    else:
        wrapOff(snakePosition)
    
    for block in snakeBody[1:]:
        if snakePosition[0] == block[0] and snakePosition[1] == block[1]:
            gameOver()
    
    showScore()
    pygame.display.update()
    fpsController.tick(23) # Frame Rate Control
