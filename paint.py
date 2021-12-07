from pyvirtualcam import PixelFormat
from VirtualMouse import Mouse
import pyvirtualcam
import numpy as np
import time
import cv2 

States = ['Pencil', 'Eraser', 'Line', 'Patrat', 'Square', 'Cerc', 'Circle', 'None']  


class blackboard:
    def __init__(self, height, width, mouse): 
        self.mouse = mouse
        self.details = (height, width) 

        self.menuBoard = np.zeros((height, width, 3), np.uint8)   
        self.shapeBoard = np.zeros((height, width, 3), np.uint8)  

        self.coord = [0, 0]
        self.color = (100, 255, 255)
        self.grosime = 5
       
        self.activeMenu = False
        self.activeCascade = False
        self.activeSquare = False
        self.activeCircle =  False   
        self.startShapes = False  # THE ERROR 


        self.startPoint = (0, 0) 
        self.lastPoint = (0, 0)
        self.lastMode = 'None' 
        self.last_coord = [0,0]
        self.last_mode = 'None'  

        self.state = States[0] 

        self.moveYindexUpTOdown = 30  
        self.moveXindexRightTOleft = 30


        self.menu = {'details': (200, 200),
                     'tool': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\tool.png'),(50,50)),
                     'tool_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\tool_activ.png'),(50,50)),
                     'stilou': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\pix.png'),(50,50)),
                     'stilou_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\pix_activ.png'),(50,50)),
                     'radiera': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\radiera.png'),(50,50)),
                     'radiera_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\radiera_activ.png'),(50,50)),
                     'shapes': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\shapes.png'), (50, 50)),
                     'shapes_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\shapes_activ.png'), (50, 50)),

                     'squares' : cv2.resize(cv2.imread(r'menu_bb_draw_imgs\squares.png'), (50, 50)),
                     'squares_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\squares_activ.png'), (50, 50)),
                     'circles': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\circles.png'), (50, 50)),
                     'circles_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\circles_activ.png'), (50, 50)),

                     'cerc': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\cerc.png'), (50, 50)),
                     'cerc_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\cerc_activ.png'), (50, 50)),
                     'circle': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\circle.png'), (50, 50)),
                     'circle_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\circle_activ.png'), (50, 50)),

                     'line': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\line.png'), (50, 50)),
                     'line_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\line_activ.png'), (50, 50)),

                     'patrat': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\patrat.png'), (50, 50)),
                     'patrat_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\patrat_activ.png'), (50, 50)),
                     'square': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\square.png'), (50, 50)),
                     'square_activ': cv2.resize(cv2.imread(r'menu_bb_draw_imgs\square_activ.png'), (50, 50))
                     }

    def drawMenu(self ):
        # Draw tool icon
        if self.activeMenu:
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -150 - self.moveXindexRightTOleft :-100 - self.moveXindexRightTOleft] = self.menu['tool_activ'][:, :]
        else:
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -150 - self.moveXindexRightTOleft :-100 - self.moveXindexRightTOleft] = self.menu['tool'][:, :]

            if self.activeSquare:
                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.activeSquare = False
            elif self.activeCircle:
                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.activeCircle = False

            self.activeCascade = False

        # Draw other icons
        if self.state == States[0] and self.activeMenu:
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = self.menu['stilou_activ'][:, :]
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = self.menu['radiera'][:, :]
            if self.activeCascade:
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = self.menu['line'][:,:]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['squares'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circles'][:, :]

                if self.activeSquare:
                    self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['patrat']
                    self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['square']
                elif self.activeCircle:
                    self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['cerc']
                    self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circle']


        elif self.state == States[1] and self.activeMenu:
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = self.menu['stilou'][:, :]
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = self.menu['radiera_activ'][:, :]
            if self.activeCascade:
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = self.menu['line'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['squares'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circles'][:, :]

                if self.activeSquare:
                    self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['patrat']
                    self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['square']
                elif self.activeCircle:
                    self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['cerc']
                    self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circle']


        if self.activeMenu and self.activeCascade:
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -270 - self.moveXindexRightTOleft :-220 - self.moveXindexRightTOleft] = self.menu['shapes_activ'][:,:]
            if self.activeSquare:
                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['patrat']
                self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['square']
            elif self.activeCircle:
                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['cerc']
                self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circle']

            if self.state == States[3]:
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = self.menu['stilou'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = self.menu['radiera'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = self.menu['line_activ'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['squares'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circles'][:, :]

                if self.activeSquare:
                    self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['patrat']
                    self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['square']
                elif self.activeCircle:
                    self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['cerc']
                    self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circle']

            elif self.state == States[4]:
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = self.menu['stilou'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = self.menu['radiera'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = self.menu['line'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['squares_activ'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circles'][:, :]

                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['patrat']
                self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['square_activ']


            elif self.state == States[5]:
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = self.menu['stilou'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = self.menu['radiera'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = self.menu['line'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['squares_activ'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circles'][:, :]

                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['patrat_activ']
                self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['square']


            elif self.state == States[6]:
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = self.menu['stilou'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = self.menu['radiera'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = self.menu['line'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['squares'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circles_activ'][:, :]

                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['cerc']
                self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circle_activ']

            
            elif self.state == States[7]:
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = self.menu['stilou'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = self.menu['radiera'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = self.menu['line'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = self.menu['squares'][:, :]
                self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circles_activ'][:, :]

                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['cerc_activ']
                self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = self.menu['circle'] 
            


        elif self.activeMenu and not self.activeCascade:
            self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -270 - self.moveXindexRightTOleft :-220 - self.moveXindexRightTOleft] = self.menu['shapes'][:,:]
            if self.activeSquare:
                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.activeSquare = False
            if self.activeCircle:
                self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                self.activeCircle = False 
        
        

        # Change state
        if self.mouse.mouseMode == 'Select':
            if ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 150 - self.moveXindexRightTOleft  < self.coord[0] < self.details[1]-100 - self.moveXindexRightTOleft) and not self.activeMenu:
                if (self.mouse.clicked):
                    self.activeMenu = True
            elif ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 150 - self.moveXindexRightTOleft  < self.coord[0] < self.details[1]-100 - self.moveXindexRightTOleft) and self.activeMenu:
                if(self.mouse.clicked):
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -90 - self.moveXindexRightTOleft:-40 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -210 - self.moveXindexRightTOleft:-160 - self.moveXindexRightTOleft] = np.zeros((50,50,3))
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -270 - self.moveXindexRightTOleft :-220 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = np.zeros((50,50,3))
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50,50,3))
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50,50,3))
                    if self.activeSquare:
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.activeSquare = False
                    if self.activeCircle:
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.activeCircle = False

                    self.activeMenu = False 

            elif ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 210 - self.moveXindexRightTOleft < self.coord[0] < self.details[1]-160 - self.moveXindexRightTOleft) and self.activeMenu:
                self.state = States[0]
            elif ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 90 - self.moveXindexRightTOleft < self.coord[0] < self.details[1]-40 - self.moveXindexRightTOleft) and self.activeMenu:
                self.state = States[1]
            elif ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 270 - self.moveXindexRightTOleft  < self.coord[0] < self.details[1] - 220 - self.moveXindexRightTOleft) and self.activeMenu:
                if self.activeCascade and self.mouse.clicked:
                    self.activeCascade = False
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -330 - self.moveXindexRightTOleft:-280 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                    self.menuBoard[ 25 + self.moveYindexUpTOdown :75 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                    if self.activeSquare:
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.activeSquare = False
                    if self.activeCircle:
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.activeCircle = False

                elif not self.activeCascade and self.mouse.clicked:
                    self.activeCascade = True


            if ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 330 - self.moveXindexRightTOleft < self.coord[0] < self.details[1] - 280 - self.moveXindexRightTOleft) and self.activeCascade:
                    self.state = States[3] 

                    
            elif ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 390 - self.moveXindexRightTOleft < self.coord[0] < self.details[1] - 340 - self.moveXindexRightTOleft) and self.activeCascade:
                if self.mouse.clicked:
                    if not self.activeSquare:
                        self.activeSquare = True
                        self.state = States[5]
                    else:
                        self.activeSquare = False
                        self.state = States[0]
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))

                    if self.activeCircle:
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown:195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.activeCircle = False
            elif ( 25 + self.moveYindexUpTOdown  < self.coord[1] < 75 + self.moveYindexUpTOdown) and (self.details[1] - 450 - self.moveXindexRightTOleft < self.coord[0] < self.details[1] - 400 - self.moveXindexRightTOleft) and self.activeCascade:
                if self.mouse.clicked:
                    if not self.activeCircle:
                        self.activeCircle = True
                        self.state = States[7]
                    else:
                        self.activeCircle = False
                        self.state = States[0]
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -450 - self.moveXindexRightTOleft:-400 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))

                    if self.activeSquare:
                        self.menuBoard[85 + self.moveYindexUpTOdown:135 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.menuBoard[145 + self.moveYindexUpTOdown: 195 + self.moveYindexUpTOdown, -390 - self.moveXindexRightTOleft :-340 - self.moveXindexRightTOleft] = np.zeros((50, 50, 3))
                        self.activeSquare = False

            if (85 + self.moveYindexUpTOdown < self.coord[1] < 135 + self.moveYindexUpTOdown) and (self.details[1] - 390 - self.moveXindexRightTOleft < self.coord[0] < self.details[1] - 340 - self.moveXindexRightTOleft) and self.activeSquare:
                self.state = States[5]
            elif (145 + self.moveYindexUpTOdown < self.coord[1] < 195 + self.moveYindexUpTOdown) and (self.details[1] - 390 - self.moveXindexRightTOleft < self.coord[0] < self.details[1] - 340 - self.moveXindexRightTOleft) and self.activeSquare:
                self.state = States[4]

            if (85 + self.moveYindexUpTOdown < self.coord[1] < 135 + self.moveYindexUpTOdown) and (self.details[1] - 450 - self.moveXindexRightTOleft < self.coord[0] < self.details[1] - 400 - self.moveXindexRightTOleft) and self.activeCircle:
                self.state = States[7]
            elif (145 + self.moveYindexUpTOdown < self.coord[1] < 195 + self.moveYindexUpTOdown) and (self.details[1] - 450 - self.moveXindexRightTOleft < self.coord[0] < self.details[1] - 400 - self.moveXindexRightTOleft) and self.activeCircle:
                self.state = States[6]
        
        



    def draw(self, canvas):
        if self.last_coord == [0,0]:
            self.last_coord = self.coord 
        
        

        if self.state == States[0]:
            if self.mouse.mouseMode == 'Draw' and self.last_mode == self.mouse.mouseMode:
                canvas = cv2.line(canvas, self.last_coord, self.coord, self.color, self.grosime)
            elif self.mouse.mouseMode == 'Draw' and self.last_mode != self.mouse.mouseMode:
                canvas = cv2.line(canvas, (self.coord[0]-5, self.coord[1]-5), self.coord, self.color, self.grosime)
        elif self.state == States[1] and self.mouse.mouseMode == 'Draw':
            if self.mouse.mouseMode == 'Draw' and self.last_mode == self.mouse.mouseMode:
                canvas = cv2.line(canvas, self.last_coord, self.coord, (0,0,0), self.grosime*10)
            elif self.mouse.mouseMode == 'Draw' and self.last_mode != self.mouse.mouseMode:
                canvas = cv2.line(canvas, (self.coord[0]-5, self.coord[1]-5), self.coord, (0,0,0), self.grosime*10) 
        
        self.last_coord = self.coord
        self.last_mode = self.mouse.mouseMode

        return canvas 



    def shapes(self,canvas):
        if self.mouse.mouseMode != 'Draw':
            self.startShapes = True 
        elif self.coord != [0,0 ]:
            
             

            if self.state == States[3]:
                if self.startShapes:
                    canvas = cv2.bitwise_or(canvas, self.shapeBoard)
                    self.shapeBoard = np.zeros((self.details[0], self.details[1], 3), np.uint8)
                    self.startPoint = self.coord
                    self.lastPoint = (self.coord[0]+5, self.coord[1]+5)
                    self.shapeBoard = cv2.line(self.shapeBoard, self.startPoint, self.lastPoint, self.color, self.grosime)
                else:
                    self.shapeBoard = cv2.line(self.shapeBoard, self.startPoint, self.lastPoint, (0,0,0), self.grosime)
                    self.lastPoint = self.coord
                    self.shapeBoard = cv2.line(self.shapeBoard, self.startPoint, self.coord, self.color, self.grosime)

            elif self.state == States[4]:
                if self.startShapes:
                    canvas = cv2.bitwise_or(canvas, self.shapeBoard)
                    self.shapeBoard = np.zeros((self.details[0], self.details[1], 3), np.uint8)
                    self.startPoint = self.coord
                    self.lastPoint = (self.coord[0] + 5, self.coord[1] + 5)
                    self.shapeBoard = cv2.rectangle(self.shapeBoard, self.startPoint, self.lastPoint, self.color, -1)
                else:
                    self.shapeBoard = cv2.rectangle(self.shapeBoard, self.startPoint, self.lastPoint, (0,0,0), -1)
                    self.lastPoint = self.coord
                    self.shapeBoard = cv2.rectangle(self.shapeBoard, self.startPoint, self.coord, self.color, -1)

            elif self.state == States[5]:
                if self.startShapes:
                    canvas = cv2.bitwise_or(canvas, self.shapeBoard)
                    self.shapeBoard = np.zeros((self.details[0], self.details[1], 3), np.uint8)
                    self.startPoint = self.coord
                    self.lastPoint = (self.coord[0] + 5, self.coord[1] + 5)
                    self.shapeBoard = cv2.rectangle(self.shapeBoard, self.startPoint, self.lastPoint, self.color, self.grosime)
                else:
                    self.shapeBoard = cv2.rectangle(self.shapeBoard, self.startPoint, self.lastPoint, (0,0,0), self.grosime)
                    self.lastPoint = self.coord
                    self.shapeBoard = cv2.rectangle(self.shapeBoard, self.startPoint, self.coord, self.color, self.grosime)

            elif self.state == States[6]:

                if self.startShapes:
                    canvas = cv2.bitwise_or(canvas, self.shapeBoard)
                    self.shapeBoard = np.zeros((self.details[0], self.details[1], 3), np.uint8)
                    self.startPoint = self.coord
                    self.lastPoint = (self.coord[0] + 5, self.coord[1] + 5)
                    center = (int((self.startPoint[0] + self.lastPoint[0]) / 2), int((self.startPoint[1] + self.lastPoint[1]) / 2))
                    r = int(((self.startPoint[0] - self.lastPoint[0]) ** 2 + (self.startPoint[1] - self.lastPoint[1]) ** 2) ** (1 / 2))
                    self.shapeBoard = cv2.circle(self.shapeBoard, center, r, self.color, -1)
                else:
                    center = (int((self.startPoint[0] + self.lastPoint[0]) / 2), int((self.startPoint[1] + self.lastPoint[1]) / 2))
                    r = int(((self.startPoint[0] - self.lastPoint[0]) ** 2 + (self.startPoint[1] - self.lastPoint[1]) ** 2) ** (1 / 2))
                    self.shapeBoard = cv2.circle(self.shapeBoard, center, r, (0,0,0), -1)
                    self.lastPoint = self.coord

                    center = (int((self.startPoint[0] + self.lastPoint[0]) / 2), int((self.startPoint[1] + self.lastPoint[1]) / 2))
                    r = int(((self.startPoint[0] - self.lastPoint[0]) ** 2 + (self.startPoint[1] - self.lastPoint[1]) ** 2) ** (1 / 2))
                    self.shapeBoard = cv2.circle(self.shapeBoard, center, r, self.color, -1)

            elif self.state == States[7]:

                if self.startShapes:
                    canvas = cv2.bitwise_or(canvas, self.shapeBoard)
                    self.shapeBoard = np.zeros((self.details[0], self.details[1], 3), np.uint8)
                    self.startPoint = self.coord
                    self.lastPoint = (self.coord[0] + 5, self.coord[1] + 5)
                    center = (int((self.startPoint[0] + self.lastPoint[0]) / 2), int((self.startPoint[1] + self.lastPoint[1]) / 2))
                    r = int(((self.startPoint[0] - self.lastPoint[0]) ** 2 + (self.startPoint[1] - self.lastPoint[1]) ** 2) ** (1 / 2))
                    self.shapeBoard = cv2.circle(self.shapeBoard, center, r, self.color, self.grosime)
                else:
                    center = (int((self.startPoint[0] + self.lastPoint[0]) / 2), int((self.startPoint[1] + self.lastPoint[1]) / 2))
                    r = int(((self.startPoint[0] - self.lastPoint[0]) ** 2 + (self.startPoint[1] - self.lastPoint[1]) ** 2) ** (1 / 2))
                    self.shapeBoard = cv2.circle(self.shapeBoard, center, r, (0,0,0), self.grosime)

                    self.lastPoint = self.coord
                    center = (int((self.startPoint[0] + self.lastPoint[0]) / 2), int((self.startPoint[1] + self.lastPoint[1]) / 2))
                    r = int(((self.startPoint[0] - self.lastPoint[0]) ** 2 + (self.startPoint[1] - self.lastPoint[1]) ** 2) ** (1 / 2))
                    self.shapeBoard = cv2.circle(self.shapeBoard, center, r, self.color, self.grosime)            
            self.startShapes = False 
            
        
        return canvas, self.shapeBoard
 

         

    def  converterMenuBoard(self,frame,canvas): 
        imgGray =  cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)   

        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV ) 

        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR) 

        frame  = cv2.bitwise_and(frame, imgInv)  
        frame = cv2.bitwise_or(frame,canvas) 
        return frame


    def start(self,frame ):

        if self.mouse.hands:
            self.coord = self.mouse.lmList1[8] 
        elif self.mouse.mouseMode !='Draw':
            self.coord = [0,0] 
        
        self.drawMenu()  
        frame = self.converterMenuBoard(frame,self.menuBoard) 
        return frame