import DBHelper
import Facial_Recognition_Registration


def upload_your_face(firstname, lastname, email, phone, address):
    # Determines user ID before adding the data to the database.
    # User ID is determined from number of user dataset in database
    # Later on it starts face recognition system and uploads it into the database based on the given user ID.
    users = DBHelper.db.child("Users").get()
    try:
        count = 1
        for user in users.each():
            count += 1
        DBHelper.upload_data("User_" + str(count), firstname, lastname, email, phone, address)
        Facial_Recognition_Registration.register_your_face("User_" + str(count))
        for x in range(20):
            DBHelper.upload_user_photo("User_" + str(count) + "/" + str(x) + ".jpg")
    except:
        DBHelper.upload_data("User_1", firstname, lastname, email, phone, address)
        Facial_Recognition_Registration.register_your_face("User_1")
        for x in range(20):
            DBHelper.upload_user_photo("User_1/" + str(x) + ".jpg")


if __name__ == "__main__":
    f = input('Enter your First Name:')
    l = input('Enter your Last Name:')
    e = input('Enter your E-Mail:')
    p = input('Enter your Phone:')
    a = input('Enter your Address:')
    upload_your_face(f, l, e, p, a)