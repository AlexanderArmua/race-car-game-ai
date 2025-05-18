#!/usr/bin/env python3
"""
Entry point for the Car Racing Game

This script imports and runs the main function from the src package,
avoiding import issues and making it easy to launch the game.
"""
import os
import sys

# Add the project root to the Python path to ensure imports work correctly
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main import main

if __name__ == "__main__":
    main()
