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
        GPIO.setup(5,GPIO.IN)     # start motor button, initially True
        GPIO.setup(13,GPIO.IN)    # stop motor button, initially True
        GPIO.setup(16,GPIO.IN)    # start alarm button, initially True
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
        self.motorStop=False
        self.alarmStop=False
        
     
    
# new update motor and alarm functions, are able to connect embedded system throught firebase

    def start_motor(self):
        
        self.motorStop=self.stop_motor()
        
        while (not self.motorStop) or (not GPIO.input(5)): #break the loop when motor stop signal is detected
            
            self.motorStop=self.stop_motor()

    
    def stop_motor(self):
        
        database = self.firebase.database() # get alarm on/off signal from firebase
        signals = database.child("signal")
        motorSignal = signals.child("motor").get().val()
        
        
        if (motorSignal=="off") or (not GPIO.input(13)):
            print("stopping motor...")
            self.EN1.ChangeDutyCycle(0)
            self.EN2.ChangeDutyCycle(0)
            print("motor stops")
            return True
        elif motorSignal=="on":
            
            self.EN1.ChangeDutyCycle(50)
            self.EN2.ChangeDutyCycle(50)

            GPIO.output(self.Motor1['input1'], GPIO.HIGH)
            GPIO.output(self.Motor1['input2'], GPIO.LOW)
                
            GPIO.output(self.Motor2['input1'], GPIO.HIGH)
            GPIO.output(self.Motor2['input2'], GPIO.LOW)
            
            print("motor is turned on")
            return False

    
    def start_alarm(self):
        
        self.alarmStop=self.stop_alarm()
        
        while (not self.alarmStop) or (not GPIO.input(16)): # if alarmStop is False or button is pressed
#                                                           # enter the loop
            self.alarmStop=self.stop_alarm()                # infinitely check if alarmStop True
            
                                                            # break the loop if alarm is turned off
    def stop_alarm(self):
        
        database = self.firebase.database() # get alarm on/off signal from firebase
        signals = database.child("signal")
        alarmSignal = signals.child("alarm").get().val()

        if alarmSignal=="off":
            print("Alarm turning off...")
            self.alarmStop=True
            GPIO.output(26,False)
            print("Alarm is off")
            return True
        elif alarmSignal=="on":
            GPIO.output(26,True)
            print("Alarm is turned on")
            return False

        
if __name__=="__main__":
        
    #print("Execute function...")
        
    
    motor1=Motor()
    
    while True: # turn on the system forever
        
        motor1.start_alarm() # alarm on/off test
        motor1.start_motor() # motor on/off test
