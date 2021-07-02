## importing
import cv2
import time
import mediapipe as mp
import speech_recognition as s_r


# a,b is for number 1,2 whereas op is for operator
def calculator(a, op, b):
    switcher = {
        '+': a + b,
        '-': a - b,
        '*': a * b,
        '/': round(a / b, 3),
        '%': round(a % b, 3),
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

#    speech_said = speech()
    print("Command given:", speech_said)
    if speech_said == "number":
        print("hi")
    elif speech_said == "operator":
        print("ji")
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


def number_identify(frame_count, flag_num_1, flag_op, lmList, num_1, tipID, img, operator, num):
    if len(lmList) != 0:

        if lmList[20][2] < lmList[18][2] and lmList[16][2] < lmList[13][2] and lmList[12][2] < lmList[9][2] and \
                lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
            # print("end open")
            num = 4
            frame_count = frame_count + 1
            if frame_count > 30 and (flag_num_1 or flag_op == 1):
                num_1 = num_1 + str(num)
                frame_count = 0
                operator = "/"

        elif lmList[16][2] < lmList[13][2] and lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and \
                lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
            #      print("ring open")
            num = 3
            frame_count = frame_count + 1
            if frame_count > 30 and (flag_num_1 or flag_op == 1):
                num_1 = num_1 + str(num)
                frame_count = 0
                operator = "*"

        elif lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] < \
                lmList[tipID[0] - 2][1]:
            #   print("middle open")
            num = 2
            frame_count = frame_count + 1
            if frame_count > 30 and (flag_num_1 or flag_op == 1):
                num_1 = num_1 + str(num)
                frame_count = 0
                operator = "-"

        elif lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
            # print("index open")
            num = 1
            frame_count = frame_count + 1
            if frame_count > 30 and (flag_num_1 or flag_op == 1):
                num_1 = num_1 + str(num)
                frame_count = 0
                operator = "+"

        elif lmList[tipID[0]][1] < lmList[tipID[0] - 2][1]:
            # print("thumb close")
            num = 0
            frame_count = frame_count + 1
            if frame_count > 30 and flag_num_1:
                num_1 = num_1 + str(num)
                frame_count = 0

        elif lmList[20][2] < lmList[18][2] and lmList[16][2] < lmList[13][2] and lmList[12][2] < lmList[9][2] and \
                lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
            #         print("end open")
            num = 5
            frame_count = frame_count + 1
            if frame_count > 30 and (flag_num_1 or flag_op == 1):
                num_1 = num_1 + str(num)
                frame_count = 0
                operator = "%"

        elif lmList[12][2] < lmList[9][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > \
                lmList[tipID[0] - 2][1]:
            #   print("middle open")
            num = 8
            frame_count = frame_count + 1
            if frame_count > 30 and flag_num_1:
                num_1 = num_1 + str(num)
                frame_count = 0

        elif lmList[20][2] < lmList[18][2] and lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > \
                lmList[tipID[0] - 2][1]:
            #         print("end open")
            num = 9
            frame_count = frame_count + 1
            if frame_count > 30 and flag_num_1:
                num_1 = num_1 + str(num)
                frame_count = 0

        elif lmList[8][2] < lmList[5][2] and lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
            # print("index open")
            num = 7
            frame_count = frame_count + 1
            if frame_count > 30 and (flag_num_1 or flag_op == 1):
                num_1 = num_1 + str(num)
                frame_count = 0
                operator = ">"

        elif lmList[tipID[0]][1] > lmList[tipID[0] - 2][1]:
            # print("thumb open")
            num = 6
            frame_count = frame_count + 1
            if frame_count > 30 and (flag_num_1 or flag_op == 1):
                num_1 = num_1 + str(num)
                frame_count = 0
                operator = "<"

        cv2.rectangle(img, (40, 275), (130, 385), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, str(num), (45, 375), cv2.FONT_HERSHEY_PLAIN, 8, (0, 255, 0), 15)
    return num_1, operator, frame_count


def main():
    a = b = n = x = 0
    flag_num_1 = flag_op = flag_result = num = 0
    flag_task = "first"
    frame_count = 0
    tipID = [4, 8, 12, 16, 20]
    num_1 = num_2 = op = ""
    operator = ""

    print(" ")
    print("Digits can be entered from 0-9")
    print("Operations available are 1. Addition ")
    print("                         2. Subtraction ")
    print("                         3. Multiplication ")
    print("                         4. Division ")
    print("                         5. Modulus")
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

        num_1, operator, frame_count = number_identify(frame_count, flag_num_1, flag_op, lmList, num_1, tipID, img, operator, num)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(img, f'FPS:{int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.putText(img, f'Timer:{float(start)}', (50, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        if start > 9:
            if flag_task == "first" and len(num_1) < 3:
                cv2.putText(img, 'Enter First number', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                cv2.putText(img, f'Number:{str(num_1)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                flag_num_1 = 1
    #           print("First number",num_1)
                operator = ""
                a = num_1
                if len(num_1) == 2:
                    flag_task = "operator"

            elif flag_task == "operator" and len(operator) < 2:
                cv2.putText(img, 'Enter Operator', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                cv2.putText(img, f'Operator:{str(operator)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                cv2.putText(img, str(a), (40, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                flag_op = 1
                flag_num_1 = 0
                num_1 = ""
    #           print("Operator", operator)
                op = operator
                if len(operator) == 1:
                    flag_task = "second"

            elif flag_task == "second" and len(num_1) < 3:
                cv2.putText(img, 'Enter Second number', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                cv2.putText(img, f'Number:{str(num_1)}', (40, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                cv2.putText(img, str(a) + str(op), (40, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                flag_op = 0
                flag_num_1 = 1
    #           print("Enter Second number", num_1)
                b = num_1
                if len(num_1) == 2:
                    flag_task = "result"

            elif flag_task == "result":
                result = calculator(int(a), op, int(b))
                cv2.putText(img, 'Result is: ' + str(result), (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                cv2.putText(img, str(a) + str(op) + str(b) + " = " + str(result), (40, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                print("First number:", a)
                print("Operator:", op)
                print("Second number:", b)
                print("Result is:", result)
                print(" ")
                if x == 35:
                    flag_result = 1
                else:
                    x = x + 1

                if n != 1 and flag_result == 1:
                    n = n + 1
                    flag_task = "first"
                    num_1 = ""
                    flag_result = 0
                    x = 0
                elif n == 1 and flag_result == 1:
                    cv2.putText(img, 'Thank You', (160, 400), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                    print("Thank You")
                    time.sleep(1)
                    break

        cv2.imshow("Video", img)
        cv2.waitKey(1)

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
