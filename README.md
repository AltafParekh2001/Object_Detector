# Live Object Detection System

Real-time object detection using Facebook's DETR model and Hugging Face Transformers.

## Features

- 📹 Real-time webcam detection
- 🎯 91 object classes
- 📊 Bounding boxes with confidence scores
- ⚡ High performance FPS counter
- 🎨 Color-coded detection boxes
- 🖼️ Screenshot functionality
- ⏸️ Pause/Resume detection
- 📈 Session statistics

## System Requirements

- Python 3.8+
- Webcam
- 8GB RAM minimum
- NVIDIA GPU optional

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Program
```bash
python main.py
```

### 3. Keyboard Shortcuts
- **Q** - Quit
- **P** - Pause/Resume
- **S** - Screenshot

## Configuration

Edit `config.py` to customize:
- Camera settings
- Detection sensitivity
- Display options
- Output directory

## Troubleshooting

**Camera not working:**
- Check if camera is connected
- Try different CAMERA_INDEX in config.py
- Close other camera apps (Zoom, Teams, etc.)

**Low FPS:**
- Increase SKIP_FRAMES in config.py
- Reduce CAMERA_WIDTH/HEIGHT
- Lower CONFIDENCE_THRESHOLD

## Detectable Objects (91 Classes)

- People: person
- Animals: cat, dog, bird, horse, cow, sheep, elephant, bear, zebra, giraffe
- Vehicles: car, bicycle, motorcycle, airplane, bus, train, truck, boat
- Electronics: laptop, tv, keyboard, mouse, cell phone, remote
- Furniture: chair, couch, bed, table, bench
- And 46 more classes...


## License

MIT License

## Support

For issues, check config.py or enable DEBUG_MODE
