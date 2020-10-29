import sys
import os

import cv2
import numpy as np

from glob import glob
from skimage import io


def face_detector_haarcascade(image):

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    resize_fx = 1
    resize_fy = 1
    grey = cv2.resize(grey, dsize=None, fx=resize_fx, fy=resize_fy, interpolation = cv2.INTER_AREA)

    pwd = sys.path[0]
    classfier = cv2.CascadeClassifier(pwd + "/Facial_models/haarcascade_frontalface_alt2.xml")

    faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=1, minSize=(16, 16)) 

    if len(faceRects) > 0:
        for faceRect in faceRects:
            x, y, w, h = faceRect
            x = int(x/resize_fx)
            y = int(y/resize_fy)
            w = int(w/resize_fx)
            h = int(h/resize_fy) 
            cv2.rectangle(image, (x - 10, y - 10), (x + w + 10, y + h + 10), (0, 255, 0), 5) 

    return image


def face_detector_ssd(image):

    pwd = sys.path[0]
    net = cv2.dnn.readNetFromCaffe(pwd+"/Facial_models/deploy.prototxt", pwd+"/Facial_models/res10_300x300_ssd_iter_140000_fp16.caffemodel")

    resize = (800, 800)
    confidence_thres = 0.65
    
    blob = cv2.dnn.blobFromImage(cv2.resize(image, dsize=resize), 1.0, resize, (104.0, 177.0, 123.0))
   # blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    net.setInput(blob)

    detections = net.forward()

    h,w,c=image.shape

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_thres:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY),(0, 255,0), 5)
            cv2.putText(image, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 1.00, (0, 255, 0), 3)
    
    return image



if __name__=="__main__":

    image_name = "8.jpg"
    split_name = image_name.split(".")

    image_read_path = sys.path[0]+"/Facial_test_images/"+image_name
    image_save_path = sys.path[0]+"/Facial_test_images/output/"+split_name[0]+"_result."+split_name[1]

    image = cv2.imread(image_read_path)

    image = face_detector_ssd(image)
    #image = face_detector_haarcascade(image)

    print(image_save_path)

    cv2.imwrite(image_save_path, image)
    cv2.imshow("result", image)
    cv2.waitKey()
    cv2.destroyAllWindows()

    


