import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep, time
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

ClickedText = ""
keyboard = Controller()
def drawALL(img, buttonList, rectColor=(255, 0, 255), textColor=(255, 255, 255)):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), rectColor, cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, textColor, 3)
    return img

class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

timeout = 3 # seconds
start_time = time()

while True:
    success, img = cap.read()

    if not success:
        break
        
    img= detector.findHands(img)
    lmlist, bboxInfo = detector.findPosition(img)
    drawALL(img, buttonList, (0, 0, 0), (255, 255, 255))

    if lmlist:
        start_time = time()
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            if x<lmlist[8][0]<x+w and y<lmlist[8][1] < y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                l,_,_=detector.findDistance(8,12,img)
                # print(l)
                if l < 50:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                    ClickedText += button.text
                    sleep(0.3)
    else:
        elapsed_time = time() - start_time
        if elapsed_time > timeout:
            print("Hand not found for more than {} seconds. Exiting program...".format(timeout))
            break
    cv2.rectangle(img, (55,345), (700,450), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, ClickedText, (60,425), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    cv2.imshow('camera',img)
    cv2.waitKey(1)