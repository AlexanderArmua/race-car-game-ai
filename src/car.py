import pygame

from .sensor import Sensor

class Car:
    def __init__(self, x, y, img_path, width=60):
        self.x = x
        self.y = y
        self.speed = 5
        
        # Load image
        self.image = pygame.image.load(img_path).convert_alpha()
        original_width, original_height = self.image.get_size()
        aspect_ratio = original_height / original_width
        self.width = width
        self.height = int(width * aspect_ratio)
        self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        
        # Sensors
        self.sensors = [
            Sensor(self.x, self.y, 135),
            Sensor(self.x + self.width / 2 - (10 / 5), self.y, 90),
            Sensor(self.x + self.width - 10, self.y, 45),
            Sensor(self.x, self.y + 10, 180),
            Sensor(self.x + self.width - 10, self.y + 10, 0)
        ]
        
    def update(self, keys, display_width, display_height):
        change_x = 0
        change_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.x > 0:
                change_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.x < display_width - self.width:
                change_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.y > 0:
                change_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.y < display_height - self.height:
                change_y = self.speed
        
        self.x += change_x
        self.y += change_y
        
        self._update_sensors(change_x, change_y)
                
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
        # Draw sensors
        self._draw_sensors(screen)

    def _update_sensors(self, change_x, change_y):
        for sensor in self.sensors:
            sensor.update(change_x, change_y)
    
    def _draw_sensors(self, screen):
        for sensor in self.sensors:
            sensor.draw(screen)        
                         
    def check_rays_collision(self, wall_rects):
        all_collissions = []

        for rect in wall_rects:
            for sensor in self.sensors:
                intersection = sensor.check_collision(rect)
                if intersection:
                    all_collissions.append(intersection)
                else:
                    all_collissions.append(None)
        
        return all_collissions
    
    def get_info_text(self):
        return f'Car Info: X={self.x}, Y={self.y}, Max speed: {self.speed}'
