import cv2
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# import Led


def capture_image():
    # Led.turn_on_light()

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open camera.")
        exit()

    ret, frame = camera.read()
    if ret: 
        img_path ="/home/sortware/Documents/Sort-ware-Solutions/Pre-Scanned_Cards/image_capture.jpg"
        cv2.imwrite(img_path, frame) #change path
        print("Image saved")
    else:
        print("Failed to capture image.")

    camera.release()


