import os, signal
import RPi.GPIO as GPIO
import pyrebase          # u need to install Pyrebase module firstly
import time
from picamera import PiCamera
from time import sleep

class Car:
    print("Starting of the program")
    def __init__(self):
        config = {     
            "apiKey": "AIzaSyAdL0W5HscjEDFPK4BDi6Cnc7FLa30GPYY",
            "authDomain": "vehicleantitheftrecognition.firebaseapp.com",
            "databaseURL": "https://vehicleantitheftrecognition.firebaseio.com",
            "projectId": "vehicleantitheftrecognition",
            "storageBucket": "vehicleantitheftrecognition.appspot.com",
            "messagingSenderId": "163692530359",
            "appId": "1:163692530359:web:b6dc7ccfc56a79afb11b32",
            "measurementId": "G-EPWP2LK89Q"
        }
        
        self.firebase = pyrebase.initialize_app(config)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # preset GPIO ports for 2 motors
        self.Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}
        self.Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}
        
        # preset the port for buttons and alarm
        GPIO.setup(26,GPIO.OUT)   # alarm output
        
        # preset the port for the distance sensor
        self.GPIO_TRIGGER = 18
        self.GPIO_ECHO = 4
        # set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        
        for x in self.Motor1:
            GPIO.setup(self.Motor1[x], GPIO.OUT)
            GPIO.setup(self.Motor2[x], GPIO.OUT)
        
        # utilize PWM function, enable motors and frequency is 100Hz
        self.EN1 = GPIO.PWM(self.Motor1['EN'], 100)    
        self.EN2 = GPIO.PWM(self.Motor2['EN'], 100)    
        self.EN1.start(0)                    
        self.EN2.start(0)
        
        # stop signals for motors and alarm
        self.motorStop=True
        self.alarmStop=True
        self.cameraOff=True
        
        # countor for theaf picture been taken
        self.counter = self.firebase.database().child("signal").child(1).child("counter").get().val()
        #print(str(self.counter))
        
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
    
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance
        
if __name__=="__main__":
    #print("Execute function...")
    
    car=Car()
    
    while True: # turn on the system forever
        # get connection to firebase
        database = car.firebase.database()
        signals = database.child("signal")
        auth = car.firebase.auth()
        storage = car.firebase.storage()
        
        # get signal from firebase
        motorSignal = signals.child(1).child("motor").get().val()
        signals = database.child("signal")
        alarmSignal = signals.child(1).child("alarm").get().val()
        signals = database.child("signal")
        cameraSignal = signals.child(1).child("camera").get().val()
        
        # get distance data from distance sensor
        dist = car.distance()
        #print ("Measured Distance = %.1f cm" % dist)
        
        # Turn on motor if get sensor signal
        if (motorSignal=="on" and car.motorStop):
            car.start_motor()
        elif ((motorSignal=="off" or dist<=5) and not car.motorStop):
            # Stop the motor if the vehicle is too close to the item at front as well
            car.stop_motor()
            
        # Turn on alarm if get sensor signal
        if (alarmSignal=="on" and car.alarmStop):
            car.start_alarm()
        elif (alarmSignal=="off" and not car.alarmStop):
            car.stop_alarm()
            
        # Turn on remote camera if get sensor signal
        if (cameraSignal=="on" and car.cameraOff):
            car.start_camera()
        elif (cameraSignal=="off" and not car.cameraOff):
            car.stop_camera()
            
        # Take a picture of someone or some thing try to get close to the vehicle
        if (dist<=15 and car.cameraOff and car.motorStop and car.alarmStop):
            time.sleep(5)
            dist = car.distance()
            if (dist<=15):
                print('Take a theaf picture due to distance at ' + str(int(dist)) + 'cm')
                camera = PiCamera()
                camera.start_preview()
                # Camera warm-up time
                time.sleep(1)
                camera.capture('/home/pi/Vehicle-Anti-Theft-Face-Recognition-System/sensor/picture'+str(car.counter)+'.jpg')
                camera.close()
                storage.child('Photos_of_Thieves/Thief_Sensor/picture'+str(car.counter)+'.jpg').put('/home/pi/Vehicle-Anti-Theft-Face-Recognition-System/sensor/picture'+str(car.counter)+'.jpg')
                car.counter+=1
                car.firebase.database().child("signal").child(1).child("counter").set(car.counter)
        time.sleep(1)