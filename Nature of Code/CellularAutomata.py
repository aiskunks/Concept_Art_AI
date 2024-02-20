import pygame
import sys
import random 
class CA:
    def __init__(self):
        self.w = 10
        self.generation = 0
        self.generations = []
        self.ruleset = [0, 1, 0, 1, 1, 0, 1, 0] # Change the rule set in the form of binary numbers from 0-255 to change patterns
        self.cells = [random.randint(0, 1) for _ in range(width // self.w)]
        self.cells[len(self.cells)//2] = 1
        # if you want to change the pattern using rules, use the following cell declaration, else previous
        # self.cells = self.initialize_cells()

    def initialize_cells(self):
        # Repeat the ruleset to fill the initial cells
        num_repeats = (width // self.w) // len(self.ruleset) + 1
        initial_cells = [bit for bit in (self.ruleset * num_repeats)[:width // self.w]]
        return initial_cells

    def generate(self):
        nextgen = [0] * len(self.cells)
        for i in range(1, len(self.cells)-1):
            left = self.cells[i-1]
            me = self.cells[i]
            right = self.cells[i+1]
            nextgen[i] = self.rules(left, me, right)
        self.cells = nextgen
        self.generations.append(self.cells.copy())
        self.generation += 1

    def rules(self, a, b, c):
        s = str(a) + str(b) + str(c)
        index = int(s, 2)
        return self.ruleset[index]

    def draw(self, screen):
        for gen_index, generation in enumerate(self.generations):
            for i in range(len(generation)):
                if generation[i] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (i*self.w, gen_index*self.w, self.w, self.w))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (i*self.w, gen_index*self.w, self.w, self.w))


# Pygame setup
pygame.init()
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Cellular Automaton setup
ca = CA()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ca.generate()
    screen.fill((255, 255, 255))
    ca.draw(screen)

    pygame.display.flip()
    clock.tick(10)  # Adjust the speed of the simulation
