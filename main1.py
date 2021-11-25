import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os 
import pyvirtualcam
from pyvirtualcam import PixelFormat
import skimage 
from skimage import color, data  
from VirtualMouse import Mouse   
from main import MainMenu 

from finaltest import Prezentare  
from paint import blackboard  

 



cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

mouse = Mouse()  
 
_, img = cap.read() 
mm = MainMenu(mouse,img)    

while True:
    success, img = cap.read()    
    img = cv2.flip(img,1) 
    mouse.active(img)   
    img = mm.activate(img)   

    cv2.imshow("Image", img)  
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break 
    cv2.waitKey(1)


