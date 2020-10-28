import cv2 
import numpy as np

import sys,os,numpy
from glob import glob
from skimage import io

#read test photo 
pwd  =  sys.path[0]
img = cv2.imread(pwd + "/Facial_test_images/6.jpg")

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

resize_fx = 1
resize_fy = 1

grey = cv2.resize(grey, dsize=None, fx=resize_fx, fy=resize_fy, interpolation = cv2.INTER_AREA)


classfier = cv2.CascadeClassifier(pwd + "/Facial_models/haarcascade_frontalface_alt2.xml")

faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=1, minSize=(16, 16)) 

color = (0, 255, 0)
if len(faceRects) > 0:
    for faceRect in faceRects:
        x, y, w, h = faceRect
        x = int(x/resize_fx)
        y = int(y/resize_fy)
        w = int(w/resize_fx)
        h = int(h/resize_fy) 
        cv2.rectangle(img, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 5) 

cv2.imwrite(pwd + "/Facial_test_images/output-a.jpg",img) 
cv2.imshow("face_image_a",img)



image =  cv2.imread(pwd + "/Facial_test_images/6.jpg")

net = cv2.dnn.readNetFromCaffe(pwd+"/Facial_models/deploy.prototxt", pwd+"/Facial_models/res10_300x300_ssd_iter_140000_fp16.caffemodel")

blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

net.setInput(blob)

detections = net.forward()

h,w,c=image.shape
for i in range(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.65:
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(image, (startX, startY), (endX, endY),(0, 255,0), 5)
        cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 1.00, (0, 255, 0), 3)

cv2.imwrite(pwd + "/Facial_test_images/output-b.jpg", image) 
cv2.imshow("face_image_b",image)
cv2.waitKey(0)
