import sys
import os
import math
import cv2
import dlib
import numpy as np
import Facial_Recognition_Render as fr
import _pickle as cPickle
import glob

faceWidth = 320
faceHeight = 320
SKIP_FRAMES = 1

def alignFace(imFace, landmarks):
    l_x = landmarks[39][0]
    l_y = landmarks[39][1]
    r_x = landmarks[42][0]
    r_y = landmarks[42][1]
    dy = r_y - l_y
    dx = r_x - l_x
    # Convert from radians to degrees
    angle = math.atan2(dy, dx) * 180.0 / math.pi  

    eyesCenter = ((l_x + r_x)*0.5, (l_y + r_y)*0.5)
    rotMatrix = cv2.getRotationMatrix2D(eyesCenter, angle, 1)
    alignedImFace = np.zeros(imFace.shape, dtype=np.uint8)
    alignedImFace = cv2.warpAffine(imFace, rotMatrix, (imFace.shape[1],imFace.shape[0]))
    return alignedImFace

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

    resize = (300, 300)
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

def training_data_loader():
    imagesFolder = sys.path[0]+"/Facial_images/face_rec/train/"
    subfolders = []

    for x in os.listdir(imagesFolder):
        xpath = os.path.join(imagesFolder, x)
        if os.path.isdir(xpath):
            subfolders.append(xpath)

    imagePaths = []
    labels = []
    labelsMap = {}
    labelsMap[-1] = "unknown"

    for i, subfolder in enumerate(subfolders):
        labelsMap[i] = os.path.basename(subfolder)
        for x in os.listdir(subfolder):
            xpath = os.path.join(subfolder, x)
            if x.endswith('jpg') or x.endswith('pgm'):
                imagePaths.append(xpath)
                labels.append(i)

    imagesFaceTrain = []
    labelsFaceTrain = []

    faceDetector = dlib.get_frontal_face_detector() 
    landmarkDetector = dlib.shape_predictor(sys.path[0]+"/Facial_models/shape_predictor_68_face_landmarks.dat")
    
    for j, imagePath in enumerate(imagePaths):
        im = cv2.imread(imagePath, 0)
        imHeight, imWidth = im.shape[:2]

        landmarks = fr.getLandmarks(faceDetector, landmarkDetector, im)

        landmarks = np.array(landmarks)
        
        if len(landmarks) == 68:
            x1Limit = landmarks[0][0] - (landmarks[36][0] - landmarks[0][0])
            x2Limit = landmarks[16][0] + (landmarks[16][0] - landmarks[45][0])
            y1Limit = landmarks[27][1] - 3*(landmarks[30][1] - landmarks[27][1])
            y2Limit = landmarks[8][1] + (landmarks[30][1] - landmarks[29][1])

            x1 = max(x1Limit,0)
            x2 = min(x2Limit, imWidth)
            y1 = max(y1Limit, 0)
            y2 = min(y2Limit, imHeight)
            imFace = im[y1:y2, x1:x2]

            alignedFace = alignFace(imFace, landmarks)
            alignedFace = cv2.resize(alignedFace, (faceHeight, faceWidth))

            imagesFaceTrain.append(np.float32(alignedFace)/255.0)
            labelsFaceTrain.append(labels[j])
    
    return imagesFaceTrain, labelsFaceTrain, labelsMap

def training_recognizer(rec_type):
   
    imagesFaceTrain, labelsFaceTrain, labelsMap = training_data_loader()

    if (rec_type=='LBPH'):
        faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
        print("Training using LBPH Faces")
    elif (rec_type=='Eigen'):
        faceRecognizer = cv2.face.EigenFaceRecognizer_create()
        print("Training using Eigen Faces")
    elif (rec_type=='Fisher'):
        faceRecognizer = cv2.face.FisherFaceRecognizer_create()
        print("Training using Fisher Faces")

    faceRecognizer.train(imagesFaceTrain, np.array(labelsFaceTrain))
    faceRecognizer.write(sys.path[0]+'/Facial_models/face_rec_model.yml')

    with open(sys.path[0]+'/Facial_models/labels_map.pkl', 'wb') as f:
        cPickle.dump(labelsMap, f)

