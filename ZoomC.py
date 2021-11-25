import cv2 


class Zoom:
    def __init__(self, mouse): 
        self.startDist = None
        self.scale = 0
        self.cx, self.cy = 500,500  
        self.mouse = mouse 
        

    def activate(self,kek):
        #if kek == None:
            #return img 
        
        kek["grImg"] = cv2.imread(f'ImageGraphics\{kek["name"]}.jpg') 
        kek["grImg"] = cv2.resize(kek["grImg"],(400,400), False, 0, 0) 
    
    
        if len(self.mouse.hands) == 2:
            # print(detector.fingersUp(hands[ 0]), detector.fingersUp(hands[ 1]))

            if self.mouse.fingerUp1 == [ 1, 1, 0, 0, 0] and self.mouse.fingerUp2 == [ 1, 1, 0, 0, 0]:
            

                if self.startDist is None:
                    self.startDist = self.mouse.lenCenterHand    
                self.scale = int((self.mouse.lenCenterHand - self.startDist) // 2) 

                self.cx, self.cy = self.mouse.infoHand[ 4:] 

        else:
            self.startDist = None
    
        try:
            h1, w1, _= kek["grImg"].shape
            newH, newW = ((h1+self.scale)//2)*2, ((w1+self.scale)//2)*2 

            kek["grImg"] = cv2.resize(kek["grImg"], (newW,newH)) 
            #img[ self.cy-newH//2 : self.cy+ newH//2, self.cx-newW//2:self.cx+ newW//2] = kek["grImg"] 
            kek["cy"] = self.cy-newH//2 
            kek["cy1"] = self.cy+ newH//2 
            kek["cx"] =  self.cx-newW//2 
            kek["cx1"] =  self.cx+ newW//2
        except: 
            pass  
        
        return kek 


