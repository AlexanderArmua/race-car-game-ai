import sys
import random

import pygame

# Local imports - using relative imports since config is now inside src
from .config.settings import (
    BACKGROUND_COLOR,
    DISPLAY_HEIGHT,
    DISPLAY_WIDTH,
    CARS_AMOUNT,
    FPS,
    GENERATION_TIME_LIMIT,
    RANDOM_SEED,
    USE_FIXED_SEED,
)
from .race_info import RaceInfo
from .track import Track
from .ai.car_alg_gen import CarAlgGen
from .metrics_logger import MetricsLogger


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

def set_random_seed():
    """Set random seeds for reproducibility if enabled in settings."""
    if USE_FIXED_SEED:
        # Set seeds for different libraries that might use randomness
        random.seed(RANDOM_SEED)
        print(f"Using fixed random seed: {RANDOM_SEED}")

        return RANDOM_SEED
    else:
        seed = random.randrange(sys.maxsize)
        random.seed(seed)
        print(f"Using random behavior (no fixed seed) - Random seed: {seed}")

        return seed    


def main():
    # Set random seed before anything else
    seed = set_random_seed()

    clock, screen = init_game()

    alg_gen = CarAlgGen(CARS_AMOUNT)
    rna_cars = alg_gen.generate_initial_population()

    track = Track(screen, rna_cars, DISPLAY_WIDTH, DISPLAY_HEIGHT)

    race_info = RaceInfo(screen, track)
    race_info.set_alg_gen(alg_gen)  # Pass the genetic algorithm reference

    # Create a metrics logger
    metrics_logger = MetricsLogger(seed)

    # Main game loop
    running = True

    seconds_running = 0

    while running:
        # Control frame rate
        clock.tick(FPS)
        seconds_running += 1/FPS

        running = control_events(track)

        # Draw game objects
        track.draw(BACKGROUND_COLOR)

        # Metrics for AI
        race_info.draw()

        # Update display
        pygame.display.update()

        if track.are_all_cars_dead() or seconds_running > GENERATION_TIME_LIMIT:
            seconds_running = 0

            best_car = max(track.cars, key=lambda car: car.get_score())

            # Log metrics for this generation
            metrics_logger.log_generation(
                alg_gen.get_generation(),
                best_car.get_score(),
                track.get_all_cars_alive(),
                track.cars
            )

            new_rnas = alg_gen.get_new_population()

            track.restart_cars(new_rnas)
            
            # Reset best car in race_info when a new generation starts
            race_info.best_car = None
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
