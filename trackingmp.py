import socket
import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#UDP Deffinitions
IP_ADDRESS = "127.0.0.1"
PORT_NUM = 5008
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#------------------------------------------------------------------------------------------------------------------------

#MEDIA PIPE SETUP

#Face detection model
model_path = 'face_landmarker.task'
# Setup based on official MediaPipe Face Landmarker documentation:
# https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python#live-stream_2
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a face landmarker instance with the live stream mode:
def print_result(result, output_image, timestamp_ms):
    print('face landmarker result: {}'.format(result))

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result,
    num_faces=1)

#Time settup (to get frame timestamp)
start_time = time.time()

#------------------------------------------------------------------------------------------------------------------------

#misc. fn's

def get_horizontal_distance(frame, center, x, y, w, h):
    eye_center = x + (w//2)
    return (eye_center - center)/center

def get_timestamp():
    curr_time = time.time()
    elapsed_time = curr_time - start_time
    return int(elapsed_time * 1000)

#------------------------------------------------------------------------------------------------------------------------

#MAIN CAPTURE

#innitializing face detection model
with FaceLandmarker.create_from_options(options) as landmarker:

    # Initialize the webcam hardware (0 is the default built-in camera)
    cap = cv2.VideoCapture(0)

    print("Click the camera window and press 'q' to quit!")
    # Will begin capturing
    delay_count = 0
    delay = 30
    he_string = "0.00"
    while True:
        # Capture frame-by-frame
        # 'frame' is a giant multi-dimensional grid of pixel numbers
        ret, frame = cap.read()
        frame_timestamp = get_timestamp()
        

        if not ret:
            print("Error: Could not read from webcam.")
            break

        #frame_h, frame_w = frame.shape
        #frame_center = frame_w // 2
        
        #creating the mediapipe image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        #running model
        landmarker.detect_async(mp_image, frame_timestamp)
        
        
        #Sending horizontal eye (he) string to unity through UDP
        #client_socket.sendto(he_string.encode(), (IP_ADDRESS, PORT_NUM))

        
        #print data
        delay_count += 1
        # if delay_count % delay == 0:
        #     print (he_string)
        
        
        #display
        cv2.imshow('Web Screen', frame)

        # q to quit - 1ms buffer
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Shut off
    cap.release()
    cv2.destroyAllWindows()