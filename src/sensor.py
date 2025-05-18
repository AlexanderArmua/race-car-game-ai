import math
from typing import List, Optional, Tuple, Union

import pygame

# Type aliases for clarity
Point = Tuple[int, int]
Line = Tuple[Point, Point]
Color = Tuple[int, int, int]

class Sensor:
    def __init__(self, offset: Tuple[int, int], relative_angle_degree: float, sensor_size: int = 5, max_ray_length: int = 1000) -> None:
        """
        Initialize a distance sensor for collision detection.
        
        Args:
            offset: Position offset from car center (x, y)
            relative_angle_degree: Angle of the sensor relative to car direction
            sensor_size: Radius of the sensor visualization
            max_ray_length: Maximum distance the sensor can detect
        """
        self.offset_x: int = offset[0]  # relative to car center
        self.offset_y: int = offset[1]
        self.relative_angle_deg: float = relative_angle_degree  # relative angle
        self.max_ray_length: int = max_ray_length
        self.sensor_size: int = sensor_size
        self.ray_color: Color = (255, 0, 255)
        self.sensor_color: Color = (255, 0, 0)
        
        self.x: float = 0.0
        self.y: float = 0.0
        self.absolute_angle_rad: float = 0.0  # to be updated later

        self.current_length: float = self.max_ray_length
        self.colission_distance: Optional[float] = None

    def update(self, car_x: float, car_y: float, car_angle_deg: float, sensor_size: Optional[float] = None) -> None:
        """
        Update sensor position and orientation based on car movement.
        
        Args:
            car_x: Car's current x position
            car_y: Car's current y position
            car_angle_deg: Car's current angle in degrees
            sensor_size: New sensor ray length if collision detected
        """
        car_angle_rad: float = math.radians(car_angle_deg)

        # For POSITIONS, rotate offset with NEGATIVE car angle
        rotated_x: float = self.offset_x * math.cos(-car_angle_rad) - self.offset_y * math.sin(-car_angle_rad)
        rotated_y: float = self.offset_x * math.sin(-car_angle_rad) + self.offset_y * math.cos(-car_angle_rad)

        self.x = car_x + rotated_x
        self.y = car_y + rotated_y

        # For RAY DIRECTIONS, rotate normally (positive)
        total_angle_deg: float = car_angle_deg + self.relative_angle_deg
        self.absolute_angle_rad = math.radians(total_angle_deg)

        if sensor_size is not None:
            self.current_length = sensor_size
            self.colission_distance = sensor_size
        else:
            self.current_length = self.max_ray_length
            self.colission_distance = None
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the sensor and its ray on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw sensor center
        pygame.draw.circle(screen, self.sensor_color, (int(self.x), int(self.y)), self.sensor_size // 2)

        # Draw sensor ray
        end_x: float = self.x + self.current_length * math.cos(self.absolute_angle_rad)
        end_y: float = self.y - self.current_length * math.sin(self.absolute_angle_rad)

        pygame.draw.line(screen, self.ray_color, (self.x, self.y), (end_x, end_y), 1)

    def get_distance_to_collision(self, line: Line) -> Optional[float]:
        """
        Calculate the distance to intersection with a line.
        
        Args:
            line: Track boundary line to check for intersection
            
        Returns:
            Distance to the intersection or None if no intersection
        """
        # 1) compute ray end‐point
        end_x: float = self.x + self.max_ray_length * math.cos(self.absolute_angle_rad)
        end_y: float = self.y - self.max_ray_length * math.sin(self.absolute_angle_rad)

        # 2) unpack track segment
        (x1, y1), (x2, y2) = line
        #    and ray segment
        x3, y3 = self.x, self.y
        x4, y4 = end_x, end_y

        # 3) solve intersection via determinant
        denom: float = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None   # parallel or collinear

        t: float = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u: float = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

        # 4) intersection only if both parameters in [0,1]
        if 0 <= t <= 1 and 0 <= u <= 1:
            return u * self.max_ray_length

        return None
        
    def get_colission_distance(self) -> Optional[float]:
        """
        Get the distance to the nearest collision detected by this sensor.
        
        Returns:
            Distance to collision or None if no collision
        """
        return self.colission_distance
