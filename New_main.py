import cv2
import time
import mediapipe as mp
import speech_recognition as s_r
import pyaudio


def calculator(a, op, b):
    switcher = {
        '+': a + b,
        '-': a - b,
        '*': a * b,
        '/': a / b,
        '%': a % b,
        '>': a > b,
        '<': a < b
      }
    return switcher.get(op, "nothing")


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
    result = a = b = 0
    flag_num_1 = flag_num_2 = flag_op = flag_result = 0
    frame_count = timer_count = 0
    tipID = [4, 8, 12, 16, 20]
    num = 0
    num_1 = num_2 = operator = op = ""

    print("Digits can be entered from 0-9")
    print("Operations available are 1. Addition ")
    print("                         2. Subtraction ")
    print("                         3. Multiplication ")
    print("                         4. Division ")
    print("                         5. Modulus ")
    print("                         6. Less Than ")
    print("                         7. Greater Than ")

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

            if lmList[20][2] < lmList[18][2] and lmList[16][2] < lmList[13][2] and lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
                #print("end open")
                num = 4
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and (flag_num_1 or flag_op == 1):
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    operator = "/"

            elif lmList[16][2] < lmList[13][2] and lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
                #      print("ring open")
                num = 3
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and (flag_num_1 or flag_op == 1):
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    operator = "*"

            elif lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
                #   print("middle open")
                num = 2
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and (flag_num_1 or flag_op == 1):
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    operator = "-"

            elif lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
                # print("index open")
                num = 1
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and (flag_num_1 or flag_op == 1):
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    operator = "+"

            elif lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
                # print("thumb close")
                num = 0
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and flag_num_1:
                    num_1 = num_1 + str(num)
                    frame_count = 0

            elif lmList[20][2] < lmList[18][2] and lmList[16][2] < lmList[13][2] and lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
                #         print("end open")
                num = 5
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and (flag_num_1 or flag_op == 1):
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    operator = "%"

            elif lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
                #   print("middle open")
                num = 8
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and flag_num_1:
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    
            elif lmList[20][2] < lmList[18][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
                #         print("end open")
                num = 9
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and flag_num_1:
                    num_1 = num_1 + str(num)
                    frame_count = 0

            elif lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
                # print("index open")
                num = 7
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and (flag_num_1 or flag_op == 1):
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    operator = ">"

            elif lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
                # print("thumb open")
                num = 6
                frame_count = frame_count + 1
                timer_count = timer_count + 1
                if frame_count > 40 and (flag_num_1 or flag_op == 1):
                    num_1 = num_1 + str(num)
                    frame_count = 0
                    operator = "<"

            cv2.rectangle(img, (40, 275), (130, 385), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(num), (45, 375), cv2.FONT_HERSHEY_PLAIN, 8, (0, 255, 0), 15)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(img, f'FPS:{int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.putText(img, f'Timer:{float(start)}', (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        if start > 10.8 and start<11:
            print("LLL0", timer_count)

        if 11 < start< 19:
            cv2.putText(img, 'Enter First number', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(img, f'Number:{str(num_1)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            flag_num_1 = 1
           # print("First number",num_1)
            operator = ""
            a = num_1
            if start > 18.8:
                print("LLL1",timer_count)

        elif 19< start < 22:
            cv2.putText(img, 'Enter Operator', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(img, f'Operator:{str(operator)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv2.putText(img, str(a), (40, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            flag_op = 1
            flag_num_1 = 0
            num_1 = ""
           # print("Operator", operator)
            op = operator
            if start > 21.8:
                print("LLL2",timer_count)

        elif 22 < start < 29:
            cv2.putText(img, 'Enter Second number', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            cv2.putText(img, f'Number:{str(num_1)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv2.putText(img, str(a) + str(op), (40, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            flag_num_2 = 1
            flag_op = 0
            flag_num_1 = 1
           # print("Enter Second number", num_1)
            b = num_1
            if start > 28.8 :
                print("LLL3",timer_count)

        elif 29 < start < 31:
            result = calculator(int(a), op, int(b))
            cv2.putText(img, 'Result is:' + str(result), (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
            #cv2.putText(img, 'Result is:' + str(result), (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv2.putText(img, str(a) + str(op) + str(b) + " = " + str(result), (40, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
           # print("Result is:", result)
            flag_result = 1
            if start > 30.8:
                print("LLL4",timer_count)
                break

        #print("Firs number", a)
        #print("Second number", b)
        #print("Operator",op)
        #print("Result", result)
        cv2.imshow("Video", img)
        cv2.waitKey(1)
        #print(timer_count)

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
