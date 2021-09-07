import cv2
import sys
import tkinter as tk
import os
import threading


cascPath = 'opencv-files/haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
path='training-data'
f=open('temp.txt','r+')
counter=0
wajah = f.read()
video_capture = cv2.VideoCapture(0)


def capt_img(frame,counter):
    cv2.imwrite(os.path.join(wajah, "{}.jpg".format(counter)), frame)
    cv2.putText(frame, "Berhasil Disimpan", (200, 400), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

while video_capture.isOpened():
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    print("Found {0} faces!".format(len(faces)))

    if cv2.waitKey(1) & 0xFF == ord('w'):
        capt_img(frame,counter)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    cv2.imshow('Video', frame)
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
        counter=counter+1



    # Display the resulting frame



# When everything is done, release the capture
video_capture.release()
cv2.waitKey(25)
cv2.destroyAllWindows()
exit()


