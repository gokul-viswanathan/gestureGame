from flask import Flask, render_template, request, Response
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

app = Flask('game_play')
mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)  
            frame = buffer.tobytes()
            # results = holistic_model.process(frame)

            # #right hand landmarks
            # mp_drawing.draw_landmarks(
            # frame,
            # results.right_hand_landmarks,
            # mp_holistic.HAND_CONNECTIONS
            # )
        
            # # Drawing Left hand Land Marks
            # mp_drawing.draw_landmarks(
            # frame,
            # results.left_hand_landmarks,
            # mp_holistic.HAND_CONNECTIONS
            # )

            yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['GET', 'POST'])
def game():
    return render_template('gameSite.html')

if __name__ == '__main__':
    app.run()