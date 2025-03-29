import cv2
import numpy as np
import mediapipe as mp
import random
import time

# Initialize Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Snake properties
snake = [(400, 300)]  # Initial position
snake_length = 10  # Length of the snake
speed = 5  # Smoothness factor

# Generate a valid fruit position within bounds
def get_new_fruit():
    return random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)

fruit_x, fruit_y = get_new_fruit()

# OpenCV Window
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

game_over = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            finger_x, finger_y = int(index_finger.x * WIDTH), int(index_finger.y * HEIGHT)

            # Move snake towards finger
            snake.append((finger_x, finger_y))
            if len(snake) > snake_length:
                snake.pop(0)

            # Draw the snake continuously following the finger
            for i in range(1, len(snake)):
                cv2.line(frame, snake[i - 1], snake[i], (0, 255, 0), 10)

            # Draw fruit
            cv2.circle(frame, (fruit_x, fruit_y), 10, (0, 0, 255), -1)

            # Check if snake eats fruit
            if abs(finger_x - fruit_x) < 15 and abs(finger_y - fruit_y) < 15:
                snake_length += 10  # Increase length
                fruit_x, fruit_y = get_new_fruit()

            # Check for self-collision (Game Over)
            if len(snake) > 20 and (finger_x, finger_y) in snake[:-10]:
                game_over = True
                break

    if game_over:
        cv2.putText(frame, "GAME OVER!", (250, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        cv2.imshow("Snake Game", frame)
        cv2.waitKey(2000)  # Show Game Over screen for 2 seconds
        snake = [(400, 300)]
        snake_length = 10
        fruit_x, fruit_y = get_new_fruit()
        game_over = False  # Reset the game

    cv2.imshow("Snake Game", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
