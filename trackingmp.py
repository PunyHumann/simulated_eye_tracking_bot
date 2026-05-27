import os
import socket
import cv2
import time
import threading
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils as mp_drawing
from mediapipe.tasks.python.vision import drawing_styles


keep_running = True
frame = None

#UDP Deffinitions
IP_ADDRESS = "127.0.0.1"
PORT_NUM = 5008
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#------------------------------------------------------------------------------------------------------------------------

#misc. fn's

def get_timestamp():
    curr_time = time.time()
    elapsed_time = curr_time - start_time
    return int(elapsed_time * 1000)

#------------------------------------------------------------------------------------------------------------------------

#DEEPFACE SETUP:

def deepface_file_pass():
    while True:
        if frame is not None and os.path.isfile("deepface_check.txt"):
            cv2.imwrite("deepface_frame.jpg", frame)
            os.remove("deepface_check.txt")

deepface_thread = threading.Thread(target=deepface_file_pass, daemon=True)
deepface_thread.start()

#------------------------------------------------------------------------------------------------------------------------

#MEDIA PIPE SETUP

#globals
#clipboard containing latest mp image
mp_clipboard = None
eye_center_x = 0.0
eye_center_y = 0.0

#Face detection model
model_path = 'face_landmarker.task'
# MediaPipe setup:
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Here we can play around with the result
def return_result(result, output_image, timestamp_ms):
    global keep_running
    global mp_clipboard
    global eye_center_x
    global eye_center_y
    MY_POINT_COLOR = (255, 0, 0)
    #custom_line_spec = mp_drawing.DrawingSpec(color=MY_LINE_COLOR, thickness=1, circle_radius=1)
    custom_point_spec = mp_drawing.DrawingSpec(color=MY_POINT_COLOR, thickness=1, circle_radius=1)

    #print('face landmarker result: {}'.format(result))
    if result.face_landmarks and keep_running:
        face_landmarks = result.face_landmarks[0]
        numpy_matrix = output_image.numpy_view().copy()

        #drawing face mesh
        mp_drawing.draw_landmarks(
            image=numpy_matrix,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
            landmark_drawing_spec=custom_point_spec,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
            # connection_drawing_spec=custom_line_spec
            )
        
        mp_drawing.draw_landmarks(
            image=numpy_matrix,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_LEFT_IRIS,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style())
        
        mp_drawing.draw_landmarks(
            image=numpy_matrix,
            landmark_list=face_landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_RIGHT_IRIS,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style())
        
        #isolating eyes coords
        far_left_eye_corner = result.face_landmarks[0][33]
        far_right_eye_corner = result.face_landmarks[0][362]
        lc_x, lc_y = far_left_eye_corner.x, far_left_eye_corner.y
        rc_x, rc_y = far_right_eye_corner.x, far_right_eye_corner.y
        eye_center_x = ((lc_x + rc_x)/2 - 0.5) * 2
        eye_center_y = ((lc_y + rc_y)/2 - 0.5) * -2
        #print(f"x: {eye_center_x}, y: {eye_center_y}")

        mp_clipboard = numpy_matrix
        
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=return_result,
    num_faces=1,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True)

#Time settup (to get frame timestamp)
start_time = time.time()

#------------------------------------------------------------------------------------------------------------------------

#MAIN CAPTURE

#innitializing face detection model
with FaceLandmarker.create_from_options(options) as landmarker:

    # Initialize the webcam hardware (0 is the default built-in camera)
    cap = cv2.VideoCapture(0)

    # Will begin capturing
    try:
        while True:
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
            #running media pipe model
            landmarker.detect_async(mp_image, frame_timestamp)
            
            #image output
            if mp_clipboard is not None:
                rendered_frame = cv2.cvtColor(mp_clipboard, cv2.COLOR_RGB2BGR)
                cv2.imshow("Face detection", rendered_frame)
            
            #udp
            eye_center_x_string = f"{eye_center_x:.2f}"
            eye_center_y_string = f"{eye_center_y:.2f}"
            udp_string = eye_center_x_string + ',' + eye_center_y_string
            client_socket.sendto(udp_string.encode(), (IP_ADDRESS, PORT_NUM))

            cv2.waitKey(1)
        
    except KeyboardInterrupt:
        # Shut off
        cap.release()
        cv2.destroyAllWindows()