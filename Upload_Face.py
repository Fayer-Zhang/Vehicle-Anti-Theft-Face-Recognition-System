import DBHelper
import Facial_Recognition_Software


def upload_your_face(firstname, lastname, email, phone, address):
    # Determines user ID before adding the data to the database.
    # User ID is determined from number of user dataset in database
    count = 0
    users = DBHelper.db.child("Users").get()
    try:
        for user in users.each():
            count += 1
        DBHelper.upload_data(count, firstname, lastname, email, phone, address)
    except:
        DBHelper.upload_data("1", firstname, lastname, email, phone, address)


