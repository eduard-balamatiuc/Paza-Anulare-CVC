import numpy as np
import cv2  
import cvzone
from handmodule import HandDetector 


Mods = ['Draw', 'Select', 'None']

class Mouse:
    def __init__(self):
        self.detector = HandDetector(detectionCon=0.90, maxHands = 2) 
        self.mouseMode = Mods[2] 
        self.__clicks = [0,0,0,0,0,0]
        self.clicked = False
        self.distance = 0
        self.__count = 0 
        self.hands = None 
        self.lmList1 = None  
        self.lmList2 = None 
        self.fingerUp1 = None 
        self.fingerUp2 = None 
        self.lenCenterHand = None  
        self.infoHand = None 
        self.distanceIndexLongFingers = None 
        self.prevImgCoords = (0,0) 


    def selectMode(self):
        if self.hands:
            fingers = self.detector.fingersUp(self.hands[0]) 

            if (fingers == [1, 1, 0, 0,0]):

                self.mouseMode = Mods[0]
            elif (fingers == [1, 1, 1, 0,0]):
                self.mouseMode = Mods[1]
            else:
                self.mouseMode = Mods[2]


    def __click(self, frame):
        if self.mouseMode == Mods[1]:
            self.distance, _ , _  = self.detector.findDistance(self.lmList1[8], self.lmList1[12], frame) 
            return True if self.distance < 30 else False
        return False

    def check_click(self, frame):
        if (self.__click(frame)):
            self.__clicks[self.__count] = 1
            if self.__count < 5:
                self.__count += 1
            else:
                self.__count = 0
        else:
            self.__clicks = [0, 0, 0, 0, 0, 0]
            self.__count = 0

        if self.__clicks == [1, 1, 1, 1, 1, 1]:
            self.__clicks = [0, 0, 0, 0, 0, 0]
            print('click')
            self.clicked = True
            return True

        self.clicked = False
        return False 

    def active(self, frame): 
        self.hands, _  =  self.detector.findHands(frame, flipType = False )  

        if self.hands:
            self.lmList1 = self.hands[0]["lmList"] 
            self.fingerUp1 = self.detector.fingersUp(self.hands[0])  
            # Draw/Select/None Mode   
            self.selectMode() 
            # Check cliks
            self.check_click(frame)  
            self.distanceIndexLongFingers, _, _ = self.detector.findDistance(self.lmList1[8], self.lmList1[12], frame)  
            if len(self.hands) == 2:
                self.fingerUp2 = self.detector.fingersUp(self.hands[1] ) 
                self.lmList2 = self.hands[1]["lmList"] 
                self.lenCenterHand, self.infoHand, _ = self.detector.findDistance(self.hands[0]["center"], self.hands[1]["center"], frame) 

    def cursorOverlay(self,frame,paintStr = False, menuCoordY = 0): 
        if paintStr:
            if self.hands and  self.lmList1[8]  not in range ( frame.shape[0] - 100,   frame.shape[0]) and self.lmList1[8]  not in range ( frame.shape[1] - 200,   frame.shape[1]):
                if  self.lmList1[8][0] != self.prevImgCoords[0] and   self.lmList1[8][1]  != self.prevImgCoords[1]:
                    cv2.rectangle(frame, (0, menuCoordY), (frame.shape[1], frame.shape[0] - 100), (255,255,255), cv2.FILLED) 
                    cv2.rectangle(frame, (0, menuCoordY), (frame.shape[1] - 200, frame.shape[0]), (255,255,255), cv2.FILLED)
                    cv2.circle(frame, (self.lmList1[8][0], self.lmList1[8][1]), 5, (255, 0, 255), cv2.FILLED)  
                self.prevImgCoords =  (self.lmList1[8][0], self.lmList1[8][1])
            else: 
                cv2.rectangle(frame, (0, menuCoordY), (frame.shape[1], frame.shape[0] - 100), (255,255,255), cv2.FILLED) 
                cv2.rectangle(frame, (0, menuCoordY), (frame.shape[1] - 200, frame.shape[0]), (255,255,255), cv2.FILLED)
        else:
            if self.hands:
                cv2.circle(frame, (self.lmList1[8][0], self.lmList1[8][1]), 5, (255, 0, 255), cv2.FILLED)

                    
        
    