import os, signal
import RPi.GPIO as GPIO
import pyrebase          # u need to install Pyrebase module firstly
from time import sleep

class Motor:
    print("Starting of the program")
    def __init__(self):
        config = {     
          "apiKey": "AIzaSyAdL0W5HscjEDFPK4BDi6Cnc7FLa30GPYY",
          "authDomain": "vehicleantitheftrecognition.firebaseapp.com",
          "databaseURL": "https://vehicleantitheftrecognition.firebaseio.com/",
          "storageBucket": "vehicleantitheftrecognition.firebaseapp.com"
        }
        self.firebase = pyrebase.initialize_app(config)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #preset GPIO ports for 2 motors
        self.Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}
        self.Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}
        # preset the port for buttons and alarm
        GPIO.setup(26,GPIO.OUT)   # alarm output
        for x in self.Motor1:
            GPIO.setup(self.Motor1[x], GPIO.OUT)
            GPIO.setup(self.Motor2[x], GPIO.OUT)
        #utilize PWM function, enable motors and frequency is 100Hz
        self.EN1 = GPIO.PWM(self.Motor1['EN'], 100)    
        self.EN2 = GPIO.PWM(self.Motor2['EN'], 100)    
        self.EN1.start(0)                    
        self.EN2.start(0)
        #stop signals for motors and alarm
        self.motorStop=True
        self.alarmStop=True
        self.cameraOff=True
        
# new update motor and alarm functions, are able to connect embedded system throught firebase

    def start_motor(self):
        self.motorStop=False
        self.EN1.ChangeDutyCycle(50)
        self.EN2.ChangeDutyCycle(50)
        GPIO.output(self.Motor1['input1'], GPIO.LOW)
        GPIO.output(self.Motor1['input2'], GPIO.HIGH)
        GPIO.output(self.Motor2['input1'], GPIO.HIGH)
        GPIO.output(self.Motor2['input2'], GPIO.LOW)
        print("motor is turned on")

    def stop_motor(self):
        print("stopping motor...")
        self.motorStop=True
        self.EN1.ChangeDutyCycle(0)
        self.EN2.ChangeDutyCycle(0)
        print("motor stops")
    
    def start_alarm(self):
        print("Alarm is turned on")
        self.alarmStop=False
        GPIO.output(26,True)
        return False

    def stop_alarm(self):
        print("Alarm turning off...")
        self.alarmStop=True
        GPIO.output(26,False)
        print("Alarm is off")
        return True

    def kill_target(self, target):
        cmd_run="ps aux | grep {}".format(target)
        out=os.popen(cmd_run).read()
        for line in os.popen("ps ax | grep "+target+" | grep -v grep"):
            fields = line.split()
            #print(fields)
            pid = fields[0]
            a = os.kill(int(pid),signal.SIGKILL)
            print('Killed PID %s, return value:%s' % (pid, a))

    def start_camera(self):
        self.cameraOff=False
        print("Remote camera is turned on")
        os.system('python3 remote_camera.py &')

    def stop_camera(self):        
        self.cameraOff=True
        self.kill_target("remote_camera.py")
        print("Remote camera is off")
        #return False
        
if __name__=="__main__":
    #print("Execute function...")
    
    car=Motor()
    
    while True: # turn on the system forever
        database = car.firebase.database() # get camera on/off signal from firebase
        signals = database.child("signal")
        motorSignal = signals.child(1).child("motor").get().val()
        signals = database.child("signal")
        alarmSignal = signals.child(1).child("alarm").get().val()
        signals = database.child("signal")
        cameraSignal = signals.child(1).child("camera").get().val()
        if (motorSignal=="on" and car.motorStop):
            car.start_motor()
        elif (motorSignal=="off" and not car.motorStop):
            car.stop_motor()
        if (alarmSignal=="on" and car.alarmStop):
            car.start_alarm()
        elif (alarmSignal=="off" and not car.alarmStop):
            car.stop_alarm()
        if (cameraSignal=="on" and car.cameraOff):
            car.start_camera()
        elif (cameraSignal=="off" and not car.cameraOff):
            car.stop_camera()