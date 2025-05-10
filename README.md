# Car Racing Game with Genetic AI

A car racing game built with Pygame, featuring a genetic algorithm that learns to navigate any track.

## Project Overview

This project consists of two main components:
1. A car racing game with basic physics and collision detection
2. A genetic algorithm implementation that trains AI agents to drive on any track

![image](https://github.com/user-attachments/assets/00aacacb-81f0-436b-ab77-69e51edafe0b)


## Installation

### Prerequisites

#### macOS
```bash
# Install SDL dependencies (required for Pygame)
brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf pkg-config
```

#### Ubuntu/Debian
```bash
# Install SDL dependencies
sudo apt-get install python3-pygame
# OR install the SDL dependencies
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

### First-time Setup

```bash
# Clone the repository
git clone git@github.com:AlexanderArmua/race-car-game-ai.git
cd car-racing

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Game

```bash
# If returning to the project after previously setting it up:
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the game
python run_game.py
```

### Controls
- Arrow keys or WASD to move the car
- Space to pause the game
- Esc to quit

## Project Structure

```
├── run_game.py         # Entry point script
├── src/                # Source code
│   ├── main.py         # Main game logic
│   ├── car.py          # Car class and physics
│   ├── track.py        # Track generation and rendering
│   ├── sensor.py       # Sensors for collision detection
│   ├── race_info.py    # Race information display
│   └── config/         # Configuration files
│       └── settings.py # Game settings
├── assets/             # Game assets (images, sounds)
│   └── car.png         # Car sprite
├── README.md           # Project documentation
├── INSTALL.md          # Detailed installation instructions
└── requirements.txt    # Project dependencies
```

## Development

### Code Formatting

This project uses [Black](https://github.com/psf/black) for code formatting, [isort](https://pycqa.github.io/isort/) for import organization, and [pylint](https://pylint.pycqa.org/) for linting.

#### Setup Development Environment

```bash
# Install development tools
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install black isort pylint
```

#### Formatting Commands

```bash
# Format a single file
black path/to/file.py

# Format all Python files in the project
black .

# Organize imports in a file
isort path/to/file.py

# Organize imports in all Python files
isort .

# Run both formatting tools on the entire project
isort . && black .

# Check code with pylint
pylint path/to/file.py
```

The project also includes VSCode configurations for automatic formatting on save.

## Future Enhancements

- Multiple track layouts
- Enhanced car physics
- Visualization of AI training progress
- Save/load trained AI models

## License

[MIT](LICENSE)
