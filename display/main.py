import pygame

class Display:
    
    def __init__(self,m):
        
        self.width = 580
        self.height = 650
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.colors = {
            "white":(209, 238, 238),
            "black":(171, 178, 191),
            "font":(0, 0, 0),
            "hover":(128, 138, 135),
            "press":(128, 128, 128),
            "autoOn":(0, 255, 0),
            "autoOff":(255, 0, 0)
        }
        
        self.bg = pygame.image.load("assets\\bg.webp")
    
    def main(self,m):
        
        self.screen.blit(self.bg, (0, 0))
        
        self.buttons(m)
        
    def buttons(self,m):
        
        pos = [50,150]
        
        for i in range(5):
            
            for j in range(5):
                
                pygame.draw.rect(self.screen, (100,100,100), (pos[0], pos[1], 100, 100))
                
            pos[1] += 120