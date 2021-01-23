import DBHelper
import Start_Engine
import Upload_Face

if __name__ == "__main__":
    print("Starting the Program.")
    while True:
        if DBHelper.get_power() == "on":
            Start_Engine.start()

        if None not in (DBHelper.get_register_firstname(),
                        DBHelper.get_register_lastname(),
                        DBHelper.get_register_email(),
                        DBHelper.get_register_phone()):
            Upload_Face.upload_your_face(DBHelper.get_register_firstname(), DBHelper.get_register_lastname(),
                                         DBHelper.get_register_email(), DBHelper.get_register_phone())
            DBHelper.remove_register_data()
