import cv2
import retinex
import numpy as np

cascPath = 'opencv-files/haarcascade_frontalface_alt.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

img = cv2.imread('training-data/irvan/19.jpg')
faces = faceCascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)
print("Found {0} faces!".format(len(faces)))


def get_perform(img):
    f = open('gray.txt', 'a')
    f.write(str(img) + "\n")
    f.flush()


for (x, y, w, h) in faces:
    face = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
    im = img[y:y + w, x:x + h]
    dim = (100, 100)
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    msr = retinex.main_msr(resized)
    msrcr = retinex.main_msrcr(resized)
    gray = cv2.cvtColor(msr, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(msrcr, cv2.COLOR_BGR2GRAY)
    #get_perform(gray)
    #counter = counter + 1
    #cv2.imwrite('ori.jpg', img)
    #cv2.imwrite('face.jpg', im)
    #cv2.imwrite('face.jpg', resized)
    #cv2.imwrite('msr.jpg', msr)
    #cv2.imshow('Img', im)
    #cv2.waitKey(5000)
    #cv2.imwrite('grey.jpg', gray)
    #mean, eigen = cv2.PCACompute(gray, mean=None)


    #ndarray = np.full((100, 100),eigen,  dtype=np.uint8)
    #get_perform(eigen)
    #get_perform(ndarray)
    cv2.imshow('MSR', msr)
    cv2.imshow('MSRCR', msrcr)
    cv2.waitKey(5000)





