import sys

import pygame

# Local imports - using relative imports since config is now inside src
from .car import Car
from .config.settings import (
    BACKGROUND_COLOR,
    CAR_IMAGE_PATH,
    CAR_WIDTH,
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    FPS,
)
from .race_info import RaceInfo
from .track import Track


def main():
    # Initialize pygame
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('UTN - IA 2025 - Car Game')
    
    # Set up clock for controlling frame rate
    clock = pygame.time.Clock()
    
    # Create game objects
    car_x = (DISPLAY_WIDTH - CAR_WIDTH) // 2
    car_y = (DISPLAY_HEIGHT - CAR_WIDTH) // 2
    
    car = Car(car_x, car_y, CAR_IMAGE_PATH, CAR_WIDTH)
    track = Track(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    race_info = RaceInfo()
    
    # Main game loop
    running = True
    
    while running:
        # Control frame rate
        clock.tick(FPS)
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car.change_pause()
        
        # Get key states
        keys = pygame.key.get_pressed()
        
        # Update game objects
        car.update(keys, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        
        # Draw game objects
        track.draw(screen, BACKGROUND_COLOR)
        car.draw(screen)
        
        # Metrics for AI
        # 5 sensors - 2 walls - 10 possible collisions
        sensor_detections = car.check_rays_collision(track.get_boundary_rects())
        # Car info
        car_info = car.get_info()

        # Draw UI elements
        race_info.draw_collision_info(screen, sensor_detections)
        race_info.draw_car_info(screen, car_info)
        
        # Update display
        pygame.display.update()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
