import math
import random
from typing import Any, Dict, List, Optional, Tuple, Union

import pygame

from .ai.car_rna import CarRNA, CarRNAResult
from .car_metric import CarMetric
from .config.settings import CAR_SPEED, CAR_TURN_SPEED, MANUAL_CONTROL
from .sensor import Sensor

# Type aliases for clarity
Point = Tuple[int, int]
Line = Tuple[Point, Point]


class Car:
    def __init__(
        self,
        rna: CarRNA,
        x: float,
        y: float,
        img_path: str,
        width: int = 60,
        image: Optional[pygame.Surface] = None,
    ) -> None:
        """
        Initialize a car with neural network for driving.

        Args:
            rna: Neural network that controls the car
            x: Initial x position
            y: Initial y position
            img_path: Path to the car image file
            width: Width to scale the car image to
            image: Pre-loaded image (optional)
        """
        self.rna: CarRNA = rna
        self.x: float = x
        self.y: float = y
        self.angle: float = 90
        self.speed: float = CAR_SPEED
        self.turn_speed: float = CAR_TURN_SPEED
        self.alive: bool = True
        self.pause: bool = False

        # Load and scale image
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))

        self.rotated_car: pygame.Surface = pygame.transform.rotate(
            self.image, self.angle
        )

        # Useful to get the position of the car in any moment
        self.rect = self.rotated_car.get_rect(center=(self.x, self.y))

        car_width, car_height = self.image.get_size()

        # Sensor offsets (relative to center, without rotation)
        self.sensor_offsets: List[Tuple[int, int]] = [
            (car_width // 2, -car_height // 2),  # topleft
            (car_width // 2, 0),  # midtop
            (car_width // 2, car_height // 2),  # topright
        ]

        # Sensors
        self.sensors: List[Sensor] = [
            Sensor(self.sensor_offsets[0], 45),  # left-top
            Sensor(self.sensor_offsets[1], 0),  # mid-top
            Sensor(self.sensor_offsets[2], -45),  # right-top
        ]
        
        # Car metrics display
        self.metrics: CarMetric = CarMetric()

    def update(self, keys: List[int], lines: List[Line]) -> None:
        """
        Update the car's position, orientation, and state.

        Args:
            keys: List of keyboard inputs
            lines: Track boundary lines for collision detection
        """
        if keys[pygame.K_SPACE]:
            self.pause = not self.pause

        if self.pause or not self.alive:
            return

        new_angle: float = 0

        if MANUAL_CONTROL:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                new_angle = self.turn_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                new_angle = -self.turn_speed
        else:
            result: CarRNAResult = self.rna.get_interpretated_result(
                self.check_rays_collision()
            )

            if result == CarRNAResult.LEFT:
                new_angle = self.turn_speed
            elif result == CarRNAResult.RIGHT:
                new_angle = -self.turn_speed

        # New angle for the car
        self.angle = (self.angle + new_angle) % 360

        rad: float = math.radians(self.angle)

        change_x: float = self.speed * math.cos(rad)
        change_y: float = -self.speed * math.sin(rad)

        self.x += change_x
        self.y += change_y

        # Rotate the car image
        self.rotated_car = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_car.get_rect(center=(self.x, self.y))

        # Update sensors position
        self._update_sensors(lines)

        # Check collisions
        collision: bool = self.check_collision()
        if collision:
            self.alive = False

        if self.alive:
            self.rna.increase_score(1)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the car, its sensors, and metrics on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        screen.blit(self.rotated_car, self.rect.topleft)

        # Draw sensors
        self._draw_sensors(screen)
        
        # Draw metrics above the car
        self.metrics.draw(
            screen=screen,
            car_x=self.x,
            car_y=self.y,
            rect_height=self.rect.height,
            score=self.get_score(),
            is_alive=self.alive
        )

    def _update_sensors(self, lines: List[Line]) -> None:
        """
        Update the position and collision data of all sensors.

        Args:
            lines: Track boundary lines for collision detection
        """
        for sensor in self.sensors:
            sensor_size: Optional[float] = (
                self.get_closest_colission_between_sensor_and_lines(sensor, lines)
            )
            sensor.update(self.x, self.y, self.angle, sensor_size)

    def _draw_sensors(self, screen: pygame.Surface) -> None:
        """
        Draw all sensors on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        for sensor in self.sensors:
            sensor.draw(screen)

    def check_rays_collision(self) -> List[Optional[float]]:
        """
        Returns a list of distances to the nearest collision point for each sensor.

        Returns:
            List of distances (None if no collision detected)
        """
        collisions: List[Optional[float]] = []

        for sensor in self.sensors:
            sensor_collision_distance: Optional[float] = sensor.get_colission_distance()
            collisions.append(sensor_collision_distance)

        return collisions

    def get_closest_colission_between_sensor_and_lines(
        self, sensor: Sensor, lines: List[Line]
    ) -> Optional[float]:
        """
        Find the closest collision between a sensor and track lines.

        Args:
            sensor: The sensor to check collisions for
            lines: Track boundary lines for collision detection

        Returns:
            Distance to the closest collision or None if no collision
        """
        sensor_colissions: Optional[float] = None

        for line in lines:
            colission: Optional[float] = sensor.get_distance_to_collision(line)

            if sensor_colissions is None or (
                colission is not None and colission < sensor_colissions
            ):
                sensor_colissions = colission

        return sensor_colissions

    def is_alive(self) -> bool:
        """
        Returns True if the car is alive, False otherwise.
        """
        return self.alive

    def get_info(self) -> Dict[str, Union[int, float, bool]]:
        """
        Get information about the car's current state.

        Returns:
            Dictionary containing car status information
        """
        return {
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "alive": self.alive,
            "angle": self.angle,
        }

    def check_collision(self) -> bool:
        """
        Check if the car has collided with any track boundary.

        Returns:
            True if collision detected, False otherwise
        """
        for sensor in self.sensors:
            sensor_collision_distance: Optional[float] = sensor.get_colission_distance()

            if (
                sensor_collision_distance is not None
                and sensor_collision_distance <= self.speed
            ):
                return True

        return False

    def change_pause(self) -> None:
        """
        Changes the pause state of the car.
        """
        self.pause = not self.pause

    def get_score(self) -> int:
        """
        Get the current score of the car.

        Returns:
            The car's score
        """
        return self.rna.get_score()
