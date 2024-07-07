from typing import Any

import cv2
import numpy as np
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks


class HandDetector:
    def __init__(self, static_mode: bool = False, max_hands: int = 2, detection_con: float = .5, min_track_con: float = .5) -> None:
        self.hands: Hands = Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=min_track_con
        )

    def find_hands(self, frame: np.ndarray, draw: bool = True, flip: bool = True) -> tuple[np.ndarray, list[dict[str, Any]]]:
        img_rgb: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        all_hands: list[dict[str, Any]] = []

        h, w = frame.shape[:2]
        if results.multi_hand_landmarks:
            for hand_type, hand_lms in zip(results.multi_handedness, results.multi_hand_landmarks):
                my_hand = {}

                my_lm_list = []
                x_list = []
                y_list = []
                for lm in hand_lms.landmark:
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    my_lm_list.append((px, py, pz))
                    x_list.append(px)
                    y_list.append(py)

                x_min, x_max = min(x_list), max(x_list)
                y_min, y_max = min(y_list), max(y_list)

                box_w, box_h = x_max - x_min, y_max - y_min
                bbox = x_min, y_min, box_w, box_h
                cx = bbox[0] + (bbox[2] // 2)
                cy = bbox[1] + (bbox[3] // 2)

                my_hand['lmList'] = my_lm_list
                my_hand['bbox'] = bbox
                my_hand['center'] = (cx, cy)

                if flip:
                    if hand_type.classification[0].label == 'Right':
                        my_hand['type'] = 'Left'
                    else:
                        my_hand['type'] = 'Right'
                else:
                    my_hand['type'] = hand_type.classification[0].label

                all_hands.append(my_hand)
                if draw:
                    draw_landmarks(frame, hand_lms, HAND_CONNECTIONS)

                    frame = cv2.rectangle(
                        frame,
                        (bbox[0] - 20, bbox[1] - 20),
                        (bbox[0] + bbox[2] + 20,
                         bbox[1] + bbox[3] + 20),
                        (255, 0, 255),
                        2
                    )

                    frame = cv2.putText(
                        frame,
                        my_hand['type'],
                        (bbox[0] - 30, bbox[1] - 30),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (255, 0, 255),
                        2
                    )

        return frame, all_hands
