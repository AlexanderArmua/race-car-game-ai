# Game settings
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
BACKGROUND_COLOR = (234, 212, 252)
FPS = 60

# Car settings
import os
# Define the path relative to the project root
CAR_IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'car.png')
if not os.path.exists(CAR_IMAGE_PATH):
    raise FileNotFoundError(f"Car image not found at {CAR_IMAGE_PATH}")

CAR_WIDTH = 60
CAR_SPEED = 5

# AI settings
POPULATION_SIZE = 50
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7