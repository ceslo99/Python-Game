import pygame, sys, random, time
from pygame.locals import *
pygame.init()

# Creates size of screen
windowSize= [640,480]
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

blue = pygame.color.Color('#0a32f4')
red = pygame.color.Color('#ff0000')
yellow = pygame.color.Color('#ffff00')
black = pygame.color.Color('#000000')
white = pygame.color.Color('#ffffff')
half_black = pygame.color.Color('#000000cc')

#loads player image by using variable
player = pygame.image.load("mario.png")
#changes the size
player = pygame.transform.scale(player, (30,45))

#.get_rect gets baasically the position of the image
pos = player.get_rect()

#this is a list and saved the number 320 and 240
pos.center = [320,240]

#font
basicFont = pygame.font.Font('freesansbold.ttf', 32)

# Text
gameOverSurf = basicFont.render("You survived:", True, white)
gameOverRect = gameOverSurf.get_rect()
gameOverRect.center = (320, 130)

maxStars = 6


def main():
    #grabs the position 0 from the list pos and stores it in x which is 320
    playerx = pos.center[0]
    playery = pos.center[1]
    while True:
        runGame()


def runGame():

    
    
    global stars
    
    #starting player position
    playerx = (windowSize[0]/2)-40
    playery = 410

    pos.center = [playerx,playery]


    


    #list to hold star object
    stars = []

    # clock
    start = time.time()
    time.clock()
    elapsed = 0
    
    
    while True:

        # Create clock object
        clockSurf = basicFont.render(getTime(start, elapsed), True, white)
        clockRect = clockSurf.get_rect()
        clockRect.center = (320, 20)
        screen.fill(black)
        
        # Draw the floor
        pygame.draw.rect(screen, blue, [0, 440, windowSize[0], 40])

		
        # move falling stars
        for fsObj in stars:
            fsObj['y'] += fsObj['fallingVelocity']
            fsObj['rect'] = pygame.Rect((fsObj['x'], fsObj['y'], fsObj['width'], fsObj['height']))
			
        # draw falling stars
        drawStars()
		
        # remove off screen stars
        for i in range(len(stars) - 1, -1, -1):
            if stars[i]['y'] > 480:
                del stars[i]
		
        # add falling stars to list stars
        if len(stars) < maxStars:
            stars.append(createFallingStar())
  
        keys = pygame.key.get_pressed()
        

        if keys[K_a] or keys[K_LEFT]:
            playerx -= 10
        if keys[K_d] or keys[K_RIGHT]:
            playerx += 10

        if playerx + 40< 0:
            playerx = 500
        elif playerx > 600:
            playerx = 10

        pos.center = [playerx,playery]
        #sets up the screen with the image stored in player and in location of pos
        screen.blit(player, pos)
        #pygame.display.flip()
       # player = pygame.draw.rect(screen, red, [playerx, playery, 80, 40])
        

        # draw clock
        screen.blit(clockSurf, clockRect)

        # check if player collides with a star
        for i in range(len(stars) -1, -1, -1):
            star = stars[i]
            if pos.colliderect(star['rect']):
                print("hit", pygame.time.get_ticks()*.001)
                endScreen(start, elapsed)
                return
            
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
        pygame.display.flip()
        clock.tick(60)
def endScreen(start, elapsed):
    # Fonts
    smallFont = pygame.font.Font('freesansbold.ttf', 16)
    largeFont = pygame.font.Font('freesansbold.ttf', 128)
    
    # Transparent overlay
    coverFill = pygame.Surface((640,480), pygame.SRCALPHA, 32)
    coverFill.fill(half_black)
    screen.blit(coverFill, (0,0))
    
    # Text
    endClockSurf = largeFont.render(getTime(start, elapsed), True, white)
    endClockRect = gameOverSurf.get_rect()
    endClockRect.center = (260, 160)
    
    gameOverSurf2 = smallFont.render("Press R to restart", True, white)
    gameOverRect2 = gameOverSurf.get_rect()
    gameOverRect2.center = (360, 380)
    
    # draw the text
    screen.blit(gameOverSurf, gameOverRect)
    screen.blit(gameOverSurf2, gameOverRect2)
    screen.blit(endClockSurf, endClockRect)
    pygame.display.flip()

    while True:	
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == pygame.K_r:
                    return
        clock.tick(60)

def getTime(start, elapsed):
    seconds = int(time.time() - start)
    struct_time = time.gmtime(seconds)
    return time.strftime("%M:%S", struct_time)

def createFallingStar():
    fs = {}
    randomSize = random.randint(30,40)
    fs['width'] = randomSize
    fs['height'] = randomSize
    fs['x'] = random.randint(0,600)
    fs['y'] = (-40)
    fs['fallingVelocity'] = random.randint(7, 13)
    fs['rect'] = pygame.Rect((fs['x'], fs['y'], fs['width'], fs['height']))
    return fs

def drawStars():
    for fsObj in stars:
        pygame.draw.rect(screen, yellow, [fsObj['x'], fsObj['y'], fsObj['width'], fsObj['height']])

#function to close game
def terminate():
    pygame.quit()
    sys.exit()

if __name__== '__main__':
    main()
 
