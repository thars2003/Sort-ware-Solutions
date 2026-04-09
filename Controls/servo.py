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
    try:
        lgpio.gpio_free(h, PIN)
    except:
        pass
    lgpio.gpio_claim_output(h, PIN)
    lgpio.tx_servo(h, PIN, pw, SERVO_FREQ)
    time.sleep(0.5)
    lgpio.gpio_free(h, PIN)

def cleanup(sig=None, frame=None):
    lgpio.gpiochip_close(h)
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def initialize():
    move_servo_degrees(97)

def hold_card():

    move_servo_degrees(80)

def release_card():
    move_servo_degrees(45)
    move_servo_degrees(97)