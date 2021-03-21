import pyrebase
import sys

pwd = sys.path[0]

firebaseConfig = {
    'apiKey': "AIzaSyAdL0W5HscjEDFPK4BDi6Cnc7FLa30GPYY",
    'authDomain': "vehicleantitheftrecognition.firebaseapp.com",
    'databaseURL': "https://vehicleantitheftrecognition.firebaseio.com",
    'projectId': "vehicleantitheftrecognition",
    'storageBucket': "vehicleantitheftrecognition.appspot.com",
    'messagingSenderId': "163692530359",
    'appId': "1:163692530359:web:b6dc7ccfc56a79afb11b32",
    'measurementId': "G-EPWP2LK89Q",
    'serviceAccount': pwd + '/vehicleantitheftrecognition-firebase-adminsdk-krrgw-05da515de5.json'
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()


# Create account function which creates a new authentication info.
def create_account(email, password, confirm_password):
    if password == confirm_password:
        auth.create_user_with_email_and_password(email, password)
        print("Account successfully created.")
    else:
        print("Confirmed password doesn't match to other password.")


# Login function which verifies the given authentication info.
def login(email, password):
    try:
        auth.sign_in_with_email_and_password(email, password)
        print("Successfully Logged in.")
    except:
        print("Invalid username or password.")


# Uploads the data of specified user into firebase.
def upload_data(user_id, firstname, lastname, email, phone):
    data = {"First Name": firstname, "Last Name": lastname, "E-Mail": email, "Phone": phone}
    db.child("Users").child(user_id).set(data)


# Removes the data of specified user from firebase.
def remove_data(user_id):
    db.child("Users").child(user_id).remove()


# Returns the first name or else an empty string.
def get_firstname(user_id):
    firstname = db.child("Users").child(str(user_id)).child("First Name").get().val()
    return firstname


# Returns the last name or else an empty string.
def get_lastname(user_id):
    lastname = db.child("Users").child(str(user_id)).child("Last Name").get().val()
    return lastname


# Returns the e-mail or else an empty string.
def get_email(user_id):
    email = db.child("Users").child(str(user_id)).child("E-Mail").get().val()
    return email


# Returns the phone or else an empty string.
def get_phone(user_id):
    phone = db.child("Users").child(str(user_id)).child("Phone").get().val()
    return phone


# Uploads the photos of user, input should be something like "example.jpg"
def upload_user_photo(user_id):
    storage.child("Photos_of_Users/" + user_id).put("Facial_images/face_rec/train/" + user_id)


# Uploads the photos of thief, input should be something like "example.jpg"
def upload_thief_photo(thief_id):
    storage.child("Photos_of_Thieves/" + thief_id).put("Photos_of_Thieves/" + thief_id)


# Downloads the specified user's photos, input should be something like "example.jpg"
def download_user_photo(user_id):
    storage.child("Photos_of_Users/" + user_id).download("Facial_images/face_rec/train/" + user_id)


# Downloads the specified thief's photos, input should be something like "example.jpg"
def download_thief_photo(thief_id):
    storage.child("Photos_of_Thieves/" + thief_id).download("Photos_of_Thieves/" + thief_id)


# Deletes photo of the specified user.
def delete_user_photo(user_photo):
    storage.delete('Photos_of_Users/' + user_photo)


# Deletes photo of the specified thief.
def delete_thief_photo(user_photo):
    storage.delete('Photos_of_Thieves/' + user_photo)


# Motor signal getter
def get_motor():
    motor = db.child("signal").child("1").child("motor").get().val()
    return motor


# Motor signal setter
def set_motor(motor):
    db.child("signal").child("1").child("motor").set(motor)


# Alarm signal getter
def get_alarm():
    alarm = db.child("signal").child("1").child("alarm").get().val()
    return alarm


# Alarm signal setter
def set_alarm(alarm):
    db.child("signal").child("1").child("alarm").set(alarm)


# Power signal getter
def get_power():
    alarm = db.child("signal").child("1").child("power").get().val()
    return alarm


# Power signal setter
def set_power(power):
    db.child("signal").child("1").child("power").set(power)


# Returns the first name or else an empty string.
def get_register_firstname():
    firstname = db.child("signal").child("2").child("First Name").get().val()
    return firstname


# Returns the last name or else an empty string.
def get_register_lastname():
    lastname = db.child("signal").child("2").child("Last Name").get().val()
    return lastname


# Returns the e-mail or else an empty string.
def get_register_email():
    email = db.child("signal").child("2").child("E-Mail").get().val()
    return email


# Returns the phone or else an empty string.
def get_register_phone():
    phone = db.child("signal").child("2").child("Phone").get().val()
    return phone


# Uploads the data of user input into firebase.
def upload_register_data(firstname, lastname, email, phone):
    data = {"First Name": firstname, "Last Name": lastname, "E-Mail": email, "Phone": phone}
    db.child("signal").child("2").set(data)


# Removes the inputs.
def remove_register_data():
    db.child("signal").child("2").remove()


# Downloads user photo to the specified folder.
def download_user_photo_other(user_id, other_id):
    storage.child("Photos_of_Users/" + user_id).download("Facial_images/face_rec/train/" + other_id)


# Downloads thief photo to the specified folder.
def download_thief_photo_other(thief_id, other_id):
    storage.child("Photos_of_Thieves/" + thief_id).download("Photos_of_Thieves/" + other_id)


# Returns the first name or else an empty string.
def get_removal_firstname():
    firstname = db.child("signal").child("3").child("First Name").get().val()
    return firstname


# Returns the last name or else an empty string.
def get_removal_lastname():
    lastname = db.child("signal").child("3").child("Last Name").get().val()
    return lastname


# Returns the e-mail or else an empty string.
def get_removal_email():
    email = db.child("signal").child("3").child("E-Mail").get().val()
    return email


# Returns the phone or else an empty string.
def get_removal_phone():
    phone = db.child("signal").child("3").child("Phone").get().val()
    return phone


# Uploads the data of user input into firebase.
def upload_removal_data(firstname, lastname, email, phone):
    data = {"First Name": firstname, "Last Name": lastname, "E-Mail": email, "Phone": phone}
    db.child("signal").child("3").set(data)


# Removes the inputs.
def remove_removal_data():
    db.child("signal").child("3").remove()


# Uploads the data of specified thief into firebase.
def upload_thief_data(thief_id, date, time):
    data = {"Date": date, "Time": time}
    db.child("Thieves").child(thief_id).set(data)


# Returns the e-mail or else an empty string.
def get_time(thief_id):
    email = db.child("Thieves").child(str(thief_id)).child("Time").get().val()
    return email


# Returns the phone or else an empty string.
def get_date(thief_id):
    phone = db.child("Thieves").child(str(thief_id)).child("Date").get().val()
    return phone

# Returns the first name or else an empty string.
def get_update_firstname():
    firstname = db.child("signal").child("4").child("First Name").get().val()
    return firstname


# Returns the last name or else an empty string.
def get_update_lastname():
    lastname = db.child("signal").child("4").child("Last Name").get().val()
    return lastname


# Returns the e-mail or else an empty string.
def get_update_email():
    email = db.child("signal").child("4").child("E-Mail").get().val()
    return email


# Returns the phone or else an empty string.
def get_update_phone():
    phone = db.child("signal").child("4").child("Phone").get().val()
    return phone


# Uploads the data of user input into firebase.
def upload_update_data(firstname, lastname, email, phone):
    data = {"First Name": firstname, "Last Name": lastname, "E-Mail": email, "Phone": phone}
    db.child("signal").child("4").set(data)


# Removes the inputs.
def remove_update_data():
    db.child("signal").child("4").remove()


if __name__ == "__main__":
    upload_data("User_3", "RandomFirst", "RandomLast", "Random@gmail.com", "0000000000")
