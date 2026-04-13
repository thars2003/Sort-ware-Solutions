import dispenser
import time
# # dispenser._get_bin_motor().enable()
dispenser._get_dispense_motor().enable()

dispenser.dispense_card()

dispenser.dispense_card()
dispenser.dispense_card()

dispenser._get_dispense_motor().disable()



# dispenser.move_bin(9)
# dispenser.move_bin(4)
# time.sleep(5)
# dispenser.move_bin(2)
# time.sleep(5)
# dispenser.move_bin(9)
# time.sleep(5)

# dispenser.move_bin(2)