import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt 
from collections import Counter 





class SignLClass:
    def __init__(self):
        self.model = torch.hub.load(r'yolov5', 'custom', path=r'yolov5\best2.pt', source='local')
        self.sentence = ''
        self.sentence2 = '' 
        self.font = cv2.FONT_HERSHEY_PLAIN
    
        
    def most_common(self,List):
        List = Counter(List)
        return(List.most_common(1)[0][0]) 
    
    def activate(self,frame):

        results = self.model(frame)
        
        #cv2.imshow('YOLO', np.squeeze(results.render()))
        res = results.pandas().xyxy[0]['name']

        if len(res):
            res = res[0]
            #cv2.putText(frame,res,(80,420),self.font,2,(222,222,222),2)
            self.sentence += res    
            if len(self.sentence) == 15:
                res = self.most_common(self.sentence)
                
                res3 = res
                self.sentence = ''
                
                
                if res3 == 'del':
                    self.sentence2 = self.sentence2[:-1]
                elif res3 == 'space':
                    self.sentence2 += ' '
                else:
                    self.sentence2 += res3
                    print(self.sentence2)

                if len(self.sentence2) == 30:
                    self.sentence2 = ''
        
        #cv2.putText(frame,self.sentence2,(200,600),self.font,2, ( 37,68,175) ,4) 
        return self.sentence2 

