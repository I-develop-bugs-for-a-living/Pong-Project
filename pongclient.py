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

# change this to change the speed of the ball
ballSpeed = 6
basic_font = pygame.font.Font('freesansbold.ttf', 32)


class Game():
    def __init__(self, ball) -> None:
        print("Game initialized")
        self.ball = ball
        self.scorePlayer1 = 0
        self.scorePlayer2 = 0
    
    def check(self, player, player2):
        self.collision(player, player2)
        self.scoring()
        self.displayScore()

    # if player and ball collide, reverse xdirection
    def collision(self, player1, player2):
        if player1.paddel.colliderect(self.ball.ball):
            self.ball.directionX = 1
            theta = abs(player1.paddel.centery - self.ball.ball.centery) / 70 * 2
            speed = math.sqrt(((1+theta**2)/ballSpeed**2)**-1)
            self.ball.speed_x = speed
            self.ball.speed_y = speed * theta
            if player1.paddel.centery - self.ball.ball.centery > 0:
                self.ball.directionY = -1
            else:
                self.ball.directionY = 1
        if player2.paddel.colliderect(self.ball.ball):
            self.ball.directionX = -1
            theta = abs(player2.paddel.centery - self.ball.ball.centery) / 70 * 2
            speed = math.sqrt(((1+theta**2)/ballSpeed**2)**-1)
            self.ball.speed_x = speed
            self.ball.speed_y = speed * theta
            if player2.paddel.centery - self.ball.ball.centery > 0:
                self.ball.directionY = -1
            else:
                self.ball.directionY = 1
    
    # if ball hits left or right hits left or right border, increment scoring counter
    def scoring(self):
        if self.ball.ball.left <= 0:
            self.ball.reset()
            self.scorePlayer1 += 1

        if self.ball.ball.right >= scaledWidth:
            self.ball.reset()
            self.scorePlayer2 += 1

    # draw Score on the canvas
    def displayScore(self):
        player1Score = basic_font.render(str(self.scorePlayer1), True, scoreColor)
        player2Score = basic_font.render(str(self.scorePlayer2), True, scoreColor)

        player2ScoreRect = player1Score.get_rect(midright = (scaledWidth / 2 - 40, 40))
        player1ScoreRect = player2Score.get_rect(midleft = (scaledWidth / 2 + 40, 40))

        screen.blit(player1Score, player1ScoreRect)
        screen.blit(player2Score, player2ScoreRect)

def redrawWindow(win, player, player2, ball, game):
    win.fill(backroundColor)
    ball.update(screen)
    player.draw(win)
    player2.draw(win)
    game.check(player, player2)
    pygame.display.update()

# Ball
ball = Ball(ballSpeed)

# Game
game = Game(ball)

n = Network()
p = n.getP()[0]

# Gameloop
while True:
    clock.tick(60)
    
    # Controls
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    
    receive = n.send(p, ball, game.scorePlayer1, game.scorePlayer2)
    p2 = receive[0]
    p.move()

    redrawWindow(screen, p, p2, ball, game)

