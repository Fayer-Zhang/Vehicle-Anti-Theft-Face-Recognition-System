import DBHelper
'import Start_Engine'
import Upload_Face

if __name__ == "__main__":
    print("Starting the Program.")
    while True:
        if DBHelper.get_power() == "on":
            'Start_Engine.start()'

        if None not in (DBHelper.get_signal_firstname(),
                        DBHelper.get_signal_lastname(),
                        DBHelper.get_signal_email(),
                        DBHelper.get_signal_phone(),
                        DBHelper.get_signal_address()):
            Upload_Face.upload_your_face(DBHelper.get_signal_firstname(), DBHelper.get_signal_lastname(),
                                         DBHelper.get_signal_email(), DBHelper.get_signal_phone(),
                                         DBHelper.get_signal_address())
            DBHelper.reset_data()
