import car
import pygame
import math
import mppi
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Car instance
car = car.Car(x=0, y=-400, vx=0, vy=0)
mppi = mppi.MPPI(0.016667,50, 100)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()

    """
    if keys[pygame.K_UP]:
        car.u[1] = -1
    elif keys[pygame.K_DOWN]:
        car.u[1] = 1
    else: 
        car.u[1] = 0
    
    if keys[pygame.K_LEFT]:
        car.u[0] = -1  
    elif keys[pygame.K_RIGHT]:
        car.u[0] = 1
    else: car.u[0] = 0
    """
    # Update car dynamics
    car.previous_positions, costs, action = mppi.allPaths(car.x)
    
    car.u = action
    #print(car.u)

    car.update(dt)
    screen.fill(WHITE)

    
    
    for j in range(len(car.previous_positions)-1):
        for i in range(len(car.previous_positions[j])):
            screen.set_at((car.previous_positions[j][i][0] + WIDTH // 2, car.previous_positions[j][i][1] + HEIGHT // 2), (255,0,0))
            
    for i in range(len(car.previous_positions[len(car.previous_positions)-1])):
        screen.set_at((car.previous_positions[len(car.previous_positions)-1][i][0] + WIDTH // 2, car.previous_positions[len(car.previous_positions)-1][i][1] + HEIGHT // 2), (0,0,255))

    # Draw everything
    pygame.draw.rect(screen, (255,255,0), (WIDTH // 2-100, HEIGHT // 2 - 100, 200, 200))
    
    pygame.draw.rect(screen, BLACK, (int(car.x[0]) + WIDTH // 2, int(car.x[1]) + HEIGHT // 2, car.width, car.height))

    pygame.display.flip()

pygame.quit()
