import pygame
import sys
from pygame.math import Vector2

class KochLine:
    def __init__(self, a, b):
        self.start = Vector2(a)
        self.end = Vector2(b)

    def display(self):
        pygame.draw.line(screen, (0, 0, 0), (self.start.x, self.start.y), (self.end.x, self.end.y), 1)

    def kochA(self):
        return Vector2(self.start)

    def kochB(self):
        v = self.end - self.start
        v /= 3
        v += self.start
        return v

    def kochC(self):
        a = Vector2(self.start)
        v = self.end - self.start
        v /= 3
        a += v
        v.rotate_ip(-60)
        a += v
        return a

    def kochD(self):
        v = self.end - self.start
        v *= 2 / 3.0
        v += self.start
        return v

    def kochE(self):
        return Vector2(self.end)

def generate(lines):
    next_lines = []
    for l in lines:
        a = l.kochA()
        b = l.kochB()
        c = l.kochC()
        d = l.kochD()
        e = l.kochE()
        next_lines.append(KochLine(a, b))
        next_lines.append(KochLine(b, c))
        next_lines.append(KochLine(c, d))
        next_lines.append(KochLine(d, e))
    return next_lines

# Pygame setup
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Create the KochLine objects
start = width // 3, height // 2
end = 2 * width // 3, height // 2
lines = [KochLine(start, end)]
lines2 = [KochLine(end, start)]

# Generate the Koch lines
for i in range(5):
    lines = generate(lines)

for i in range(5):
    lines2 = generate(lines2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Draw the Koch lines
    for l in lines:
        l.display()
    
    for l in lines2:
        l.display()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

