import cv2
import time
import os
from pathlib import Path
import configparser

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

mode = config.get('config', 'mode')
time_limit = int(config.get('config', 'time'))
capture_interval = int(config.get('config', 'capture_interval'))
motion_detection_interval = int(config.get('config', 'motion_detection_interval'))

if mode == 'photo':
    print("Capturing photos...")
else:
    print("Recording videos...")

    
# initialize motion detection parameters
motion_frame = None
motion_detected = False
frame_count = 0

# start capture loop
while True:

    # initialize video capture
    cap = cv2.VideoCapture(-1, cv2.CAP_V4L)
    time.sleep(2)

    # capture a frame
    ret, frame = cap.read()
    if frame is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
    else:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

    cap.release()

    # increment frame count
    frame_count += 1

    # convert frame to grayscale for motion detection
    
    
    # set initial motion frame
    if motion_frame is None:
        motion_frame = gray
        continue
    
    # detect motion every nth frame
    if frame_count % motion_detection_interval == 0:
    # calculate difference between current frame and motion frame
        frame_delta = cv2.absdiff(motion_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    
        # dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
    
        # find contours in the thresholded image
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # check if motion is detected
        for c in contours:
            if cv2.contourArea(c) < 500:
                continue
            motion_detected = True
    
        # reset motion frame if no motion is detected
        if not motion_detected:
            motion_frame = gray
    
        # capture photo or record video if motion is detected
        if motion_detected:
            if mode == 'photo':
                # capture a single frame
                image_path = f'motion_on_{time.time()}.png'
                cv2.imwrite('Captures/' + image_path, frame)
                print("Photo captured!")
            else:

                # initialize video capture
                cap = cv2.VideoCapture(-1, cv2.CAP_V4L)
                time.sleep(2)

                # initialize video writer
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(f'motion_video_{time.time()}.avi', fourcc, 20.0, (640, 480))
                # start recording
                start_time = time.time()
                while time.time() - start_time < time_limit:
                    # capture a frame
                    ret, frame = cap.read()
                    # write the frame to the video file 
                    out.write(frame)
                    # display the frame
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                # release the writer
                out.release()
                cv2.destroyAllWindows()
                cap.release()
                print("Video recorded!")
        
            # reset motion detection parameters
            motion_detected = False
            motion_frame = None
            frame_count = 0
    
            #
    