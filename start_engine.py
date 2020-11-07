import DBHelper
import Facial_Recognition_Software


def start():
    # Downloads all the user and thief photos from database to the project folder first or updates them.
    count = 0
    users = DBHelper.db.child("Users").get()
    try:
        for user in users.each():
            count = +1
            DBHelper.download_user_photo("user" + str(count) + "_" + str(1) + ".jpg")
            DBHelper.download_user_photo("user" + str(count) + "_" + str(2) + ".jpg")
            DBHelper.download_user_photo("user" + str(count) + "_" + str(3) + ".jpg")
            DBHelper.download_user_photo("user" + str(count) + "_" + str(4) + ".jpg")
            DBHelper.download_user_photo("user" + str(count) + "_" + str(5) + ".jpg")
            DBHelper.download_user_photo("user" + str(count) + "_" + str(6) + ".jpg")
            DBHelper.download_user_photo("user" + str(count) + "_" + str(7) + ".jpg")
    except:
        print("No Users are registered.")
    count = 0
    try:
        for user in users.each():
            count = +1
            DBHelper.download_thief_photo("user" + str(count) + "_" + str(1) + ".jpg")
            DBHelper.download_thief_photo("user" + str(count) + "_" + str(2) + ".jpg")
            DBHelper.download_thief_photo("user" + str(count) + "_" + str(3) + ".jpg")
            DBHelper.download_thief_photo("user" + str(count) + "_" + str(4) + ".jpg")
            DBHelper.download_thief_photo("user" + str(count) + "_" + str(5) + ".jpg")
            DBHelper.download_thief_photo("user" + str(count) + "_" + str(6) + ".jpg")
            DBHelper.download_thief_photo("user" + str(count) + "_" + str(7) + ".jpg")
    except:
        return 0


start()
