import os
import subprocess
import signal
import time
import sys

print("Starting Cube...")
print("Press ENTER to Exit...")

mp_tracker = subprocess.Popen(
    [sys.executable, "trackingmp.py"],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
print("MediaPipe innitialized...")
time.sleep(2)
ollama_engine = subprocess.Popen(
    [sys.executable, "ollama_engine.py"],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
print("Ollama engine innitialized...")

#Press 'enter' to exit
try:
    input()

except (KeyboardInterrupt, Exception):
    pass
    
os.kill(mp_tracker.pid, signal.CTRL_C_EVENT)
os.kill(ollama_engine.pid, signal.CTRL_C_EVENT)
mp_tracker.wait()
ollama_engine.wait()

print("Everything off...")