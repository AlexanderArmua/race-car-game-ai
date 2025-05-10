import pygame


class Track:
    def __init__(self, display_width: int, display_height: int, border_padding: float = 0.1, track_width: float = 0.2):
        """
        Initializes the track.
        
        Args:
            display_width: Width of the display
            display_height: Height of the display
            border_padding: Padding from the edges of the display
            track_width: Width of the track
        """
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
    
    def draw(self, screen: pygame.Surface, background_color: tuple[int, int, int]):
        """
        Draws the track on the screen.
        
        Args:
            screen: Pygame screen object
            background_color: Tuple of RGB values for the background color
        """
        # Fill entire screen first
        screen.fill(background_color)
        
        # Draw outer track (grey)
        pygame.draw.rect(screen, (128, 128, 128), self.outer_rect)
        
        # Draw inner green rectangle (cutout inside the track)
        pygame.draw.rect(screen, background_color, self.inner_rect)
        
        # Optional: Draw borders (lines)
        pygame.draw.rect(screen, (255, 0, 0), self.outer_rect, 3)  # Outer border
        pygame.draw.rect(screen, (255, 0, 0), self.inner_rect, 3)  # Inner border
    
    def get_boundary_rects(self) -> list[pygame.Rect]:
        """
        Returns a list of Pygame Rect objects:
        - Each Rect represents a track boundary
        """

        return [self.outer_rect, self.inner_rect]

    def get_rect_lines(self, rect: pygame.Rect) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Returns a list of lines that define the rectangle:
        - Each tuple contains two points (start and end) that define a line
        - Example: [(x1, y1), (x2, y2)]
        """
        x, y, w, h = rect
        top = ((x, y), (x + w, y))
        right = ((x + w, y), (x + w, y + h))
        bottom = ((x + w, y + h), (x, y + h))
        left = ((x, y + h), (x, y))

        return [top, right, bottom, left]

    def get_track_lines(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Returns a list of lines that define the track:
        - Each tuple contains two points (start and end) that define a line
        - Example: [(x1, y1), (x2, y2)]
        """
        
        lines = []
        for rect in self.get_boundary_rects():
            lines.extend(self.get_rect_lines(rect))

        return lines
