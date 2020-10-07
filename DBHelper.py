import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyAdL0W5HscjEDFPK4BDi6Cnc7FLa30GPYY",
    'authDomain': "vehicleantitheftrecognition.firebaseapp.com",
    'databaseURL': "https://vehicleantitheftrecognition.firebaseio.com",
    'projectId': "vehicleantitheftrecognition",
    'storageBucket': "vehicleantitheftrecognition.appspot.com",
    'messagingSenderId': "163692530359",
    'appId': "1:163692530359:web:b6dc7ccfc56a79afb11b32",
    'measurementId': "G-EPWP2LK89Q"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

class DBHelper:

    # Create account function which creates a new authentication info.
    def createaccount(username, password, confirmpassword):
        email = username + "@hotmail.com"
        if password == confirmpassword:
            auth.create_user_with_email_and_password(email,password)
            print("Account sucessfully created.")
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
    def uploadData(userID, firstname, lastname, email, phone, address):
        data = {"First Name": firstname, "Last Name": lastname, "E-Mail": email, "Phone": phone, "Address": address}
        db.child("Users").child(userID).set(data)

    # Removes the data of specified user uploaded into firebase.
    def removeData(userID):
        db.child("Users").child(userID).remove()

    # Returns the first name or else an empty string.
    def getfirstname(userID):
        firstname = ""
        users = db.child("Users").get()
        for user in users.each():
            if user.key() == userID:
                firstname = user.val()["First Name"]
        return firstname

    # Returns the last name or else an empty string.
    def getlastname(userID):
        lastname = ""
        users = db.child("Users").get()
        for user in users.each():
            if user.key() == userID:
                lastname = user.val()["Last Name"]
        return lastname

    # Returns the e-mail or else an empty string.
    def getemail(userID):
        email = ""
        users = db.child("Users").get()
        for user in users.each():
            if user.key() == userID:
                email = user.val()["E-Mail"]
        return email

    # Returns the phone or else an empty string.
    def getphone(userID):
        phone = ""
        users = db.child("Users").get()
        for user in users.each():
            if user.key() == userID:
                phone = user.val()["Phone"]
        return phone

    # Returns the address or else an empty string.
    def getaddress(userID):
        address = ""
        users = db.child("Users").get()
        for user in users.each():
            if user.key() == userID:
                address = user.val()["Address"]
        return address

    # Uploads the photo of user, input should be something like "example.png"
    def uploaduserphoto(userphoto):
        userphoto_str = str(userphoto)
        storage.child("Photos_of_Users/" + str(userphoto)).put("Photos_of_Users/" + str(userphoto))

    # Uploads the photo of user, input should be something like "example.png"
    def uploadthiefphoto(userphoto):
        userphoto_str = str(userphoto)
        storage.child("Photos_of_Thieves/" + str(userphoto)).put("Photos_of_Thieves/" + str(userphoto))

    # Downloads all the user photos, input should be something like "example.png"
    def downloadalluserphotos(self):
        storage.child("Photos_of_Users").download("Storage_from_Database")

    # Downloads all the thief photos, input should be something like "example.png"
    def downloadallthiefphotos(self):
        storage.child("Photos_of_Thieves").download("Storage_from_Thieves")