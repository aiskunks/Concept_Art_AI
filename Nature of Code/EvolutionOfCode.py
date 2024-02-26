import pygame
import random

class DNA:
    def __init__(self, target):
        self.genes = [chr(random.randint(32, 127)) for _ in range(len(target))]
        self.fitness = 0
    def calculate_fitness(self, target):
        score = sum(1 for a, b in zip(self.genes, target) if a == b)
        self.fitness = score / len(target)
        return self.fitness
    def crossover(self, partner):
        child = DNA("".join(self.genes))  # Initialize child with random genes
        midpoint = random.randint(0, len(self.genes))

        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]

        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = chr(random.randint(32, 127))



# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create a population
target = "to be or not to be"
population_size = 50000
population = [DNA(target) for _ in range(population_size)]
generation = 1
best_phrase = None
closest_phrases = []

# Main loop
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused 

    screen.fill((255, 255, 255))

    if not paused:

        # Create an empty mating pool
        mating_pool = []

        # Fill the mating pool based on fitness
        for dna in population:
            n = int(dna.calculate_fitness(target) * 100)
            mating_pool.extend([dna] * n)

        # Mutation Rate
        mutation_rate = 0.01

        # Reproduction
        for i in range(population_size):
            a = random.randint(0, len(mating_pool) - 1)
            b = random.randint(0, len(mating_pool) - 1)
            partner_a = mating_pool[a]
            partner_b = mating_pool[b]

            # Crossover
            child = partner_a.crossover(partner_b)

            # Mutation
            child.mutate(mutation_rate)

            # Overwrite the population with the new children
            population[i] = child

        # Find the best phrase in the current generation
        best_dna = population[0]
        for dna in population:
            if dna.fitness > best_dna.fitness:
                best_dna = dna

        closest_phrases.append(best_dna.genes)

        # Display content of the Best DNA in the mating pool
        font = pygame.font.Font(None, 26)
        phrasetext = font.render("Best Phrase: ", True, (0, 0, 0))
        screen.blit(phrasetext, (50, 25))
        font = pygame.font.Font(None, 36)
        text = font.render("".join(best_dna.genes), True, (0, 0, 0))
        screen.blit(text, (50, 50))

        # Display content of the population
        font = pygame.font.Font(None, 24)

        # Display generation
        generation_text = font.render(f"Generation: {generation}", True, (0, 0, 0))
        screen.blit(generation_text, (50, 510))

        # Calculate and display average fitness
        total_fitness = sum(dna.calculate_fitness(target) for dna in population)
        average_fitness = total_fitness / population_size
        average_fitness_text = font.render(f"Average Fitness: {average_fitness:.2f}", True, (0, 0, 0))
        screen.blit(average_fitness_text, (50, 530))

        # Display total population and mutation rate
        info_text = font.render(f"Population: {population_size}  Mutation Rate: {mutation_rate:.2%}", True, (0, 0, 0))
        screen.blit(info_text, (50, 550))

        # Check if the target phrase is found
        if ''.join(best_dna.genes) == target:
            paused = not paused
            # Display content of the Best DNA in the mating pool
            font = pygame.font.Font(None, 26)
            phrasetext = font.render("Best Phrase: ", True, (0, 0, 0))
            screen.blit(phrasetext, (50, 25))
            font = pygame.font.Font(None, 36)
            text = font.render("".join(best_dna.genes), True, (0, 0, 0))
            screen.blit(text, (50, 50))

            # Display content of the population
            font = pygame.font.Font(None, 24)

            # Display generation
            generation_text = font.render(f"Generation: {generation}", True, (0, 0, 0))
            screen.blit(generation_text, (50, 510))

            # Calculate and display average fitness
            total_fitness = sum(dna.calculate_fitness(target) for dna in population)
            average_fitness = total_fitness / population_size
            average_fitness_text = font.render(f"Average Fitness: {average_fitness:.2f}", True, (0, 0, 0))
            screen.blit(average_fitness_text, (50, 530))

            # Display total population and mutation rate
            info_text = font.render(f"Population: {population_size}  Mutation Rate: {mutation_rate:.2%}", True, (0, 0, 0))
            screen.blit(info_text, (50, 550))

            font = pygame.font.Font(None, 26)
            phrasetext = font.render("All Closest Phrases: ", True, (0, 0, 0))
            screen.blit(phrasetext, (580, 25))
            y_offset = 50
            for i in range(len(closest_phrases) - 1, len(closest_phrases) - 21, -1):
                phrase_text = font.render(f"{''.join(closest_phrases[i])}", True, (0, 0, 0))
                screen.blit(phrase_text, (580, y_offset))
                y_offset += 20

        generation += 1

        pygame.display.flip()
        clock.tick(60)

pygame.quit()