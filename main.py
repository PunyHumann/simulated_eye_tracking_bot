import os
import subprocess
import signal
import time
import sys

print("Starting Cube...")
print("Press Ctrl+C or cmd+C to Exit...")

mp_tracker = subprocess.Popen([sys.executable, "trackingmp.py"])
print("MediaPipe innitialized...")
time.sleep(2)
ollama_engine = subprocess.Popen([sys.executable, "ollama_engine.py"])
print("Ollama engine innitialized...")

#Press 'enter' to exit
try:
    while True:
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):   
    mp_tracker.terminate()
    ollama_engine.terminate()

    try:
        mp_tracker.wait(timeout=3)
    except subprocess.TimeoutExpired:
        print("mp tracker took to long, force kill...")
        mp_tracker.kill()
        
    try:
        ollama_engine.wait(timeout=3)
    except subprocess.TimeoutExpired:
        print("ollama took too long, force kill...")
        ollama_engine.kill()


print("Everything off...")