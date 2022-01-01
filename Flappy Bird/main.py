import time
import pygame
from pygame.locals import *
import random
import sys
import os

FPS = 40
SCREENWIDTH = 390
SCREENNHEIGHT = 610
# SCREENWIDTH = 290
# SCREENNHEIGHT = 510
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENNHEIGHT))
GROUNDY = SCREENNHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER0 = 'G:\\Python\\Flappy Bird\\gallery\\sprites\\bird.png'
PLAYER1 = 'G:\\Python\\Flappy Bird\\gallery\\sprites\\bird.png'
PIPE = 'G:\\Python\\Flappy Bird\\gallery\\sprites\\pipe.png'
BACKGROUND = 'G:\\Python\\Flappy Bird\\gallery\\sprites\\background.png'
file_Path = os.listdir('G:\\Python\\Flappy Bird\\gallery\\sprites\\bird')


def welcome_Screen():
    playerx = int((SCREENWIDTH/5)-20)
    playery = int((SCREENNHEIGHT - GAME_SPRITES['player0'].get_height())/1.8)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENNHEIGHT * 0.08)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player0'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def main_Game():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    new_Pipe1 = getRandomPipe()
    new_Pipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': new_Pipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_Pipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': new_Pipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_Pipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = 1
    playerMaxVelY = 50
    playerMinVelY = -8
    playerAccY = 1

    playerFlappeAccV = -9
    playerFlapped = False

    while True:
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        rotateAngl = 0
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlappeAccV
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
                    rotateAngl = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    rotateAngl = 25
        for i in range(0, len(file_Path)):
            SCREEN.blit(pygame.transform.rotozoom(
                GAME_SPRITES[f'player{i}'], rotateAngl, 1),  (playerx, playery))
        crashTest = isCollied(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + GAME_SPRITES['player0'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your Score is {score}")
                GAME_SOUNDS['point'].play()
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player0'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (lowerPipe['x'], lowerPipe['y']))

        # print(f"\nPlayer Y = {playery}")
        # SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        # SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        myDigit = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigit:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xOffSet = (SCREENWIDTH - width) / 2
        for digit in myDigit:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (xOffSet, SCREENNHEIGHT * 0.12))
            xOffSet += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollied(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 40 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][1].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player0'].get_height()) > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENNHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENNHEIGHT -
                                          GAME_SPRITES['base'].get_height() - 1.2 * offset))
    y1 = pipeHeight - y2 + offset
    pipeX = SCREENWIDTH + 10
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird By Abdul-Mannan')

    # Game Images
    GAME_SPRITES['numbers'] = (
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\0.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\1.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\2.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\3.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\4.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\5.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\6.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\7.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\8.png').convert_alpha(),
        pygame.image.load('G:\\Python\\Flappy Bird\\gallery\\sprites\\9.png').convert_alpha(),3
    )
    GAME_SPRITES['message'] = pygame.image.load(
        'G:\\Python\\Flappy Bird\\gallery\\sprites\\message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        'G:\\Python\\Flappy Bird\\gallery\\sprites\\base.png').convert_alpha()
    GAME_SPRITES['gameOver'] = pygame.image.load(
        'G:\\Python\\Flappy Bird\\gallery\\sprites\\gameOver.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.image.load(PIPE).convert_alpha(),
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180)
    )

    # Game Sounds
    GAME_SOUNDS['hit'] = pygame.mixer.Sound(
        'G:\\Python\\Flappy Bird\\gallery\\audio\\hit.wav')
    GAME_SOUNDS['die'] = pygame.mixer.Sound(
        'G:\\Python\\Flappy Bird\\gallery\\audio\\die.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound(
        'G:\\Python\\Flappy Bird\\gallery\\audio\\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(
        'G:\\Python\\Flappy Bird\\gallery\\audio\\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound(
        'G:\\Python\\Flappy Bird\\gallery\\audio\\wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player0'] = pygame.image.load(PLAYER0).convert_alpha()
    GAME_SPRITES['player1'] = pygame.image.load(PLAYER1).convert_alpha()
    # GAME_SPRITES['player0'] = pygame.image.load(PLAYER0).convert_alpha()

    while True:
        welcome_Screen()
        main_Game()
