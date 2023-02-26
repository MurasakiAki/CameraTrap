import cv2
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mode = config.get('motion', 'mode')
time_limit = int(config.get('motion', 'time'))

if mode == 'photo':
    print("Capturing photo...")
    # initialize video capture
    cap = cv2.VideoCapture(0)
    # capture a single frame
    ret, frame = cap.read()
    # save the captured frame
    cv2.imwrite('motion_photo.jpg', frame)
    # release the capture
    cap.release()
    print("Photo captured!")
else:
    print("Recording video...")
    # initialize video capture
    cap = cv2.VideoCapture(0)
    # initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('motion_video.avi', fourcc, 20.0, (640, 480))
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
    # release the capture and writer
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Video recorded!")
