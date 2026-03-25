import Computer_Vision.Magic as Magic
import Computer_Vision.Pokemon as Pokemon
import Computer_Vision.read_cards as read_cards
import Computer_Vision.camera as camera

camera.capture_image()
text=read_cards.read(f"image_capture")
print (text)