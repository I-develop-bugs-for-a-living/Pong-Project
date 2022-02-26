from turtle import right
import pygame, random, sys

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

ballSpeedX = 4
ballSpeedY = 4
basic_font = pygame.font.Font('freesansbold.ttf', 32)

class Player():
    def __init__(self, speed, width):
        self.speed = speed
        self.paddel = pygame.Rect(width, scaledHeight/2 - 70, 10, 140)
        self.movementy = 0
        self.movementx = 0

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

class Ball():
    def __init__(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.directionX = random.choice((-1, 1))
        self.directionY = random.choice((-1, 1))
        self.ball = pygame.Rect(scaledWidth/2 - 15, scaledHeight/2 - 15, 30, 30)

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
        self.ball.center = (scaledWidth/2, scaledHeight/2)

    def draw(self):
        pygame.draw.rect(screen, ligth_grey, self.ball)

class Game():
    def __init__(self, player1, player2, ball) -> None:
        self.player1 = player1
        self.player2 = player2
        self.ball = ball
        self.scorePlayer1 = 0
        self.scorePlayer2 = 0
    
    def check(self):
        self.collision()
        self.scoring()
        self.displayScore()

    def collision(self):
        if self.player1.paddel.colliderect(self.ball.ball):
            self.ball.directionX = 1
        if self.player2.paddel.colliderect(self.ball.ball):
            self.ball.directionX = -1
        
    def scoring(self):
        if self.ball.ball.left <= 0:
            self.ball.reset()
            self.scorePlayer1 += 1
            print(self.scorePlayer1, self.scorePlayer2)

        if self.ball.ball.right >= scaledWidth:
            self.ball.reset()
            self.scorePlayer2 += 1
            print(self.scorePlayer1, self.scorePlayer2)

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
ball = Ball(ballSpeedX, ballSpeedY)

# Game
game = Game(player1, player2, ball)

while True:
    for event in pygame.event.get():
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

    screen.fill(backroundColor)

    for player in players:
        player.update()

    ball.update()

    game.check()

    pygame.display.flip()
    clock.tick(60)
