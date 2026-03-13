from gpiozero import Servo
from time import sleep

servo = Servo(21)

def move_servo_degrees(angle):
    # Convert 0–180° range to -1.0–+1.0 range for gpiozero Servo
    duty = (angle / 90.0) - 1.0
    servo.value = duty
    sleep(0.5)
    servo.value = None  # stop PWM to reduce jitter

def intialize():
   # print("Initializing servo to 90° (neutral position)")
    move_servo_degrees(90)

def hold_card():
    #print("Holding card (moving to 45°)")
    move_servo_degrees(45)

def release_card():
    #print("Releasing card (moving back to 90°)")
    move_servo_degrees(45)
    move_servo_degrees(90)
