import time
import board
import neopixel

# ==========================
# LED CONFIGURATION
# ==========================
LED_PIN = board.D18
NUM_LEDS = 12
GLOBAL_BRIGHTNESS = 1.0  # 0.0 – 1.0 (master brightness)

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=GLOBAL_BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# ==========================
# HELPER FUNCTIONS
# ==========================
def set_pixel(index, r, g, b, brightness=1.0):
    """
    Set a single LED's color and brightness
    brightness: 0.0 – 1.0
    """
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

# Set each LED individually
set_pixel(0, 255, 255, 255, 0.05)  # Very dim white
set_pixel(1, 255, 255, 255, 0.10)  # Dim white
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

# Keep LEDs on
while True:
    time.sleep(1)







###### RAINBOW LED #######


# import timecd 
# import board
# import neopixel
# import colorsys

# # LED configuration
# PIN = board.D18        # GPIO18 (PWM-capable)
# NUMPIXELS = 12         # Adjust to your ring size
# MAX_BRIGHTNESS = 150   # Match Arduino sketch (0–255)

# # Create NeoPixel object
# pixels = neopixel.NeoPixel(
#     PIN,
#     NUMPIXELS,
#     brightness=0.0,
#     auto_write=False,
#     pixel_order=neopixel.GRB
# )

# def update_rainbow(brightness):
#     # Convert Arduino-style brightness (0–255) to 0.0–1.0
#     pixels.brightness = brightness / 255.0

#     for i in range(NUMPIXELS):
#         # Spread hue evenly across the ring
#         hue = i / NUMPIXELS
#         r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

#         pixels[i] = (
#             int(r * 255),
#             int(g * 255),
#             int(b * 255)
#         )

#     pixels.show()

# while True:
#     # 1. FADE IN
#     for b in range(0, MAX_BRIGHTNESS + 1, 2):
#         update_rainbow(b)
#         time.sleep(0.013)  # ~1 second total fade

#     # 2. FADE OUT
#     for b in range(MAX_BRIGHTNESS, -1, -2):
#         update_rainbow(b)
#         time.sleep(0.013)

