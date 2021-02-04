import DBHelper
import Facial_Recognition_Thief_Registration
from datetime import datetime


def upload_thief_face():
    # Determines thief ID before adding the data to the database.
    # Thief ID is determined from number of user dataset in database
    # Later on it starts face recognition system and uploads it into the database based on the given thief ID.
    thieves = DBHelper.db.child("Thieves").get()
    try:
        count = 1
        for thief in thieves.each():
            count += 1
        Facial_Recognition_Thief_Registration.register_your_face("Thief_" + str(count))
        for i in range(50):
            DBHelper.upload_thief_photo("Thief_" + str(count) + "/" + str(i) + ".jpg")
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        DBHelper.upload_thief_data("Thief_" + str(count), date, time)
        print("An intruder is recorded.")
    except:
        Facial_Recognition_Thief_Registration.register_your_face("Thief_1")
        for i in range(50):
            DBHelper.upload_thief_photo("Thief_1/" + str(i) + ".jpg")
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        DBHelper.upload_thief_data("Thief_1", date, time)
        print("An intruder is recorded.")


if __name__ == "__main__":
    upload_thief_face()
