# Car Racing Game with Genetic AI

A car racing game built with Pygame, featuring a genetic algorithm that learns to navigate any track.

## Project Overview

This project consists of two main components:
1. A car racing game with basic physics and collision detection
2. A genetic algorithm implementation that trains AI agents to drive on any track

![image](https://github.com/user-attachments/assets/00aacacb-81f0-436b-ab77-69e51edafe0b)


## Installation

```bash
# Clone the repository
git clone <your-repository-url>
cd car-racing

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the game
python src/main.py
```

### Controls
- Arrow keys or WASD to move the car
- Esc to quit

## Project Structure

```
├── src/                # Source code
│   ├── main.py         # Entry point
│   ├── car.py          # Car class and physics
│   ├── track.py        # Track generation and rendering
│   ├── sensors.py      # Sensors for collision detection
│   └── ai/             # AI components
│       ├── genetic.py  # Genetic algorithm implementation
│       └── neural.py   # Neural network for the car agents
├── assets/             # Game assets (images, sounds)
│   └── car.png         # Car sprite
├── config/             # Configuration files
│   └── settings.py     # Game and AI settings
├── tests/              # Unit and integration tests
├── README.md           # Project documentation
└── requirements.txt    # Project dependencies
```

## Future Enhancements

- Multiple track layouts
- Enhanced car physics
- Visualization of AI training progress
- Save/load trained AI models

## License

[MIT](LICENSE)