def face_recognition_inference(rec_type):
    #testFiles = glob.glob(sys.path[0]+'/Facial_test_images/face_rec/test/*.jpg')
    #testFiles.sort()
    i = 0
    correct = 0
    error = 0
    faceDetector = dlib.get_frontal_face_detector()
    landmarkDetector = dlib.shape_predictor(sys.path[0]+'/Facial_models/shape_predictor_68_face_landmarks.dat')
    
    if (rec_type=='LBPH'):
        faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
        print("Test using LBPH Faces")
    elif (rec_type=='Eigen'):
        faceRecognizer = cv2.face.EigenFaceRecognizer_create()
        print("Test using Eigen Faces")
    elif (rec_type=='Fisher'):
        faceRecognizer = cv2.face.FisherFaceRecognizer_create()
        print("Test using Fisher Faces")
    
    faceRecognizer.read(sys.path[0]+'/Facial_models/face_rec_model.yml')
    labelsMap = np.load(sys.path[0]+'/Facial_models/labels_map.pkl', allow_pickle=True)

    cam = cv2.VideoCapture(1)

    while(True):
        #imagePath = testFiles[i]
        success, original = cam.read()
        im = cv2.resize(original, (640, 480))
        i += 1

        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        imHeight, imWidth = im.shape[:2]

        landmarks = fr.getLandmarks(faceDetector, landmarkDetector, im)
        landmarks = np.array(landmarks)

        if len(landmarks) == 68:
            x1Limit = landmarks[0][0] - (landmarks[36][0] - landmarks[0][0])
            x2Limit = landmarks[16][0] + (landmarks[16][0] - landmarks[45][0])
            y1Limit = landmarks[27][1] - 3*(landmarks[30][1] - landmarks[27][1])
            y2Limit = landmarks[8][1] + (landmarks[30][1] - landmarks[29][1])

            x1 = max(x1Limit,0)
            x2 = min(x2Limit, imWidth)
            y1 = max(y1Limit, 0)
            y2 = min(y2Limit, imHeight)
            imFace = im[y1:y2, x1:x2]

            alignedFace = alignFace(imFace, landmarks)
            alignedFace = cv2.resize(alignedFace, (faceHeight, faceWidth))
            imFaceFloat = np.float32(alignedFace)/255.0

            predictedLabel = -1
            predictedLabel, score = faceRecognizer.predict(imFaceFloat)
            center = ( int((x1 + x2) /2), int((y1 + y2)/2) )
            radius = int((y2-y1)/2.0)
            text = '{} {}%'.format(labelsMap[predictedLabel],round(score, 5))
            cv2.rectangle(original, (x1, y1), (x2, y2), (0, 255, 0), 5) 
            cv2.putText(original, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)

        cv2.imshow('Face Recognition Demo', original)

        k = cv2.waitKey(10)
          

    cam.release()
    cv2.destroyAllWindows() 


if __name__=="__main__":
    mode = 'test'
    rec_type = 'Fisher'  # 'LBPH' 'Fisher' 'Eigen'

    if mode == 'train':
        training_recognizer(rec_type)
    elif (mode == 'test'):
        face_recognition_inference(rec_type)





    # video process (keep it in case if needed)
    '''
    cameraCapture = cv2.VideoCapture(1)
    success, frame = cameraCapture.read()

    while success and cv2.waitKey(1) == -1:
        success, frame = cameraCapture.read()
        face_detector_ssd(frame)
        cv2.imshow("video", frame)

    cameraCapture.release()
    cv2.destroyAllWindows() 
    '''

    # image process (keep it in case if needed)
    '''
    image_name = "8.jpg"
    split_name = image_name.split(".")

    image_read_path = sys.path[0]+"/Facial_test_images/"+image_name
    image_save_path = sys.path[0]+"/Facial_test_images/output/"+split_name[0]+"_result."+split_name[1]

    image = cv2.imread(image_read_path)

    image = face_detector_ssd(image)
    image = face_detector_haarcascade(image)

    print(image_save_path)

    cv2.imwrite(image_save_path, image)
    cv2.imshow("result", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    '''

    


