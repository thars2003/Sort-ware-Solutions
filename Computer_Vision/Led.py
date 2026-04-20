import time
import board
import neopixel
import lgpio

LED_PIN = board.D18
NUM_LEDS = 12
GLOBAL_BRIGHTNESS = 0.5

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=GLOBAL_BRIGHTNESS,
    auto_write=False
)

def set_pixel(index, r, g, b, brightness=1.0):
    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)
    pixels[index] = (r, g, b)

def clear():
    pixels.fill((0, 0, 0))
    pixels.show()

def show():
    pixels.show()

def turn_on_light():
    # chip= lgpio.gpiochip_open(0)
    # lgpio.gpio_claim_input(chip,25)
    # lgpio.gpio_claim_output(chip,18)
    # lgpio.gpiochip_close(chip)
    clear()
    for x in range(12):
        set_pixel(x, 255, 255,255, 0.10)
        show()
    # set_pixel(0, 255, 255, 255, 0.05) # Very dim white 
    # set_pixel(1, 255, 255, 255, 0.10) # Dim white 
    # set_pixel(2, 255, 255, 255, 0.15) 
    # set_pixel(3, 255, 255, 255, 0.25) 
    # set_pixel(4, 255, 255, 255, 0.35) 
    # set_pixel(5, 255, 255, 255, 0.45) 
    # set_pixel(6, 255, 255, 255, 0.55) 
    # set_pixel(7, 255, 255, 255, 0.65) 
    # set_pixel(8, 255, 255, 255, 0.75) 
    # set_pixel(9, 255, 255, 255, 0.85) 
    # set_pixel(10, 255, 255, 255, 0.95) 
    # set_pixel(11, 255, 255, 255, 1.00)
    # show()

turn_on_light()