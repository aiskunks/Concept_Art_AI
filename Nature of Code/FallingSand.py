import pygame
import random
import colorsys

def make_2d_grid(cols, rows):
    arr = [[0 for _ in range(cols)] for _ in range(rows)]
    return arr

def rotate_matrix(matrix):
    return list(map(list, zip(*matrix[::-1])))

pygame.init()

width, height = 400, 400
w = 5
rows, cols = height // w, width // w
grid = make_2d_grid(cols, rows)
hue_value = 10
gravity = 0.18

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Falling Sand")

clock = pygame.time.Clock()

rotate_button_rect = pygame.Rect(10, 10, 100, 30)
rotate_button_color = (0, 255, 0)
rotate_button_text_color = (255, 255, 255)
rotate_button_font = pygame.font.Font(None, 24)

rotate_angle = 0

def draw_button():
    pygame.draw.rect(screen, rotate_button_color, rotate_button_rect)
    text = rotate_button_font.render("Rotate", True, rotate_button_text_color)
    text_rect = text.get_rect(center=rotate_button_rect.center)
    screen.blit(text, text_rect)

def draw_grid():
    for i in range(cols):
        for j in range(rows):
            if grid[i][j] > 0:
                rgb_color = [int(c * 255) for c in colorsys.hsv_to_rgb(grid[i][j]/360, 1, 1)]
                pygame.draw.rect(screen, rgb_color, (i * w, j * w, w, w))

def update_grid():
    next_grid = make_2d_grid(cols, rows)
    for i in range(cols):
        for j in range(rows):
            state = grid[i][j]
            if state > 0:
                below = grid[i][j + 1] if j + 1 < rows else 0

                direction = -1 if random.randint(0, 1) < 0.5 else 1
                below_r = grid[i + direction][j + 1] if 0 <= i + direction < cols and j + 1 < rows else -1
                below_l = grid[i - direction][j + 1] if 0 <= i - direction < cols and j + 1 < rows else -1

                if below == 0 and j + 1 < rows:
                    next_grid[i][j + 1] = state
                elif below_r == 0 and 0 <= i + direction < cols:
                    next_grid[i + direction][j + 1] = state
                elif below_l == 0 and 0 <= i - direction < cols:
                    next_grid[i - direction][j + 1] = state
                else:
                    next_grid[i][j] = state

    return next_grid

def rotate_canvas():
    global rotation_angle
    rotation_angle += 90
    if rotation_angle >= 360:
        rotation_angle = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rotate_button_rect.collidepoint(event.pos):
                rotate_angle += 90
                grid = rotate_matrix(grid)

    mouse_col, mouse_row = pygame.mouse.get_pos()
    mouse_col //= w
    mouse_row //= w

    matrix = 3
    extent = matrix // 2
    for i in range(-extent, extent + 1):
        for j in range(-extent, extent + 1):
            if random.random() < 0.75:
                col = mouse_col + i
                row = mouse_row + j
                if 0 <= col < cols and 0 <= row < rows:
                    grid[col][row] = hue_value

    hue_value += 1
    if hue_value > 360:
        hue_value = 1

    screen.fill((0, 0, 0))
    draw_grid()
    draw_button()
    grid = update_grid()

    # Apply gravity to all non-zero cells
    for i in range(cols):
        for j in range(rows - 1, 0, -1):
            if grid[i][j] > 0:
                grid[i][j] = 0  # Clear the current cell
                new_row = min(rows - 1, j + int(gravity * w))  # Apply gravity
                grid[i][new_row] = hue_value

    rotated_grid = rotate_matrix(grid)
    rotated_rows, rotated_cols = len(rotated_grid), len(rotated_grid[0])


    pygame.display.flip()
    clock.tick(10)

pygame.quit()
