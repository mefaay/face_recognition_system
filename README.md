# Face Recognition System

## Overview

This project is a face recognition system that allows users to register individuals with photos, query their details, and recognize faces via uploaded images or a live camera feed. The system is designed to be user-friendly and can be applied in various fields such as security systems, attendance tracking, and monitoring.

## Features

- **Register Individuals**: Add individuals with their photo and personal details (name, phone, address).
- **Query Individuals**: Search for individuals by their name, with support for case-insensitive and accent-insensitive queries.
- **Face Recognition**: Upload an image or use a camera to recognize faces and display detailed information.
- **Camera Support**: Capture and recognize faces directly from a live camera feed.
- **Display Information**: View recognized individuals' details (name, phone, address) alongside their photos.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mefaay/face_recognition_system.git
    ```
2. Navigate to the project directory:
    ```bash
    cd face_recognition_system
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```bash
    python app.py
    ```
2. Use the interface to register, query, or recognize faces via uploaded images or live camera feed.

## Technologies Used

- **Python**: The core programming language used.
- **Tkinter**: For the graphical user interface (GUI).
- **OpenCV**: For handling image and video capture.
- **face_recognition**: For facial recognition functionality.
- **SQLite**: For managing the database of registered individuals.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
