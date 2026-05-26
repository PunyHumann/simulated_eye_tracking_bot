# Project CUBE: Interactive AI Robotics Interface

## Overview
Project CUBE is an interactive, spatially-aware robotic assistant that bridges local AI processing with real-time 3D visualization. It utilizes a multi-threaded Python backend to handle computer vision, speech recognition, and conversational AI, streaming live data to a Unity 3D client via an optimized UDP network pipeline. 

## System Architecture
The project is decoupled into a heavy-duty backend logic server and a lightweight frontend visual client, allowing them to run concurrently without performance bottlenecks:

* **Cognitive Engine (Ollama):** Drives the conversational logic using the `llama3.2:3b` local LLM, maintaining conversational context and history to generate natural responses.
* **Spatial Vision (MediaPipe & OpenCV):** Captures real-time facial landmarks from your webcam, isolating eye coordinates to dynamically control the virtual robot's physical orientation and "gaze."
* **Audio Synthesis & Recognition:** Uses a continuous background listening thread for speech-to-text (STT) and Piper TTS (with local `.onnx` models) for seamless, cross-platform voice generation.
* **The Bridge (UDP Pipeline):** The Python backend broadcasts spatial coordinate data and triggers via a local UDP socket (Port 5008). The Unity C# client intercepts these packets to update the 3D cube's behavior with near-zero latency.

## Prerequisites
* **Python:** 3.10+
* **Ollama:** Installed and running locally on the host machine.
* **Hardware:** System microphone and webcam.
* **macOS Only:** PortAudio is required (`brew install portaudio`) prior to fetching Python dependencies.

## Setup & Installation

**1. Clone & Initialize**
Clone the repository and initialize a Python virtual environment:
`git clone https://github.com/PunyHumann/simulated_eye_tracking_bot.git`
`cd simulated_eye_tracking_bot`
`python -m venv venv`
*(Activate the environment: `venv\Scripts\activate` on Windows, or `source venv/bin/activate` on macOS/Linux).*

**2. Install Dependencies**
`pip install -r requirements.txt`

**3. Fetch AI Models**
* **Ollama:** Run `ollama run llama3.2:3b` in your terminal to fetch the core language model.
* **Piper TTS:** Place your desired `.onnx` voice model and its corresponding `.json` file into the `tts_voices/` directory.
* **MediaPipe:** Ensure the `face_landmarker.task` file is located in the root directory.

## Usage 

**1. Launch the Backend Server**
Ensure Ollama is running in the background, then execute the main Python bridge:
`python main.py`

**2. Launch the Unity Client**
* Open the `unity_robot_sim` folder in the Unity Editor.
* Navigate to **Sample Scenes -> Sample Scene**.
* In the Hierarchy, expand **Rotation Test** and click on **THE_CUBE**.
* In the Inspector, verify the `UDP_mp_tracker` C# script is attached.
* Press **Play** in Unity to establish the connection and begin the simulation!

*(To safely terminate the system and release your camera/mic, press `Ctrl + C` in the Python terminal).*