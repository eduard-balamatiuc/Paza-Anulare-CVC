import cv2
from deepface import DeepFace
import pandas as pd
import time
import pandas as pd
from datetime import datetime





class EmotionCheck:
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_Default.xml')
        data  = {'time': [0], 'emotion': ['null'] }
        self.df = pd.DataFrame(data)

    def activate(self,img):
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection = False)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.1, 4) 
        new_row = {'time': datetime.now(), 'emotion':result['dominant_emotion']}
        self.df = self.df.append(new_row, ignore_index = True) 
        return img