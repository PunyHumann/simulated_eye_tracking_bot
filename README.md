Project CUBE: Interactive AI Robotics Interface
Overview
Project CUBE is a modular, locally-hosted conversational AI and computer vision backend designed to interface with a visual client (such as Unity). The system combines local Large Language Models (LLMs), real-time facial tracking, and cross-platform audio synthesis to create an interactive, spatially aware robotic assistant.

System Architecture
The project is divided into distinct operational modules that run concurrently:

Cognitive Engine (Ollama): Utilizes the llama3.2:3b model to generate context-aware, concise responses based on a persistent chat history.

Speech Recognition (STT): Captures ambient audio via the system microphone and processes it continuously using a background listening thread.

Audio Synthesis (TTS): Uses Piper TTS with local .onnx models to generate responsive audio seamlessly across Windows, macOS, and Linux environments.

Spatial Vision (MediaPipe & OpenCV): Tracks user facial landmarks in real-time, isolates the coordinates of the eyes, and transmits the user's focal point over a UDP socket (Port 5008) to control the physical or virtual orientation of the robot.

Prerequisites
Python: Version 3.10 or higher.

Ollama: Installed and running locally on the host machine.

Hardware: System microphone and webcam.

macOS Users Only: Must install PortAudio via Homebrew (brew install portaudio) before installing Python dependencies.

Installation
1. Clone the repository and navigate to the directory:

Bash
git clone <your-repository-url>
cd <your-repository-folder>
2. Initialize a Python virtual environment:

Bash
python -m venv venv
Activate on Windows: venv\Scripts\activate
Activate on macOS/Linux: source venv/bin/activate

3. Install project dependencies:

Bash
pip install -r requirements.txt
4. Download AI Models:

Ollama: Run ollama run llama3.2:3b in your terminal to fetch the core LLM.

Piper TTS: Place your desired .onnx voice model (e.g., en_US-amy-medium.onnx) and its corresponding .json file into the tts_voices/ directory.

MediaPipe: Ensure the face_landmarker.task file is located in the root directory alongside your vision script.

Usage
The system is separated into discrete scripts to allow for modular execution and debugging.

1. Start the Background AI Service
Ensure the Ollama application is running in the background of your operating system.

2. Run the Vision and Tracking Module
This will initialize the webcam and begin streaming UDP coordinate data.

Bash
python trackingmp.py
3. Run the Conversational Audio Engine
This initiates the microphone listener, the Ollama chat loop, and the audio playback router.

Bash
python ollama_engine.py
Press Ctrl + C in either terminal to safely terminate the processes and release the hardware peripherals.

Network Protocol
The vision module broadcasts structural data over a local UDP socket. By default, it targets:

IP Address: 127.0.0.1 (Localhost)

Port: 5008

Payload Format: Comma-separated floating-point strings representing normalized X and Y coordinates (e.g., -0.15,0.42).
