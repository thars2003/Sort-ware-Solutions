#!/usr/bin/env python3
"""
Vref Adjustment WITHOUT Multimeter - Interactive Guide
Helps you tune the current limit by testing motor performance
"""

import lgpio
import time

STEP_PIN = 22
DIR_PIN = 10

def vref_tuning_guide():
    """Interactive guide for adjusting Vref without a multimeter"""
    
    print("=" * 60)
    print("A4988 CURRENT LIMIT ADJUSTMENT (No Multimeter)")
    print("=" * 60)
    print()
    print("Since you don't have a multimeter, we'll tune by ear/feel.")
    print()
    print("GOAL: Find the sweet spot where motor runs smoothly")
    print("  - Too LOW:  Motor buzzes but doesn't turn")
    print("  - Too HIGH: Driver gets very hot")
    print("  - JUST RIGHT: Motor turns smoothly, driver warm but not hot")
    print()
    print("=" * 60)
    print("PREPARATION")
    print("=" * 60)
    print()
    print("1. Locate the small potentiometer screw on the A4988")
    print("2. Get a small flathead screwdriver")
    print("3. Power everything up (12V connected)")
    print()
    print("STARTING POSITION:")
    print("  Turn potentiometer COUNTER-CLOCKWISE all the way")
    print("  (gently - don't force it)")
    print("  Then turn CLOCKWISE about 1/4 turn")
    print("  This is your safe starting point (probably too low)")
    print()
    
    input("Have you set the starting position? Press Enter to continue...")
    
    h = lgpio.gpiochip_open(4)
    lgpio.gpio_claim_output(h, STEP_PIN)
    lgpio.gpio_claim_output(h, DIR_PIN)
    lgpio.gpio_write(h, STEP_PIN, 0)
    lgpio.gpio_write(h, DIR_PIN, 0)
    
    delay = 0.0075
    iteration = 1
    
    print()
    print("=" * 60)
    print("TUNING PROCESS")
    print("=" * 60)
    
    while True:
        print(f"\n--- ITERATION {iteration} ---")
        print("This will run 1 full rotation (200 steps)")
        print()
        
        response = input("Ready to test? (Enter = test, 'q' = quit): ")
        if response.lower() == 'q':
            break
        
        # Run test rotation
        print("Testing motor... ", end="", flush=True)
        
        failed = False
        for i in range(400):
            lgpio.gpio_write(h, STEP_PIN, 1)
            time.sleep(delay)
            lgpio.gpio_write(h, STEP_PIN, 0)
            time.sleep(delay)
        
        print("Complete!")
        print()
        
        # Get feedback
        print("What happened?")
        print("  1 - Motor BUZZED but didn't turn (or barely moved)")
        print("  2 - Motor turned but SKIPPED some steps")
        print("  3 - Motor turned SMOOTHLY - perfect!")
        print("  4 - Motor turned but driver is getting HOT")
        print()
        
        result = input("Enter 1-4: ").strip()
        
        if result == "1":
            print("\n→ Current too LOW")
            print("  ACTION: Turn potentiometer CLOCKWISE 1/8 turn")
            print("  This increases current to the motor")
            input("  Press Enter after adjusting...")
            
        elif result == "2":
            print("\n→ Current still a bit too LOW")
            print("  ACTION: Turn potentiometer CLOCKWISE 1/16 turn")
            print("  Small adjustment")
            input("  Press Enter after adjusting...")
            
        elif result == "3":
            print("\n✓ PERFECT! You've found the sweet spot!")
            print()
            print("OPTIONAL: Touch the A4988 chip")
            hot = input("Is it too hot to touch comfortably? (y/n): ")
            
            if hot.lower() == 'y':
                print("→ Slightly too high, turn COUNTER-CLOCKWISE 1/16 turn")
                input("  Press Enter after adjusting...")
            else:
                print("\n" + "=" * 60)
                print("SUCCESS! Vref is properly set!")
                print("=" * 60)
                print()
                print("MARK THIS POSITION:")
                print("  - Put a piece of tape next to the potentiometer")
                print("  - Draw a line on the screw with marker")
                print("  - Take a photo for reference")
                print()
                print("Your motor should now work reliably!")
                print("=" * 60)
                break
                
        elif result == "4":
            print("\n→ Current too HIGH")
            print("  ACTION: Turn potentiometer COUNTER-CLOCKWISE 1/8 turn")
            print("  This reduces current and heat")
            input("  Press Enter after adjusting...")
            
        else:
            print("Invalid input, try again")
            continue
        
        iteration += 1
    
    lgpio.gpiochip_close(h)
    print("\nTuning session complete!")

def quick_reference():
    """Print quick reference card"""
    print()
    print("=" * 60)
    print("QUICK REFERENCE - Vref Tuning Without Multimeter")
    print("=" * 60)
    print()
    print("SYMPTOMS & FIXES:")
    print()
    print("Motor buzzes, doesn't turn:")
    print("  → Turn CLOCKWISE (increase current)")
    print()
    print("Motor turns but skips steps:")
    print("  → Turn CLOCKWISE slightly (increase current)")
    print()
    print("Driver gets very hot:")
    print("  → Turn COUNTER-CLOCKWISE (decrease current)")
    print()
    print("Motor runs perfectly:")
    print("  → You're done! Mark the position!")
    print()
    print("ADJUSTMENT SIZES:")
    print("  First try:     1/4 turn clockwise from minimum")
    print("  Big change:    1/8 turn")
    print("  Fine tuning:   1/16 turn")
    print()
    print("SAFETY:")
    print("  - Driver getting warm is NORMAL")
    print("  - Driver too hot to touch = TOO HIGH")
    print("  - Start low, increase gradually")
    print("  - If unsure, turn it down")
    print("=" * 60)

if __name__ == "__main__":
    print()
    print("Choose an option:")
    print("  1 - Interactive tuning guide")
    print("  2 - Quick reference only")
    print()
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        vref_tuning_guide()
    elif choice == "2":
        quick_reference()
    else:
        print("Invalid choice")
