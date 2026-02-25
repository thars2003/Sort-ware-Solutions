
#!/usr/bin/env python3
"""
Servo Testing Code
#Pin 18 - Data

"""

from gpiozero import AngularServo
from time import sleep

# Define the servo on Pin 18
# min_pulse_width and max_pulse_width are usually 0.5ms and 2.5ms
# expressed in seconds (0.0005 and 0.0025)
servo = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)

try:
    while True:
        print("Moving to 0 degrees")
        servo.angle = 0
        sleep(2)

        print("Moving to 90 degrees")
        servo.angle = 90
        sleep(2)

        print("Moving to 180 degrees")
        servo.angle = 180
        sleep(2)

except KeyboardInterrupt:
    # This cleanly stops the PWM signal
    servo.detach()
    print("Stopped.")
