import pygame
import sys

# Local imports - using relative imports since config is now inside src
from .car import Car
from .track import Track
from .sensors import Sensors
from .config.settings import (
    DISPLAY_WIDTH, DISPLAY_HEIGHT, BACKGROUND_COLOR, FPS,
    CAR_IMAGE_PATH, CAR_WIDTH
)

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
    sensors = Sensors()
    
    # Main game loop
    running = True
    
    while running:
        # Control frame rate
        clock.tick(FPS)
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get key states
        keys = pygame.key.get_pressed()
        
        # Update game objects
        car.update(keys, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        
        # Clear screen
        screen.fill(BACKGROUND_COLOR)
        
        # Draw game objects
        track.draw(screen)
        car.draw(screen)
        
        # Draw UI elements
        sensors.draw_collision_info(screen, car, track)
        sensors.draw_car_info(screen, car)
        
        # Update display
        pygame.display.update()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
