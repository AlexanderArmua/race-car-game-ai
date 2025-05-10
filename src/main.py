import sys

import pygame

# Local imports - using relative imports since config is now inside src
from .config.settings import (
    BACKGROUND_COLOR,
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    FPS,
)
from .race_info import RaceInfo
from .track import Track


def init_game():
    # Initialize pygame
    pygame.init()

    # Set up clock for controlling frame rate
    clock = pygame.time.Clock()
    
    # Set window title
    pygame.display.set_caption('UTN - IA 2025 - Car Game')

    # Set up display
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    return clock, screen
    
def control_events(track: Track) -> bool:
    """
    Check key events and update game objects.
    Returns True if the game should continue running, False otherwise.
    """

    # Process events
    for event in pygame.event.get():
        is_close = event.type == pygame.QUIT
        is_escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

        if is_close or is_escape:
            return False
    
    # Get key states
    keys = pygame.key.get_pressed()

    # Update game objects
    track.update(keys)

    return True

def main():
    clock, screen = init_game()
        
    track = Track(screen, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    race_info = RaceInfo(screen, track)
    
    # Main game loop
    running = True
    
    while running:
        # Control frame rate
        clock.tick(FPS)
        
        running = control_events(track)
        
        # Draw game objects
        track.draw(BACKGROUND_COLOR)
        
        # Metrics for AI
        race_info.draw()
        
        # Update display
        pygame.display.update()

        if track.are_all_cars_dead():
            track.restart_cars()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
