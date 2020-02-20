from InterfazLcd import *
from imageProcessing import *

class menu:
    lcd = InterfazLCD(1)
    imp = ImgProcessing(0)
    
    def __init__(self):
        self.state = 0
    
    def print_menu(self,argument):
        switcher = { 
            0: "Menu Principal de Programa", 
            1: "Iniciar Conteo", 
            2: "Calibrar Contador",
            3: "Resetear Contador", 
        }
        print(switcher.get(argument, "nothing"))
    
    
