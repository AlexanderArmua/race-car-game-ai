from typing import Dict, List, Optional, Tuple, Union

import pygame

from .ai.car_alg_gen import CarAlgGen
from .car import Car
from .track import Track


class RaceInfo:
    def __init__(self, screen: pygame.Surface, track: Track) -> None:
        self.font: pygame.font.Font = pygame.font.Font("freesansbold.ttf", 16)
        self.small_font: pygame.font.Font = pygame.font.Font("freesansbold.ttf", 12)
        self.screen: pygame.Surface = screen
        self.track: Track = track
        self.alg_gen: Optional[CarAlgGen] = None
        self.best_car: Optional[Car] = None
        self.generation_data: List[Tuple[int, int]] = []  # (generation, cars_alive)

    def set_alg_gen(self, alg_gen: CarAlgGen) -> None:
        """Set the reference to the genetic algorithm."""
        self.alg_gen = alg_gen

    def update_generation_data(self, generation: int, cars_alive: int) -> None:
        """Update the generation data for the line chart."""
        # Only add new data if it's a new generation
        if not self.generation_data or self.generation_data[-1][0] != generation:
            self.generation_data.append((generation, cars_alive))

    def draw(self) -> None:
        """Draw all the race information elements to the screen."""
        # Find best car
        alive_cars: List[Car] = [car for car in self.track.cars if car.is_alive()]
        if alive_cars:
            current_best_car: Car = max(alive_cars, key=lambda car: car.get_score())
            if (
                self.best_car is None
                or current_best_car.get_score() > self.best_car.get_score()
            ):
                self.best_car = current_best_car

        # Draw cars status panel
        self.draw_cars_status_panel()

        # Draw generation counter at the bottom left
        if self.alg_gen is not None:
            gen_text: str = f"Gen: {self.alg_gen.get_generation()}"

            # Create background for generation text
            gen_overlay: pygame.Surface = pygame.Surface((100, 25))
            gen_overlay.set_alpha(128)
            gen_overlay.fill((50, 50, 50))

            # Position at bottom left with small margin
            screen_height: int = self.screen.get_height()
            self.screen.blit(gen_overlay, (10, screen_height - 35))

            # Render generation text
            self.screen.blit(
                self.font.render(gen_text, True, (255, 255, 255)),
                (15, screen_height - 30),
            )

        # Draw neural network weights for the best car
        if self.best_car is not None:
            self.draw_neural_network_weights(self.best_car)

        # Draw generation chart
        self.draw_generation_chart()

    def draw_cars_status_panel(self) -> None:
        """Draw the cars status panel with improved styling."""
        # Panel dimensions and positioning
        panel_width: int = 200
        row_height: int = 20
        panel_height: int = (
            len(self.track.cars) * row_height + 52
        )  # Extra space for title and padding
        panel_x: int = 10
        panel_y: int = 25

        # Create panel background
        panel: pygame.Surface = pygame.Surface((panel_width, panel_height))
        panel.set_alpha(180)  # More opaque like neural network panel
        panel.fill((30, 30, 40))  # Same color as neural network panel
        self.screen.blit(panel, (panel_x, panel_y))

        # Draw panel title
        title_text: str = "Cars Status"
        self.screen.blit(
            self.font.render(title_text, True, (255, 255, 255)),
            (panel_x + 10, panel_y + 10),
        )

        # Draw column headers
        headers: List[str] = ["Car", "Status", "Score"]
        header_positions: List[int] = [10, 50, 120]

        for header, x_pos in zip(headers, header_positions):
            self.screen.blit(
                self.small_font.render(header, True, (200, 200, 255)),
                (panel_x + x_pos, panel_y + 35),
            )

        # Draw separator line below headers
        pygame.draw.line(
            self.screen,
            (100, 100, 150),
            (panel_x + 5, panel_y + 50),
            (panel_x + panel_width - 5, panel_y + 50),
            1,
        )

        # Draw car info rows
        for i, car in enumerate(self.track.cars):
            row_y: int = panel_y + 55 + i * row_height

            # Car number
            car_num_text: str = f"{i + 1:02d}"
            self.screen.blit(
                self.small_font.render(car_num_text, True, (255, 255, 255)),
                (panel_x + 15, row_y),
            )

            # Status with color (green for alive, red for dead)
            if car.is_alive():
                status_text: str = "ALIVE"
                status_color: Tuple[int, int, int] = (100, 255, 100)  # Green
            else:
                status_text: str = "DEAD"
                status_color: Tuple[int, int, int] = (255, 100, 100)  # Red

            self.screen.blit(
                self.small_font.render(status_text, True, status_color),
                (panel_x + 50, row_y),
            )

            # Score
            score_text: str = f"{car.get_score():03d}"

            # Highlight the best car
            if self.best_car and car.get_score() == self.best_car.get_score():
                score_color: Tuple[int, int, int] = (
                    255,
                    255,
                    100,
                )  # Yellow for best car
            else:
                score_color: Tuple[int, int, int] = (255, 255, 255)  # White for others

            self.screen.blit(
                self.small_font.render(score_text, True, score_color),
                (panel_x + 120, row_y),
            )

    def build_car_info_text(self, car: Car, i: int) -> str:
        """Legacy method kept for compatibility."""
        text = f"{i + 1:02d}: "

        if car.is_alive():
            text += "Alive"
        else:
            text += "Dead"

        text += " | "

        text += f"Score: {car.get_score():03d}"

        return text

    def draw_neural_network_weights(self, car: Car) -> None:
        """Draw neural network visualization for the best car with neurons as circles and weights as colored lines."""
        screen_width: int = self.screen.get_width()
        screen_height: int = self.screen.get_height()

        # Create background for neural network display
        nn_width: int = 320
        nn_height: int = 220
        nn_overlay: pygame.Surface = pygame.Surface((nn_width, nn_height))
        nn_overlay.set_alpha(180)  # More opaque to make visualization clearer
        nn_overlay.fill((30, 30, 40))

        # Position in the right side of the screen
        nn_x: int = screen_width - nn_width - 10
        nn_y: int = screen_height - nn_height - 10

        self.screen.blit(nn_overlay, (nn_x, nn_y))

        # Draw title
        title_text: str = "Best Car Neural Network"
        self.screen.blit(
            self.font.render(title_text, True, (255, 255, 255)), (nn_x + 10, nn_y + 10)
        )

        # Draw score
        score_text: str = f"Score: {car.get_score()}"
        self.screen.blit(
            self.font.render(score_text, True, (255, 255, 100)), (nn_x + 10, nn_y + 35)
        )

        # Get chromosome weights
        weights: List[float] = car.rna.get_chromosomes()

        # Define neuron positions
        neuron_radius: int = 15

        # Layer spacing
        layer_x_spacing: int = 100
        layer_y_start: int = nn_y + 100  # Y-position of the first neuron in each layer

        # Define neuron positions for each layer
        # Layer 0 (input) - 3 neurons
        l0_x: int = nn_x + 40
        l0_neurons: List[Tuple[int, int]] = []
        for i in range(3):
            l0_neurons.append((l0_x, layer_y_start + i * 50))

        # Layer 1 (hidden) - 3 neurons
        l1_x: int = l0_x + layer_x_spacing
        l1_neurons: List[Tuple[int, int]] = []
        for i in range(3):
            l1_neurons.append((l1_x, layer_y_start + i * 50))

        # Layer 2 (output) - 1 neuron
        l2_x: int = l1_x + layer_x_spacing
        l2_neurons: List[Tuple[int, int]] = [
            (l2_x, layer_y_start + 50)
        ]  # Center vertically

        # First, draw the connections (weights) between neurons
        # Weights 0-8: Layer 0 to Layer 1 (3x3 connections)
        # Each input neuron connects to all 3 hidden neurons
        weight_idx: int = 0
        for i in range(3):  # For each input neuron
            for j in range(3):  # For each hidden neuron
                weight: float = weights[weight_idx]
                self._draw_weight_line(l0_neurons[i], l1_neurons[j], weight)
                weight_idx += 1

        # Weights 9-11: Layer 1 to Layer 2 (3x1 connections)
        # Each hidden neuron connects to the single output neuron
        for i in range(3):  # For each hidden neuron
            weight: float = weights[weight_idx]
            self._draw_weight_line(l1_neurons[i], l2_neurons[0], weight)
            weight_idx += 1

        # Now draw the neurons (circles) over the connections
        # Layer names
        layer_names: List[str] = ["Inputs", "Hidden", "Output"]
        layer_positions: List[int] = [l0_x, l1_x, l2_x]

        for name, x_pos in zip(layer_names, layer_positions):
            self.screen.blit(
                self.small_font.render(name, True, (200, 200, 255)),
                (x_pos - 20, nn_y + 65),
            )

        # Input neuron labels
        input_labels: List[str] = ["L", "M", "R"]  # Left, Middle, Right sensors
        for i, label in enumerate(input_labels):
            self.screen.blit(
                self.small_font.render(label, True, (255, 255, 255)),
                (l0_neurons[i][0] - 30, l0_neurons[i][1] - 7),
            )

        # Draw all neurons
        for pos in l0_neurons:
            self._draw_neuron(pos, (100, 200, 255))  # Input neurons in blue

        for pos in l1_neurons:
            self._draw_neuron(pos, (255, 200, 100))  # Hidden neurons in orange

        for pos in l2_neurons:
            self._draw_neuron(pos, (100, 255, 150))  # Output neuron in green

        # Add behavior label for output neuron
        behavior_labels: List[str] = ["<", "^", ">"]  # Left, Straight, Right
        result_value: float = car.rna.get_result([0.5, 0.5, 0.5])  # Sample input

        # Determine which behavior is active based on output value
        if result_value < -0.33:
            behavior_idx: int = 0  # Left
        elif result_value < 0.3:
            behavior_idx: int = 1  # Straight
        else:
            behavior_idx: int = 2  # Right

        # Show all possibilities with current highlighted
        behavior_text: str = ""
        for i, label in enumerate(behavior_labels):
            if i == behavior_idx:
                behavior_text += f"[{label}]"
            else:
                behavior_text += f" {label} "

        self.screen.blit(
            self.small_font.render(behavior_text, True, (255, 255, 255)),
            (l2_neurons[0][0] + 30, l2_neurons[0][1] - 7),
        )

    def _draw_neuron(
        self, position: Tuple[int, int], color: Tuple[int, int, int]
    ) -> None:
        """Draw a neuron as a circle."""
        pygame.draw.circle(
            self.screen, color, position, 15, 0  # Fill color  # Radius  # Filled circle
        )
        # Add outline
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),  # White outline
            position,
            15,  # Radius
            2,  # Outline width
        )

    def _draw_weight_line(
        self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], weight: float
    ) -> None:
        """Draw a connection line between neurons representing a weight."""
        # Determine color based on weight sign
        if weight > 0:
            color: Tuple[int, int, int] = (0, 255, 0)  # Green for positive
        elif weight < 0:
            color: Tuple[int, int, int] = (255, 0, 0)  # Red for negative
        else:
            color: Tuple[int, int, int] = (128, 128, 128)  # Gray for zero

        # Determine line width based on weight magnitude (1-5 pixels)
        magnitude: float = abs(weight)
        width: int = 1 + int(magnitude * 4)  # Scale to 1-5 pixels

        # Draw the line
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

        # Add weight text near the middle of the line
        if magnitude > 0.1:  # Only show significant weights
            mid_x: float = (start_pos[0] + end_pos[0]) / 2
            mid_y: float = (start_pos[1] + end_pos[1]) / 2

            weight_text: str = f"{weight:.1f}"
            text_surface: pygame.Surface = self.small_font.render(
                weight_text, True, (255, 255, 255)
            )
            # Add small black background for better readability
            text_bg: pygame.Surface = pygame.Surface(
                (text_surface.get_width() + 4, text_surface.get_height() + 2)
            )
            text_bg.fill((0, 0, 0))
            text_bg.set_alpha(150)

            self.screen.blit(
                text_bg,
                (
                    mid_x - text_surface.get_width() / 2 - 2,
                    mid_y - text_surface.get_height() / 2 - 1,
                ),
            )
            self.screen.blit(
                text_surface,
                (
                    mid_x - text_surface.get_width() / 2,
                    mid_y - text_surface.get_height() / 2,
                ),
            )

    def draw_generation_chart(self) -> None:
        """Draw a line chart showing generation vs cars alive in the top-right corner."""
        if len(self.generation_data) < 1:
            return  # Need at least 1 point to draw the chart

        # Chart dimensions and positioning
        chart_width: int = 300
        chart_height: int = 200
        margin: int = 10
        
        # Position in top-right corner
        screen_width: int = self.screen.get_width()
        chart_x: int = screen_width - chart_width - margin
        chart_y: int = margin
        
        # Create background for chart
        chart_overlay: pygame.Surface = pygame.Surface((chart_width, chart_height))
        chart_overlay.set_alpha(180)
        chart_overlay.fill((30, 30, 40))
        self.screen.blit(chart_overlay, (chart_x, chart_y))
        
        # Draw title
        title_text: str = "Cars Alive by Generation"
        self.screen.blit(
            self.font.render(title_text, True, (255, 255, 255)),
            (chart_x + 10, chart_y + 10)
        )
        
        # Chart area (leave space for title and labels)
        plot_margin: int = 40
        plot_x: int = chart_x + plot_margin
        plot_y: int = chart_y + plot_margin
        plot_width: int = chart_width - 2 * plot_margin
        plot_height: int = chart_height - 2 * plot_margin
        
        # Draw chart border
        pygame.draw.rect(
            self.screen,
            (100, 100, 150),
            (plot_x, plot_y, plot_width, plot_height),
            2
        )
        
        # Get data ranges
        generations: List[int] = [data[0] for data in self.generation_data]
        cars_alive_values: List[int] = [data[1] for data in self.generation_data]
        
        min_gen: int = min(generations)
        max_gen: int = max(generations)
        min_cars: int = 0  # Always start from 0
        max_cars: int = max(cars_alive_values) if cars_alive_values else 1
        
        # Ensure we have some range to work with
        if max_gen == min_gen:
            max_gen = min_gen + 1
        if max_cars == min_cars:
            max_cars = min_cars + 1
            
        # Draw grid lines and labels
        # Vertical lines (generations)
        num_gen_lines: int = min(5, max_gen - min_gen + 1)
        for i in range(num_gen_lines):
            if num_gen_lines > 1:
                gen_value: float = min_gen + (max_gen - min_gen) * i / (num_gen_lines - 1)
            else:
                gen_value: float = min_gen
            x: int = plot_x + int(plot_width * i / max(1, num_gen_lines - 1)) if num_gen_lines > 1 else plot_x
            
            # Draw grid line
            pygame.draw.line(
                self.screen,
                (70, 70, 80),
                (x, plot_y),
                (x, plot_y + plot_height),
                1
            )
            
            # Draw label
            label: str = f"{int(gen_value)}"
            self.screen.blit(
                self.small_font.render(label, True, (200, 200, 200)),
                (x - 10, plot_y + plot_height + 5)
            )
        
        # Horizontal lines (cars alive)
        num_car_lines: int = 5
        for i in range(num_car_lines):
            cars_value: float = min_cars + (max_cars - min_cars) * i / (num_car_lines - 1)
            y: int = plot_y + plot_height - int(plot_height * i / (num_car_lines - 1))
            
            # Draw grid line
            pygame.draw.line(
                self.screen,
                (70, 70, 80),
                (plot_x, y),
                (plot_x + plot_width, y),
                1
            )
            
            # Draw label
            label: str = f"{int(cars_value)}"
            self.screen.blit(
                self.small_font.render(label, True, (200, 200, 200)),
                (plot_x - 35, y - 6)
            )
        
        # Draw the data points and line chart
        points: List[Tuple[int, int]] = []
        
        for generation, cars_alive in self.generation_data:
            # Convert data to pixel coordinates
            x_ratio: float = (generation - min_gen) / (max_gen - min_gen) if max_gen != min_gen else 0
            y_ratio: float = (cars_alive - min_cars) / (max_cars - min_cars) if max_cars != min_cars else 0
            
            pixel_x: int = plot_x + int(x_ratio * plot_width)
            pixel_y: int = plot_y + plot_height - int(y_ratio * plot_height)
            
            points.append((pixel_x, pixel_y))
        
        # Draw the line connecting all points (if we have more than one point)
        if len(points) >= 2:
            pygame.draw.lines(self.screen, (100, 255, 100), False, points, 3)
            
        # Draw points as small circles (even for single points)
        for point in points:
            pygame.draw.circle(self.screen, (255, 255, 100), point, 4)
        
        # Draw axis labels
        # X-axis label
        x_label: str = "Generation"
        x_label_surface: pygame.Surface = self.small_font.render(x_label, True, (255, 255, 255))
        self.screen.blit(
            x_label_surface,
            (plot_x + plot_width // 2 - x_label_surface.get_width() // 2, chart_y + chart_height - 15)
        )
        
        # Y-axis label (rotated would be ideal, but we'll use abbreviated text)
        y_label: str = "Cars"
        y_label_surface: pygame.Surface = self.small_font.render(y_label, True, (255, 255, 255))
        self.screen.blit(y_label_surface, (chart_x + 5, plot_y + plot_height // 2))
