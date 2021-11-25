from ZoomC import Zoom 
from VirtualMouse  import Mouse 
from keyboardClass  import KeyboardClass 
from Graphic  import GraphSaveImage  
import cv2


class KeyboardFull:
    def __init__(self,mouse):
        self.m = mouse 
        self.keyboard_class =  KeyboardClass(mouse) 
        self.selectedImg = None 
        self.index = 0  
        self.imgList = list()  
        self.indexImg = None
        self.moveIndex = 0
        self.keyboardIndexTurnOn = 1
        self.z = Zoom(mouse) 
        self.eqInTheBox = None



    def activate(self, img):
            
        if len(self.imgList) > 0:

            for i in range(0,len(self.imgList)):
                if  self.imgList[i]["cx"] - 50 < self.m.lmList1[8][0] < self.imgList[i ]["cx1"]  +  50 and   self.imgList[i]["cy"] - 50 <   self.m.lmList1[8][1] <self.imgList[i]["cy1"] +50:
                    self.keyboardIndexTurnOn = 0 
                    if  self.m.clicked:
                        self.selectedImg = self.imgList[i] 
                        self.imgList.pop(i) 
                        self.imgList.append(self.selectedImg)
                        self.indexImg = len(self.imgList) - 1
                    break           
                else:
                    self.keyboardIndexTurnOn = 1 

            for i in range(0,len(self.imgList)):
                try:
                    img[ self.imgList[i]["cy"]: self.imgList[i]["cy1"], self.imgList[i]["cx"]  :  self.imgList[i]["cx1"] ]= self.imgList[i]["grImg"]  
                except:
                    img = cv2.putText(img, 'Move back or Use the zoom gesture again', (340,360), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255, 0, 0), 2, cv2.LINE_AA)
                    pass  
        
            if  self.selectedImg is not None:
                self.selectedImg = self.z.activate(self.selectedImg)
                if 10 < self.selectedImg["grImg"].shape[0] < 1200 and 10 <  self.selectedImg["grImg"].shape[1] < 700:
                    self.imgList[self.indexImg]= self.selectedImg    

        if self.keyboardIndexTurnOn == 1:

            img,self.eqInTheBox = self.keyboard_class.activate(img)  # _, str   

        if self.eqInTheBox != None:
            gr = 0 
            gr = GraphSaveImage(self.eqInTheBox,-300,300)  
            gr.save_graph_img(self.eqInTheBox)  
            if self.index !=0:
                self.moveIndex += 200 
            self.index += 1
            temp = cv2.imread(f'ImageGraphics\{self.eqInTheBox}.jpg') 
            temp = cv2.resize(temp,(200,200), False, 0, 0)  
            dictInit = {
                "name": self.eqInTheBox, 
            "grImg" : temp, 
            "cy" : 0,  
            "cy1" : temp.shape[1], 
            "cx" : self.moveIndex,
            "cx1" : temp.shape[0] + self.moveIndex
            } 
            self.imgList.append(dictInit)  

        return img  

