import pygame
import math
import random

screen_width = 1980
screen_height = 1080
scale = 0.5
scaledWidth = screen_width * scale
scaledHeight = screen_height * scale
ballSpeed = 6
ligth_grey = (250, 250, 250)

class Player():
    def __init__(self, speed, x, scaledHeight, scaledWidth):
        self.vel = speed
        self.paddel = pygame.Rect(x, scaledHeight/2 - 70, 10, 140)
        self.scaledHeight = scaledHeight
        self.scaledWidth = scaledWidth

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddel.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.paddel.x += self.vel

        if keys[pygame.K_UP]:
            self.paddel.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.paddel.y += self.vel
        self.collidesWithBorder()

    def collidesWithBorder(self):
        if self.paddel.top <= 0:
            self.paddel.top = 0
        if self.paddel.bottom >= self.scaledHeight:
            self.paddel.bottom = self.scaledHeight
        if self.paddel.right >= self.scaledWidth:
            self.paddel.right = self.scaledWidth
        if self.paddel.left <= 0:
            self.paddel.left = 0

    def draw(self, screen):
        ligth_grey = (250, 250, 250)
        pygame.draw.rect(screen, ligth_grey, self.paddel)

class Ball():
    def __init__(self, speed):
        self.speed_x = math.sqrt((speed**2)/2)
        self.speed_y = math.sqrt((speed**2)/2)
        self.directionX = random.choice((-1, 1))
        self.directionY = random.choice((-1, 1))
        self.ball = pygame.Rect(scaledWidth/2 - 15, scaledHeight/2 - 15, 20, 20)

    def update(self, screen):
        self.draw(screen)
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

    def draw(self, screen):
        pygame.draw.rect(screen, ligth_grey, self.ball)