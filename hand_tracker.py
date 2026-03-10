import cv2
import mediapipe as mp
import threading
import time

class HandTracker:
    def __init__(self, camera_index=0, smoothing_factor=0.3):
        self.camera_index = camera_index
        self.smoothing_factor = smoothing_factor
        
        # MediaPipe initialization
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Tracking state
        self.current_pos = None      # Raw position
        self.smoothed_pos = None     # Smoothed position
        self.is_detected = False
        self.confidence = 0.0
        
        # Threading state
        self.capture = cv2.VideoCapture(self.camera_index)
        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def _update_loop(self):
        while self.running:
            success, frame = self.capture.read()
            if not success:
                time.sleep(0.01)
                continue
            
            # Flip frame horizontally for selfie-view display and convert to RGB
            frame = cv2.flip(frame, 1)
            results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if results.multi_hand_landmarks and results.multi_handedness:
                hand_landmarks = results.multi_hand_landmarks[0]
                handedness = results.multi_handedness[0]
                
                # Get index finger tip (landmark 8)
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                # Store normalized coordinates
                self.current_pos = (index_tip.x, index_tip.y)
                self.confidence = handedness.classification[0].score
                self.is_detected = True
            else:
                self.is_detected = False
                # Slowly decay confidence
                self.confidence = max(0.0, self.confidence - 0.1)

            # Small sleep to yield execution
            time.sleep(0.005)

    def get_position(self, screen_width, screen_height):
        """Returns the smoothed pixel coordinates of the index finger."""
        if not self.is_detected or self.current_pos is None:
            return None
            
        target_x = self.current_pos[0] * screen_width
        target_y = self.current_pos[1] * screen_height
        
        if self.smoothed_pos is None:
            self.smoothed_pos = (target_x, target_y)
        else:
            # Exponential Moving Average for smoothing
            new_x = self.smoothed_pos[0] + self.smoothing_factor * (target_x - self.smoothed_pos[0])
            new_y = self.smoothed_pos[1] + self.smoothing_factor * (target_y - self.smoothed_pos[1])
            self.smoothed_pos = (new_x, new_y)
            
        return self.smoothed_pos

    def get_expo_stats(self):
        return {
            "detected": self.is_detected,
            "confidence": self.confidence
        }

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
        self.capture.release()
        self.hands.close()
