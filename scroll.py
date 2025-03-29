import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open webcam
cap = cv2.VideoCapture(0)

prev_y = None  # Store previous Y position of index finger
click_triggered = False  # Prevent multiple clicks on a single pinch

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural movement
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip position (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Get thumb tip position (landmark 4)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

            # Draw circles on index finger and thumb tips
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)  # Green circle for index finger
            cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), -1)  # Blue circle for thumb

            # Scroll logic
            if prev_y is not None:
                if y < prev_y - 100:  # Finger moved up
                    print("Scrolling Up")
                    pyautogui.scroll(-100)

            prev_y = y  # Update previous Y position

            

            # Calculate distance between thumb and index finger
            pinch_distance = math.hypot(thumb_x - x, thumb_y - y)

            # Air Click - Pause Video
            if pinch_distance < 30 and not click_triggered:
                print("Air Click - Pausing Video")

                # Click in the center of the screen to focus on the video
                screen_width, screen_height = pyautogui.size()
                pyautogui.click(screen_width // 2, screen_height // 2)

                time.sleep(0.2)  # Small delay to ensure focus
                pyautogui.press("space")  # Simulate spacebar press (pauses the video)
                click_triggered = True  # Prevent multiple clicks

            elif pinch_distance > 40:
                click_triggered = False  # Reset click trigger when fingers move apart

    # Show the frame
    cv2.imshow("Reels Scroller", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
