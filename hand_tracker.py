import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands, min_detection_confidence=detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def find_gesture(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame for visualization
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # --- Gesture Recognition Logic ---
                landmarks = hand_landmarks.landmark
                finger_tips = [8, 12, 16, 20] # Index, Middle, Ring, Pinky tips
                thumb_tip = 4

                # Check if fingers are open or closed
                fingers_up = []
                # Thumb check (compares x-coordinate)
                if landmarks[thumb_tip].x < landmarks[thumb_tip - 1].x:
                    fingers_up.append(1)
                else:
                    fingers_up.append(0)

                # Other four fingers check (compares y-coordinate)
                for tip_id in finger_tips:
                    if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                        fingers_up.append(1)
                    else:
                        fingers_up.append(0)
                
                total_fingers = fingers_up.count(1)

                # Determine Gesture based on the number and position of raised fingers
                if total_fingers == 0 or (fingers_up[0] == 0 and total_fingers == 1):
                    gesture = "Rock"
                elif total_fingers == 5:
                    gesture = "Paper"
                elif fingers_up[1] and fingers_up[2] and not fingers_up[3] and not fingers_up[4]:
                    gesture = "Scissors"

        return gesture, frame