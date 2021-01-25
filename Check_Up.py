import os
import DBHelper


def update():
    # Downloads all the user and thief photos from database to the project folder first or updates them.
    users = DBHelper.db.child("Users").get()
    thieves = DBHelper.db.child("Thieves").get()
    print("Checking and updating User photos...")
    try:
        count = 0
        for user in users.each():
            count += 1
            if not os.path.isdir("Facial_images/face_rec/train/User_" + str(count)):
                os.makedirs("Facial_images/face_rec/train/User_" + str(count))
            for i in range(50):
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
            for i in range(50):
                DBHelper.download_thief_photo("Thief_" + str(count) + "/" + str(i) + ".jpg")
        print("Success.")
    except:
        print("No Thieves are registered.")


if __name__ == "__main__":
    update()
