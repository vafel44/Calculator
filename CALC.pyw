import pygame

from display.main import Display
from func.logic import Logic
from func.userInput import UserInput

class Main:
    
    def __init__(self):
        
        pygame.init()
        
        self.Display = Display(self)
        self.Logic = Logic(self)
        self.UI = UserInput(self)
        
        pygame.display.set_caption("Калькулятор SLL 0.1")
    
    def start(self):
        
        print('Начало работы')
        
        while True:
            
            self.UI.main(self)  
            self.Display.main(self)
            
            pygame.display.flip()
    
Calc = Main()

Calc.start()