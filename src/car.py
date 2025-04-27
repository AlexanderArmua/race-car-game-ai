import pygame
import math

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
        
        # Ray properties
        self.ray_length = 300
        self.ray_color = (255, 0, 255)
        self.ray_angle_right = 45
        self.ray_angle_left = 135
        self.angle_rad_right = math.radians(self.ray_angle_right)
        self.angle_rad_left = math.radians(self.ray_angle_left)
        
    def update(self, keys, display_width, display_height):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.x > 0:
                self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.x < display_width - self.width:
                self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.y > 0:
                self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.y < display_height - self.height:
                self.y += self.speed
                
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
        # Draw sensors
        self._draw_sensors(screen)
    
    def _draw_sensors(self, screen):
        sensor_size = self.width / 10
        
        # Define sensor positions
        sensor1 = (self.x, self.y)
        sensor2 = (self.x + self.width / 2 - (sensor_size / 5), self.y)
        sensor3 = (self.x + self.width - sensor_size, self.y)
        sensor4 = (self.x, self.y + sensor_size + 2)
        sensor5 = (self.x + self.width - sensor_size, self.y + sensor_size + 2)
        
        # Draw sensor squares
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sensor1[0], sensor1[1], sensor_size, sensor_size))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sensor2[0], sensor2[1], sensor_size, sensor_size))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sensor3[0], sensor3[1], sensor_size, sensor_size))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sensor4[0], sensor4[1], sensor_size, sensor_size))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(sensor5[0], sensor5[1], sensor_size, sensor_size))
        
        # Draw ray lines
        pygame.draw.line(screen, self.ray_color, sensor1, 
                         (sensor1[0] + self.ray_length * math.cos(self.angle_rad_left), 
                          sensor1[1] - self.ray_length * math.sin(self.angle_rad_left)), 2)
        pygame.draw.line(screen, self.ray_color, sensor2, 
                         (sensor2[0], sensor2[1] - self.ray_length), 2)
        pygame.draw.line(screen, self.ray_color, sensor3, 
                         (sensor3[0] + self.ray_length * math.cos(self.angle_rad_right), 
                          sensor3[1] - self.ray_length * math.sin(self.angle_rad_right)), 2)
        pygame.draw.line(screen, self.ray_color, sensor4, 
                         (sensor4[0] - self.ray_length, sensor4[1]), 2)
        pygame.draw.line(screen, self.ray_color, sensor5, 
                         (sensor5[0] + self.ray_length, sensor5[1]), 2)
                         
    def check_ray_collision(self, wall_rect):
        sensor1 = (self.x, self.y)
        ray_end = (sensor1[0] + self.ray_length * math.cos(self.angle_rad_left), 
                  sensor1[1] - self.ray_length * math.sin(self.angle_rad_left))
        
        return wall_rect.clipline(sensor1, ray_end)
    
    def get_info_text(self):
        return f'Car Info: X={self.x}, Y={self.y}, Max speed: {self.speed}'
