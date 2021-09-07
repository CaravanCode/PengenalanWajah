import cv2
import os
import numpy as np
from msr import main_msr
from pyfirmata2 import Arduino
import time

import configparser

#array untuk menyimpan nama subjek
#subjects = []
subjects = np.load('subjects.npy')

board = Arduino(Arduino.AUTODETECT)
pin9 = board.get_pin('d:9:o')


config = configparser.RawConfigParser()
config_path = 'config.txt'
config.read(config_path)
durasi = int(config.get('Config', 'durasi'))
treshold = int(config.get('Config', 'treshold'))
recog_counter = 0

cascPath = 'opencv-files/haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)


def retinex_img(img):
    img = np.double(img)
    msr = main_msr(img)
    return msr


def get_perform(pred, confidence, time, count):
    f = open('output/irvan_20lux.txt', 'a')
    f.write(str(count) + "\n")
    f.write(str(pred) + "\n")
    f.write(str(confidence) + "\n")
    f.write(str(time) + "\n")
    f.write("    " + "\n")
    f.flush()
    os.fsync(f)


#function untuk deteksi wajah
def detect_face(img):
    face_cascade = cv2.CascadeClassifier('opencv-files/haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)
    
    #jika tidak ada wajah terdeteksi return None
    if (len(faces) == 0):
        return None, None

    (x, y, w, h) = faces[0]
    im = img[y:y + w, x:x + h]
    dim = (100, 100)
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)

    #img_retinex = retinex_img(resized)
    #gray = cv2.cvtColor(img_retinex, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    return gray, faces[0]


face_recognizer = cv2.face.EigenFaceRecognizer_create()
face_recognizer.read('eigen.yml')


def buka():
    pin9.write(1)


def tutup():
    pin9.write(0)


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)



def predict(test_img):

    stat = "F"
    img = test_img.copy()
    if img is None:
        return None, stat, None, None
    else:
        face, rect = detect_face(img)
        if not rect is None:
            #predict the image using our face recognizer
            label, confidence = face_recognizer.predict(face)
            #get name of respective label returned by face recognizer
            label_text = subjects[label-1]
            #label_text = labels[label]

            #draw a rectangle around face detected
            draw_rectangle(img, rect)
            #draw name of predicted person
            if not confidence>treshold:
                print("{} Confidence: {}".format(label_text,confidence))
                draw_text(img, label_text, rect[0], rect[1]-5)
                stat = 'T'
            else:
                print("Mistaken as {} with Confidence: {}".format(label_text, confidence))
                draw_text(img, "Tidak Dikenal", rect[0], rect[1] - 5)
                stat = 'F'
                label_text = 'Tidak Dikenal'
            return img, stat, confidence, label_text
        else:
            return None, stat, None, None


print("Predicting images...")


def recog():
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        tic = time.perf_counter()
        pred, stat, conf, name = predict(frame)
        global recog_counter
        if not pred is None:
            cv2.imshow('Video', pred)
            recog_counter += 1
            toc = time.perf_counter()
            elapsed_time = toc - tic
            print(elapsed_time)
            get_perform(name, conf, elapsed_time,recog_counter)
            if stat == 'T':
                cv2.waitKey(20)
                break
            else:
                pin9.write(0)
        else:
            cv2.imshow('Video', frame)
            pin9.write(0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            exit()
    pin9.write(1)
    print('Buka')
    time.sleep(durasi)
    recog()


if __name__=='__main__':
    recog()






