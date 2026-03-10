from gpiozero import AngularServo
import sys

# Setup - Adjust min_pulse_width/max_pulse_width if your servo jitters
servo = AngularServo(18, min_angle=0, max_angle=180, 
                    min_pulse_width=0.0005, max_pulse_width=0.0025)

print("--- Servo Manual Control ---")
print("Type 'u' and Enter to go to 20°")
print("Type 'd' and Enter to go to 0°")
print("Type 'exit' to quit")
print("----------------------------")

try:
    while True:
        # Wait for user to type something
        command = input("Enter command (l/m): ").lower().strip()

		
        if command == 'l':
            print("Dispense Position")
            servo.angle = 90
            
        
        elif command == 'm':
            print("Scanning Position")
            servo.angle = 0
            
        elif command == 'exit':
            print("Exiting...")
            break
            
        else:
            print("Unknown command! Use 'u', 'd', or 'exit'.")

except KeyboardInterrupt:
    pass

finally:
    servo.detach()
    print("\nServo detached. Goodbye!")
