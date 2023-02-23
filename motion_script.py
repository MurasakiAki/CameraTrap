import cv2
import time
import datetime
from configparser import ConfigParser

# Initialize camera
camera = cv2.VideoCapture(0)
time.sleep(2)

# Capture initial frame for comparison
_, initial_frame = camera.read()

#Increase brightness in case of dark enviroment
def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

#Increasing brightness of the initial frame
initial_gray = increase_brightness(initial_frame)
initial_gray = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)

# Define threshold for motion detection
threshold = 10000

#Set config from config file
config = ConfigParser()
config.read("config.ini")

mode = config.get('config', 'mode')
video_time = config.getint('config', 'time')
print(mode)

# Main loop for motion detection
while True:
    # Capture current frame and convert to grayscale
    _, current_frame = camera.read()
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Calculate difference between current and previous frame
    frame_diff = cv2.absdiff(initial_gray, current_gray)

    # Apply threshold to detect motion
    _, frame_diff_threshold = cv2.threshold(frame_diff, 45, 255, cv2.THRESH_BINARY)

    # Calculate number of non-zero pixels in thresholded difference image
    motion = cv2.countNonZero(frame_diff_threshold)
    
    # If motion is detected, print message and save image
    if motion > threshold:
        current_time = time.ctime()
        file_name = f"motion_detected_on_"+ current_time +".jpg"
        print("Motion detected!")
        cv2.imwrite("Captures/"+file_name, current_frame)

    # Set current frame as previous frame for next iteration
    initial_gray = current_gray

    # Wait for a moment before repeating loop
    time.sleep(0.1)