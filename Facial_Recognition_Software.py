import cv2 
import numpy as np

import sys,os,numpy
from glob import glob
from skimage import io

#read test photo 
pwd  =  sys.path[0]
img = cv2.imread(pwd + "/Facial_test_images/photo2.jpg")

color = (0, 255, 0)

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

classfier = cv2.CascadeClassifier(pwd + "/Facial_models/haarcascade_frontalface_alt2.xml")

faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32)) 

if len(faceRects) > 0:
    for faceRect in faceRects:
        x, y, w, h = faceRect 
        cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 3) 

cv2.imwrite('output.jpg',img) 
cv2.imshow("face_image",img)
cv2.waitKey(0)