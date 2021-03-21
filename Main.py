import DBHelper
import Start_Engine
import Upload_Face
import Remove_Face
import Check_Up
import Update

if __name__ == "__main__":
    print("Must do the check up First, this may take long...")
    Check_Up.update()
    print("Starting the program.")
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

        if None not in (DBHelper.get_removal_firstname(),
                        DBHelper.get_removal_lastname(),
                        DBHelper.get_removal_email(),
                        DBHelper.get_removal_phone()):
            Remove_Face.remove_your_face(DBHelper.get_removal_firstname(), DBHelper.get_removal_lastname(),
                                         DBHelper.get_removal_email(), DBHelper.get_removal_phone())
            DBHelper.remove_removal_data()

        if None not in (DBHelper.get_update_firstname(),
                        DBHelper.get_update_lastname(),
                        DBHelper.get_update_email(),
                        DBHelper.get_update_phone()):
            Update.update_your_face(DBHelper.get_update_firstname(), DBHelper.get_update_lastname(),
                                    DBHelper.get_update_email(), DBHelper.get_update_phone())
            DBHelper.remove_update_data()
