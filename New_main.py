import cv2
import time
import mediapipe as mp
import speech_recognition as s_r
import pyaudio


def speech():
    r = s_r.Recognizer()
    my_mic_device = s_r.Microphone(device_index=1)
    with my_mic_device as source:
        print("SPEAK NOW")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    speech_said = r.recognize_google(audio)
    return speech_said


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
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


def main():
    result = 0
    flag_num_1 = flag_num_2 = flag_op = flag_result = 0
    frame_count = 0
    tipID = [4, 8, 12, 16, 20]
    num = 0
    digit = 0
    num_1 = num_2 = operator = ""

    print("Speak 'START' to start entering numbers and 'STOP' to exit program")
    print("Speak 'NUMBER' to enter digits and 'OPERATOR' to select an operation")
    print("Digits can be entered from 0-9")
    print("Operations available are 1. Addition ")
    print("                         2. Subtraction ")
    print("                         3. Multiplication ")
    print("                         4. Division ")

    flag = {"first": False, "operator": False, "second": False, "clear": False}
    frame_count_same_frames = 0
    first, operator, second = "", "", ""
    frame_count_clear_frames = 0

    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    prev_time = 0
    detector = handDetector(detectionCon=0.70)

    # frame_counting fingers after detection
    while True:
        start = time.process_time()
        success, img = capture.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        # print(lmList)

        if len(lmList) != 0:
            finger = []

            if lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
                # print("thumb open")
                num = 6
                frame_count = frame_count + 1
                if lmList[8][2] < lmList[5][2]:
                    # print("index open")
                    num = 7
                    frame_count = frame_count + 1
                    if lmList[12][2] < lmList[9][2]:
                        #   print("middle open")
                        num = 8
                        frame_count = frame_count + 1
                        if lmList[16][2] < lmList[13][2]:
                            #      print("ring open")
                            # num = 9
                            if lmList[20][2] < lmList[18][2]:
                                #start = time.process_time()
                                #         print("end open")
                                num = 5
                                frame_count = frame_count + 1
                                #print(time.process_time() - start)
                                if frame_count > 100:
                                    num_1 = num_1 + str(num)
                                    frame_count = 0


                    elif lmList[20][2] < lmList[18][2]:
                        #         print("end open")
                        num = 9
                        frame_count = frame_count + 1
                        if frame_count > 100:
                            num_1 = num_1 + str(num)
                            frame_count = 0
            #  finger.append(1)
            else:
                # print("thumb close")
                num = 0
                frame_count = frame_count + 1
                if lmList[8][2] < lmList[5][2]:
                    # print("index open")
                    num = 1
                    frame_count = frame_count + 1
                    #while flag_op == 1:
                     #   operator = '+'
                      #  flag_op = 2
                    if lmList[12][2] < lmList[9][2]:
                        #   print("middle open")
                        num = 2
                        frame_count = frame_count + 1
                        if lmList[16][2] < lmList[13][2]:
                            #      print("ring open")
                            num = 3
                            frame_count = frame_count + 1
                            if lmList[20][2] < lmList[18][2]:
                                #         print("end open")
                                num = 4
                                frame_count = frame_count + 1
                                if frame_count > 100:
                                    num_1 = num_1 + str(num)
                                    frame_count = 0

            cv2.rectangle(img, (40, 275), (130, 385), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(num), (45, 375), cv2.FONT_HERSHEY_PLAIN, 8, (0, 255, 0), 15)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(img, f'FPS:{int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.putText(img, f'Timer:{float(start)}', (50, 90), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

       #if 14 < start< 24 and flag_num_1 == 0
        if 14 < start< 24:
            cv2.putText(img, 'Enter First number', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(img, f'Number:{str(num_1)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            flag_num_1 = 1
            #speech_said = speech()
            #print("Command given:", speech_said)
            #if speech_said == "exit":
            #print("Enter First number")

        elif 25< start < 30 :
            cv2.putText(img, 'Enter Operator', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(img, f'Operator:{str(operator)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            flag_op = 1
            flag_num_1 = 0
            print("Enter Operator")
            #print("Operator", operator)
            flag_op = 1
        elif 31 < start < 41 :
            cv2.putText(img, 'Enter Second number', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(img, f'Number:{str(num_1)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            print("Enter Second number")
            flag_num_2 = 1
        elif 41 < start < 45:
            cv2.putText(img, 'Result is:' + str(result), (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(img, 'Result is:' + str(result), (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

            print("Result is:",result)
            flag_result = 1

        cv2.imshow("Video", img)
        cv2.waitKey(1)
        print(frame_count)

    #print(time.process_time() - start)
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
