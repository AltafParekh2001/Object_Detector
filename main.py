#!/usr/bin/env python3
"""
Live Object Detection - Main Entry Point

Usage:
    python main.py
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from detector import ObjectDetector
from config import *

def main():
    print()
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 15 + "LIVE OBJECT DETECTION SYSTEM" + " " * 25 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print()

    if SAVE_DETECTIONS:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"[INFO] Output directory: {OUTPUT_DIR}")

    print("[INFO] Initializing detector...")
    detector = ObjectDetector(
        MODEL_NAME=MODEL_NAME,
        confidence_threshold=CONFIDENCE_THRESHOLD
    )

    print()
    print("[INFO] Starting live detection...")
    print()

    detector.run()

    print("[INFO] Program finished!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        print("[INFO] Check config.py for settings")
        sys.exit(1)
