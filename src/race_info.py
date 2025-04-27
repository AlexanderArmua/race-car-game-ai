import pygame

class RaceInfo:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 16)

    def draw_car_info(self, screen, car):
        screen.blit(self.font.render(car.get_info_text(), True, (0, 0, 0)), (10, 10))
        
    def draw_collision_info(self, screen, car, track):
        collissions = car.check_rays_collision(track.get_track_rects())

        # Draw background for collision info with transparency
        overlay = pygame.Surface((300, 180))
        overlay.set_alpha(128) # 0 = fully transparent, 255 = fully opaque
        overlay.fill((50, 50, 50))
        screen.blit(overlay, (5, 25))

        for i, collision in enumerate(collissions):
            text = f"Sensor {i} - "

            if not collision:
                text += "No collision"
            else:
                text += f"Hit - ({collision[0]}, {collision[1]})"

            screen.blit(
                self.font.render(text, True, (255, 127, 255)), (10, 30 + i * 16)
            )
    
