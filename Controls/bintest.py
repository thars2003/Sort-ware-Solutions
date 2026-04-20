import dispenser
import time

# dispenser._get_bin_motor().enable()
dispenser._get_bin_motor().enable()
dispenser._get_dispense_motor().enable()

dispenser.dispense_card()
dispenser.dispense_card()
# dispenser.dispense_card()
# dispenser.dispense_card()
# dispenser.dispense_card()
# dispenser.dispense_card()
# dispenser.dispense_card()

# dispenser.step_clockwise(dispenser._get_bin_motor(), calibrate=True)


dispenser._get_dispense_motor().disable()
dispenser._get_bin_motor().disable()


# dispenser.move_bin(9)

# dispenser.move_bin(4)
# time.sleep(5)
# time.sleep(5)
# dispenser.move_bin(2)
# time.sleep(5)
# dispenser.move_bin(9)
# time.sleep(5)

# dispenser.move_bin(2)

def boot_buzzer():
    import lgpio
    import time

    BUZZER_PIN = 20
    # Ensure melody and durations are accessible (passed in or defined)
    melody = [523, 659, 784, 1047]  # C5, E5, G5, C6
    durations = [0.1, 0.1, 0.1, 0.3]

    h_buzz = lgpio.gpiochip_open(0)
    
    try:
        lgpio.gpio_claim_output(h_buzz, BUZZER_PIN)

        for freq, dur in zip(melody, durations):
            # Start the tone
            lgpio.tx_pwm(h_buzz, BUZZER_PIN, freq, 50)
            time.sleep(dur)
            
            # Silence the buzzer by forcing the pin LOW 
            # This is cleaner than duty 0 for preventing screeching
            lgpio.tx_pwm(h_buzz, BUZZER_PIN, freq, 0) 
            lgpio.gpio_write(h_buzz, BUZZER_PIN, 0)
            time.sleep(0.03)
            
    except Exception as e:
        print(f"Buzzer Error: {e}")
    
    finally:
        # Cleanup: Ensure pin is LOW and released
        lgpio.gpio_write(h_buzz, BUZZER_PIN, 0)
        lgpio.gpio_free(h_buzz, BUZZER_PIN)
        lgpio.gpiochip_close(h_buzz)
# boot_buzzer()
