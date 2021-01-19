import os
import dlib
import cv2
import sys
import numpy as np

try:
  import cPickle  # Python2.
except ImportError:
  import _pickle as cPickle  # Python3.

def enroll_face_dataset():
  pwd = sys.path[0]
  PREDICTOR_PATH = pwd + '/Facial_models/shape_predictor_68_face_landmarks.dat'
  FACE_RECOGNITION_MODEL_PATH = pwd + '/Facial_models/dlib_face_recognition_resnet_model_v1.dat'

  faceDetector = dlib.get_frontal_face_detector()
  shapePredictor = dlib.shape_predictor(PREDICTOR_PATH)
  faceRecognizer = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)


  faceDatasetFolder = pwd + '/Facial_images/face_rec/train/'

  subfolders = []
  for x in os.listdir(faceDatasetFolder):
    xpath = os.path.join(faceDatasetFolder, x)
    if os.path.isdir(xpath):
      subfolders.append(xpath)


  nameLabelMap = {}
  labels = []
  imagePaths = []
  for i, subfolder in enumerate(subfolders):
    for x in os.listdir(subfolder):
      xpath = os.path.join(subfolder, x)
      if x.endswith('jpg'):
        imagePaths.append(xpath)
        labels.append(i)
        nameLabelMap[xpath] = subfolder.split('/')[-1]

  index = {}
  i = 0
  faceDescriptors = None
  for imagePath in imagePaths:
    print("processing: {}".format(imagePath))
    img = cv2.imread(imagePath)

    faces = faceDetector(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    print("{} Face(s) found".format(len(faces)))

    for k, face in enumerate(faces):

      shape = shapePredictor(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), face)

      landmarks = [(p.x, p.y) for p in shape.parts()]

      faceDescriptor = faceRecognizer.compute_face_descriptor(img, shape)

    
      faceDescriptorList = [x for x in faceDescriptor]
      faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
      faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]


      if faceDescriptors is None:
        faceDescriptors = faceDescriptorNdarray
      else:
        faceDescriptors = np.concatenate((faceDescriptors, faceDescriptorNdarray), axis=0)

      index[i] = nameLabelMap[imagePath]
      i += 1

  # Write descriors and index to disk
  np.save(pwd+'/Facial_models/descriptors.npy', faceDescriptors)
  with open(pwd+'/Facial_models/index.pkl', 'wb') as f:
    cPickle.dump(index, f)
