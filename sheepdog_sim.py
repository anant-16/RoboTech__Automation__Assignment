import pygame
import random
import math

# ---- Configuration ----
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHEEP_COUNT = 3
SHEEP_RADIUS = 15
DOG_RADIUS = 20
SHEEP_SPEED = 2
DOG_SPEED = 3
FEAR_DISTANCE = 100  # pixels
SAFE_ZONE_X = SCREEN_WIDTH - 50

# ---- Colors ----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)

# ---- Initialize Pygame ----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sheepdog Simulation")
clock = pygame.time.Clock()

# ---- Sheep Class ----
class Sheep:
    def __init__(self):
        self.x = random.randint(50, 200)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.alive = True

    def move_away(self, dog_x, dog_y):
        dx = self.x - dog_x
        dy = self.y - dog_y
        distance = math.hypot(dx, dy)
        if distance < FEAR_DISTANCE:
            # Move away proportional to fear
            if distance == 0:
                distance = 1
            self.x += (dx / distance) * SHEEP_SPEED
            self.y += (dy / distance) * SHEEP_SPEED
        # Keep inside screen
        self.x = max(SHEEP_RADIUS, min(SCREEN_WIDTH - SHEEP_RADIUS, self.x))
        self.y = max(SHEEP_RADIUS, min(SCREEN_HEIGHT - SHEEP_RADIUS, self.y))

# ---- Sheepdog Class ----
class Sheepdog:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

    def move_towards_sheep(self, sheep_list):
        if not sheep_list:
            return
        # Select nearest sheep
        target = min(sheep_list, key=lambda s: math.hypot(s.x - self.x, s.y - self.y))
        # Herding point: behind sheep (relative to safe zone)
        target_x = target.x - 30
        target_y = target.y
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return
        self.x += (dx / distance) * DOG_SPEED
        self.y += (dy / distance) * DOG_SPEED

# ---- Create agents ----
sheep_list = [Sheep() for _ in range(SHEEP_COUNT)]
dog = Sheepdog()

# ---- Main Loop ----
running = True
while running:
    screen.fill(WHITE)
    # Draw safe zone
    pygame.draw.rect(screen, GREEN, (SAFE_ZONE_X, 0, SCREEN_WIDTH - SAFE_ZONE_X, SCREEN_HEIGHT))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sheep
    for sheep in sheep_list:
        if sheep.alive:
            sheep.move_away(dog.x, dog.y)
            # Check safe zone
            if sheep.x >= SAFE_ZONE_X:
                sheep.alive = False
            else:
                pygame.draw.circle(screen, BLACK, (int(sheep.x), int(sheep.y)), SHEEP_RADIUS)

    # Update dog
    alive_sheep = [s for s in sheep_list if s.alive]
    dog.move_towards_sheep(alive_sheep)
    pygame.draw.circle(screen, RED, (int(dog.x), int(dog.y)), DOG_RADIUS)

    pygame.display.flip()
    clock.tick(60)

    # Check if all sheep are safe
    if all(not s.alive for s in sheep_list):
        print("All sheep are safe! Simulation complete.")
        pygame.time.wait(2000)
        running = False

pygame.quit()
