
import lgpio
import time
import atexit

NUM_BINS = 9
REV_PER_BIN = 1.0  # Revolutions per bin
current_bin = 1  # Track current bin

_motor_instance = None  # Singleton motor instance


class A4988StepperMotor:
    def __init__(self, step_pin=15, dir_pin=16, steps_per_rev=200):
        self.STEP_PIN = step_pin
        self.DIR_PIN = dir_pin
        self.steps_per_rev = steps_per_rev
        self.h = lgpio.gpiochip_open(4)
        lgpio.gpio_claim_output(self.h, self.STEP_PIN)
        lgpio.gpio_claim_output(self.h, self.DIR_PIN)
        lgpio.gpio_write(self.h, self.STEP_PIN, 0)
        lgpio.gpio_write(self.h, self.DIR_PIN, 0)

    def set_direction(self, clockwise=True):
        lgpio.gpio_write(self.h, self.DIR_PIN, 1 if clockwise else 0)
        time.sleep(0.01)  # Small delay for direction to settle
    
    def step(self, steps, delay=0.005, clockwise=True):
        self.set_direction(clockwise)
        
        for _ in range(steps):
            lgpio.gpio_write(self.h, self.STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(self.h, self.STEP_PIN, 0)
            time.sleep(delay)
    
    def rotate(self, revolutions, rpm=60, clockwise=True):
    
        steps = int(revolutions * self.steps_per_rev)
        delay = 60.0 / (rpm * self.steps_per_rev * 2)
        min_delay = 0.005  # 5 ms minimum
        if delay < min_delay:
            print(f"RPM too high for safe operation, using min_delay={min_delay}s")
            delay = min_delay

        print(f"Rotating {revolutions} revolutions at {rpm} RPM ({'CW' if clockwise else 'CCW'}), step delay: {delay:.4f}s")
        self.step(steps, delay, clockwise)

    def cleanup(self):
        lgpio.gpiochip_close(self.h)


_motor_instance = None

def _get_motor():
    global _motor_instance
    if _motor_instance is None:
        _motor_instance = A4988StepperMotor(step_pin=22, dir_pin=10)
    return _motor_instance

def move_bin(target_bin):
    motor = _get_motor()


def step_clockwise(motor):
    global current_bin
    motor.rotate(REV_PER_BIN, rpm=60, clockwise=True)
    current_bin += 1
    if current_bin > NUM_BINS:
        current_bin = 1


def step_counterclockwise(motor):
    global current_bin
    motor.rotate(REV_PER_BIN, rpm=60, clockwise=False)
    current_bin -= 1
    if current_bin < 1:
        current_bin = NUM_BINS


def move_bin(target_bin):
    """Move to a target bin. Motor is initialized automatically."""
    motor = _get_motor()
    global current_bin
    if target_bin == current_bin:
        return
    cw_steps = (target_bin - current_bin) % NUM_BINS
    ccw_steps = (current_bin - target_bin) % NUM_BINS
    if cw_steps <= ccw_steps:
        for _ in range(cw_steps):
            step_clockwise(motor)
    else:
        for _ in range(ccw_steps):
            step_counterclockwise(motor)

def dispense_card():
    motor = _get_motor()

    print("Dispensing card...")
    # push card fix rev and rpm
    motor.rotate(1.632, rpm=30, clockwise=False)
    # slight reverse to prevent double feed
    # motor.rotate(0.20, rpm=30, clockwise=True)


    time.sleep(0.3)

# Automatically cleanup motor on exit
atexit.register(lambda: _motor_instance.cleanup() if _motor_instance else None)

# dispense_card()
