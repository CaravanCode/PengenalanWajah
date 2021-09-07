import numpy as np
from msr import *
import cv2

path = 'training-data/irvan/1.png'
img = cv2.imread(path)
def msr(img):
    img = np.double(img)
    msr = main_msr(img)
    return msr


def msrcr(img):
    img = np.double(img)
    msrcr = main_msrcr(img)
    return msrcr
