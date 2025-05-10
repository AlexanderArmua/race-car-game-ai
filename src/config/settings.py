# Car settings
import os

# Game settings
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800
BACKGROUND_COLOR = (0, 140, 0) # Green grass
FPS = 30
CARS_AMOUNT = 20

# Define the path relative to the project root
CAR_IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'car.png')
if not os.path.exists(CAR_IMAGE_PATH):
    raise FileNotFoundError(f"Car image not found at {CAR_IMAGE_PATH}")

CAR_WIDTH = 30
CAR_SPEED = 5

MANUAL_CONTROL = True
