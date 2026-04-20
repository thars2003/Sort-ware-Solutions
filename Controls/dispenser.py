import lgpio
import time
import atexit


NUM_BINS = 9
REV_PER_BIN = 1.0  # Revolutions per bin
step_count = 0  # Track total steps
calibrate=False

# Shared chip handle
_chip_handle = None


def _get_chip():
    global _chip_handle
    if _chip_handle is None:
        _chip_handle = lgpio.gpiochip_open(4)
    return _chip_handle
class A4988StepperMotor:
    def __init__(self, step_pin, dir_pin, enable_pin=None, steps_per_rev=200, chip_handle=None):
        self.STEP_PIN = step_pin
        self.DIR_PIN = dir_pin
        self.ENABLE_PIN = enable_pin
        self.steps_per_rev = steps_per_rev
        self.h = chip_handle if chip_handle is not None else lgpio.gpiochip_open(4)

        for pin in [self.STEP_PIN, self.DIR_PIN]:
            try:
                lgpio.gpio_free(self.h, pin)
            except lgpio.error:
                pass
            lgpio.gpio_claim_output(self.h, pin)
            lgpio.gpio_write(self.h, pin, 0)

        if self.ENABLE_PIN is not None:
            try:
                lgpio.gpio_free(self.h, self.ENABLE_PIN)
            except lgpio.error:
                pass
            lgpio.gpio_claim_output(self.h, self.ENABLE_PIN)
            lgpio.gpio_write(self.h, self.ENABLE_PIN, 1)  # Start disabled (high = off)

    def enable(self):
        if self.ENABLE_PIN is not None:
            lgpio.gpio_write(self.h, self.ENABLE_PIN, 0)  # Low = on add a rotational limit

    def disable(self):
        if self.ENABLE_PIN is not None:
            lgpio.gpio_write(self.h, self.ENABLE_PIN, 1)  # High = off

