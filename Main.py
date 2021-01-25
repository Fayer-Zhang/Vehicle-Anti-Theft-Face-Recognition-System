import DBHelper
import Start_Engine
import Upload_Face
import Remove_Face
import Check_Up

if __name__ == "__main__":
    print("Starting the Program.")
    while True:
        if DBHelper.get_power() == "on":
            Check_Up.update()
            Start_Engine.start()

        if None not in (DBHelper.get_register_firstname(),
                        DBHelper.get_register_lastname(),
                        DBHelper.get_register_email(),
                        DBHelper.get_register_phone()):
            Upload_Face.upload_your_face(DBHelper.get_register_firstname(), DBHelper.get_register_lastname(),
                                         DBHelper.get_register_email(), DBHelper.get_register_phone())
            Check_Up.update()
            DBHelper.remove_register_data()

        if None not in (DBHelper.get_removal_firstname(),
                        DBHelper.get_removal_lastname(),
                        DBHelper.get_removal_email(),
                        DBHelper.get_removal_phone()):
            Check_Up.update()
            Remove_Face.remove_your_face(DBHelper.get_removal_firstname(), DBHelper.get_removal_lastname(),
                                         DBHelper.get_removal_email(), DBHelper.get_removal_phone())
            DBHelper.remove_removal_data()
