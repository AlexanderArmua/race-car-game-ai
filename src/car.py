import math
import random

import pygame

from .sensor import Sensor
from .track import Track


class Car:
    def __init__(self, x, y, img_path, width=60):
        self.x = x
        self.y = y
        self.angle = 90
        self.speed = 0.1
        self.turn_speed = 3
        self.alive = True
        self.pause = False
        
        # Load and scale image
        self.image = pygame.image.load(img_path).convert_alpha()
        original_width, original_height = self.image.get_size()
        aspect_ratio = original_height / original_width
        self.width = width
        self.height = int(width * aspect_ratio)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))

        self.rotated_car = pygame.transform.rotate(self.image, self.angle)

        # Useful to get the position of the car in any moment
        self.rect = self.rotated_car.get_rect(center=(self.x, self.y))

        car_width, car_height = self.image.get_size()

        # Sensor offsets (relative to center, without rotation)
        self.sensor_offsets = [
            (car_width // 2, -car_height // 2),  # topleft
            (car_width // 2, 0),                # midtop
            (car_width // 2, car_height // 2),   # topright
        ]

        # Sensors
        self.sensors = [
            Sensor(self.sensor_offsets[0], 45),  # left-top
            Sensor(self.sensor_offsets[1], 0),   # mid-top
            Sensor(self.sensor_offsets[2], -45),   # right-top
        ]
    
    
    def update(self, keys, display_width, display_height):
        if self.pause or not self.alive: return

        new_angle = 0
        
        # Key pressed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: new_angle = self.turn_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: new_angle = -self.turn_speed

        # New angle for the car
        self.angle = (self.angle + new_angle) % 360

        rad = math.radians(self.angle)

        change_x = self.speed * math.cos(rad)
        change_y = -self.speed * math.sin(rad) 

        self.x += change_x
        self.y += change_y

        # Rotate the car image
        self.rotated_car = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_car.get_rect(center=(self.x, self.y))

        # Update sensors position
        self._update_sensors()
                
    def draw(self, screen):
        screen.blit(self.rotated_car, self.rect.topleft)
        
        # Draw sensors
        self._draw_sensors(screen)

    def _update_sensors(self):
        for sensor in self.sensors:
            sensor.update(self.x, self.y, self.angle)
    
    def _draw_sensors(self, screen):
        for sensor in self.sensors:
            sensor.draw(screen)        
                         
    def check_rays_collision(self, track: Track) -> list[float | None]:
        """
        Returns a list of distances to the nearest collision point for each sensor.
        """

        lines = track.get_track_lines()
        sensors = self.sensors

        collisions = []

        for sensor in sensors:
            sensor_colissions: float | None = None

            for line in lines:
                colission = sensor.get_distance_to_collision(line)

                if sensor_colissions is None or (colission is not None and colission < sensor_colissions):
                    sensor_colissions = colission
            
            collisions.append(sensor_colissions)

        return collisions

    def is_alive(self):
        return self.alive

    def get_info(self):
        return {
            'x': self.x,
            'y': self.y,
            'speed': self.speed,
            'alive': self.alive,
            'angle': self.angle
        }

    def change_pause(self):
        self.pause = not self.pause