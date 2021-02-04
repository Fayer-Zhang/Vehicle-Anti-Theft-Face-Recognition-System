import DBHelper
import os
import shutil
import Facial_Recognition_Enrollment


def remove_your_face(firstname, lastname, email, phone):
    users = DBHelper.db.child("Users").get()
    try:
        count = 0
        count2 = 0
        for user in users.each():
            count += 1
        print("Removing the specified User...")
        for user in users.each():
            count2 += 1
            if DBHelper.get_firstname("User_" + str(count2)) == firstname and DBHelper.get_lastname(
                    "User_" + str(count2)) == lastname and DBHelper.get_email(
                "User_" + str(count2)) == email and DBHelper.get_phone("User_" + str(count2)) == phone:
                DBHelper.remove_data("User_" + str(count2))
                for i in range(50):
                    DBHelper.delete_user_photo("User_" + str(count2) + "/" + str(i) + ".jpg")
                print("Successfully removed the User.")
                break
        print("Reorganizing the Users... (This may take long time.)")
        if count2 != count and count - count2 - 1 != 0:
            for x in range(count - count2 - 1):
                DBHelper.upload_data("User_" + str(count2), DBHelper.get_firstname("User_" + str(count2 + 1)),
                                     DBHelper.get_lastname("User_" + str(count2 + 1)),
                                     DBHelper.get_email("User_" + str(count2 + 1)),
                                     DBHelper.get_phone("User_" + str(count2 + 1)))
                if not os.path.isdir("Facial_images/face_rec/train/User_" + str(count2)):
                    os.makedirs("Facial_images/face_rec/train/User_" + str(count2))
                for i in range(50):
                    DBHelper.download_user_photo_other("User_" + str(count2 + 1) + "/" + str(i) + ".jpg",
                                                       "User_" + str(count2) + "/" + str(i) + ".jpg")
                    DBHelper.upload_user_photo("User_" + str(count2) + "/" + str(i) + ".jpg")
                    DBHelper.delete_user_photo("User_" + str(count2 + 1) + "/" + str(i) + ".jpg")
                count2 += 1
            DBHelper.remove_data("User_" + str(count))
            shutil.rmtree("Facial_images/face_rec/train/User_" + str(count))
        elif count2 != count and count - count2 - 1 == 0:
            DBHelper.upload_data("User_" + str(count2), DBHelper.get_firstname("User_" + str(count2 + 1)),
                                 DBHelper.get_lastname("User_" + str(count2 + 1)),
                                 DBHelper.get_email("User_" + str(count2 + 1)),
                                 DBHelper.get_phone("User_" + str(count2 + 1)))
            if not os.path.isdir("Facial_images/face_rec/train/User_" + str(count2)):
                os.makedirs("Facial_images/face_rec/train/User_" + str(count2))
            for i in range(50):
                DBHelper.download_user_photo_other("User_" + str(count2 + 1) + "/" + str(i) + ".jpg",
                                                   "User_" + str(count2) + "/" + str(i) + ".jpg")
                DBHelper.upload_user_photo("User_" + str(count2) + "/" + str(i) + ".jpg")
                DBHelper.delete_user_photo("User_" + str(count2 + 1) + "/" + str(i) + ".jpg")
            DBHelper.remove_data("User_" + str(count))
            shutil.rmtree("Facial_images/face_rec/train/User_" + str(count))
        Facial_Recognition_Enrollment.enroll_face_dataset()
        print("Success.")
    except:
        print("No Users exist for User Removal.")


if __name__ == "__main__":
    f = input('Enter your First Name:')
    l = input('Enter your Last Name:')
    e = input('Enter your E-Mail:')
    p = input('Enter your Phone:')
    remove_your_face(f, l, e, p)
