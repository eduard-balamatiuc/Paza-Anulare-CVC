import sched
import click
from cv2 import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


class CheckAttendance():
    def __init__(self):

        self.TOLERANCE = 0.6
        self.check_time = 30.0

    # connect to the package with people images
    def connect(self):
        path = "E:/CVC/Project/Attendance/People"
        images = []
        classNames = []
        peopleList = os.listdir(path)

        for cl in peopleList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        return images, classNames

    # find encodings on each photo
    def findEncodings(self):
        encodeList = []
        images = self.connect()[0]
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)
            if len(encode) > 0:
                encodeList.append(encode[0])
            else:
                print("No face found in the image! ", len(encodeList))
        return encodeList

    # Mark the presence in file
    def markAttendance(self, name):
        with open('E:/CVC/Project/Attendance/Attendance.csv', 'r+') as f:
            myDataList = f.readline()
            nameList = []
            for line in myDataList:
                entry = line.split(' ')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'Name: {name}; time: {dtString}\n')

    # check if the person is present
    def check(self, image):
        classNames = self.connect()[1]
        encodeListKnown = self.findEncodings()
        facesCurFrame = face_recognition.face_locations(image)
        encodesCurFrame = face_recognition.face_encodings(image, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, self.TOLERANCE)
            faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDist)

            if matches[matchIndex] > 0.50:
                print(matches[matchIndex])
                name = classNames[matchIndex]
                if os.path.getsize(
                        "E:/CVC/Project/Attendance/Attendance.csv") == 0:
                    self.markAttendance(name)
                    # self.start_time = time.time()
            else:
                name = 'Unknown'
                print(matches[matchIndex])
                if os.path.getsize(
                        "E:/CVC/Project/Attendance/Attendance.csv") == 0:
                    self.markAttendance(name)
                    # self.start_time = time.time()

            #  in case the frame around face is needed
            # y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            # cv2.rectangle(img, (x1, y1), (x2, y2), (32, 80, 238), 1)
            # cv2.rectangle(img, (x1, y2 - 20), (x2, y2), (32, 80, 238), cv2.FILLED)
            # cv2.putText(img, name, (x1 + 3, y2 - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)


def main():
    camera = cv2.VideoCapture(0)

    while True:
        success, img = camera.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        CheckAttendance().check(imgS)
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
