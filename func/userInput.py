import pygame
import sys

class UserInput:
    
    def __init__(self,m):
        pass
    
    def main(self,m):
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()
                sys.exit()