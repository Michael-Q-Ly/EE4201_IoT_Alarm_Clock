import sys
import face_recognition as fr
import cv2

BORDER_COLOR     = (0,255,0)
BORDER_THICKNESS = 2

""" Set up camera """
PORT = 0
cam = cv2.VideoCapture(PORT)

if not cam:
    print( 'Failed VideoCapture: unable to open device {}'.format(PORT) )
    sys.exit(1)

while True:
    ret, frame  = cam.read()

    rgb_frame   = frame[ : , : , : : -1]

    face_locations  = fr.face_locations(rgb_frame)
    face_encodings  = fr.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        cv2.rectangle(frame, (left, top), (right, bottom), BORDER_COLOR, BORDER_THICKNESS)
        
    cv2.imshow('Video', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()