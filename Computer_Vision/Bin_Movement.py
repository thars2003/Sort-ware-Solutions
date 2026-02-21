
# current_bin = 1
# NUM_BINS = 9

# def move_bin(target_bin):
#     global current_bin

#     if target_bin == current_bin:
#         print(f"Already at bin {target_bin}")
#         return

#     cw = (target_bin - current_bin) % NUM_BINS
#     ccw = (current_bin - target_bin) % NUM_BINS

#     if cw_steps <= ccw_steps:
#         print(f"Moving CW {cw_steps} step(s) to reach bin {target_bin}")
#         for _ in range(cw_steps):
#             step_clockwise(motor)
#     else:
#         print(f"Moving CCW {ccw_steps} step(s) to reach bin {target_bin}")
#         for _ in range(ccw_steps):
#             step_counterclockwise(motor)

#     current_bin = target_bin
#     print(f"Now at bin {current_bin}")

# def step_clockwise(motor):
#     global current_bin
#     print(f"Stepping CW from bin {current_bin}")
#     motor.rotate(revolutions=REV_PER_BIN, rpm=40, clockwise=True)
#     current_bin += 1
#     if current_bin > NUM_BINS:
#         current_bin = 1
#     print(f"Now at bin {current_bin}")

# def step_counterclockwise(motor):
#     global current_bin
#     print(f"Stepping CCW from bin {current_bin}")
#     motor.rotate(revolutions=REV_PER_BIN, rpm=40, clockwise=False)
#     current_bin -= 1
#     if current_bin < 1:
#         current_bin = NUM_BINS
#     print(f"Now at bin {current_bin}")

import lgpio
import time
import atexit

NUM_BINS = 9
REV_PER_BIN = 1  # Revolutions per bin
current_bin = 1  # Track current bin

_motor_instance = None  # Singleton motor instance


class A4988StepperMotor:
    def __init__(self, step_pin=22, dir_pin=10, steps_per_rev=200):
        self.STEP_PIN = step_pin
        self.DIR_PIN = dir_pin
        self.steps_per_rev = steps_per_rev
        self.h = lgpio.gpiochip_open(4)
        lgpio.gpio_claim_output(self.h, self.STEP_PIN)
        lgpio.gpio_claim_output(self.h, self.DIR_PIN)
        lgpio.gpio_write(self.h, self.STEP_PIN, 0)
        lgpio.gpio_write(self.h, self.DIR_PIN, 0)

    def set_direction(self, clockwise=True):
        """
        Set rotation direction
        
        Args:
            clockwise: True for clockwise, False for counter-clockwise
        """
        lgpio.gpio_write(self.h, self.DIR_PIN, 1 if clockwise else 0)
        time.sleep(0.001)  # Small delay for direction to settle
    
    def step(self, steps, delay=0.005, clockwise=True):
        """
        Move the motor a specific number of steps
        
        Args:
            steps: Number of steps to move
            delay: Delay between steps in seconds (controls speed)
            clockwise: Direction of rotation
        """
        self.set_direction(clockwise)
        
        for _ in range(steps):
            lgpio.gpio_write(self.h, self.STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(self.h, self.STEP_PIN, 0)
            time.sleep(delay)
    
    def rotate(self, revolutions, rpm=30, clockwise=True):
        """
        Rotate the motor by a number of revolutions at a given speed
        
        Args:
            revolutions: Number of full rotations
            rpm: Rotations per minute (speed)
            clockwise: Direction of rotation
        """
        steps = int(revolutions * self.steps_per_rev)
        
        # Safe delay per half-step
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
    motor.rotate(REV_PER_BIN, rpm=40, clockwise=True)
    current_bin += 1
    if current_bin > NUM_BINS:
        current_bin = 1


def step_counterclockwise(motor):
    global current_bin
    motor.rotate(REV_PER_BIN, rpm=40, clockwise=False)
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


# Automatically cleanup motor on exit
atexit.register(lambda: _motor_instance.cleanup() if _motor_instance else None)
# def move_bin1():
#     global current_bin
#     current_bin = 1
#     print("Moving to bin 1")

# def move_bin2():
#     global current_bin
#     current_bin = 2
#     print("Moving to bin 2")
#     return current_bin

# def move_bin3():
#     global current_bin
#     current_bin = 3
#     print("Moving to bin 3")

# def move_bin4():
#     global current_bin
#     current_bin = 4
#     print("Moving to bin 4")

# def move_bin5():
#     global current_bin
#     current_bin = 5
#     print("Moving to bin 5")

# def move_bin6():
#     global current_bin
#     current_bin = 6
#     print("Moving to bin 6")

# def move_bin7():
#     global current_bin
#     current_bin = 7
#     print("Moving to bin 7")

# def move_bin8():
#     global current_bin
#     current_bin = 8
#     print("Moving to bin 8")

# def move_bin9():
#     global current_bin
#     current_bin = 9
#     print("Moving to bin 9")