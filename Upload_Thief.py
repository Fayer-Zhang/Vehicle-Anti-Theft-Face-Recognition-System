import DBHelper
import Facial_Recognition_Thief_Registration
from datetime import datetime
from joblib import Parallel, delayed
import multiprocessing


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
        Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(upload_parallel_thief_photos)(i, count) for i in range(50))
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        DBHelper.upload_thief_data("Thief_" + str(count), date, time)
        print("An intruder is recorded.")
    except:
        Facial_Recognition_Thief_Registration.register_your_face("Thief_1")
        Parallel(n_jobs=multiprocessing.cpu_count())(
            delayed(upload_parallel_thief_photo)(i) for i in range(50))
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M:%S")
        DBHelper.upload_thief_data("Thief_1", date, time)
        print("An intruder is recorded.")


def upload_parallel_thief_photos(i, count):
    DBHelper.upload_thief_photo("Thief_" + str(count) + "/" + str(i) + ".jpg")


def upload_parallel_thief_photo(i):
    DBHelper.upload_thief_photo("Thief_1/" + str(i) + ".jpg")


if __name__ == "__main__":
    upload_thief_face()