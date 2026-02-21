#!/usr/bin/env python3
"""
A4988 Stepper Motor Driver Controller for Raspberry Pi 5
Controls a NEMA 17 stepper motor using GPIO pins

IMPORTANT: If motor buzzes but doesn't rotate:
1. Adjust the A4988 current limit potentiometer (small screw on driver)
2. Formula: Vref = Current_Limit / 2.5 (for most A4988 boards)
3. For NEMA 17 (typically 1.5A): Vref should be around 0.6V
4. Measure Vref with multimeter between potentiometer and GND
5. Turn potentiometer CLOCKWISE to increase current
6. Start low and increase gradually until motor runs smoothly

GPIO Pin Configuration:
- GPIO 22: STEP (controls motor steps)
- GPIO 10: DIR (controls direction)
- ENABLE: Hardwired to GND (always enabled - no GPIO needed)

Wiring Guide:
A4988 Pin -> Connection
--------------------------
STEP      -> GPIO 22
DIR       -> GPIO 10
ENABLE    -> GND (hardwired, always enabled)
MS1       -> GND (for full step mode)
MS2       -> GND (for full step mode)
MS3       -> GND (for full step mode)
RESET     -> SLEEP (connect together)
VDD       -> 3.3V or 5V (logic power)
VMOT      -> 12V (motor power supply)
GND       -> Common ground
1A, 1B    -> Motor coil A
2A, 2B    -> Motor coil B
"""

import lgpio
import time

class A4988StepperMotor:
    def __init__(self, step_pin=22, dir_pin=10, steps_per_rev=200):
        """
        Initialize the A4988 stepper motor controller
        
        Args:
            step_pin: GPIO pin for STEP signal
            dir_pin: GPIO pin for DIR (direction) signal
            steps_per_rev: Steps per revolution (200 for NEMA 17 in full step mode)
        
        Note: ENABLE pin should be hardwired to GND (always enabled)
        """
        self.STEP_PIN = step_pin
        self.DIR_PIN = dir_pin
        self.steps_per_rev = steps_per_rev
        
        # Open GPIO chip
        self.h = lgpio.gpiochip_open(4)  # Pi 5 uses gpiochip4
        
        # Setup pins as outputs
        lgpio.gpio_claim_output(self.h, self.STEP_PIN)
        lgpio.gpio_claim_output(self.h, self.DIR_PIN)
        
        # Initialize pins
        lgpio.gpio_write(self.h, self.STEP_PIN, 0)
        lgpio.gpio_write(self.h, self.DIR_PIN, 0)
        
        print(f"A4988 Stepper Motor initialized")
        print(f"STEP: GPIO {self.STEP_PIN}")
        print(f"DIR: GPIO {self.DIR_PIN}")
        print(f"ENABLE: Hardwired to GND (always enabled)")
    
    def set_direction(self, clockwise=True):
        """
        Set rotation direction
        
        Args:
            clockwise: True for clockwise, False for counter-clockwise
        """
        lgpio.gpio_write(self.h, self.DIR_PIN, 1 if clockwise else 0)
        time.sleep(0.001)  # Small delay for direction to settle
    
    def step(self, steps, delay=0.0075, clockwise=True):
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
    
    def rotate(self, revolutions, rpm=20, clockwise=True):
        """
        Rotate the motor by a number of revolutions at a given speed
        
        Args:
            revolutions: Number of full rotations
            rpm: Rotations per minute (speed)
            clockwise: Direction of rotation
        """
        steps = int(revolutions * self.steps_per_rev)
        
        # Calculate delay based on RPM
        # delay = (60 / (rpm * steps_per_rev * 2))
        # The *2 is because we have two delays per step (HIGH and LOW)
        delay = 60.0 / (rpm * self.steps_per_rev * 2)
        
        print(f"Rotating {revolutions} revolutions at {rpm} RPM ({'CW' if clockwise else 'CCW'})")
        self.step(steps, delay, clockwise)
    
    def rotate_degrees(self, degrees, rpm=20, clockwise=True):
        """
        Rotate the motor by a specific number of degrees
        
        Args:
            degrees: Degrees to rotate
            rpm: Rotations per minute (speed)
            clockwise: Direction of rotation
        """
        steps = int((degrees / 360.0) * self.steps_per_rev)
        delay = 60.0 / (rpm * self.steps_per_rev * 2)
        
        print(f"Rotating {degrees} degrees at {rpm} RPM ({'CW' if clockwise else 'CCW'})")
        self.step(steps, delay, clockwise)
    
    def cleanup(self):
        """Clean up GPIO pins"""
        lgpio.gpiochip_close(self.h)
        print("GPIO cleanup complete")
        print("Note: Motor remains enabled (ENABLE hardwired to GND)")


def main():
    """Example usage of the stepper motor controller"""
    
    # Create motor instance
    motor = A4988StepperMotor(step_pin=22, dir_pin=10)
    
    print("\nNote: Motor is always enabled (ENABLE pin hardwired to GND)")
    print("Starting tests in 2 seconds...")
    time.sleep(2)
    
    try:
        
        # Example 1: Rotate 1 full revolution clockwise at 20 RPM
        print("\n--- Example 1: 1 revolution CW at 20 RPM ---")
        motor.rotate(revolutions=1, rpm=20, clockwise=True)
        time.sleep(1)
        
        # Example 2: Rotate 1 full revolution counter-clockwise at 20 RPM
        print("\n--- Example 2: 1 revolution CCW at 20 RPM ---")
        motor.rotate(revolutions=1, rpm=20, clockwise=False)
        time.sleep(1)
        
        # Example 3: Rotate 90 degrees clockwise
        print("\n--- Example 3: 90 degrees CW at 20 RPM ---")
        motor.rotate_degrees(degrees=90, rpm=20, clockwise=True)
        time.sleep(1)
        
        # Example 4: Move 200 steps (1 revolution) with custom speed
        print("\n--- Example 4: 200 steps with 0.0075s delay ---")
        motor.step(steps=200, delay=0.0075, clockwise=True)
        time.sleep(1)
        
        # Example 5: Slower, reliable rotation - 1 revolution at 20 RPM
        print("\n--- Example 5: 1 revolution at 20 RPM ---")
        motor.rotate(revolutions=1, rpm=20, clockwise=True)
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    
    finally:
        # Always cleanup
        motor.cleanup()
        print("Program finished")


if __name__ == "__main__":
    main()