import cv2
import mediapipe as mp
import math
import numpy as np
 
 
class poseDetector():
 
    def __init__(self, mode = False, complexity = 1, smooth = True,
                segmentationenable = False, smoothsegmentation = True,  
                detectionCon = 0.5, trackCon = 0.5):
 
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.segmentationenable = segmentationenable
        self.smoothsegmentation = smoothsegmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, 
                                    self.smooth, self.segmentationenable,
                                    self.smoothsegmentation, self.detectionCon, self.trackCon)
 
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw = True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw = True):
        #Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        #Calculate the angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2))
        
        if angle < 0:
            angle = abs(angle)


        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 0), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)

        return angle

    def biceps_curls(self, img):
        angle_left = poseDetector.findAngle(self, img, 11, 13, 15)
        percentage_left = np.interp(angle_left, (160, 60), (0, 100))
        angle_right = poseDetector.findAngle(self, img, 12, 14, 16)
        percentage_right = np.interp(angle_right, (160, 60), (0, 100))

        return (percentage_left + percentage_right) // 2


    def squats(self, img):
        angle_left = poseDetector.findAngle(self, img, 23, 25, 27)
        percentage_left = np.interp(angle_left, (170, 90), (0, 100))
        angle_right = poseDetector.findAngle(self, img, 24, 26, 28)
        percentage_right = np.interp(angle_right, (170, 90), (0, 100))

        return (percentage_left + percentage_right) // 2

    def dips(self, img):
        angle_left = poseDetector.findAngle(self, img, 11, 13, 15)
        percentage_left = np.interp(angle_left, (160, 100), (0, 100))
        angle_right = poseDetector.findAngle(self, img, 12, 14, 16)
        percentage_right = np.interp(angle_right, (160, 100), (0, 100))
        
        return (percentage_left + percentage_right) // 2

    def crunches(self, img):
        angle = poseDetector.findAngle(self, img, 11, 23, 25)
        percentage = np.interp(angle, (180, 110), (0, 100))

        return percentage
