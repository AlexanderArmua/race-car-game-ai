import os
import csv
import glob
import datetime
from typing import List


class MetricsLogger:
    def __init__(self, seed: int):
        """Initialize the metrics logger."""
        self.seed = seed
        self.log_file_path = self._create_log_file()
        self._initialize_csv()

    def _create_log_file(self) -> str:
        """Create a new log file with an incrementing numeric prefix and timestamp.

        Returns:
            str: Path to the created log file
        """
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        # Find the next run number by checking existing files
        next_run_number = self._get_next_run_number(logs_dir)

        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        filename = f"{next_run_number:03d}_{timestamp}.csv"

        return os.path.join(logs_dir, filename)

    def _get_next_run_number(self, logs_dir: str) -> int:
        """Get the next run number by checking existing files.

        Args:
            logs_dir: Directory containing log files

        Returns:
            int: Next run number to use
        """
        # Get all CSV files in the logs directory
        existing_files = glob.glob(os.path.join(logs_dir, "*.csv"))

        if not existing_files:
            return 1  # Start with 001 if no files exist

        # Extract run numbers from existing files
        run_numbers = []
        for file_path in existing_files:
            file_name = os.path.basename(file_path)
            try:
                # Extract numeric prefix (assume format is NNN_*.csv)
                run_number = int(file_name.split('_')[0])
                run_numbers.append(run_number)
            except (ValueError, IndexError):
                # Skip files that don't match the expected format
                continue

        if not run_numbers:
            return 1  # Start with 001 if no valid run numbers found

        # Return the next number after the highest existing one
        return max(run_numbers) + 1

    def _initialize_csv(self):
        """Initialize the CSV file with headers and metadata."""
        with open(self.log_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write metadata first (commented lines that explain the run configuration)
            writer.writerow(['# Metrics Log File'])
            writer.writerow([f'# Random seed value: {self.seed}'])
            writer.writerow(['# ------------------------------'])

            # Write actual headers
            writer.writerow(['generation', 'best_car_score', 'best_weights'])

    def log_generation(self, generation: int, best_car_score: float, best_weights: List[float]):
        """Log metrics for the current generation.

        Args:
            generation: Current generation number
            best_car_score: Score of the best performing car
            best_weights: Neural network weights of the best car
        """
        with open(self.log_file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Convert neurons list to string representation
            weights_str = ','.join([str(n) for n in best_weights])

            # Write the row with generation, score, and neurons (in quotes)
            writer.writerow([generation, best_car_score, f'"{weights_str}"'])

        # Also print to console for immediate feedback
        # print(f"Generation: {generation} - Best car score: {best_car_score}")