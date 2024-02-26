import pygame
import sys

def drawCircle(x, y, radius):
    pygame.draw.ellipse(screen, (0, 0, 0), (x - radius/2, y - radius/2, radius, radius), 1)

    if radius > 8:
        # Recursion done 4 times give a pattern in x and y plane, if done 2 times then pattern appears in horizontal plane only
        drawCircle(x + radius/2, y, radius/2)
        drawCircle(x - radius/2, y, radius/2)
        # By commenting the following two lines, the pattern is displayed on a single horizontal line
        drawCircle(x, y + radius/2, radius/2)
        drawCircle(x, y - radius/2, radius/2)

# Pygame setup
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Draw the circles
    drawCircle(width/2, height/2, 400)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
