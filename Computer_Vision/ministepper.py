#!/usr/bin/env python3
"""
NEMA 8 Continuous Rotation
Runs motor continuously until you press Ctrl+C to stop

GPIO 23: DIR (direction)
GPIO 24: STEP (step pulses)
"""

import lgpio
import time

# GPIO pin configuration
STEP_PIN = 24
DIR_PIN = 23

class ContinuousStepperMotor:
    def __init__(self, step_pin=24, dir_pin=23, reverse=True):
        """
        Initialize stepper motor controller
        
        Args:
            step_pin: GPIO pin for STEP signal
            dir_pin: GPIO pin for DIR signal
            reverse: True to reverse direction, False for normal
        """
        self.STEP_PIN = step_pin
        self.DIR_PIN = dir_pin
        self.reverse = reverse
        
        # Open GPIO chip
        self.h = lgpio.gpiochip_open(4)
        
        # Setup pins as outputs
        lgpio.gpio_claim_output(self.h, self.STEP_PIN)
        lgpio.gpio_claim_output(self.h, self.DIR_PIN)
        
        # Initialize pins
        lgpio.gpio_write(self.h, self.STEP_PIN, 0)
        lgpio.gpio_write(self.h, self.DIR_PIN, 1 if reverse else 0)
        
        print(f"NEMA 8 Stepper Motor initialized")
        print(f"STEP: GPIO {self.STEP_PIN}")
        print(f"DIR: GPIO {self.DIR_PIN}")
        print(f"Direction: {'REVERSED' if reverse else 'NORMAL'}")
    
    def run_continuous(self, rpm=40):
        """
        Run motor continuously until interrupted
        
        Args:
            rpm: Speed in rotations per minute
        """
        # Calculate delay for desired RPM
        # Assuming 200 steps per revolution (adjust if using microstepping)
        steps_per_rev = 200
        delay = 60.0 / (rpm * steps_per_rev * 2)
        
        print(f"\nRunning continuously at {rpm} RPM")
        print("Press Ctrl+C to stop")
        print()
        
        step_count = 0
        
        try:
            while True:
                lgpio.gpio_write(self.h, self.STEP_PIN, 1)
                time.sleep(delay)
                lgpio.gpio_write(self.h, self.STEP_PIN, 0)
                time.sleep(delay)
                
                step_count += 1
                
                # Print status every 200 steps (1 revolution)
                if step_count % 200 == 0:
                    revolutions = step_count / 200
                    print(f"Completed {revolutions:.0f} revolutions ({step_count} steps)")
        
        except KeyboardInterrupt:
            print(f"\n\nStopped by user")
            print(f"Total: {step_count} steps ({step_count/200:.1f} revolutions)")
    
    def cleanup(self):
        """Clean up GPIO pins"""
        lgpio.gpiochip_close(self.h)
        print("GPIO cleanup complete")


def main():
    """Run motor continuously"""
    
    print("=" * 60)
    print("CONTINUOUS MOTOR ROTATION")
    print("=" * 60)
    print()
    
    # CONFIGURATION
    REVERSE = True  # Change to True to reverse direction
    RPM = 30         # Change this to adjust speed (5-60 typical range)
    
    print(f"Configuration:")
    print(f"  Direction: {'REVERSED' if REVERSE else 'NORMAL'}")
    print(f"  Speed: {RPM} RPM")
    print()
    print("To change direction or speed, edit REVERSE and RPM in the code")
    print()
    
    # Create motor instance
    motor = ContinuousStepperMotor(step_pin=24, dir_pin=23, reverse=REVERSE)
    
    try:
        # Run continuously
        motor.run_continuous(rpm=RPM)
    
    finally:
        motor.cleanup()
        print("Program finished")


if __name__ == "__main__":
    main()