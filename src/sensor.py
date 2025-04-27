import pygame
import math

class Sensor:
    def __init__(self, position, angle_degree, sensor_size = 10, ray_length = 300):
        self.x = position[0]
        self.y = position[1]
        self.ray_length = ray_length
        self.angle_rad = math.radians(angle_degree)
        self.sensor_size = sensor_size
        self.ray_color = (255, 0, 255)
        self.sensor_color = (255, 0, 0)

    def update(self, extra_x, extra_y, new_angle):
        self.x = self.x + extra_x
        self.y = self.y + extra_y
        
        if new_angle is not None:
            self.angle_rad += math.radians(new_angle)
        
    def draw(self, screen):
        # Draw sensor square
        # pygame.draw.rect(screen, self.sensor_color, pygame.Rect(self.x, self.y, self.sensor_size, self.sensor_size))

        pygame.draw.circle(screen, self.sensor_color, ((self.x, self.y)), self.sensor_size // 2)

        # Draw sensor ray line
        pygame.draw.line(screen, self.ray_color, 
                        (self.x, self.y), 
                        (
                            self.x + self.ray_length * math.cos(self.angle_rad), 
                            self.y - self.ray_length * math.sin(self.angle_rad)
                        ), 2)

    def check_collision(self, rect):
        intersection = rect.clipline(
                            (self.x, self.y), 
                            (
                                self.x + self.ray_length * math.cos(self.angle_rad), 
                                self.y - self.ray_length * math.sin(self.angle_rad)
                            ))

        return intersection
    
        