import lgpio
import time
import signal
import sys

CHIP = 0
PIN = 12
SERVO_FREQ = 50

h = lgpio.gpiochip_open(CHIP)

def move_servo_degrees(angle):
    pw = int(500 + (angle / 180.0) * 2000)
    lgpio.gpio_claim_output(h, PIN)  # claim before each move
    lgpio.tx_servo(h, PIN, pw, SERVO_FREQ)
    time.sleep(0.5)
    lgpio.gpio_free(h, PIN)  # free after each move to stop PWM

def cleanup(sig=None, frame=None):
    lgpio.gpiochip_close(h)  # just close the chip, pin is already freed
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def initialize():
    move_servo_degrees(90)

def hold_card():
    move_servo_degrees(65)
    

def release_card():
    move_servo_degrees(50)
    move_servo_degrees(90)
   

# initialize()
# time.sleep(5)
# hold_card()
# time.sleep(5)
release_card()
time.sleep(5)
hold_card()
cleanup()