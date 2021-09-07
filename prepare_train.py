import cv2
import os
import numpy as np
from msr import *
import sys

subjects = []

def main_f():
    def retinex_img(img):
        img = np.double(img)
        msr = main_msr(img)
        return msr


    def detect_face(img):
        face_cascade = cv2.CascadeClassifier('opencv-files/haarcascade_frontalface_alt.xml')
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)

        # jika tidak ada wajah terdeteksi return None
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


    def prepare_training_data(data_folder_path):
        # Ambil semua direktori didalam direktori 'training-data'
        dirs = os.listdir(data_folder_path)
        label_counter = 0
        # array untuk menyimpan wajah
        faces = []
        # array untuk menyimpan label
        labels = []

        for dir_name in dirs:
            subjects.append(dir_name)
            label_counter += 1
            label = label_counter
            print(label)
            print(subjects)

            subject_dir_path = data_folder_path + "/" + dir_name
            subject_images_names = os.listdir(subject_dir_path)

            for image_name in subject_images_names:

                if image_name.startswith("."):
                    continue

                image_path = subject_dir_path + "/" + image_name

                # read image
                image = cv2.imread(image_path)

                # detect face
                face, rect = detect_face(image)

                if face is not None:
                    # add face to list of faces
                    faces.append(face)
                    print(len(faces))
                    # add label for this face
                    labels.append(label)

        return faces, labels


    faces, labels = prepare_training_data("training-data")
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    eigen_train = cv2.face_EigenFaceRecognizer.create()
    eigen_train.train(faces, np.array(labels))
    eigen_train.save('eigen.yml')
    print('Data eigen berhasil disimpan')
    np.save('subjects.npy', subjects)
    print('Data subjek berhasil disimpan')
    print("Selesai")
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    exit()


if __name__ == '__main__':
    main_f()