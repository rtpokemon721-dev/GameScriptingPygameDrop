import pygame
import random
import sys
import time

pygame.init()

width = 800
height = 600
size = (width, height)

#time stuff
clock = pygame.time.Clock()
prev_time = time.time()
dt = 0
FPS = 60
TARGET_FPS = 60

black = (0,0,0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chicken Click Game")

thwomp = pygame.image.load("Thwomp.png")
powerUp = pygame.image.load("Mario_clock.png")

iterator = 0
numOfThwomps = 5
startX = []
startY = []
speed = []
powerUpTimer = 0

while iterator < numOfThwomps:
  startX.append(random.randint(0, width - thwomp.get_width() + 1))
  startY.append(0 - random.randint(thwomp.get_height(), thwomp.get_height() * 2))
  speed.append(2)
  iterator += 1

powerUpX = random.randint(0, width - powerUp.get_width() + 1)
powerUpY = (0 - random.randint(powerUp.get_height(), powerUp.get_height() * 2))
powerUpSpeed = 3
powerUpPressed  = False

replayscreen = False

bigfont = pygame.font.SysFont(None, 200)
playagaintext = bigfont.render("Play Again?", True, (0,200,0))
pax = width/2 - playagaintext.get_rect().width/2

smallfont = pygame.font.SysFont(None, 100)
yestext = smallfont.render("YES", True, (0, 200, 0))
yesx = width/4 - yestext.get_rect().width/2
notext = smallfont.render("NO", True, (0,200,0))
nox = width - width/4 - yestext.get_rect().width/2

#gameloop

gameover = False
while gameover == False:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover == True
    
    #On mouse click
    if pygame.mouse.get_pressed()[0]:
        coords = pygame.mouse.get_pos()
        if replayscreen == False:
            iterator = 0 
            while iterator < numOfThwomps:
                if coords[0] >= startX[iterator] and coords[0] <= startX[iterator] + thwomp.get_width() and coords[1] > startY[iterator] and coords[1] < startY[iterator] + thwomp.get_height():
                    startX[iterator] =  random.randint(0, width - thwomp.get_width() + 1)
                    startY[iterator] = 0 - random.randint(thwomp.get_height(), thwomp.get_height() * 2)
                    break
                iterator += 1
            
        if coords[0] >= powerUpX and coords[0] <= powerUpX + powerUp.get_width() and coords[1] > powerUpY and coords[1] < powerUpY + powerUp.get_height():
            iterator = 0
            powerUpX =  random.randint(0, width - powerUp.get_width() + 1)
            powerUpY = 0 - random.randint(powerUp.get_height(), powerUp.get_height() * 2)
            powerUpSpeed = 3
            powerUpTimer = 0
            #powerUpPressed = True
            while iterator < numOfThwomps:
                speed[iterator] = speed[iterator] * 2
                iterator += 1
            iterator = 0
        else:
            if coords[0] > yesx and coords[0] < yesx + yestext.get_rect().width and coords[1] > 450 and coords[1] < 450 + yestext.get_rect().height:
                iterator = 0
                while iterator < numOfThwomps:
                    startX[iterator] =  random.randint(0, width - thwomp.get_width() + 1)
                    startY[iterator] = 0 - random.randint(thwomp.get_height(), thwomp.get_height() * 2)
                    speed[iterator] = 2
                    iterator +=1
                replayscreen = False
                powerUpTimer = 0
                powerUpX =  random.randint(0, width - powerUp.get_width() + 1)
                powerUpY = 0 - random.randint(powerUp.get_height(), powerUp.get_height() * 2)


            if coords[0] > nox and coords[0] < nox + notext.get_rect().width and coords[1] > 450 and coords[1] < 450 + notext.get_rect().height:
                gameover = True

    #Update
    if replayscreen == False:
        #compute delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now        
        
        iterator = 0
        powerUpTimer += 1 * dt
        durationTimer = 0 
        #Game Over
        while iterator < numOfThwomps:
            if startY[iterator] + thwomp.get_height() > height:
                replayscreen = True
                break 
            startY[iterator] += speed[iterator]
            iterator += 1
        iterator = 0
        #PowerUp gets reset when missed
        if powerUpY + powerUp.get_height() > height:
            powerUpX = random.randint(0, width - powerUp.get_width() + 1)
            powerUpY = 0 - random.randint(powerUp.get_height(), powerUp.get_height() * 2)
            powerUpTimer = 0
            
        #if power up timer is greater than 10 it'll start falling
        if powerUpTimer > 10 and powerUpPressed == False:
            powerUpY += powerUpSpeed
        #while powerUpPressed == True:
        #    durationTimer += 1 * dt
        #    if durationTimer > 10:
        #        powerUpPressed == False
        #        durationTimer = 0

    #Drawing
    if replayscreen == False:
        screen.fill(black)
        iterator = 0
        while iterator < numOfThwomps:
            screen.blit(thwomp, (startX[iterator], startY[iterator]))
            iterator += 1
        iterator = 0
        screen.blit(powerUp, (powerUpX, powerUpY))
    else:
        screen.fill((200, 0,0))

        screen.blit(playagaintext, (pax, 150))
        screen.blit(yestext, (yesx, 450))
        screen.blit(notext, (nox, 450))   

    pygame.display.flip()
pygame.display.quit()
