import pygame

class Track:
    def __init__(self, display_width, display_height, border_padding=0.02):
        self.display_width = display_width
        self.display_height = display_height
        self.border_padding = border_padding
        
        # Calculate rectangle with padding
        self.wall_rect = pygame.Rect(
            0 + border_padding * display_width, 
            0 + border_padding * display_height, 
            display_width - 2 * border_padding * display_width, 
            display_height - 2 * border_padding * display_height
        )
    
    def draw(self, screen):
        # Draw track border
        pygame.draw.rect(screen, (255, 0, 0), self.wall_rect, 2)
    
    def get_wall_rect(self):
        return self.wall_rect
