import DBHelper
import Facial_Recognition_Registration
import Facial_Recognition_Enrollment
from joblib import Parallel, delayed
import multiprocessing
import Facial_Image_Augmentation



def upload_your_face(firstname, lastname, email, phone):
    # Determines user ID before adding the data to the database.
    # User ID is determined from number of user dataset in database
    # Later on it starts face recognition system and uploads it into the database based on the given user ID.
    users = DBHelper.db.child("Users").get()
    print("Registering the User information...")
    try:
        count = 1
        for user in users.each():
            count += 1
        print("Face registration start...")
        
        Facial_Recognition_Registration.register_your_face("User_" + str(count))
        
        Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(upload_parallel_user_photos)(i, count) for i in range(10))
        DBHelper.upload_data("User_" + str(count), firstname, lastname, email, phone)
        
        print("Data saved! Starting enrollment...")
        Facial_Recognition_Enrollment.enroll_face_dataset()
        print("Face registration completed!")
        print("Success.")
    
    except:
        print("Face registration start...")
        
        Facial_Recognition_Registration.register_your_face("User_1")

        Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(upload_parallel_user_photo)(i) for i in range(10))
        DBHelper.upload_data("User_1", firstname, lastname, email, phone)
        
        print("Data saved! Starting enrollment...")
        Facial_Recognition_Enrollment.enroll_face_dataset()
        print("Face registration completed!")
        print("Success.")


def upload_parallel_user_photos(i, count):
    DBHelper.upload_user_photo("User_" + str(count) + "/" + str(i) + ".jpg")


def upload_parallel_user_photo(i):
    DBHelper.upload_user_photo("User_1/" + str(i) + ".jpg")


if __name__ == "__main__":
    f = input('Enter your First Name:')
    l = input('Enter your Last Name:')
    e = input('Enter your E-Mail:')
    p = input('Enter your Phone:')
    upload_your_face(f, l, e, p)