#

    def set_direction(self, clockwise=True):
        lgpio.gpio_write(self.h, self.DIR_PIN, 1 if clockwise else 0)
        time.sleep(0.01)

    def step(self, steps, delay=0.005, clockwise=True):
        self.set_direction(clockwise)
        for _ in range(steps):
            lgpio.gpio_write(self.h, self.STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(self.h, self.STEP_PIN, 0)
            time.sleep(delay)

    def rotate(self, revolutions, rpm, clockwise=True):
        steps = int(revolutions * self.steps_per_rev)
        delay = 60.0 / (rpm * self.steps_per_rev * 2)
        min_delay = 0.005
        if delay < min_delay:
            # print(f"RPM too high for safe operation, using min_delay={min_delay}s")
            delay = min_delay
        # print(f"Rotating {revolutions} revolutions at {rpm} RPM ({'CW' if clockwise else 'CCW'}), step delay: {delay:.4f}s")
        self.step(steps, delay, clockwise)

    def rotate_smooth(self, revolutions, min_rpm=10, max_rpm=60, clockwise=True):
        steps = int(revolutions * self.steps_per_rev)
        self.set_direction(clockwise)
        
        # Bell curve: ramp up for first 1/3, full speed for middle 1/3, ramp down for last 1/3
        ramp_steps = steps // 3
        
        for i in range(steps):
            # Calculate current rpm based on position in bell curve
            if i < ramp_steps:
                # Ramp up
                progress = i / ramp_steps
            elif i > steps - ramp_steps:
                # Ramp down
                progress = (steps - i) / ramp_steps
            else:
                # Full speed
                progress = 1.0

            current_rpm = min_rpm + (max_rpm - min_rpm) * progress
            delay = 60.0 / (current_rpm * self.steps_per_rev * 2)
            min_delay = 0.005
            if delay < min_delay:
                delay = min_delay

            lgpio.gpio_write(self.h, self.STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(self.h, self.STEP_PIN, 0)
            time.sleep(delay)

    def cleanup(self):
        pass  # Chip handle is shared, closed in _cleanup()


_bin_motor_instance = None      # Moves the bin carousel
_dispense_motor_instance = None  # Dispenses cards


def _get_bin_motor():
    global _bin_motor_instance
    print("_get_bin_motor called")
    if _bin_motor_instance is None:
        # print("Initializing bin motor...")
        _bin_motor_instance = A4988StepperMotor(step_pin=13, dir_pin=19, enable_pin=11, chip_handle=_get_chip())
        print("Bin motor initialized")
    return _bin_motor_instance


def _get_dispense_motor():
    global _dispense_motor_instance
    print("_get_dispense_motor called")
    if _dispense_motor_instance is None:
        # print("Initializing dispence motor...")
        _dispense_motor_instance = A4988StepperMotor(step_pin=22, dir_pin=10, enable_pin=27, chip_handle=_get_chip())
        print("dispense motor initialized")
    return _dispense_motor_instance
    

def _apply_step(clockwise):
    global step_count, current_bin
    motor = _get_bin_motor()
    motor.enable()

    if clockwise:
        # motor.rotate_smooth(REV_PER_BIN, min_rpm=10, max_rpm=60, clockwise=True)
        motor.rotate(REV_PER_BIN,60, clockwise=True)
        current_bin = (current_bin % NUM_BINS) + 1
        step_count += 1
    else:
        # motor.rotate_smooth(REV_PER_BIN, min_rpm=10, max_rpm=60, clockwise=False)
        motor.rotate(REV_PER_BIN,60, clockwise=False)
        current_bin -= 1
        if current_bin < 1:
            current_bin = NUM_BINS
        step_count -= 1

    # Hit +18 — wound clockwise too far, unwind counterclockwise
    if step_count >= 18:
        # print("Rotational limit reached (+18), unwinding CCW...")
        for _ in range(18):
            # motor.rotate_smooth(REV_PER_BIN, min_rpm=10, max_rpm=60, clockwise=False)
            motor.rotate(REV_PER_BIN,60, clockwise=False)
        step_count = 0

    # Hit -18 — wound counterclockwise too far, unwind clockwise
    elif step_count <= -18:
        # print("Rotational limit reached (-18), unwinding CW...")
        for _ in range(18):
            # motor.rotate_smooth(REV_PER_BIN, min_rpm=10, max_rpm=60, clockwise=True)
            motor.rotate(REV_PER_BIN,60, clockwise=True)
        step_count = 0

    motor.disable()
def step_clockwise(motor,calibrate):
    global current_bin
    _apply_step(clockwise=True)
    # motor.rotate_smooth(REV_PER_BIN, min_rpm=10, max_rpm=60, clockwise=False)
    motor.rotate(REV_PER_BIN,60, clockwise=False)
    if calibrate:
        current_bin=1
        calibrate=False
   
def step_counterclockwise(motor,calibrate):
    global current_bin
    _apply_step(clockwise=False)
    # motor.rotate_smooth(REV_PER_BIN, min_rpm=10, max_rpm=60, clockwise=True)
    motor.rotate(REV_PER_BIN,60, clockwise=True)
    if calibrate:
        current_bin=1
        calibrate=False


current_bin = 1 

def move_bin(target_bin):
    global calibrate
    motor = _get_bin_motor()
    global current_bin
    _get_bin_motor().enable()
    print(f"current:{current_bin}target_bin:{target_bin}")

    if target_bin == current_bin:
        return

    cw_steps = (target_bin - current_bin) % NUM_BINS
    ccw_steps = (current_bin - target_bin) % NUM_BINS

    if cw_steps <= ccw_steps:
        for _ in range(cw_steps):
            step_clockwise(motor,calibrate)
    else:
        for _ in range(ccw_steps):
            step_counterclockwise(motor,calibrate)
    _get_bin_motor().disable()

def dispense_card():
    motor = _get_dispense_motor()
    motor.enable()
    # print(f"Dispense motor STEP_PIN={motor.STEP_PIN}, DIR_PIN={motor.DIR_PIN}, handle={motor.h}")
    print("Dispensing card...")
    #motor.rotate(1.845, rpm=30, clockwise=False) #1.632 Tharshini
    motor.rotate(1.845, rpm=60, clockwise=False) #Louis Test
    time.sleep(1)
    # motor = _get_dispense_motor()
    # print("Dispensing card...")
    motor.rotate(0.5, rpm=30, clockwise=True)
    # time.sleep(0.3)
    motor.disable()

def _cleanup():
    global _chip_handle
    if _chip_handle is not None:
        lgpio.gpiochip_close(_chip_handle)
        _chip_handle = None


atexit.register(_cleanup)