import math

import pygame


class Sensor:
    def __init__(self, offset, relative_angle_degree, sensor_size=10, max_ray_length=1000):
        self.offset_x, self.offset_y = offset  # relative to car center
        self.relative_angle_deg = relative_angle_degree  # relative angle
        self.max_ray_length = max_ray_length
        self.sensor_size = sensor_size
        self.ray_color = (255, 0, 255)
        self.sensor_color = (255, 0, 0)
        
        self.x = 0
        self.y = 0
        self.absolute_angle_rad = 0  # to be updated later

        self.current_length = self.max_ray_length
        self.colission_distance = None

    def update(self, car_x: int, car_y: int, car_angle_deg: int, sensor_size: float | None = None):
        car_angle_rad = math.radians(car_angle_deg)

        # For POSITIONS, rotate offset with NEGATIVE car angle
        rotated_x = self.offset_x * math.cos(-car_angle_rad) - self.offset_y * math.sin(-car_angle_rad)
        rotated_y = self.offset_x * math.sin(-car_angle_rad) + self.offset_y * math.cos(-car_angle_rad)

        self.x = car_x + rotated_x
        self.y = car_y + rotated_y

        # For RAY DIRECTIONS, rotate normally (positive)
        total_angle_deg = car_angle_deg + self.relative_angle_deg
        self.absolute_angle_rad = math.radians(total_angle_deg)

        if sensor_size is not None:
            self.current_length = sensor_size
            self.colission_distance = sensor_size
        else:
            self.current_length = self.max_ray_length
            self.colission_distance = None
    
    def draw(self, screen: pygame.Surface):
        # Draw sensor center
        pygame.draw.circle(screen, self.sensor_color, (int(self.x), int(self.y)), self.sensor_size // 2)

        # Draw sensor ray
        end_x = self.x + self.current_length * math.cos(self.absolute_angle_rad)
        end_y = self.y - self.current_length * math.sin(self.absolute_angle_rad)

        pygame.draw.line(screen, self.ray_color, (self.x, self.y), (end_x, end_y), 2)

    def get_distance_to_collision(self, line: tuple[tuple[int, int], tuple[int, int]]) -> float | None:
        """
        Returns the distance to the line between the sensor and the line or None if there is no intersection.
        """
        # 1) compute ray end‐point
        end_x = self.x + self.max_ray_length * math.cos(self.absolute_angle_rad)
        end_y = self.y - self.max_ray_length * math.sin(self.absolute_angle_rad)

        # 2) unpack track segment
        (x1, y1), (x2, y2) = line
        #    and ray segment
        x3, y3 = self.x, self.y
        x4, y4 = end_x, end_y

        # 3) solve intersection via determinant
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None   # parallel or collinear

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

        # 4) intersection only if both parameters in [0,1]
        if 0 <= t <= 1 and 0 <= u <= 1:
            return u * self.max_ray_length

        return None
        
    def get_colission_distance(self) -> float | None:
        return self.colission_distance
