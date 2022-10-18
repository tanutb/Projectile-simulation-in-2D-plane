import pygame
from ui import ui 
class Main:
    BG = pygame.image.load('img\BG.jpg')
    def __init__(self):
        self.WIDTH = 1250
        self.HEIGHT = 700
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    def run(self):
        clock = pygame.time.Clock()
        ui1 = ui()
        while ui1.isrunning() :
            self.window.fill((0,0,0))
            self.window.blit(self.BG,(0,0))
            ui1.draw_event(self.window)
            ui1.event_handle(self.window)
            clock.tick(30)
            pygame.display.flip()
            
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("FRA163 G7 Projectile Simulation")
    main = Main()
    main.run()
    pygame.quit()