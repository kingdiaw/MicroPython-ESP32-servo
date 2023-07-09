#IMPORT RELATED LIBRARY
from machine import Pin, I2C
from button import PushButton
from servo import Servo
import time
import utime

#CONSTANT

#GLOBAL VAR
ledTick = 0
servoTick = 0
angleServo = 0
servoDir = 0
servoDirOld = 0
buttonTick = 0
buttonState = ""

#USER DEFINE CLASS

#USER DEFINE FUNCTION
start_time = time.ticks_ms()
def millis():
    return time.ticks_ms() - start_time

def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value

print('Version: Read Push Button and Blink LED independance')

#SETUP SECTION
led = Pin(2, Pin.OUT)
gButton = PushButton (5)
s1 = Servo(13)       # Servo pin is connected to GPIO13

#LOOP SECTION
while True:
    buttonState = gButton.read_button()
    
    if millis() >= ledTick:
        ledTick = millis()+1000
        led.value(not led.value())

    if buttonState == "FALLING":
        print("Button pressed")       
        timestamp = utime.time()
        time_tuple = utime.localtime(timestamp)
        time_string = "{}-{:02d}-{:02d} {}:{:02d}:{:02d}".format(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3],time_tuple[4],time_tuple[5])
        print(time_string)
    
    if millis() >= servoTick:
        servoTick = millis() + 50
        if servoDir == 0:	#Left
            angleServo = angleServo + 10
            if angleServo > 180:
                angleServo = 180
                servoDir = 1
        elif servoDir == 1:	#Right
            angleServo = angleServo - 10
            if angleServo < 0:
                angleServo = 0
                servoDir = 0
        if servoDirOld != servoDir:
            if servoDirOld == 0 and servoDir == 1:
                print ("Servo Turn Right")
            elif servoDirOld == 1 and servoDir == 0:
                print ("Servo Turn Left")
            servoDirOld = servoDir
        servo_Angle(angleServo)
     