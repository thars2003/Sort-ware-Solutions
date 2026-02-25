import cv2

camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

ret, frame = camera.read()
if ret:
    cv2.imwrite("demo1.jpg", frame)
    print("Image saved as demo1.jpg")
else:
    print("Failed to capture image.")

camera.release()
