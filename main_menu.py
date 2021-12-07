import cv2
from numpy.core.fromnumeric import resize
from sportDraw import * 
from presentation_list import presentation_table  
from paint import blackboard  
from finaltest import Prezentare 
from keyboard_full import KeyboardFull 
from train_project import Train 
from emotion import EmotionCheck
from paint_2 import blackboard2   
from check_attendance import CheckAttendance

from deepface import DeepFace
import pandas as pd
import time
from datetime import datetime 
from threading import Timer 
import schedule  

import numpy as np  

from sign_language import SignLClass 

class MainMenu: 

    def __init__(self,mouse,img):            
        self.mouse = mouse  

        self.seconds_to_go_for = 3 # How long the timer will go for
        self.current_time = 0  
        self.ti = 0  
        self.ti2 = 0

        self.schedEmotionIndex = False

        #img stuff 
        self.y_dimension, self.x_dimension = img.shape[:-1]
        self.constant_menu = int((self.y_dimension*6.17283950617)/100)
        self.constant_window_x = int((self.x_dimension*16.5517241379)/100)
        self.constant_window_y = int((self.y_dimension*12.3456790123)/100)
        self.constant_buttons_x = int((self.x_dimension*4.13793103448)/100)
        self.constant_buttons_y = int((self.y_dimension*3.08641975309)/100)  

        self.videoResizeCanva = np.zeros((self.y_dimension,self.x_dimension,3), np.uint8) 
        self.videoResizeCanva =  cv2.rectangle(self.videoResizeCanva, (0, 0), (self.x_dimension, self.y_dimension), (255,255,255), cv2.FILLED)  
        self.videoResizeIndex = False 

        self.sport = sport_table(self.constant_menu, self.constant_menu, self.x_dimension//3 + 6*self.constant_menu-self.constant_menu//2 ,self.constant_menu ) 
        self.sport_table_index = False # 1  

        self.signL = SignLClass()  
        self.signBool =  False 

        self.closeBool = False 



        self.menu = {
                'check_attendance_simple' : cv2.imread('images/check_attendance_simple.png'),
                'check_attendance_active' : cv2.imread('images/check_attendance_active.png'),
                'choose_presentation_simple' : cv2.imread('images/choose_presentation_simple.png'),
                'choose_presentation_active' : cv2.imread('images/choose_presentation_active.png'),
                'close_simple' : cv2.imread('images/close_simple.png'),
                'close_active' : cv2.imread('images/close_active.png'),
                'video_big_simple' : cv2.imread('images/video_big_simple.png'),
                'video_big_active' : cv2.imread('images/video_big_active.png'),
                'video_small_simple' : cv2.imread('images/video_small_simple.png'),
                'video_small_active' : cv2.imread('images/video_small_active.png'),
                'subtitles_simple' : cv2.imread('images/subtitles_simple.png'),
                'subtitles_active' : cv2.imread('images/subtitles_active.png'),
                'sport_simple' :   cv2.imread('images/sport_simple.png'), 
                'sport_active' :   cv2.imread('images/sport_active.png'),
                'brush_simple' :   cv2.imread('images/brush_simple.png'),  
                'brush_active' :   cv2.imread('images/brush_active.png'), 
                'keyboard_simple' :   cv2.imread('images/keyboard_simple.png'), 
                'keyboard_active' :   cv2.imread('images/keyboard_active.png')

        } 



        self.window = {
                    'check_attendance_window' : cv2.imread('images/check_attendance_window.png'), 
                    'check_mood_window' : cv2.imread('images/check_mood_window.png'),
                    'share_presentation_window' : cv2.imread('images/share_presentation_window.png')
        } 
        self.window_bool = { 
                    'check_attendance_window' : False,
                    'check_mood_window' : False,
                    'share_presentation_window' : False,
                    
        }
        self.window_mult_i = { 
                    'check_attendance_window' : 4,
                    'check_mood_window' : 4,
                    'share_presentation_window' : 1
        }

        self.buttons = {'check_button' : cv2.imread('images/check_button.png'),
                    'choose_button' : cv2.imread('images/choose_button.png'),
                    'no_button' : cv2.imread('images/no_button.png'),
                    'yes_button' : cv2.imread('images/yes_button.png')
        } 

        self.menu = self.resize_dict(self.menu, self.constant_menu, self.constant_menu)
        self.window = self.resize_dict(self.window,  self.constant_window_x, self.constant_window_y )
        self.buttons = self.resize_dict(self.buttons, self.constant_buttons_x, self.constant_buttons_y) 

        self.presentation = presentation_table( self.constant_menu*6 , self.constant_menu ,self.x_dimension//3 + 6*self.constant_menu - self.constant_menu//2  - self.buttons['choose_button'].shape[0]//2 , self.constant_menu*3 - self.buttons['choose_button'].shape[0] ) 
        self.presentation_table_index =False    
        self.presIndex = False  #2 

     

        self.b = 0  #blackboard in Presentation 
        self.b2 = blackboard2(720,1280, self.mouse ) #blackboard in Paint  
        self.b2Index = False  
        self.p = 0  #presentation  

        self.t = Train() 
        self.trainActivateIndex = False  #3
        self.tempTrainName = None 

        self.em = EmotionCheck()
        self.emotionIndex = False #4

        self.keyboardGraphIndex = False   #5
        self.keyboard_graph_feature  = KeyboardFull(mouse)  

        self.att = CheckAttendance()   
        self.attIndex = False 
        self.startTime = 0  
        self.attIndexSched = False
        
            

    def resize_dict(self,dictionary, constantx, constanty):

        for i in dictionary:
            dictionary[i] = cv2.resize(dictionary[i], (constantx, constanty))
        return dictionary 
    

    def changeStateClick(self,index): 
        if index == True:
            index = False
        else:
            index = True 
        return index 
    
    def resetWindows(self,activeWindow):
        for element in self.window_bool:
            if element != activeWindow:
                self.window_bool[element] = False  
    
    def video_resize(self,img):
        img = cv2.resize(img, ( 200, 100 ), False, 0, 0 ) 
        self.videoResizeCanva[self.y_dimension - 100 : self.y_dimension,  self.x_dimension - 200 : self.x_dimension] = img  
        self.mouse.cursorOverlay(self.videoResizeCanva,True)
        return self.videoResizeCanva

        


     
 
    def activate(self,img,cap):

        if self.signBool:
            _, imgTemp = cap.read()
            sent = self.signL.activate(imgTemp)    
            imgTemp  = cv2.flip(imgTemp,1)  
            imgTemp = cv2.putText(imgTemp,sent,(300,600),cv2.FONT_HERSHEY_PLAIN,2, ( 37,68,175) ,4) 
            img = imgTemp
        

        if self.videoResizeIndex:
            img = self.video_resize(img)
            

        #Resizing every dictionary elements      
        cv2.rectangle(img, (0, 0), (self.x_dimension, self.constant_menu), (124, 140, 208), cv2.FILLED)
        
        
        #add simple icons 
        img[ 0 :self.menu['choose_presentation_simple'].shape[1],  self.x_dimension//3 + self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + self.constant_menu-self.constant_menu//2 + self.menu['choose_presentation_simple'].shape[0]] = self.menu['choose_presentation_simple']  
        img[ 0 :self.menu['subtitles_simple'].shape[1],  self.x_dimension//3 + 2*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 2*self.constant_menu-self.constant_menu//2 + self.menu['subtitles_simple'].shape[0]] = self.menu['subtitles_simple']
        img[ 0 :self.menu['keyboard_simple'].shape[1],  self.x_dimension//3 + 3*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 3*self.constant_menu-self.constant_menu//2 + self.menu['keyboard_simple'].shape[0]] = self.menu['keyboard_simple']
        img[ 0 :self.menu['check_attendance_simple'].shape[1],  self.x_dimension//3 + 4*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 4*self.constant_menu-self.constant_menu//2 + self.menu['check_attendance_simple'].shape[0]] = self.menu['check_attendance_simple'] 
        if self.videoResizeIndex:
            img[ 0 :self.menu['video_big_simple'].shape[1],  self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 + self.menu['video_big_simple'].shape[0]] = self.menu['video_big_simple']
        else:
            img[ 0 :self.menu['video_small_simple'].shape[1],  self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 + self.menu['video_small_simple'].shape[0]] = self.menu['video_small_simple']
        img[ 0 :self.menu['close_simple'].shape[1],  self.x_dimension - self.constant_menu  - 15 : self.x_dimension - self.constant_menu - 15   + self.menu['close_simple'].shape[0]] = self.menu['close_simple'] 
        img[ 0 :self.menu['sport_simple'].shape[1], self.x_dimension//3 + 6*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 6*self.constant_menu-self.constant_menu//2 + self.menu['sport_simple'].shape[0]] = self.menu['sport_simple'] 
        img[ 0 :self.menu['brush_simple'].shape[1], self.x_dimension//3 + 7*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 7*self.constant_menu-self.constant_menu//2 + self.menu['brush_simple'].shape[0]] = self.menu['brush_simple'] 

        if self.presentation_table_index and self.window_bool['share_presentation_window'] == True :
            self.presentation.draw(img,self.mouse)
            if self.presentation.selectedPresentation is not None:
                self.b = blackboard(720, 1280, self.mouse)
                self.p = Prezentare(1280, 720, self.b,  self.mouse,  f"PresentationFiles/{self.presentation.presList[self.presentation.selectedPresentation ] }" ) 
                self.presentation.selectedPresentation = None 
                self.presentation_table_index = False 
                self.window_bool['share_presentation_window'] = False
                self.presIndex = True 
        




        if self.mouse.hands:
            if self.mouse.lmList1[8][0]  in range(self.x_dimension//3 + self.constant_menu-self.constant_menu//2, self.x_dimension//3 + self.constant_menu-self.constant_menu//2  + self.menu['choose_presentation_simple'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu):
                img[ 0 :self.menu['choose_presentation_active'].shape[1],  self.x_dimension//3 + self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + self.constant_menu-self.constant_menu//2 + self.menu['choose_presentation_active'].shape[0]] = self.menu['choose_presentation_active']  
                if self.mouse.clicked:
                    self.window_bool['share_presentation_window'] = self.changeStateClick(self.window_bool['share_presentation_window'])
                    self.sport_table_index = False #1  
                    self.presentation_table_index = False 
                    self.presIndex = False  #2  
                    self.trainActivateIndex = False  #3 
                    self.emotionIndex = False #4 
                    self.keyboardGraphIndex = False   #5
                    self.resetWindows('share_presentation_window') 
                    self.b2Index = False 



            if self.mouse.lmList1[8][0]  in range(self.x_dimension//3 + 2*self.constant_menu-self.constant_menu//2, self.x_dimension//3 + 2*self.constant_menu-self.constant_menu//2  + self.menu['subtitles_active'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu):
                img[ 0 :self.menu['subtitles_active'].shape[1],  self.x_dimension//3 + 2*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 2*self.constant_menu-self.constant_menu//2 + self.menu['subtitles_active'].shape[0]] = self.menu['subtitles_active']  
                if self.mouse.clicked:
                    self.signBool =  self.changeStateClick(self.signBool) 
                    self.sport_table_index = False #1  
                    self.presentation_table_index = False 
                    self.presIndex = False  #2  
                    self.trainActivateIndex = False  #3 
                    self.emotionIndex = False #4 
                    self.keyboardGraphIndex = False   #5
                    self.resetWindows('None') 
                    self.b2Index = False 
                    self.videoResizeIndex = False

            if self.mouse.lmList1[8][0]  in range(self.x_dimension//3 + 3*self.constant_menu-self.constant_menu//2, self.x_dimension//3 + 3*self.constant_menu-self.constant_menu//2  + self.menu['keyboard_active'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu):
                img[ 0 :self.menu['keyboard_active'].shape[1],  self.x_dimension//3 + 3*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 3*self.constant_menu-self.constant_menu//2 + self.menu['keyboard_active'].shape[0]] = self.menu['keyboard_active']
                if self.mouse.clicked:
                    self.keyboardGraphIndex = self.changeStateClick(self.keyboardGraphIndex)   
                    self.presentation_table_index = False 
                    self.sport_table_index = False #1 
                    self.presIndex = False  #2  
                    self.trainActivateIndex = False  #3 
                    self.emotionIndex = False #4 
                    self.resetWindows('add_editors_window') 

            if self.mouse.lmList1[8][0]  in range(self.x_dimension//3 + 4*self.constant_menu-self.constant_menu//2, self.x_dimension//3 + 4*self.constant_menu-self.constant_menu//2  + self.menu['check_attendance_active'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu):
                img[ 0 :self.menu['check_attendance_active'].shape[1],  self.x_dimension//3 + 4*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 4*self.constant_menu-self.constant_menu//2 + self.menu['check_attendance_active'].shape[0]] = self.menu['check_attendance_active']
                if self.mouse.clicked:
                    self.attIndex = False  
                    self.attIndexSched =False 
                    self.schedEmotionIndex = False

                    self.window_bool['check_attendance_window'] = self.changeStateClick(self.window_bool['check_attendance_window'])  
                    self.presentation_table_index = False 
                    self.sport_table_index = False #1 
                    self.presIndex = False  #2  
                    self.trainActivateIndex = False  #3 
                    self.emotionIndex = False #4  
                    self.keyboardGraphIndex = False   #5 
                    self.resetWindows('check_attendance_window') 
 

            if self.mouse.lmList1[8][0]  in range(self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2, self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2  + self.menu['video_small_active'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu):
                if self.videoResizeIndex:
                    img[ 0 :self.menu['video_big_active'].shape[1],  self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 + self.menu['video_big_active'].shape[0]] = self.menu['video_big_active']
                else:
                    img[ 0 :self.menu['video_small_active'].shape[1],  self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 5*self.constant_menu-self.constant_menu//2 + self.menu['video_small_active'].shape[0]] = self.menu['video_small_active']
                if self.mouse.clicked:
                    self.videoResizeIndex = self.changeStateClick(self.videoResizeIndex)  

            if self.mouse.lmList1[8][0]  in range( self.x_dimension - self.constant_menu  - 15 ,  self.x_dimension - self.constant_menu  - 15  + self.menu['close_active'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu): 
                img[ 0 :self.menu['close_active'].shape[1],  self.x_dimension - self.constant_menu  - 15 : self.x_dimension - self.constant_menu  - 15 +  self.menu['close_active'].shape[0]] = self.menu['close_active']  
                if self.mouse.clicked:
                    self.closeBool = True 

            
            if self.mouse.lmList1[8][0]  in range(self.x_dimension//3 + 6*self.constant_menu-self.constant_menu//2, self.x_dimension//3 + 6*self.constant_menu-self.constant_menu//2  + self.menu['sport_active'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu):
                img[ 0 :self.menu['sport_active'].shape[1],  self.x_dimension//3 + 6*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 6*self.constant_menu-self.constant_menu//2 + self.menu['sport_active'].shape[0]] = self.menu['sport_active']
                if self.mouse.clicked:
                    self.sport_table_index  = self.changeStateClick(self.sport_table_index) 
                    self.trainActivateIndex = False 
                    self.presIndex = False  #2  
                    self.emotionIndex = False #4 
                    self.keyboardGraphIndex = False   #5  
                    self.b2Index = False  #6  
                    self.videoResizeIndex = False 
                    self.resetWindows('None') 
                    

            if self.mouse.lmList1[8][0]  in range(self.x_dimension//3 + 7*self.constant_menu-self.constant_menu//2, self.x_dimension//3 + 7*self.constant_menu-self.constant_menu//2  + self.menu['sport_active'].shape[0] )   and self.mouse.lmList1[8][1] in range(0, self.constant_menu):
                img[ 0 :self.menu['brush_active'].shape[1],  self.x_dimension//3 + 7*self.constant_menu-self.constant_menu//2 : self.x_dimension//3 + 7*self.constant_menu-self.constant_menu//2 + self.menu['brush_active'].shape[0]] = self.menu['brush_active']
                if self.mouse.clicked:
                    self.b2Index = self.changeStateClick(self.b2Index) 
                    if self.b2Index == False: 
                        height = 720 
                        width = 1280
                        self.b2.board = np.zeros((height , width , 3), np.uint8)
                        self.b2.menuBoard = np.zeros((height, width, 3), np.uint8)   
                        self.b2.shapeBoard = np.zeros((height, width, 3), np.uint8)  
                    self.sport_table_index = False #1 
                    self.trainActivateIndex = False  #3
                    self.presIndex = False  #2  
                    self.emotionIndex = False #4 
                    self.keyboardGraphIndex = False   #5 
                    self.resetWindows('None')    



        
        for element in self.window_bool:
            if self.window_bool[element] == True:
                y = self.constant_menu
                y1 =  self.constant_menu  + self.window[element].shape[0] 
                x =  self.x_dimension//3 + self.window_mult_i[element]*self.constant_menu-self.constant_menu//2 
                x1 = self.x_dimension//3 + self.window_mult_i[element]*self.constant_menu-self.constant_menu//2 + self.window[element].shape[1]
                if element == 'check_mood_window':
                    img[ y  : y1 , x - 45 : x1 - 45  ] = self.window[element]
                else:
                    img[ y: y1, x : x1  ] = self.window[element] 
                if element == 'share_presentation_window': 
                    if  x1 - self.buttons['choose_button'].shape[1]  < self.mouse.lmList1[8][0] < x1  and  y1 - self.buttons['choose_button'].shape[0]   <    self.mouse.lmList1[8][1] < y1 :
                        img[ y1 -  self.buttons['choose_button'].shape[0] : y1, x1 -  self.buttons['choose_button'].shape[1] : x1 ] = self.buttons['choose_button'] 
                        if self.mouse.clicked:
                            self.presentation_table_index  = self.changeStateClick(self.presentation_table_index) 
                            
                if element == 'check_attendance_window':
                    if  x1 - self.buttons['check_button'].shape[1]  < self.mouse.lmList1[8][0] < x1  and  y1 - self.buttons['check_button'].shape[0]   <    self.mouse.lmList1[8][1] < y1 :
                        img[ y1 -  self.buttons['check_button'].shape[0] : y1, x1 -  self.buttons['check_button'].shape[1] : x1 ] = self.buttons['check_button']
                        if self.mouse.clicked:
                            self.window_bool[element] = False 
                            self.window_bool['check_mood_window'] = True   
                
                if element =='check_mood_window':
                    
                    if  x1 - self.buttons['yes_button'].shape[1] - 45  < self.mouse.lmList1[8][0] < x1  -45 and  y1 - self.buttons['yes_button'].shape[0]   <    self.mouse.lmList1[8][1] < y1 :
                        img[ y1 -  self.buttons['yes_button'].shape[0] : y1, x1 -  self.buttons['yes_button'].shape[1]  - 45 : x1 - 45 ] = self.buttons['yes_button']
                        if self.mouse.clicked: 
                            def timerLeap():
                                self.emotionIndex = True 
                                self.current_time = int(time.time()) # Gets the time before the timer starts 

                            def scheduleTimer():
                                self.ti = Timer(2,timerLeap) 
                                self.ti.start()  

                            self.schedEmotionIndex = True  
                            schedule.every(3).minutes.do(scheduleTimer)  
                    
                            self.resetWindows('None')
                            self.sport_table_index = False #1


                    if  x1 - self.buttons['yes_button'].shape[1] - self.buttons['no_button'].shape[1] - 45 < self.mouse.lmList1[8][0] < x1 - self.buttons['yes_button'].shape[1] - 45  and  y1 - self.buttons['no_button'].shape[0]  <    self.mouse.lmList1[8][1] < y1: 
                        img[ y1  - self.buttons['no_button'].shape[0] : y1 , x1 -  self.buttons['yes_button'].shape[1]  - self.buttons['no_button'].shape[1] - 45 : x1 -  self.buttons['yes_button'].shape[1] - 45 ] = self.buttons['no_button'] 
            
                        if self.mouse.clicked: 
                            def timerLeap():
                                self.startTime = int(time.time()) 
                                self.attIndex = True 
                            def scheduleTimer():
                                self.ti2 = Timer(5,timerLeap) 
                                self.ti2.start()  

                            self.attIndexSched = True 
                            schedule.every(2).minutes.do(scheduleTimer)
                            
                            
                            self.ti2 = Timer(3,timerLeap) 
                            self.ti2.start() 
                            self.resetWindows('None')  
                            self.schedEmotionIndex = False
                            
                    


        
        if self.sport_table_index:
            self.sport.draw(img,self.mouse)
            if self.sport.trainIndexExName != None:
                self.trainActivateIndex = True  

                self.presIndex = False  #2  
                self.emotionIndex = False #4 
                self.keyboardGraphIndex = False   #5 

                self.tempTrainName = self.sport.trainIndexExName 
                self.sport.trainIndexExName = None 
                self.t.count = 0
                self.t.dir = 0 
                self.t.per = None 
                self.sport_table_index = False 
        
        if self.trainActivateIndex:
            self.t.activate(img,self.tempTrainName)

        

        if self.presIndex:
            img = self.p.activate(img) 
            img = self.b.start(img)  
            self.mouse.cursorOverlay(img) 

            if self.p.imgIndex >= len(self.p.imgList):
                self.presIndex = False 
                self.p  = 0
                self.b = 0   


        if self.schedEmotionIndex or self.attIndexSched:
            schedule.run_pending()
        
        if self.emotionIndex: 
            time_now = int(time.time())
            img = self.em.activate(img ) 
            if time_now >= self.current_time + self.seconds_to_go_for:
                self.emotionIndex  = False 
                self.em.df.to_csv('emotion_file.csv') 
                self.current_time = 0 
                self.attIndex = True 
                self.startTime = time.time() 
      

            

        
        if self.keyboardGraphIndex:
            img = self.keyboard_graph_feature.activate(img)  

        if self.b2Index:
            img = self.b2.start(img)   
        
        if self.attIndex:
            time_now = int(time.time())
            self.att.activate(img) 
            if time_now >= self.startTime + self.seconds_to_go_for:
                self.attIndex = False 
                self.startTime - 0  
        

    

        
        
         

            
        return img 

