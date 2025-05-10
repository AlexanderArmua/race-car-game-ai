import pygame


class Track:
    def __init__(self, display_width, display_height, border_padding=0.1, track_width=0.2):
        self.display_width = display_width
        self.display_height = display_height
        self.border_padding = border_padding
        self.track_width = track_width
        
        # Outer boundary rectangle (big)
        self.outer_rect = pygame.Rect(
            display_width * border_padding, 
            display_height * border_padding, 
            display_width * (1 - 2 * border_padding), 
            display_height * (1 - 2 * border_padding)
        )
        
        # Inner boundary rectangle (small)
        self.inner_rect = pygame.Rect(
            display_width * (border_padding + track_width), 
            display_height * (border_padding + track_width), 
            display_width * (1 - 2 * (border_padding + track_width)), 
            display_height * (1 - 2 * (border_padding + track_width))
        )
    
    def draw(self, screen, background_color):
        # Fill entire screen first
        screen.fill(background_color)
        
        # Draw outer track (grey)
        pygame.draw.rect(screen, (128, 128, 128), self.outer_rect)
        
        # Draw inner green rectangle (cutout inside the track)
        pygame.draw.rect(screen, background_color, self.inner_rect)
        
        # Optional: Draw borders (lines)
        pygame.draw.rect(screen, (255, 0, 0), self.outer_rect, 3)  # Outer border
        pygame.draw.rect(screen, (255, 0, 0), self.inner_rect, 3)  # Inner border
    
    """
    Returns a list of Pygame Rect objects:
    - Each Rect represents a track boundary
    """
    def get_track_rects(self):
        return [self.outer_rect, self.inner_rect]
