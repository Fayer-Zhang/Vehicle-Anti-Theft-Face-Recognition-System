import sys
import os
import math
import cv2
import Facial_Recognition_Enrollment


def register_your_face(label):
    num_cap = 50

    path = sys.path[0] + '/Facial_images/face_rec/train/' + label

    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)

    cap = cv2.VideoCapture(0)
    c = 0
    while c < num_cap:
        ret, frame = cap.read()

        cv2.imshow("capture", frame)

        cv2.imwrite(path + '/' + str(c) + '.jpg', frame)

        c = c + 1
        cv2.waitKey(500)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("Face registration start...")
    print()
    label = input('Pleas enter your Name/Label: ')
    register_your_face(label)
    print("Data saved! Starting enrollment...")
    print()
    Facial_Recognition_Enrollment.enroll_face_dataset()  # Need discuss and modify after intergrate with database.
    print("Face registration completed!")
    print()
