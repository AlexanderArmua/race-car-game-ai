from typing import Any, Tuple

import pygame


class CarMetric:
    """
    A class to handle the display of car metrics directly above the car.
    This separates the display logic from the car logic.
    """

    def __init__(self) -> None:
        """
        Initialize the car metric display.
        """
        self.font = pygame.font.Font("freesansbold.ttf", 10)

    def draw(
        self,
        screen: pygame.Surface,
        car_x: float,
        car_y: float,
        rect_height: int,
        score: int,
        is_alive: bool,
    ) -> None:
        """
        Draw the car's metrics (score and alive status) above the car.

        Args:
            screen: Pygame surface to draw on
            car_x: X position of the car
            car_y: Y position of the car
            rect_height: Height of the car rectangle
            score: Current score of the car
            is_alive: Whether the car is alive or not
        """
        # Create text for score and status
        score_text = f"Score: {score:03d}"

        if is_alive:
            status_text = "ALIVE"
            status_color = (100, 255, 100)  # Green
        else:
            status_text = "DEAD"
            status_color = (255, 100, 100)  # Red

        # Render text surfaces
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        status_surface = self.font.render(status_text, True, status_color)

        # Create background for better visibility
        bg_width = max(score_surface.get_width(), status_surface.get_width()) + 6
        bg_height = score_surface.get_height() + status_surface.get_height() + 2
        bg_surface = pygame.Surface((bg_width, bg_height))
        bg_surface.set_alpha(150)  # Semi-transparent background
        bg_surface.fill((30, 30, 40))

        # Position above the car
        car_center_x = car_x
        car_top_y = car_y - rect_height // 2

        # Draw background
        bg_pos = (car_center_x - bg_width // 2, car_top_y - bg_height - 5)
        screen.blit(bg_surface, bg_pos)

        # Draw score text
        score_pos = (
            car_center_x - score_surface.get_width() // 2,
            car_top_y - bg_height - 3,
        )
        screen.blit(score_surface, score_pos)

        # Draw status text below score
        status_pos = (
            car_center_x - status_surface.get_width() // 2,
            car_top_y - status_surface.get_height() - 5,
        )
        screen.blit(status_surface, status_pos)
