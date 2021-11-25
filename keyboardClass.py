import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone 
from VirtualMouse import Mouse 



class KeyboardClass: 
    def __init__(self,mouse): 

  
        self.boardIndex = 0   
        self.temp = 0 
        self.word = "none" 
        self.mouse = mouse

        self.keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", ],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L" ],
                ["Z", "X", "C", "V", "B", "N", "M","del", "Meth" ] ]


        self.keys2 = [["acos", "asin", "cos", "sin", "tan","*", "+", "-", "/","^","(", ")"], 
                ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "del" ], 
                ["i", "y", "z", "rad", "log", "exp", "ln", "pi","x", "BACK" ] ]  

        
        class Button():
            def __init__(self, pos, text, size):
                self.pos = pos
                self.size = size
                self.text = text 
                        
        

        self.finalFont = 5
        self.cx,self.cy = 300,430   

        self.finalText = ""
        self.wordList =  []   
        self.indexWord = 0   
        self.dictInit = {  
        "word": self.finalText,  
        "cx" : self.cx , 
        "cy" :  self.cy
        }   

        self.wordList.append(self.dictInit) 

        
        self.buttonList = [] 
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):

                self.buttonList.append(Button([100 * j + 50, 100 * i + 50], key,[85,85]))  #  scale*x/y + pos  


        self.buttonList2 = [] 
        for i in range(len(self.keys2)):
            for j, key in enumerate(self.keys2[i]):
                self.buttonList2.append(Button([100 * j + 50 , 100 * i + 50], key,[85,85]))  #  scale*x/y + pos  
    



    def drawAll(self,img, buttonList):

        for button in buttonList:

            x, y = button.pos
            w, h = button.size
            cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                            20, rt=0)
            cv2.rectangle(img, button.pos, (x + w, y + h), (124, 140, 208), cv2.FILLED)
            if len(button.text) > 1:
                cv2.putText(img, button.text, (x + 5, y + 50), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2) 
            else:
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4) 

        return img,buttonList 

    

    
    def activate(self,img):

        if self.mouse.hands and  self.mouse.fingerUp1 ==  [1, 1, 1,  0, 0 ]:

            if self.boardIndex == 0:
                img, self.temp = self.drawAll(img, self.buttonList) 
            if self.boardIndex == 1:
                img, self.temp = self.drawAll(img,self.buttonList2) 

            
            for button in self.temp:
                x, y = button.pos
                w, h = button.size 
            
        
                if x < self.mouse.lmList1[8][0] < x + w and y < self.mouse.lmList1[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), ( 37,68,175  ), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4) 
            
                    ## when clicked
                    if self.mouse.clicked: 
                        if button.text == "Meth": 
              
                            self.boardIndex = 1  
                            break 
                        if button.text == "BACK": 
                
                            self.boardIndex = 0
                            break
                        
                        
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4) 
                    

                        if self.wordList[self.indexWord]["cx"] != 300 and self.wordList[self.indexWord]["cy"] != 430:
                            self.cx = 300
                            self.cy = 430 
                            self.finalText= "" 
                            self.finalText+= button.text  
                            self.dictInit = {  
                            "word" : self.finalText,
                            "cx" : self.cx ,  
                            "cy" : self.cy  
                            } 
                            self.wordList.append(self.dictInit)
                            self.indexWord += 1   
                        
                        else:
                            if button.text == 'del' and self.finalText!= "": 
                                self.finalText = self.finalText[:len(self.finalText) - 1] 
                            
                            else:
                                if button.text != 'del':
                                    self.finalText+= button.text
                            self.wordList[self.indexWord]["word"] =  f'{self.finalText}'
                     
            
                            
                    

        
        



        if self.mouse.hands and  self.mouse.fingerUp1 == [ 0, 1, 1, 0,  0 ]: 
            
            cursor = self.mouse.lmList1[8]   
            if self.mouse.distanceIndexLongFingers < 30:
                cursor = self.mouse.lmList1[8] 
                for index in range(0,len(self.wordList)): #len(Wordlist)
                    if  self.wordList[index]["cx"]  - 50  < cursor[0]  < self.wordList[index]["cx"] + 50  and self.wordList[index]["cy"] - 50 < cursor[1] < self.wordList[index]["cy"] +50:
                        self.wordList[index]["cx"] , self.wordList[index]["cy"] = cursor 
                        self.cx,self.cy = cursor 
                        cv2.rectangle(img, (1220,100), (1270, 150), ( 37,68,175  ), cv2.FILLED) 
                        cv2.putText(img,"T",( 1230,130 ) , cv2.FONT_HERSHEY_SIMPLEX, 1, 	( 28,46,102 ) , 2, cv2.LINE_AA )  
                        if  self.wordList[index]["cx"] in range(1220, 1270) and self.wordList[index]["cy"] in range(100,150): 
                            self.wordList.pop(index) 
                       
                            if self.indexWord ==0:
                                self.finalText= "" 
                                self.dictInit = {  
                                    "word": self.finalText, 
                                    "cx" :300 , 
                                    "cy" :430
                                    }  
                                self.wordList.append(self.dictInit) 
                            
                            else: 
                                self.indexWord -= 1 
                            break  
                        
                        cv2.rectangle(img, (1220, 200), (1270, 250), (37,68,175  ), cv2.FILLED)  
                        cv2.putText(img,"G",( 1230,230 ) , cv2.FONT_HERSHEY_SIMPLEX, 1, 	( 28,46,102 ) , 2, cv2.LINE_AA )
                        if  self.wordList[index]["cx"] in range(1220, 1270) and self.wordList[index]["cy"] in range(200,250): 
                            self.word = self.wordList[index]["word"] 
                            self.wordList.pop(index) 
                         
                            if self.indexWord ==0:
                                self.finalText= "" 
                                self.dictInit = {  
                                    "word": self.finalText,
                                     "cx" :300 , 
                                    "cy" :430
                                    }  
                                self.wordList.append(self.dictInit) 
                            
                            else: 
                                self.indexWord -= 1  
                            print(self.word) 
                            return img, self.word  
                            break 
                        
                        

        for indexW in range(0, len(self.wordList) ):
            cv2.putText(img, self.wordList[indexW]["word"], (self.wordList[indexW]["cx"], self.wordList[indexW]["cy"] ),
                        cv2.FONT_HERSHEY_PLAIN, self.finalFont, (255, 0, 0), self.finalFont)    

        
        return img, None 

            
                
    
            
    
       





