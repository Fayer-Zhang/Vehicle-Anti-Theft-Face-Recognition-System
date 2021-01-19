import os,sys,time
import dlib
import cv2
import numpy as np

try:
  import cPickle  # Python 2
except ImportError:
  import _pickle as cPickle  # Python 3


pwd = sys.path[0]
PREDICTOR_PATH = pwd + '/Facial_models/shape_predictor_68_face_landmarks.dat'
FACE_RECOGNITION_MODEL_PATH = pwd + '/Facial_models/dlib_face_recognition_resnet_model_v1.dat'

SKIP_FRAMES = 10
THRESHOLD = 0.4

faceDetector = dlib.get_frontal_face_detector()
shapePredictor = dlib.shape_predictor(PREDICTOR_PATH)
faceRecognizer = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)

index = np.load(pwd+'/Facial_models/index.pkl', allow_pickle=True)
faceDescriptorsEnrolled = np.load(pwd+'/Facial_models/descriptors.npy')


cam = cv2.VideoCapture(1)

count = 0

while True:
  t = time.time()
  success, im = cam.read()

  if not success:
    print('cannot capture input from camera')
    break


  if (count % SKIP_FRAMES) == 0:

    img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    faces = faceDetector(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    for face in faces:

      shape = shapePredictor(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), face)

      x1 = face.left()
      y1 = face.top()
      x2 = face.right()
      y2 = face.bottom()

      faceDescriptor = faceRecognizer.compute_face_descriptor(img, shape)

      # dlib format to list
      faceDescriptorList = [m for m in faceDescriptor]
      # to numpy array
      faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
      faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]

      # Euclidean distances
      distances = np.linalg.norm(faceDescriptorsEnrolled - faceDescriptorNdarray, axis=1)
      
      # Calculate minimum distance and index of face
      argmin = np.argmin(distances)    # index
      minDistance = distances[argmin]  # minimum distance

   
      if minDistance <= THRESHOLD:
        label = index[argmin]
      else:
        label = 'unknown'

      print("time taken = {:.3f} seconds".format(time.time() - t))


      cv2.rectangle(im, (x1, y1), (x2, y2), (0, 255, 0), 2)

      #center = (int((x1 + x2)/2.0), int((y1 + y2)/2.0))
      #radius = int((y2-y1)/2.0)
      #color = (0, 255, 0)
      #cv2.circle(im, center, radius, color, thickness=1, lineType=8, shift=0)

      font_face = cv2.FONT_HERSHEY_SIMPLEX
      font_scale = 0.8
      text_color = (0, 255, 0)
      printLabel = '{} {:0.4f}'.format(label, minDistance)
      cv2.putText(im, printLabel, (int(x1), int(y1)) , font_face, font_scale, text_color, thickness=2)


    cv2.imshow('img', im)

  k = cv2.waitKey(1) & 0xff
  if k == 27:
    break 

  count += 1
cv2.destroyAllWindows()