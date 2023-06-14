import cv2
import mediapipe as mp

import pyautogui
from pynput.keyboard import Key,Controller


virtualkeyboard = Controller()
state =None

video = cv2.VideoCapture(0)


width=int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(width,height)

myhands=mp.solutions.hands

# print("my hands: ", myhands)
mydrawing=mp.solutions.drawing_utils

hand_object=myhands.Hands(min_detection_confidence=0.75,min_tracking_confidence=0.75) 

# print("what is hand_object: ", hand_object)

def count_fingers(myimage,lst):
    count=0
    global state

    thresh = (lst.landmark[0].y*100-lst.landmark[9].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100)>thresh:
        count+=1
    if (lst.landmark[9].y*100 - lst.landmark[12].y*100)>thresh:
        count+=1
    if (lst.landmark[13].y*100 - lst.landmark[16].y*100)>thresh:
        count+=1
    if (lst.landmark[17].y*100 - lst.landmark[20].y*100)>thresh:
        count+=1

    tf = count
    if tf == 4:
        state="play"
    if tf == 0 and state=='play':
        state='pause'
        virtualkeyboard.press(Key.space)

    finger_tip_x=(lst.landmark[8])*width
    if(tf==1):
        if(finger_tip_x<width-400):
            state="backward"
            virtualkeyboard.press(Key.left)
        if(finger_tip_x>width-400):
            state='forward'
            virtualkeyboard.press(Key.right)
            #fdds gi

    print("what is the state: ",state)

    return tf


while True:
    dummy,frame = video.read()
    flipImage=cv2.flip(frame,1)

    result=hand_object.process(cv2.cvtColor (flipImage,cv2.COLOR_BGR2RGB)) 
    # print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:
        hand_keypoints = result.multi_hand_landmarks[0]
        #print(hand_keypoints)
        mycount = count_fingers(flipImage,hand_keypoints)
        cv2.putText(flipImage,"count" +str(mycount),(100,100),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,225),2)
        mydrawing.draw_landmarks(flipImage,hand_keypoints,myhands.HAND_CONNECTIONS)
        
       

    cv2.imshow('Hand Guestures: ',flipImage)

    if cv2.waitKey(1) == 27:
        break
    

video.release()
cv2.destroyAllWindows()