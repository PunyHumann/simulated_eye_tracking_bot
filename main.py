import subprocess
import time
import keyboard
import sys

print("Starting Cube...")

mp_tracker = subprocess.Popen([sys.executable, "trackingmp.py"])
print("MediaPipe innitialized...")

time.sleep(2)

ollama_engine = subprocess.Popen([sys.executable, "ollama_engine.py"])
print("Ollama engine innitialized...")

