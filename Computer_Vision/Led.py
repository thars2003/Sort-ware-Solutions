import time
import board
import neopixel

# ==========================
# LED CONFIGURATION
# ==========================
LED_PIN = board.D18      # GPIO18
NUM_LEDS = 12
GLOBAL_BRIGHTNESS = 0.5  # 0.0 – 1.0

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=GLOBAL_BRIGHTNESS,
    auto_write=False
)

# ==========================
# HELPER FUNCTIONS
# ==========================
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

# ==========================
# EXAMPLE USAGE
# ==========================
clear()

set_pixel(0, 255, 255, 255, 0.05) # Very dim white 
set_pixel(1, 255, 255, 255, 0.10) # Dim white 
set_pixel(2, 255, 255, 255, 0.15) 
set_pixel(3, 255, 255, 255, 0.25) 
set_pixel(4, 255, 255, 255, 0.35) 
set_pixel(5, 255, 255, 255, 0.45) 
set_pixel(6, 255, 255, 255, 0.55) 
set_pixel(7, 255, 255, 255, 0.65) 
set_pixel(8, 255, 255, 255, 0.75) 
set_pixel(9, 255, 255, 255, 0.85) 
set_pixel(10, 255, 255, 255, 0.95) 
set_pixel(11, 255, 255, 255, 1.00)

show()

while True:
    time.sleep(1)

if __name__ == "__main__":
    turn_on_light()