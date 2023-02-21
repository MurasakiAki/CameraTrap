import cv2
import time

# Initialize camera
camera = cv2.VideoCapture(0)
time.sleep(2)

# Capture initial frame for comparison
_, previous_frame = camera.read()
previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

# Define threshold for motion detection
threshold = 10000

# Main loop for motion detection
while True:
    # Capture current frame and convert to grayscale
    _, current_frame = camera.read()
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Calculate difference between current and previous frame
    frame_diff = cv2.absdiff(previous_gray, current_gray)

    # Apply threshold to detect motion
    _, frame_diff_threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    # Calculate number of non-zero pixels in thresholded difference image
    motion = cv2.countNonZero(frame_diff_threshold)
    
    # If motion is detected, print message and save image
    if motion > threshold:
        print("Motion detected!")
        cv2.imwrite("motion_detected.jpg", current_frame)

    # Set current frame as previous frame for next iteration
    previous_gray = current_gray

    # Wait for a moment before repeating loop
    time.sleep(0.1)