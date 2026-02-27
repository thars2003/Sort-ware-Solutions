
#!/usr/bin/env python3
"""
Servo Testing Code
#Pin 18 - Data Pin Orange
#5V - Red Wire
#GND - Brown Wire

"""

from gpiozero import AngularServo
from time import sleep

# Define the servo on Pin 18
# min_pulse_width and max_pulse_width are usually 0.5ms and 2.5ms
# expressed in seconds (0.0005 and 0.0025)
servo = AngularServo(18,
					min_angle= 0, 
                    max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025)

try:
    while True: 
        print("Moving to 0 degrees")
        servo.angle = 0
        sleep(2)

        print("Moving to 90 degrees")
        servo.angle = 90
        sleep(2)

        print("Moving to 179 degrees")
        servo.angle = 179
        sleep(2)

except KeyboardInterrupt:
    # This cleanly stops the PWM signal
    servo.detach()
    print("Stopped.")
