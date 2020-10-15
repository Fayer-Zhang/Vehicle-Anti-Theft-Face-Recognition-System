# import the RPi library
import RPi.GPIO as GPIO
import time

# initialize the ports
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# preset the port for button and alarm
GPIO.setup(5,GPIO.IN)     # button 1
GPIO.setup(6,GPIO.IN)     # button 2
GPIO.setup(13,GPIO.IN)    # button 3
GPIO.setup(16,GPIO.IN)    # button 4
GPIO.setup(26,GPIO.OUT)   # alarm

# preset the port for the L293D
Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}
Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}
for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)
EN1 = GPIO.PWM(Motor1['EN'],100)
EN2 = GPIO.PWM(Motor2['EN'],100)
EN1.start(0)
EN2.start(0)

while True:
    if not GPIO.input(5):
        # If press button 1, two DC motors running full speed forward
        EN1.ChangeDutyCycle(100)
        EN2.ChangeDutyCycle(100)
        print ("FORWARD MOTION")
        GPIO.output(Motor1['input1'],GPIO.HIGH)
        GPIO.output(Motor1['input2'],GPIO.LOW)
        GPIO.output(Motor2['input2'],GPIO.HIGH)
        GPIO.output(Motor2['input1'],GPIO.LOW)
    elif not GPIO.input(6):
        # If press button 2, two DC motors running full speed backword
        EN1.ChangeDutyCycle(100)
        EN2.ChangeDutyCycle(100)
        print ("BACKWORD MOTION")
        GPIO.output(Motor1['input1'],GPIO.LOW)
        GPIO.output(Motor1['input2'],GPIO.HIGH)
        GPIO.output(Motor2['input2'],GPIO.LOW)
        GPIO.output(Motor2['input1'],GPIO.HIGH)
    elif not GPIO.input(13):
        # If press button 3, two DC motors stop running
        print ("STOP")
        EN1.ChangeDutyCycle(0)
        EN2.ChangeDutyCycle(0)
    elif not GPIO.input(16):
        # If press button 4, alarm starts beeping
        print ("ALARM")
        GPIO.output(26,True)
    else:
        # If no button been pressed, alarm stop beeping
        GPIO.output(26,False)