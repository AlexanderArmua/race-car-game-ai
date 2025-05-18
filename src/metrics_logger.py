import csv
import datetime
import glob
import os
from typing import Any, Dict, List, Optional, Tuple, Union

from .car import Car


class MetricsLogger:
    def __init__(self, seed: int) -> None:
        """
        Initialize the metrics logger.
        
        Args:
            seed: Random seed value used for this run
        """
        self.seed: int = seed
        self.log_file_path: str = self._create_log_file()
        self._initialize_csv()

    def _create_log_file(self) -> str:
        """
        Create a new log file with an incrementing numeric prefix and timestamp.

        Returns:
            Path to the created log file
        """
        # Create logs directory if it doesn't exist
        logs_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        # Find the next run number by checking existing files
        next_run_number: int = self._get_next_run_number(logs_dir)

        # Generate filename with timestamp
        timestamp: str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        filename: str = f"{next_run_number:03d}_{timestamp}.csv"

        return os.path.join(logs_dir, filename)

    def _get_next_run_number(self, logs_dir: str) -> int:
        """
        Get the next run number by checking existing files.

        Args:
            logs_dir: Directory containing log files

        Returns:
            Next run number to use
        """
        # Get all CSV files in the logs directory
        existing_files: List[str] = glob.glob(os.path.join(logs_dir, "*.csv"))

        if not existing_files:
            return 1  # Start with 001 if no files exist

        # Extract run numbers from existing files
        run_numbers: List[int] = []
        for file_path in existing_files:
            file_name: str = os.path.basename(file_path)
            try:
                # Extract numeric prefix (assume format is NNN_*.csv)
                run_number: int = int(file_name.split('_')[0])
                run_numbers.append(run_number)
            except (ValueError, IndexError):
                # Skip files that don't match the expected format
                continue

        if not run_numbers:
            return 1  # Start with 001 if no valid run numbers found

        # Return the next number after the highest existing one
        return max(run_numbers) + 1

    def _initialize_csv(self) -> None:
        """Initialize the CSV file with headers and metadata."""
        with open(self.log_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write metadata first (commented lines that explain the run configuration)
            writer.writerow(['# Metrics Log File'])
            writer.writerow([f'# Random seed value: {self.seed}'])
            writer.writerow(['# ------------------------------'])

            # Write actual headers
            writer.writerow(['generation', 'best_car_score', 'cars_alive', 'best_weights'])

    def log_generation(self, generation: int, best_car_score: float, cars_alive: int, all_cars: List[Car]) -> None:
        """
        Log metrics for the current generation.

        Args:
            generation: Current generation number
            best_car_score: Score of the best performing car
            cars_alive: Number of cars still alive
            all_cars: List of all cars in the current generation
        """
        with open(self.log_file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # List of cars in format [{ score: int, weights: list[float] }]
            cars_list: List[Dict[str, Any]] = [{
                'score': car.get_score(),
                'weights': car.rna.get_chromosomes()
            } for car in all_cars]

            # Convert cars list to string representation
            cars_list_str: str = ','.join([str(car) for car in cars_list])

            # Write the row with generation, score, and neurons (in quotes)
            writer.writerow([generation, best_car_score, cars_alive, f'"{cars_list_str}"'])

        # Also print to console for immediate feedback
        # print(f"Generation: {generation} - Best car score: {best_car_score}")