import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Read first frame to get its size
ret, frame = cap.read()
if not ret:
    print("Error: Couldn't capture frame from webcam")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Create a blank black canvas with the same size as the webcam frame
canvas = np.zeros_like(frame)

# Define HSV color range for red object (adjust based on object color)
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# Store previous point to draw continuous lines
prev_x, prev_y = None, None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame to avoid mirror effect
    frame = cv2.flip(frame, 1)

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask to detect red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour (assumed to be the marker)
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 500:  # Minimum size to ignore noise
            # Get the center of the contour
            M = cv2.moments(max_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                # Draw circle where the marker is detected
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                # Draw on canvas if a previous point exists
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (cx, cy), (255, 255, 255), 5)

                # Update previous point
                prev_x, prev_y = cx, cy
            else:
                prev_x, prev_y = None, None
        else:
            prev_x, prev_y = None, None
    else:
        prev_x, prev_y = None, None

    # Merge frame with canvas
    combined = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Show output
    cv2.imshow("Air Writing", combined)

    # Clear drawing if 'c' is pressed
    key = cv2.waitKey(1)
    if key == ord('c'):
        canvas[:] = 0  # Reset canvas
    elif key == 27:  # Press 'ESC' to exit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
