import configparser
import cv2
import time
import os
from pathlib import Path

# Load configuration settings from config.ini file

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)
mode = config.get('Settings', 'mode')
time_limit = config.getint('Settings', 'time')
is_running = config.getboolean('Settings', 'is_running')

# Initialize camera and motion detector
camera = None
detector = cv2.createBackgroundSubtractorMOG2()

# Create folder to store captured files if it does not already exist
if not os.path.exists('Captures'):
    os.makedirs('Captures')

# Main loop to capture photos or videos when motion is detected
while is_running:
    try:
        # Initialize camera if it has not already been initialized
        if camera is None:
            camera = cv2.VideoCapture(0)

        # Capture a frame from the camera and convert it to grayscale
        ret, frame = camera.read()
        if not ret:
            raise Exception("Error: Camera read failed")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply background subtraction to the frame to detect motion
        mask = detector.apply(gray)

        # Check if enough motion has been detected to trigger a capture
        motion = (cv2.countNonZero(mask) > 1000)

        # If motion has been detected, capture a photo or video based on the configuration settings
        if motion:
            filename = time.strftime('%Y%m%d-%H%M%S')
            if mode == 'photo':
                cv2.imwrite(f'Captures/{filename}.jpg', frame)
            elif mode == 'video':
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(f'Captures/{filename}.mp4', fourcc, 20.0, (640, 480))
                start_time = time.time()
                while (time.time() - start_time) < time_limit:
                    ret, frame = camera.read()
                    if not ret:
                        raise Exception("Error: Camera read failed")
                    out.write(frame)
                out.release()

        # Wait for a short period of time before capturing the next frame
        time.sleep(0.1)

        # Check the is_running setting in the config file to see if the loop should be stopped
        config.read(config_path)
        is_running = config.getboolean('Settings', 'is_running')

    except KeyboardInterrupt:
        # If the user presses CTRL+C, release the camera and video writer objects
        print("\nStopping the script...")
        if camera is not None:
            camera.release()
        cv2.destroyAllWindows()
        break

# Release the camera and video writer objects
if camera is not None:
    camera.release()
cv2.destroyAllWindows()