import cv2
import torch
import numpy as np
from ultralytics import YOLO
import time
from datetime import datetime
import os
from config import *

class ObjectDetector:
    """IMPROVED: Live Object Detection using YOLOv8 (Better than DETR)"""

    def __init__(self, confidence_threshold=CONFIDENCE_THRESHOLD,MODEL_NAME=MODEL_NAME):
        """Initialize detector with YOLOv8 model"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Device: {self.device.upper()}")

        print(f"[INFO] Loading YOLOv8 model (BETTER at small objects like pens)...")
        # YOLOv8 is MUCH better at detecting small objects and faces than DETR
        self.detector = YOLO('yolov8m.pt')  # 'm' = medium (balanced speed/accuracy)
        print("[INFO] YOLOv8 model loaded successfully!")

        self.confidence_threshold = confidence_threshold
        self.frame_count = 0
        self.detection_count = 0
        self.start_time = None

    def detect(self, frame):
        """
        Detect objects in frame using YOLOv8
        YOLOv8 is MUCH better at:
        - Small objects (like pens)
        - Faces and people
        - Multiple objects at once
        """
        try:
            # Run YOLOv8 detection
            # conf parameter is KEY - lower it to detect smaller/weaker objects
            results = self.detector(frame, conf=self.confidence_threshold, verbose=False)

            detections = []
            if results and len(results) > 0:
                boxes = results[0].boxes

                for box in boxes:
                    # Extract box coordinates (in pixel values, not normalized)
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    # Get confidence and class
                    confidence = box.conf[0].item()
                    class_id = int(box.cls[0].item())

                    # Get class name from YOLO
                    class_name = results[0].names[class_id]

                    detections.append({
                        'box': {
                            'xmin': x1,
                            'ymin': y1,
                            'xmax': x2,
                            'ymax': y2
                        },
                        'label': class_name,
                        'score': confidence,
                        'class_id': class_id
                    })

            return detections
        except Exception as e:
            print(f"[ERROR] Detection failed: {e}")
            return []

    def draw_boxes(self, frame, detections):
        """Draw bounding boxes on frame with better styling"""
        for idx, detection in enumerate(detections):
            box = detection['box']
            xmin = int(box['xmin'])
            ymin = int(box['ymin'])
            xmax = int(box['xmax'])
            ymax = int(box['ymax'])

            label = detection['label']
            score = detection['score']

            # Select color based on class
            color = COLORS[idx % len(COLORS)]

            # Draw thick rectangle for visibility
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, LINE_THICKNESS)

            # Prepare text with confidence
            text = f"{label}: {score:.1%}"

            # Draw text with background for better visibility
            font = cv2.FONT_HERSHEY_SIMPLEX
            (text_width, text_height), baseline = cv2.getTextSize(
                text, font, FONT_SCALE, 2
            )

            # Draw background rectangle for text
            cv2.rectangle(
                frame,
                (xmin, ymin - text_height - 10),
                (xmin + text_width + 5, ymin),
                color,
                -1  # Filled
            )

            # Draw text
            cv2.putText(
                frame, text,
                (xmin + 2, ymin - 5),
                font, FONT_SCALE,
                (255, 255, 255), 2
            )

        return frame

    def run(self):
        """Run live detection with improved settings"""
        print()
        print("=" * 70)
        print("🚀 IMPROVED LIVE OBJECT DETECTION (YOLOv8)")
        print("=" * 70)
        print()

        print(f"[INFO] Opening camera (index: {CAMERA_INDEX})...")
        cap = cv2.VideoCapture(CAMERA_INDEX)

        if not cap.isOpened():
            print("[ERROR] Could not open camera")
            print("[INFO] Try different CAMERA_INDEX in config.py")
            return

        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
        # Increase brightness for better detection
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
        cap.set(cv2.CAP_PROP_CONTRAST, 0.5)

        print(f"[INFO] Camera opened successfully!")
        print(f"[INFO] Resolution: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
        print()
        print("-" * 70)
        print(f"[INFO] Press '{QUIT_KEY.upper()}' to quit")
        print(f"[INFO] Press '{PAUSE_KEY.upper()}' to pause")
        print(f"[INFO] Press '{SCREENSHOT_KEY.upper()}' to screenshot")
        print("-" * 70)
        print(f"[INFO] YOLOv8 Model - BETTER at detecting pens, faces, and small objects!")
        print()

        self.frame_count = 0
        self.detection_count = 0
        self.start_time = time.time()
        paused = False

        print("[INFO] Warming up camera...")
        for _ in range(CAMERA_WARMUP_FRAMES):
            cap.read()
        print("[INFO] Warmup complete! Detection starting...")
        print()

        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    print("[ERROR] Failed to read frame")
                    break

                frame = cv2.flip(frame, 1)  # Mirror effect
                self.frame_count += 1

                detections = []

                # Process frame every N frames for performance
                if not paused and self.frame_count % SKIP_FRAMES == 0:
                    detections = self.detect(frame)
                    self.detection_count += len(detections)

                    # Print detections to console
                    if detections:
                        print(f"[FRAME {self.frame_count}] Detected {len(detections)} objects:", end=" ")
                        for det in detections:
                            print(f"{det['label']}({det['score']:.0%})", end=" ")
                        print()

                # Draw detections on frame
                frame = self.draw_boxes(frame, detections)

                # Calculate FPS
                elapsed = time.time() - self.start_time
                fps = self.frame_count / elapsed if elapsed > 0 else 0

                # Add info overlay
                if SHOW_FPS:
                    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if SHOW_DETECTED_COUNT:
                    cv2.putText(frame, f"Detected: {len(detections)}", (10, 70),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Add model info
                cv2.putText(frame, "Model: YOLOv8 (Better!)", (10, 110),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

                if paused:
                    cv2.putText(frame, "PAUSED", (frame.shape[1]//2-50, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.putText(frame, f"Press '{QUIT_KEY}' to quit", 
                           (10, frame.shape[0] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                # Display frame
                cv2.imshow(WINDOW_TITLE, frame)

                # Handle keyboard input
                key = cv2.waitKey(500) & 0xFF

                if key == ord(QUIT_KEY):
                    print()
                    print("[INFO] Quit command received...")
                    break
                elif key == ord(PAUSE_KEY):
                    paused = not paused
                    status = "PAUSED" if paused else "RESUMED"
                    print(f"[INFO] Detection {status}")
                elif key == ord(SCREENSHOT_KEY):
                    filename = f"{OUTPUT_DIR}screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    os.makedirs(OUTPUT_DIR, exist_ok=True)
                    cv2.imwrite(filename, frame)
                    print(f"[INFO] Screenshot saved: {filename}")

        except KeyboardInterrupt:
            print()
            print("[INFO] Interrupted by user...")

        finally:
            cap.release()
            cv2.destroyAllWindows()

            # Print statistics
            elapsed = time.time() - self.start_time
            print()
            print("=" * 70)
            print("SESSION STATISTICS")
            print("=" * 70)
            print(f"Total frames: {self.frame_count}")
            print(f"Total detections: {self.detection_count}")
            print(f"Duration: {elapsed:.2f}s")
            print(f"Average FPS: {self.frame_count/elapsed:.2f}")
            print("=" * 70)
            print("[INFO] Camera closed successfully!")
            print("[INFO] YOLOv8 is better at detecting small objects like pens!")
            print()

if __name__ == "__main__":
    detector = ObjectDetector()
    detector.run()