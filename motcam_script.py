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

# create capture object
cap = cv2.VideoCapture(0)
# create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

if mode == 'photo':
    print("Capturing photo...")
    while True:
        # read a frame
        ret, frame = cap.read()
        # apply background subtraction
        fgmask = fgbg.apply(frame)
        # count non-zero pixels in the mask
        count = cv2.countNonZero(fgmask)
        # if motion is detected, take a photo
        if count > 100:
            image_path = f'motion_on{time.ctime()}.png'
            cv2.imwrite('Captures/' + image_path, frame)
            print("Photo captured!")
            break
        # display the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

elif mode == 'video':
    print("Recording video...")
    # initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('motion_video.avi', fourcc, 20.0, (640, 480))
    # start recording
    start_time = time.time()
    while True:
        # read a frame
        ret, frame = cap.read()
        # apply background subtraction
        fgmask = fgbg.apply(frame)
        # count non-zero pixels in the mask
        count = cv2.countNonZero(fgmask)
        # if motion is detected, start recording
        if count > 100:
            print("Motion detected! Recording video...")
            while time.time() - start_time < time_limit:
                # read a frame
                ret, frame = cap.read()
                # apply background subtraction
                fgmask = fgbg.apply(frame)
                # write the frame to the video file
                out.write(frame)
                # count non-zero pixels in the mask
                count = cv2.countNonZero(fgmask)
                # if motion is no longer detected, stop recording
                if count <= 100:
                    print("Motion stopped! Video recorded!")
                    break
                # display the frame
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            break
        # display the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# release the capture and writer
cap.release()
cv2.destroyAllWindows()
if mode == 'video':
    out.release()
