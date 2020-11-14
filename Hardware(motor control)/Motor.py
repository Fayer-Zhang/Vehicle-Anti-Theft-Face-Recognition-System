import RPi.GPIO as GPIO
from time import sleep

class Motor:
    
    print("Starting of the program")
    
    def __init__(self):
        
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
        
    
    def start_motor(self):
        
        while (not self.motorStop) or (not GPIO.input(5)): #break the loop when motor stop signal is detected
            
            print ("FORWARD MOTION")
            self.motorStop=self.stop_motor()
            
            self.EN1.ChangeDutyCycle(50)
            self.EN2.ChangeDutyCycle(50)

            GPIO.output(self.Motor1['input1'], GPIO.HIGH)
            GPIO.output(self.Motor1['input2'], GPIO.LOW)
                
            GPIO.output(self.Motor2['input1'], GPIO.HIGH)
            GPIO.output(self.Motor2['input2'], GPIO.LOW)

        GPIO.cleanup()
    
    def stop_motor(self):
        
        userStop=input("Stop the motor? choose between Y/N")
        
        if (userStop=="Y") or (not GPIO.input(13)):
            print("stopping motor...")
            self.EN1.ChangeDutyCycle(0)
            self.EN2.ChangeDutyCycle(0)
            print("motor stops")
            return True
        elif userStop=="N":
            return False
        else:
            self.stop_motor(self)
            
    
    def start_alarm(self):
        
        while (not self.alarmStop) or (not GPIO.input(16)):
            
            self.alarmStop=self.stop_alarm()
            GPIO.output(26,True)
        
        GPIO.cleanup()
    
    def stop_alarm(self):
        
        stopRequest=input("Turn off the alarm? choose between Y/N")
        if stopRequest=="Y":
            print("Alarm turning off...")
            GPIO.output(26,False)
            print("Alarm is off")
            return True
        elif stopRequest=="N":
            return False
        else:
            self.stop_alarm()
            
        
if __name__=="__main__":
        
    #print("Execute function...")
        
    
    motor1=Motor()
    #motor1.start_motor()
    motor1.start_alarm()
    
        
