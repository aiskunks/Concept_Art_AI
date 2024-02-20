import pygame
import random
import copy

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

# Set up the Game of Life parameters
columns, rows = 80, 60
w = width // columns
board = [[random.randint(0, 1) for _ in range(rows)] for _ in range(columns)]

def calculate_neighbors(x, y):
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbors += board[(x + i + columns) % columns][(y + j + rows) % rows]
    neighbors -= board[x][y]
    return neighbors

def update_board():
    next_board = copy.deepcopy(board)
    for x in range(columns):
        for y in range(rows):
            neighbors = calculate_neighbors(x, y)

            if board[x][y] == 1 and (neighbors < 2 or neighbors > 3):
                next_board[x][y] = 0
            elif board[x][y] == 0 and neighbors == 3:
                next_board[x][y] = 1

    return next_board

def draw_board():
    for i in range(columns):
        for j in range(rows):
            color = (0, 0, 0) if board[i][j] == 1 else (255, 255, 255)
            pygame.draw.rect(screen, color, (i * w, j * w, w, w))
            pygame.draw.rect(screen, (0, 0, 0), (i * w, j * w, w, w), 1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate the next generation
    board = update_board()

    # Draw the current generation
    screen.fill((255, 255, 255))
    draw_board()

    pygame.display.flip()
    clock.tick(10)  # Adjust the speed of the simulation

pygame.quit()
