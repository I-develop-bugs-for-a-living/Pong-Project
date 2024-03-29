import pygame, random, sys
import math

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
# Item color
red = (250, 0, 0)
# ScoreboardColor
scoreColor = (250, 250, 250)

# change this to change the speed of the ball
ballSpeed = 6
basic_font = pygame.font.Font('freesansbold.ttf', 32)

class Player():
    def __init__(self, speed, width):
        self.speed = speed
        self.paddel = pygame.Rect(width, scaledHeight/2 - 70, 10, 140)
        self.movementy = 0
        self.movementx = 0
        self.width = width

    def collidesWithBorder(self):
        if self.paddel.top <= 0:
            self.paddel.top = 0
        if self.paddel.bottom >= scaledHeight:
            self.paddel.bottom = scaledHeight
        if self.paddel.right >= scaledWidth:
            self.paddel.right = scaledWidth
        if self.paddel.left <= 0:
            self.paddel.left = 0

    def draw(self):
        pygame.draw.rect(screen, ligth_grey, self.paddel)

    def update(self):
        self.draw()
        self.paddel.y += self.movementy * self.speed
        self.paddel.x += self.movementx * self.speed
        self.collidesWithBorder()

    def reset(self):
        self.paddel.x = self.width
        self.paddel.y = scaledHeight/2 - 70

class Ball():
    def __init__(self, speed):
        self.speed_x = math.sqrt((speed**2)/2)
        self.speed_y = math.sqrt((speed**2)/2)
        self.directionX = random.choice((-1, 1))
        self.directionY = random.choice((-1, 1))
        self.ball = pygame.Rect(scaledWidth/2 - 15, scaledHeight/2 - 15, 20, 20)

    def update(self):
        self.draw()
        self.ball.x += self.speed_x * self.directionX
        self.ball.y += self.speed_y * self.directionY
        self.collisions()

    def collisions(self):
        if self.ball.top <= 0 or self.ball.bottom >= scaledHeight:
            self.directionY *= -1

    def reset(self):
        self.directionX = random.choice((-1, 1))
        self.directionY = random.choice((-1, 1))
        self.speed_x = math.sqrt((ballSpeed**2)/2)
        self.speed_y = math.sqrt((ballSpeed**2)/2)
        self.ball.center = (scaledWidth/2, scaledHeight/2)

    def draw(self):
        pygame.draw.rect(screen, ligth_grey, self.ball)

class PowerUp():
    def __init__(self):
        self.box = pygame.Rect(200, 200, 50, 50)
        self.colors = [red, ligth_grey, red, red]
        self.tag = 0
        self.types = ["Speed", "Size", "Teleport"]

    def update(self):
        self.draw()

    def randomPosition(self):
        self.box.x = 20
        self.box.y = 20

    def draw(self):
        pygame.draw.rect(screen, self.color, self.box)
    

class Game():
    def __init__(self, player1, player2, ball, powerUp) -> None:
        self.player1 = player1
        self.player2 = player2
        self.ball = ball
        self.powerUp = powerUp
        self.scorePlayer1 = 0
        self.scorePlayer2 = 0
    
    def check(self):
        self.collision()
        self.scoring()
        self.displayScore()

    # if player and ball collide, reverse xdirection
    def collision(self):
        self.ballPowerUpCollision()
        if self.player1.paddel.colliderect(self.ball.ball):
            self.ball.directionX = 1
            theta = abs(self.player1.paddel.centery - self.ball.ball.centery) / 70 * 2
            speed = math.sqrt(((1+theta**2)/ballSpeed**2)**-1)
            self.ball.speed_x = speed
            self.ball.speed_y = speed * theta
            if self.player1.paddel.centery - self.ball.ball.centery > 0:
                self.ball.directionY = -1
            else:
                self.ball.directionY = 1
        if self.player2.paddel.colliderect(self.ball.ball):
            self.ball.directionX = -1
            theta = abs(self.player2.paddel.centery - self.ball.ball.centery) / 70 * 2
            speed = math.sqrt(((1+theta**2)/ballSpeed**2)**-1)
            self.ball.speed_x = speed
            self.ball.speed_y = speed * theta
            if self.player2.paddel.centery - self.ball.ball.centery > 0:
                self.ball.directionY = -1
            else:
                self.ball.directionY = 1
    
    def ballPowerUpCollision(self):
        if self.powerUp.box.colliderect(self.ball.ball):
            self.powerUp.randomPosition()
            if self.ball.directionX == -1:
                self.player2.speed *= 2
            if self.ball.directionX == 1:
                self.player1.speed *= 2
    
    # if ball hits left or right hits left or right border, increment scoring counter
    def scoring(self):
        if self.ball.ball.left <= 0:
            self.ball.reset()
            self.player1.reset()
            self.player2.reset()
            self.scorePlayer1 += 1

        if self.ball.ball.right >= scaledWidth:
            self.ball.reset()
            self.player1.reset()
            self.player2.reset()
            self.scorePlayer2 += 1

    # draw Score on the canvas
    def displayScore(self):
        player1Score = basic_font.render(str(self.scorePlayer1), True, scoreColor)
        player2Score = basic_font.render(str(self.scorePlayer2), True, scoreColor)

        player2ScoreRect = player1Score.get_rect(midright = (scaledWidth / 2 - 40, 40))
        player1ScoreRect = player2Score.get_rect(midleft = (scaledWidth / 2 + 40, 40))

        screen.blit(player1Score, player1ScoreRect)
        screen.blit(player2Score, player2ScoreRect)

# Players
players = []
player1 = Player(5, 20)
player2 = Player(5, scaledWidth - 20)
players.append(player1)
players.append(player2)

# Ball
ball = Ball(ballSpeed)

# PowerUp
powerup = PowerUp()

# Game
game = Game(player1, player2, ball, powerup)

# Gameloop
while True:
    # Controls
    for event in pygame.event.get():
        # Quit game with red x
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.movementy = -1
            if event.key == pygame.K_DOWN:
                player1.movementy = 1
            if event.key == pygame.K_LEFT:
                player1.movementx = -1
            if event.key == pygame.K_RIGHT:
                player1.movementx = 1
            

            if event.key == pygame.K_w:
                player2.movementy = -1
            if event.key == pygame.K_s:
                player2.movementy = 1
            if event.key == pygame.K_d:
                player2.movementx = 1
            if event.key == pygame.K_a:
                player2.movementx = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player1.movementy = 0
            if event.key == pygame.K_DOWN:
                player1.movementy = 0
            if event.key == pygame.K_LEFT:
                player1.movementx = 0
            if event.key == pygame.K_RIGHT:
                player1.movementx = 0

            if event.key == pygame.K_w:
                player2.movementy = 0
            if event.key == pygame.K_s:
                player2.movementy = 0
            if event.key == pygame.K_d:
                player2.movementx = 0
            if event.key == pygame.K_a:
                player2.movementx = 0
    
    # draw Background
    screen.fill(backroundColor)

    for player in players:
        player.update()

    ball.update()

    powerup.update()
    
    game.check()

    pygame.display.flip()
    clock.tick(60)
