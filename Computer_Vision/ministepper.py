#!/usr/bin/env python3
"""
Simple NEMA 8 Motor Control - One Direction Only
GPIO 23: DIR (direction)
GPIO 24: STEP (step pulses)
"""

import lgpio
import time

# GPIO pin configuration
STEP_PIN = 24
DIR_PIN = 23

class SimpleStepperMotor:
    def __init__(self, step_pin=24, dir_pin=23, steps_per_rev=200, microstep_mode=1, reverse=False):
        """
        Initialize stepper motor controller
        
        Args:
            step_pin: GPIO pin for STEP signal
            dir_pin: GPIO pin for DIR signal
            steps_per_rev: Base steps per revolution (200 for most steppers)
            microstep_mode: 1, 2, 4, 8, or 16 depending on MS pin configuration
            reverse: True to reverse direction, False for normal
        """
        self.STEP_PIN = step_pin
        self.DIR_PIN = dir_pin
        self.steps_per_rev = steps_per_rev * microstep_mode
        self.reverse = reverse
        
        # Open GPIO chip
        self.h = lgpio.gpiochip_open(4)
        
        # Setup pins as outputs
        lgpio.gpio_claim_output(self.h, self.STEP_PIN)
        lgpio.gpio_claim_output(self.h, self.DIR_PIN)
        
        # Initialize pins
        lgpio.gpio_write(self.h, self.STEP_PIN, 0)
        # Set direction based on reverse flag
        lgpio.gpio_write(self.h, self.DIR_PIN, 1 if reverse else 0)
        
        print(f"NEMA 8 Stepper Motor initialized")
        print(f"STEP: GPIO {self.STEP_PIN}")
        print(f"DIR: GPIO {self.DIR_PIN}")
        print(f"Direction: {'REVERSED' if reverse else 'NORMAL'}")
        print(f"Steps per revolution: {self.steps_per_rev}")
    
    def rotate(self, revolutions=1, rpm=20):
        """
        Rotate the motor
        
        Args:
            revolutions: Number of full rotations
            rpm: Speed in rotations per minute
        """
        steps = int(revolutions * self.steps_per_rev)
        delay = 60.0 / (rpm * self.steps_per_rev * 2)
        
        print(f"Rotating {revolutions} revolutions at {rpm} RPM...")
        
        for i in range(steps):
            lgpio.gpio_write(self.h, self.STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(self.h, self.STEP_PIN, 0)
            time.sleep(delay)
            
            if (i + 1) % 100 == 0:
                print(f"  {i+1}/{steps} steps")
        
        print("✓ Complete!")
    
    def rotate_degrees(self, degrees, rpm=20):
        """
        Rotate by specific degrees
        
        Args:
            degrees: Degrees to rotate
            rpm: Speed in rotations per minute
        """
        steps = int((degrees / 360.0) * self.steps_per_rev)
        delay = 60.0 / (rpm * self.steps_per_rev * 2)
        
        print(f"Rotating {degrees} degrees at {rpm} RPM...")
        
        for i in range(steps):
            lgpio.gpio_write(self.h, self.STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(self.h, self.STEP_PIN, 0)
            time.sleep(delay)
        
        print("✓ Complete!")
    
    def step(self, steps, delay=0.0075):
        """
        Move a specific number of steps
        
        Args:
            steps: Number of steps to move
            delay: Delay between steps in seconds
        """
        print(f"Moving {steps} steps...")
        
        for i in range(steps):
            lgpio.gpio_write(self.h, self.STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(self.h, self.STEP_PIN, 0)
            time.sleep(delay)
        
        print("✓ Complete!")
    
    def cleanup(self):
        """Clean up GPIO pins"""
        lgpio.gpiochip_close(self.h)
        print("GPIO cleanup complete")


def main():
    """Example usage"""
    
    # Create motor instance
    # If using microstepping (MS pins to VDD), change microstep_mode
    # microstep_mode=1  for full step (MS pins to GND)
    # microstep_mode=16 for 1/16 step (MS pins to VDD)
    
    # To reverse direction, set reverse=True
    motor = SimpleStepperMotor(step_pin=24, dir_pin=23, microstep_mode=1, reverse=False)
    
    print("\nStarting motor tests...")
    print("If motor goes the wrong way, change reverse=False to reverse=True above")
    time.sleep(1)
    
    try:
        # Example 1: Rotate 1 full revolution at 20 RPM
        print("\n--- Example 1: 1 revolution at 20 RPM ---")
        motor.rotate(revolutions=1, rpm=20)
        time.sleep(1)
        
        # Example 2: Rotate 2 revolutions at 30 RPM
        print("\n--- Example 2: 2 revolutions at 30 RPM ---")
        motor.rotate(revolutions=2, rpm=30)
        time.sleep(1)
        
        # Example 3: Rotate 90 degrees
        print("\n--- Example 3: 90 degrees ---")
        motor.rotate_degrees(degrees=90, rpm=20)
        time.sleep(1)
        
        # Example 4: Move 200 steps
        print("\n--- Example 4: 200 steps ---")
        motor.step(steps=200, delay=0.0075)
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    
    finally:
        motor.cleanup()
        print("Program finished")


if __name__ == "__main__":
    main()