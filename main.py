#############
# imports
#############
import cv2
import pygame
from HandDetector import HandDetector

############
# Global things
###########
# Define the size of the game window
WIDTH = 640
HEIGHT = 480
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("OpenCV")

WHITE = (255,255,255)
BLACK = (0,0,0)

BACKGROUND = (240,240,240)
background1 = pygame.image.load("assets/background.jpg")
background1 = pygame.transform.scale(background1, (840,680))


#########
# Function definitions
#########
def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)


#########
# main function
#########
def main():
    state = 0
    mode = 0
    run = True
    pygame.font.init()
    defaultFont = pygame.font.SysFont("ariel",50)

    while run:
        if state == 0:

            gameTitle = pygame.image.load("assets/title.png")
            gameTitle = pygame.transform.scale(gameTitle, (400,200))
            playButton = pygame.image.load("assets/button.png")
            playButton = pygame.transform.scale(playButton, (400,300))
            helpButton = pygame.image.load("assets/help.png")
            helpButton = pygame.transform.scale(helpButton, (270,170))
            
            WINDOW.fill(BACKGROUND)
            WINDOW.blit(background1, (0, -90))
            WINDOW.blit(WINDOW, (0,0))

            WINDOW.blit(gameTitle, (WIDTH/2 - gameTitle.get_width()/2, 0))
            WINDOW.blit(playButton, (WIDTH/2 - playButton.get_width()/2, 150))
            WINDOW.blit(helpButton, (WIDTH - helpButton.get_width() + 20, 100))


            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
                    
            keysPressed = pygame.key.get_pressed()
            if keysPressed[pygame.K_SPACE] == True:
                state = 2

            if keysPressed[pygame.K_h] == True:
                state = 1


        elif state == 1:
            WINDOW.fill(BACKGROUND)
            WINDOW.blit(background1, (0, -90))
            WINDOW.blit(WINDOW, (0,0))

            howToPlayTitle = pygame.image.load("assets/how2play.png")
            howToPlayTitle = pygame.transform.scale(howToPlayTitle, (500,150))
            howToPlay = pygame.image.load("assets/howToPLay.png")
            howToPlay = pygame.transform.scale(howToPlay, (550,350))

            WINDOW.blit(howToPlayTitle, (WIDTH/2 - howToPlayTitle.get_width()/2, 0))
            WINDOW.blit(howToPlay, (WIDTH/2 - howToPlay.get_width()/2, 125))


            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()

            keysPressed = pygame.key.get_pressed()
            if keysPressed[pygame.K_ESCAPE] == True:
                state = 0


        elif state == 2:
            # make a hand detector
            handDetector = HandDetector()

            # keeps track if pygame should keep running
            gameIsRunning = True

            # circle vars
            circleX = 0
            circleY = 0
            circleZ = 0
            circleColor = WHITE

            # rect vars
            clearColor = (100,100,100)
            drawColor = (0,0,0)
            eraserColor = (255,255,255)

            # keeps track of whether hand is open or closed
            handIsOpen = True

            # rectangle object
            clearButton = pygame.Rect(0,0, 100,75)
            drawButton = pygame.Rect(WIDTH/2 - 50 ,0,100,75)
            eraserButton = pygame.Rect(WIDTH - 100,0, 100,75)

            cursor = pygame.image.load("assets/cursor.png")
            cursor = pygame.transform.scale(cursor, (50,50))

            # fill the background
            WINDOW.fill(BACKGROUND)

            # while the opencv window is running
            while not handDetector.shouldClose and gameIsRunning:
                # update the webcam feed and hand tracker calculations
                handDetector.update()

                # draws rectangle on window
                pygame.draw.rect(WINDOW, clearColor, clearButton)
                pygame.draw.rect(WINDOW, drawColor, drawButton)
                pygame.draw.rect(WINDOW, eraserColor, eraserButton)

                # if there is at least one hand seen, then
                # print out the landmark positions
                if len(handDetector.landmarkDictionary) > 0: 
                    #print(handDetector.landmarkDictionary[0])
                    circleX = handDetector.landmarkDictionary[0][8][0]
                    circleY = handDetector.landmarkDictionary[0][8][1]
                    circleZ = handDetector.landmarkDictionary[0][8][2]
                    circleZ = abs(circleZ)*5

                    # mirror circleX so that it is more intuitive
                    circleX = WIDTH - mapToNewRange(circleX, 0, 640, 0, WIDTH)
                    # map circleY to pygame window size
                    circleY = mapToNewRange(circleY, 0, 480, 0, HEIGHT)

                    
                    if mode == 0:
                        if handDetector.landmarkDictionary[0][8][1] < handDetector.landmarkDictionary[0][9][1] and handDetector.landmarkDictionary[0][12][1] > handDetector.landmarkDictionary[0][9][1]:
                            WINDOW.fill(BACKGROUND)
                            pygame.draw.rect(WINDOW, clearColor, clearButton)
                            pygame.draw.rect(WINDOW, drawColor, drawButton)
                            pygame.draw.rect(WINDOW, eraserColor, eraserButton)
                            WINDOW.blit(cursor, (circleX,circleY))
                    if mode == 1:
                        if handDetector.landmarkDictionary[0][8][1] < handDetector.landmarkDictionary[0][9][1] and handDetector.landmarkDictionary[0][12][1] > handDetector.landmarkDictionary[0][9][1]:
                            handIsOpen = True
                            circleColor = BLACK
                            pygame.draw.circle(WINDOW, circleColor, (circleX, circleY), 5)
                        
                    if mode == 2:
                        if handDetector.landmarkDictionary[0][8][1] < handDetector.landmarkDictionary[0][9][1] and handDetector.landmarkDictionary[0][12][1] > handDetector.landmarkDictionary[0][9][1]:
                            handIsOpen = True
                            circleColor = BACKGROUND
                            pygame.draw.circle(WINDOW, circleColor, (circleX, circleY), 20)
                        

                    # collsion circle and rect
                    if handDetector.landmarkDictionary[0][8][1] and handDetector.landmarkDictionary[0][12][1] < handDetector.landmarkDictionary[0][9][1]:
                        #WINDOW.blit(cursor, (circleX,circleY))
                        if clearButton.collidepoint(circleX, circleY):
                            WINDOW.fill(BACKGROUND)
                            pygame.draw.rect(WINDOW, clearColor, clearButton)
                            pygame.draw.rect(WINDOW, drawColor, drawButton)
                            pygame.draw.rect(WINDOW, eraserColor, eraserButton)
                            mode = 0

                        if drawButton.collidepoint(circleX, circleY):
                            
                            mode = 1
                            print(mode)

                        if eraserButton.collidepoint(circleX, circleY):
                            
                            mode = 2
                            print(mode)

                # for all the game events
                for event in pygame.event.get():
                    # if the game is exited out of, then stop running the game
                    if event.type == pygame.QUIT:
                        gameIsRunning = False
                        run = False

                # put code here that should be run every frame
                # of your game             
                pygame.display.update()

            # Closes all the frames
            cv2.destroyAllWindows()



if __name__ == "__main__":
    main()



