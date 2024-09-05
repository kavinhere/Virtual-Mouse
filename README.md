# CV_Virtual_mouse_Project
Its a hands-on project built using python 
This project implements a *Virtual Mouse* using computer vision techniques. The virtual mouse allows users to interact with their computer using hand gestures, which are captured by a camera and translated into mouse movements and clicks.

## Features

- *Hand Gesture Recognition*: Uses a webcam to capture hand gestures.
- *Mouse Control*: Translates gestures into mouse movements and actions (e.g., clicks).
- *Real-time Tracking*: Provides real-time feedback on hand position and gestures.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- PyAutoGUI

To install the dependencies, run:

bash
pip install opencv-python mediapipe pyautogui

Usage
Clone the repository:

bash
git clone https://github.com/kavinhere/Virtual-Mouse.git
Navigate to the project directory:

bash
cd virtual-mouse

Run the script:

bash
python Virtual_Mouse.py

Make sure your webcam is connected and accessible.

How It Works:

The script captures live video feed from the webcam.
It detects hand landmarks using the Mediapipe library.
The detected hand gestures are mapped to corresponding mouse movements and actions using PyAutoGUI.
Contributing
If you'd like to contribute to the project, feel free to submit a pull request or open an issue for discussion.

License:

This project is licensed under the MIT License.

