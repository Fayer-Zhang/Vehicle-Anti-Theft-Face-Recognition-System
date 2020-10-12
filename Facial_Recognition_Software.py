import cv2 
import numpy as np 

import sys,os,glob,numpy
from skimage import io

#read test photo 
img = cv2.imread("C:/Users/fayer/OneDrive - University of Ottawa/CEG 4912/Project Test/data/photo4.jpg") 
color = (0, 255, 0)

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

classfier = cv2.CascadeClassifier("C:/Users/fayer/OneDrive - University of Ottawa/CEG 4912/Project Test/model/haarcascade_frontalface_alt2.xml")

faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32)) 

if len(faceRects) > 0:
    for faceRect in faceRects:
        x, y, w, h = faceRect 
        cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 3) 

cv2.imwrite('output.jpg',img) 
cv2.imshow("face_image",img)
cv2.waitKey(0)
