import pygame

class Sensors:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        
    def draw_collision_info(self, screen, car, track):
        if car.check_ray_collision(track.get_wall_rect()):
            screen.blit(self.font.render("Ray hit the wall!", True, (255, 0, 0)), (10, 30))
    
    def draw_car_info(self, screen, car):
        screen.blit(self.font.render(car.get_info_text(), True, (0, 0, 0)), (10, 10))
