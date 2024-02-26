import pygame
import sys

def cantor(x, y, length):
    if length >= 1:
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x + length, y), 5)
        y += 20
        cantor(x, y, length / 3)
        cantor(x + length * 2 / 3, y, length / 3)

# Pygame setup
pygame.init()
width, height = 800, 200
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Draw the Cantor set
    cantor(50, 50, 700)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
