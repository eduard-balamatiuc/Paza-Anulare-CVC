from paint import blackboard
import cv2 
import cvzone
from cvzone.HandTrackingModule import HandDetector
import os 
import pyvirtualcam
from pyvirtualcam import PixelFormat
import skimage 
from skimage import color, data  
import numpy as np    
from VirtualMouse import Mouse 



class Prezentare:

    def __init__ (self,camWidth,camHeight, blackb, mouse,path): 
        self.mouse = mouse 
        self.b = blackb  
        self.counterSave =0 
        
        self.camWidth = camWidth 
        self.camHeight = camHeight  
        self.canvas2 = np.zeros((self.camHeight,self.camWidth,3), np.uint8) 
        self.canvasShape2 =  np.zeros((self.camHeight,self.camWidth,3), np.uint8)   
        self.canvas1 = np.zeros((self.camHeight,self.camWidth,3), np.uint8) 
        self.canvasShape1 =  np.zeros((self.camHeight,self.camWidth,3), np.uint8)  


        ########## DRAW stuff
        #self.brushThickness = 15 

        #self.drawColor = (0,0,255 ) # B G R   

        self.imgCanvas = np.zeros((self.camHeight,self.camWidth,3), np.uint8) 
        self.imgCanvas2 =  np.zeros((self.camHeight,self.camWidth,3), np.uint8)    

        #ZOOM 
        self.startDist = None
        self.scale = 0
        self.cx, self.cy = 0,0  
        self.newH, self.newW = 0,0  

        self.drawRemovalIndex = 1  
        #self.eraserBool = False 


        #######  
        self.path = path 
        #self.path = [x for x in path if os.path.isdir(x)] 
        #self.imgList = [x for x in os.listdir(self.path) if os.path.isdir(x)]
        self.imgListdemoo = os.listdir(self.path)  

        self.imgList = [ x for x in range ( len(self.imgListdemoo) )  ]  

        for i in range(0, len(self.imgListdemoo)): 
            w =    self.imgListdemoo[i].split("Slide")[-1]  
            w =  int (  w.split(".")[0] ) 
            self.imgList[ w - 1 ] = self.imgListdemoo[i] 

        for i in range(len(self.imgList)):
            self.imgListdemoo[i] = self.imgList[i]
         


        

  
        self.imgIndex = -1   
        self.zoomIndex = 0   
        self.indexCanva = 0   

        #self.imgList = os.listdir(self.path)  
        #for i in range(0, len(self.imgList) ):
            #self.imgList[i] = cv2.imread( f'{self.path}/{self.imgList[i]}' ) 
            #self.imgList[i] = cv2.resize(self.imgList[i], (self.camWidth - 1, self.camHeight - 1 ), False, 0, 0 )  

            
    
    def convertCanva1(self, img ):

        if self.imgIndex  in range(0,len(self.imgList)):


            if self.zoomIndex == 1: 
                
 
            
                try: 
                    self.indexCanva =1  
                    
                        
                    self.imgList[self.imgIndex] = cv2.resize(self.imgList[self.imgIndex], ( self.camWidth - int(self.camWidth/2) , self.camHeight - int(self.camHeight/2) ), False, 0, 0 )     

                    
                    h1, w1, _ =  self.imgList[self.imgIndex].shape
                    self.newH = ((h1+self.scale)//2)*2 
                    self.newW = ((w1+self.scale)//2)*2 

                    self.imgList[self.imgIndex] = cv2.resize(self.imgList[self.imgIndex], (self.newW,self.newH))  
                    
                    imgTest =  cv2.resize(self.imgCanvas, (  self.newW  , self.newH ), False, 0, 0 )  

                    self.imgList[self.imgIndex] = self.converterCanvas(self.imgList[self.imgIndex], imgTest) 

                    
                    
                    img[ self.cy-self.newH//2 : self.cy+ self.newH//2, self.cx-self.newW//2:self.cx+ self.newW//2 ] = self.imgList[self.imgIndex]    

                    self.canvasShape2 = self.canvasShape1  

                        
                    
                    
                    


                    
                
                    
                except: 
                    img = cv2.putText(img, "OUT OF CAMERA's BOUNDS. Either move back or use the zoom gesture again.", (10,600), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, ( 37,68,175), 2, cv2.LINE_AA)
                    self.newH = self.camHeight
                    self.newW = self.camWidth   
                    self.indexCanva = 0   
                    self.canvasShape1 = self.canvasShape2 

                    pass   


            else: 

                try:
                                
                    if self.newH == 0 or self.newW == 0 or self.newH >= self.camHeight-100  or  self.newW >= self.camWidth-100 :
                        
                        self.imgList[self.imgIndex] = cv2.resize(self.imgList[self.imgIndex], ( self.camWidth - 1 , self.camHeight - 1  ), False, 0, 0 ) 

                        
                        imgTest =  cv2.resize(self.imgCanvas, ( self.camWidth -1 , self.camHeight -1 ), False, 0, 0 ) 

                        self.imgList[self.imgIndex] = self.converterCanvas(self.imgList[self.imgIndex], imgTest) 


                        
                        h, w, _  = self.imgList[self.imgIndex].shape                        
                        

                        img[0  : 0 + h, 0 : 0 + w] = self.imgList[self.imgIndex]      

                                
                        
                    else:
                        self.imgList[self.imgIndex] = cv2.resize(self.imgList[self.imgIndex], ( self.newW , self.newH  ) )  

                        
                        imgTest =  cv2.resize(self.imgCanvas, ( self.newW , self.newH), False, 0, 0 )  

                        self.imgList[self.imgIndex] = self.converterCanvas(self.imgList[self.imgIndex], imgTest)  



                    
                        img[self.cy-self.newH//2 : self.cy+ self.newH//2, self.cx-self.newW//2:self.cx+ self.newW//2 ] = self.imgList[self.imgIndex]    
                        

                        
                        
                except:
                    img = cv2.putText(img, "OUT OF CAMERA's BOUNDS.Either move back or use the zoom gesture again.", (10,700), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, ( 37,68,175), 2, cv2.LINE_AA) 
                    pass
        
            


            ######## 
        return img  


        
    def convertCanva2(self,img):

        ## CONVERT draw
        if self.drawRemovalIndex == 1 and self.indexCanva == 1:  
            img = self.converterCanvas(img,self.imgCanvas2)

          

        elif self.drawRemovalIndex ==  1:  
            pass 
        
    
        else:   
            self.imgCanvas = np.zeros((720,1280,3), np.uint8)  
            self.imgCanvas2 = np.zeros((720,1280,3), np.uint8)    
            self.canvasShape1 = np.zeros((720,1280,3), np.uint8) 
            self.canvasShape2 = np.zeros((720,1280,3), np.uint8) 
           
        
        return img 






    def skip(self ):

        if  self.mouse.fingerUp1 == [0,0,0,0,1]  and self.imgIndex <= len(self.imgList): 
            self.imgIndex += 1  
            #self.newH, self.newW = 0,0  
            self.drawRemovalIndex = 0  
            self.canvas2 = np.zeros((self.camHeight,self.camWidth,3), np.uint8) 
            self.canvasShape2 =  np.zeros((self.camHeight,self.camWidth,3), np.uint8)   
            self.canvas1 = np.zeros((self.camHeight,self.camWidth,3), np.uint8) 
            self.canvasShape1 =  np.zeros((self.camHeight,self.camWidth,3), np.uint8)   
            self.imgCanvas = np.zeros((self.camHeight,self.camWidth,3), np.uint8) 
            self.imgCanvas2 =  np.zeros((self.camHeight,self.camWidth,3), np.uint8) 
            cv2.waitKey(500) 
             
        elif self.imgIndex in range(0, len(self.imgList)):
            self.drawRemovalIndex = 1
        
        
    def draw(self, img ):    
    
        if self.drawRemovalIndex == 1: 

            ########## DRAWING ##########
            """  

            if fingerUp1 ==[1,1,1,0,0]: 
                cv2.rectangle(img, (x1,y1-25), (x2,y2 + 25), (255,0,255), cv2.FILLED ) 

                if x1 > 1150 and 0 < y1 < 200: 
                    self.eraserBool = False 
                    self.drawColor  = (55,86,50)
                    if self.indexCanva == 0:

                        cv2.circle(self.imgCanvas,(1200,100), 20, self.drawColor, cv2.FILLED) 
                    else:
                        cv2.circle(self.imgCanvas2,(1200,100), 20, self.drawColor, cv2.FILLED)
                else:
                    cv2.circle(self.imgCanvas,(1200,100), 20, (0,0,0), cv2.FILLED) 
                    cv2.circle(self.imgCanvas2,(1200,100), 20, (0,0,0), cv2.FILLED)  

                if x1 > 1150 and 200 < y1 < 400: 
                    self.eraserBool = False
                    self.drawColor  = (87,56,34) 
                    if self.indexCanva == 0:

                        cv2.circle(self.imgCanvas,(1200,300), 20, self.drawColor, cv2.FILLED)
                    else:
                        cv2.circle(self.imgCanvas2,(1200,300), 20, self.drawColor, cv2.FILLED) 
                else:
                    cv2.circle(self.imgCanvas,(1200,300), 20, (0,0,0), cv2.FILLED)
                    cv2.circle(self.imgCanvas2,(1200,300), 20, (0,0,0), cv2.FILLED)

                if x1 >  1150 and 400 < y1 < 600: 
                    self.eraserBool = False
                    self.drawColor  = (53,21,125)
                    if self.indexCanva == 0: 

                        cv2.circle(self.imgCanvas,(1200,500), 20, self.drawColor, cv2.FILLED) 
                    else:
                        cv2.circle(self.imgCanvas2,(1200,500), 20, self.drawColor, cv2.FILLED) 
                else:
                    cv2.circle(self.imgCanvas,(1200,500), 20, (0,0,0), cv2.FILLED)
                    cv2.circle(self.imgCanvas2,(1200,500), 20, (0,0,0), cv2.FILLED) 


                if x1 > 950 and x1 <1050 and 0 < y1 < 50: 
                    self.eraserBool = True 
                    self.drawColor  = (0,0,0) 
                    if self.indexCanva == 0: 

                        cv2.circle(self.imgCanvas,(1050,25), 20, (180,174,226), cv2.FILLED) 
                    else:
                        cv2.circle(self.imgCanvas2,(1050,25), 20, (180,174,226), cv2.FILLED) 
                else:
                    cv2.circle(self.imgCanvas,(1050,25), 20, (0,0,0), cv2.FILLED)
                    cv2.circle(self.imgCanvas2,(1050,25), 20, (0,0,0), cv2.FILLED) 
            """
                    

            if  ( self.newH == 0 and self.newW == 0 ) or   (  self.newH  == self.camHeight  and self.newW  == self.camWidth ) :   
                
                self.indexCanva = 0 

                """
                if self.eraserBool:
                    self.brushThickness = 50
                else:
                    self.brushThickness = 20 
                """ 

                #cv2.line(self.imgCanvas, (xp,yp), (x1,y1), self.drawColor, self.brushThickness )  

                self.imgCanvas= self.b.draw(self.imgCanvas )    

              
                self.canvas1,  self.canvasShape1 = self.b.shapes(self.imgCanvas) 

                #img = self.converterCanvas(img, self.canvasShape1)   
                self.imgCanvas = self.converterCanvas(self.imgCanvas,self.canvas1)  
               

                #img = self.converterCanvas(img, self.canvasShape1) 
            
                    #self.imgCanvas = self.converterCanvas(self.imgCanvas, self.canvasShape1)
                      

               



                #img  = self.converterCanvas(img,self.canvas1)   


                    
 
                  
                
                #img = cv2.bitwise_or(img,canvas1) 
                #img = cv2.bitwise_or(img,canvasShape1)
                #self.imgCanvas = self.converterCanvas(canvas, canvasShape1)  
             

                

            else:


                self.indexCanva = 1  
    

                """
                if self.eraserBool:
                    self.brushThickness = 50
                else:
                    self.brushThickness = 20  
                """ 
                #cv2.line(self.imgCanvas2, (xp,yp), (x1,y1), self.drawColor, self.brushThickness )  

                self.imgCanvas2 = self.b.draw(self.imgCanvas2)  

                self.canvas2,  self.canvasShape2 = self.b.shapes(self.imgCanvas2)

                  

                   

                #self.imgCanvas2 = self.converterCanvas(self.imgCanvas2, self.canvas2) 
                #img = self.converterCanvas(img, self.canvasShape2) 
                self.imgCanvas2 = self.converterCanvas(self.imgCanvas2,self.canvas2)   
              
                #img = self.converterCanvas(img, self.canvasShape2) 

                #img= self.converterCanvas(img , self.canvasShape2)

                #img  = self.converterCanvas(img,self.canvas2)  
                
    

                

                #img = cv2.bitwise_or(img,canvas2)    

            
            
                #img  = self.converterCanvas(img,self.canvas2)  
        

    
                #self.imgCanvas2 = self.converterCanvas(self.imgCanvas2, canvasShape2) 

                #self.imgCanvas2 = self.converterCanvas(self.imgCanvas2,canvas2)  
        
        #img = self.convertCanva1(img) 



        
        return img 

                  
                
    def  converterCanvas(self,frame,canvas): 
        imgGray =  cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)   

        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV ) 

        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR) 

        frame  = cv2.bitwise_and(frame, imgInv)  
        frame = cv2.bitwise_or(frame,canvas) 
        return frame


    def zoom(self,img):    
        lenght = 0 
        # zoom  
        if len(self.mouse.hands) == 2:
            # print(self.detector.fingersUp(hands[0]), self.detector.fingersUp(hands[1]))
            if self.mouse.fingerUp1 == [1, 1, 1, 1, 1] and self.mouse.fingerUp2 == [1, 1, 1, 1, 1]:
                self.zoomIndex = 1

                # point 8 is the tip of the index finger
                if self.startDist is None:
                        #length, info, img = self.detector.findDistance(lmList1[8], lmList2[8], img)
                        self.startDist =  self.mouse.lenCenterHand
        
                    #length, info, img = self.detector.findDistance(lmList1[8], lmList2[8], img)
                self.scale = int((self.mouse.lenCenterHand - self.startDist) // 2)
                self.cx, self.cy = self.mouse.infoHand[4:]

            else:
                self.zoomIndex = 0
        else:
            #self.mouse.detector.maxHands = 1
            self.startDist = None 




    def activate(self, img): 
        if self.mouse.hands:
            self.skip() 


          

        #if self.imgIndex > -1:
            #self.imgList[self.imgIndex] = cv2.imread( f'{self.path}/{self.imgList[self.imgIndex ]}' )  
            #print(self.imgIndex) 
        #if self.imgIndex > -1:
            #self.imgList[self.imgIndex] = cv2.resize ( self.imgList[self.imgIndex], (self.camWidth - 1, self.camHeight - 1 )  ) 

    
        #self.imgList = os.listdir(self.path)  
        #for i in range(0, len(self.imgList) ):
            #self.imgList[i] = cv2.imread( f'{self.path}/{self.imgList[i]}' ) 
            #self.imgList[i] = cv2.resize(self.imgList[i], (self.camWidth - 1, self.camHeight - 1 ), False, 0, 0 )  
        
        if self.imgIndex > -1 and self.imgIndex < len(self.imgList):
            self.imgList[self.imgIndex] = cv2.imread( f'{self.path}/{self.imgListdemoo[self.imgIndex]}' ) 
            self.imgList[self.imgIndex] = cv2.resize(self.imgList[self.imgIndex], (self.camWidth - 1, self.camHeight - 1 ), False, 0, 0 )    
        
        self.zoom(img)  


        
          
        img = self.convertCanva1(img)   
        img = self.draw(img)
        img = self.converterCanvas(img, self.canvasShape1) 
        img = self.converterCanvas(img, self.canvasShape2)
        img = self.convertCanva2(img)   

        if self.mouse.fingerUp1  == [0,0,0,0,0] and self.mouse.fingerUp2 == [0,0,0,0,0] and self.imgIndex >= 0 and self.mouse.hands:
            cv2.imwrite(f'SavedScreens/screen{self.counterSave}.jpg', img) 
            cv2.waitKey(500) 
            self.counterSave = self.counterSave + 1

        #img = self.draw(img)  

        return img 
        
            
        





   