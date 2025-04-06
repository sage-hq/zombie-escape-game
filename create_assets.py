import pygame
import os

# Initialize Pygame
pygame.init()

# Create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')
if not os.path.exists('assets/images'):
    os.makedirs('assets/images')

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asset Creation")

# Create player sprite
player_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
# Draw player (simple stick figure)
pygame.draw.circle(player_surface, WHITE, (25, 15), 10)  # Head
pygame.draw.line(player_surface, WHITE, (25, 25), (25, 35), 2)  # Body
pygame.draw.line(player_surface, WHITE, (25, 35), (15, 45), 2)  # Left leg
pygame.draw.line(player_surface, WHITE, (25, 35), (35, 45), 2)  # Right leg
pygame.draw.line(player_surface, WHITE, (25, 30), (15, 25), 2)  # Left arm
pygame.draw.line(player_surface, WHITE, (25, 30), (35, 25), 2)  # Right arm
pygame.image.save(player_surface, 'assets/images/Player.png')

# Create zombie sprite
zombie_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
# Draw zombie (similar to player but green and more menacing)
pygame.draw.circle(zombie_surface, GREEN, (25, 15), 12)  # Bigger head
pygame.draw.line(zombie_surface, GREEN, (25, 25), (25, 40), 3)  # Thicker body
pygame.draw.line(zombie_surface, GREEN, (25, 40), (15, 48), 3)  # Left leg
pygame.draw.line(zombie_surface, GREEN, (25, 40), (35, 48), 3)  # Right leg
pygame.draw.line(zombie_surface, GREEN, (25, 30), (10, 35), 3)  # Left arm (reaching)
pygame.draw.line(zombie_surface, GREEN, (25, 30), (40, 35), 3)  # Right arm (reaching)
pygame.image.save(zombie_surface, 'assets/images/Zombie-left.png')

# Create ground texture
ground_surface = pygame.Surface((100, 100))
ground_surface.fill(BROWN)
# Add some texture
for i in range(20):
    x = pygame.random.randint(0, 99)
    y = pygame.random.randint(0, 99)
    pygame.draw.circle(ground_surface, (BROWN[0]-20, BROWN[1]-20, BROWN[2]-20), (x, y), 2)
pygame.image.save(ground_surface, 'assets/images/ground.png')

print("Assets created successfully!")
pygame.quit()