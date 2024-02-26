import pygame
import random
from pygame.math import Vector2

class DNA:
    def __init__(self, lifespan, maxforce, genes=None):
        # Recieves genes and create a dna object
        self.lifespan = lifespan
        self.maxforce = maxforce
        self.genes = None
        if genes:
            self.genes = genes
        # If no genes just create random dna
        else:
            self.genes = []
            for i in range(self.lifespan):
                # Gives random vectors
                gene = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
                # Sets maximum force of vector to be applied to a rocket
                gene.scale_to_length(self.maxforce)
                self.genes.append(gene)

    # Performs a crossover with another member of the species
    def crossover(self, partner):
        newgenes = []
        # Picks random midpoint
        mid = random.randint(0, len(self.genes) - 1)
        for i in range(len(self.genes)):
            # If i is greater than mid, the new gene should come from this partner
            if i > mid:
                newgenes.append(self.genes[i])
            # If i < mid, new gene should come from other partner's gene
            else:
                newgenes.append(partner.genes[i])
        # Gives DNA object an array
        return DNA(self.lifespan, self.maxforce, newgenes)

    # Adds random mutation to the genes to add variance.
    def mutation(self):
        for i in range(len(self.genes)):
            # if random number less than 0.01, new gene is then a random vector
            if random.random() < 0.01:
                self.genes[i] = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
                self.genes[i].scale_to_length(self.maxforce)

class Rocket:
    def __init__(self, width, height, target, dna):
        self.pos = pygame.Vector2(width / 2, height-25)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.completed = False
        self.crashed = False
        self.dna = dna
        self.fitness = 0
        self.target = target
        self.r = 3

    def apply_force(self, force):
        self.acc += force

    def calc_fitness(self, width):
        d = pygame.Vector2.distance_to(self.pos, self.target)
        self.fitness = width - (d / width) * width
        if self.completed:
            self.fitness *= 10
        if self.crashed:
            self.fitness /= 10

    def update(self, width, height, count, rx, ry, rw, rh):
        d = Vector2.distance_to(self.pos, self.target)
        if d < 10:
            self.completed = True
            self.pos = target.copy()
        if rx < self.pos.x < rx + rw and ry < self.pos.y < ry + rh:
            self.crashed = True
        if self.pos.x > width - 5 or self.pos.x < 5 or self.pos.y > height - 5 or self.pos.y < 5:
            self.crashed = True

        self.apply_force(self.dna.genes[count])

        if not self.completed and not self.crashed:
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0
            self.vel.scale_to_length(4)

    def show(self, screen):
        theta = self.vel.angle_to(Vector2(0, 1)) + pygame.math.Vector2().angle_to(Vector2(1, 0))
        pygame.draw.polygon(screen, (175, 175, 175), self.get_rotated_points(theta), 2)
    
    def get_rotated_points(self, angle):
        points = [Vector2(0, -self.r * 2), Vector2(-self.r, self.r * 2), Vector2(self.r, self.r * 2)]
        return [p.rotate(angle) + self.pos for p in points]

class Population:
    def __init__(self, width, height, target, dna, popsize):
        self.rockets = [Rocket(width, height, target, dna) for _ in range(popsize)]
        self.popsize = popsize
        self.matingpool = []
        self.target = target
        self.width = width
        self.height = height
        
    def evaluate(self):
        maxfit = 0
        for rocket in self.rockets:
            rocket.calc_fitness(self.width)
            if rocket.fitness > maxfit:
                maxfit = rocket.fitness

        for rocket in self.rockets:
            rocket.fitness /= maxfit

        self.matingpool = []
        for rocket in self.rockets:
            n = int(rocket.fitness * 100)
            self.matingpool.extend([rocket] * n)

    def selection(self):
        new_rockets = []
        for i in range(self.popsize):
            parentA = random.choice(self.matingpool).dna
            parentB = random.choice(self.matingpool).dna
            child = parentA.crossover(parentB)
            child.mutation()
            new_rockets.append(Rocket(self.width, self.height, self.target, dna=child))

        self.rockets = new_rockets

    def run(self, screen, count, rx, ry, rw, rh):
        for rocket in self.rockets:
            rocket.update(self.width, self.height, count, rx, ry, rw, rh)
            rocket.show(screen)


# Pygame initialization
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Evolution")
clock = pygame.time.Clock()

# Initialize variables
population_size = 50
lifespan = 350
count = 0
rx, ry, rw, rh = width/2 - 100, height/4, 200, 10
target = Vector2(width / 2, 50)
maxforce = 0.5

# Main game loop
dna = DNA(lifespan, maxforce)
population = Population(width, height, target, dna, population_size)
generation = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))

    population.run(screen, count, rx, ry, rw, rh)

    # Render barrier for rockets
    pygame.draw.rect(screen, (255, 255, 255), (rx, ry, rw, rh))
    # Render target
    pygame.draw.ellipse(screen, (255, 255, 255), (target.x - 8, target.y - 8, 16, 16))

    # Display content of the population
    font = pygame.font.Font(None, 24)

    # Display generation
    generation_text = font.render(f"Time: {count}", True, (255, 255, 255))
    screen.blit(generation_text, (50, 550))
    generation_text = font.render(f"Generation: {generation}", True, (255, 255, 255))
    screen.blit(generation_text, (50, 570))
    
    pygame.display.flip()
    clock.tick(60)

    count += 1

    if count == lifespan:
        population.evaluate()
        population.selection()
        count = 0
        generation += 1