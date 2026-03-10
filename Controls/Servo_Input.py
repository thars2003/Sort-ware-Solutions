from gpiozero import AngularServo
from time import sleep

# Setup the servo globally to avoid "re-exporting" the pin every time
# Adjust pulse widths if your servo doesn't hit the full 180 range
servo = AngularServo(18, min_angle=0, max_angle=180, 
                     min_pulse_width=0.0005, max_pulse_width=0.0025)

def move_and_detach(angle):
    try:
        print(f"Moving to {angle}°...")
        servo.angle = angle
        sleep(0.5)  # Enough time for the physical arm to move
        servo.detach()
        print("Servo detached (idle).")
    except ValueError:
        print("Error: Please enter a value between 0 and 180.")

if __name__ == "__main__":
    print("--- Servo Controller ---")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("Enter angle (0-180): ").strip().lower()
        
        if user_input == 'exit':
            break
            
        try:
            print(f"90 is down and 70 is up")
            angle_val = float(user_input)
            move_and_detach(angle_val)
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("Program exited.")
