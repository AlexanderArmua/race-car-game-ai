import math
import random

import pygame

from .sensor import Sensor
from .track import Track


class Car:
    def __init__(self, x, y, img_path, width=60, track: Track = None):
        self.x = x
        self.y = y
        self.angle = 90
        self.speed = 3
        self.turn_speed = 3
        self.alive = True
        self.pause = False
        self.track = track
        
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
    
    def update(self, keys: list[int]):
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
                
    def draw(self, screen: pygame.Surface):
        screen.blit(self.rotated_car, self.rect.topleft)
        
        # Draw sensors
        self._draw_sensors(screen)

    def _update_sensors(self):
        for sensor in self.sensors:
            sensor_size = self.get_closest_colission_between_sensor_and_lines(sensor)

            sensor.update(self.x, self.y, self.angle, sensor_size)
    
    def _draw_sensors(self, screen: pygame.Surface):
        for sensor in self.sensors:
            sensor.draw(screen)        
                         
    def check_rays_collision(self) -> list[float | None]:
        """
        Returns a list of distances to the nearest collision point for each sensor.
        """

        collisions: list[float | None] = []

        for sensor in self.sensors:
            sensor_collision_distance = sensor.get_colission_distance()

            collisions.append(sensor_collision_distance)

        return collisions

    def get_closest_colission_between_sensor_and_lines(self, sensor: Sensor) -> float | None:
        lines = self.track.get_track_lines()

        sensor_colissions: float | None = None

        for line in lines:
            colission = sensor.get_distance_to_collision(line)

            if sensor_colissions is None or (colission is not None and colission < sensor_colissions):
                sensor_colissions = colission

        return sensor_colissions

    def is_alive(self) -> bool:
        """
        Returns True if the car is alive, False otherwise.
        """
        return self.alive

    def get_info(self) -> dict[str, int | float | bool]:
        return {
            'x': self.x,
            'y': self.y,
            'speed': self.speed,
            'alive': self.alive,
            'angle': self.angle
        }

    def change_pause(self) -> None:
        """
        Changes the pause state of the car.
        """
        self.pause = not self.pause