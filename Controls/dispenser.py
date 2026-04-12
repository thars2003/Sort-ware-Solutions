import lgpio
import time
import atexit

NUM_BINS = 9
REV_PER_BIN = 1.0  # Revolutions per bin
current_bin = 1  # Track current bin
step_count = 0  # Track total steps

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
            lgpio.gpio_write(self.h, self.ENABLE_PIN, 0)  # Low = on

    def disable(self):
        if self.ENABLE_PIN is not None:
            lgpio.gpio_write(self.h, self.ENABLE_PIN, 1)  # High = off

# class A4988StepperMotor:
#     def __init__(self, step_pin, dir_pin, steps_per_rev=200, chip_handle=None):
#         self.STEP_PIN = step_pin
#         self.DIR_PIN = dir_pin
#         self.steps_per_rev = steps_per_rev
#         self.h = chip_handle if chip_handle is not None else lgpio.gpiochip_open(4)
#         try:
#             lgpio.gpio_free(self.h, self.STEP_PIN)
#         except lgpio.error:
#             pass

#         try:
#             lgpio.gpio_free(self.h, self.DIR_PIN)
#         except lgpio.error:
#             pass
#         lgpio.gpio_claim_output(self.h, self.STEP_PIN)
#         lgpio.gpio_claim_output(self.h, self.DIR_PIN)
#         lgpio.gpio_write(self.h, self.STEP_PIN, 0)
#         lgpio.gpio_write(self.h, self.DIR_PIN, 0)

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

    def rotate(self, revolutions, rpm=60, clockwise=True):
        steps = int(revolutions * self.steps_per_rev)
        delay = 60.0 / (rpm * self.steps_per_rev * 2)
        min_delay = 0.005
        if delay < min_delay:
            print(f"RPM too high for safe operation, using min_delay={min_delay}s")
            delay = min_delay
        print(f"Rotating {revolutions} revolutions at {rpm} RPM ({'CW' if clockwise else 'CCW'}), step delay: {delay:.4f}s")
        self.step(steps, delay, clockwise)

    def cleanup(self):
        pass  # Chip handle is shared, closed in _cleanup()


_bin_motor_instance = None      # Moves the bin carousel
_dispense_motor_instance = None  # Dispenses cards


def _get_bin_motor():
    global _bin_motor_instance
    print("_get_bin_motor called")
    if _bin_motor_instance is None:
        print("Initializing bin motor...")
        _bin_motor_instance = A4988StepperMotor(step_pin=13, dir_pin=19, enable_pin=11, chip_handle=_get_chip())
        print("Bin motor initialized")
    return _bin_motor_instance


def _get_dispense_motor():
    global _dispense_motor_instance
    print("_get_dispense_motor called")
    if _dispense_motor_instance is None:
        print("Initializing dispence motor...")
        _dispense_motor_instance = A4988StepperMotor(step_pin=22, dir_pin=10, enable_pin=27, chip_handle=_get_chip())
        print("dispense motor initialized")
    return _dispense_motor_instance
    


# def step_clockwise(motor):
#     global current_bin, step_count
#     motor.rotate(REV_PER_BIN, rpm=60, clockwise=True)
#     current_bin += 1
#     step_count += 1
#     if current_bin > NUM_BINS:
#         current_bin = 1


# def step_counterclockwise(motor):
#     global current_bin, step_count
#     motor.rotate(REV_PER_BIN, rpm=60, clockwise=False)
#     current_bin -= 1
#     step_count-=1
#     if current_bin < 1:
#         current_bin = NUM_BINS

def _apply_step(clockwise):
    global step_count, current_bin
    motor = _get_bin_motor()

    if clockwise:
        motor.rotate(REV_PER_BIN, rpm=60, clockwise=True)
        current_bin = (current_bin % NUM_BINS) + 1
        step_count += 1
    else:
        motor.rotate(REV_PER_BIN, rpm=60, clockwise=False)
        current_bin -= 1
        if current_bin < 1:
            current_bin = NUM_BINS
        step_count -= 1

    # Hit +18 — wound clockwise too far, unwind counterclockwise
    if step_count >= 18:
        print("Rotational limit reached (+18), unwinding CCW...")
        for _ in range(18):
            motor.rotate(REV_PER_BIN, rpm=60, clockwise=False)
        step_count = 0

    # Hit -18 — wound counterclockwise too far, unwind clockwise
    elif step_count <= -18:
        print("Rotational limit reached (-18), unwinding CW...")
        for _ in range(18):
            motor.rotate(REV_PER_BIN, rpm=60, clockwise=True)
        step_count = 0


def step_clockwise(motor):
    _apply_step(clockwise=True)


def step_counterclockwise(motor):
    _apply_step(clockwise=False)


def move_bin(target_bin):
    motor = _get_bin_motor()
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
    motor = _get_dispense_motor()
    print(f"Dispense motor STEP_PIN={motor.STEP_PIN}, DIR_PIN={motor.DIR_PIN}, handle={motor.h}")
    print("Dispensing card...")
    motor.rotate(1.845, rpm=30, clockwise=False) #1.632
    time.sleep(1)
    # motor = _get_dispense_motor()
    # print("Dispensing card...")
    motor.rotate(0.4, rpm=30, clockwise=True)
    # time.sleep(0.3)


def _cleanup():
    global _chip_handle
    if _chip_handle is not None:
        lgpio.gpiochip_close(_chip_handle)
        _chip_handle = None


atexit.register(_cleanup)