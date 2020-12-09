# Vehicle-Anti-Theft-Face-Recognition-System

README file for the Vehicle Anti Theft Face Recognition System.

# Student Info

Software: Batuhan Basoglu, Feier Zhang, Alexandre Pereira, Sam Hermas Parada

Hardware: Qian Ma, Leyao Li

# Instructions

In order:
1. Start Hardware/Updated_HW_codes/NewMotorFunc.py from the Raspberry Pi for Motor/Alarm functions.
2. Start Main.py for Anti-Theft Face Recognition Software.
3. Start UI/app from android studio or download the app to your phone for the user interface of the program.

# System Requirements

- Android Studio is required for the User Interface component and Pycharm is recommended for the Software and Hardware components.
- For installation of dlib and Anaconda follow these tutorials.
    - https://www.learnopencv.com/install-opencv-3-and-dlib-on-windows-python-only/
    - https://www.pyimagesearch.com/2017/05/01/install-dlib-raspberry-pi/
- For the integration of the other imports in the file try to update the anaconda through 
anaconda command prompt.
    - conda update --all
- For the vehicleantitheftrecognition-firebase-adminsdk-krrgw-05da515de5.json, in DBHelper.py
add the file path to the 'service account' if it doesn't work.

# Notes

- Code might break if you have your webcam is opened during execution. You have to close the webcam first.
- In order to make Hardware part work, you need to execute the hardware code from Raspberry Pi hardware component we designed. 
- You can execute the Software and User Interface components from different computers or from the same computer as Raspberry Pi.
 It is user's choice.