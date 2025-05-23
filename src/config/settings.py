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
CAR_SPEED = 20
CAR_TURN_SPEED = 10

# Probability of mutation during reproduction in the genetic algorithm.
# Valid range: 0.0 (no mutation) to 1.0 (always mutate).
MUTATION_RATE = 0.1

# Amount of crossover to take from each parent.
# Valid range: 0.0 (don't take from parent) to 1.0 (take all from parent).
CROSSOVER_RATE = 0.8

# If true, the user can control the cars manually.
MANUAL_CONTROL = False

# Factor to normalize the inputs to be between 0 and 1.
NORMALIZATION_FACTOR = 100
