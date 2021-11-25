import cv2  
import numpy as np  
import os 



class element:
    def __init__(self,width,height,posx,posy,drawIndex,name,  color): 
        name = str(name) 
        self.cx =posx 
        self.cy = posy 
        self.canvas = np.zeros((height,width,3), np.uint8)  
        self.canvas =  cv2.rectangle(self.canvas, (0, 0), (width, height), color, cv2.FILLED)  

        self.elem = np.zeros((height - 4 ,width - 4, 3), np.uint8)  
        self.elem =  cv2.rectangle(self.elem, (0, 0), (width - 4 , height - 4 ), (255,255,255), cv2.FILLED) 
        

        self.canvas[  2 :height - 2 , 2 :width  - 2 ] = self.elem      

        self.cx1 = self.cx + self.canvas.shape[0] 
        self.cy1 = self.cy + self.canvas.shape[1]

        self.canvas = cv2.putText(self.canvas,f'{name}',( 10 , height - 10 ) , cv2.FONT_HERSHEY_SIMPLEX, 1, 	( 0,0,0 ) , 2, cv2.LINE_AA ) 

        self.drawIndex = drawIndex 
        self.presIndex  = False


    def draw(self,img):
        if self.drawIndex:
            img[self.cx : self.cx1, self.cy : self.cy1 ] = self.canvas


class presentation_table:
    def __init__(self,resizeX,resizeY,posX,posY):
        self.ListNonHover = list ()
        self.ListHover = list ()
        self.resizeX = resizeX 
        self.resizeY = resizeY
        self.posX = posX
        self.posY = posY 
        self.updateY = posY  
        self.updateX = posX
        self.selectedPresentation = None  
        self.presList = os.listdir("prezentare_img") 

        for i in range(0, len(self.presList)): 
            if i != 0:
                self.updateY = self.updateY + self.resizeY
            self.ListNonHover.append(element(self.resizeX,resizeY, self.updateY, self.updateX,True,self.presList[i], (124, 140, 208) )  )   
            self.ListHover.append(element(self.resizeX,resizeY,self.updateY,self.updateX,False,self.presList[i],   ( 37,68,175) ) )   

 


    def changeStateClick(self,drawIndex):
        if drawIndex == True:
            drawIndex = False
        else:
            drawIndex = True 
        return drawIndex 
    
 
    def checkForHover(self,m, obj,index):
        if m.hands:
            if obj.cx < m.lmList1[8][1] <  obj.cx1 and obj.cy < m.lmList1[8][0] < obj.cy1 and self.ListNonHover[index].drawIndex == True:
                obj.drawIndex =  True
                if m.clicked:
                    self.selectedPresentation = index             
            else:
                obj.drawIndex = False 
            






    def draw(self,img,m): 
        for i in range (0, len(self.ListNonHover)):
            self.checkForHover(m,self.ListHover[i],i) 
            if self.ListHover[i].drawIndex == True:
                self.ListHover[i].draw(img) 
            else:
                self.ListNonHover[i].draw(img)




    
        
        
