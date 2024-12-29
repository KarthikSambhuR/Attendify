# Attendify - Prototype

Attendify is a lightweight, standalone application designed for managing student attendance using face detection and recognition. It operates without the need for a server, ensuring simplicity and ease of use.

## Features
- **Face Detection**: Utilizes advanced algorithms for reliable face detection.
- **Dynamic Student Management**:  
  - Add students without modifying the code.  
  - Remove students effortlessly with minimal steps.  
- **Serverless Operation**: Stores data locally using SQLite.

## Requirements
To run Attendify, ensure the following are installed on your system:
1. **Python**  
2. **Libraries**:  
   - DLib  
   - face_recognition  
   - OpenCV  
   - NumPy (*up to version 2.0, excluding 2.0*)  
   - Pillow  
   - Tkinter  
   - SQLite3  
   - pickle  

## Installation

### Step 1: Install Dependencies
Run the following command to install the required Python libraries:
```bash
python -m pip install dlib pillow opencv-python face-recognition
```

### Step 2: Resolving Installation Errors
If you encounter issues installing DLib, consider using precompiled binaries from this repository:  
[Precompiled DLib for Windows](https://github.com/z-mahmud22/Dlib_Windows_Python3.x)

## Running the Application
Execute the following command in your terminal to start Attendify:
```bash
python attendify.py
```

## Screenshots
<p align="center">
  <img src="https://raw.githubusercontent.com/KarthikSambhuR/Attendify/refs/heads/main/screenshot/add.png" alt="Add" height="300">
  <img src="https://raw.githubusercontent.com/KarthikSambhuR/Attendify/refs/heads/main/screenshot/main.png" alt="Main" height="300">
  <img src="https://raw.githubusercontent.com/KarthikSambhuR/Attendify/refs/heads/main/screenshot/remove.png" alt="Remove" height="300">
</p>
