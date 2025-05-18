import pygame

from .ai.car_rna import CarRNA
from .car import Car
from .config.settings import CAR_IMAGE_PATH, CAR_WIDTH

# Create game objects
init_car_x = 860
init_car_y = 500
max_car_per_line = 5


class Track:
    def __init__(
        self,
        screen: pygame.Surface,
        rnas: list[CarRNA],
        display_width: int,
        display_height: int,
        border_padding: float = 0.1,
        track_width: float = 0.2,
    ):
        """
        Initializes the track.

        Args:
            display_width: Width of the display
            display_height: Height of the display
            border_padding: Padding from the edges of the display
            track_width: Width of the track
        """
        self.rnas = rnas
        self.screen = screen
        self.display_width = display_width
        self.display_height = display_height
        self.border_padding = border_padding
        self.track_width = track_width

        self.car_image = self.get_car_image(CAR_IMAGE_PATH, CAR_WIDTH)

        # Outer boundary rectangle (big)
        self.outer_rect = pygame.Rect(
            display_width * border_padding,
            display_height * border_padding,
            display_width * (1 - 2 * border_padding),
            display_height * (1 - 2 * border_padding),
        )

        # Inner boundary rectangle (small)
        self.inner_rect = pygame.Rect(
            display_width * (border_padding + track_width),
            display_height * (border_padding + track_width),
            display_width * (1 - 2 * (border_padding + track_width)),
            display_height * (1 - 2 * (border_padding + track_width)),
        )

        self.restart_cars(self.rnas)

    def update(self, keys: list[int]):
        # Update cars
        for car in self.cars:
            car.update(keys, self.get_track_lines())

    def draw(self, background_color: tuple[int, int, int]):
        """
        Draws the track on the screen.

        Args:
            screen: Pygame screen object
            background_color: Tuple of RGB values for the background color
        """
        # Fill entire screen first
        self.screen.fill(background_color)

        # Draw outer track (grey)
        pygame.draw.rect(self.screen, (128, 128, 128), self.outer_rect)

        # Draw inner green rectangle (cutout inside the track)
        pygame.draw.rect(self.screen, background_color, self.inner_rect)

        # Optional: Draw borders (lines)
        pygame.draw.rect(self.screen, (255, 0, 0), self.outer_rect, 3)  # Outer border
        pygame.draw.rect(self.screen, (255, 0, 0), self.inner_rect, 3)  # Inner border

        # Draw cars
        for car in self.cars:
            car.draw(self.screen)

    def get_boundary_rects(self) -> list[pygame.Rect]:
        """
        Returns a list of Pygame Rect objects:
        - Each Rect represents a track boundary
        """

        return [self.outer_rect, self.inner_rect]

    def get_rect_lines(
        self, rect: pygame.Rect
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
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

    def get_car_image(self, img_path: str, car_width: int) -> pygame.Surface:
        """
        Returns a scaled car image based on the given width for the current track.
        """
        image = pygame.image.load(img_path).convert_alpha()
        original_width, original_height = image.get_size()
        aspect_ratio = original_height / original_width
        width = car_width
        height = int(width * aspect_ratio)

        return pygame.transform.smoothscale(image, (width, height))

    def generate_cars(self) -> list[Car]:
        cars = []

        for i in range(len(self.rnas)):
            x = init_car_x + (i % max_car_per_line) * 50
            y = init_car_y + (i // max_car_per_line) * 50

            rna = self.rnas[i]

            cars.append(Car(rna, x, y, CAR_IMAGE_PATH, CAR_WIDTH, self.car_image))

        return cars

    def get_all_cars_alive(self) -> int:
        return sum(1 for car in self.cars if car.is_alive())

    def are_all_cars_dead(self) -> bool:
        for car in self.cars:
            if car.is_alive():
                return False

        return True

    def restart_cars(self, rnas: list[CarRNA]):
        self.rnas = rnas

        self.cars = self.generate_cars()
