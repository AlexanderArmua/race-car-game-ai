import pygame

from .car import Car
from .track import Track
from .ai.car_alg_gen import CarAlgGen


class RaceInfo:
    def __init__(self, screen: pygame.Surface, track: Track):
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.screen = screen
        self.track = track
        self.alg_gen = None
        
    def set_alg_gen(self, alg_gen: CarAlgGen):
        """Set the reference to the genetic algorithm."""
        self.alg_gen = alg_gen
        
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
            
        # Draw generation counter at the bottom left
        if self.alg_gen is not None:
            gen_text = f"Gen: {self.alg_gen.get_generation()}"
            
            # Create background for generation text
            gen_overlay = pygame.Surface((100, 25))
            gen_overlay.set_alpha(128)
            gen_overlay.fill((50, 50, 50))
            
            # Position at bottom left with small margin
            screen_height = self.screen.get_height()
            self.screen.blit(gen_overlay, (10, screen_height - 35))
            
            # Render generation text
            self.screen.blit(
                self.font.render(gen_text, True, (255, 255, 255)), 
                (15, screen_height - 30)
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
    
