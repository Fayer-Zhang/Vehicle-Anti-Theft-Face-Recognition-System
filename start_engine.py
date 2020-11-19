import os
import DBHelper
import Facial_Recognition_Wrapper


def start():
    # Downloads all the user and thief photos from database to the project folder first or updates them.
    # Then it starts Facial Recognition Software.
    users = DBHelper.db.child("Users").get()
    thieves = DBHelper.db.child("Thieves").get()
    print("Checking and updating User photos...")
    try:
        count = 0
        for user in users.each():
            count += 1
            if not os.path.isdir("Facial_images/face_rec/train/User_" + str(count)):
                os.makedirs("Facial_images/face_rec/train/User_" + str(count))
            for i in range(20):
                DBHelper.download_user_photo("User_" + str(count) + "/" + str(i) + ".jpg")
        print("Success.")
    except:
        print("No Users are registered.")
    count = 0
    print("Checking and updating Thief photos...")
    try:
        for thief in thieves.each():
            count += 1
            if not os.path.isdir("Photos_of_Thieves/Thief_" + str(count)):
                os.makedirs("Photos_of_Thieves/Thief_" + str(count))
            for i in range(20):
                DBHelper.download_thief_photo("Thief_" + str(count) + "/" + str(i) + ".jpg")
        print("Success.")
    except:
        print("No Thieves are registered.")
    Facial_Recognition_Wrapper.training_recognizer("LBPH")
    Facial_Recognition_Wrapper.face_recognition_inference("LBPH")


if __name__ == "__main__":
    start()