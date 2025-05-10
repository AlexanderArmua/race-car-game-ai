import pygame

from .car import Car
from .track import Track


class RaceInfo:
    def __init__(self, screen: pygame.Surface, track: Track):
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.screen = screen
        self.track = track
        
    def draw(self):
        # Draw background for collision info with transparency
        height = len(self.track.cars) * 17
        
        overlay = pygame.Surface((170, height))
        overlay.set_alpha(128) # 0 = fully transparent, 255 = fully opaque
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (5, 25))

        for i, car in enumerate(self.track.cars):
            text = self.build_car_info_text(car, i)
            
            self.screen.blit(
                self.font.render(text, True, (255, 127, 255)), (10, 30 + i * 16)
            )
    
    def build_car_info_text(self, car: Car, i: int) -> str:
        text = f"{i + 1:02d}: "

        if car.is_alive():
            text += "Alive"
        else:
            text += "Dead"

        text += " | "

        text += f"Score: {car.get_score():03d}"

        return text
    
