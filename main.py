import cv2
import time
import mediapipe as mp
import os
#pip install --upgrade cv2
#pip install opencv-python
#pip install mediapipe

class handDetector():
        def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
                self.mode = mode
                self.maxHands = maxHands
                self.detectionCon = detectionCon
                self.trackCon = trackCon

                self.mpHands = mp.solutions.hands
                self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                                self.detectionCon, self.trackCon)
                self.mpDraw = mp.solutions.drawing_utils

        def findHands(self, img, draw=True):
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.results = self.hands.process(imgRGB)
                # print(results.multi_hand_landmarks)

                if self.results.multi_hand_landmarks:
                        for handLms in self.results.multi_hand_landmarks:
                                if draw:
                                        self.mpDraw.draw_landmarks(img, handLms,
                                                                   self.mpHands.HAND_CONNECTIONS)
                return img

        def findPosition(self, img, handNo=0, draw=True):

                lmList = []
                if self.results.multi_hand_landmarks:
                        myHand = self.results.multi_hand_landmarks[handNo]
                        for id, lm in enumerate(myHand.landmark):
                                # print(id, lm)
                                h, w, c = img.shape
                                cx, cy = int(lm.x * w), int(lm.y * h)
                                # print(id, cx, cy)
                                lmList.append([id, cx, cy])
                                if draw:
                                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                return lmList


capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#wCam, hCam= 640, 480
#capture.set(3, wCam)
#capture.set(4, hCam)
prev_time=0
detector = handDetector(detectionCon=0.70)
tipID = [4, 8, 12, 16, 20]
num = 0
while True:
        success, img = capture.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        #print(lmList)

        if len(lmList) != 0:
            finger= []

            if ( lmList[tipID[0]][1] > lmList[tipID[0]-2][1] ):
               # print("thunm open")
                num = 6
                if (lmList[8][2] < lmList[5][2]):
                    # print("index open")
                    num = 7
                    if (lmList[12][2] < lmList[9][2]):
                        #   print("middle open")
                        num = 8
                        if (lmList[16][2] < lmList[13][2]):
                            #      print("ring open")
                            #num = 9
                            if (lmList[20][2] < lmList[18][2]):
                                #         print("end open")
                                num = 5
                    elif (lmList[20][2] < lmList[18][2]):
                                #         print("end open")
                                num = 9
              #  finger.append(1)
            else:
               # print("thunm close")
                num = 0
                if (lmList[8][2] < lmList[5][2]):
                    # print("index open")
                    num = 1
                    if (lmList[12][2] < lmList[9][2]):
                        #   print("middle open")
                        num = 2
                        if (lmList[16][2] < lmList[13][2]):
                            #      print("ring open")
                            num = 3
                            if (lmList[20][2] < lmList[18][2]):
                                #         print("end open")
                                num = 4
             #   finger.append(0)
            #print(finger)

            #finger_count = finger.count(1)
            #print(finger_count)




            cv2.rectangle(img, (20, 225), (170, 425), (0,255,0), cv2.FILLED)
            cv2.putText(img, str(num), (45,375), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)

        current_time = time.time()
        fps = 1/(current_time - prev_time)
        prev_time= current_time

        cv2.putText(img, f'FPS:{int(fps)}',(400,70), cv2.FONT_HERSHEY_PLAIN, 3 ,(0,255,0), 3)
        cv2.imshow("Video", img)
        cv2.waitKey(1)


capture.release()
cv2.destroyAllWindows()

