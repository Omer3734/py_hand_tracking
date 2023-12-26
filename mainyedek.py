import time
import cv2
import mediapipe
import pyautogui
import threading

thread_lock = threading.Lock()

cam = cv2.VideoCapture(0)
_, frame = cam.read()
screen_w, screen_h = pyautogui.size()
mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands()
mp_drawing_utils = mediapipe.solutions.drawing_utils
frame_height, frame_width, _ = frame.shape

rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)




margin_percentage = 0.2
margin_x = int(frame_width * margin_percentage)
margin_y = int(frame_height * margin_percentage)

temp_x = 0
temp_y = 0

def screen():
    cv2.imshow("Image", frame)
    cv2.waitKey(1)

def mouse_movement():
    global frame, result, hand_landmarks
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)
    hand_landmarks = result.multi_hand_landmarks[0]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    if result.multi_hand_landmarks:

        index_finger_tip_x, index_finger_tip_y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)

        new_x = int((index_finger_tip_x - margin_x) * (screen_w / (frame_width - 2 * margin_x)))
        new_y = int((index_finger_tip_y - margin_y) * (screen_h / (frame_height - 2 * margin_y)))
        cv2.circle(frame, (new_x, new_y), 3, (0, 255, 255))

        if (abs(new_x - temp_x) and abs(new_y - temp_y) > 13):
            pyautogui.moveTo(new_x, new_y)

def mouse_click():
    global thumb_tip, middle_pip

    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

    thumb_tip_x, thumb_tip_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
    middle_pip_x, middle_pip_y = int(middle_pip.x * frame_width), int(middle_pip.y * frame_height)
    if ((thumb_tip_x + thumb_tip_y) - (middle_pip_x + middle_pip_y)) > -18:
        pyautogui.click()
        time.sleep(0.5)


while True:
    screen()
    mouse_movement()
    mouse_click()