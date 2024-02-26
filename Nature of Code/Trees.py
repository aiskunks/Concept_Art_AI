import pygame
import sys
import math
import random

# Symmetric Tree
def draw_branch(surface, start, angle, length, width):
    end_x = start[0] + length * math.cos(angle)
    end_y = start[1] + length * math.sin(angle)
    end_point = (int(end_x), int(end_y))

    pygame.draw.line(surface, (0, 0, 0), start, end_point, width)

    if length > 5:  # Set a minimum length to stop recursion
        new_length = length * 0.7  # Adjust the length reduction factor
        new_width = int(width * 0.8)  # Adjust the width reduction factor

        # Gives random angle to the branch, can be set to a static value
        random_angle = random.uniform(-math.radians(45), math.radians(45))

        draw_branch(surface, end_point, angle - random_angle, new_length, new_width)
        draw_branch(surface, end_point, angle + random_angle, new_length, new_width)

def setup():
    pygame.init()
    return pygame.display.set_mode((800, 600))

# Pygame setup
screen = setup()
clock = pygame.time.Clock()
screen.fill((255, 255, 255))

# Draw the tree in the middle
start_point = (400, 500)
draw_branch(screen, start_point, -math.pi / 2, 100, 10)  # Initial angle set to math.pi / 2
# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
