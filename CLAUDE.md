# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Run game: `python run_game.py` or `./run_game.py`
- Install dependencies: `pip install -r requirements.txt`
- Install in dev mode: `pip install -e .`
- Tests: No test framework implemented yet

## Code Style Guidelines

- **Imports**: Standard library first, then third-party, then local (using relative imports)
- **Formatting**: 4-space indentation, no line length limit enforced
- **Types**: No type annotations used (Python duck typing)
- **Naming**: 
  - Classes: PascalCase
  - Functions/variables: snake_case
  - Constants: UPPER_SNAKE_CASE
- **Error handling**: Use basic try/except blocks where needed
- **File organization**: 
  - Main game logic in src/
  - Settings and configuration in src/config/
  - Assets in assets/ directory

## Project Overview

This is a car racing game built with Pygame that includes a genetic algorithm implementation for AI training. The project uses Python 3.6+ and has minimal dependencies (pygame and numpy).