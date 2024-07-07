from argparse import ArgumentParser

import cv2 as cv
from hand_detector import HandDetector
import socket

parser = ArgumentParser()
parser.add_argument('--webcam', type=int, default=0,
                    help='The webcam ID in your system. It starts from 0')
parser.add_argument('--min-conf', type=float, default=.7,
                    help='The minimum number of confidence for hand detection')
parser.add_argument('--min-track-conf', type=float, default=.8,
                    help='The minimum number of confidence for hand tracking')
parser.add_argument('--ip', type=str, default='127.0.0.1',
                    help='The IP address to send data to Unity and C#')
parser.add_argument('--port', type=int, default=5052,
                    help='The port to send data to Unity and C#')
opt = parser.parse_args()

cap = cv.VideoCapture(opt.webcam)
detector = HandDetector(max_hands=1, detection_con=opt.min_conf, min_track_con=opt.min_track_conf)

# Communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (opt.ip, opt.port)

while True:
    frame = cap.read()[1]
    h = frame.shape[0]

    frame, hands = detector.find_hands(frame)

    data = []
    # 21 landmarks values: (x, y, z)
    if hands:
        # Get the first hand detected
        hand = hands[0]
        lm_list = hand['lmList']
        for lm in lm_list:
            data.extend([lm[0], h - lm[1], lm[2]])

        sock.sendto(str.encode(str(data)), server_address)

    cv.imshow(f'webcam {opt.webcam}', frame)
    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
