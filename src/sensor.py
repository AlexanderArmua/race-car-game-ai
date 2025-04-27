import pygame
import math

class Sensor:
    def __init__(self, offset, relative_angle_degree, sensor_size=10, ray_length=300):
        self.offset_x, self.offset_y = offset  # relative to car center
        self.relative_angle_deg = relative_angle_degree  # relative angle
        self.ray_length = ray_length
        self.sensor_size = sensor_size
        self.ray_color = (255, 0, 255)
        self.sensor_color = (255, 0, 0)
        
        self.x = 0
        self.y = 0
        self.absolute_angle_rad = 0  # to be updated later

    def update(self, car_x, car_y, car_angle_deg):
        car_angle_rad = math.radians(car_angle_deg)

        # For POSITIONS, rotate offset with NEGATIVE car angle
        rotated_x = self.offset_x * math.cos(-car_angle_rad) - self.offset_y * math.sin(-car_angle_rad)
        rotated_y = self.offset_x * math.sin(-car_angle_rad) + self.offset_y * math.cos(-car_angle_rad)

        self.x = car_x + rotated_x
        self.y = car_y + rotated_y

        # For RAY DIRECTIONS, rotate normally (positive)
        total_angle_deg = car_angle_deg + self.relative_angle_deg
        self.absolute_angle_rad = math.radians(total_angle_deg)
    
    def draw(self, screen):
        # Draw sensor center
        pygame.draw.circle(screen, self.sensor_color, (int(self.x), int(self.y)), self.sensor_size // 2)

        # Draw sensor ray
        end_x = self.x + self.ray_length * math.cos(self.absolute_angle_rad)
        end_y = self.y - self.ray_length * math.sin(self.absolute_angle_rad)

        pygame.draw.line(screen, self.ray_color, (self.x, self.y), (end_x, end_y), 2)

    def check_collision(self, rect):
        intersection = rect.clipline(
            (self.x, self.y), 
            (
                self.x + self.ray_length * math.cos(self.absolute_angle_rad), 
                self.y - self.ray_length * math.sin(self.absolute_angle_rad)
            ))

        return intersection
    
        