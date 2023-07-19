# Import
import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time


# Initialize
pygame.init()
pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Pop")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

def Bchoice():
    li=["blue.png","green.png","orange.png","purple.png","red.png","yellow.png"]
    return pygame.image.load(random.choice(li)).convert_alpha()


# Images
imgBalloon = Bchoice()
balloon=pygame.image.load("balloon.jpg").convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 500, 300

# Variables
speed = 15
score = 0
startTime = time.time()
totalTime = 30

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


def resetBalloon():
    rectBalloon.x = random.randint(100, img.shape[1] - 100)
    rectBalloon.y = img.shape[0] + 50



# Main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    timeRemain = int(totalTime -(time.time()-startTime))
    if timeRemain <0:
        window.fill((255,255,255))
        window.blit(balloon,(10,20))
        window.blit(balloon,(img.shape[1]-500,20))
        font = pygame.font.Font(None, 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time UP', True, (50, 50, 255))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (530, 275))

    else:
        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        rectBalloon.y -= speed  # Move the balloon up
        # check if balloon has reached the top without pop
        if rectBalloon.y < -250:
            imgBalloon=Bchoice()
            resetBalloon()
            speed += 1

        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8]
            if rectBalloon.collidepoint(x, y):
                imgBalloon=Bchoice()
                resetBalloon()
                score += 10
                speed += 1

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(imgBalloon, rectBalloon)

        font = pygame.font.Font(None, 50)
        textScore = font.render(f'Score: {score}', True, (255, 50, 50))
        textTime = font.render(f'Time: {timeRemain}', True, (255, 50, 50))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1000, 35))


    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)
# TroubleShooting
# If you are using the latest version of CVZone and face the following error


# Then change the code

# x,y = hand[‘lmList’][8]

# to

# x,y = hand[‘lmList’][8][0:2]

# This is because the newer versions of CVZone have the x, y, and z coordinates. In this example, we only need x and y. So we will use [0:2] to extract the first two elements, which are x and y.

# The code will look like this

