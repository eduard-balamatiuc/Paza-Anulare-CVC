import cv2  



class element:
    def __init__(self, path,width,height,posx,posy,drawIndex): 
        self.cx =posx 
        self.cy = posy 
        self.elem =  cv2.imread(path) 
        self.elem = cv2.resize(self.elem,(width,height)) 
        self.cx1 = self.cx + self.elem.shape[0] 
        self.cy1 = self.cy + self.elem.shape[1] 
        self.drawIndex = drawIndex


    def draw(self,img):
        if self.drawIndex:
            img[self.cx : self.cx1, self.cy : self.cy1 ] = self.elem


class sport_table:
    def __init__(self,resizeX,resizeY,posX,posY):
        self.ListNonHover = list ()
        self.ListHover = list ()
        self.resizeX = resizeX 
        self.resizeY = resizeY
        self.posX = posX
        self.posY = posY 
        self.trainIndexExName =  None  
      
        self.updateX = self.posX - self.resizeX 
        self.updateY = self.posY + self.resizeY  

        self.ListNonHover.append(element('sportImg/NonHover/1.png',self.resizeX,resizeY,posY,self.updateX, False)  )  
        self.ListNonHover.append(element('sportImg/NonHover/2.png',self.resizeX,resizeY,self.updateY,self.updateX,False ) )  

        self.ListHover.append(element('sportImg/Hover/1.png',self.resizeX,resizeY,posY,self.updateX, False)  )  
        self.ListHover.append(element('sportImg/Hover/2.png',self.resizeX,resizeY,self.updateY,self.updateX,False ) )  

        self.updateY = self.updateY + self.resizeY  

        self.ListNonHover.append(element('sportImg/NonHover/3.png',self.resizeX,resizeY,self.updateY,self.updateX,False) )  

        self.ListHover.append(element('sportImg/Hover/3.png',self.resizeX,resizeY,self.updateY,self.updateX,False) )  

        self.updateY = self.updateY + resizeY 

        self.ListNonHover.append(element('sportImg/NonHover/4.png',self.resizeX,resizeY,self.updateY,self.updateX, False) ) 
        self.ListNonHover.append(element('sportImg/NonHover/test.png',self.resizeX,self.resizeY,posY,posX,True))    
        self.ListNonHover.append(element('sportImg/NonHover/kek.png',self.resizeX*2,self.resizeY,posY,posX +resizeX,True))   

              
        self.ListHover.append(element('sportImg/Hover/4.png',self.resizeX,resizeY,self.updateY,self.updateX, False) ) 
        self.ListHover.append(element('sportImg/Hover/test.png',self.resizeX,self.resizeY,posY,posX,False))    
        self.ListHover.append(element('sportImg/NonHover/kek.png',self.resizeX*2,self.resizeY,posY,posX +resizeX,False)) 
     

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
            else:
                obj.drawIndex = False 
            if m.clicked and index == 4 and obj.cx < m.lmList1[8][1] <  obj.cx1 and obj.cy < m.lmList1[8][0] < obj.cy1 and self.ListNonHover[index].drawIndex == True:
                for j in range(0,4):
                    self.ListNonHover[j].drawIndex = self.changeStateClick(self.ListNonHover[j].drawIndex) 
            if m.clicked and index == 0 and obj.cx < m.lmList1[8][1] <  obj.cx1 and obj.cy < m.lmList1[8][0] < obj.cy1 and self.ListNonHover[index].drawIndex == True:
                self.trainIndexExName = 'squats'
            if m.clicked and index == 1 and obj.cx < m.lmList1[8][1] <  obj.cx1 and obj.cy < m.lmList1[8][0] < obj.cy1 and self.ListNonHover[index].drawIndex == True:
                self.trainIndexExName = 'biceps'
            if m.clicked and index == 2 and obj.cx < m.lmList1[8][1] <  obj.cx1 and obj.cy < m.lmList1[8][0] < obj.cy1 and self.ListNonHover[index].drawIndex == True:
                self.trainIndexExName = 'crunches'
            if m.clicked and index == 3 and obj.cx < m.lmList1[8][1] <  obj.cx1 and obj.cy < m.lmList1[8][0] < obj.cy1 and self.ListNonHover[index].drawIndex == True:
                self.trainIndexExName = 'dips'  
        





    def draw(self,img,m):
        for i in range (0, len(self.ListNonHover)):
             
            self.checkForHover(m,self.ListHover[i],i) 

            if self.ListHover[i].drawIndex == True:
                self.ListHover[i].draw(img) 
            else:
                self.ListNonHover[i].draw(img)




    
        
        
