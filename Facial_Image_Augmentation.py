import sys
import cv2
import os
import numpy as np
import math
import random


def facial_recognition_augmentation(label):
    aug = 5
    image_path = sys.path[0] + '/Facial_images/face_rec/train/' + label + '/'
    imagelist = os.listdir(image_path)

    for file_name in imagelist:
        (nameWithoutExtention, extention) = os.path.splitext(os.path.basename(file_name))

        if (extention==".jpg"):

            #print(image_path+file_name)
            inputImage = cv2.imread(image_path+file_name)
        
            for i in range(aug):
                rotate = random.randint(-8,8)
                brightness = random.randint(-30, +30)
                clahe = random.uniform(0.0, 1.0)

                choice = random.randint(0, 10)

                (h, w) = inputImage.shape[:2] #10
                center = (w // 2, h // 2) #11
                
                M = cv2.getRotationMatrix2D(center, rotate, 1.0) #12
                inputImage = cv2.warpAffine(inputImage, M, (w, h)) #13
                
                if (choice%3 == 1):
                    clahe = cv2.createCLAHE(clipLimit=clahe, tileGridSize=(8,8))
                    inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
                    l, a, b = cv2.split(inputImage)  # split on 3 different channels
                    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
                    inputImage = cv2.merge((l2,a,b))  # merge channels
                    inputImage = cv2.cvtColor(inputImage, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
                elif(choice%3 == 2):
                    fI = inputImage/255.0
                    gamma = random.uniform(0.2, 0.4)
                    #inputImage = np.power(fI, gamma)
                else:
                    cv2.addWeighted( inputImage, 0.5, inputImage, 0.5, brightness, inputImage)

                choice_1 = random.randint(0, 10)
                if (choice_1%2 == 1):
                    gauss = random.randint(1, 2)*2-1

                    inputImage = cv2.GaussianBlur(inputImage, (gauss,gauss), 0)
                
                cv2.imwrite(image_path+nameWithoutExtention+"_aug"+str(i)+".jpg", inputImage)


