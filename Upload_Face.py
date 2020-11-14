import DBHelper
import Facial_Recognition_Registration


def upload_your_face(firstname, lastname, email, phone, address):
    # Determines user ID before adding the data to the database.
    # User ID is determined from number of user dataset in database
    count = 0
    users = DBHelper.db.child("Users").get()
    try:
        for user in users.each():
            count += 1
        DBHelper.upload_data("user_" + str(count), firstname, lastname, email, phone, address)
        Facial_Recognition_Registration.register_your_face("user_" + str(count))
        for x in range(20):
            DBHelper.upload_user_photo("user_" + str(count) + "/" + str(x) + ".jpg")
    except:
        DBHelper.upload_data("1", firstname, lastname, email, phone, address)
        Facial_Recognition_Registration.register_your_face("user_1")
        for x in range(20):
            DBHelper.upload_user_photo("user_1/" + str(x) + ".jpg")
