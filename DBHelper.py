import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyAdL0W5HscjEDFPK4BDi6Cnc7FLa30GPYY",
    'authDomain': "vehicleantitheftrecognition.firebaseapp.com",
    'databaseURL': "https://vehicleantitheftrecognition.firebaseio.com",
    'projectId': "vehicleantitheftrecognition",
    'storageBucket': "vehicleantitheftrecognition.appspot.com",
    'messagingSenderId': "163692530359",
    'appId': "1:163692530359:web:b6dc7ccfc56a79afb11b32",
    'measurementId': "G-EPWP2LK89Q",
    'serviceAccount': 'vehicleantitheftrecognition-firebase-adminsdk-krrgw-05da515de5.json'
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()


# Create account function which creates a new authentication info.
def create_account(username, password, confirm_password):
    email = username + "@hotmail.com"
    if password == confirm_password:
        auth.create_user_with_email_and_password(email, password)
        print("Account successfully created.")
    else:
        print("Confirmed password doesn't match to other password.")


# Login function which verifies the given authentication info.
def login(username, password):
    email = username + "@hotmail.com"
    try:
        auth.sign_in_with_email_and_password(email, password)
        print("Successfully Logged in.")
    except:
        print("Invalid username or password.")


# Uploads the data of specified user uploaded into firebase.
def upload_data(user_id, firstname, lastname, email, phone, address):
    data = {"First Name": firstname, "Last Name": lastname, "E-Mail": email, "Phone": phone, "Address": address}
    db.child("Users").child(user_id).set(data)


# Removes the data of specified user uploaded into firebase.
def remove_data(user_id):
    db.child("Users").child(user_id).remove()


# Returns the first name or else an empty string.
def get_firstname(user_id):
    firstname = ""
    users = db.child("Users").get()
    for user in users.each():
        if user.key() == user_id:
            firstname = user.val()["First Name"]
    return firstname


# Returns the last name or else an empty string.
def get_lastname(user_id):
    lastname = ""
    users = db.child("Users").get()
    for user in users.each():
        if user.key() == user_id:
            lastname = user.val()["Last Name"]
    return lastname


# Returns the e-mail or else an empty string.
def get_email(user_id):
    email = ""
    users = db.child("Users").get()
    for user in users.each():
        if user.key() == user_id:
            email = user.val()["E-Mail"]
    return email


# Returns the phone or else an empty string.
def get_phone(user_id):
    phone = ""
    users = db.child("Users").get()
    for user in users.each():
        if user.key() == user_id:
            phone = user.val()["Phone"]
    return phone


# Returns the address or else an empty string.
def get_address(user_id):
    address = ""
    users = db.child("Users").get()
    for user in users.each():
        if user.key() == user_id:
            address = user.val()["Address"]
    return address


# Uploads the photo of user, input should be something like "example.png"
def upload_user_photo(user_photo):
    storage.child("Photos_of_Users/" + user_photo).put("Photos_of_Users/" + user_photo)


# Uploads the photo of thief, input should be something like "example.png"
def upload_thief_photo(user_photo):
    storage.child("Photos_of_Thieves/" + user_photo).put("Photos_of_Thieves/" + user_photo)


# Downloads the specified user photo.
def download_user_photo(user_photo):
    storage.child("Photos_of_Users/" + str(user_photo)).download("Users_from_Database/" + str(user_photo))


# Downloads the specified thief photo.
def download_thief_photo(user_photo):
    storage.child("Photos_of_Thieves/" + str(user_photo)).download("Thieves_from_Database/" + str(user_photo))


# Deletes photo of the specified user.
def delete_user_photo(user_photo):
    storage.delete('Photos_of_Users/' + user_photo)

# Deletes photo of the specified thief.
def delete_thief_photo(user_photo):
    storage.delete('Photos_of_Thieves/' + user_photo)
