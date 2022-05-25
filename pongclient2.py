import pygame, random
import math
from network import Network
from playerPong import Ball


# To add sound use pygame mixer

pygame.init()
clock = pygame.time.Clock()

screen_width = 1980
screen_height = 1080
scale = 0.5
scaledWidth = screen_width * scale
scaledHeight = screen_height * scale
screen = pygame.display.set_mode((int(scaledWidth), int(scaledHeight)))
pygame.display.set_caption('Fabis lustiges Pong')

# Change these 3 to set color for the game
# Background Color
backroundColor = pygame.Color('#000000')
# Ball and Paddel color
ligth_grey = (250, 250, 250)
# ScoreboardColor
scoreColor = (250, 250, 250)

scorep1 = 0
scorep2 = 0

# change this to change the speed of the ball
ballSpeed = 6
basic_font = pygame.font.Font('freesansbold.ttf', 32)

def redrawWindow(win, player, player2, ball, scp1, scp2):
    win.fill(backroundColor)
    player.draw(win)
    player2.draw(win)
    ball.draw(win)
    displayScore(scp1, scp2)
    pygame.display.update()

def displayScore(scorePlayer1, scorePlayer2):
    player1Score = basic_font.render(str(scorePlayer1), True, scoreColor)
    player2Score = basic_font.render(str(scorePlayer2), True, scoreColor)

    player2ScoreRect = player1Score.get_rect(midright = (scaledWidth / 2 - 40, 40))
    player1ScoreRect = player2Score.get_rect(midleft = (scaledWidth / 2 + 40, 40))

    screen.blit(player1Score, player1ScoreRect)
    screen.blit(player2Score, player2ScoreRect)

n = Network()
p = n.getP()[0]
ball1 = Ball(6)

# Gameloop
while True:
    clock.tick(60)
    
    # Controls
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
    receive = n.send(p, ball1, scorep1, scorep2)
    p2 = receive[0]
    ball = receive[1]
    scoreplayer1 = receive[2]
    scoreplayer2 = receive[3]


    p.move()

    redrawWindow(screen, p, p2, ball, scoreplayer1, scoreplayer2)