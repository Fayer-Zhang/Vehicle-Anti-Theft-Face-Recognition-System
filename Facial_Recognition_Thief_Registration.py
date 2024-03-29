import sys
import os
import math
import cv2


def register_your_face(label):
    num_cap = 10

    path = sys.path[0] + '/Photos_of_Thieves/' + label

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
    print("Data is successfully saved.")
    print()
