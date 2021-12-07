import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os 
import pyvirtualcam
from pyvirtualcam import PixelFormat
import skimage 
from skimage import color, data  
from VirtualMouse import Mouse   
from main_menu import MainMenu 

from finaltest import Prezentare  
from paint import blackboard  

 



cap = cv2.VideoCapture(0) 
w = 1280
h = 720 
cap.set(3, 1280)
cap.set(4, 720)

mouse = Mouse()  
 
_, img = cap.read() 
mm = MainMenu(mouse,img)    
with pyvirtualcam.Camera(w, h, 30, fmt=PixelFormat.BGR, print_fps=False) as cam:
    print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)') 
    while True:
        success, img = cap.read()    
        img = cv2.flip(img,1) 
        mouse.active(img)   
        img = mm.activate(img,cap)   
        #cv2.imshow("Image", img)
        #
        # # Wait until it's time for the next frame. 
        cam.send(img) # cv2.flip(img,1) 
        cam.sleep_until_next_frame()
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break 
        #cv2.waitKey(1)


