import pygame
import sys
import noise
import random
from pygame.math import Vector2

class Path:
    def __init__(self, start, end, radius=20):
        self.start = Vector2(start)
        self.end = Vector2(end)
        self.radius = radius

    def display(self, screen):
        # Display the path
        pygame.draw.line(screen, (0, 100, 0), self.start, self.end, self.radius * 2)
        pygame.draw.line(screen, (0, 0, 0), self.start, self.end, 1)

class FlowField:
    def __init__(self, width, height, resolution):
        self.resolution = resolution
        self.cols = width // resolution
        self.rows = height // resolution
        self.field = [[None] * self.rows for _ in range(self.cols)]
        self.init_field()

    def init_field(self):
        xoff = 0
        for i in range(self.cols):
            yoff = 0
            for j in range(self.rows):
                theta = pygame.math.Vector2(noise.pnoise2(xoff, yoff), noise.pnoise2(xoff + 1, yoff + 1))
                self.field[i][j] = pygame.math.Vector2(theta.x, theta.y)
                yoff += 0.1
            xoff += 0.1

    def lookup(self, lookup):
        column = int(min(max(lookup.x // self.resolution, 0), self.cols - 1))
        row = int(min(max(lookup.y // self.resolution, 0), self.rows - 1))
        return self.field[column][row].copy()


class Vehicle:
    def __init__(self, x, y):
        self.acceleration = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.location = Vector2(x, y)
        self.r = 3.0
        self.maxspeed = 4
        self.maxforce = 0.2

    def update(self, flow):
        desired = flow.lookup(self.location)
        if desired.length() > 0.0001:
            desired.scale_to_length(self.maxspeed)

        # Steering is desired minus velocity
        steer = desired - self.velocity
        if steer.length() > 0.0001:
            steer.scale_to_length(self.maxforce)

        # Apply the steering force
        self.apply_force(steer)

        # Avoid edges
        self.avoid_edges(800, 600)

        # Standard Euler integration
        self.velocity += self.acceleration
        if self.velocity.length() > 0.0001:
            self.velocity.scale_to_length(self.maxspeed)
        self.location += self.velocity
        self.acceleration *= 0

    def apply_force(self, force):
        self.acceleration += force

    def seek(self, target):
        desired = target - self.location
        desired.normalize_ip()
        desired *= self.maxspeed
        steer = desired - self.velocity
        print("steer: ", steer)
        if steer.length() > 0.0001:
            steer.scale_to_length(self.maxforce)
        self.apply_force(steer)

    def display(self):
        theta = self.velocity.angle_to(Vector2(0, 1)) + pygame.math.Vector2().angle_to(Vector2(1, 0))
        pygame.draw.polygon(screen, (175, 175, 175), self.get_rotated_points(theta), 2)

    def arrive(self, target):
        desired = target - self.location
        d = desired.length()
        desired.normalize_ip()
        if d < 100:
            m = pygame.math.lerp(0, self.maxspeed, d / 100)
            desired *= m
        else:
            desired *= self.maxspeed
        steer = desired - self.velocity
        if steer.length() > 0.0001:
            steer.scale_to_length(self.maxforce)
        self.apply_force(steer)

        pygame.draw.circle(screen, (255, 0, 0), (int(target.x), int(target.y)), 10)

    def get_rotated_points(self, angle):
        points = [Vector2(0, -self.r * 2), Vector2(-self.r, self.r * 2), Vector2(self.r, self.r * 2)]
        return [p.rotate(angle) + self.location for p in points]

    def avoid_edges(self, width, height):
        if self.location.x < 25:
            desired = pygame.math.Vector2(self.maxspeed, self.velocity.y)
            steer = desired - self.velocity
            if steer.length() > 0.0001:
                steer.scale_to_length(self.maxforce)
            self.apply_force(steer)

        # Add similar logic for other edges as needed
        if self.location.x > width - 25:
            desired = pygame.math.Vector2(-self.maxspeed, self.velocity.y)
            steer = desired - self.velocity
            if steer.length() > 0.0001:
                steer.scale_to_length(self.maxforce)
            self.apply_force(steer)

        if self.location.y < 25:
            desired = pygame.math.Vector2(self.velocity.x, self.maxspeed)
            steer = desired - self.velocity
            if steer.length() > 0.0001:
                steer.scale_to_length(self.maxforce)
            self.apply_force(steer)

        if self.location.y > height - 25:
            desired = pygame.math.Vector2(self.velocity.x, -self.maxspeed)
            steer = desired - self.velocity
            if steer.length() > 0.0001:
                steer.scale_to_length(self.maxforce)
            self.apply_force(steer)

    def follow(self, flow):
    # What is the vector at that spot in the flow field?
        desired = flow.lookup(self.location)
        desired.scale_to_length(self.maxspeed)

        # Steering is desired minus velocity
        steer = desired - self.velocity
        if steer.length() > 0.0001:
            steer.scale_to_length(self.maxforce)

        # Apply the steering force
        self.apply_force(steer)

    def follow(self, path):
        # Predict the vehicle's future location
        predict = self.velocity.normalize() * 25
        predict_loc = self.location + predict

        # Find the normal point along the path
        a = path.start
        b = path.end
        normal_point = self.get_normal_point(predict_loc, a, b)

        # Move a little further along the path and set a target
        direction = (b - a).normalize() * 10
        target = normal_point + direction

        # If we are off the path, seek that target in order to stay on the path
        distance = normal_point.distance_to(predict_loc)
        if distance > path.radius:
            self.seek(target)
    
    def get_normal_point(self, p, a, b):
        ap = p - a
        ab = b - a

        # Ensure ab is not a zero vector before normalizing
        if ab.length() > 0:
            ab.normalize()
            ab *= ap.dot(ab)

        normal_point = a + ab
        return normal_point
    
    def separate(self, vehicles):
        desired_separation = self.r * 2
        sum_force = Vector2()
        count = 0

        for other in vehicles:
            distance = self.location.distance_to(other.location)

            if 0 < distance < desired_separation:
                diff = self.location - other.location
                diff.normalize()
                diff /= distance
                sum_force += diff
                count += 1

        if count > 0:
            sum_force /= count
            sum_force.normalize()
            sum_force *= self.maxspeed
            steer = sum_force - self.velocity
            if steer.length() > 0.0001:
                steer.scale_to_length(self.maxforce)
            self.apply_force(steer)


def setup():
    pygame.init()
    return pygame.display.set_mode((800, 600))

# Pygame setup
screen = setup()
clock = pygame.time.Clock()

# Create a vehicle
# vehicle = Vehicle(0, 300)

# Create vehicles
vehicles = [Vehicle(random.uniform(0, 320), random.uniform(0, 240)) for _ in range(2)]

flow = FlowField(800, 600, 20)
path = Path((0, 350), (800, 350), 20)
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Display flow lines
    for x in range(0, 800, 20):
        for y in range(0, 600, 20):
            start = Vector2(x, y)
            direction = flow.lookup(start)
            end = start + direction * 10  # Adjust the length of the vectors as needed
            pygame.draw.line(screen, (0, 0, 0), start, end, 1)


    # # vehicle.seek(Vector2(pygame.mouse.get_pos()))
    # vehicle.arrive(Vector2(400,350))
    # vehicle.update(flow)
    # # If you want to follow a particular path, uncomment the following line:
    # # vehicle.follow(path)
    # vehicle.display()
    for vehicle in vehicles:
        vehicle.separate(vehicles)
        vehicle.update(flow)
        vehicle.arrive(Vector2(400,350))
        vehicle.display()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
