from typing import Dict, List, Optional, Tuple, Union

import pygame

from .ai.car_alg_gen import CarAlgGen
from .car import Car
from .track import Track


class RaceInfo:
    def __init__(self, screen: pygame.Surface, track: Track) -> None:
        self.font: pygame.font.Font = pygame.font.Font('freesansbold.ttf', 16)
        self.small_font: pygame.font.Font = pygame.font.Font('freesansbold.ttf', 12)
        self.screen: pygame.Surface = screen
        self.track: Track = track
        self.alg_gen: Optional[CarAlgGen] = None
        self.best_car: Optional[Car] = None
        
    def set_alg_gen(self, alg_gen: CarAlgGen) -> None:
        """Set the reference to the genetic algorithm."""
        self.alg_gen = alg_gen
        
    def draw(self) -> None:
        """Draw all the race information elements to the screen."""
        # Find best car
        alive_cars: List[Car] = [car for car in self.track.cars if car.is_alive()]
        if alive_cars:
            current_best_car: Car = max(alive_cars, key=lambda car: car.get_score())
            if self.best_car is None or current_best_car.get_score() > self.best_car.get_score():
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
                (15, screen_height - 30)
            )
        
        # Draw neural network weights for the best car
        if self.best_car is not None:
            self.draw_neural_network_weights(self.best_car)
    
    def draw_cars_status_panel(self) -> None:
        """Draw the cars status panel with improved styling."""
        # Panel dimensions and positioning
        panel_width: int = 200
        row_height: int = 20
        panel_height: int = len(self.track.cars) * row_height + 52  # Extra space for title and padding
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
            (panel_x + 10, panel_y + 10)
        )
        
        # Draw column headers
        headers: List[str] = ["Car", "Status", "Score"]
        header_positions: List[int] = [10, 50, 120]
        
        for header, x_pos in zip(headers, header_positions):
            self.screen.blit(
                self.small_font.render(header, True, (200, 200, 255)),
                (panel_x + x_pos, panel_y + 35)
            )
        
        # Draw separator line below headers
        pygame.draw.line(
            self.screen,
            (100, 100, 150),
            (panel_x + 5, panel_y + 50),
            (panel_x + panel_width - 5, panel_y + 50),
            1
        )
        
        # Draw car info rows
        for i, car in enumerate(self.track.cars):
            row_y: int = panel_y + 55 + i * row_height
            
            # Car number
            car_num_text: str = f"{i + 1:02d}"
            self.screen.blit(
                self.small_font.render(car_num_text, True, (255, 255, 255)),
                (panel_x + 15, row_y)
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
                (panel_x + 50, row_y)
            )
            
            # Score
            score_text: str = f"{car.get_score():03d}"
            
            # Highlight the best car
            if self.best_car and car.get_score() == self.best_car.get_score():
                score_color: Tuple[int, int, int] = (255, 255, 100)  # Yellow for best car
            else:
                score_color: Tuple[int, int, int] = (255, 255, 255)  # White for others
                
            self.screen.blit(
                self.small_font.render(score_text, True, score_color),
                (panel_x + 120, row_y)
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
            self.font.render(title_text, True, (255, 255, 255)), 
            (nn_x + 10, nn_y + 10)
        )
        
        # Draw score
        score_text: str = f"Score: {car.get_score()}"
        self.screen.blit(
            self.font.render(score_text, True, (255, 255, 100)), 
            (nn_x + 10, nn_y + 35)
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
        l2_neurons: List[Tuple[int, int]] = [(l2_x, layer_y_start + 50)]  # Center vertically
        
        # First, draw the connections (weights) between neurons
        # Weights 0-8: Layer 0 to Layer 1 (3x3 connections)
        # Each input neuron connects to all 3 hidden neurons
        weight_idx: int = 0
        for i in range(3):  # For each input neuron
            for j in range(3):  # For each hidden neuron
                weight: float = weights[weight_idx]
                self._draw_weight_line(
                    l0_neurons[i], 
                    l1_neurons[j], 
                    weight
                )
                weight_idx += 1
        
        # Weights 9-11: Layer 1 to Layer 2 (3x1 connections)
        # Each hidden neuron connects to the single output neuron
        for i in range(3):  # For each hidden neuron
            weight: float = weights[weight_idx]
            self._draw_weight_line(
                l1_neurons[i], 
                l2_neurons[0], 
                weight
            )
            weight_idx += 1
            
        # Now draw the neurons (circles) over the connections
        # Layer names
        layer_names: List[str] = ["Inputs", "Hidden", "Output"]
        layer_positions: List[int] = [l0_x, l1_x, l2_x]
        
        for name, x_pos in zip(layer_names, layer_positions):
            self.screen.blit(
                self.small_font.render(name, True, (200, 200, 255)),
                (x_pos - 20, nn_y + 65)
            )
        
        # Input neuron labels
        input_labels: List[str] = ["L", "M", "R"]  # Left, Middle, Right sensors
        for i, label in enumerate(input_labels):
            self.screen.blit(
                self.small_font.render(label, True, (255, 255, 255)),
                (l0_neurons[i][0] - 30, l0_neurons[i][1] - 7)
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
            (l2_neurons[0][0] + 30, l2_neurons[0][1] - 7)
        )
    
    def _draw_neuron(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """Draw a neuron as a circle."""
        pygame.draw.circle(
            self.screen,
            color,  # Fill color
            position,
            15,  # Radius
            0   # Filled circle
        )
        # Add outline
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),  # White outline
            position,
            15,  # Radius
            2    # Outline width
        )
    
    def _draw_weight_line(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], weight: float) -> None:
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
        pygame.draw.line(
            self.screen,
            color,
            start_pos,
            end_pos,
            width
        )
        
        # Add weight text near the middle of the line
        if magnitude > 0.1:  # Only show significant weights
            mid_x: float = (start_pos[0] + end_pos[0]) / 2
            mid_y: float = (start_pos[1] + end_pos[1]) / 2
            
            weight_text: str = f"{weight:.1f}"
            text_surface: pygame.Surface = self.small_font.render(weight_text, True, (255, 255, 255))
            # Add small black background for better readability
            text_bg: pygame.Surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 2))
            text_bg.fill((0, 0, 0))
            text_bg.set_alpha(150)
            
            self.screen.blit(text_bg, (mid_x - text_surface.get_width()/2 - 2, mid_y - text_surface.get_height()/2 - 1))
            self.screen.blit(text_surface, (mid_x - text_surface.get_width()/2, mid_y - text_surface.get_height()/2))
    
