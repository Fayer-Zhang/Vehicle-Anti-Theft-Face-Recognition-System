import DBHelper

def remove_your_face():
    users = DBHelper.db.child("Users").get()
    try:
        count = 0
        for user in users.each():
            count += 1
        DBHelper.upload_data("User_" + str(count), firstname, lastname, email, phone)
        Facial_Recognition_Registration.register_your_face("User_" + str(count))
        for i in range(20):
            DBHelper.upload_user_photo("User_" + str(count) + "/" + str(i) + ".jpg")
    except:
        print("No Users are registered.")