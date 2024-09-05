import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize the video capture and hand detector
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils

# Get the screen size
screen_width, screen_height = pyautogui.size()

# Smooth the cursor movement
previous_x, previous_y = 0, 0
smoothening = 5  # Decrease this value for faster movement

# Add a small delay in PyAutoGUI to help stabilize the cursor
pyautogui.PAUSE = 0.001  # Faster sampling rate

def fingers_up(landmarks):
    """ Check which fingers are up based on their landmark positions. """
    tips = [8, 12, 16, 20]  # Index, middle, ring, and pinky tips
    finger_status = []
    
    for tip in tips:
        # Check if the tip of the finger is above the lower joint
        if landmarks[tip].y < landmarks[tip - 2].y:
            finger_status.append(True)
        else:
            finger_status.append(False)
    
    # Thumb is a special case (Check if it's extended by comparing x-coordinates)
    thumb_tip_x = landmarks[4].x
    thumb_joint_x = landmarks[2].x
    if thumb_tip_x < thumb_joint_x:
        finger_status.append(True)
    else:
        finger_status.append(False)
    
    return finger_status

while True:
    # Read a frame from the camera
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark

            # Get the coordinates for the index finger, middle finger, and thumb
            index_finger_tip = landmarks[8]
            middle_finger_tip = landmarks[12]
            thumb_tip = landmarks[4]

            index_x = int(index_finger_tip.x * frame_width)
            index_y = int(index_finger_tip.y * frame_height)
            middle_x = int(middle_finger_tip.x * frame_width)
            middle_y = int(middle_finger_tip.y * frame_height)
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)

            # Convert to screen coordinates
            screen_x = np.interp(index_x, (0, frame_width), (0, screen_width))
            screen_y = np.interp(index_y, (0, frame_height), (0, screen_height))

            # Smooth cursor movement with acceleration
            current_x = previous_x + (screen_x - previous_x) / smoothening
            current_y = previous_y + (screen_y - previous_y) / smoothening

            # Move the cursor
            pyautogui.moveTo(current_x, current_y)
            previous_x, previous_y = current_x, current_y

            # Check if the thumb and index finger are close enough to perform a single-click
            thumb_index_distance = np.hypot(thumb_x - index_x, thumb_y - index_y)
            if thumb_index_distance < 40:
                pyautogui.click()
                pyautogui.sleep(0.25)  # Add a short delay to prevent multiple clicks

            # Check if the index finger and middle finger are close enough to perform a double-click
            index_middle_distance = np.hypot(middle_x - index_x, middle_y - index_y)
            if index_middle_distance < 40:
                pyautogui.doubleClick()
                pyautogui.sleep(0.25)  # Add a short delay to prevent multiple double-clicks

            # Check if all fingers are up to perform a scroll down
            if all(fingers_up(landmarks)):
                pyautogui.scroll(-30)  # Scroll down
                pyautogui.sleep(0.1)  # Add a short delay to prevent continuous scrolling

            # Check if all fingers are closed (except the thumb) to perform a scroll up
            if not any(fingers_up(landmarks)[:4]):
                pyautogui.scroll(30)  # Scroll up
                pyautogui.sleep(0.1)  # Add a short delay to prevent continuous scrolling

    # Display the frame with landmarks
    cv2.imshow('Virtual Mouse', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
