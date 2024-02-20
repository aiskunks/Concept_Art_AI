import pygame
from pygame.locals import QUIT

class PVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y

pygame.init()

width, height = 200, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PVector with Pygame")

location = PVector(100, 100)
velocity = PVector(2.5, 5)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    location.add(velocity)

    if location.x > width or location.x < 0:
        velocity.x *= -1

    if location.y > height or location.y < 0:
        velocity.y *= -1

    screen.fill((255, 255, 255))
    pygame.draw.ellipse(screen, (175, 175, 175), (location.x - 8, location.y - 8, 16, 16))

    pygame.display.flip()
    clock.tick(60)
