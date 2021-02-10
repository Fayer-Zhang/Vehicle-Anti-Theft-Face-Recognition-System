import DBHelper
import Facial_Recognition_Inference


def start():
    # It checks if a user is registered then starts the Facial Recognition Software.
    users = DBHelper.db.child("Users").get()
    count = 0
    for user in users.each():
        count += 1
    if count != 0:
        print("Initializing the Face Recognition Software...")
        Facial_Recognition_Inference.inference()
    else:
        print("No Users exist for Facial Recognition Software.")


if __name__ == "__main__":
    DBHelper.set_power("on")
    start()
