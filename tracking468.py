import socket
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#UDP Deffinitions
IP_ADDRESS = "127.0.0.1"
PORT_NUM = 5008
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def get_horizontal_distance(frame, center, x, y, w, h):
    eye_center = x + (w//2)
    return (eye_center - center)/center



# Initialize the webcam hardware (0 is the default built-in camera)
cap = cv2.VideoCapture(0)

print("Click the camera window and press 'q' to quit!")
# Will begin capturing
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
delay_count = 0
delay = 30
he_string = "0.00"
while True:
    # Capture frame-by-frame
    # 'frame' is a giant multi-dimensional grid of pixel numbers
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read from webcam.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_h, frame_w = gray_frame.shape
    frame_center = frame_w // 2
    
    #frame, scale factor, numNeighbors
    face_boxes = face_cascade.detectMultiScale(gray_frame, 1.25, 7)

    for (x, y, w, h) in face_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
        head_frame = gray_frame[y:y+(h//2), x:x+w]
        eye_boxes = eye_cascade.detectMultiScale(head_frame, 1.02, 10)
        for (e_x, e_y, e_w, e_h) in eye_boxes:
            true_ex = x + e_x
            true_ey = y + e_y
            cv2.rectangle(frame, (true_ex, true_ey), (true_ex + e_w, true_ey + e_h), (0, 255, 0), 3)
            #-1.0 - 1.0
            he_distance = get_horizontal_distance(gray_frame, frame_center, true_ex, true_ey, e_w, e_h)
            he_string = f"{he_distance:.2f}"
    
    #Sending horizontal eye (he) string to unity through UDP
    client_socket.sendto(he_string.encode(), (IP_ADDRESS, PORT_NUM))

    
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