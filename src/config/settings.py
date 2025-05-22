# Car settings
import os

# Game settings
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800
BACKGROUND_COLOR = (0, 140, 0)  # Green grass
FPS = 500
CARS_AMOUNT = 30

# AI settings
GENERATION_TIME_LIMIT = 2  # Seconds before creating a new generation
MAXIMUM_SCORE = 100
RANDOM_SEED = 2062072707638544738  # Fixed seed for reproducibility (change this value to get different but reproducible results)
USE_FIXED_SEED = False  # Set to False to use random behavior

# Define the path relative to the project root
CAR_IMAGE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "car.png"
)
if not os.path.exists(CAR_IMAGE_PATH):
    raise FileNotFoundError(f"Car image not found at {CAR_IMAGE_PATH}")

CAR_WIDTH = 30
CAR_SPEED = 30
CAR_TURN_SPEED = 10

MUTATION_RATE = 0.1

CROSSOVER_RATE = 0.8

MANUAL_CONTROL = False
