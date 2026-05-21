import socket
import cv2
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils as mp_drawing
from mediapipe.tasks.python.vision import drawing_styles


keep_running = True

#UDP Deffinitions
IP_ADDRESS = "127.0.0.1"
PORT_NUM = 5008
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#------------------------------------------------------------------------------------------------------------------------

#MEDIA PIPE SETUP

#clipboard containing latest mp image
mp_clipboard = None

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
    global keep_running
    global mp_clipboard
    #print('face landmarker result: {}'.format(result))
    if result.face_landmarks and keep_running:
        face_landmarks = result.face_landmarks[0]
        numpy_matrix = output_image.numpy_view().copy()

        mp_drawing.draw_landmarks(
            image=numpy_matrix,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style())
        mp_clipboard = numpy_matrix
        
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result,
    num_faces=1,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True)

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
    while keep_running:
        # Capture frame-by-frame
        # 'frame' is a giant multi-dimensional grid of pixel numbers
        ret, frame = cap.read()
        frame_timestamp = get_timestamp()
        
        if not ret:
            print("Error: Could not read from webcam.")
            break
        
        #converting BGR to RGB / creating mp image object
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        #running model
        landmarker.detect_async(mp_image, frame_timestamp)
        
        if mp_clipboard is not None:
            #print("something is here")
            rendered_frame = cv2.cvtColor(mp_clipboard, cv2.COLOR_RGB2BGR)
            cv2.imshow("Face detection", rendered_frame)
        #else:
            #cv2.imshow("Face detection", frame)
        # q to quit - 1ms buffer
        if cv2.waitKey(1) & 0xFF == ord('q'):
            keep_running = False
        
        #Sending horizontal eye (he) string to unity through UDP
        #client_socket.sendto(he_string.encode(), (IP_ADDRESS, PORT_NUM))

        
    # Shut off
    cap.release()
    cv2.destroyAllWindows()