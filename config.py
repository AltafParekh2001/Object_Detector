# Configuration file for Live Object Detection

# CAMERA SETTINGS
CAMERA_INDEX = 0              # Default camera (0 = webcam)
CAMERA_WIDTH = 1280           # Camera frame width
CAMERA_HEIGHT = 720           # Camera frame height
CAMERA_FPS = 30               # Frames per second
CAMERA_WARMUP_FRAMES = 30     # Warmup before detection

# MODEL SETTINGS
# MODEL_NAME = "facebook/detr-resnet-50"
MODEL_NAME = "yolov8m"
CONFIDENCE_THRESHOLD = 0.3
SKIP_FRAMES = 2

# DISPLAY SETTINGS
WINDOW_TITLE = "Live Object Detection"
SHOW_FPS = True
SHOW_DETECTED_COUNT = True
SHOW_CONFIDENCE = True
LINE_THICKNESS = 3
FONT_SCALE = 0.6

# OUTPUT SETTINGS
SAVE_DETECTIONS = True
OUTPUT_DIR = "outputs/"
SAVE_FREQUENCY = 30

# COLOR SETTINGS (BGR)
COLORS = [
    (0, 255, 0),      # Green
    (255, 0, 0),      # Blue
    (0, 0, 255),      # Red
    (0, 255, 255),    # Yellow
    (255, 0, 255),    # Magenta
    (255, 165, 0),    # Orange
    (128, 0, 128),    # Purple
    (0, 128, 128),    # Teal
]

# KEYBOARD SHORTCUTS
QUIT_KEY = 'q'
PAUSE_KEY = 'p'
SCREENSHOT_KEY = 's'

# LOGGING
DEBUG_MODE = True
LOG_FILE = "detection.log"