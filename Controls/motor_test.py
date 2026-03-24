import lgpio
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, 27)
lgpio.gpio_write(h, 27, 0)  # Enable motor
print("Motor should now lock up. Does it?")
input("Press enter when done")