import DBHelper
import Facial_Recognition_Registration
import Facial_Recognition_Enrollment
from joblib import Parallel, delayed
import multiprocessing


def update_your_face(firstname, lastname, email, phone):
    # Determines user ID before adding the data to the database.
    # User ID is determined from number of user dataset in database
    # Later on it starts face recognition system and uploads it into the database based on the given user ID.
    users = DBHelper.db.child("Users").get()
    print("Updating the User information...")
    try:
        count = 0
        for user in users.each():
            count += 1
            if DBHelper.get_email("User_" + str(count)) == email:
                break
        print("Face registration start...")
        Facial_Recognition_Registration.register_your_face("User_" + str(count))
        Parallel(n_jobs=multiprocessing.cpu_count())(delayed(update_parallel_user_photos)(i, count) for i in range(10))
        DBHelper.upload_data("User_" + str(count), firstname, lastname, email, phone)
        print("Data saved! Starting enrollment...")
        Facial_Recognition_Enrollment.enroll_face_dataset()
        print("Face registration completed!")
        print("Success.")
    except:
        print("It seems there is no user registered.")


def update_parallel_user_photos(i, count):
    DBHelper.delete_user_photo("User_" + str(count) + "/" + str(i) + ".jpg")
    DBHelper.upload_user_photo("User_" + str(count) + "/" + str(i) + ".jpg")


if __name__ == "__main__":
    f = input('Enter your First Name:')
    l = input('Enter your Last Name:')
    e = input('Enter your E-Mail:')
    p = input('Enter your Phone:')
    update_your_face(f, l, e, p)
