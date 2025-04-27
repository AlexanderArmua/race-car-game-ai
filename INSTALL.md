# Installation Guide

This document provides detailed instructions for setting up the Car Racing Game with Genetic AI project.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Setup Steps

### 1. Clone the Repository

```bash
git clone git@github.com:AlexanderArmua/race-car-game-ai.git
cd car-racing
```

### 2. Install SDL Dependencies (Required for Pygame)

**On macOS with Homebrew:**
```bash
# Install SDL libraries
brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-pygame
# OR install the SDL dependencies
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

**On Windows:**
Pygame usually installs without additional dependencies on Windows.

### 3. Create a Virtual Environment (Recommended)

Creating a virtual environment helps isolate project dependencies from your system-wide Python installation.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively, you can install the package in development mode:
```bash
pip install -e .
```

### 5. Verify Installation

Run the game to verify that everything is working correctly:

```bash
# Run the game using the entry point script
python run_game.py

# Alternatively, make it executable and run directly
chmod +x run_game.py
./run_game.py
```

You should see a window open with the car racing game.

## Project Structure

- `src/`: Contains the game's source code
  - `main.py`: Entry point for the game
  - `car.py`: Car class with physics and movement logic
  - `track.py`: Track generation and rendering
  - `sensors.py`: Sensors for collision detection
  - `ai/`: AI-related modules
    - `genetic.py`: Genetic algorithm implementation
    - `neural.py`: Neural network for the car agents
- `assets/`: Game assets like images and sounds
- `config/`: Configuration files
- `tests/`: Unit and integration tests

## Running Tests

-- ToDo

## Troubleshooting

### Common Issues

1. **Missing SDL dependencies**: Pygame relies on SDL libraries, which need to be installed:
   - macOS: `brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf`
   - Ubuntu/Debian: `sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev`

2. **Missing dependencies**: Make sure you've installed all dependencies with `pip install -r requirements.txt`

3. **Import errors**: If you get import errors when running the game, check that your current directory structure matches the expected structure, or adjust the import paths accordingly.

4. **File not found errors**: Ensure that the path to assets (like the car image) is correct. The path might need to be adjusted depending on whether you're using the original main.py or the refactored version.

### Getting Help

If you encounter any issues, please open an issue on the project's GitHub page.