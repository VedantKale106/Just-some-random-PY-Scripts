import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

class GestureControlApp(App):
    def build(self):
        self.image = Image()
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Run at 30 FPS
        self.cap = cv2.VideoCapture(0)

        self.prev_y = None
        self.click_triggered = False
        return self.image

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip the frame for natural movement
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame with MediaPipe
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get index finger position
                index_finger_tip = hand_landmarks.landmark[8]
                x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                # Get thumb position
                thumb_tip = hand_landmarks.landmark[4]
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)

                # Scroll logic
                if self.prev_y is not None:
                    if y < self.prev_y - 100:  # Finger moved up
                        print("Scrolling Up")
                        pyautogui.scroll(-100)

                self.prev_y = y  # Update previous Y position

                # Check for pinch gesture (Thumb & Index Finger)
                pinch_distance = math.hypot(thumb_x - x, thumb_y - y)
                if pinch_distance < 30 and not self.click_triggered:
                    print("Air Click - Pausing Video")

                    # Simulate a spacebar press to pause the video
                    pyautogui.press("space")
                    self.click_triggered = True

                elif pinch_distance > 40:
                    self.click_triggered = False  # Reset when fingers move apart

        # Convert to Kivy texture for display
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = texture

    def on_stop(self):
        self.cap.release()  # Release webcam when app stops

# Run the app
if __name__ == "__main__":
    GestureControlApp().run()
