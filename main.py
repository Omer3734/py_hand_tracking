import time
import cv2
import mediapipe as mp
import pyautogui
import threading

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

screen_size_x, screen_size_y = pyautogui.size().width, pyautogui.size().height

webcam = cv2.VideoCapture(0)
success, img = webcam.read()
img = cv2.resize(img, (160, 120))
frame_height, frame_width, _ = img.shape

margin_percentage = 0.25
margin_x = int(frame_width * margin_percentage)
margin_y = int(frame_height * margin_percentage)

lock = threading.Lock()  # to ensure thread-safe access to shared resources

# İlk başta, bir önceki pozisyonları saklamak için değişkenleri tanımlayın.
previous_x = 0
previous_y = 0

def move_mouse(hand_landmarks):
    global previous_x, previous_y  # Önceki pozisyonları global olarak tanımlayın.

    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    index_finger_tip_x, index_finger_tip_y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)

    new_x = int((index_finger_tip_x - margin_x) * (screen_size_x / (frame_width - 2 * margin_x)))
    new_y = int((index_finger_tip_y - margin_y) * (screen_size_y / (frame_height - 2 * margin_y)))

    print("///", abs(new_x - previous_x), abs(new_y - previous_y))
    # Önceki pozisyonlarla karşılaştırma yaparak küçük hareketleri engelleme
    if abs(new_x - previous_x) > 13 or abs(new_y - previous_y) > 13:
        with lock:
            pyautogui.moveTo(new_x, new_y)

        # Yeni pozisyonları güncelle
        previous_x, previous_y = new_x, new_y

def click_mouse(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

    thumb_tip_x, thumb_tip_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
    middle_pip_x, middle_pip_y = int(middle_pip.x * frame_width), int(middle_pip.y * frame_height)
    print(abs(thumb_tip_x - middle_pip_x))
    if (abs(thumb_tip_x - middle_pip_x) < 10):
        with lock:
            pyautogui.click()
            time.sleep(0.2)

def hand_tracking():
    while webcam.isOpened():
        success, img = webcam.read()
        img = cv2.flip(img, 1)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.3).process(img)


        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)
                move_mouse(hand_landmarks)
                click_mouse(hand_landmarks)

        cv2.imshow('Koolac', img)

        if cv2.waitKey(50) & 0xFF == ord("q"):
            break

    webcam.release()
    cv2.destroyAllWindows()

# Create and start the threads
hand_tracking_thread = threading.Thread(target=hand_tracking)
hand_tracking_thread.start()

# Wait for the threads to finish
hand_tracking_thread.join()
