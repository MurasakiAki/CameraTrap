import os
import cv2
import time
import imutils
from pathlib import Path
from configparser import ConfigParser

# Initialize camera
camera = cv2.VideoCapture(0)
time.sleep(2)

#Initialize config parser
config = ConfigParser()

# Capture initial frame for comparison
_, initial_frame = camera.read()
initial_frame = imutils.rotate(initial_frame, 180)
initial_gray = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)

#Set camera config from config file
path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")

config.read(config_path)

mode = config.get('config', 'mode')
video_time = config.getint('config', 'time')
#print(mode)

# Main loop for motion detection
while True:

    #Photo mode
    if mode == "photo":
        # Define threshold for motion detection
        threshold = 10000

        # Capture current frame and convert to grayscale
        config = ConfigParser()
        _, current_frame = camera.read()
        current_frame = imutils.rotate(current_frame, 180)
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
            #print("Motion detected!")
            cv2.imwrite("Captures/"+file_name, current_frame)
            
        # Set current frame as previous frame for next iteration
        initial_gray = current_gray

        # Wait for a moment before repeating loop
        time.sleep(0.2)

    #Video mode
    elif mode == "video":
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))
    
        start_time = time.time()
        while (time.time() - start_time) < video_time:
            ret, frame = camera.read()
            out.write(frame)
        
        camera.release()
        out.release()